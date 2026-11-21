"""Support staff answering tickets: take a ticket, chat with the customer, end
the chat. The rules live here; the web API only passes requests through.

Who is answering always comes from the person's own sign-in (their name and
staff ID), never from something they type, so the team numbers can be trusted.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..tickets import CLOSED, IN_PROGRESS, OPEN, TicketStore
from .accounts import Account

MAX_MESSAGE_LENGTH = 2000


class TicketChatError(Exception):
    def __init__(self, message: str, status: int = 400) -> None:
        super().__init__(message)
        self.status = status


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def first_name(name: str) -> str:
    return (name or "").split(" ")[0] or "A team member"


def _person(account: Account) -> dict[str, str]:
    return {"name": account.name or "Admin", "staff_id": account.staff_id, "email": account.email}


def _found(ticket: dict[str, Any] | None) -> dict[str, Any]:
    if ticket is None:
        raise TicketChatError("No such ticket.", status=404)
    return ticket


def _is_mine(ticket: dict[str, Any], account: Account) -> bool:
    assigned = ticket.get("assigned_to") or {}
    return bool(assigned) and assigned.get("email", "").lower() == account.email.lower()


def take(store: TicketStore, ticket_id: str, account: Account) -> dict[str, Any]:
    """Make this ticket the signed-in person's. Taking your own ticket again is fine."""

    def change(ticket: dict[str, Any]) -> None:
        status = ticket.get("status", OPEN)
        if status == CLOSED:
            raise TicketChatError("This ticket is closed.", status=409)
        if status == IN_PROGRESS and not _is_mine(ticket, account):
            raise TicketChatError(f"{ticket['assigned_to']['name']} is already answering this ticket.", status=409)
        if status == OPEN:
            ticket["status"] = IN_PROGRESS
            ticket["assigned_to"] = _person(account)
            ticket["assigned_at"] = _now()

    return _found(store.update(ticket_id, change))


def staff_message(store: TicketStore, ticket_id: str, account: Account, text: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """A reply from the person answering the ticket."""
    text = _clean(text)
    message = {"from": "staff", "name": account.name or "Admin", "staff_id": account.staff_id, "text": text, "at": _now()}

    def change(ticket: dict[str, Any]) -> None:
        if ticket.get("status") != IN_PROGRESS or not _is_mine(ticket, account):
            raise TicketChatError("Take the ticket first. Only the person answering it can reply.", status=409)
        ticket.setdefault("messages", []).append(message)

    return _found(store.update(ticket_id, change)), message


def customer_message(store: TicketStore, ticket_id: str, customer_email: str, text: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """A message from the customer the ticket belongs to."""
    text = _clean(text)
    message = {"from": "customer", "text": text, "at": _now()}

    def change(ticket: dict[str, Any]) -> None:
        if str(ticket.get("customer_email", "")).lower() != customer_email.lower():
            # Someone else's ticket gets the same answer as a missing one.
            raise TicketChatError("No such ticket.", status=404)
        if ticket.get("status") == CLOSED:
            raise TicketChatError("This chat has ended. Please start a new chat if you need more help.", status=409)
        ticket.setdefault("messages", []).append(message)

    return _found(store.update(ticket_id, change)), message


def end(store: TicketStore, ticket_id: str, account: Account) -> dict[str, Any]:
    """Close the ticket: the work is done."""

    def change(ticket: dict[str, Any]) -> None:
        if ticket.get("status") == CLOSED:
            raise TicketChatError("This ticket is already closed.", status=409)
        if ticket.get("status") != IN_PROGRESS or not _is_mine(ticket, account):
            raise TicketChatError("Only the person answering this ticket can end the chat.", status=409)
        ticket["status"] = CLOSED
        ticket["closed_at"] = _now()

    return _found(store.update(ticket_id, change))


def team(tickets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Who answered how many tickets, for the admin overview."""
    people: dict[str, dict[str, Any]] = {}
    for ticket in tickets:
        assigned = ticket.get("assigned_to")
        if not assigned:
            continue
        key = assigned.get("email") or assigned.get("staff_id") or assigned.get("name")
        row = people.setdefault(
            key,
            {"name": assigned.get("name", ""), "staff_id": assigned.get("staff_id", ""), "taken": 0, "closed": 0,
             "answering_now": 0, "messages": 0, "_minutes": []},
        )
        row["taken"] += 1
        row["messages"] += sum(1 for m in ticket.get("messages", []) if m.get("from") == "staff")
        if ticket.get("status") == CLOSED:
            row["closed"] += 1
            minutes = _minutes_between(ticket.get("assigned_at"), ticket.get("closed_at"))
            if minutes is not None:
                row["_minutes"].append(minutes)
        elif ticket.get("status") == IN_PROGRESS:
            row["answering_now"] += 1
    result = []
    for row in people.values():
        minutes = row.pop("_minutes")
        row["average_minutes_to_close"] = round(sum(minutes) / len(minutes), 1) if minutes else None
        result.append(row)
    return sorted(result, key=lambda r: (-r["closed"], -r["taken"], r["name"]))


def _minutes_between(start: str | None, finish: str | None) -> float | None:
    try:
        return (datetime.fromisoformat(finish) - datetime.fromisoformat(start)).total_seconds() / 60
    except (TypeError, ValueError):
        return None


def _clean(text: str) -> str:
    text = (text or "").strip()
    if not text:
        raise TicketChatError("The message is empty.")
    if len(text) > MAX_MESSAGE_LENGTH:
        raise TicketChatError(f"The message is too long (at most {MAX_MESSAGE_LENGTH:,} characters).")
    return text

