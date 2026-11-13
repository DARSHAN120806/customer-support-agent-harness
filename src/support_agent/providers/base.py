"""The shared shape every model provider must follow.

The agent loop only talks to this interface. It does not know or care whether
the model is reached through Amazon Bedrock, the Anthropic API, or a fake model
used in tests. That is what makes the provider swappable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ToolCall:
    """One request from the model to run a tool."""

    id: str
    name: str
    input: dict[str, Any]


@dataclass(frozen=True)
class ModelResponse:
    """What came back from one call to the model."""

    # The raw content blocks. These are sent back to the model unchanged on the
    # next call, so the model can see what it said and which tools it asked for.
    content: list[Any]
    # All the plain text in the response, joined together.
    text: str
    tool_calls: list[ToolCall]
    # Why the model stopped: "end_turn", "tool_use", "max_tokens", "refusal", ...
    stop_reason: str | None
    input_tokens: int
    output_tokens: int


class ModelProvider(Protocol):
    def create_message(
        self,
        *,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> ModelResponse:
        """Send the conversation to the model and return its response."""
        ...
