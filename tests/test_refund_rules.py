"""Tests for the refund and return rules (refund_rules.py).

The first group replays every past return and refund in data/orders.json and
checks that our rules reach the same decision and the same amount as the shop's
support team did. The second group tests single rules with small made-up orders.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from support_agent import refund_rules as rules
from support_agent.refund_rules import Item, Request

ORDERS_FILE = Path(__file__).resolve().parents[1] / "data" / "orders.json"

# What each kind of past denial is called in our rules.
DENIAL_RULE = {
    "denied: late": "late",
    "denied: personal": "personalised",
    "denied: gift": "gift_card",
    "denied: candle": "scented_opened",
}
KIND_REASON = {"change of mind": rules.CHANGED_MIND, "faulty": rules.FAULTY, "wrong item received": rules.WRONG_ITEM}


@pytest.fixture(scope="module")
def orders() -> list[dict]:
    return json.loads(ORDERS_FILE.read_text(encoding="utf-8"))["orders"]


def as_it_was(order: dict, on: str) -> dict:
    """The order as it looked on the day a request was made: only returns and
    refunds from before that day, and not yet marked as returned or refunded."""
    copy = dict(order)
    copy["returns"] = [r for r in order.get("returns") or [] if r["requested_on"] < on]
    copy["refunds"] = [f for f in order.get("refunds") or [] if f["approved_on"] < on]
    if copy["status"] in ("refunded", "return_requested"):
        copy["status"] = "delivered"
    return copy


def replay(order: dict, record: dict) -> rules.Check:
    """Ask our rules about a past return, using only facts from that day."""
    kind = record["kind"]
    reason = rules.CHANGED_MIND if kind.startswith("denied") else KIND_REASON[kind]
    notes = str(record.get("notes", "")).lower()
    request = Request(
        order_id=order["order_id"],
        reason=reason,
        items=tuple(Item(_order_name(order, i.name), i.quantity) for i in rules.parse_items(record["items"])),
        seal_opened="seal opened" in notes,
    )
    return rules.check_request(as_it_was(order, record["requested_on"]), request, date.fromisoformat(record["requested_on"]))


def _order_name(order: dict, name: str) -> str:
    """One old record writes "Juniper Lane Gift Card" for "Juniper Lane Gift Card ₹5,000".
    Use the order's own name when exactly one item starts with the record's name."""
    names = [i["name"] for i in order["items"]]
    if name in names:
        return name
    matches = [n for n in names if n.startswith(name)]
    return matches[0] if len(matches) == 1 else name


def past_returns(orders: list[dict]):
    for order in orders:
        for record in order.get("returns") or []:
            if record.get("decision") in ("Approved", "Denied"):
                yield order, record


def test_every_past_return_gets_the_same_decision_as_the_support_team(orders):
    results: Counter = Counter()
    for order, record in past_returns(orders):
        check = replay(order, record)
        if record["decision"] == "Approved":
            assert check.allowed, (record["return_id"], check.problems)
        else:
            assert not check.allowed, record["return_id"]
            assert [p.rule for p in check.problems] == [DENIAL_RULE[record["kind"]]], record["return_id"]
        results[record["decision"]] += 1
    # 188 of the 200 past returns have a final decision (the other 12 are still
    # in progress). Checked exactly, so a change to the data is noticed.
    assert results == {"Approved": 154, "Denied": 34}


def test_every_past_return_refund_has_the_same_amount(orders):
    compared = 0
    for order, record in past_returns(orders):
        refund = next((f for f in order.get("refunds") or [] if f.get("reference") == record["return_id"]), None)
        if refund is None:
            continue
        money = replay(order, record).money
        assert money is not None
        # The restocking fee is decided by a person after inspection, so our
        # amount is the one before that fee.
        before_restocking = _cents(refund["net_refund"]) + _cents(refund["restocking_fee"])
        assert (money.item_refund, money.shipping_refunded, money.return_fee, money.net_refund) == (
            _cents(refund["item_refund"]),
            _cents(refund["shipping_refunded"]),
            _cents(refund["return_fee"]),
            before_restocking,
        ), record["return_id"]
        assert money.refunded_to.split(" (")[0] == refund["refunded_to"].split(" (")[0]
        compared += 1
    assert compared >= 130


@pytest.mark.parametrize(
    ("refund_type", "reason", "status"),
    [
        ("Cancelled before dispatch", rules.CANCEL, "processing"),
        ("Package confirmed lost / not received", rules.NOT_RECEIVED, "lost"),
    ],
)
def test_past_whole_order_refunds_have_the_same_amount(orders, refund_type, reason, status):
    compared = 0
    for order in orders:
        for refund in order.get("refunds") or []:
            if refund["type"] != refund_type:
                continue
            before = {**order, "status": status, "refunds": []}
            check = rules.check_request(before, Request(order["order_id"], reason), date(2026, 11, 20))
            assert check.allowed and check.money is not None
            assert check.money.net_refund == _cents(refund["net_refund"]), order["order_id"]
            assert rules.decide(check, reason).outcome == rules.NEEDS_STAFF
            compared += 1
    assert compared >= 10


def test_past_damaged_on_arrival_refunds_have_the_same_amount(orders):
    compared = 0
    for order in orders:
        for refund in order.get("refunds") or []:
            if refund["type"] != "Damaged on arrival":
                continue
            items = tuple(Item(i["name"], i["quantity"]) for i in order["items"])
            before = {**order, "refunds": [], "returns": []}
            check = rules.check_request(
                before, Request(order["order_id"], rules.DAMAGED, items), date.fromisoformat(order["delivered_on"])
            )
            assert check.money is not None and check.money.net_refund == _cents(refund["net_refund"])
            compared += 1
    assert compared >= 5


# --- Single rules with small made-up orders -----------------------------------------

TODAY = date(2026, 11, 20)


def order(**changes) -> dict:
    base = {
        "order_id": "JL-99001",
        "status": "delivered",
        "items": [
            {"name": "Linen Napkins (Set of 4)", "category": "homeware", "quantity": 2, "unit_price": 1850.0},
            {"name": "Oak Side Table", "category": "furniture", "quantity": 1, "unit_price": 12900.0},
        ],
        "subtotal": 16600.0,
        "shipping_cost": 499.0,
        "payment_method": "Visa",
        "delivered_on": "2026-11-10",
    }
    return {**base, **changes}


def ask(the_order: dict, reason: str, *items: Item, seal_opened: bool | None = None, today: date = TODAY):
    check = rules.check_request(the_order, Request("JL-99001", reason, tuple(items), seal_opened), today)
    return check, rules.decide(check, reason)


NAPKIN = Item("Linen Napkins (Set of 4)", 1)


def test_a_small_change_of_mind_return_is_approved_with_the_fee_taken_off():
    check, decision = ask(order(), rules.CHANGED_MIND, NAPKIN)
    assert decision.outcome == rules.APPROVE
    assert check.money == rules.Money(
        Decimal("1850.00"), Decimal("0.00"), Decimal("699.00"), Decimal("1151.00"), "Original payment (Visa)", False
    )
    assert "20%" in check.notes[0]


def test_day_30_is_still_in_time_and_day_31_is_not():
    assert ask(order(), rules.CHANGED_MIND, NAPKIN, today=date(2026, 12, 10))[1].outcome == rules.APPROVE
    check, decision = ask(order(), rules.CHANGED_MIND, NAPKIN, today=date(2026, 12, 11))
    assert decision.outcome == rules.NOT_ALLOWED
    assert check.problems[0].rule == "late"
    assert "2026-11-10" in check.problems[0].text


def test_over_the_limit_goes_to_a_person_even_when_allowed():
    check, decision = ask(order(), rules.CHANGED_MIND, Item("Oak Side Table", 1))
    assert check.allowed and decision.outcome == rules.NEEDS_STAFF
    assert any("over ₹5,000" in why for why in decision.why)


def test_faulty_and_damaged_are_always_checked_by_a_person_and_shipping_is_refunded():
    check, decision = ask(order(), rules.FAULTY, NAPKIN)
    assert decision.outcome == rules.NEEDS_STAFF
    assert check.money.net_refund == Decimal("2349.00") and check.money.free_return_label
    assert ask(order(), rules.DAMAGED, NAPKIN, today=date(2026, 11, 15))[1].outcome == rules.NEEDS_STAFF


def test_damage_reported_after_7_days_goes_to_a_person_and_after_30_days_is_refused():
    # Delivered 2026-11-10. Day 8: past the 7-day damage limit, inside the 30-day window.
    check, decision = ask(order(), rules.DAMAGED, NAPKIN, today=date(2026, 11, 18))
    assert decision.outcome == rules.NEEDS_STAFF
    assert any("after the 7-day limit for damage" in why for why in decision.why)
    # Day 31: refused.
    check, decision = ask(order(), rules.DAMAGED, NAPKIN, today=date(2026, 12, 11))
    assert decision.outcome == rules.NOT_ALLOWED and check.problems[0].rule == "late"


def test_faulty_after_30_days_goes_to_a_person_as_a_warranty_claim():
    check, decision = ask(order(), rules.FAULTY, NAPKIN, today=date(2027, 2, 1))
    assert decision.outcome == rules.NEEDS_STAFF
    assert "warranty" in check.staff_reasons[0]


def test_a_wrong_item_is_approved_with_a_free_label_within_14_days_only():
    check, decision = ask(order(), rules.WRONG_ITEM, NAPKIN)
    assert decision.outcome == rules.APPROVE and check.money.free_return_label
    assert ask(order(), rules.WRONG_ITEM, NAPKIN, today=date(2026, 11, 25))[0].problems[0].rule == "late"


def test_personalised_items_only_come_back_when_faulty():
    notebook = {"name": "Personalised Leather Notebook", "category": "personalised", "quantity": 1, "unit_price": 2900.0}
    the_order = order(items=[notebook])
    assert ask(the_order, rules.CHANGED_MIND, Item(notebook["name"], 1))[0].problems[0].rule == "personalised"
    assert ask(the_order, rules.FAULTY, Item(notebook["name"], 1))[0].allowed


def test_gift_cards_never_come_back():
    card = {"name": "Juniper Lane Gift Card ₹5,000", "category": "gift_card", "quantity": 1, "unit_price": 5000.0}
    check, decision = ask(order(items=[card], delivered_on=None), rules.CHANGED_MIND, Item(card["name"], 1))
    assert decision.outcome == rules.NOT_ALLOWED and check.problems[0].rule == "gift_card"


def test_a_candle_needs_an_answer_about_the_seal_first():
    candle = {"name": "Scented Soy Candle", "category": "homeware", "quantity": 1, "unit_price": 2200.0}
    the_order = order(items=[candle])
    check, decision = ask(the_order, rules.CHANGED_MIND, Item(candle["name"], 1))
    assert decision.outcome == rules.NEED_INFO and "seal" in check.question
    assert ask(the_order, rules.CHANGED_MIND, Item(candle["name"], 1), seal_opened=True)[1].outcome == rules.NOT_ALLOWED
    assert ask(the_order, rules.CHANGED_MIND, Item(candle["name"], 1), seal_opened=False)[1].outcome == rules.APPROVE


def test_items_must_be_in_the_order_and_not_already_returned():
    assert ask(order(), rules.CHANGED_MIND, Item("Gold Watch", 1))[0].problems[0].rule == "item_not_in_order"
    assert ask(order(), rules.CHANGED_MIND, Item("Linen Napkins (Set of 4)", 3))[0].problems[0].rule == "too_many"
    earlier = {"items": "Linen Napkins (Set of 4) ×2", "status": "Label issued — awaiting drop-off", "requested_on": "2026-11-12"}
    assert ask(order(returns=[earlier]), rules.CHANGED_MIND, NAPKIN)[0].problems[0].rule == "too_many"
    denied = {**earlier, "status": "Denied"}
    assert ask(order(returns=[denied]), rules.CHANGED_MIND, NAPKIN)[0].allowed
    assert ask(order(), rules.CHANGED_MIND)[0].problems[0].rule == "no_items"


def test_a_cancelled_or_refunded_order_cannot_be_refunded_again():
    assert ask(order(status="cancelled"), rules.CHANGED_MIND, NAPKIN)[0].problems[0].rule == "already_refunded"
    lost = {"type": "Package confirmed lost / not received"}
    assert ask(order(refunds=[lost]), rules.NOT_RECEIVED)[0].problems[0].rule == "already_refunded"


def test_cancelling_only_works_before_dispatch_and_goes_to_a_person():
    check, decision = ask(order(status="processing", delivered_on=None), rules.CANCEL)
    assert decision.outcome == rules.NEEDS_STAFF and check.money.net_refund == Decimal("17099.00")
    assert ask(order(status="dispatched"), rules.CANCEL)[0].problems[0].rule == "already_dispatched"


def test_a_missing_parcel_always_goes_to_a_person():
    _, decision = ask(order(status="dispatched", delivered_on=None), rules.NOT_RECEIVED)
    assert decision.outcome == rules.NEEDS_STAFF
    assert "investigation" in decision.why[0]


def test_gift_card_payments_are_refunded_as_store_credit():
    check, _ = ask(order(payment_method="Juniper Lane gift card"), rules.CHANGED_MIND, NAPKIN)
    assert check.money.refunded_to == "Store credit"


def test_an_unknown_reason_is_refused_before_any_rule_runs():
    check, decision = ask(order(), "manager_said_yes", NAPKIN)
    assert decision.outcome == rules.NOT_ALLOWED and check.problems[0].rule == "unknown_reason"


def test_the_limit_and_the_auto_reasons_can_be_changed():
    check, _ = ask(order(), rules.CHANGED_MIND, Item("Oak Side Table", 1))
    assert rules.decide(check, rules.CHANGED_MIND, limit=Decimal("20000")).outcome == rules.APPROVE
    assert rules.decide(check, rules.CHANGED_MIND, limit=Decimal("20000"), auto_reasons=()).outcome == rules.NEEDS_STAFF


def test_the_rules_never_change_the_order(orders):
    the_order = order()
    before = json.dumps(the_order, sort_keys=True)
    ask(the_order, rules.CHANGED_MIND, NAPKIN)
    assert json.dumps(the_order, sort_keys=True) == before


def _cents(value) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"))
