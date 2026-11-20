"""Tests for the plain-language meaning of warranty claim statuses.

Added after the agent read "Approved — awaiting product" as "a replacement is
on its way", when it means the shop is waiting for the customer's product."""

from __future__ import annotations

import importlib.util
import json
import re

from conftest import DATA_DIR

from support_agent.prompts import build_system_prompt

ROOT = DATA_DIR.parent


def importer():
    path = ROOT / "scripts" / "import_synthetic_data.py"
    spec = importlib.util.spec_from_file_location("import_synthetic_data", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def claims() -> list[dict]:
    data = json.loads((DATA_DIR / "orders.json").read_text(encoding="utf-8"))
    return [claim for order in data["orders"] for claim in order.get("warranty_claims", [])]


def test_every_claim_carries_the_meaning_of_its_status():
    meanings = importer().CLAIM_STATUS_MEANING

    assert claims()
    for claim in claims():
        assert claim["status_meaning"] == meanings[claim["status"]], claim["claim_id"]


def test_the_meaning_sits_right_after_the_status():
    for claim in claims():
        keys = list(claim)
        assert keys.index("status_meaning") == keys.index("status") + 1, claim["claim_id"]


def test_awaiting_product_says_the_customer_must_send_it_and_nothing_was_sent_yet():
    meaning = importer().CLAIM_STATUS_MEANING["Approved — awaiting product"]

    assert "customer now needs to send the product back" in meaning
    assert "Nothing has been repaired, replaced, or refunded yet" in meaning


def test_the_policy_document_explains_the_same_statuses_in_the_same_words():
    policy = (DATA_DIR / "knowledge_base" / "warranty.md").read_text(encoding="utf-8")
    section = policy.split("## Warranty claim statuses", 1)[1].split("\n## ", 1)[0]

    for status, meaning in importer().CLAIM_STATUS_MEANING.items():
        assert f"| {status} | {meaning} |" in section, status


def test_meanings_only_use_figures_from_the_policies():
    policy = (DATA_DIR / "knowledge_base" / "warranty.md").read_text(encoding="utf-8")
    policy += (DATA_DIR / "knowledge_base" / "refunds.md").read_text(encoding="utf-8")
    original = policy.split("## Warranty claim statuses")[0] + policy.split("## Replacements under warranty")[1]

    for meaning in importer().CLAIM_STATUS_MEANING.values():
        for figure in re.findall(r"\d+(?:–\d+)? (?:business )?days", meaning):
            assert figure in original, figure


def test_a_new_status_without_a_meaning_stops_the_import(monkeypatch):
    module = importer()
    monkeypatch.setitem(module.CLAIM_STATUS_MEANING, "Under review", None)
    monkeypatch.delitem(module.CLAIM_STATUS_MEANING, "Under review")

    try:
        module.build()
    except ValueError as error:
        assert "no meaning written for status 'Under review'" in str(error)
    else:
        raise AssertionError("the import should have stopped")


def test_the_prompt_tells_the_agent_to_report_records_exactly():
    prompt = build_system_prompt()

    assert "status_meaning" in prompt
    assert "Say only what the record shows has happened" in prompt


def test_the_status_section_can_be_found_by_search(knowledge_base):
    hits = knowledge_base.search("What does the warranty claim status 'Approved — awaiting product' mean?")

    assert any(hit.chunk.section == "Warranty claim statuses" for hit in hits)


def test_claims_under_review_show_no_outcome_before_a_decision():
    under_review = [claim for claim in claims() if claim["status"] == "Under review"]

    assert len(under_review) == 5
    for claim in under_review:
        assert "outcome" not in claim and "decided_on" not in claim, claim["claim_id"]
    internal = (DATA_DIR / "internal" / "business_records.md").read_text(encoding="utf-8")
    assert "| WC-40075 | JL-10639 | Cracked casing from a drop (accidental damage) |" in internal
