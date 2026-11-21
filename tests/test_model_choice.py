"""Tests for choosing the model: the OpenAI-compatible connection (OpenAI,
OpenRouter, Groq, Ollama, LM Studio), the OpenAI-compatible search model, and
the model choice saved from the admin panel. Nothing here calls a real service."""

from __future__ import annotations

import dataclasses
import json
from types import SimpleNamespace

import httpx
import openai
import pytest
from anthropic.types import TextBlock, ToolUseBlock

from support_agent.app import embeddings_cache_path
from support_agent.config import ConfigError, Settings
from support_agent.embeddings import OpenAICompatibleEmbedder
from support_agent.model_settings import apply, key_hint, load_saved, load_settings, public_view, save
from support_agent.providers import create_embedder, create_provider
from support_agent.providers.openai_compatible import (
    OpenAICompatibleProvider,
    to_openai_messages,
    to_openai_tools,
    to_service_error,
)
from support_agent.retry import ServiceError
from support_agent.safety import find_hidden_tech_terms

SECRET = "sk-test-1234567890abcd"


@pytest.fixture
def settings(monkeypatch) -> Settings:
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "bedrock")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    for name in ("SUPPORT_AGENT_MODEL", "SUPPORT_AGENT_BASE_URL", "SUPPORT_AGENT_API_KEY", "SUPPORT_AGENT_EMBEDDING_PROVIDER"):
        monkeypatch.delenv(name, raising=False)
    return Settings.from_env()


# --- Translating the conversation ---------------------------------------------------


def test_our_conversation_becomes_openai_messages():
    messages = [
        {"role": "user", "content": "Where is JL-10231?"},
        {
            "role": "assistant",
            "content": [
                {"type": "text", "text": "Let me check."},
                {"type": "tool_use", "id": "call_1", "name": "lookup_order", "input": {"order_id": "JL-10231"}},
            ],
        },
        {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "call_1", "content": "Delivered."}]},
        {"role": "assistant", "content": "It was delivered."},
    ]

    result = to_openai_messages("Rules", messages)

    assert result[0] == {"role": "system", "content": "Rules"}
    assert result[1] == {"role": "user", "content": "Where is JL-10231?"}
    assert result[2]["role"] == "assistant" and result[2]["content"] == "Let me check."
    assert result[2]["tool_calls"] == [
        {"id": "call_1", "type": "function", "function": {"name": "lookup_order", "arguments": '{"order_id": "JL-10231"}'}}
    ]
    assert result[3] == {"role": "tool", "tool_call_id": "call_1", "content": "Delivered."}
    assert result[4] == {"role": "assistant", "content": "It was delivered."}


def test_blocks_from_the_anthropic_library_are_translated_too():
    # A chat started on one model keeps its own blocks; the translation reads
    # library objects as well as plain dictionaries.
    blocks = [
        TextBlock(type="text", text="One moment."),
        ToolUseBlock(type="tool_use", id="toolu_1", name="search_knowledge_base", input={"query": "returns"}),
    ]

    (_, assistant) = to_openai_messages("s", [{"role": "assistant", "content": blocks}])

    assert assistant["content"] == "One moment."
    assert assistant["tool_calls"][0]["function"]["name"] == "search_knowledge_base"


def test_a_tool_only_answer_has_no_text_and_several_results_become_separate_messages():
    messages = [
        {"role": "assistant", "content": [{"type": "tool_use", "id": "a", "name": "x", "input": {}}, {"type": "tool_use", "id": "b", "name": "y", "input": {}}]},
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "a", "content": [{"type": "text", "text": "A"}]},
            {"type": "tool_result", "tool_use_id": "b", "content": "B", "is_error": True},
        ]},
    ]

    _, assistant, first, second = to_openai_messages("s", messages)

    assert assistant["content"] is None and len(assistant["tool_calls"]) == 2
    assert (first["content"], second["content"]) == ("A", "B")


def test_our_tools_become_openai_functions():
    tool = {"name": "lookup_order", "description": "Look up", "input_schema": {"type": "object", "properties": {}}}

    assert to_openai_tools([tool]) == [
        {"type": "function", "function": {"name": "lookup_order", "description": "Look up", "parameters": tool["input_schema"]}}
    ]


# --- Reading the answer --------------------------------------------------------------


def answer(content=None, tool_calls=None, finish_reason="stop", usage=(120, 30)):
    calls = [
        SimpleNamespace(id=cid, function=SimpleNamespace(name=name, arguments=args)) for cid, name, args in (tool_calls or [])
    ]
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content, tool_calls=calls), finish_reason=finish_reason)],
        usage=SimpleNamespace(prompt_tokens=usage[0], completion_tokens=usage[1]) if usage else None,
    )


class FakeOpenAI:
    def __init__(self, response=None, error=None):
        self.response, self.error, self.request = response, error, None
        self.chat = SimpleNamespace(completions=self)

    def create(self, **request):
        self.request = request
        if self.error:
            raise self.error
        return self.response


def test_a_text_answer_is_read_with_its_tokens():
    client = FakeOpenAI(answer("  Hello.  "))
    provider = OpenAICompatibleProvider(client, "llama3.1", 500)

    result = provider.create_message(system="s", messages=[{"role": "user", "content": "Hi"}], tools=[])

    assert (result.text, result.stop_reason, result.tool_calls) == ("Hello.", "end_turn", [])
    assert (result.input_tokens, result.output_tokens) == (120, 30)
    assert result.content == [{"type": "text", "text": "Hello."}]
    assert client.request["model"] == "llama3.1" and client.request["max_tokens"] == 500
    assert "tools" not in client.request


def test_tool_requests_are_read_and_kept_as_our_own_blocks():
    client = FakeOpenAI(answer(None, [("c1", "lookup_order", '{"order_id": "JL-10231"}')], finish_reason="tool_calls"))
    provider = OpenAICompatibleProvider(client, "m", 100)

    result = provider.create_message(system="s", messages=[], tools=[{"name": "lookup_order", "input_schema": {}}])

    assert result.stop_reason == "tool_use"
    assert [(c.id, c.name, c.input) for c in result.tool_calls] == [("c1", "lookup_order", {"order_id": "JL-10231"})]
    assert result.content == [{"type": "tool_use", "id": "c1", "name": "lookup_order", "input": {"order_id": "JL-10231"}}]
    assert client.request["tools"][0]["function"]["name"] == "lookup_order"


def test_a_local_server_that_says_stop_while_asking_for_a_tool_still_counts_as_a_tool_request():
    client = FakeOpenAI(answer(None, [("c1", "lookup_order", "{}")], finish_reason="stop"))

    result = OpenAICompatibleProvider(client, "m", 100).create_message(system="s", messages=[], tools=[])

    assert result.stop_reason == "tool_use"


@pytest.mark.parametrize("arguments", ["not json", "[1, 2]", None])
def test_unreadable_tool_input_becomes_empty(arguments):
    client = FakeOpenAI(answer(None, [("c1", "lookup_order", arguments)], finish_reason="tool_calls"))

    (call,) = OpenAICompatibleProvider(client, "m", 100).create_message(system="s", messages=[], tools=[]).tool_calls

    assert call.input == {}


def test_a_cut_off_answer_and_missing_token_counts():
    client = FakeOpenAI(answer("Half", finish_reason="length", usage=None))

    result = OpenAICompatibleProvider(client, "m", 100).create_message(system="s", messages=[], tools=[])

    assert result.stop_reason == "max_tokens" and (result.input_tokens, result.output_tokens) == (0, 0)


def test_an_empty_answer_is_an_error_that_is_not_retried():
    client = FakeOpenAI(SimpleNamespace(choices=[], usage=None))

    with pytest.raises(ServiceError) as caught:
        OpenAICompatibleProvider(client, "m", 100).create_message(system="s", messages=[], tools=[])

    assert not caught.value.retryable


REQUEST = httpx.Request("POST", "http://localhost:11434/v1/chat/completions")


def test_a_model_that_is_not_running_is_a_retryable_connection_error():
    client = FakeOpenAI(error=openai.APIConnectionError(request=REQUEST))

    with pytest.raises(ServiceError) as caught:
        OpenAICompatibleProvider(client, "m", 100).create_message(system="s", messages=[], tools=[])

    assert caught.value.kind == "connection" and caught.value.retryable
    assert "is it running" in str(caught.value)


@pytest.mark.parametrize(("status", "kind", "retryable"), [(401, "auth", False), (404, "not_found", False), (429, "rate_limit", True), (503, "server_error", True)])
def test_http_errors_say_whether_to_try_again(status, kind, retryable):
    error = openai.APIStatusError("problem", response=httpx.Response(status, request=REQUEST), body=None)

    result = to_service_error(error)

    assert (result.kind, result.retryable) == (kind, retryable)


def test_timeouts_and_other_errors():
    assert to_service_error(openai.APITimeoutError(request=REQUEST)).retryable
    assert to_service_error(ValueError("odd")).kind == "unexpected"


# --- Building the chosen model -------------------------------------------------------


def test_an_openai_compatible_model_needs_an_address_and_a_name(settings):
    local = dataclasses.replace(settings, provider="openai_compatible", model="llama3.1", api_base_url="http://localhost:11434/v1")

    assert isinstance(create_provider(local), OpenAICompatibleProvider)
    with pytest.raises(ConfigError, match="web address"):
        create_provider(dataclasses.replace(local, api_base_url=None))


def test_bedrock_needs_a_region(settings):
    with pytest.raises(ConfigError, match="region"):
        create_provider(dataclasses.replace(settings, aws_region=None))


def test_the_search_model_can_be_titan_or_openai_compatible(settings):
    local = dataclasses.replace(
        settings, embedding_provider="openai_compatible", embedding_model="nomic-embed-text", embedding_base_url="http://localhost:11434/v1"
    )

    assert create_embedder(local).name == "openai-compatible/nomic-embed-text"
    with pytest.raises(ConfigError, match="web address"):
        create_embedder(dataclasses.replace(local, embedding_base_url=None))
    with pytest.raises(ConfigError, match="AWS_REGION"):
        create_embedder(dataclasses.replace(settings, aws_region=None))


def test_each_search_model_keeps_its_own_saved_index(settings):
    local = dataclasses.replace(settings, embedding_provider="openai_compatible")

    assert embeddings_cache_path(settings, "amazon.titan-embed-text-v2:0/512").name == "knowledge_base_embeddings.json"
    assert embeddings_cache_path(local, "openai-compatible/nomic-embed-text").name == (
        "knowledge_base_embeddings-openai-compatible-nomic-embed-text.json"
    )


class FakeEmbeddingsClient:
    def __init__(self, vector=None, error=None):
        self.vector, self.error = vector, error
        self.embeddings = self

    def create(self, model, input):
        if self.error:
            raise self.error
        return SimpleNamespace(data=[SimpleNamespace(embedding=self.vector)])


def test_local_embeddings_are_scaled_to_length_one():
    embedder = OpenAICompatibleEmbedder(FakeEmbeddingsClient([3.0, 4.0]), "nomic-embed-text")

    assert embedder.embed("hello") == [0.6, 0.8]


@pytest.mark.parametrize("client", [FakeEmbeddingsClient([0.0, 0.0]), FakeEmbeddingsClient(None), FakeEmbeddingsClient(error=openai.APIConnectionError(request=REQUEST))])
def test_bad_or_failed_embeddings_become_service_errors(client):
    with pytest.raises(ServiceError) as caught:
        OpenAICompatibleEmbedder(client, "m").embed("hello")

    assert caught.value.service == "embeddings"


# --- Settings from .env -------------------------------------------------------------


def test_env_can_choose_an_openai_compatible_model(monkeypatch, settings):
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "openai_compatible")
    monkeypatch.setenv("SUPPORT_AGENT_MODEL", "llama3.1")
    with pytest.raises(ConfigError, match="SUPPORT_AGENT_BASE_URL"):
        Settings.from_env()

    monkeypatch.setenv("SUPPORT_AGENT_BASE_URL", "http://localhost:11434/v1")
    monkeypatch.setenv("SUPPORT_AGENT_API_KEY", SECRET)
    chosen = Settings.from_env()

    assert (chosen.provider, chosen.api_base_url) == ("openai_compatible", "http://localhost:11434/v1")
    assert SECRET not in repr(chosen)  # keys never appear when settings are printed


def test_an_unknown_search_model_kind_is_refused(monkeypatch, settings):
    monkeypatch.setenv("SUPPORT_AGENT_EMBEDDING_PROVIDER", "magic")

    with pytest.raises(ConfigError, match="EMBEDDING_PROVIDER"):
        Settings.from_env()


# --- The saved choice ----------------------------------------------------------------

LOCAL_CHAT = {"provider": "openai_compatible", "model": "llama3.1", "base_url": "http://localhost:11434/v1",
              "api_key": SECRET, "aws_region": None, "input_price": 0, "output_price": 0}
TITAN = {"provider": "titan", "model": "amazon.titan-embed-text-v2:0", "base_url": None, "api_key": None}


def test_a_saved_choice_is_read_back_and_applied_on_top_of_env(settings, tmp_path):
    path = tmp_path / "model_settings.json"
    save(path, LOCAL_CHAT, TITAN)

    chosen = apply(settings, load_saved(path))

    assert (chosen.provider, chosen.model, chosen.api_base_url, chosen.api_key) == (
        "openai_compatible", "llama3.1", "http://localhost:11434/v1", SECRET
    )
    assert chosen.input_price_per_million_tokens == 0 and chosen.aws_region == "us-east-1"
    assert chosen.log_file == settings.log_file  # everything else stays as in .env


def test_load_settings_uses_the_saved_choice_when_there_is_one(monkeypatch, tmp_path, settings):
    path = tmp_path / "chosen.json"
    monkeypatch.setenv("SUPPORT_AGENT_MODEL_SETTINGS_FILE", str(path))
    assert load_settings().provider == "bedrock"

    save(path, LOCAL_CHAT, TITAN)
    assert load_settings().provider == "openai_compatible"


def test_a_damaged_saved_choice_says_how_to_recover(tmp_path):
    path = tmp_path / "model_settings.json"
    path.write_text("{ not json", encoding="utf-8")

    with pytest.raises(ConfigError, match="Delete that file"):
        load_saved(path)

    path.write_text(json.dumps({"chat": {"provider": "magic"}, "search": TITAN}), encoding="utf-8")
    with pytest.raises(ConfigError):
        load_saved(path)


def test_the_admin_panel_never_sees_a_whole_key(settings):
    chosen = apply(settings, {"chat": LOCAL_CHAT, "search": TITAN})

    view = public_view(chosen, {"chat": LOCAL_CHAT, "search": TITAN, "saved_at": "2026-11-21T10:00:00+00:00"})

    assert SECRET not in json.dumps(view)
    assert view["chat"]["key_hint"] == "…abcd"
    assert view["source"] == "admin panel"
    assert key_hint(None) is None and key_hint("short") == "set"


def test_the_names_of_newly_supported_models_are_hidden_from_customers():
    assert sorted(find_hidden_tech_terms("I'm Qwen, running on Ollama.")) == ["Ollama", "Qwen"]
    assert find_hidden_tech_terms("Hi Gemma, your order has shipped.") == []  # a customer's name
