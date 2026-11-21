"""Support staff deciding refund and return requests in the admin panel.

Only requests the refund rules sent to the team ("waiting_for_staff") can be
decided here. A person can:

    approve   optionally taking off a restocking fee (up to 20% of the items,
              only for a change of mind, as the Refund Policy says)
    deny      with a short reason, which the customer is told

The decision is written on the request, with who made it and when, and the
customer is told on the request's ticket (live in their chat window if it is
open, otherwise under "Your tickets"). Nothing here changes the order data or
moves any money.
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

from .. import refund_rules
from ..currency import format_inr
from ..refund_requests import (
    APPROVED,
    APPROVED_BY_STAFF,
    DENIED_BY_STAFF,
    WAITING_FOR_STAFF,
    RefundRequestStore,
)
from ..tickets import CLOSED, OPEN, TicketStore
from .accounts import Account

MAX_NOTE_LENGTH = 1000

# Words for the statuses, as the customer and the panel show them.
STATUS_WORDS = {
    APPROVED: "Approved",
    WAITING_FOR_STAFF: "Waiting for the support team",
    APPROVED_BY_STAFF: "Approved by the support team",
    DENIED_BY_STAFF: "Not approved",
}
REASON_WORDS = {
    refund_rules.CHANGED_MIND: "Changed their mind",
    refund_rules.FAULTY: "Faulty",
    refund_rules.DAMAGED: "Damaged on arrival",
    refund_rules.WRONG_ITEM: "Wrong item",
    refund_rules.NOT_RECEIVED: "Not received",
    refund_rules.CANCEL: "Cancel before dispatch",
}


class RefundDecisionError(Exception):
    def __init__(self, message: str, status: int = 400) -> None:
        super().__init__(message)
        self.status = status


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _amount(value: Any) -> Decimal:
    try:
        amount = Decimal(str(value)).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        raise RefundDecisionError("The restocking fee must be an amount in rupees.") from None
    if amount < 0:
        raise RefundDecisionError("The restocking fee cannot be negative.")
    return amount


def what(record: dict[str, Any]) -> str:
    """'Linen Napkins (Set of 4) ×1 from order JL-10231', or 'order JL-10231'."""
    items = ", ".join(f"{i['name']} ×{i['quantity']}" for i in record.get("items") or [])
    return f"{items} from order {record['order_id']}" if items else f"order {record['order_id']}"


def decide(
    requests: RefundRequestStore,
    tickets: TicketStore,
    request_id: str,
    person: Account,
    *,
    approve: bool,
    note: str = "",
    restocking_fee: Any = 0,
) -> dict[str, Any]:
    """Approve or deny a waiting request, and tell the customer on its ticket."""
    note = (note or "").strip()
    if len(note) > MAX_NOTE_LENGTH:
        raise RefundDecisionError(f"The note can be at most {MAX_NOTE_LENGTH} characters.")
    if not approve and len(note) < 5:
        raise RefundDecisionError("Write a short reason for the customer when you do not approve a request.")
    fee = _amount(restocking_fee or 0)

    def change(record: dict[str, Any]) -> None:
        if record.get("status") != WAITING_FOR_STAFF:
            raise RefundDecisionError("This request has already been decided.", status=409)
        money = record.get("money") or {}
        if approve:
            items = Decimal(money.get("item_refund", "0"))
            if fee and record.get("reason") != refund_rules.CHANGED_MIND:
                raise RefundDecisionError("A restocking fee is only taken for a change of mind.")
            limit = (items * refund_rules.MAX_RESTOCKING_PERCENT / 100).quantize(Decimal("0.01"))
            if fee > limit:
                raise RefundDecisionError(
                    f"The restocking fee can be at most {refund_rules.MAX_RESTOCKING_PERCENT}% of the items "
                    f"({format_inr(limit)})."
                )
            before = Decimal(money.get("net_refund", "0"))
            money["restocking_fee"] = str(fee)
            money["net_refund"] = str(max(before - fee, Decimal("0.00")))
            record["money"] = money
        record["status"] = APPROVED_BY_STAFF if approve else DENIED_BY_STAFF
        record["decided_by"] = {"name": person.name or "Admin", "staff_id": person.staff_id}
        record["decided_at"] = _now()
        record["staff_note"] = note

    record = requests.update(request_id, change)
    if record is None:
        raise RefundDecisionError("No such request.", status=404)
    message = customer_message(record)

    def tell_customer(ticket: dict[str, Any]) -> None:
        ticket.setdefault("messages", []).append(
            {
                "from": "staff",
                "name": person.name or "Admin",
                "staff_id": person.staff_id,
                "text": message,
                "at": record["decided_at"],
            }
        )
        # The request was all the ticket was waiting for, so it is done. A ticket
        # someone is chatting on stays open; they end it themselves.
        if ticket.get("status", OPEN) == OPEN:
            ticket["status"] = CLOSED
            ticket["closed_at"] = record["decided_at"]

    if record.get("ticket_id"):
        tickets.update(record["ticket_id"], tell_customer)
    return record


def customer_message(record: dict[str, Any]) -> str:
    """What the customer is told about a decision. Written by code, so the
    amounts are always the ones on the request."""
    money = record.get("money") or {}
    if record["status"] == APPROVED_BY_STAFF:
        text = f"Your request {record['request_id']} for {what(record)} has been approved."
        if money:
            text += f" Refund: {format_inr(money['net_refund'])}, to {money.get('refunded_to', 'your original payment')}."
            if Decimal(money.get("restocking_fee") or "0"):
                text += f" This includes a restocking fee of {format_inr(money['restocking_fee'])}."
    else:
        text = f"Your request {record['request_id']} for {what(record)} was not approved."
    if record.get("staff_note"):
        text += f" Note from the support team: {record['staff_note']}"
    return text


def admin_view(record: dict[str, Any], customer: dict[str, Any] | None) -> dict[str, Any]:
    """A request for the admin panel. The email stays masked, as everywhere there."""
    view = {key: value for key, value in record.items() if key != "customer_email"}
    view["customer_email"] = "[EMAIL]"
    view["customer_name"] = customer["name"] if customer else None
    view["customer_id"] = customer["customer_id"] if customer else None
    view["status_words"] = STATUS_WORDS.get(record.get("status", ""), record.get("status", ""))
    view["reason_words"] = REASON_WORDS.get(record.get("reason", ""), record.get("reason", ""))
    return view


def customer_view(record: dict[str, Any]) -> dict[str, Any]:
    """A request as its customer sees it: no staff IDs, no internal reasons."""
    money = record.get("money") or {}
    decided = record.get("decided_by") or {}
    return {
        "request_id": record["request_id"],
        "created_at": record.get("created_at", ""),
        "order_id": record.get("order_id"),
        "items": record.get("items") or [],
        "reason": REASON_WORDS.get(record.get("reason", ""), ""),
        "status": record.get("status"),
        "status_words": STATUS_WORDS.get(record.get("status", ""), ""),
        "net_refund": money.get("net_refund"),
        "refunded_to": money.get("refunded_to"),
        "ticket_id": record.get("ticket_id"),
        "decided_by": (decided.get("name") or "").split(" ")[0] or None,
        "staff_note": record.get("staff_note") or None,
    }
