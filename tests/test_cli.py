"""Tests for the terminal chat. The model is a fake and the typed lines are
scripted, so these tests are free and need no keys."""

from __future__ import annotations

import pytest
from conftest import PRIYA
from fakes import FakeProvider, text_response, tool_response

from support_agent import cli
from support_agent.app import Resources
from support_agent.config import ConfigError
from support_agent.event_log import read_events
from support_agent.prompts import fallback_reply
from support_agent.providers.base import ToolCall
from support_agent.retry import ServiceError


@pytest.fixture
def environment(monkeypatch, tmp_path):
    """Settings for a test chat. The real .env file is never read."""
    monkeypatch.setattr(cli, "load_dotenv", lambda *args, **kwargs: None)
    for name in ("SUPPORT_AGENT_MODEL", "ANTHROPIC_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "bedrock")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setenv("SUPPORT_AGENT_LOG_FILE", str(tmp_path / "logs" / "agent.jsonl"))
    monkeypatch.setenv("SUPPORT_AGENT_TICKETS_FILE", str(tmp_path / "tickets" / "tickets.jsonl"))
    return tmp_path


def use_fake_model(monkeypatch, knowledge_base, orders, responses) -> FakeProvider:
    provider = FakeProvider(responses)

    def fake_resources(settings):
        from support_agent.tickets import TicketStore

        return Resources(provider, knowledge_base, orders, TicketStore(settings.tickets_file))

    monkeypatch.setattr(cli, "load_resources", fake_resources)
    return provider


def type_lines(monkeypatch, *lines: str) -> None:
    """Act as the person at the keyboard. After the last line, the terminal closes."""
    queue = list(lines)

    def fake_input(prompt=""):
        if not queue:
            raise EOFError
        return queue.pop(0)

    monkeypatch.setattr("builtins.input", fake_input)


def test_a_chat_shows_each_reply_and_what_was_used(
    environment, monkeypatch, capsys, knowledge_base, orders
):
    use_fake_model(
        monkeypatch,
        knowledge_base,
        orders,
        [
            tool_response(ToolCall("c1", "lookup_order", {"order_id": "JL-10231"})),
            text_response("It was delivered on 2026-11-07."),
        ],
    )
    type_lines(monkeypatch, "Where is JL-10231?", "quit")

    assert cli.main(["--email", PRIYA]) == 0

    out = capsys.readouterr().out
    assert f"Signed in as {PRIYA}." in out
    assert "Agent: It was delivered on 2026-11-07." in out
    assert "[completed, 2 step(s), used: lookup_order," in out
    # The chat is logged to the file named in the settings.
    events = list(read_events(environment / "logs" / "agent.jsonl"))
    assert [e["event"] for e in events][-1] == "turn_end"


def test_empty_lines_are_skipped_and_exit_works_in_any_case(
    environment, monkeypatch, capsys, knowledge_base, orders
):
    provider = use_fake_model(monkeypatch, knowledge_base, orders, [text_response("Hi!")])
    type_lines(monkeypatch, "", "   ", "EXIT")

    assert cli.main(["--email", PRIYA]) == 0
    assert provider.requests == []


def test_the_email_is_asked_for_when_not_given(environment, monkeypatch, capsys, knowledge_base, orders):
    use_fake_model(monkeypatch, knowledge_base, orders, [text_response("Hello Priya.")])
    type_lines(monkeypatch, PRIYA, "Hi", "quit")

    assert cli.main([]) == 0
    assert f"Signed in as {PRIYA}." in capsys.readouterr().out


def test_closing_the_terminal_at_the_email_question_ends_quietly(
    environment, monkeypatch, knowledge_base, orders
):
    provider = use_fake_model(monkeypatch, knowledge_base, orders, [text_response("Hi")])
    type_lines(monkeypatch)  # no lines at all

    assert cli.main([]) == 0
    assert provider.requests == []


def test_an_automatic_ticket_is_shown(environment, monkeypatch, capsys, knowledge_base, orders):
    loop = tool_response(ToolCall("c1", "search_knowledge_base", {"query": "returns"}))
    use_fake_model(monkeypatch, knowledge_base, orders, [loop])
    monkeypatch.setenv("SUPPORT_AGENT_MAX_STEPS", "2")
    type_lines(monkeypatch, "Hello?", "quit")

    cli.main(["--email", PRIYA])

    out = capsys.readouterr().out
    assert "[step_limit," in out and "automatic ticket TCK-" in out


def test_a_crash_shows_the_polite_reply_and_the_chat_continues(
    environment, monkeypatch, capsys, knowledge_base, orders
):
    provider = use_fake_model(
        monkeypatch, knowledge_base, orders, [RuntimeError("bug"), text_response("Back again.")]
    )
    type_lines(monkeypatch, "First", "Second", "quit")

    assert cli.main(["--email", PRIYA]) == 0

    captured = capsys.readouterr()
    assert f"Agent: {fallback_reply()}" in captured.out
    assert "unexpected error: RuntimeError" in captured.err
    assert "Agent: Back again." in captured.out
    # The failed message was removed, so the second request starts cleanly.
    assert provider.requests[1]["messages"] == [{"role": "user", "content": "Second"}]
    errors = [e for e in read_events(environment / "logs" / "agent.jsonl") if e["event"] == "error"]
    assert errors[0]["operation"] == "agent_run"


def test_a_settings_problem_is_explained(environment, monkeypatch, capsys):
    monkeypatch.delenv("AWS_REGION")
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)

    assert cli.main(["--email", PRIYA]) == 1
    assert "Configuration problem: AWS_REGION is not set" in capsys.readouterr().err


@pytest.mark.parametrize("retryable, hint_shown", [(False, True), (True, False)])
def test_a_search_service_problem_at_start_is_explained(
    environment, monkeypatch, capsys, retryable, hint_shown
):
    def broken(settings):
        raise ServiceError("no access", service="embeddings", kind="AccessDenied", retryable=retryable)

    monkeypatch.setattr(cli, "load_resources", broken)

    assert cli.main(["--email", PRIYA]) == 1
    err = capsys.readouterr().err
    assert "Could not prepare the document search: no access" in err
    assert ("Check AWS_REGION" in err) is hint_shown


def test_a_damaged_data_file_is_explained(environment, monkeypatch, capsys):
    def broken(settings):
        raise ConfigError("The orders file is missing or damaged.")

    monkeypatch.setattr(cli, "load_resources", broken)

    assert cli.main(["--email", PRIYA]) == 1
    assert "The orders file is missing or damaged." in capsys.readouterr().err
