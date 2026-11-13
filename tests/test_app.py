"""Tests for the fully assembled agent: real tools and safety checks, with a
fake model and a fake embedding model in place of the paid services."""

from __future__ import annotations

import dataclasses

import pytest
from conftest import PRIYA, TODAY
from fakes import FakeProvider, text_response, tool_response

from support_agent.agent import COMPLETED, REPLY_BLOCKED, STEP_LIMIT
from support_agent.app import Resources, create_agent
from support_agent.config import Settings
from support_agent.providers.base import ToolCall


@pytest.fixture
def settings(monkeypatch, tmp_path) -> Settings:
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "bedrock")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.delenv("SUPPORT_AGENT_MODEL", raising=False)
    return dataclasses.replace(
        Settings.from_env(),
        max_steps=4,
        cache_dir=tmp_path,
        log_file=tmp_path / "logs" / "agent.jsonl",
    )


def build(settings, knowledge_base, orders, tickets, responses):
    provider = FakeProvider(responses)
    resources = Resources(provider, knowledge_base, orders, tickets)
    agent, session = create_agent(settings, resources, PRIYA, today=TODAY)
    return agent, session, provider


def test_a_normal_order_question_end_to_end(settings, knowledge_base, orders, tickets):
    agent, _, provider = build(
        settings,
        knowledge_base,
        orders,
        tickets,
        [
            tool_response(ToolCall("c1", "lookup_order", {"order_id": "JL-10231"})),
            tool_response(
                ToolCall("c2", "calculate_date", {"start_date": "2026-11-07", "add_days": 30})
            ),
            text_response(
                "Your order was delivered on 7 November 2026 and the total was $60.50. "
                "You can return it until 7 December 2026."
            ),
        ],
    )
    result = agent.run("Tell me about order JL-10231")

    assert result.outcome == COMPLETED
    assert "$60.50" in result.reply
    assert not result.escalated
    assert tickets.all() == []
    # The model was told today's date and given all four tools.
    assert "2026-11-12" in provider.requests[0]["system"]
    assert len(provider.requests[0]["tools"]) == 4


def test_a_made_up_price_is_blocked_and_a_ticket_is_created(settings, knowledge_base, orders, tickets):
    agent, session, _ = build(
        settings,
        knowledge_base,
        orders,
        tickets,
        [text_response("Express shipping costs $3.00.")],  # repeated on the rewrite too
    )
    result = agent.run("How much is express shipping?")

    assert result.outcome == REPLY_BLOCKED
    assert "$3.00" not in result.reply
    saved = tickets.all()
    assert len(saved) == 1
    assert saved[0]["ticket_id"] in result.reply
    assert saved[0]["customer_email"] == PRIYA
    assert "How much is express shipping?" in saved[0]["summary"]
    assert session.ticket_ids == [saved[0]["ticket_id"]]


def test_blocked_reply_reuses_the_ticket_the_model_already_created(
    settings, knowledge_base, orders, tickets
):
    agent, _, _ = build(
        settings,
        knowledge_base,
        orders,
        tickets,
        [
            tool_response(
                ToolCall(
                    "c1",
                    "escalate_to_human",
                    {"reason": "refund_request", "summary": "Wants a refund.", "order_id": "JL-10231"},
                )
            ),
            text_response("I've processed your refund."),
        ],
    )
    result = agent.run("Refund JL-10231 now")

    assert result.outcome == REPLY_BLOCKED
    saved = tickets.all()
    assert len(saved) == 1  # not two
    assert saved[0]["reason"] == "refund_request"
    assert saved[0]["ticket_id"] in result.reply


def test_running_out_of_steps_creates_a_ticket(settings, knowledge_base, orders, tickets):
    agent, _, _ = build(
        settings,
        knowledge_base,
        orders,
        tickets,
        [tool_response(ToolCall("c1", "search_knowledge_base", {"query": "returns"}))],
    )
    result = agent.run("Hello?")

    assert result.outcome == STEP_LIMIT
    assert len(tickets.all()) == 1
    assert "step limit" in tickets.all()[0]["summary"]


def test_another_customers_order_stays_hidden_end_to_end(settings, knowledge_base, orders, tickets):
    agent, _, provider = build(
        settings,
        knowledge_base,
        orders,
        tickets,
        [
            tool_response(ToolCall("c1", "lookup_order", {"order_id": "JL-10240"})),
            text_response("I can't find that order on this account."),
        ],
    )
    agent.run("What's in order JL-10240?")

    tool_result = provider.requests[1]["messages"][2]["content"][0]["content"]
    assert "No order JL-10240 was found" in tool_result
    assert "Earbuds" not in tool_result
