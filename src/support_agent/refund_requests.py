"""Refund and return requests started in the chat.

Each request is saved as one line of JSON, next to the tickets. A request is
only a record: it never changes the order data (data/orders.json) and never
moves any money. In a real shop the warehouse and payment systems would pick
the approved requests up from here.

    approved            the shop's rules approved it in the chat (small, simple cases)
    waiting_for_staff   allowed by the rules, but a person must decide; it has a ticket
    approved_by_staff   a person approved it in the admin panel (Stage R3)
    denied_by_staff     a person turned it down (Stage R3)

Only `refund_rules.decide` can make a request "approved"; the AI cannot.
"""

from __future__ import annotations

import json
import os
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .refund_rules import CANCEL, NOT_RECEIVED, Decision, Request
from .tickets import TicketError, _lock_for

APPROVED = "approved"
WAITING_FOR_STAFF = "waiting_for_staff"
APPROVED_BY_STAFF = "approved_by_staff"
DENIED_BY_STAFF = "denied_by_staff"
STATUSES = (APPROVED, WAITING_FOR_STAFF, APPROVED_BY_STAFF, DENIED_BY_STAFF)

# The first words of the tool result when the shop's rules approved a request.
# Only the tool writes tool results, so a reply may say "approved" only when this
# appears in a tool result (safety.check_reply and the evaluation grader).
APPROVED_MARKER = "APPROVED BY THE SHOP'S REFUND RULES"

# Requests with these statuses still hold their items: the same items cannot be
# asked for again. A request turned down by a person frees them.
STILL_OPEN = (APPROVED, WAITING_FOR_STAFF, APPROVED_BY_STAFF)


class RefundRequestStore:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._lock = _lock_for(path)

    @property
    def path(self) -> Path:
        return self._path

    def create(
        self,
        *,
        customer_email: str,
        conversation_id: str | None,
        request: Request,
        decision: Decision,
        status: str,
        ticket_id: str | None = None,
        details: str = "",
    ) -> dict[str, Any]:
        money = decision.check.money
        now = datetime.now(timezone.utc)
        record = {
            # The random part makes the number impossible to guess from another one.
            "request_id": f"RQ-{now:%Y%m%d}-{secrets.token_hex(3).upper()}",
            "created_at": now.isoformat(timespec="seconds"),
            "status": status,
            "customer_email": customer_email,
            "conversation_id": conversation_id,
            "order_id": request.order_id,
            "reason": request.reason,
            "items": [{"name": item.name, "quantity": item.quantity} for item in request.items],
            "seal_opened": request.seal_opened,
            # Amounts as text ("4200.00"), so they stay exact.
            "money": None
            if money is None
            else {
                "item_refund": str(money.item_refund),
                "shipping_refunded": str(money.shipping_refunded),
                "return_fee": str(money.return_fee),
                "net_refund": str(money.net_refund),
                "refunded_to": money.refunded_to,
                "free_return_label": money.free_return_label,
            },
            "why_staff": list(decision.why) if status == WAITING_FOR_STAFF else [],
            "notes": list(decision.check.notes),
            "ticket_id": ticket_id,
            "details": details,
        }
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._lock, self._path.open("a", encoding="utf-8") as file:
                file.write(json.dumps(record, ensure_ascii=False) + "\n")
        except OSError as error:
            raise TicketError(f"The request file could not be written ({type(error).__name__}).") from error
        return record

    def all(self) -> list[dict[str, Any]]:
        with self._lock:
            return self._read()

    def get(self, request_id: str) -> dict[str, Any] | None:
        return next((r for r in self.all() if r.get("request_id") == request_id), None)

    def for_order(self, order_id: str, customer_email: str) -> list[dict[str, Any]]:
        """Earlier requests on this order by this customer, oldest first."""
        email = customer_email.strip().lower()
        return [
            r for r in self.all() if r.get("order_id") == order_id and str(r.get("customer_email", "")).lower() == email
        ]

    def update(self, request_id: str, change: Callable[[dict[str, Any]], None]) -> dict[str, Any] | None:
        """Change one request, written to a copy and swapped in (like tickets)."""
        with self._lock:
            records = self._read()
            record = next((r for r in records if r.get("request_id") == request_id), None)
            if record is None:
                return None
            change(record)
            new_file = self._path.with_suffix(".jsonl.new")
            new_file.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
            os.replace(new_file, self._path)
            return record

    def _read(self) -> list[dict[str, Any]]:
        if not self._path.exists():
            return []
        records = []
        for line in self._path.read_text(encoding="utf-8").splitlines():
            try:
                records.append(json.loads(line))
            except ValueError:
                continue  # A damaged or empty line is skipped, not fatal.
        return records


def requests_next_to(tickets_file: Path) -> RefundRequestStore:
    """The requests file kept next to the tickets file. The chat tool and the
    admin panel both use this, so they always read and write the same file."""
    return RefundRequestStore(tickets_file.parent / "refund_requests.jsonl")


def with_earlier_requests(order: dict[str, Any], earlier: list[dict[str, Any]]) -> dict[str, Any]:
    """The order as the rules should see it: requests made in the chat count
    like the returns already on the order, so the same items cannot be asked
    for twice and a whole-order refund cannot be requested twice."""
    order = dict(order)
    returns = list(order.get("returns") or [])
    refunds = list(order.get("refunds") or [])
    for record in earlier:
        if record.get("status") not in STILL_OPEN:
            continue
        if record.get("reason") in (CANCEL, NOT_RECEIVED):
            refunds.append({"type": "Cancelled or not received (requested in the chat)"})
            continue
        items = ", ".join(f"{i['name']} ×{i['quantity']}" for i in record.get("items") or [])
        returns.append({"items": items, "status": f"Requested in the chat ({record['request_id']})"})
    order["returns"] = returns
    order["refunds"] = refunds
    return order
