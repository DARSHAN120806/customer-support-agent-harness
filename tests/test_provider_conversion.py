"""Tests for turning the model's real response objects into our own shape, and
for building the real clients. Nothing here calls a paid service."""

from __future__ import annotations

import anthropic
import pytest
from anthropic.types import Message

from support_agent.embeddings import TITAN_DIMENSIONS, TitanEmbedder
from support_agent.providers.anthropic_sdk import AnthropicSDKProvider, to_service_error


def message(content: list[dict], stop_reason: str = "end_turn", **usage) -> Message:
    """A response object exactly as the Anthropic library returns it."""
    return Message.model_validate(
        {
            "id": "msg_test",
            "type": "message",
            "role": "assistant",
            "model": "test-model",
            "content": content,
            "stop_reason": stop_reason,
            "stop_sequence": None,
            "usage": {"input_tokens": 100, "output_tokens": 20, **usage},
        }
    )


class FakeClient:
    """Records the request and returns a prepared response."""

    def __init__(self, response: Message) -> None:
        self.response = response
        self.request: dict = {}
        self.messages = self

    def create(self, **request):
        self.request = request
        return self.response


def test_text_tool_calls_and_tokens_are_read_from_a_real_response():
    response = message(
        [
            {"type": "text", "text": "Let me check. "},
            {"type": "tool_use", "id": "toolu_1", "name": "lookup_order", "input": {"order_id": "JL-10231"}},
            {"type": "text", "text": " One moment."},
        ],
        stop_reason="tool_use",
        cache_creation_input_tokens=30,
        cache_read_input_tokens=50,
    )
    client = FakeClient(response)
    provider = AnthropicSDKProvider(client, "test-model", max_output_tokens=1000)

    result = provider.create_message(
        system="rules", messages=[{"role": "user", "content": "Hi"}], tools=[{"name": "lookup_order"}]
    )

    assert result.text == "Let me check.  One moment."
    assert [(c.id, c.name, c.input) for c in result.tool_calls] == [
        ("toolu_1", "lookup_order", {"order_id": "JL-10231"})
    ]
    assert result.stop_reason == "tool_use"
    # Cached input still counts as input for the budget and the cost estimate.
    assert (result.input_tokens, result.output_tokens) == (180, 20)
    # The original blocks are kept, so they can be sent back on the next call.
    assert result.content == list(response.content)
    assert client.request == {
        "model": "test-model",
        "max_tokens": 1000,
        "system": "rules",
        "messages": [{"role": "user", "content": "Hi"}],
        "tools": [{"name": "lookup_order"}],
    }


def test_no_tools_means_no_tools_field_in_the_request():
    client = FakeClient(message([{"type": "text", "text": "Hello"}]))
    AnthropicSDKProvider(client, "m", 100).create_message(system="s", messages=[], tools=[])

    assert "tools" not in client.request


def test_blocks_other_than_text_and_tool_use_are_ignored_for_the_reply():
    response = message(
        [
            {"type": "thinking", "thinking": "", "signature": "sig"},
            {"type": "text", "text": "Answer."},
        ]
    )
    result = AnthropicSDKProvider(FakeClient(response), "m", 100).create_message(system="s", messages=[], tools=[])

    assert result.text == "Answer." and result.tool_calls == []
    assert len(result.content) == 2  # the thinking block is kept for the next call


def test_an_unexpected_error_type_is_not_retried():
    error = to_service_error(ValueError("strange"))

    assert (error.kind, error.retryable) == ("unexpected", False)


def test_a_connection_error_from_the_client_becomes_a_service_error():
    class Broken:
        def __init__(self):
            self.messages = self

        def create(self, **request):
            raise anthropic.APIConnectionError(request=None)

    with pytest.raises(Exception) as caught:
        AnthropicSDKProvider(Broken(), "m", 100).create_message(system="s", messages=[], tools=[])

    assert caught.value.retryable and caught.value.kind == "connection"


def test_the_titan_client_is_built_without_its_own_retries():
    embedder = TitanEmbedder("us-east-1", timeout_seconds=42)
    config = embedder._client.meta.config

    assert embedder.name == f"amazon.titan-embed-text-v2:0/{TITAN_DIMENSIONS}"
    assert embedder._client.meta.region_name == "us-east-1"
    assert config.retries["total_max_attempts"] == 1
    assert config.read_timeout == 42
