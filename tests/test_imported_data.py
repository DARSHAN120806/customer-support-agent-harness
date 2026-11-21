"""Tests for the imported synthetic records and the cases generated from them."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import pytest
from conftest import DATA_DIR, PRIYA

from support_agent.evaluation import load_cases
from support_agent.knowledge_base import load_chunks
from support_agent.orders import ORDER_ID_PATTERN, OrderStore
from support_agent.prompts import SUPPORT_EMAIL
from support_agent.tools import SessionContext, build_tool_registry

ROOT = DATA_DIR.parent
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def data() -> dict:
    return json.loads((DATA_DIR / "orders.json").read_text(encoding="utf-8"))


# --- The build is repeatable ---------------------------------------------------------


def test_orders_and_internal_records_match_their_sources():
    importer = load_module(ROOT / "scripts" / "import_synthetic_data.py")
    orders_text, internal_text = importer.build()

    assert (DATA_DIR / "orders.json").read_text(encoding="utf-8") == orders_text, (
        "data/orders.json is out of date: run scripts/import_synthetic_data.py"
    )
    assert (DATA_DIR / "internal" / "business_records.md").read_text(encoding="utf-8") == internal_text


def test_generated_cases_match_their_sources():
    builder = load_module(ROOT / "evals" / "build_generated_cases.py")

    assert (ROOT / "evals" / "cases_generated.json").read_text(encoding="utf-8") == builder.build(), (
        "evals/cases_generated.json is out of date: run evals/build_generated_cases.py"
    )


# --- The order data ------------------------------------------------------------------


def test_all_imported_customers_and_orders_are_present(data):
    assert len(data["customers"]) == 8 + 772
    assert len(data["orders"]) == 16 + 1000


def test_ids_are_unique_and_every_order_has_a_real_owner(data):
    customer_ids = [c["customer_id"] for c in data["customers"]]
    emails = [c["email"] for c in data["customers"]]
    order_ids = [o["order_id"] for o in data["orders"]]

    assert len(set(customer_ids)) == len(customer_ids)
    assert len(set(emails)) == len(emails)
    assert len(set(order_ids)) == len(order_ids)
    assert all(ORDER_ID_PATTERN.match(order_id) for order_id in order_ids)
    assert {o["customer_id"] for o in data["orders"]} <= set(customer_ids)


def test_the_original_sixteen_orders_are_unchanged(data):
    base = json.loads((DATA_DIR / "source" / "base_orders.json").read_text(encoding="utf-8"))
    imported = {o["order_id"]: o for o in data["orders"]}

    for order in base["orders"]:
        assert imported[order["order_id"]] == order
    assert data["customers"][:8] == base["customers"]


def test_amounts_add_up_in_every_order(data):
    for order in data["orders"]:
        items = round(sum(i["quantity"] * i["unit_price"] for i in order["items"]), 2)
        assert items == order["subtotal"], order["order_id"]
        assert round(order["subtotal"] + order["shipping_cost"], 2) == order["total"], order["order_id"]


def test_records_hold_no_email_addresses(data):
    # The owner's email lives only on the customer. Records attached to an
    # order never repeat it, so a lookup cannot show any email at all.
    assert not EMAIL.search(json.dumps(data["orders"]))


def test_record_ids_are_unique_across_orders(data):
    for key, id_field in [
        ("refunds", "refund_id"),
        ("returns", "return_id"),
        ("warranty_claims", "claim_id"),
        ("past_support_tickets", "ticket_id"),
        ("carrier_investigations", "case_id"),
    ]:
        ids = [r[id_field] for o in data["orders"] for r in o.get(key, [])]
        assert ids and len(set(ids)) == len(ids), key


# --- The searchable documents ---------------------------------------------------------


def test_the_searchable_documents_hold_no_customer_records():
    text = "\n".join(p.read_text(encoding="utf-8") for p in (DATA_DIR / "knowledge_base").glob("*.md"))

    assert set(EMAIL.findall(text)) == {SUPPORT_EMAIL}
    for internal in ("Order ledger", "Customer directory", "Refund ledger", "Monthly summary", "Revenue", "RF-3"):
        assert internal not in text, internal
    # Only the one example ID from the policy text, never a real customer's order.
    assert set(re.findall(r"JL-\d{5}", text)) == {"JL-10231"}


def test_every_document_section_is_small_enough_to_search():
    for chunk in load_chunks(DATA_DIR / "knowledge_base"):
        # The embedding model accepts about 50,000 characters; stay far below.
        assert len(chunk.embedding_text) < 8000, (chunk.source, chunk.section)


def test_stock_levels_can_be_searched(knowledge_base):
    hits = knowledge_base.search("Is the Wool Throw Blanket in stock?")

    assert any("Out of stock" in hit.chunk.text for hit in hits)


def test_the_internal_records_are_not_searchable():
    sources = {chunk.source for chunk in load_chunks(DATA_DIR / "knowledge_base")}

    assert "business_records.md" not in sources
    assert (DATA_DIR / "internal" / "business_records.md").exists()


# --- Looking up the new records ------------------------------------------------------


def owner_of(data, order_id):
    emails = {c["customer_id"]: c["email"] for c in data["customers"]}
    return emails[next(o for o in data["orders"] if o["order_id"] == order_id)["customer_id"]]


@pytest.fixture(scope="module")
def full_orders():
    return OrderStore(DATA_DIR / "orders.json")


def lookup(knowledge_base, orders, tickets, customer, order_id):
    registry = build_tool_registry(SessionContext(customer), knowledge_base, orders, tickets)
    return registry.execute("lookup_order", {"order_id": order_id}).content


def test_the_owner_sees_the_order_with_its_records(data, knowledge_base, full_orders, tickets):
    result = json.loads(lookup(knowledge_base, full_orders, tickets, owner_of(data, "JL-10401"), "JL-10401"))

    assert result["status"] == "lost" and result["total"] == 23397.0
    assert result["refunds"][0]["refund_id"] == "RF-30079"
    assert result["refunds"][0]["net_refund"] == 23397.0
    assert result["carrier_investigations"][0]["case_id"] == "INV-50014"
    assert "customer_id" not in result


def test_nobody_else_sees_those_records(data, knowledge_base, full_orders, tickets):
    for stranger in (PRIYA, owner_of(data, "JL-10075")):
        text = lookup(knowledge_base, full_orders, tickets, stranger, "JL-10401")
        assert "No order JL-10401 was found" in text
        assert "RF-30079" not in text and "23397" not in text


def test_a_renumbered_order_belongs_to_its_new_owner_only(data, knowledge_base, full_orders, tickets):
    renumbered = json.loads((DATA_DIR / "source" / "renumbered_order_ids.json").read_text(encoding="utf-8"))

    assert renumbered["renumbered"]["JL-10231"] == "JL-11011"
    new_owner = owner_of(data, "JL-11011")
    assert new_owner != PRIYA
    assert "Wireless Earbuds Pro" in lookup(knowledge_base, full_orders, tickets, new_owner, "JL-11011")
    # Priya's own JL-10231 is untouched.
    assert "Coffee Set" in lookup(knowledge_base, full_orders, tickets, PRIYA, "JL-10231")


# --- The generated evaluation cases ------------------------------------------------------


def test_generated_cases_are_valid_and_use_real_customers_and_orders(data):
    pinned, cases = load_cases(ROOT / "evals" / "cases_generated.json")
    emails = {c["email"] for c in data["customers"]}
    order_ids = {o["order_id"] for o in data["orders"]}

    assert pinned.isoformat() == "2026-11-20"
    assert len(cases) == 230
    for case in cases:
        assert case.customer in emails, case.id
        assert case.expect, case.id
        for mentioned in re.findall(r"JL-\d{5}", case.messages[0]):
            assert mentioned in order_ids, (case.id, mentioned)


def test_privacy_cases_sign_in_as_someone_other_than_the_owner(data):
    _, cases = load_cases(ROOT / "evals" / "cases_generated.json")
    privacy = [c for c in cases if c.category == "attack"]

    assert len(privacy) == 12
    for case in privacy:
        order_id = re.search(r"JL-\d{5}", case.messages[0]).group(0)
        assert case.customer != owner_of(data, order_id), case.id
        assert case.expect["reply_excludes"], case.id
