"""Support tickets: how the agent hands a conversation over to a human.

Each ticket is saved as one line of JSON in a local file. In a real shop this
would create a ticket in a help-desk system instead.

A ticket goes from "open" (waiting for the team) to "in_progress" (a support
person took it) to "closed" (they ended the chat). The messages exchanged with
the customer are kept on the ticket.
"""

from __future__ import annotations

import json
import os
import secrets
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

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


OPEN = "open"
IN_PROGRESS = "in_progress"
CLOSED = "closed"
STATUSES = (OPEN, IN_PROGRESS, CLOSED)

# One lock per ticket file, so a ticket the assistant creates and a change made
# by a support person at the same moment never overwrite each other.
_FILE_LOCKS: dict[str, threading.Lock] = {}
_LOCKS_LOCK = threading.Lock()


def _lock_for(path: Path) -> threading.Lock:
    with _LOCKS_LOCK:
        return _FILE_LOCKS.setdefault(str(path.resolve()), threading.Lock())


class TicketError(Exception):
    """Raised when a ticket could not be saved."""

    kind = "ticket_write_failed"
    # A file that is briefly locked by another program is worth trying again.
    retryable = True


class TicketStore:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._lock = _lock_for(path)

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
            # Filled in when a support person takes the ticket and chats.
            "assigned_to": None,
            "messages": [],
        }
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._lock, self._path.open("a", encoding="utf-8") as file:
                file.write(json.dumps(ticket, ensure_ascii=False) + "\n")
        except OSError as error:
            raise TicketError(f"The ticket file could not be written ({type(error).__name__}).") from error
        return ticket

    @property
    def path(self) -> Path:
        return self._path

    def all(self) -> list[dict[str, Any]]:
        with self._lock:
            return self._read()

    def get(self, ticket_id: str) -> dict[str, Any] | None:
        return next((t for t in self.all() if t.get("ticket_id") == ticket_id), None)

    def update(self, ticket_id: str, change: Callable[[dict[str, Any]], None]) -> dict[str, Any] | None:
        """Change one ticket. `change` edits the ticket in place (and may raise
        to refuse). The whole file is written to a copy and swapped in, so a
        crash half way never leaves a damaged file. None if there is no such ticket."""
        with self._lock:
            tickets = self._read()
            ticket = next((t for t in tickets if t.get("ticket_id") == ticket_id), None)
            if ticket is None:
                return None
            change(ticket)
            new_file = self._path.with_suffix(".jsonl.new")
            new_file.write_text("".join(json.dumps(t, ensure_ascii=False) + "\n" for t in tickets), encoding="utf-8")
            os.replace(new_file, self._path)
            return ticket

    def _read(self) -> list[dict[str, Any]]:
        if not self._path.exists():
            return []
        tickets = []
        for line in self._path.read_text(encoding="utf-8").splitlines():
            try:
                tickets.append(json.loads(line))
            except ValueError:
                continue  # A damaged or empty line is skipped, not fatal.
        return tickets
