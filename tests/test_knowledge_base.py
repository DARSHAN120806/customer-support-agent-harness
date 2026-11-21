"""Tests for loading and searching the shop's documents."""

from __future__ import annotations

from conftest import DATA_DIR
from fakes import FakeEmbedder

from support_agent.knowledge_base import KnowledgeBase, load_chunks


def test_documents_are_split_into_sections():
    chunks = load_chunks(DATA_DIR / "knowledge_base")

    sources = {chunk.source for chunk in chunks}
    assert sources == {
        "company_overview.md",
        "faq.md",
        "refunds.md",
        "returns.md",
        "shipping.md",
        "warranty.md",
    }
    return_window = next(chunk for chunk in chunks if chunk.section == "Return window")
    assert return_window.title == "Returns Policy"
    assert "30 days" in return_window.text
    # The one-line "last updated" note under each title is not kept as a section.
    assert all(chunk.section != "Introduction" for chunk in chunks)


def test_search_finds_the_right_section(knowledge_base):
    hits = knowledge_base.search("How much does express shipping cost?")

    assert hits[0].chunk.section == "Shipping options and prices"
    assert "₹1,299" in hits[0].chunk.text


def test_search_finds_a_product_in_the_price_table(knowledge_base):
    hits = knowledge_base.search("price of the Oak Side Table")

    assert any("₹12,900" in hit.chunk.text for hit in hits)


def test_search_returns_best_match_first_and_at_most_top_k(knowledge_base):
    hits = knowledge_base.search("return an item within the return window")

    assert 1 <= len(hits) <= 6
    assert [hit.score for hit in hits] == sorted((hit.score for hit in hits), reverse=True)


def test_unrelated_question_returns_nothing(knowledge_base):
    assert knowledge_base.search("zebra astronomy volcano") == []


def test_embeddings_are_cached_and_only_changed_text_is_embedded_again(tmp_path):
    folder = tmp_path / "docs"
    folder.mkdir()
    (folder / "a.md").write_text("# Doc\n\n## One\nFirst section.\n\n## Two\nSecond section.\n", encoding="utf-8")
    cache = tmp_path / "cache" / "embeddings.json"

    first = FakeEmbedder()
    KnowledgeBase.build(folder, first, cache_path=cache)
    assert first.calls == 2

    second = FakeEmbedder()
    KnowledgeBase.build(folder, second, cache_path=cache)
    assert second.calls == 0

    (folder / "a.md").write_text("# Doc\n\n## One\nFirst section.\n\n## Two\nChanged text.\n", encoding="utf-8")
    third = FakeEmbedder()
    KnowledgeBase.build(folder, third, cache_path=cache)
    assert third.calls == 1


def test_cache_from_another_embedding_model_is_not_reused(tmp_path):
    folder = tmp_path / "docs"
    folder.mkdir()
    (folder / "a.md").write_text("# Doc\n\n## One\nFirst section.\n", encoding="utf-8")
    cache = tmp_path / "embeddings.json"
    KnowledgeBase.build(folder, FakeEmbedder(), cache_path=cache)

    other = FakeEmbedder()
    other.name = "a-different-model"
    KnowledgeBase.build(folder, other, cache_path=cache)
    assert other.calls == 1
