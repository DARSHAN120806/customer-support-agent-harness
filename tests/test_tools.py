"""Tests for the three support tools."""

from __future__ import annotations

import json

from conftest import MARCUS, PRIYA

from support_agent.tools import SessionContext, build_tool_registry

# --- The tool list ---------------------------------------------------------


def test_only_the_expected_tools_exist(registry):
    assert registry.names() == [
        "search_knowledge_base",
        "lookup_order",
        "calculate_date",
        "escalate_to_human",
    ]


def test_there_is_no_tool_that_can_change_anything(registry):
    for name in ("issue_refund", "refund_order", "cancel_order", "update_address"):
        assert registry.execute(name, {}).is_error


# --- search_knowledge_base ---------------------------------------------------


def test_search_returns_text_with_its_source(registry):
    result = registry.execute("search_knowledge_base", {"query": "How long is the return window?"})

    assert not result.is_error
    assert "returns.md" in result.content
    assert "30 days" in result.content


def test_search_says_so_when_nothing_is_relevant(registry):
    result = registry.execute("search_knowledge_base", {"query": "zebra astronomy volcano"})

    assert not result.is_error
    assert "No relevant information" in result.content


def test_search_without_a_query_is_an_error(registry):
    assert registry.execute("search_knowledge_base", {}).is_error
    assert registry.execute("search_knowledge_base", {"query": "   "}).is_error


# --- lookup_order ------------------------------------------------------------


def test_customer_can_see_their_own_order(registry):
    result = registry.execute("lookup_order", {"order_id": "JL-10231"})

    order = json.loads(result.content)
    assert order["status"] == "delivered"
    assert order["total"] == 6050.0
    assert order["delivered_on"] == "2026-11-07"
    assert "customer_id" not in order


def test_order_id_is_tidied_up(registry):
    result = registry.execute("lookup_order", {"order_id": "  jl-10231 "})

    assert json.loads(result.content)["order_id"] == "JL-10231"


def test_customer_cannot_see_another_customers_order(registry):
    # JL-10240 belongs to Marcus; the session is signed in as Priya.
    result = registry.execute("lookup_order", {"order_id": "JL-10240"})

    assert "No order JL-10240 was found" in result.content
    for private_detail in ("Wireless Earbuds", "9199", "TRK", "PayPal", "marcus"):
        assert private_detail not in result.content


def test_someone_elses_order_looks_exactly_like_a_missing_order(registry):
    someone_elses = registry.execute("lookup_order", {"order_id": "JL-10240"}).content
    missing = registry.execute("lookup_order", {"order_id": "JL-99999"}).content

    assert someone_elses.replace("JL-10240", "X") == missing.replace("JL-99999", "X")


def test_email_typed_into_the_tool_input_is_ignored(registry):
    # Even if the model were tricked into passing another email, the tool only
    # ever uses the signed-in email held by the harness.
    result = registry.execute(
        "lookup_order", {"order_id": "JL-10240", "customer_email": MARCUS, "email": MARCUS}
    )

    assert "No order JL-10240 was found" in result.content


def test_the_owner_can_see_that_same_order(knowledge_base, orders, tickets):
    marcus_registry = build_tool_registry(
        SessionContext(customer_email="  Marcus.Bell@Example.com "), knowledge_base, orders, tickets
    )
    result = marcus_registry.execute("lookup_order", {"order_id": "JL-10240"})

    assert json.loads(result.content)["total"] == 9199.0


def test_badly_formed_order_id_is_an_error(registry):
    for bad in ("12345", "JL-123", "ORDER-10231", "JL-10231; DROP TABLE"):
        result = registry.execute("lookup_order", {"order_id": bad})
        assert result.is_error
        assert "JL-" in result.content


# --- calculate_date (today is 12 November 2026 in these tests) ----------------


def test_return_deadline_is_worked_out_in_code(registry):
    result = registry.execute("calculate_date", {"start_date": "2026-11-07", "add_days": 30})

    assert "is 2026-12-07" in result.content
    assert "7 December 2026" in result.content
    assert "25 days from today" in result.content
    assert "has not passed" in result.content


def test_warranty_end_date_is_worked_out_in_code(registry):
    result = registry.execute("calculate_date", {"start_date": "2026-09-18", "add_years": 1})

    assert "is 2027-09-18" in result.content
    assert "has not passed" in result.content


def test_a_deadline_in_the_past_is_reported_as_passed(registry):
    result = registry.execute("calculate_date", {"start_date": "2026-09-18", "add_days": 30})

    assert "is 2026-10-18" in result.content
    assert "25 days ago" in result.content
    assert "already passed" in result.content


def test_month_ends_and_leap_years_are_handled(registry):
    january_31 = registry.execute("calculate_date", {"start_date": "2027-01-31", "add_months": 1})
    leap_day = registry.execute("calculate_date", {"start_date": "2028-02-29", "add_years": 1})

    assert "is 2027-02-28" in january_31.content
    assert "is 2029-02-28" in leap_day.content


def test_bad_date_inputs_are_errors(registry):
    for bad in (
        {"start_date": "7 November"},
        {"start_date": "2026-13-40"},
        {"start_date": "2026-11-07", "add_days": -5},
        {"start_date": "2026-11-07", "add_days": "thirty"},
        {},
    ):
        assert registry.execute("calculate_date", bad).is_error


# --- escalate_to_human ---------------------------------------------------------


def test_escalation_creates_a_ticket_in_the_file(registry, tickets, session):
    result = registry.execute(
        "escalate_to_human",
        {
            "reason": "refund_request",
            "summary": "Customer wants a refund for the coffee set in JL-10231, delivered 7 Nov.",
            "order_id": "jl-10231",
        },
    )

    saved = tickets.all()
    assert len(saved) == 1
    ticket = saved[0]
    assert ticket["ticket_id"] in result.content
    assert ticket["status"] == "open"
    assert ticket["reason"] == "refund_request"
    assert ticket["order_id"] == "JL-10231"
    assert ticket["customer_email"] == PRIYA
    assert "coffee set" in ticket["summary"]
    assert session.ticket_ids == [ticket["ticket_id"]]


def test_ticket_always_uses_the_signed_in_email(registry, tickets):
    registry.execute(
        "escalate_to_human",
        {"reason": "other", "summary": "Test.", "customer_email": MARCUS},
    )

    assert tickets.all()[0]["customer_email"] == PRIYA


def test_each_ticket_gets_its_own_number(registry, tickets):
    for reason in ("refund_request", "warranty_claim", "other"):
        registry.execute("escalate_to_human", {"reason": reason, "summary": "Test."})

    ids = [ticket["ticket_id"] for ticket in tickets.all()]
    assert len(set(ids)) == 3


def test_the_same_issue_is_not_ticketed_twice(registry, tickets):
    request = {"reason": "refund_request", "summary": "Refund please.", "order_id": "JL-10231"}
    first = registry.execute("escalate_to_human", request)
    second = registry.execute("escalate_to_human", request)

    assert len(tickets.all()) == 1
    assert tickets.all()[0]["ticket_id"] in first.content
    assert tickets.all()[0]["ticket_id"] in second.content
    assert "already covers" in second.content


def test_there_is_a_limit_on_tickets_per_conversation(registry, tickets):
    order_ids = ["JL-10001", "JL-10002", "JL-10003", "JL-10004", "JL-10005", "JL-10006"]
    results = [
        registry.execute(
            "escalate_to_human", {"reason": "order_problem", "summary": "x", "order_id": order_id}
        )
        for order_id in order_ids
    ]

    assert len(tickets.all()) == 5
    assert results[-1].is_error


def test_escalation_needs_a_valid_reason_and_a_summary(registry, tickets):
    assert registry.execute("escalate_to_human", {"reason": "refund_request"}).is_error
    assert registry.execute("escalate_to_human", {"reason": "made_up", "summary": "x"}).is_error
    assert registry.execute(
        "escalate_to_human", {"reason": "other", "summary": "x", "order_id": "nonsense"}
    ).is_error
    assert tickets.all() == []
