"""Tests for the problems found on 21 Nov 2026 when the owner tested a warranty
claim as Priya and then tried to answer it as the admin:

- the assistant worked out a correct warranty date in its head ("18 September
  2027"), the figure check blocked it, and Priya got the generic fallback;
- the API on port 8000 answered "Not Found" to a browser.
"""

from __future__ import annotations

import pytest
from fakes import FakeProvider, text_response, tool_response
from test_safety import Recorder, make_agent

from support_agent.agent import COMPLETED, REPLY_BLOCKED
from support_agent.providers.base import ToolCall
from support_agent.safety import date_worked_out_in_head

SOURCES = '{"order_id": "JL-10198", "delivered_on": "2026-09-18"}\n| Electronics | 1 year |\nReturn within 30 days.'


@pytest.mark.parametrize(
    ("reply", "call"),
    [
        ("Your warranty runs until 18 September 2027.", {"start_date": "2026-09-18", "add_years": 1}),
        ("It ends on 2027-09-18.", {"start_date": "2026-09-18", "add_years": 1}),
        ("The return window closed on 18 October 2026.", {"start_date": "2026-09-18", "add_days": 30}),
    ],
)
def test_a_date_worked_out_correctly_is_checked_with_the_date_tool(reply, call):
    assert date_worked_out_in_head(reply, SOURCES) == ("calculate_date", call)


@pytest.mark.parametrize(
    "reply",
    [
        "Your warranty runs until 20 September 2027.",  # a wrong date gets no help
        "Your warranty runs until 18 September 2028.",  # 2 years is not in the sources
        "Your order was delivered on 18 September 2026.",  # already a source date
    ],
)
def test_a_wrong_or_known_date_gets_no_tool_call(reply):
    assert date_worked_out_in_head(reply, SOURCES) is None


def test_the_warranty_answer_reaches_the_customer_instead_of_the_fallback(registry):
    # The owner's test: the assistant looks the order up, then writes the right
    # warranty end date without the date tool, twice. Before the fix the reply
    # was blocked; now the harness confirms the date with calculate_date first.
    answer = "Your speaker is still under warranty until 18 September 2027. I have passed this to our team."
    provider = FakeProvider([
        tool_response(ToolCall("c1", "lookup_order", {"order_id": "JL-10198"})),
        tool_response(ToolCall("c2", "search_knowledge_base", {"query": "warranty length electronics"})),
        text_response(answer),
        text_response(answer),
    ])
    result = make_agent(provider, registry, Recorder()).run("I want to claim the warranty on my speaker from JL-10198")

    assert result.outcome == COMPLETED and "18 September 2027" in result.reply
    assert "calculate_date" in result.tools_used


def test_a_wrong_date_is_still_blocked(registry):
    wrong = "Your speaker is under warranty until 20 September 2027."
    provider = FakeProvider([
        tool_response(ToolCall("c1", "lookup_order", {"order_id": "JL-10198"})),
        tool_response(ToolCall("c2", "search_knowledge_base", {"query": "warranty length electronics"})),
        text_response(wrong),
        text_response(wrong),
    ])
    result = make_agent(provider, registry, Recorder()).run("Warranty on JL-10198?")

    assert result.outcome == REPLY_BLOCKED and "20 September 2027" not in result.reply


def test_the_api_sends_a_browser_to_the_website(monkeypatch, tmp_path, knowledge_base, orders):
    import dataclasses

    from fastapi.testclient import TestClient

    from support_agent.app import Resources
    from support_agent.config import Settings
    from support_agent.tickets import TicketStore
    from support_agent.web.accounts import AccountStore
    from support_agent.web.api import create_app

    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "bedrock")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    settings = dataclasses.replace(
        Settings.from_env(), cache_dir=tmp_path, log_file=tmp_path / "agent.jsonl",
        model_settings_file=tmp_path / "private" / "model_settings.json",
    )
    resources = Resources(FakeProvider([]), knowledge_base, orders, TicketStore(tmp_path / "tickets.jsonl"))
    client = TestClient(create_app(settings, resources, accounts=AccountStore([])), follow_redirects=False)

    assert client.get("/").headers["location"] == "http://localhost:5173"
    for path in ("/dashboard", "/admin"):
        response = client.get(path)
        assert response.status_code in (302, 307) and response.headers["location"] == "http://localhost:5173/#/dashboard"
