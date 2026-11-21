"""A provider for any service that speaks the OpenAI "chat completions" format.

That one format is used by OpenAI itself and by many other services: OpenRouter,
Groq, and local model runners such as Ollama and LM Studio. So this single file
lets the shop use any of them.

The rest of the program keeps the conversation in one format (text blocks,
"tool_use" requests and "tool_result" answers). This file translates that
conversation into the OpenAI format before each call, and translates the answer
back, so the agent loop and every safety check work exactly the same whichever
model is behind them.
"""

from __future__ import annotations

import json
from typing import Any

import openai

from ..retry import ServiceError
from .base import ModelResponse, ToolCall

RETRYABLE_STATUS_CODES = {408, 409, 429}
_KIND_BY_STATUS = {
    400: "bad_request",
    401: "auth",
    403: "permission",
    404: "not_found",
    408: "timeout",
    409: "conflict",
    413: "request_too_large",
    422: "bad_request",
    429: "rate_limit",
}
# Why the model stopped, in the words the agent loop expects.
_STOP_REASON = {
    "stop": "end_turn",
    "tool_calls": "tool_use",
    "function_call": "tool_use",
    "length": "max_tokens",
    "content_filter": "refusal",
}


def to_service_error(error: Exception) -> ServiceError:
    """Turn an error from the OpenAI library into a ServiceError that says
    whether it is worth trying again."""
    if isinstance(error, openai.APITimeoutError):
        return ServiceError("The model took too long to answer.", service="model", kind="timeout", retryable=True)
    if isinstance(error, openai.APIConnectionError):
        return ServiceError(
            "Could not connect to the model service. If it is a local model, is it running?",
            service="model",
            kind="connection",
            retryable=True,
        )
    if isinstance(error, openai.APIStatusError):
        status = error.status_code
        retryable = status in RETRYABLE_STATUS_CODES or status >= 500
        kind = _KIND_BY_STATUS.get(status, "server_error" if status >= 500 else "request_error")
        return ServiceError(
            f"The model service returned an error (HTTP {status}): {str(error)[:300]}",
            service="model",
            kind=kind,
            retryable=retryable,
        )
    return ServiceError(
        f"Unexpected problem calling the model: {type(error).__name__}",
        service="model",
        kind="unexpected",
        retryable=False,
    )


def _field(block: Any, name: str, default: Any = None) -> Any:
    """Read a field from a block that may be a dictionary or a library object."""
    if isinstance(block, dict):
        return block.get(name, default)
    return getattr(block, name, default)


def _blocks(content: Any) -> list[Any]:
    """A message's content as a list of blocks (plain text becomes one block)."""
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return list(content or [])


def to_openai_messages(system: str, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Translate our conversation into OpenAI chat messages."""
    result: list[dict[str, Any]] = [{"role": "system", "content": system}]
    for message in messages:
        blocks = _blocks(message.get("content"))
        if message.get("role") == "assistant":
            text = "".join(str(_field(b, "text", "")) for b in blocks if _field(b, "type") == "text")
            calls = [
                {
                    "id": _field(b, "id"),
                    "type": "function",
                    "function": {"name": _field(b, "name"), "arguments": json.dumps(_field(b, "input") or {})},
                }
                for b in blocks
                if _field(b, "type") == "tool_use"
            ]
            out: dict[str, Any] = {"role": "assistant", "content": text or None}
            if calls:
                out["tool_calls"] = calls
            result.append(out)
            continue

        # A customer message, or the results of the tools the model asked for.
        # Each tool result becomes its own "tool" message, as the format requires.
        texts = []
        for b in blocks:
            if _field(b, "type") == "tool_result":
                content = _field(b, "content", "")
                if not isinstance(content, str):
                    content = "".join(str(_field(part, "text", "")) for part in _blocks(content))
                result.append({"role": "tool", "tool_call_id": _field(b, "tool_use_id"), "content": content})
            elif _field(b, "type") == "text":
                texts.append(str(_field(b, "text", "")))
        if texts:
            result.append({"role": "user", "content": "\n".join(texts)})
    return result


def to_openai_tools(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Translate our tool list into OpenAI "function" tools."""
    return [
        {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool.get("description", ""),
                "parameters": tool.get("input_schema", {"type": "object", "properties": {}}),
            },
        }
        for tool in tools
    ]


def _arguments(raw: Any) -> dict[str, Any]:
    """The tool's input. Anything that is not a JSON object is treated as empty,
    and the tool then reports what is missing, as with the other providers."""
    if isinstance(raw, dict):
        return raw
    try:
        value = json.loads(raw or "{}")
    except (TypeError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


class OpenAICompatibleProvider:
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
            "messages": to_openai_messages(system, messages),
        }
        if tools:
            request["tools"] = to_openai_tools(tools)

        try:
            response = self._client.chat.completions.create(**request)
        except openai.APIError as error:
            raise to_service_error(error) from error

        if not response.choices:
            raise ServiceError("The model service sent an empty answer.", service="model", kind="bad_response", retryable=False)
        choice = response.choices[0]
        message = choice.message
        text = (message.content or "").strip()
        tool_calls = [
            ToolCall(id=call.id, name=call.function.name, input=_arguments(call.function.arguments))
            for call in (message.tool_calls or [])
            if getattr(call, "function", None) is not None
        ]

        # Kept in our own block format, so the next call (and the forced search,
        # which adds blocks of its own) can be translated the same way.
        content: list[dict[str, Any]] = []
        if text:
            content.append({"type": "text", "text": text})
        content += [{"type": "tool_use", "id": c.id, "name": c.name, "input": c.input} for c in tool_calls]

        stop_reason = _STOP_REASON.get(choice.finish_reason or "", choice.finish_reason)
        # Some local servers report "stop" even when they asked for a tool.
        if tool_calls:
            stop_reason = "tool_use"

        usage = response.usage
        return ModelResponse(
            content=content,
            text=text,
            tool_calls=tool_calls,
            stop_reason=stop_reason,
            input_tokens=(getattr(usage, "prompt_tokens", 0) or 0) if usage else 0,
            output_tokens=(getattr(usage, "completion_tokens", 0) or 0) if usage else 0,
        )
