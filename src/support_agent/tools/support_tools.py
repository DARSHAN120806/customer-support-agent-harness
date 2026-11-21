"""The tools of the support agent.

    search_knowledge_base   look something up in the shop's documents
    lookup_order            read one of the current customer's orders
    calculate_date          work out a deadline, such as when a warranty ends
    escalate_to_human       hand the conversation to the human support team
    request_refund_or_return  start a refund, return or cancellation (refund_tool.py)

No tool changes the shop's data. request_refund_or_return only writes a request
record, and the decision is made by plain code (refund_rules.py), never by the
AI. There are no address changes and nothing moves money.
"""

from __future__ import annotations

import calendar
import json
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

from .. import event_log
from ..event_log import EventLogger, NullLogger
from ..knowledge_base import KnowledgeBase
from ..orders import OrderStore, normalize_email, normalize_order_id
from ..prompts import SUPPORT_EMAIL
from ..refund_requests import RefundRequestStore
from ..retry import RetryPolicy, ServiceError, call_with_retry
from ..tickets import ESCALATION_REASONS, TicketError, TicketStore
from .refund_tool import make_refund_tool
from .registry import Tool, ToolError, ToolRegistry, require_text

# More tickets than this in one conversation means something is going wrong.
MAX_TICKETS_PER_CONVERSATION = 5


@dataclass
class SessionContext:
    """Facts about the current conversation that the harness knows for certain.

    `customer_email` is the email the customer is signed in with. It comes from
    the harness, never from what the customer types in the chat, so a customer
    cannot gain access to another person's orders by claiming to be them.
    """

    customer_email: str
    ticket_ids: list[str] = field(default_factory=list)
    # Tickets already created in this conversation, by (reason, order ID), so the
    # same issue is not sent to the support team twice.
    tickets_by_issue: dict[tuple[str, str | None], str] = field(default_factory=dict)
    # Where this conversation's events are recorded.
    logger: EventLogger | NullLogger = field(default_factory=NullLogger)
    # How often, and how patiently, failed calls are tried again.
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    # Refund and return requests made in this conversation.
    refund_request_ids: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.customer_email = normalize_email(self.customer_email)


def create_ticket(
    session: SessionContext,
    tickets: TicketStore,
    *,
    reason: str,
    summary: str,
    order_id: str | None,
    created_by: str,
) -> str:
    """Create a ticket, remember it for this conversation, and log it. Every
    ticket goes through here, whether the model or the harness asked for it."""
    try:
        # A ticket file that is briefly locked is tried again after a short wait.
        ticket = call_with_retry(
            lambda: tickets.create(
                customer_email=session.customer_email,
                reason=reason,
                summary=summary,
                order_id=order_id,
                conversation_id=session.logger.conversation_id or None,
            ),
            session.retry_policy,
            on_retry=event_log.retry_recorder(session.logger, "ticket_write"),
        )
    except TicketError as error:
        event_log.log_error(session.logger, "ticket_write", error, reason=reason)
        raise
    session.ticket_ids.append(ticket["ticket_id"])
    session.tickets_by_issue[(reason, order_id)] = ticket["ticket_id"]
    session.logger.log(
        event_log.TICKET_CREATED,
        ticket_id=ticket["ticket_id"],
        reason=reason,
        order_id=order_id,
        created_by=created_by,  # "model" or "harness"
        summary=summary,
    )
    return ticket["ticket_id"]


def build_tool_registry(
    session: SessionContext,
    knowledge_base: KnowledgeBase,
    orders: OrderStore,
    tickets: TicketStore,
    today: date | None = None,
    refund_requests: RefundRequestStore | None = None,
) -> ToolRegistry:
    today = today or date.today()
    # Requests are kept next to the tickets unless a file is given.
    requests = refund_requests or RefundRequestStore(tickets.path.parent / "refund_requests.jsonl")
    registry = ToolRegistry()
    registry.register(make_search_tool(session, knowledge_base))
    registry.register(make_order_tool(session, orders))
    registry.register(make_date_tool(today))
    registry.register(make_escalation_tool(session, tickets))
    registry.register(make_refund_tool(session, orders, tickets, requests, today, create_ticket))
    return registry


def make_search_tool(session: SessionContext, knowledge_base: KnowledgeBase) -> Tool:
    def search(tool_input: dict[str, Any]) -> str:
        query = require_text(tool_input, "query", max_length=500)
        try:
            hits = call_with_retry(
                lambda: knowledge_base.search(query),
                session.retry_policy,
                on_retry=event_log.retry_recorder(session.logger, "embedding"),
            )
        except ServiceError as error:
            event_log.log_error(session.logger, "embedding", error)
            # The model must not answer from memory when the search is down.
            raise ToolError(
                "The document search is temporarily unavailable, so the shop's documents "
                "could not be checked. Do not answer from memory. Hand over with "
                "escalate_to_human (reason unsure_of_answer)."
            ) from error
        if not hits:
            return "No relevant information was found in the shop's documents for this query."
        return "\n\n".join(
            f'Result {number} (from {hit.chunk.source}, section "{hit.chunk.section}"):\n'
            f"{hit.chunk.text}"
            for number, hit in enumerate(hits, start=1)
        )

    return Tool(
        name="search_knowledge_base",
        description=(
            "Search the shop's official documents: shipping, returns, refunds and "
            "warranty policies, the FAQ, and the company overview with the product "
            "catalogue and prices. Use this before answering any question about "
            "policies, prices, products, or how the shop works. Returns the most "
            "relevant sections, or a message saying nothing relevant was found. "
            "Search for one topic at a time, phrased as a short question."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "What to look for, e.g. 'How long do refunds take?'",
                }
            },
            "required": ["query"],
            "additionalProperties": False,
        },
        handler=search,
    )


def make_order_tool(session: SessionContext, orders: OrderStore) -> Tool:
    def lookup(tool_input: dict[str, Any]) -> str:
        raw_order_id = require_text(tool_input, "order_id", max_length=40)
        order_id = normalize_order_id(raw_order_id)
        if order_id is None:
            raise ToolError(
                "That is not a valid order ID. Order IDs look like JL-10231 "
                "(JL- followed by five digits). Ask the customer to check it."
            )
        order = orders.get_order_for_customer(order_id, session.customer_email)
        if order is None:
            # The same message is used whether the order does not exist or
            # belongs to another customer, so nothing about other customers leaks.
            return (
                f"No order {order_id} was found for the signed-in customer. "
                "Either the order ID is wrong, or the order was placed with a "
                "different email address. No details can be shared."
            )
        return json.dumps(order, indent=2)

    return Tool(
        name="lookup_order",
        description=(
            "Look up one order by its order ID. Returns the status, items, prices, "
            "shipping and tracking details, and delivery dates, plus every record "
            "linked to that order: refunds and refund disputes, returns, warranty "
            "claims, carrier investigations, damaged-package reports, address change "
            "requests, and past support tickets. Use it whenever the customer asks "
            "about the progress of any of these, such as 'where is my refund?' or "
            "'what happened to my warranty claim?'; ask for the order ID if you don't "
            "have it. It only returns orders that belong to the customer who is "
            "signed in to this chat; the check is done automatically, so you do not "
            "pass an email address."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID given by the customer, e.g. 'JL-10231'.",
                }
            },
            "required": ["order_id"],
            "additionalProperties": False,
        },
        handler=lookup,
    )


def add_to_date(start: date, days: int = 0, months: int = 0, years: int = 0) -> date:
    """Add calendar months and years, then days. When the target month is
    shorter (31 January plus 1 month), the last day of that month is used."""
    month_index = start.month - 1 + months + 12 * years
    year, month = start.year + month_index // 12, month_index % 12 + 1
    day = min(start.day, calendar.monthrange(year, month)[1])
    return date(year, month, day) + timedelta(days=days)


def make_date_tool(today: date) -> Tool:
    def read_whole_number(tool_input: dict[str, Any], name: str) -> int:
        value = tool_input.get(name, 0)
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 3650:
            raise ToolError(f"'{name}' must be a whole number between 0 and 3650.")
        return value

    def calculate(tool_input: dict[str, Any]) -> str:
        raw_start = require_text(tool_input, "start_date", max_length=20)
        try:
            start = date.fromisoformat(raw_start)
        except ValueError:
            raise ToolError("'start_date' must be a real date written as YYYY-MM-DD.") from None
        days = read_whole_number(tool_input, "add_days")
        months = read_whole_number(tool_input, "add_months")
        years = read_whole_number(tool_input, "add_years")

        result = add_to_date(start, days, months, years)
        added = ", ".join(
            f"{amount} {unit}{'' if amount == 1 else 's'}"
            for amount, unit in ((years, "year"), (months, "month"), (days, "day"))
            if amount
        )
        difference = (result - today).days
        if difference > 0:
            compared = f"That is {difference} day{'' if difference == 1 else 's'} from today, so it has not passed yet."
        elif difference < 0:
            compared = f"That was {-difference} day{'' if difference == -1 else 's'} ago, so it has already passed."
        else:
            compared = "That is today."
        return (
            f"{start.isoformat()} plus {added or 'nothing'} is {result.isoformat()} "
            f"({result:%A} {result.day} {result:%B %Y}). Today is {today.isoformat()}. {compared}"
        )

    return Tool(
        name="calculate_date",
        description=(
            "Add days, months, or years to a date and compare the result with today. "
            "Use this for every deadline you mention: when a return window closes, "
            "when a warranty runs out, or whether a date has already passed. Take the "
            "start date from the order and the length of the period from the policy. "
            "Working dates out without this tool is a common source of mistakes."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "The date to start from, as YYYY-MM-DD, e.g. a delivery date.",
                },
                "add_days": {"type": "integer", "description": "Days to add. Default 0."},
                "add_months": {"type": "integer", "description": "Months to add. Default 0."},
                "add_years": {"type": "integer", "description": "Years to add. Default 0."},
            },
            "required": ["start_date"],
            "additionalProperties": False,
        },
        handler=calculate,
    )


def make_escalation_tool(session: SessionContext, tickets: TicketStore) -> Tool:
    def escalate(tool_input: dict[str, Any]) -> str:
        reason = require_text(tool_input, "reason", max_length=40)
        if reason not in ESCALATION_REASONS:
            raise ToolError(f"'reason' must be one of: {', '.join(ESCALATION_REASONS)}.")
        summary = require_text(tool_input, "summary", max_length=1500)

        order_id = None
        raw_order_id = tool_input.get("order_id")
        if isinstance(raw_order_id, str) and raw_order_id.strip():
            order_id = normalize_order_id(raw_order_id)
            if order_id is None:
                raise ToolError("'order_id' is not a valid order ID. Leave it out if unsure.")

        existing = session.tickets_by_issue.get((reason, order_id))
        if existing:
            return (
                f"Ticket {existing} already covers this issue in this conversation. "
                "No new ticket was created. Give the customer this ticket number."
            )
        if len(session.ticket_ids) >= MAX_TICKETS_PER_CONVERSATION:
            raise ToolError(
                "The limit of tickets for one conversation has been reached. Refer the "
                f"customer to their existing ticket numbers: {', '.join(session.ticket_ids)}."
            )

        try:
            ticket_id = create_ticket(
                session,
                tickets,
                reason=reason,
                summary=summary,
                order_id=order_id,
                created_by="model",
            )
        except TicketError as error:
            raise ToolError(
                "The ticket could not be saved, so no ticket exists. Apologise, do not "
                f"give a ticket number, and ask the customer to email {SUPPORT_EMAIL}."
            ) from error
        return (
            f"Ticket {ticket_id} was created for the human support team. "
            "Give the customer this ticket number."
        )

    return Tool(
        name="escalate_to_human",
        description=(
            "Hand this conversation to the human support team by creating a ticket. "
            "Use this for anything you cannot complete or answer yourself. The "
            "support team reads only the ticket, not this chat, so the summary must "
            "stand on its own. Returns the ticket number to give to the customer."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "enum": ESCALATION_REASONS,
                    "description": "The main reason for handing over.",
                },
                "summary": {
                    "type": "string",
                    "description": (
                        "What the customer wants, what you already found out or told "
                        "them, and what the support team needs to do next."
                    ),
                },
                "order_id": {
                    "type": "string",
                    "description": "The order this is about, if there is one.",
                },
            },
            "required": ["reason", "summary"],
            "additionalProperties": False,
        },
        handler=escalate,
        read_only=False,
    )
