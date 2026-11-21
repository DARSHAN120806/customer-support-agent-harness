"""The admin panel's model settings: the form it sends, how a choice is checked
and merged with saved keys, and the connection test.

Admin only. Keys typed into the form are kept on the server; the browser only
ever gets back their last four characters.
"""

from __future__ import annotations

import dataclasses
import time
from typing import Any, Callable, Literal

from pydantic import BaseModel, Field

from ..config import ConfigError, Settings
from ..model_settings import apply
from ..retry import ServiceError

# A tiny made-up tool, to see whether the model can ask for tools at all. A
# model that cannot do that cannot look up orders or search the documents.
TEST_TOOL = {
    "name": "lookup_order",
    "description": "Look up an order by its order ID.",
    "input_schema": {
        "type": "object",
        "properties": {"order_id": {"type": "string", "description": "The order ID, like JL-10231."}},
        "required": ["order_id"],
    },
}


class ChatForm(BaseModel):
    provider: Literal["bedrock", "anthropic", "openai_compatible"]
    model: str = Field(min_length=1, max_length=200)
    base_url: str | None = Field(None, max_length=500)
    # Left empty: keep the key saved before for this provider (or the .env key).
    api_key: str | None = Field(None, max_length=1000)
    aws_region: str | None = Field(None, max_length=40)
    # Used for the cost estimates and the cost limit. 0 for a local model.
    input_price: float = Field(0, ge=0, le=1000)
    output_price: float = Field(0, ge=0, le=1000)


class SearchForm(BaseModel):
    provider: Literal["titan", "openai_compatible"]
    model: str = Field(min_length=1, max_length=200)
    base_url: str | None = Field(None, max_length=500)
    api_key: str | None = Field(None, max_length=1000)


class ModelForm(BaseModel):
    chat: ChatForm
    search: SearchForm


def _clean(value: str | None) -> str | None:
    value = (value or "").strip()
    return value or None


def problems(form: ModelForm) -> list[str]:
    """What is missing or wrong in the form, in plain words."""
    found = []
    for part, label in ((form.chat, "chat model"), (form.search, "search model")):
        if part.provider == "openai_compatible":
            url = _clean(part.base_url)
            if not url:
                found.append(f"The {label} needs a web address, for example http://localhost:11434/v1 for Ollama.")
            elif not url.startswith(("http://", "https://")):
                found.append(f"The {label}'s web address must start with http:// or https://.")
    return found


def to_saved(form: ModelForm, saved: dict[str, Any] | None) -> tuple[dict[str, Any], dict[str, Any]]:
    """The form as it will be saved. An empty key keeps the key saved before
    for the same provider, so the admin never has to type it twice."""
    before_chat = (saved or {}).get("chat", {})
    before_search = (saved or {}).get("search", {})
    chat = {
        "provider": form.chat.provider,
        "model": form.chat.model.strip(),
        "base_url": _clean(form.chat.base_url) if form.chat.provider == "openai_compatible" else None,
        "api_key": None,
        "aws_region": _clean(form.chat.aws_region) if form.chat.provider == "bedrock" else None,
        "input_price": form.chat.input_price,
        "output_price": form.chat.output_price,
    }
    if form.chat.provider != "bedrock":  # Bedrock signs in with the AWS details in .env
        chat["api_key"] = _clean(form.chat.api_key) or (
            before_chat.get("api_key") if before_chat.get("provider") == form.chat.provider else None
        )
    search = {
        "provider": form.search.provider,
        "model": form.search.model.strip(),
        "base_url": _clean(form.search.base_url) if form.search.provider == "openai_compatible" else None,
        "api_key": None,
    }
    if form.search.provider == "openai_compatible":
        search["api_key"] = _clean(form.search.api_key) or (
            before_search.get("api_key") if before_search.get("provider") == form.search.provider else None
        )
    return chat, search


def candidate_settings(base: Settings, chat: dict[str, Any], search: dict[str, Any]) -> Settings:
    """The settings the app would run with if this choice were saved."""
    return apply(base, {"chat": chat, "search": search})


def same_search(a: Settings, b: Settings) -> bool:
    keys = ("embedding_provider", "embedding_model", "embedding_base_url", "embedding_api_key", "aws_region")
    return all(getattr(a, k) == getattr(b, k) for k in keys)


def _ms(started: float) -> int:
    return round((time.perf_counter() - started) * 1000)


def _problem(error: Exception) -> str:
    if isinstance(error, (ServiceError, ConfigError)):
        return str(error)
    return f"Unexpected problem: {type(error).__name__}"


def check_connection(
    settings: Settings,
    provider_factory: Callable[[Settings], Any],
    embedder_factory: Callable[[Settings], Any],
) -> dict[str, Any]:
    """Try the chosen models with tiny requests. Nothing is saved or switched.

    The chat model gets two very short requests (a few hundred tokens in all,
    a fraction of a cent on a paid service, free on a local one): one plain
    reply, and one that should make it ask for a tool. The search model gets
    one short text.
    """
    result: dict[str, Any] = {}
    small = dataclasses.replace(settings, max_output_tokens=200)

    started = time.perf_counter()
    try:
        provider = provider_factory(small)
        reply = provider.create_message(
            system="This is a connection test. Reply with the single word OK.",
            messages=[{"role": "user", "content": "Connection test"}],
            tools=[],
        )
        tool_reply = provider.create_message(
            system="This is a test of tool use. Call the lookup_order tool for the order the user names. "
            "Do not answer in text.",
            messages=[{"role": "user", "content": "Please look up order JL-10231."}],
            tools=[TEST_TOOL],
        )
        result["chat"] = {
            "ok": True,
            "reply": reply.text[:200],
            "tools_ok": any(call.name == "lookup_order" for call in tool_reply.tool_calls),
            "ms": _ms(started),
        }
    except Exception as error:  # every failure becomes a message for the admin
        result["chat"] = {"ok": False, "error": _problem(error), "ms": _ms(started)}

    started = time.perf_counter()
    try:
        vector = embedder_factory(settings).embed("Connection test")
        result["search"] = {"ok": True, "dimensions": len(vector), "ms": _ms(started)}
    except Exception as error:
        result["search"] = {"ok": False, "error": _problem(error), "ms": _ms(started)}
    return result
