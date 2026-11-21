"""The refund and return tool: request_refund_or_return.

The AI collects the facts (order, items, reason) and calls this tool. The
decision is made here, in plain code, by refund_rules.py, never by the AI:

    approved           small, simple cases (refund_rules.decide): saved as approved
    sent to the team   allowed, but a person must decide: saved, with a ticket
    not allowed        the policy does not allow it: nothing is saved
    one question first a candle's seal: nothing is saved until the customer answers

The tool only writes a request record. It never changes the order data and
never moves any money.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from .. import event_log, refund_rules
from ..currency import format_inr
from ..orders import OrderStore, normalize_order_id
from ..prompts import SUPPORT_EMAIL
from ..refund_requests import (
    APPROVED,
    APPROVED_MARKER,
    STILL_OPEN,
    WAITING_FOR_STAFF,
    RefundRequestStore,
    with_earlier_requests,
)
from ..retry import call_with_retry
from ..tickets import TicketError, TicketStore
from .registry import Tool, ToolError, require_text

# More requests than this in one conversation means something is going wrong.
MAX_REQUESTS_PER_CONVERSATION = 3

REASON_WORDS = {
    refund_rules.CHANGED_MIND: "changed my mind / no longer wanted",
    refund_rules.FAULTY: "faulty",
    refund_rules.DAMAGED: "damaged on arrival",
    refund_rules.WRONG_ITEM: "wrong item received",
    refund_rules.NOT_RECEIVED: "parcel not received",
    refund_rules.CANCEL: "cancel before dispatch",
}


def _read_items(tool_input: dict[str, Any]) -> tuple[refund_rules.Item, ...]:
    raw = tool_input.get("items") or []
    if not isinstance(raw, list) or len(raw) > 20:
        raise ToolError("'items' must be a list of up to 20 items, each with a name and a quantity.")
    items = []
    for entry in raw:
        if not isinstance(entry, dict):
            raise ToolError("Each item must have a 'name' and a 'quantity'.")
        name = require_text(entry, "name", max_length=120)
        quantity = entry.get("quantity", 1)
        if isinstance(quantity, bool) or not isinstance(quantity, int) or not 1 <= quantity <= 20:
            raise ToolError("Each item's 'quantity' must be a whole number from 1 to 20.")
        items.append(refund_rules.Item(name.strip(), quantity))
    return tuple(items)


def _describe(request: refund_rules.Request) -> str:
    what = ", ".join(f"{item.name} ×{item.quantity}" for item in request.items) or "the whole order"
    return f"{what} from order {request.order_id} (reason: {REASON_WORDS[request.reason]})"


def _money_lines(money: refund_rules.Money) -> str:
    lines = [f"Items: {format_inr(money.item_refund)}."]
    if money.shipping_refunded:
        lines.append(f"Shipping refunded: {format_inr(money.shipping_refunded)}.")
    if money.return_fee:
        lines.append(f"Return fee taken off: {format_inr(money.return_fee)}.")
    lines.append(f"Refund: {format_inr(money.net_refund)}, to {money.refunded_to}.")
    return " ".join(lines)


def make_refund_tool(
    session: Any,
    orders: OrderStore,
    tickets: TicketStore,
    requests: RefundRequestStore,
    today: date,
    create_ticket: Any,
) -> Tool:
    def handle(tool_input: dict[str, Any]) -> str:
        order_id = normalize_order_id(require_text(tool_input, "order_id", max_length=40))
        if order_id is None:
            raise ToolError("That is not a valid order ID. Order IDs look like JL-10231.")
        reason = require_text(tool_input, "reason", max_length=40)
        if reason not in refund_rules.REASONS:
            raise ToolError(f"'reason' must be one of: {', '.join(refund_rules.REASONS)}.")
        items = _read_items(tool_input) if reason in refund_rules.ITEM_REASONS else ()
        seal = tool_input.get("seal_opened")
        if seal is not None and not isinstance(seal, bool):
            raise ToolError("'seal_opened' must be true or false, or left out.")
        details = str(tool_input.get("details") or "")[:1000]

        order = orders.get_order_for_customer(order_id, session.customer_email)
        if order is None:
            # The same text as lookup_order, so nothing about other customers leaks.
            return (
                f"No order {order_id} was found for the signed-in customer. "
                "Either the order ID is wrong, or the order was placed with a "
                "different email address. Nothing was created."
            )

        earlier = [r for r in requests.for_order(order_id, session.customer_email) if r.get("status") in STILL_OPEN]
        if reason in (refund_rules.CANCEL, refund_rules.NOT_RECEIVED):
            same = next((r for r in earlier if r.get("reason") == reason), None)
            if same:
                return (
                    f"Request {same['request_id']} already covers this ({same['status'].replace('_', ' ')}). "
                    "Nothing new was created. Give the customer that request number."
                )
        if len(session.refund_request_ids) >= MAX_REQUESTS_PER_CONVERSATION:
            raise ToolError(
                "The limit of requests for one conversation has been reached. Hand over with "
                "escalate_to_human instead."
            )

        request = refund_rules.Request(order_id, reason, items, seal)
        check = refund_rules.check_request(with_earlier_requests(order, earlier), request, today)
        decision = refund_rules.decide(check, reason)

        session.logger.log(
            event_log.REFUND_REQUEST,
            order_id=order_id,
            reason=reason,
            items=[f"{i.name} ×{i.quantity}" for i in items],
            outcome=decision.outcome,
            rules=[p.rule for p in check.problems],
            net_refund=str(check.money.net_refund) if check.money else None,
        )

        if decision.outcome == refund_rules.NEED_INFO:
            return (
                f'ONE QUESTION FIRST. Nothing was created yet. Ask the customer: "{check.question}" '
                "Then call request_refund_or_return again with seal_opened set to their answer."
            )

        if decision.outcome == refund_rules.NOT_ALLOWED:
            if any(p.rule == "item_not_in_order" for p in check.problems):
                names = "; ".join(i["name"] for i in order.get("items") or [])
                return (
                    f"An item name does not match the order. Nothing was created. The items on "
                    f"order {order_id} are: {names}. Use the names exactly as written here, or ask "
                    "the customer which item they mean."
                )
            why = " ".join(p.text for p in check.problems)
            return (
                f"NOT ALLOWED BY THE SHOP'S POLICY. Nothing was created. Why: {why} "
                "Explain this to the customer kindly, in your own words, without promising anything "
                "else. If they disagree or think there is a mistake, offer to hand over to the "
                "support team with escalate_to_human."
            )

        assert check.money is not None
        if decision.outcome == refund_rules.APPROVE:
            try:
                record = call_with_retry(
                    lambda: requests.create(
                        customer_email=session.customer_email,
                        conversation_id=session.logger.conversation_id or None,
                        request=request,
                        decision=decision,
                        status=APPROVED,
                        details=details,
                    ),
                    session.retry_policy,
                )
            except TicketError as error:
                raise _not_saved() from error
            session.refund_request_ids.append(record["request_id"])
            label = (
                "A free return label is emailed within 1 business day."
                if check.money.free_return_label
                else "A return label is emailed within 1 business day."
            )
            notes = " ".join(check.notes)
            return (
                f"{APPROVED_MARKER}. Request {record['request_id']}: return of {_describe(request)}. "
                f"{_money_lines(check.money)} "
                f"Next steps: {label} Drop the parcel off with the carrier within 14 days of receiving "
                "the label. The item is inspected within 3 business days of arriving, and the refund "
                f"is then sent within 5–7 business days. {notes} "
                "Tell the customer the request number, that the return is approved, and these amounts "
                "and steps exactly as written here. Do not add other amounts or dates."
            )

        # Allowed by the policy, but a person decides.
        ticket_reason = "return_request" if reason in refund_rules.ITEM_REASONS else "refund_request"
        ticket_id = session.tickets_by_issue.get((ticket_reason, order_id))
        why = " ".join(decision.why)
        if ticket_id is None:
            summary = (
                f"Refund/return request from the chat: {_describe(request)}. "
                f"The shop's rules allow it and worked out: {_money_lines(check.money)} "
                f"A person must decide because: {why} Customer's words: {details or '(none)'}"
            )
            try:
                ticket_id = create_ticket(
                    session, tickets, reason=ticket_reason, summary=summary[:1500], order_id=order_id,
                    created_by="model",
                )
            except TicketError as error:
                raise _not_saved() from error
        try:
            record = call_with_retry(
                lambda: requests.create(
                    customer_email=session.customer_email,
                    conversation_id=session.logger.conversation_id or None,
                    request=request,
                    decision=decision,
                    status=WAITING_FOR_STAFF,
                    ticket_id=ticket_id,
                    details=details,
                ),
                session.retry_policy,
            )
        except TicketError as error:
            raise _not_saved() from error
        session.refund_request_ids.append(record["request_id"])
        return (
            f"SENT TO THE SUPPORT TEAM. Ticket {ticket_id} (request {record['request_id']}). "
            f"The policy allows this request, but a person must decide because: {why} "
            "Tell the customer the ticket number and that a person from the support team will "
            "review it and reply. Do not say it is approved, and do not promise an amount or a date."
        )

    return Tool(
        name="request_refund_or_return",
        description=(
            "Start a refund, return or cancellation for one of the signed-in customer's orders. "
            "The shop's rules decide the outcome, not you: small, simple returns are approved "
            "straight away, others go to the support team with a ticket, and some are not "
            "allowed by the policy. Look the order up first, and use the item names exactly as "
            "lookup_order shows them. Only call this when the customer clearly asks for a "
            "refund, return or cancellation, and report the result exactly as it is returned."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The order, e.g. 'JL-10231'."},
                "reason": {
                    "type": "string",
                    "enum": list(refund_rules.REASONS),
                    "description": (
                        "changed_mind: no longer wanted, bought by mistake, colour or size not right. "
                        "faulty: does not work properly. damaged_on_arrival: arrived broken. "
                        "wrong_item: not what was ordered. not_received: the parcel never arrived. "
                        "cancel: stop an order that has not been dispatched."
                    ),
                },
                "items": {
                    "type": "array",
                    "description": "The items to return, for every reason except cancel and not_received.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Exactly as on the order."},
                            "quantity": {"type": "integer", "description": "How many. Default 1."},
                        },
                        "required": ["name"],
                        "additionalProperties": False,
                    },
                },
                "seal_opened": {
                    "type": "boolean",
                    "description": "Only for candles and scented products: has the seal been opened?",
                },
                "details": {
                    "type": "string",
                    "description": "What the customer said about the problem, for the support team.",
                },
            },
            "required": ["order_id", "reason"],
            "additionalProperties": False,
        },
        handler=handle,
        read_only=False,
        # Anything written before the rules answer is a guess ("I'll approve that"),
        # so it is never shown. The reply after the result is.
        shows_text_alongside=False,
    )


def _not_saved() -> ToolError:
    return ToolError(
        "The request could not be saved, so nothing was created. Apologise, do not give a "
        f"request or ticket number, and ask the customer to email {SUPPORT_EMAIL}."
    )
