"""Support tickets: how the agent hands a conversation over to a human.

Each ticket is saved as one line of JSON in a local file. In a real shop this
would create a ticket in a help-desk system instead.
"""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ESCALATION_REASONS = [
    "refund_request",
    "return_request",
    "warranty_claim",
    "order_problem",
    "upset_customer",
    "unsure_of_answer",
    "outside_shop_documents",
    "human_requested",
    "other",
]


class TicketStore:
    def __init__(self, path: Path) -> None:
        self._path = path

    def create(
        self,
        *,
        customer_email: str,
        reason: str,
        summary: str,
        order_id: str | None = None,
        conversation_id: str | None = None,
    ) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        ticket = {
            # The random part makes the ID impossible to guess from another one.
            "ticket_id": f"TCK-{now:%Y%m%d}-{secrets.token_hex(3).upper()}",
            "created_at": now.isoformat(timespec="seconds"),
            "status": "open",
            # Links the ticket to the conversation in the event log.
            "conversation_id": conversation_id,
            "customer_email": customer_email,
            "reason": reason,
            "order_id": order_id,
            "summary": summary,
        }
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(ticket, ensure_ascii=False) + "\n")
        return ticket

    def all(self) -> list[dict[str, Any]]:
        if not self._path.exists():
            return []
        lines = self._path.read_text(encoding="utf-8").splitlines()
        return [json.loads(line) for line in lines if line.strip()]
