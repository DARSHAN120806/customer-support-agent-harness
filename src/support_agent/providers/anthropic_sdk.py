"""A provider built on the official Anthropic Python library.

The Anthropic library offers several clients (Anthropic API, Amazon Bedrock, ...)
that all expose the same `messages.create` call. This class wraps any of them and
converts the response into our own `ModelResponse` shape, and any failure into
our own `ServiceError`, so the rest of the program never depends on the library.
"""

from __future__ import annotations

from typing import Any

import anthropic

from ..retry import ServiceError
from .base import ModelResponse, ToolCall

# HTTP status codes that mean "try again in a moment".
RETRYABLE_STATUS_CODES = {408, 409, 429}
_KIND_BY_STATUS = {
    400: "bad_request",
    401: "auth",
    403: "permission",
    404: "not_found",
    408: "timeout",
    409: "conflict",
    413: "request_too_large",
    429: "rate_limit",
}


def to_service_error(error: Exception) -> ServiceError:
    """Turn an error from the Anthropic library into a ServiceError that says
    whether it is worth trying again."""
    if isinstance(error, anthropic.APITimeoutError):
        return ServiceError(
            "The model took too long to answer.", service="model", kind="timeout", retryable=True
        )
    if isinstance(error, anthropic.APIConnectionError):
        return ServiceError(
            "Could not connect to the model service.",
            service="model",
            kind="connection",
            retryable=True,
        )
    if isinstance(error, anthropic.APIStatusError):
        status = error.status_code
        retryable = status in RETRYABLE_STATUS_CODES or status >= 500
        kind = _KIND_BY_STATUS.get(status, "server_error" if status >= 500 else "request_error")
        return ServiceError(
            f"The model service returned an error (HTTP {status}): {str(error)[:300]}",
            service="model",
            kind=kind,
            retryable=retryable,
            retry_after=_retry_after_seconds(error),
        )
    return ServiceError(
        f"Unexpected problem calling the model: {type(error).__name__}",
        service="model",
        kind="unexpected",
        retryable=False,
    )


def _retry_after_seconds(error: anthropic.APIStatusError) -> float | None:
    try:
        return float(error.response.headers.get("retry-after"))
    except (AttributeError, TypeError, ValueError):
        return None


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

        try:
            response = self._client.messages.create(**request)
        except anthropic.APIError as error:
            raise to_service_error(error) from error

        # A response is a list of blocks of different types (text, tool_use,
        # thinking, ...), so we pick out each kind by its type.
        text = "".join(block.text for block in response.content if block.type == "text")
        tool_calls = [
            ToolCall(
                id=block.id,
                name=block.name,
                # The input should be a dictionary; anything else is treated as
                # empty, and the tool then reports what is missing.
                input=dict(block.input) if isinstance(block.input, dict) else {},
            )
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
