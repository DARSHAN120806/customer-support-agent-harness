"""Tests for the rule: a shop question the documents cannot answer must end
with a ticket, even if the model only offers one."""

from __future__ import annotations

import pytest
from fakes import FakeProvider, text_response, tool_response

from support_agent.agent import COMPLETED, Agent
from support_agent.prompts import SUPPORT_EMAIL
from support_agent.providers.base import ToolCall
from support_agent.safety import check_reply, collect_sources, is_unanswered_shop_question

ALLOWED = {"priya.nair@example.com", SUPPORT_EMAIL}
SEARCHED = ["search_knowledge_base"]


@pytest.mark.parametrize(
    "reply",
    [
        "I don't have information about gift wrapping in our shop documents.",
        "I do not have any details on that. Would you like me to create a ticket?",
        "I couldn't find anything about engraving options.",
        "Gift wrapping isn't mentioned in our documents.",
        "I'm not able to say whether we offer it or not.",
        "I'm not sure whether that is covered.",
    ],
)
def test_replies_that_admit_the_documents_have_no_answer_are_recognised(reply):
    assert is_unanswered_shop_question(reply, SEARCHED)


@pytest.mark.parametrize(
    "reply",
    [
        "You can return most items within 30 days of delivery.",
        "We accept Visa, Mastercard, American Express and PayPal.",
        "I can't find that order on this account.",
        "Would you like me to hand this over to the team to start a return?",
    ],
)
def test_replies_that_answer_the_question_are_left_alone(reply):
    assert not is_unanswered_shop_question(reply, SEARCHED)


def test_unrelated_requests_are_not_ticketed():
    # No search was run, which is how a request about the weather looks.
    assert not is_unanswered_shop_question("I don't have information about the weather.", [])


def test_nothing_to_do_when_the_model_already_handed_over():
    tools_used = ["search_knowledge_base", "escalate_to_human"]

    assert not is_unanswered_shop_question("I don't have information about that.", tools_used)


# --- The agent loop ------------------------------------------------------------------


class Recorder:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def __call__(self, why: str, customer_message: str, already_escalated: bool) -> str:
        self.calls.append((why, customer_message))
        return "TCK-AUTO-1"


def make_agent(provider, registry, recorder) -> Agent:
    return Agent(
        provider,
        registry,
        system_prompt="test",
        max_steps=6,
        reply_check=lambda reply, messages, tools_used: check_reply(
            reply, ALLOWED, collect_sources(messages), tools_used
        ),
        auto_escalate=recorder,
    )


SEARCH = tool_response(ToolCall("c1", "search_knowledge_base", {"query": "gift wrapping"}))
OFFER = text_response(
    "I don't have information about gift wrapping. Would you like me to create a ticket?"
)


def test_model_is_told_to_create_the_ticket_and_does(registry, tickets):
    provider = FakeProvider(
        [
            SEARCH,
            OFFER,
            tool_response(
                ToolCall(
                    "c2",
                    "escalate_to_human",
                    {"reason": "outside_shop_documents", "summary": "Asks about gift wrapping."},
                )
            ),
            text_response("I couldn't find anything about gift wrapping, so I've asked the team."),
        ]
    )
    recorder = Recorder()
    result = make_agent(provider, registry, recorder).run("Do you offer gift wrapping?")

    assert result.outcome == COMPLETED
    assert result.escalated
    assert "Would you like me to" not in result.reply
    assert recorder.calls == []  # the model created the ticket itself
    assert len(tickets.all()) == 1
    assert "escalate_to_human" in provider.requests[2]["system"]


def test_harness_creates_the_ticket_when_the_model_still_only_offers(registry):
    provider = FakeProvider([SEARCH, OFFER])  # the offer is repeated on the rewrite
    recorder = Recorder()
    history: list = []
    result = make_agent(provider, registry, recorder).run("Do you offer gift wrapping?", history)

    assert result.outcome == COMPLETED  # the reply is shown, not replaced
    assert result.reply.startswith("I don't have information about gift wrapping.")
    assert "TCK-AUTO-1" in result.reply
    assert result.auto_ticket_id == "TCK-AUTO-1"
    assert result.escalated
    assert result.violations == ["handover_missing"]
    assert recorder.calls[0][1] == "Do you offer gift wrapping?"
    # The conversation history shows the customer was given the ticket number.
    assert "TCK-AUTO-1" in history[-1]["content"]


def test_an_answered_question_gets_no_ticket(registry):
    provider = FakeProvider(
        [
            tool_response(ToolCall("c1", "search_knowledge_base", {"query": "return window"})),
            text_response("You can return most items within 30 days of delivery."),
        ]
    )
    recorder = Recorder()
    result = make_agent(provider, registry, recorder).run("How long is the return window?")

    assert not result.escalated
    assert recorder.calls == []


def test_declining_an_unrelated_request_gets_no_ticket(registry):
    provider = FakeProvider([text_response("I don't have information about the weather.")])
    recorder = Recorder()
    result = make_agent(provider, registry, recorder).run("What's the weather?")

    assert not result.escalated
    assert len(provider.requests) == 1
