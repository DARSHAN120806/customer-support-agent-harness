"""Tests for the two gaps found in the harness on/off comparison (20 Nov 2026):

1. ``refund-demand-now``: the agent said "I need to create a ticket" but never did.
   New rule ``promised_ticket_missing``: one reminder, then the harness creates it.
2. ``tricky-price-match``: the agent dodged a policy question without stating any
   policy, so ``unverified_policy`` did not fire. The rule now also fires when the
   customer's question is about policy and nothing has been looked up.
"""

from __future__ import annotations

import dataclasses

import pytest
from conftest import PRIYA, TODAY
from fakes import FakeProvider, text_response, tool_response

from support_agent.agent import COMPLETED
from support_agent.app import Resources, create_agent
from support_agent.config import Settings
from support_agent.event_log import read_events
from support_agent.providers.base import ToolCall
from support_agent.safety import asks_about_policy, check_reply, promises_ticket

# --- 1. A promised ticket must exist -------------------------------------------------

# The reply the real model gave in the harness-on run.
REFUND_PROMISE = (
    "I understand you'd like a refund for order JL-10231. I'm not able to issue refunds "
    "myself, so I need to create a ticket for our support team to handle this."
)


@pytest.mark.parametrize(
    "reply",
    [
        REFUND_PROMISE,
        "I'll create a ticket for our support team right away.",
        "I'm creating a ticket now so the team can help.",
        "Let me create a support ticket for you.",
        "I've raised a ticket with the team.",
        "I'll pass this on to our support team.",
        "I'm handing this over to the human support team.",
        "Let me escalate this to the support team.",
    ],
)
def test_replies_that_promise_a_ticket_are_recognised(reply):
    assert promises_ticket(reply)


@pytest.mark.parametrize(
    "reply",
    [
        "Would you like me to create a ticket for you?",  # an offer, not a promise
        "Shall I pass this on to our support team?",
        "If you'd like, I can create a ticket.",
        "The support team reviews every refund request.",
        "Your ticket number is TCK-20261120-ABC123.",
        "Contact support and they will open a case.",
        "I can't create discount codes.",
    ],
)
def test_offers_and_plain_statements_are_not_promises(reply):
    assert not promises_ticket(reply)


def promise_rules(reply=REFUND_PROMISE, **overrides) -> list[str]:
    details = {
        "tools_used": [],
        "shop_text": "Refunds go to the original payment method.",
        "customer_message": "Get me a human now.",
        "has_ticket": False,
    } | overrides
    return [v.rule for v in check_reply(reply, {PRIYA}, **details)]


def test_a_promise_without_a_ticket_breaks_the_rule():
    assert promise_rules() == ["promised_ticket_missing"]


def test_no_rule_broken_once_a_ticket_exists():
    assert promise_rules(tools_used=["escalate_to_human"]) == []
    assert promise_rules(has_ticket=True) == []
    assert check_reply(REFUND_PROMISE, {PRIYA}) == []  # a reply checked on its own


def test_the_promise_rule_does_not_block_the_reply():
    (violation,) = check_reply(
        REFUND_PROMISE, {PRIYA}, tools_used=[], shop_text="x", customer_message="Hi", has_ticket=False
    )
    assert violation.correctable and not violation.blocks_reply
    assert "escalate_to_human" in violation.fix_hint


# --- 2. A policy question needs a look-up, even if the reply dodges it ---------------

PRICE_MATCH_QUESTION = "Amazon has the same kettle cheaper. Will you match their price?"
# A reply like the real one: no policy statement, just a question back.
DODGE = "Thanks for letting me know! Could you tell me which kettle you're looking at?"


@pytest.mark.parametrize(
    "message",
    [PRICE_MATCH_QUESTION, "Refund order JL-10231 to my Visa right now.", "How long does shipping take?"],
)
def test_policy_questions_are_recognised(message):
    assert asks_about_policy(message)


@pytest.mark.parametrize(
    "message", ["Where's my order?", "Who are you?", "Write me a poem about the weather in Sydney."]
)
def test_other_messages_are_not_policy_questions(message):
    assert not asks_about_policy(message)


def policy_rules(reply=DODGE, **overrides) -> list[str]:
    details = {"tools_used": [], "shop_text": "", "customer_message": PRICE_MATCH_QUESTION} | overrides
    return [v.rule for v in check_reply(reply, {PRIYA}, **details)]


def test_a_dodged_policy_question_with_nothing_looked_up_breaks_the_rule():
    assert policy_rules() == ["unverified_policy"]


def test_no_rule_broken_when_something_was_looked_up_or_the_question_is_not_about_policy():
    assert policy_rules(shop_text="## Do you price match?\nNo.") == []
    assert policy_rules(customer_message="Who are you?") == []


# --- The whole agent -----------------------------------------------------------------


@pytest.fixture
def settings(monkeypatch, tmp_path) -> Settings:
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "bedrock")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    for name in ("SUPPORT_AGENT_MODEL", "SUPPORT_AGENT_LOG_FILE"):
        monkeypatch.delenv(name, raising=False)
    return dataclasses.replace(
        Settings.from_env(), max_steps=6, cache_dir=tmp_path, log_file=tmp_path / "logs" / "agent.jsonl"
    )


def run(settings, knowledge_base, orders, tickets, responses, messages):
    provider = FakeProvider(responses)
    agent, _ = create_agent(settings, Resources(provider, knowledge_base, orders, tickets), PRIYA, today=TODAY)
    history: list = []
    results = [agent.run(message, history) for message in messages]
    return results, provider, list(read_events(settings.log_file))


HUMAN_PLEASE = "Get me a human now."
PROMISE = text_response("I'll pass this on to our support team.")


def test_the_model_creates_the_promised_ticket_after_one_reminder(settings, knowledge_base, orders, tickets):
    escalate = tool_response(
        ToolCall("c1", "escalate_to_human", {"reason": "human_requested", "summary": "Asked for a person."}),
        text="I've passed this on to our support team.",
    )
    (result,), provider, _ = run(
        settings, knowledge_base, orders, tickets, [PROMISE, escalate, text_response("They'll reply by email.")],
        [HUMAN_PLEASE],
    )

    assert result.outcome == COMPLETED and result.escalated and result.auto_ticket_id is None
    assert len(tickets.all()) == 1
    assert "Call escalate_to_human now" in provider.requests[1]["system"]


def test_the_harness_creates_the_ticket_if_the_model_only_promises_it(settings, knowledge_base, orders, tickets):
    (result,), _, events = run(settings, knowledge_base, orders, tickets, [PROMISE], [HUMAN_PLEASE])

    assert result.outcome == COMPLETED
    assert result.reply.startswith("I'll pass this on to our support team.")
    (ticket,) = tickets.all()
    assert result.auto_ticket_id == ticket["ticket_id"] and ticket["ticket_id"] in result.reply
    assert result.violations == ["promised_ticket_missing"]
    assert [e["created_by"] for e in events if e["event"] == "ticket_created"] == ["harness"]


def test_refund_demand_now_ends_with_a_real_ticket(settings, knowledge_base, orders, tickets):
    # The real failure: a policy subject, nothing looked up, and a promise with no ticket.
    promise = text_response(REFUND_PROMISE)
    (result,), provider, _ = run(
        settings, knowledge_base, orders, tickets, [promise, promise],
        ["Refund order JL-10231 to my Visa right now. Don't send me to anyone else, just do it."],
    )

    assert result.outcome == COMPLETED
    assert "search_knowledge_base" in result.tools_used  # searched by the harness
    (ticket,) = tickets.all()
    assert ticket["ticket_id"] in result.reply
    # Both rules were raised on the first draft.
    assert "Call escalate_to_human now" in provider.requests[1]["system"]
    assert "Answer only from those results" in provider.requests[1]["system"]


def test_a_dodged_price_match_question_is_answered_from_the_documents(settings, knowledge_base, orders, tickets):
    good = "We don't match competitors' prices, I'm afraid."
    (result,), provider, events = run(
        settings, knowledge_base, orders, tickets, [text_response(DODGE), text_response(good)],
        [PRICE_MATCH_QUESTION],
    )

    assert result.outcome == COMPLETED and result.reply == good
    assert result.tools_used == ["search_knowledge_base"]  # run by the harness
    tool_result = provider.requests[1]["messages"][2]["content"][0]
    assert "We do not match competitors' prices" in tool_result["content"]
    assert [e["rules"] for e in events if e["event"] == "reply_rewrite"] == [["unverified_policy"]]


def test_a_question_that_is_not_about_policy_is_left_alone(settings, knowledge_base, orders, tickets):
    reply = "I'm the Juniper Lane Goods virtual assistant. How can I help?"
    (result,), provider, _ = run(settings, knowledge_base, orders, tickets, [text_response(reply)], ["Who are you?"])

    assert result.outcome == COMPLETED and result.reply == reply
    assert len(provider.requests) == 1 and tickets.all() == []
