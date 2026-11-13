"""A provider built on the official Anthropic Python library.

The Anthropic library offers several clients (Anthropic API, Amazon Bedrock, ...)
that all expose the same `messages.create` call. This class wraps any of them and
converts the response into our own `ModelResponse` shape.
"""

from __future__ import annotations

from typing import Any

from .base import ModelResponse, ToolCall


class AnthropicSDKProvider:
    def __init__(self, client: Any, model: str, max_output_tokens: int) -> None:
        self._client = client
        self._model = model
        self._max_output_tokens = max_output_tokens

    def create_message(
        self,
        *,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> ModelResponse:
        request: dict[str, Any] = {
            "model": self._model,
            "max_tokens": self._max_output_tokens,
            "system": system,
            "messages": messages,
        }
        if tools:
            request["tools"] = tools

        response = self._client.messages.create(**request)

        # A response is a list of blocks of different types (text, tool_use,
        # thinking, ...), so we pick out each kind by its type.
        text = "".join(block.text for block in response.content if block.type == "text")
        tool_calls = [
            ToolCall(id=block.id, name=block.name, input=dict(block.input))
            for block in response.content
            if block.type == "tool_use"
        ]

        usage = response.usage
        input_tokens = (
            (usage.input_tokens or 0)
            + (getattr(usage, "cache_creation_input_tokens", 0) or 0)
            + (getattr(usage, "cache_read_input_tokens", 0) or 0)
        )

        return ModelResponse(
            content=list(response.content),
            text=text.strip(),
            tool_calls=tool_calls,
            stop_reason=response.stop_reason,
            input_tokens=input_tokens,
            output_tokens=usage.output_tokens or 0,
        )
