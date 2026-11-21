"""Tests for support staff answering tickets in the admin panel: taking a
ticket, chatting live with the customer, ending the chat, and the team numbers.
The model is a fake, so nothing is paid."""

from __future__ import annotations

import dataclasses
import json

import pytest
from conftest import MARCUS, PRIYA, TODAY
from fakes import FakeProvider, text_response, tool_response
from fastapi.testclient import TestClient

from support_agent.app import Resources
from support_agent.config import Settings
from support_agent.providers.base import ToolCall
from support_agent.tickets import CLOSED, IN_PROGRESS, OPEN, TicketStore
from support_agent.web.accounts import ADMIN, CUSTOMER, STAFF, Account, AccountStore, hash_password
from support_agent.web.api import create_app
from support_agent.web.ticket_chat import TicketChatError, customer_message, end, staff_message, take, team

PASSWORD = "pass-1"
ASHA = Account("asha.rao@juniperlane.example", STAFF, "", "Asha Rao", "JLS-101")
TOM = Account("tom.becker@juniperlane.example", STAFF, "", "Tom Becker", "JLS-102")


# --- The rules on their own ----------------------------------------------------------


@pytest.fixture
def store(tmp_path) -> TicketStore:
    return TicketStore(tmp_path / "tickets.jsonl")


def new_ticket(store, email=PRIYA) -> str:
    return store.create(customer_email=email, reason="human_requested", summary="Wants a person.", conversation_id="conv_000000000001")["ticket_id"]


def test_a_new_ticket_is_waiting_with_no_one_on_it(store):
    ticket = store.get(new_ticket(store))

    assert ticket["status"] == OPEN and ticket["assigned_to"] is None and ticket["messages"] == []


def test_taking_a_ticket_records_who_and_when(store):
    ticket_id = new_ticket(store)

    ticket = take(store, ticket_id, ASHA)

    assert ticket["status"] == IN_PROGRESS and ticket["assigned_at"]
    assert ticket["assigned_to"] == {"name": "Asha Rao", "staff_id": "JLS-101", "email": ASHA.email}
    assert take(store, ticket_id, ASHA)["assigned_to"]["name"] == "Asha Rao"  # taking it again is fine


def test_a_ticket_someone_else_has_cannot_be_taken_or_answered(store):
    ticket_id = new_ticket(store)
    take(store, ticket_id, ASHA)

    with pytest.raises(TicketChatError, match="Asha Rao is already answering"):
        take(store, ticket_id, TOM)
    with pytest.raises(TicketChatError, match="Take the ticket first"):
        staff_message(store, ticket_id, TOM, "Hello")
    with pytest.raises(TicketChatError, match="Only the person answering"):
        end(store, ticket_id, TOM)


def test_messages_are_kept_in_order_with_who_sent_them(store):
    ticket_id = new_ticket(store)
    customer_message(store, ticket_id, PRIYA, "Anyone there?")  # allowed while waiting
    take(store, ticket_id, ASHA)
    staff_message(store, ticket_id, ASHA, "Hi Priya, I'm here.")

    messages = store.get(ticket_id)["messages"]

    assert [(m["from"], m["text"]) for m in messages] == [("customer", "Anyone there?"), ("staff", "Hi Priya, I'm here.")]
    assert messages[1]["name"] == "Asha Rao" and messages[1]["staff_id"] == "JLS-101"


def test_a_closed_ticket_takes_no_more_messages(store):
    ticket_id = new_ticket(store)
    take(store, ticket_id, ASHA)
    closed = end(store, ticket_id, ASHA)

    assert closed["status"] == CLOSED and closed["closed_at"]
    with pytest.raises(TicketChatError, match="This chat has ended"):
        customer_message(store, ticket_id, PRIYA, "One more thing")
    with pytest.raises(TicketChatError, match="closed"):
        take(store, ticket_id, TOM)
    with pytest.raises(TicketChatError, match="already closed"):
        end(store, ticket_id, ASHA)


def test_a_customer_cannot_write_on_someone_elses_ticket(store):
    ticket_id = new_ticket(store, email=MARCUS)

    with pytest.raises(TicketChatError) as caught:
        customer_message(store, ticket_id, PRIYA, "Hi")

    assert caught.value.status == 404


def test_empty_and_overlong_messages_are_refused(store):
    ticket_id = new_ticket(store)
    take(store, ticket_id, ASHA)

    with pytest.raises(TicketChatError, match="empty"):
        staff_message(store, ticket_id, ASHA, "   ")
    with pytest.raises(TicketChatError, match="too long"):
        staff_message(store, ticket_id, ASHA, "x" * 2001)


def test_a_refused_change_leaves_the_file_as_it_was(store, tmp_path):
    ticket_id = new_ticket(store)
    take(store, ticket_id, ASHA)
    before = (tmp_path / "tickets.jsonl").read_text(encoding="utf-8")

    with pytest.raises(TicketChatError):
        take(store, ticket_id, TOM)

    assert (tmp_path / "tickets.jsonl").read_text(encoding="utf-8") == before
    with pytest.raises(TicketChatError) as caught:
        take(store, "TCK-00000000-NOPE00", ASHA)
    assert caught.value.status == 404


def test_the_team_numbers_count_who_did_what(store):
    first, second, third = new_ticket(store), new_ticket(store), new_ticket(store)
    take(store, first, ASHA)
    staff_message(store, first, ASHA, "One")
    staff_message(store, first, ASHA, "Two")
    end(store, first, ASHA)
    take(store, second, ASHA)
    take(store, third, TOM)
    end(store, third, TOM)

    rows = {r["name"]: r for r in team(store.all())}

    assert rows["Asha Rao"] | {"average_minutes_to_close": None} == {
        "name": "Asha Rao", "staff_id": "JLS-101", "taken": 2, "closed": 1, "answering_now": 1, "messages": 2,
        "average_minutes_to_close": None,
    }
    assert rows["Asha Rao"]["average_minutes_to_close"] is not None
    assert rows["Tom Becker"]["closed"] == 1 and rows["Tom Becker"]["messages"] == 0
    assert team([{"assigned_to": None}]) == []


# --- Through the web API ----------------------------------------------------------------


@pytest.fixture
def setup(monkeypatch, tmp_path, knowledge_base, orders):
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "bedrock")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.delenv("SUPPORT_AGENT_MODEL", raising=False)
    settings = dataclasses.replace(
        Settings.from_env(), max_steps=4, cache_dir=tmp_path, log_file=tmp_path / "logs" / "agent.jsonl",
        model_settings_file=tmp_path / "private" / "model_settings.json",
    )
    accounts = AccountStore([
        Account(PRIYA, CUSTOMER, hash_password(PASSWORD, n=2**4)),
        Account(MARCUS, CUSTOMER, hash_password(PASSWORD, n=2**4)),
        Account("admin@juniperlane.example", ADMIN, hash_password(PASSWORD, n=2**4), "Shop admin", "JLS-100"),
        dataclasses.replace(ASHA, password_hash=hash_password(PASSWORD, n=2**4)),
        dataclasses.replace(TOM, password_hash=hash_password(PASSWORD, n=2**4)),
    ])
    escalate = tool_response(ToolCall("c1", "escalate_to_human", {"reason": "human_requested", "summary": "Wants a person."}))
    provider = FakeProvider([escalate, text_response("I've passed you to the team."), text_response("The assistant again.")])
    tickets = TicketStore(tmp_path / "tickets.jsonl")
    client = TestClient(create_app(settings, Resources(provider, knowledge_base, orders, tickets), today=TODAY, accounts=accounts))
    return client, provider, tickets


def sign_in(client, email, password=PASSWORD) -> dict:
    response = client.post("/api/sessions", json={"email": email, "password": password})
    assert response.status_code == 201, response.text
    return response.json()


def staff(client, email) -> dict[str, str]:
    return {"Authorization": f"Bearer {sign_in(client, email)['admin_token']}"}


def customer_asks_for_a_person(client) -> tuple[str, str]:
    session_id = sign_in(client, PRIYA)["session_id"]
    reply = client.post(f"/api/sessions/{session_id}/messages", json={"text": "Can I speak to a person?"}).json()
    return session_id, reply["new_ticket_ids"][0]


def updates(client, session_id, after=0) -> dict:
    return client.get(f"/api/sessions/{session_id}/updates", params={"after": after}).json()


def test_support_staff_sign_in_with_their_name_and_id_and_see_only_their_pages(setup):
    client, _, _ = setup

    signed_in = sign_in(client, ASHA.email)
    assert (signed_in["role"], signed_in["name"], signed_in["staff_id"]) == ("staff", "Asha Rao", "JLS-101")
    headers = {"Authorization": f"Bearer {signed_in['admin_token']}"}
    assert client.get("/api/admin/me", headers=headers).json() == {"role": "staff", "name": "Asha Rao", "staff_id": "JLS-101"}

    for path in ["/api/tickets", "/api/stats", "/api/conversations", "/api/admin/orders"]:
        assert client.get(path, headers=headers).status_code == 200, path
    for path in ["/api/admin/model", "/api/admin/documents", "/api/evaluations"]:
        assert client.get(path, headers=headers).status_code == 403, path


def test_a_live_chat_goes_to_the_person_and_back_to_the_assistant_after_end(setup):
    client, provider, tickets = setup
    session_id, ticket_id = customer_asks_for_a_person(client)
    asha = staff(client, ASHA.email)
    seen = updates(client, session_id)["next"]

    view = client.post(f"/api/tickets/{ticket_id}/take", headers=asha).json()
    assert view["ticket"]["status"] == IN_PROGRESS and view["ticket"]["live"] is True
    assert view["ticket"]["assigned_to"]["name"] == "Asha Rao"
    assert [c["role"] for c in view["chat"]] == ["customer", "assistant"]  # the chat before the hand-over

    news = updates(client, session_id, seen)
    assert news["handoff"] == {"name": "Asha"}
    assert news["entries"] == [{"role": "system", "text": "Asha from the support team has joined the chat. You're now talking to a person."}]

    # The customer's next message goes to Asha, not to the assistant.
    calls_before = len(provider.requests)
    sent = client.post(f"/api/sessions/{session_id}/messages", json={"text": "My kettle leaks."}).json()
    assert sent == {"reply": None, "outcome": "sent_to_team", "new_ticket_ids": []}
    assert len(provider.requests) == calls_before
    assert tickets.get(ticket_id)["messages"][-1]["text"] == "My kettle leaks."

    client.post(f"/api/tickets/{ticket_id}/messages", headers=asha, json={"text": "Sorry to hear that. Which order?"})
    news = updates(client, session_id, news["next"])
    assert news["entries"][-1] == {"role": "staff", "text": "Sorry to hear that. Which order?", "name": "Asha"}

    ended = client.post(f"/api/tickets/{ticket_id}/end", headers=asha).json()
    assert ended["ticket"]["status"] == CLOSED
    news = updates(client, session_id, news["next"])
    assert news["handoff"] is None and "ended the chat" in news["entries"][-1]["text"]

    back = client.post(f"/api/sessions/{session_id}/messages", json={"text": "Thanks!"}).json()
    assert back["reply"] == "The assistant again."


def test_a_second_person_cannot_take_the_same_ticket(setup):
    client, _, _ = setup
    _, ticket_id = customer_asks_for_a_person(client)
    client.post(f"/api/tickets/{ticket_id}/take", headers=staff(client, ASHA.email))

    response = client.post(f"/api/tickets/{ticket_id}/take", headers=staff(client, TOM.email))

    assert response.status_code == 409 and "Asha Rao is already answering" in response.json()["detail"]


def test_a_customer_who_left_sees_the_reply_in_your_tickets_and_can_answer(setup):
    client, _, tickets = setup
    session_id, ticket_id = customer_asks_for_a_person(client)
    client.delete(f"/api/sessions/{session_id}")  # the customer signs out
    asha = staff(client, ASHA.email)

    view = client.post(f"/api/tickets/{ticket_id}/take", headers=asha).json()
    assert view["ticket"]["live"] is False
    client.post(f"/api/tickets/{ticket_id}/messages", headers=asha, json={"text": "Hi Priya, we can replace it."})

    later = sign_in(client, PRIYA)["session_id"]  # a new visit
    (mine,) = [t for t in client.get(f"/api/sessions/{later}/tickets").json() if t["ticket_id"] == ticket_id]
    assert mine["status"] == IN_PROGRESS and mine["assigned_name"] == "Asha"
    assert mine["messages"][-1] == {"from": "staff", "text": "Hi Priya, we can replace it.", "at": mine["messages"][-1]["at"], "name": "Asha"}
    assert "staff_id" not in json.dumps(mine) and ASHA.email not in json.dumps(mine)  # staff details stay inside

    answered = client.post(f"/api/sessions/{later}/tickets/{ticket_id}/messages", json={"text": "Yes please!"})
    assert answered.status_code == 200 and answered.json()["messages"][-1]["text"] == "Yes please!"
    assert tickets.get(ticket_id)["messages"][-1]["from"] == "customer"


def test_customers_cannot_reply_on_another_customers_ticket(setup):
    client, _, _ = setup
    _, ticket_id = customer_asks_for_a_person(client)
    marcus = sign_in(client, MARCUS)["session_id"]

    response = client.post(f"/api/sessions/{marcus}/tickets/{ticket_id}/messages", json={"text": "Hi"})

    assert response.status_code == 404


def test_the_ticket_list_shows_status_people_and_masked_emails(setup):
    client, _, _ = setup
    _, ticket_id = customer_asks_for_a_person(client)
    asha = staff(client, ASHA.email)
    client.post(f"/api/tickets/{ticket_id}/take", headers=asha)

    (listed,) = client.get("/api/tickets", headers=asha).json()

    assert listed["status"] == IN_PROGRESS and listed["assigned_to"]["name"] == "Asha Rao"
    assert PRIYA not in json.dumps(listed) and ASHA.email not in json.dumps(listed)
    assert client.get("/api/tickets/TCK-00000000-NOPE00", headers=asha).status_code == 404


def test_the_overview_shows_who_handled_how_many_tickets(setup):
    client, _, _ = setup
    _, ticket_id = customer_asks_for_a_person(client)
    asha = staff(client, ASHA.email)
    client.post(f"/api/tickets/{ticket_id}/take", headers=asha)
    client.post(f"/api/tickets/{ticket_id}/messages", headers=asha, json={"text": "Hello"})
    client.post(f"/api/tickets/{ticket_id}/end", headers=asha)

    stats = client.get("/api/stats", headers=asha).json()

    (row,) = stats["team"]
    assert (row["name"], row["staff_id"], row["closed"], row["messages"]) == ("Asha Rao", "JLS-101", 1, 1)
    assert stats["open_tickets"] == 0 and stats["tickets_in_progress"] == 0


def test_the_ticket_chat_needs_a_panel_sign_in(setup):
    client, _, _ = setup
    _, ticket_id = customer_asks_for_a_person(client)

    for path in [f"/api/tickets/{ticket_id}/take", f"/api/tickets/{ticket_id}/end"]:
        assert client.post(path).status_code == 401
    assert client.post(f"/api/tickets/{ticket_id}/messages", json={"text": "x"}).status_code == 401
    assert client.get(f"/api/tickets/{ticket_id}").status_code == 401


def test_the_person_answering_sees_who_the_customer_is_and_their_orders(setup):
    client, _, _ = setup
    _, ticket_id = customer_asks_for_a_person(client)
    asha = staff(client, ASHA.email)

    detail = client.get(f"/api/tickets/{ticket_id}", headers=asha).json()

    customer = detail["customer"]
    assert (customer["name"], customer["customer_id"], customer["city"]) == ("Priya Nair", "C001", "Austin, TX")
    assert [o["order_id"] for o in customer["orders"]] == ["JL-10231", "JL-10198"]  # newest first
    assert customer["email"] == "[EMAIL]" and PRIYA not in json.dumps(detail)
    (listed,) = client.get("/api/tickets", headers=asha).json()
    assert (listed["customer_name"], listed["customer_id"]) == ("Priya Nair", "C001")
