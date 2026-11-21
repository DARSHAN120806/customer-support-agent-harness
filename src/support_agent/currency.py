"""Money in the shop's currency, Indian rupees (₹).

The one place that knows how the shop writes money: "₹3,999", and with Indian
digit grouping for big amounts, "₹1,29,000" (one lakh twenty-nine thousand).

The cost of the AI service is NOT shop money: the AI service bills in US
dollars, so those costs stay in dollars everywhere.
"""

from __future__ import annotations

import re
from decimal import Decimal

SYMBOL = "₹"

# A rupee amount as people write it: "₹3,999", "₹ 699", "Rs. 1,299", "Rs 499",
# "INR 5,000". The first group is the number.
RUPEES = re.compile(r"(?:₹|\bRs\.?|\bINR)\s?(\d[\d,]*(?:\.\d+)?)", re.IGNORECASE)


def group_indian(whole: int) -> str:
    """12900 -> '12,900'; 129000 -> '1,29,000'; 10000000 -> '1,00,00,000'."""
    digits = str(abs(whole))
    if len(digits) > 3:
        head, last3 = digits[:-3], digits[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        groups.insert(0, head)
        digits = ",".join(groups) + "," + last3
    return ("-" if whole < 0 else "") + digits


def format_inr(amount: float | int | Decimal | str) -> str:
    """3999.0 -> '₹3,999'. Paise are shown only when there are some: '₹3,999.50'."""
    value = Decimal(str(amount)).quantize(Decimal("0.01"))
    whole = int(value)
    paise = abs(value - whole)
    text = SYMBOL + group_indian(whole)
    return text if paise == 0 else f"{text}.{int(paise * 100):02d}"


def parse_inr(text: str) -> float:
    """'₹1,29,000' -> 129000.0. Raises ValueError for anything else."""
    match = RUPEES.fullmatch(text.strip())
    if not match:
        raise ValueError(f"not a rupee amount: {text!r}")
    return round(float(match.group(1).replace(",", "")), 2)
