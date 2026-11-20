"""Tests for the web API. They use the fake model, so they are free and fast."""

from __future__ import annotations

import dataclasses
import json
import re
import threading

import pytest
from conftest import MARCUS, PRIYA, TODAY
from fakes import FakeProvider, text_response, tool_response
from fastapi.testclient import TestClient

from support_agent.app import Resources
from support_agent.config import Settings
from support_agent.prompts import IDENTITY_REPLY, SUPPORT_EMAIL, fallback_reply
from support_agent.providers.base import ToolCall
from support_agent.web.api import create_app
from support_agent.web.sessions import ChatSession, SessionStore

EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


@pytest.fixture
def settings(monkeypatch, tmp_path) -> Settings:
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "bedrock")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    for name in ("SUPPORT_AGENT_MODEL", "SUPPORT_AGENT_LOG_FILE"):
        monkeypatch.delenv(name, raising=False)
    return dataclasses.replace(
        Settings.from_env(), max_steps=4, cache_dir=tmp_path, log_file=tmp_path / "logs" / "agent.jsonl"
    )


@pytest.fixture
def make_client(settings, knowledge_base, orders, tickets, tmp_path):
    def make(responses, baselines_dir=None):
        provider = FakeProvider(responses)
        app = create_app(
            settings,
            Resources(provider, knowledge_base, orders, tickets),
            today=TODAY,
            baselines_dir=baselines_dir or tmp_path / "baselines",
        )
        return TestClient(app), provider

    return make


def sign_in(client, email=PRIYA) -> dict:
    response = client.post("/api/sessions", json={"email": email})
    assert response.status_code == 201, response.text
    return response.json()


# --- Health and sign-in -----------------------------------------------------------------


def test_health(make_client):
    client, _ = make_client([text_response("Hi")])

    assert client.get("/api/health").json()["status"] == "ok"


def test_finding_a_customer_for_the_demo_sign_in(make_client):
    client, _ = make_client([text_response("Hi")])

    found = client.get("/api/customers", params={"q": "priya.nair"}).json()
    assert found == [{"name": "Priya Nair", "email": PRIYA, "order_count": 2}]
    assert len(client.get("/api/customers", params={"limit": 5}).json()) == 5


def test_signing_in_shows_only_your_own_orders(make_client):
    client, _ = make_client([text_response("Hi")])
    session = sign_in(client)

    assert session["customer"]["email"] == PRIYA
    assert session["conversation_id"].startswith("conv_")
    assert session["assistant_name"] == "Juniper Lane Goods virtual assistant"
    assert sorted(o["order_id"] for o in session["orders"]) == ["JL-10198", "JL-10231"]
    assert session["transcript"] == []


def test_sign_in_ignores_capitals_and_rejects_unknown_emails(make_client):
    client, _ = make_client([text_response("Hi")])

    assert client.post("/api/sessions", json={"email": "  PRIYA.NAIR@example.com "}).status_code == 201
    assert client.post("/api/sessions", json={"email": "nobody@example.com"}).status_code == 404
    assert client.post("/api/sessions", json={}).status_code == 422


def test_session_ids_cannot_be_guessed(make_client):
    client, _ = make_client([text_response("Hi")])
    ids = {sign_in(client)["session_id"] for _ in range(5)}

    assert len(ids) == 5 and all(len(i) >= 20 for i in ids)
    assert client.get("/api/sessions/not-a-real-session").status_code == 404


# --- Chatting -------------------------------------------------------------------------


def test_a_message_gets_the_reply_and_what_happened_behind_the_scenes(make_client):
    client, _ = make_client(
        [
            tool_response(ToolCall("c1", "lookup_order", {"order_id": "JL-10231"}), input_tokens=1000, output_tokens=50),
            text_response("It was delivered on 2026-11-07.", input_tokens=1200, output_tokens=40),
        ]
    )
    session = sign_in(client)
    response = client.post(f"/api/sessions/{session['session_id']}/messages", json={"text": "Where is JL-10231?"})

    body = response.json()
    assert response.status_code == 200
    assert body["reply"] == "It was delivered on 2026-11-07." and body["outcome"] == "completed"
    details = body["details"]
    assert details["tools_used"] == ["lookup_order"] and details["steps"] == 2
    assert (details["input_tokens"], details["output_tokens"]) == (2200, 90)
    assert details["cost_usd"] > 0
    assert [e["event"] for e in details["events"]] == ["model_call", "tool_call", "model_call"]
    assert details["events"][1]["tool"] == "lookup_order"


def test_the_chat_is_kept_and_continues(make_client):
    client, provider = make_client([text_response("First."), text_response("Second.")])
    session_id = sign_in(client)["session_id"]
    client.post(f"/api/sessions/{session_id}/messages", json={"text": "One"})
    client.post(f"/api/sessions/{session_id}/messages", json={"text": "Two"})

    transcript = client.get(f"/api/sessions/{session_id}").json()["transcript"]
    assert [(t["role"], t["text"]) for t in transcript] == [
        ("customer", "One"), ("assistant", "First."), ("customer", "Two"), ("assistant", "Second."),
    ]
    assert [m["role"] for m in provider.requests[1]["messages"]] == ["user", "assistant", "user"]


def test_safety_checks_run_for_browser_chats_too(make_client):
    client, _ = make_client([text_response("I'm Claude, made by Anthropic.")])
    session_id = sign_in(client)["session_id"]
    body = client.post(f"/api/sessions/{session_id}/messages", json={"text": "Who are you?"}).json()

    assert body["reply"] == IDENTITY_REPLY and body["outcome"] == "reply_blocked"
    events = [e["event"] for e in body["details"]["events"]]
    assert "reply_rewrite" in events and "reply_blocked" in events
    assert body["details"]["violations"] == ["identity_leak"]


def test_a_new_ticket_is_reported_with_the_reply(make_client, tickets):
    client, _ = make_client(
        [
            tool_response(ToolCall("c1", "escalate_to_human", {"reason": "human_requested", "summary": "Wants a person."})),
            text_response("I've passed this to the team."),
        ]
    )
    session_id = sign_in(client)["session_id"]
    body = client.post(f"/api/sessions/{session_id}/messages", json={"text": "Human please"}).json()

    (ticket,) = tickets.all()
    assert body["new_ticket_ids"] == [ticket["ticket_id"]]
    assert client.get(f"/api/sessions/{session_id}").json()["transcript"][-1]["ticket_ids"] == [ticket["ticket_id"]]


def test_privacy_is_unchanged_in_the_browser(make_client):
    client, provider = make_client(
        [tool_response(ToolCall("c1", "lookup_order", {"order_id": "JL-10240"})), text_response("Not on your account.")]
    )
    session_id = sign_in(client)["session_id"]
    client.post(f"/api/sessions/{session_id}/messages", json={"text": "What's in JL-10240?"})

    assert "No order JL-10240 was found" in provider.requests[1]["messages"][2]["content"][0]["content"]


@pytest.mark.parametrize("text", ["", "x" * 2001])
def test_empty_or_huge_messages_are_refused_before_any_model_call(make_client, text):
    client, provider = make_client([text_response("Hi")])
    session_id = sign_in(client)["session_id"]

    assert client.post(f"/api/sessions/{session_id}/messages", json={"text": text}).status_code == 422
    assert provider.requests == []


def test_a_crash_in_the_agent_still_gives_a_polite_reply(make_client):
    client, _ = make_client([RuntimeError("bug")])
    session_id = sign_in(client)["session_id"]
    body = client.post(f"/api/sessions/{session_id}/messages", json={"text": "Hi"}).json()

    assert body["reply"] == fallback_reply() and body["outcome"] == "error"
    assert client.get(f"/api/sessions/{session_id}").json()["transcript"][-1]["text"] == fallback_reply()


def test_a_second_message_while_the_first_is_answered_is_refused(make_client):
    client, _ = make_client([text_response("Hi")])
    session_id = sign_in(client)["session_id"]
    chat = client.app.state.sessions.get(session_id)
    chat.lock.acquire()
    try:
        response = client.post(f"/api/sessions/{session_id}/messages", json={"text": "Hi"})
    finally:
        chat.lock.release()

    assert response.status_code == 409


def test_signing_out_ends_the_chat(make_client):
    client, _ = make_client([text_response("Hi")])
    session_id = sign_in(client)["session_id"]

    assert client.delete(f"/api/sessions/{session_id}").status_code == 204
    assert client.post(f"/api/sessions/{session_id}/messages", json={"text": "Hi"}).status_code == 404


# --- Dashboard ------------------------------------------------------------------------


def test_tickets_are_listed_newest_first_with_emails_masked(make_client):
    escalate = tool_response(ToolCall("c1", "escalate_to_human", {"reason": "other", "summary": f"Contact {MARCUS}."}))
    client, _ = make_client([escalate, text_response("Done."), escalate, text_response("Done.")])
    for email in (PRIYA, MARCUS):
        session_id = sign_in(client, email)["session_id"]
        client.post(f"/api/sessions/{session_id}/messages", json={"text": "Help"})

    listed = client.get("/api/tickets").json()
    assert len(listed) == 2 and listed[0]["created_at"] >= listed[1]["created_at"]
    assert not EMAIL.search(json.dumps(listed))
    assert listed[0]["customer_email"] == "[EMAIL]"


def test_conversations_are_summarised_and_replayed_from_the_log(make_client):
    client, _ = make_client([text_response("Hello!")])
    session = sign_in(client)
    client.post(f"/api/sessions/{session['session_id']}/messages", json={"text": f"Hi, I'm {PRIYA}"})

    (summary,) = client.get("/api/conversations").json()
    assert summary["conversation_id"] == session["conversation_id"]
    assert summary["turns"] == 1 and summary["escalated"] is False
    assert summary["first_message"] == "Hi, I'm [EMAIL]"

    events = client.get(f"/api/conversations/{session['conversation_id']}").json()
    assert [e["event"] for e in events][-1] == "turn_end"
    assert not EMAIL.search(json.dumps(events))
    assert client.get("/api/conversations/conv_000000000000").status_code == 404
    assert client.get("/api/conversations/..%2Fsecrets").status_code == 404


def test_evaluation_baselines_are_listed_and_readable(make_client, tmp_path):
    folder = tmp_path / "baselines"
    folder.mkdir()
    (folder / "run_a.json").write_text(
        json.dumps({"run_at": "2026-11-20T10:00:00", "model": "m", "harness": "off", "summary": {"passed": 38}}),
        encoding="utf-8",
    )
    client, _ = make_client([text_response("Hi")], baselines_dir=folder)

    (listed,) = client.get("/api/evaluations").json()
    assert listed == {"name": "run_a", "run_at": "2026-11-20T10:00:00", "model": "m", "harness": "off", "summary": {"passed": 38}}
    assert client.get("/api/evaluations/run_a").json()["summary"]["passed"] == 38
    for bad in ("missing", ".hidden", "a b"):
        assert client.get(f"/api/evaluations/{bad}").status_code == 404


def test_only_the_front_end_address_may_call_the_api(make_client):
    client, _ = make_client([text_response("Hi")])

    allowed = client.get("/api/health", headers={"Origin": "http://localhost:5173"})
    other = client.get("/api/health", headers={"Origin": "https://evil.example"})
    assert allowed.headers.get("access-control-allow-origin") == "http://localhost:5173"
    assert "access-control-allow-origin" not in other.headers


def test_the_support_email_is_never_masked_in_replies(make_client):
    client, _ = make_client([text_response(f"Write to {SUPPORT_EMAIL}.")])
    session_id = sign_in(client)["session_id"]

    assert SUPPORT_EMAIL in client.post(f"/api/sessions/{session_id}/messages", json={"text": "Email?"}).json()["reply"]


# --- The session store ----------------------------------------------------------------


def make_session(session_id: str) -> ChatSession:
    return ChatSession(session_id, agent=None, context=None, customer={})


def test_idle_sessions_are_removed():
    now = [0.0]
    store = SessionStore(idle_seconds=60, clock=lambda: now[0])
    session = store.add(make_session)

    now[0] = 59
    assert store.get(session.session_id) is session
    now[0] = 59 + 61
    assert store.get(session.session_id) is None


def test_the_number_of_sessions_is_capped_dropping_the_oldest():
    now = [0.0]
    store = SessionStore(max_sessions=2, clock=lambda: now[0])
    first = store.add(make_session)
    now[0] = 1
    second = store.add(make_session)
    now[0] = 2
    third = store.add(make_session)

    assert len(store) == 2
    assert store.get(first.session_id) is None
    assert store.get(second.session_id) and store.get(third.session_id)


def test_the_store_is_safe_with_many_threads():
    store = SessionStore(max_sessions=1000)
    threads = [threading.Thread(target=lambda: [store.add(make_session) for _ in range(50)]) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(store) == 400
