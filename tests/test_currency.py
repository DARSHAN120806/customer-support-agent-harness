"""Tests for shop money in Indian rupees: writing it, reading it, and the
safety check that stops the assistant from inventing an amount."""

from __future__ import annotations

import pytest

from support_agent.currency import format_inr, group_indian, parse_inr
from support_agent.safety import find_ungrounded_figures


@pytest.mark.parametrize(
    ("number", "text"),
    [(0, "0"), (699, "699"), (3999, "3,999"), (12900, "12,900"), (129000, "1,29,000"), (10000000, "1,00,00,000")],
)
def test_big_amounts_use_indian_digit_grouping(number, text):
    assert group_indian(number) == text


def test_amounts_are_written_with_the_rupee_sign_and_paise_only_when_needed():
    assert format_inr(3999.0) == "₹3,999"
    assert format_inr("1151.00") == "₹1,151"
    assert format_inr(3999.5) == "₹3,999.50"


@pytest.mark.parametrize("text", ["₹1,29,000", "Rs. 129000", "INR 1,29,000", "₹ 129,000"])
def test_the_usual_ways_of_writing_rupees_are_read(text):
    assert parse_inr(text) == 129000.0


def test_something_that_is_not_rupees_is_refused():
    with pytest.raises(ValueError):
        parse_inr("$12.99")


# --- The figure check, with rupees -------------------------------------------------

POLICY = "| Express | 1–2 business days after dispatch | ₹1,299 on every order |\nA ₹699 return fee."
ORDER = '{"order_id": "JL-10231", "subtotal": 6050.0, "shipping_cost": 0.0, "total": 6050.0}'


@pytest.mark.parametrize(
    "reply",
    [
        "Express shipping costs ₹1,299.",
        "Express shipping costs Rs. 1,299.",
        "Express shipping costs INR 1299.",
        "A ₹699 fee is taken off for a change of mind.",
        "Your order total was ₹6,050.",  # from the order data, written as 6050.0
    ],
)
def test_amounts_from_the_documents_or_the_order_pass(reply):
    assert find_ungrounded_figures(reply, POLICY + "\n" + ORDER) == []


@pytest.mark.parametrize(
    ("reply", "invented"),
    [
        ("Express shipping costs ₹1,499.", "₹1,499"),
        ("Express shipping costs Rs. 999.", "Rs. 999"),
        ("Express shipping costs $12.99.", "$12.99"),  # the old dollar price is no longer true
        ("Your order total was ₹60.50.", "₹60.50"),
    ],
)
def test_an_invented_amount_is_caught_however_it_is_written(reply, invented):
    assert find_ungrounded_figures(reply, POLICY + "\n" + ORDER) == [invented]


def test_a_bare_number_in_a_time_period_does_not_excuse_an_amount():
    # "3–5 business days" must not let "₹3" through.
    assert find_ungrounded_figures("It costs ₹3.", "Standard delivery takes 3–5 business days.") == ["₹3"]


def test_rupee_amounts_stay_readable_in_the_log_but_phone_numbers_are_hidden():
    from support_agent.event_log import mask_text

    assert mask_text("Total ₹1,29,000, fee ₹699, Rs. 1,00,00,000") == "Total ₹1,29,000, fee ₹699, Rs. 1,00,00,000"
    assert mask_text("₹12,900, call 512-555-0147") == "₹12,900, call [PHONE]"
