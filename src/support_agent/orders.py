"""Order data: reading orders from the JSON file.

This is the only place that reads order data, and it only ever hands out an
order to the customer who placed it.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ORDER_ID_PATTERN = re.compile(r"^JL-\d{5}$")


def normalize_order_id(raw: str) -> str | None:
    """Tidy up an order ID typed by a customer. Returns None if it cannot be a
    real order ID."""
    order_id = raw.strip().upper().replace(" ", "")
    return order_id if ORDER_ID_PATTERN.match(order_id) else None


def normalize_email(raw: str) -> str:
    return raw.strip().lower()


class OrderStore:
    def __init__(self, path: Path) -> None:
        data = json.loads(path.read_text(encoding="utf-8"))
        customers = {customer["customer_id"]: customer for customer in data["customers"]}
        self._orders: dict[str, dict[str, Any]] = {}
        self._owner_email: dict[str, str] = {}
        for order in data["orders"]:
            customer = customers[order["customer_id"]]
            self._orders[order["order_id"]] = order
            self._owner_email[order["order_id"]] = normalize_email(customer["email"])

    def get_order_for_customer(self, order_id: str, customer_email: str) -> dict[str, Any] | None:
        """Return the order only if it belongs to this customer.

        An order that does not exist and an order that belongs to someone else
        both return None, on purpose: the caller must not be able to tell the
        difference, or it could be used to discover other customers' order IDs.
        """
        order = self._orders.get(order_id)
        if order is None or self._owner_email[order_id] != normalize_email(customer_email):
            return None
        # A copy without the internal customer number, so the stored data cannot
        # be changed by accident.
        return {key: value for key, value in order.items() if key != "customer_id"}
