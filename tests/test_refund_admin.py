"""Tests for support staff deciding refund and return requests in the admin
panel (Stage R3), and for customers seeing their requests. Fake model only."""

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
from support_agent.refund_requests import APPROVED_BY_STAFF, DENIED_BY_STAFF, WAITING_FOR_STAFF, requests_next_to
from support_agent.tickets import TicketStore
from support_agent.web.accounts import ADMIN, CUSTOMER, STAFF, Account, AccountStore, hash_password
from support_agent.web.api import create_app

PASSWORD = "pass-1"
ASHA = Account("asha.rao@juniperlane.example", STAFF, "", "Asha Rao", "JLS-101")
BOTH_ITEMS = [
    {"name": "Linen Napkins (Set of 4)", "quantity": 1},
    {"name": "Ceramic Pour-Over Coffee Set", "quantity": 1},
]


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
    ])
    # Priya asks to return both items of JL-10231: ₹6,050 - ₹699 = ₹5,351, over
    # the ₹5,000 limit, so the rules send it to the team.
    provider = FakeProvider([
        tool_response(ToolCall("c1", "request_refund_or_return",
                               {"order_id": "JL-10231", "reason": "changed_mind", "items": BOTH_ITEMS})),
        text_response("A person from the support team will review it."),
    ])
    tickets = TicketStore(tmp_path / "tickets.jsonl")
    client = TestClient(create_app(settings, Resources(provider, knowledge_base, orders, tickets), today=TODAY, accounts=accounts))
    return client, tickets


def sign_in(client, email) -> dict:
    response = client.post("/api/sessions", json={"email": email, "password": PASSWORD})
    assert response.status_code == 201, response.text
    return response.json()


def panel(client, email="asha.rao@juniperlane.example") -> dict[str, str]:
    return {"Authorization": f"Bearer {sign_in(client, email)['admin_token']}"}


def waiting_request(client) -> tuple[str, dict]:
    """Priya sends her message; returns her session ID and the waiting request."""
    session = sign_in(client, PRIYA)["session_id"]
    client.post(f"/api/sessions/{session}/messages", json={"text": "I want to return everything from JL-10231."})
    (request,) = client.get("/api/admin/refund-requests", headers=panel(client)).json()
    assert request["status"] == WAITING_FOR_STAFF
    return session, request


def test_staff_see_waiting_requests_with_the_customer_and_the_amounts(setup):
    client, _ = setup
    _, request = waiting_request(client)

    assert (request["customer_name"], request["customer_id"]) == ("Priya Nair", "C001")
    assert request["customer_email"] == "[EMAIL]" and PRIYA not in json.dumps(request)
    assert request["money"]["net_refund"] == "5351.00" and request["status_words"] == "Waiting for the support team"
    assert request["reason_words"] == "Changed their mind" and request["ticket_id"].startswith("TCK-")
    assert any("over ₹5,000" in why for why in request["why_staff"])


def test_approving_records_who_and_tells_the_customer_live_and_on_the_ticket(setup):
    client, tickets = setup
    session, request = waiting_request(client)

    response = client.post(
        f"/api/admin/refund-requests/{request['request_id']}/approve",
        json={"restocking_fee": 420, "note": "Box was missing, 10% restocking fee."},
        headers=panel(client),
    )

    assert response.status_code == 200, response.text
    decided = response.json()
    assert decided["status"] == APPROVED_BY_STAFF and decided["decided_by"] == {"name": "Asha Rao", "staff_id": "JLS-101"}
    assert decided["money"]["restocking_fee"] == "420.00" and decided["money"]["net_refund"] == "4931.00"
    # On the ticket, written by code with the request's own amounts. Nobody was
    # chatting on that ticket, so deciding the request closes it.
    assert tickets.get(request["ticket_id"])["status"] == "closed"
    message = tickets.get(request["ticket_id"])["messages"][-1]
    assert message["from"] == "staff" and "₹4,931" in message["text"] and "restocking fee of ₹420" in message["text"]
    # Live in Priya's open chat window.
    entries = client.get(f"/api/sessions/{session}/updates").json()["entries"]
    assert entries[-1]["role"] == "staff" and entries[-1]["name"] == "Asha" and "approved" in entries[-1]["text"]
    # And under her own requests, without staff IDs.
    (mine,) = client.get(f"/api/sessions/{session}/refund-requests").json()
    assert mine["status_words"] == "Approved by the support team" and mine["net_refund"] == "4931.00"
    assert mine["decided_by"] == "Asha" and "JLS-101" not in json.dumps(mine)


def test_denying_needs_a_reason_which_the_customer_is_told(setup):
    client, tickets = setup
    session, request = waiting_request(client)
    deny = f"/api/admin/refund-requests/{request['request_id']}/deny"

    assert client.post(deny, json={"note": ""}, headers=panel(client)).status_code == 400
    response = client.post(deny, json={"note": "The items were used, so they cannot be returned."}, headers=panel(client))

    assert response.json()["status"] == DENIED_BY_STAFF
    assert "was not approved" in tickets.get(request["ticket_id"])["messages"][-1]["text"]
    (mine,) = client.get(f"/api/sessions/{session}/refund-requests").json()
    assert mine["status_words"] == "Not approved" and mine["staff_note"].startswith("The items were used")


def test_a_request_is_decided_only_once(setup):
    client, _ = setup
    _, request = waiting_request(client)
    approve = f"/api/admin/refund-requests/{request['request_id']}/approve"

    assert client.post(approve, json={}, headers=panel(client)).status_code == 200
    again = client.post(approve, json={}, headers=panel(client))
    assert again.status_code == 409 and "already been decided" in again.json()["detail"]


@pytest.mark.parametrize(
    ("body", "message"),
    [
        ({"restocking_fee": 1300}, "at most 20%"),  # 20% of ₹6,050 is ₹1,210
        ({"restocking_fee": -5}, ""),  # refused by the form itself
    ],
)
def test_the_restocking_fee_is_limited(setup, body, message):
    client, _ = setup
    _, request = waiting_request(client)

    response = client.post(f"/api/admin/refund-requests/{request['request_id']}/approve", json=body, headers=panel(client))

    assert response.status_code in (400, 422) and message in response.text


def test_only_signed_in_panel_users_can_see_or_decide(setup):
    client, _ = setup
    _, request = waiting_request(client)

    assert client.get("/api/admin/refund-requests").status_code == 401
    assert client.post(f"/api/admin/refund-requests/{request['request_id']}/approve", json={}).status_code == 401
    # The admin can decide too.
    admin = panel(client, "admin@juniperlane.example")
    assert client.post(f"/api/admin/refund-requests/{request['request_id']}/approve", json={}, headers=admin).status_code == 200
    assert client.post("/api/admin/refund-requests/RQ-20260101-000000/approve", json={}, headers=admin).status_code == 404


def test_a_customer_sees_only_their_own_requests(setup):
    client, _ = setup
    waiting_request(client)
    marcus = sign_in(client, MARCUS)["session_id"]

    assert client.get(f"/api/sessions/{marcus}/refund-requests").json() == []


def test_the_chat_tool_and_the_panel_use_the_same_file(tmp_path):
    assert requests_next_to(tmp_path / "tickets.jsonl").path == tmp_path / "refund_requests.jsonl"


def test_a_ticket_someone_is_chatting_on_stays_open(setup):
    client, tickets = setup
    _, request = waiting_request(client)
    asha = panel(client)
    client.post(f"/api/tickets/{request['ticket_id']}/take", headers=asha)

    client.post(f"/api/admin/refund-requests/{request['request_id']}/approve", json={}, headers=asha)

    assert tickets.get(request["ticket_id"])["status"] == "in_progress"
