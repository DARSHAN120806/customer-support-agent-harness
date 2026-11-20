"""Numbers for the admin overview, worked out from the event log and tickets.

Nothing here is stored separately: every figure is counted again from the
log (which has personal data masked) and the ticket file each time, so the
overview always matches what the replay and the ticket list show.
"""

from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
from typing import Any, Iterable

DAYS_SHOWN = 14


def overview(events: Iterable[dict[str, Any]], tickets: list[dict[str, Any]], today: date) -> dict[str, Any]:
    # Signing in starts a conversation in the log even if no message is sent.
    # Only conversations with at least one message are counted.
    conversations: set[str] = set()
    with_ticket: set[str] = set()
    customers: set[str] = set()
    outcomes: Counter[str] = Counter()
    checks: Counter[str] = Counter()
    tickets_by_who: Counter[str] = Counter()
    messages_by_day: Counter[str] = Counter()
    messages = 0
    cost = 0.0
    reply_ms: list[int] = []
    # The rules caught in each message, so a rule that was caught and then
    # blocked in the same message counts once.
    caught: dict[tuple[str, Any], set[str]] = {}

    for e in events:
        conversation = e.get("conversation_id", "")
        kind = e.get("event")
        if kind == "turn_start":
            conversations.add(conversation)
            if e.get("customer_ref"):
                customers.add(e["customer_ref"])
            messages += 1
            messages_by_day[str(e.get("ts", ""))[:10]] += 1
        elif kind == "turn_end":
            outcomes[str(e.get("outcome"))] += 1
            cost += float(e.get("cost_usd") or 0)
            if isinstance(e.get("duration_ms"), (int, float)):
                reply_ms.append(int(e["duration_ms"]))
        elif kind in ("reply_rewrite", "reply_blocked"):
            caught.setdefault((conversation, e.get("turn")), set()).update(e.get("rules") or [])
        elif kind == "ticket_created":
            with_ticket.add(conversation)
            tickets_by_who[str(e.get("created_by") or "model")] += 1

    for rules in caught.values():
        checks.update(rules)

    tickets_by_day = Counter(str(t.get("created_at", ""))[:10] for t in tickets)
    days = [today - timedelta(days=n) for n in range(DAYS_SHOWN - 1, -1, -1)]

    return {
        "conversations": len(conversations),
        "customers": len(customers),
        "messages": messages,
        "tickets": len(tickets),
        "open_tickets": sum(1 for t in tickets if str(t.get("status", "open")).lower() == "open"),
        "tickets_by_harness": tickets_by_who.get("harness", 0),
        # Share of conversations that ended up with a person.
        "handover_rate": round(len(with_ticket & conversations) / len(conversations), 3) if conversations else 0.0,
        "cost_usd": round(cost, 6),
        "cost_per_message_usd": round(cost / messages, 6) if messages else 0.0,
        "average_reply_ms": round(sum(reply_ms) / len(reply_ms)) if reply_ms else 0,
        "outcomes": dict(outcomes.most_common()),
        "checks": dict(checks.most_common()),
        "tickets_by_reason": dict(Counter(str(t.get("reason", "other")) for t in tickets).most_common()),
        "days": [
            {"date": d.isoformat(), "messages": messages_by_day.get(d.isoformat(), 0), "tickets": tickets_by_day.get(d.isoformat(), 0)}
            for d in days
        ],
    }
