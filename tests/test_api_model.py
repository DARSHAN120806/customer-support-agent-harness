"""Tests for the admin panel's model settings in the web API. The models are
fakes, so nothing is paid and no service is called."""

from __future__ import annotations

import dataclasses
import json

import pytest
from conftest import MARCUS, PRIYA, TODAY
from fakes import FakeEmbedder, FakeProvider, text_response, tool_response
from fastapi.testclient import TestClient

from support_agent.app import Resources
from support_agent.config import ConfigError, Settings
from support_agent.providers.base import ToolCall
from support_agent.retry import ServiceError
from support_agent.web.accounts import ADMIN, CUSTOMER, Account, AccountStore, hash_password
from support_agent.web.api import create_app

PASSWORD = "pass-1"
ADMIN_EMAIL = "admin@juniperlane.example"
SECRET = "sk-test-1234567890abcd"

LOCAL = {
    "chat": {"provider": "openai_compatible", "model": "llama3.1", "base_url": "http://localhost:11434/v1",
             "api_key": "", "input_price": 0, "output_price": 0},
    "search": {"provider": "titan", "model": "amazon.titan-embed-text-v2:0"},
}


@pytest.fixture(scope="module")
def accounts() -> AccountStore:
    return AccountStore(
        [
            Account(PRIYA, CUSTOMER, hash_password(PASSWORD, n=2**4)),
            Account(MARCUS, CUSTOMER, hash_password(PASSWORD, n=2**4)),
            Account(ADMIN_EMAIL, ADMIN, hash_password(PASSWORD, n=2**4)),
        ]
    )


@pytest.fixture
def settings(monkeypatch, tmp_path) -> Settings:
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "bedrock")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.delenv("SUPPORT_AGENT_MODEL", raising=False)
    return dataclasses.replace(
        Settings.from_env(),
        max_steps=4,
        cache_dir=tmp_path,
        log_file=tmp_path / "logs" / "agent.jsonl",
        model_settings_file=tmp_path / "private" / "model_settings.json",
    )


class Factories:
    """Stand-ins for building real models: they record what was asked for."""

    def __init__(self) -> None:
        self.built: list[Settings] = []
        self.embedders = 0
        self.provider_error: Exception | None = None
        self.next_provider = FakeProvider([text_response("From the new model.")])

    def provider(self, settings: Settings):
        if self.provider_error:
            raise self.provider_error
        self.built.append(settings)
        return self.next_provider

    def embedder(self, settings: Settings):
        self.embedders += 1
        return FakeEmbedder()


@pytest.fixture
def setup(settings, knowledge_base, orders, tickets, accounts):
    factories = Factories()
    first = FakeProvider([text_response("From the first model.")])
    app = create_app(
        settings,
        Resources(first, knowledge_base, orders, tickets),
        today=TODAY,
        accounts=accounts,
        provider_factory=factories.provider,
        embedder_factory=factories.embedder,
    )
    client = TestClient(app)
    token = client.post("/api/sessions", json={"email": ADMIN_EMAIL, "password": PASSWORD}).json()["admin_token"]
    admin = {"Authorization": f"Bearer {token}"}
    return client, admin, factories, settings


def chat(client, email=PRIYA) -> str:
    session = client.post("/api/sessions", json={"email": email, "password": PASSWORD}).json()["session_id"]
    return session


def say(client, session_id, text="Hi") -> str:
    return client.post(f"/api/sessions/{session_id}/messages", json={"text": text}).json()["reply"]


def test_model_settings_are_for_the_admin_only(setup):
    client, _, _, _ = setup

    for method, path in [("get", "/api/admin/model"), ("put", "/api/admin/model"), ("post", "/api/admin/model/test"), ("delete", "/api/admin/model")]:
        response = getattr(client, method)(path, **({"json": LOCAL} if method in ("put", "post") else {}))
        assert response.status_code == 401, path


def test_the_current_model_is_shown_from_env_at_first(setup):
    client, admin, _, _ = setup

    view = client.get("/api/admin/model", headers=admin).json()

    assert view["source"] == ".env"
    assert view["chat"]["provider"] == "bedrock" and view["chat"]["aws_region"] == "us-east-1"
    assert view["search"]["provider"] == "titan"
    assert view["providers"]["chat"]["openai_compatible"] == "OpenAI-compatible"


def test_saving_switches_new_chats_while_open_chats_keep_their_model(setup):
    client, admin, factories, settings = setup
    open_chat = chat(client)

    response = client.put("/api/admin/model", headers=admin, json=LOCAL)

    assert response.status_code == 200
    assert response.json()["chat"]["model"] == "llama3.1" and response.json()["source"] == "admin panel"
    assert factories.built[-1].api_base_url == "http://localhost:11434/v1"
    assert say(client, chat(client, MARCUS)) == "From the new model."
    assert say(client, open_chat) == "From the first model."
    assert client.get("/api/health").json()["model"] == "llama3.1"

    saved = json.loads(settings.model_settings_file.read_text(encoding="utf-8"))
    assert saved["chat"]["provider"] == "openai_compatible"


def test_a_key_is_saved_but_never_sent_back_and_is_kept_when_left_empty(setup):
    client, admin, factories, settings = setup
    with_key = {**LOCAL, "chat": {**LOCAL["chat"], "api_key": SECRET}}

    response = client.put("/api/admin/model", headers=admin, json=with_key)

    assert SECRET not in response.text
    assert response.json()["chat"]["key_hint"] == "…abcd"
    assert SECRET not in client.get("/api/admin/model", headers=admin).text
    assert json.loads(settings.model_settings_file.read_text(encoding="utf-8"))["chat"]["api_key"] == SECRET

    # Saving again with the key box empty keeps the key.
    client.put("/api/admin/model", headers=admin, json=LOCAL)
    assert factories.built[-1].api_key == SECRET


def test_a_missing_address_is_explained_and_nothing_changes(setup):
    client, admin, factories, settings = setup
    no_address = {**LOCAL, "chat": {**LOCAL["chat"], "base_url": ""}}

    response = client.put("/api/admin/model", headers=admin, json=no_address)

    assert response.status_code == 400 and "web address" in response.json()["detail"]
    assert factories.built == [] and not settings.model_settings_file.exists()
    bad_scheme = {**LOCAL, "chat": {**LOCAL["chat"], "base_url": "ftp://x"}}
    assert "http://" in client.put("/api/admin/model", headers=admin, json=bad_scheme).json()["detail"]


def test_a_model_that_cannot_be_built_changes_nothing(setup):
    client, admin, factories, settings = setup
    factories.provider_error = ConfigError("Amazon Bedrock needs an AWS region.")

    response = client.put("/api/admin/model", headers=admin, json=LOCAL)

    assert response.status_code == 400 and response.json()["detail"].startswith("Nothing was changed")
    assert client.get("/api/admin/model", headers=admin).json()["chat"]["provider"] == "bedrock"
    assert not settings.model_settings_file.exists()


def test_the_documents_are_indexed_again_only_when_the_search_model_changes(setup):
    client, admin, factories, _ = setup

    client.put("/api/admin/model", headers=admin, json=LOCAL)
    assert factories.embedders == 0  # same search model as before

    local_search = {**LOCAL, "search": {"provider": "openai_compatible", "model": "nomic-embed-text", "base_url": "http://localhost:11434/v1"}}
    response = client.put("/api/admin/model", headers=admin, json=local_search)

    assert response.status_code == 200 and factories.embedders == 1
    assert response.json()["search"]["model"] == "nomic-embed-text"


def test_the_connection_test_checks_replies_tools_and_search_without_saving(setup):
    client, admin, factories, settings = setup
    factories.next_provider = FakeProvider(
        [text_response("OK"), tool_response(ToolCall("c1", "lookup_order", {"order_id": "JL-10231"}))]
    )

    result = client.post("/api/admin/model/test", headers=admin, json=LOCAL).json()

    assert result["chat"]["ok"] and result["chat"]["reply"] == "OK" and result["chat"]["tools_ok"]
    assert result["search"]["ok"] and result["search"]["dimensions"] == FakeEmbedder.SIZE
    assert factories.built[-1].max_output_tokens == 200  # tiny requests only
    assert not settings.model_settings_file.exists()
    assert client.get("/api/admin/model", headers=admin).json()["chat"]["provider"] == "bedrock"


def test_the_connection_test_reports_a_model_that_cannot_use_tools(setup):
    client, admin, factories, _ = setup
    factories.next_provider = FakeProvider([text_response("OK"), text_response("Sure, the order is fine.")])

    result = client.post("/api/admin/model/test", headers=admin, json=LOCAL).json()

    assert result["chat"]["ok"] and result["chat"]["tools_ok"] is False


def test_the_connection_test_explains_a_failure(setup):
    client, admin, factories, _ = setup
    factories.provider_error = ServiceError(
        "Could not connect to the model service. If it is a local model, is it running?",
        service="model", kind="connection", retryable=True,
    )

    result = client.post("/api/admin/model/test", headers=admin, json=LOCAL).json()

    assert result["chat"]["ok"] is False and "is it running" in result["chat"]["error"]


def test_reset_goes_back_to_env_and_forgets_the_saved_choice(setup):
    client, admin, _, settings = setup
    client.put("/api/admin/model", headers=admin, json=LOCAL)
    assert settings.model_settings_file.exists()

    view = client.delete("/api/admin/model", headers=admin).json()

    assert view["source"] == ".env" and view["chat"]["provider"] == "bedrock"
    assert not settings.model_settings_file.exists()
