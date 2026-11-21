"""The shop's product list, read from the shop's own document.

Products, prices, warranties and stock levels come from the two tables in
data/knowledge_base/company_overview.md ("Product catalogue and prices" and
"Stock levels"). That is the same document the assistant searches, so the shop
page and the assistant can never disagree about a price.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .config import ConfigError
from .currency import RUPEES

OVERVIEW_FILE = "company_overview.md"
CATALOGUE_HEADING = "Product catalogue and prices"
STOCK_HEADING = "Stock levels"
MONEY = RUPEES  # "₹3,999"; prices are in Indian rupees


@dataclass(frozen=True)
class Product:
    slug: str  # a short name for web addresses and pictures, like "oak-side-table"
    name: str
    category: str
    price: float | None  # None when the buyer picks an amount (the gift card)
    price_options: list[float] = field(default_factory=list)
    warranty: str = ""
    stock_status: str = "In stock"  # "In stock", "Low stock" or "Out of stock"
    units_in_stock: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_catalogue(knowledge_base_dir: Path) -> list[Product]:
    path = knowledge_base_dir / OVERVIEW_FILE
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise ConfigError(f"The product list could not be read from {path} ({error}).") from error

    rows = _table_rows(text, CATALOGUE_HEADING)
    if not rows:
        raise ConfigError(f'No "{CATALOGUE_HEADING}" table was found in {path}.')
    stock = {r[0]: r for r in _table_rows(text, STOCK_HEADING)}

    products = []
    for name, category, price_text, warranty, *_ in rows:
        amounts = [float(a.replace(",", "")) for a in MONEY.findall(price_text)]
        single = len(amounts) == 1
        level = stock.get(name)
        products.append(
            Product(
                slug=slugify(name),
                name=name,
                category=category,
                price=amounts[0] if single else None,
                price_options=[] if single else amounts,
                warranty=warranty,
                # Items without a stock line (the gift card) never run out.
                stock_status=level[1] if level else "In stock",
                units_in_stock=int(level[2]) if level and level[2].isdigit() else None,
            )
        )
    return products


def slugify(name: str) -> str:
    """'Linen Napkins (Set of 4)' becomes 'linen-napkins-set-of-4'."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _table_rows(text: str, heading: str) -> list[list[str]]:
    """The body rows of the first table under a '## heading', as lists of cells."""
    match = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return []
    rows = []
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if set("".join(cells)) <= set("-: "):  # the |---|---| line
            continue
        rows.append(cells)
    return rows[1:]  # without the header row
