"""A fake model for tests. It replays a fixed script of responses, so tests are
fast, free, and give the same result every time."""

from __future__ import annotations

import copy
from typing import Any

from support_agent.providers.base import ModelResponse, ToolCall


def text_response(text: str, input_tokens: int = 10, output_tokens: int = 5) -> ModelResponse:
    return ModelResponse(
        content=[{"type": "text", "text": text}],
        text=text,
        tool_calls=[],
        stop_reason="end_turn",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )


def tool_response(
    *calls: ToolCall, text: str = "", input_tokens: int = 10, output_tokens: int = 5
) -> ModelResponse:
    return ModelResponse(
        content=([{"type": "text", "text": text}] if text else [])
        + [
            {"type": "tool_use", "id": call.id, "name": call.name, "input": call.input}
            for call in calls
        ],
        text=text,
        tool_calls=list(calls),
        stop_reason="tool_use",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )


def stopped_response(stop_reason: str, text: str = "") -> ModelResponse:
    return ModelResponse(
        content=[{"type": "text", "text": text}] if text else [],
        text=text,
        tool_calls=[],
        stop_reason=stop_reason,
        input_tokens=10,
        output_tokens=5,
    )


class FakeProvider:
    """Returns the scripted responses in order. If the script runs out, the last
    response is repeated, which is handy for testing the step limit."""

    def __init__(self, responses: list[ModelResponse]) -> None:
        self._responses = responses
        self.requests: list[dict[str, Any]] = []

    def create_message(self, *, system, messages, tools) -> ModelResponse:
        # Keep a copy of what the agent sent, so tests can inspect it.
        self.requests.append(
            {"system": system, "messages": copy.deepcopy(messages), "tools": tools}
        )
        index = min(len(self.requests) - 1, len(self._responses) - 1)
        return self._responses[index]


class FakeEmbedder:
    """Turns text into numbers without calling any service: each word is given a
    fixed position in the list, so texts that share words get similar numbers."""

    name = "fake-embedder"
    SIZE = 8192  # large, so two different words rarely share a position

    def __init__(self) -> None:
        self.calls = 0

    def embed(self, text: str) -> list[float]:
        import hashlib
        import math
        import re

        self.calls += 1
        vector = [0.0] * self.SIZE
        for word in re.findall(r"[a-z0-9]+", text.lower()):
            position = int(hashlib.md5(word.encode()).hexdigest(), 16) % self.SIZE
            vector[position] += 1.0
        length = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / length for value in vector]
