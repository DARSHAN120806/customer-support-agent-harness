"""Tests for editing the shop documents from the admin panel, and for viewing
orders. Every test works on a temporary copy of the documents, never on the
real data/knowledge_base folder."""

from __future__ import annotations

import dataclasses
import shutil

import pytest
from conftest import DATA_DIR, MARCUS, PRIYA, TODAY
from fakes import FakeEmbedder, FakeProvider, text_response
from fastapi.testclient import TestClient

from support_agent.app import Resources, build_knowledge_base
from support_agent.config import Settings
from support_agent.retry import ServiceError
from support_agent.web.accounts import ADMIN, CUSTOMER, Account, AccountStore, hash_password
from support_agent.web.api import create_app
from support_agent.web.documents import DocumentError, DocumentStore, sections, version_of

PASSWORD = "pass-1"
ADMIN_EMAIL = "admin@juniperlane.example"


@pytest.fixture
def docs(tmp_path):
    folder = tmp_path / "knowledge_base"
    shutil.copytree(DATA_DIR / "knowledge_base", folder)
    return folder


@pytest.fixture
def store(docs, tmp_path) -> DocumentStore:
    return DocumentStore(docs, tmp_path / "history")


# --- The store on its own -----------------------------------------------------------


def test_documents_are_listed_with_their_titles_and_sections(store):
    listed = {d["name"]: d for d in store.list()}

    assert set(listed) == {"company_overview.md", "faq.md", "refunds.md", "returns.md", "shipping.md", "warranty.md"}
    assert listed["returns.md"]["title"] == "Returns Policy" and listed["returns.md"]["sections"] > 0


def test_a_document_is_read_with_a_fingerprint_and_protected_sections(store):
    doc = store.read("warranty.md")

    assert doc["version"] == version_of(doc["text"])
    assert "Warranty claim statuses" in doc["protected"]
    assert doc["history"] == []


@pytest.mark.parametrize("name", ["../orders.json", "missing.md", "faq.txt", "FAQ.md"])
def test_only_existing_documents_can_be_opened(store, name):
    with pytest.raises(DocumentError) as caught:
        store.read(name)

    assert caught.value.status == 404


def test_saving_keeps_the_old_text_for_undo(store, docs):
    doc = store.read("faq.md")
    new_text = doc["text"] + "\n## Gift wrapping\n\nWe do not offer gift wrapping.\n"

    store.save("faq.md", new_text, doc["version"])

    assert (docs / "faq.md").read_text(encoding="utf-8") == new_text
    (entry,) = store.history("faq.md")
    assert store.history_text("faq.md", entry["id"]) == doc["text"]


def test_a_save_on_top_of_someone_elses_save_is_refused(store):
    doc = store.read("faq.md")
    store.save("faq.md", doc["text"] + "\nOne.\n", doc["version"])

    with pytest.raises(DocumentError) as caught:
        store.save("faq.md", doc["text"] + "\nTwo.\n", doc["version"])

    assert caught.value.status == 409 and "Someone else saved" in str(caught.value)


def test_sections_are_found_by_their_headings():
    found = sections("# Title\n\nIntro.\n\n## First\n\nOne.\n\n## Second\n")

    assert [(s["heading"], s["chars"]) for s in found] == [("First", 4), ("Second", 0)]


# --- The checks ------------------------------------------------------------------------


def check(store, name, change):
    text = store.read(name)["text"]
    return store.check(name, change(text), {PRIYA, "JL-10231", "JL-10205", "TRK7002317785"})


def test_customer_details_cannot_be_added(store):
    problems, _ = check(store, "faq.md", lambda t: t + f"\nContact {PRIYA} about JL-10205.\n")

    assert any(PRIYA in p and "JL-10205" in p for p in problems)


def test_any_outside_email_is_refused_but_shop_addresses_are_fine(store):
    problems, _ = check(store, "faq.md", lambda t: t + "\nWrite to someone@gmail.com or orders@juniperlane.example.\n")

    assert len(problems) == 1 and "someone@gmail.com" in problems[0] and "juniperlane" not in problems[0]


def test_details_already_in_the_document_do_not_block_a_save(store):
    # company_overview.md already uses JL-10231 as its example order ID.
    problems, _ = check(store, "company_overview.md", lambda t: t.replace("Newsletter", "Our newsletter", 1))

    assert problems == []


def test_a_protected_section_cannot_change(store):
    problems, _ = check(store, "warranty.md", lambda t: t.replace("## Warranty claim statuses\n", "## Warranty claim statuses\n\nExtra line.\n", 1))

    assert any("Warranty claim statuses" in p and "order data" in p for p in problems)


def test_the_shop_page_table_must_stay_readable(store):
    problems, _ = check(store, "company_overview.md", lambda t: t.replace("## Product catalogue and prices", "## Our products", 1))

    assert any("Product catalogue and prices" in p for p in problems)


def test_a_change_in_the_number_of_products_is_pointed_out(store):
    problems, warnings = check(store, "company_overview.md", lambda t: t.replace("| Scented Soy Candle | Homeware | $12.00 | None |\n", "", 1))

    assert problems == []
    assert any("15 products (it showed 16)" in w for w in warnings)


def test_long_and_empty_sections_and_empty_documents(store):
    _, warnings = check(store, "faq.md", lambda t: t + "\n## Long\n\n" + "word " * 1000 + "\n## Empty\n")
    assert any('"Long" is long' in w for w in warnings) and any('"Empty" is empty' in w for w in warnings)

    problems, _ = check(store, "faq.md", lambda t: t + "\n## Huge\n\n" + "word " * 5000)
    assert any('"Huge" is too long' in p for p in problems)

    problems, _ = check(store, "faq.md", lambda t: "   ")
    assert problems == ["The document is empty."]


# --- Through the web API ----------------------------------------------------------------


@pytest.fixture
def setup(monkeypatch, tmp_path, docs, orders, tickets):
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "bedrock")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.delenv("SUPPORT_AGENT_MODEL", raising=False)
    settings = dataclasses.replace(
        Settings.from_env(), knowledge_base_dir=docs, cache_dir=tmp_path,
        log_file=tmp_path / "logs" / "agent.jsonl", model_settings_file=tmp_path / "private" / "model_settings.json",
    )
    accounts = AccountStore([
        Account(PRIYA, CUSTOMER, hash_password(PASSWORD, n=2**4)),
        Account(MARCUS, CUSTOMER, hash_password(PASSWORD, n=2**4)),
        Account(ADMIN_EMAIL, ADMIN, hash_password(PASSWORD, n=2**4)),
    ])
    embedders = {"made": 0, "error": None}

    def embedder_factory(_settings):
        if embedders["error"]:
            raise embedders["error"]
        embedders["made"] += 1
        return FakeEmbedder()

    knowledge_base = build_knowledge_base(settings, FakeEmbedder())
    app = create_app(
        settings, Resources(FakeProvider([text_response("Hi")]), knowledge_base, orders, tickets),
        today=TODAY, accounts=accounts, embedder_factory=embedder_factory,
    )
    client = TestClient(app)
    token = client.post("/api/sessions", json={"email": ADMIN_EMAIL, "password": PASSWORD}).json()["admin_token"]
    return client, {"Authorization": f"Bearer {token}"}, embedders, docs, app


def test_documents_and_orders_are_for_the_admin_only(setup):
    client, _, _, _, _ = setup

    for path in ["/api/admin/documents", "/api/admin/documents/faq.md", "/api/admin/orders", "/api/admin/orders/JL-10231"]:
        assert client.get(path).status_code == 401, path
    assert client.put("/api/admin/documents/faq.md", json={"text": "x", "version": "y"}).status_code == 401


def test_saving_a_document_reindexes_the_search_and_the_assistant_finds_the_new_text(setup):
    client, admin, embedders, docs, app = setup
    doc = client.get("/api/admin/documents/faq.md", headers=admin).json()
    new_text = doc["text"] + "\n## Gift wrapping\n\nWe wrap every order in plain kraft paper for free.\n"

    response = client.put("/api/admin/documents/faq.md", headers=admin, json={"text": new_text, "version": doc["version"]})

    assert response.status_code == 200, response.text
    assert embedders["made"] == 1
    assert (docs / "faq.md").read_text(encoding="utf-8") == new_text
    saved = response.json()["document"]
    assert saved["version"] != doc["version"] and len(saved["history"]) == 1
    hits = app.state.live.resources.knowledge_base.search("Do you gift wrap orders in kraft paper?")
    assert hits and hits[0].chunk.section == "Gift wrapping"


def test_a_refused_save_explains_why_and_changes_nothing(setup):
    client, admin, embedders, docs, _ = setup
    doc = client.get("/api/admin/documents/faq.md", headers=admin).json()

    response = client.put("/api/admin/documents/faq.md", headers=admin, json={"text": doc["text"] + f"\n{PRIYA}\n", "version": doc["version"]})

    assert response.status_code == 400 and PRIYA in response.json()["detail"]
    assert (docs / "faq.md").read_text(encoding="utf-8") == doc["text"] and embedders["made"] == 0


def test_a_save_the_search_cannot_index_is_undone(setup):
    client, admin, embedders, docs, _ = setup
    embedders["error"] = ServiceError("The embedding service is down.", service="embeddings", kind="x", retryable=False)
    doc = client.get("/api/admin/documents/faq.md", headers=admin).json()

    response = client.put("/api/admin/documents/faq.md", headers=admin, json={"text": doc["text"] + "\nNew.\n", "version": doc["version"]})

    assert response.status_code == 400 and response.json()["detail"].startswith("Nothing was changed")
    assert (docs / "faq.md").read_text(encoding="utf-8") == doc["text"]


def test_an_earlier_version_can_be_viewed_and_restored(setup):
    client, admin, _, docs, _ = setup
    first = client.get("/api/admin/documents/faq.md", headers=admin).json()
    second = client.put("/api/admin/documents/faq.md", headers=admin, json={"text": first["text"] + "\nAdded.\n", "version": first["version"]}).json()["document"]
    (entry,) = second["history"]

    assert client.get(f"/api/admin/documents/faq.md/history/{entry['id']}", headers=admin).json()["text"] == first["text"]
    restored = client.post("/api/admin/documents/faq.md/restore", headers=admin, json={"version_id": entry["id"], "version": second["version"]})

    assert restored.status_code == 200
    assert (docs / "faq.md").read_text(encoding="utf-8") == first["text"]
    assert len(restored.json()["document"]["history"]) == 2  # the restore can be undone too
    assert client.get("/api/admin/documents/faq.md/history/20200101T000000000000Z", headers=admin).status_code == 404


def test_editing_the_product_table_updates_the_shop_page(setup):
    client, admin, _, _, _ = setup
    doc = client.get("/api/admin/documents/company_overview.md", headers=admin).json()
    new_text = doc["text"].replace("| Cast Iron Skillet | Homeware | $55.00 |", "| Cast Iron Skillet | Homeware | $59.00 |", 1)

    response = client.put("/api/admin/documents/company_overview.md", headers=admin, json={"text": new_text, "version": doc["version"]})

    assert response.status_code == 200, response.text
    prices = {p["name"]: p["price"] for p in client.get("/api/products").json()}
    assert prices["Cast Iron Skillet"] == 59.0


def test_orders_can_be_found_and_opened_with_the_email_masked(setup):
    client, admin, _, _, _ = setup

    found = client.get("/api/admin/orders", headers=admin, params={"q": "priya nair"}).json()
    assert {o["order_id"] for o in found["orders"]} == {"JL-10198", "JL-10231"} and found["total"] == 2
    assert client.get("/api/admin/orders", headers=admin, params={"q": "jl-10231"}).json()["total"] == 1
    assert client.get("/api/admin/orders", headers=admin, params={"q": PRIYA}).json()["total"] == 2

    detail = client.get("/api/admin/orders/jl-10231", headers=admin).json()
    assert detail["order"]["order_id"] == "JL-10231" and detail["customer"]["name"] == "Priya Nair"
    assert PRIYA not in str(detail)
    assert client.get("/api/admin/orders/JL-00000", headers=admin).status_code == 404
