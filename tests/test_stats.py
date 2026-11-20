"""Tests for the admin overview numbers, counted from log events and tickets."""

from __future__ import annotations

from datetime import date

from support_agent.web.stats import DAYS_SHOWN, overview

TODAY = date(2026, 11, 21)


def event(kind, conversation="conv_a", turn=0, ts="2026-11-21T10:00:00+00:00", **fields):
    return {"event": kind, "conversation_id": conversation, "turn": turn, "ts": ts, "customer_ref": "cust_1", **fields}


def chat(conversation, *, cost, ms, outcome="completed", extra=(), ts="2026-11-21T10:00:00+00:00"):
    return [
        event("conversation_start", conversation, ts=ts),
        event("turn_start", conversation, 1, ts=ts, message="Hi"),
        *extra,
        event("turn_end", conversation, 1, ts=ts, outcome=outcome, cost_usd=cost, duration_ms=ms),
    ]


def test_empty_log_gives_zeros_not_errors():
    result = overview([], [], TODAY)

    assert (result["conversations"], result["messages"], result["tickets"]) == (0, 0, 0)
    assert result["handover_rate"] == 0.0 and result["cost_per_message_usd"] == 0.0
    assert len(result["days"]) == DAYS_SHOWN and result["days"][-1] == {"date": "2026-11-21", "messages": 0, "tickets": 0}


def test_conversations_messages_cost_and_reply_time_are_counted():
    events = chat("conv_a", cost=0.004, ms=2000) + chat("conv_b", cost=0.006, ms=4000, ts="2026-11-20T09:00:00+00:00")

    result = overview(events, [], TODAY)

    assert (result["conversations"], result["messages"], result["customers"]) == (2, 2, 1)
    assert result["cost_usd"] == 0.01 and result["cost_per_message_usd"] == 0.005
    assert result["average_reply_ms"] == 3000
    assert result["outcomes"] == {"completed": 2}
    assert result["days"][-2:] == [
        {"date": "2026-11-20", "messages": 1, "tickets": 0},
        {"date": "2026-11-21", "messages": 1, "tickets": 0},
    ]


def test_hand_over_rate_and_who_created_the_tickets():
    ticket_by_model = event("ticket_created", "conv_a", 1, created_by="model")
    ticket_by_harness = event("ticket_created", "conv_b", 1, created_by="harness")
    events = (
        chat("conv_a", cost=0, ms=1, extra=[ticket_by_model])
        + chat("conv_b", cost=0, ms=1, extra=[ticket_by_harness])
        + chat("conv_c", cost=0, ms=1)
        + chat("conv_d", cost=0, ms=1)
    )
    tickets = [
        {"created_at": "2026-11-21T10:00:00+00:00", "status": "open", "reason": "refund_request"},
        {"created_at": "2026-11-21T10:05:00+00:00", "status": "closed", "reason": "refund_request"},
    ]

    result = overview(events, tickets, TODAY)

    assert result["handover_rate"] == 0.5
    assert result["tickets_by_harness"] == 1
    assert (result["tickets"], result["open_tickets"]) == (2, 1)
    assert result["tickets_by_reason"] == {"refund_request": 2}
    assert result["days"][-1]["tickets"] == 2


def test_a_rule_caught_then_blocked_in_one_message_counts_once():
    caught = [
        event("reply_rewrite", "conv_a", 1, rules=["identity_leak"]),
        event("reply_blocked", "conv_a", 1, rules=["identity_leak"]),
    ]
    other = [event("reply_rewrite", "conv_b", 1, rules=["identity_leak", "ungrounded_figure"])]
    events = chat("conv_a", cost=0, ms=1, outcome="reply_blocked", extra=caught) + chat("conv_b", cost=0, ms=1, extra=other)

    result = overview(events, [], TODAY)

    assert result["checks"] == {"identity_leak": 2, "ungrounded_figure": 1}
    assert result["outcomes"] == {"reply_blocked": 1, "completed": 1}


def test_a_sign_in_without_any_message_is_not_counted_as_a_conversation():
    events = chat("conv_a", cost=0, ms=1) + [event("conversation_start", "conv_quiet")]

    result = overview(events, [], TODAY)

    assert result["conversations"] == 1
    assert result["handover_rate"] == 0.0


def test_messages_older_than_the_chart_are_still_counted_in_the_totals():
    events = chat("conv_old", cost=0.001, ms=1, ts="2026-10-01T10:00:00+00:00")

    result = overview(events, [], TODAY)

    assert result["messages"] == 1
    assert sum(d["messages"] for d in result["days"]) == 0
