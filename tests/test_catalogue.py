"""Tests for reading the shop's product list from its own document."""

from __future__ import annotations

from pathlib import Path

import pytest

from support_agent.catalogue import load_catalogue, slugify
from support_agent.config import ConfigError

KB = Path(__file__).resolve().parents[1] / "data" / "knowledge_base"


def test_every_product_in_the_shop_document_is_listed():
    products = {p.name: p for p in load_catalogue(KB)}

    assert len(products) == 16
    speaker = products["Bluetooth Speaker Mini"]
    assert (speaker.category, speaker.price, speaker.warranty) == ("Electronics", 39.99, "1 year")
    assert products["Oak Side Table"].warranty == "2 years"


def test_stock_levels_come_from_the_same_document():
    products = {p.name: p for p in load_catalogue(KB)}

    assert products["Wool Throw Blanket"].stock_status == "Out of stock"
    assert products["Wool Throw Blanket"].units_in_stock == 0
    assert (products["Ceramic Planter Set"].stock_status, products["Ceramic Planter Set"].units_in_stock) == ("Low stock", 9)


def test_the_gift_card_has_amounts_to_choose_from_instead_of_one_price():
    (card,) = [p for p in load_catalogue(KB) if p.category == "Gift card"]

    assert card.price is None and card.price_options == [25.0, 50.0, 100.0]
    assert card.stock_status == "In stock" and card.units_in_stock is None


def test_slugs_are_safe_for_web_addresses():
    assert slugify("Linen Napkins (Set of 4)") == "linen-napkins-set-of-4"
    assert slugify("Electric Kettle 1.7L") == "electric-kettle-1-7l"
    assert len({p.slug for p in load_catalogue(KB)}) == 16  # all different


def test_a_missing_document_or_table_is_reported_plainly(tmp_path):
    with pytest.raises(ConfigError, match="could not be read"):
        load_catalogue(tmp_path)

    (tmp_path / "company_overview.md").write_text("# Company Overview\n\nNo tables here.\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="Product catalogue and prices"):
        load_catalogue(tmp_path)


def test_a_small_document_is_read_the_same_way(tmp_path):
    (tmp_path / "company_overview.md").write_text(
        "## Product catalogue and prices\n\n"
        "| Product | Category | Price | Warranty |\n|---|---|---|---|\n"
        "| Teapot | Homeware | $20.00 | None |\n\n"
        "## Something else\n\n| A | B |\n|---|---|\n| x | y |\n",
        encoding="utf-8",
    )
    (teapot,) = load_catalogue(tmp_path)

    assert (teapot.slug, teapot.price, teapot.stock_status) == ("teapot", 20.0, "In stock")
