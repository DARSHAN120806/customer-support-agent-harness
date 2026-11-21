"""Refund and return rules, written as plain code.

The AI never decides whether a refund or return is allowed. It only collects
the facts (which order, which items, why) and this file decides, using the
same rules as the shop's Returns and Refund policies. The same question always
gets the same answer here, whatever the customer writes in the chat.

There are two steps:

1. `check_request` looks at one order and says whether the request is allowed
   by the policy, and how much money it would be. It never approves anything.
2. `decide` says whether an allowed request can be approved straight away in
   the chat, or must go to a person in the support team.

Nothing in this file changes any data or moves any money.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from .currency import format_inr

# --- The reasons a customer can give ------------------------------------------------
# The AI must pick one of these. Anything else is refused before any rule runs.
CHANGED_MIND = "changed_mind"  # no longer wanted, bought by mistake, wrong colour...
FAULTY = "faulty"  # the item does not work properly
DAMAGED = "damaged_on_arrival"  # the parcel or item arrived broken
WRONG_ITEM = "wrong_item"  # we sent something the customer did not order
NOT_RECEIVED = "not_received"  # the parcel is lost or never arrived
CANCEL = "cancel"  # stop an order that has not been dispatched yet

REASONS = (CHANGED_MIND, FAULTY, DAMAGED, WRONG_ITEM, NOT_RECEIVED, CANCEL)

# Reasons that are about single items. The others are about the whole order.
ITEM_REASONS = (CHANGED_MIND, FAULTY, DAMAGED, WRONG_ITEM)

# --- Numbers from the policies ------------------------------------------------------
RETURN_WINDOW_DAYS = 30  # Returns Policy: "within 30 days of the delivery date"
WRONG_ITEM_DAYS = 14  # Returns Policy: wrong item, "within 14 days of delivery"
DAMAGE_REPORT_DAYS = 7  # Shipping Policy: damaged parcel, "within 7 days of delivery"
RETURN_FEE = Decimal("699.00")  # Refund Policy: ₹699, deducted for a change of mind
MAX_RESTOCKING_PERCENT = 20  # Refund Policy: "up to 20%" if used or unpackaged

# --- Item types that cannot be returned for a change of mind -------------------------
GIFT_CARD = "gift_card"
PERSONALISED = "personalised"
# Scented products can only come back if the seal has not been opened.
SCENTED_WORDS = ("candle", "scented", "diffuser")

# --- The three results of `decide` --------------------------------------------------
APPROVE = "approve"  # approved in the chat, no person needed
NEEDS_STAFF = "needs_staff"  # allowed by the rules, but a person must decide
NOT_ALLOWED = "not_allowed"  # the policy does not allow it
NEED_INFO = "need_info"  # the customer must answer a question first

# The default for `decide`: small, simple cases only (the owner's choice, 21 Nov 2026;
# $50 became ₹5,000 when the shop moved to rupees).
AUTO_APPROVE_LIMIT = Decimal("5000.00")  # ₹5,000
AUTO_APPROVE_REASONS = (CHANGED_MIND, WRONG_ITEM)

# Past returns with these words in their status did not take the items back, so
# the items can still be returned.
_RETURN_DID_NOT_HAPPEN = ("denied", "closed")

# Refund types that already paid back the whole order.
_WHOLE_ORDER_REFUNDS = ("cancelled", "lost", "not received", "damaged", "warranty")


@dataclass(frozen=True)
class Item:
    """One line of the request: an item name from the order and how many."""

    name: str
    quantity: int


@dataclass(frozen=True)
class Request:
    """What the customer is asking for, as collected by the AI."""

    order_id: str
    reason: str
    # The items to send back. Leave empty for "cancel" and "not_received",
    # which are always about the whole order.
    items: tuple[Item, ...] = ()
    # Only asked for scented products: has the seal been opened?
    # None means the customer has not said yet.
    seal_opened: bool | None = None


@dataclass(frozen=True)
class Problem:
    """One reason why the request is not allowed, in plain words."""

    rule: str  # a short fixed name, used by tests and the admin panel
    text: str  # the sentence the customer can be told


@dataclass(frozen=True)
class Money:
    """How much would be paid back, worked out exactly like the Refund Policy."""

    item_refund: Decimal
    shipping_refunded: Decimal
    return_fee: Decimal
    net_refund: Decimal
    refunded_to: str  # "Original payment (Visa)" or "Store credit"
    free_return_label: bool


@dataclass(frozen=True)
class Check:
    """The result of `check_request`."""

    allowed: bool
    problems: tuple[Problem, ...] = ()
    money: Money | None = None
    # Why a person must look at it even though the policy allows it.
    staff_reasons: tuple[str, ...] = ()
    # A question the customer must answer before the rules can decide.
    question: str | None = None
    # Things the customer should know, for example the possible restocking fee.
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class Decision:
    """The result of `decide`: what happens next."""

    outcome: str  # APPROVE, NEEDS_STAFF, NOT_ALLOWED or NEED_INFO
    check: Check
    why: tuple[str, ...] = field(default_factory=tuple)


# --- Small helpers ------------------------------------------------------------------


def _cents(value: Any) -> Decimal:
    """Turn a price from the order file into an exact amount of money."""
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _day(value: Any) -> date | None:
    return date.fromisoformat(str(value)[:10]) if value else None


def _is_scented(name: str) -> bool:
    return any(word in name.lower() for word in SCENTED_WORDS)


def parse_items(text: str) -> tuple[Item, ...]:
    """Read the items of a past return, written like "Oak Side Table ×1, Candle ×2"."""
    items = []
    for part in text.split(", "):
        match = re.fullmatch(r"(.+?) ×(\d+)", part.strip())
        if match:
            items.append(Item(match.group(1), int(match.group(2))))
    return tuple(items)


def already_returned(order: dict[str, Any]) -> dict[str, int]:
    """How many of each item are already on their way back or returned."""
    counts: dict[str, int] = {}
    for record in order.get("returns") or []:
        status = str(record.get("status", "")).lower()
        if any(word in status for word in _RETURN_DID_NOT_HAPPEN):
            continue
        for item in parse_items(str(record.get("items", ""))):
            counts[item.name] = counts.get(item.name, 0) + item.quantity
    return counts


def whole_order_refunded(order: dict[str, Any]) -> bool:
    """True if the whole order was already paid back (cancelled, lost, damaged...)."""
    if order.get("status") in ("cancelled", "refunded"):
        return True
    for refund in order.get("refunds") or []:
        kind = str(refund.get("type", "")).lower()
        if any(word in kind for word in _WHOLE_ORDER_REFUNDS):
            return True
    return False


def _refunded_to(order: dict[str, Any]) -> str:
    # Refund Policy: "Orders paid with a gift card are refunded as store credit."
    method = str(order.get("payment_method", ""))
    if "gift card" in method.lower():
        return "Store credit"
    return f"Original payment ({method})"


# --- Step 1: what the policy allows -------------------------------------------------


def check_request(order: dict[str, Any], request: Request, today: date) -> Check:
    """Say whether the policy allows this request, and how much it would be.

    `order` must already belong to the signed-in customer: the caller checks
    that with `OrderStore.get_order_for_customer`.
    """
    if request.reason not in REASONS:
        return _refused("unknown_reason", "That is not a reason we can handle in the chat.")
    if whole_order_refunded(order):
        return _refused("already_refunded", "This order has already been cancelled or refunded.")

    if request.reason == CANCEL:
        return _check_cancel(order)
    if request.reason == NOT_RECEIVED:
        return _check_not_received(order)
    return _check_items(order, request, today)


def _refused(rule: str, text: str) -> Check:
    return Check(allowed=False, problems=(Problem(rule, text),))


def _whole_order_money(order: dict[str, Any]) -> Money:
    items = _cents(order.get("subtotal", 0))
    shipping = _cents(order.get("shipping_cost", 0))
    return Money(items, shipping, Decimal("0.00"), items + shipping, _refunded_to(order), False)


def _check_cancel(order: dict[str, Any]) -> Check:
    # FAQ: an order can be cancelled only while its status is "processing".
    if order.get("status") != "processing":
        return _refused(
            "already_dispatched",
            "This order has already been dispatched, so it can no longer be cancelled. "
            "It can be returned after it arrives.",
        )
    return Check(
        allowed=True,
        money=_whole_order_money(order),
        staff_reasons=("The warehouse must stop the order before it is dispatched.",),
    )


def _check_not_received(order: dict[str, Any]) -> Check:
    status = order.get("status")
    if status in ("processing",):
        return _refused("not_dispatched_yet", "This order has not been dispatched yet.")
    # Shipping Policy: the support team opens an investigation with the carrier,
    # and only a parcel confirmed lost is refunded. That is always a person's job.
    reason = (
        "The carrier has confirmed the parcel is lost."
        if status == "lost"
        else "The support team must open an investigation with the carrier first."
    )
    return Check(allowed=True, money=_whole_order_money(order), staff_reasons=(reason,))


def _check_items(order: dict[str, Any], request: Request, today: date) -> Check:
    if not request.items:
        return _refused("no_items", "Please say which items from the order this is about.")

    ordered = {item["name"]: item for item in order.get("items") or []}
    returned = already_returned(order)
    problems: list[Problem] = []
    lines: list[tuple[dict[str, Any], int]] = []
    for wanted in request.items:
        item = ordered.get(wanted.name)
        if item is None:
            problems.append(Problem("item_not_in_order", f"{wanted.name} is not in order {request_order(order)}."))
            continue
        left = int(item.get("quantity", 0)) - returned.get(wanted.name, 0)
        if wanted.quantity < 1 or wanted.quantity > left:
            text = (
                f"{wanted.name} has already been returned."
                if left <= 0
                else f"Only {left} of {wanted.name} can be returned from this order."
            )
            problems.append(Problem("too_many", text))
            continue
        lines.append((item, wanted.quantity))
    if problems:
        return Check(allowed=False, problems=tuple(problems))

    delivered = _day(order.get("delivered_on"))
    gift_cards_only = all(item.get("category") == GIFT_CARD for item, _ in lines)
    if delivered is None and not gift_cards_only:
        return _refused("not_delivered", "This order has not been delivered yet.")
    days = (today - delivered).days if delivered else 0

    # Rules about the kind of item.
    question = None
    for item, _ in lines:
        name, category = item["name"], item.get("category")
        if category == GIFT_CARD:
            # FAQ: gift cards "cannot be returned, refunded, or exchanged for cash".
            problems.append(Problem("gift_card", "Gift cards cannot be returned or refunded."))
        elif request.reason == CHANGED_MIND and category == PERSONALISED:
            problems.append(
                Problem("personalised", f"{name} is personalised, so it can only be returned if it is faulty or damaged.")
            )
        elif request.reason == CHANGED_MIND and _is_scented(name):
            if request.seal_opened is True:
                problems.append(
                    Problem("scented_opened", f"{name} cannot be returned because its seal has been opened.")
                )
            elif request.seal_opened is None:
                question = f"Has the seal on the {name} been opened?"

    # Rules about time.
    if request.reason == CHANGED_MIND and days > RETURN_WINDOW_DAYS:
        problems.append(Problem("late", _late_text(delivered, RETURN_WINDOW_DAYS, "returns")))
    if request.reason == WRONG_ITEM and days > WRONG_ITEM_DAYS:
        problems.append(Problem("late", _late_text(delivered, WRONG_ITEM_DAYS, "a wrong item")))
    # Damage should be reported within 7 days. Reported later, but still inside
    # the 30-day return window, it is not refused outright: a person decides
    # (it may count as a faulty item). After 30 days it is refused.
    damage_reported_late = request.reason == DAMAGED and DAMAGE_REPORT_DAYS < days <= RETURN_WINDOW_DAYS
    if request.reason == DAMAGED and days > RETURN_WINDOW_DAYS:
        problems.append(Problem("late", _late_text(delivered, RETURN_WINDOW_DAYS, "damage or returns")))

    if problems:
        return Check(allowed=False, problems=tuple(problems))
    if question:
        return Check(allowed=False, question=question)

    # The money, exactly as the Refund Policy says.
    item_refund = sum((_cents(item["unit_price"]) * quantity for item, quantity in lines), Decimal("0.00"))
    our_fault = request.reason in (FAULTY, DAMAGED, WRONG_ITEM)
    shipping = _cents(order.get("shipping_cost", 0)) if our_fault else Decimal("0.00")
    fee = Decimal("0.00") if our_fault else RETURN_FEE
    net = max(item_refund + shipping - fee, Decimal("0.00"))
    money = Money(item_refund, shipping, fee, net, _refunded_to(order), free_return_label=our_fault)

    staff: list[str] = []
    notes: list[str] = []
    if request.reason == FAULTY and days > RETURN_WINDOW_DAYS:
        staff.append("More than 30 days after delivery: this is a warranty claim.")
    elif request.reason == FAULTY:
        staff.append("The item is inspected when it comes back to confirm the fault.")
    if request.reason == DAMAGED:
        staff.append("The support team must see photos of the packaging and the item.")
    if damage_reported_late:
        staff.append(
            f"Reported {days} days after delivery, after the {DAMAGE_REPORT_DAYS}-day limit for damage "
            f"but within the {RETURN_WINDOW_DAYS}-day return window."
        )
    if request.reason == CHANGED_MIND:
        notes.append(
            f"If the item comes back used or without its original packaging, up to "
            f"{MAX_RESTOCKING_PERCENT}% of its price may be deducted after inspection."
        )
    return Check(allowed=True, money=money, staff_reasons=tuple(staff), notes=tuple(notes))


def request_order(order: dict[str, Any]) -> str:
    return str(order.get("order_id", "this order"))


def _late_text(delivered: date | None, days: int, what: str) -> str:
    when = f" (delivered on {delivered.isoformat()})" if delivered else ""
    return f"The {days}-day limit for {what} has passed for this order{when}."


# --- Step 2: approve now, or ask a person -------------------------------------------


def decide(
    check: Check,
    reason: str,
    *,
    limit: Decimal = AUTO_APPROVE_LIMIT,
    auto_reasons: tuple[str, ...] = AUTO_APPROVE_REASONS,
) -> Decision:
    """Turn a policy check into what happens next.

    Only small, simple requests are approved in the chat. Everything the
    policy allows but a person should look at goes to the support team.
    """
    if check.question:
        return Decision(NEED_INFO, check, (check.question,))
    if not check.allowed:
        return Decision(NOT_ALLOWED, check, tuple(problem.text for problem in check.problems))
    assert check.money is not None
    why: list[str] = list(check.staff_reasons)
    if reason not in auto_reasons:
        why.append("This kind of request is always checked by the support team.")
    if check.money.net_refund > limit:
        why.append(f"Refunds over {format_inr(limit)} are checked by the support team.")
    if why:
        return Decision(NEEDS_STAFF, check, tuple(why))
    return Decision(APPROVE, check, ())
