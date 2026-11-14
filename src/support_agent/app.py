"""Puts the pieces together: settings, model provider, data, tools, and agent.

The terminal chat, the evaluation script, and the tests all build the agent
through this module, so they are guaranteed to use the same setup.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from . import event_log
from .agent import Agent
from .config import ConfigError, Settings
from .embeddings import TitanEmbedder
from .knowledge_base import KnowledgeBase
from .orders import OrderStore
from .prompts import SUPPORT_EMAIL, build_system_prompt
from .providers import ModelProvider, create_provider
from .retry import RetryPolicy
from .safety import Budget, check_reply, collect_sources, collect_tool_results
from .tickets import TicketStore
from .tools import SessionContext, build_tool_registry, create_ticket


@dataclass
class Resources:
    """The parts that are loaded once and shared by every conversation."""

    provider: ModelProvider
    knowledge_base: KnowledgeBase
    orders: OrderStore
    tickets: TicketStore


def load_resources(settings: Settings) -> Resources:
    if not settings.aws_region:
        raise ConfigError(
            "AWS_REGION is not set. The knowledge base search uses Amazon Titan "
            "embeddings through Bedrock, so it needs AWS_REGION and AWS sign-in details."
        )
    embedder = TitanEmbedder(
        settings.aws_region, settings.embedding_model, settings.request_timeout_seconds
    )
    # Problems with the shop's own data files are reported in plain words
    # instead of as a Python error trace.
    try:
        knowledge_base = KnowledgeBase.build(
            settings.knowledge_base_dir,
            embedder,
            cache_path=settings.cache_dir / "knowledge_base_embeddings.json",
            retry_policy=RetryPolicy(max_attempts=settings.max_attempts),
        )
    except (OSError, ValueError) as error:
        raise ConfigError(
            f"The shop documents in {settings.knowledge_base_dir} could not be loaded: {error}"
        ) from error
    try:
        orders = OrderStore(settings.orders_file)
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise ConfigError(
            f"The orders file {settings.orders_file} is missing or damaged "
            f"({type(error).__name__}: {error})."
        ) from error
    return Resources(
        provider=create_provider(settings),
        knowledge_base=knowledge_base,
        orders=orders,
        tickets=TicketStore(settings.tickets_file),
    )


def create_agent(
    settings: Settings,
    resources: Resources,
    customer_email: str,
    today: date | None = None,
    retry_policy: RetryPolicy | None = None,
) -> tuple[Agent, SessionContext]:
    """Create an agent for one conversation with one signed-in customer."""
    today = today or date.today()
    retry_policy = retry_policy or RetryPolicy(max_attempts=settings.max_attempts)
    session = SessionContext(customer_email=customer_email, retry_policy=retry_policy)
    # The log identifies the customer by a code, never by their email.
    salt = event_log.load_or_create_salt(settings.log_file.parent / ".salt")
    session.logger = event_log.EventLogger(
        settings.log_file,
        conversation_id=event_log.new_conversation_id(),
        customer_ref=event_log.customer_ref(session.customer_email, salt),
    )
    session.logger.log(
        event_log.CONVERSATION_START,
        provider=settings.provider,
        model=settings.model,
        max_steps=settings.max_steps,
        date_used=today.isoformat(),
    )
    tools = build_tool_registry(
        session, resources.knowledge_base, resources.orders, resources.tickets, today
    )

    def auto_escalate(why: str, customer_message: str, already_escalated: bool) -> str:
        """Make sure a ticket exists when the agent could not finish safely."""
        if already_escalated and session.ticket_ids:
            # The model created a ticket for this message before the reply was
            # stopped, so the customer is pointed to that one, not a second one.
            return session.ticket_ids[-1]
        return create_ticket(
            session,
            resources.tickets,
            reason="other",
            summary=f"Automatic hand-over: {why}. Customer's message: {customer_message[:1000]}",
            order_id=None,
            created_by="harness",
        )

    agent = Agent(
        provider=resources.provider,
        tools=tools,
        system_prompt=build_system_prompt(today),
        max_steps=settings.max_steps,
        budget=Budget(
            max_tokens_per_message=settings.max_tokens_per_message,
            max_cost_per_conversation_usd=settings.max_cost_per_conversation_usd,
            input_price_per_million_tokens=settings.input_price_per_million_tokens,
            output_price_per_million_tokens=settings.output_price_per_million_tokens,
        ),
        # The only email addresses a reply may contain are the customer's own and
        # the shop's support address, and every price, time period, or date in it
        # must come from a tool result, the customer's own messages, or be today.
        # A shop question the documents could not answer must end with a ticket.
        reply_check=lambda reply, messages, tools_used: check_reply(
            reply,
            {session.customer_email, SUPPORT_EMAIL},
            collect_sources(messages) + f"\n{today.isoformat()}",
            tools_used,
            # The assistant must not name the AI model or company behind it.
            shop_text=collect_tool_results(messages),
        ),
        auto_escalate=auto_escalate,
        logger=session.logger,
        retry_policy=retry_policy,
    )
    return agent, session
