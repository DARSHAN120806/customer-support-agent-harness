"""Model choices saved from the admin panel.

The .env file gives the starting settings. When the admin picks a model in the
admin panel, the choice is saved in private/model_settings.json (a folder git
never commits) and from then on it overrides the .env file. The web app, the
terminal chat and the evaluation script all read settings through
`load_settings()`, so they always use the same model.

Keys are saved in that file as typed, because the libraries need them as they
are. They are never sent back to the browser (only the last four characters),
never logged, and never printed: the Settings fields that hold them are hidden
from printing.
"""

from __future__ import annotations

import dataclasses
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import EMBEDDING_PROVIDERS, ConfigError, Settings

CHAT_PROVIDERS = {
    "bedrock": "Amazon Bedrock",
    "anthropic": "Anthropic API",
    "openai_compatible": "OpenAI-compatible",
}
SEARCH_PROVIDERS = {
    "titan": "Amazon Titan",
    "openai_compatible": "OpenAI-compatible",
}
FILE_VERSION = 1


def load_saved(path: Path) -> dict[str, Any] | None:
    """The saved choice, or None if nothing has been saved yet."""
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["chat"]["provider"] not in CHAT_PROVIDERS or data["search"]["provider"] not in SEARCH_PROVIDERS:
            raise ValueError("unknown provider")
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise ConfigError(
            f"The saved model settings in {path} could not be read ({error}). "
            "Delete that file to go back to the settings in .env."
        ) from error
    return data


def save(path: Path, chat: dict[str, Any], search: dict[str, Any]) -> dict[str, Any]:
    data = {
        "version": FILE_VERSION,
        "saved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "chat": chat,
        "search": search,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def apply(settings: Settings, saved: dict[str, Any]) -> Settings:
    """The .env settings with the saved choice on top."""
    chat, search = saved["chat"], saved["search"]
    same_chat = chat["provider"] == settings.provider
    same_search = search["provider"] == settings.embedding_provider
    return dataclasses.replace(
        settings,
        provider=chat["provider"],
        model=chat["model"],
        api_base_url=chat.get("base_url") or None,
        # A key left empty in the admin panel falls back to the .env file's key
        # for the same provider (and, for Anthropic, the library's own variable).
        api_key=chat.get("api_key") or (settings.api_key if same_chat else None),
        aws_region=chat.get("aws_region") or settings.aws_region,
        input_price_per_million_tokens=float(chat.get("input_price", settings.input_price_per_million_tokens)),
        output_price_per_million_tokens=float(chat.get("output_price", settings.output_price_per_million_tokens)),
        embedding_provider=search["provider"],
        embedding_model=search["model"],
        embedding_base_url=search.get("base_url") or None,
        embedding_api_key=search.get("api_key") or (settings.embedding_api_key if same_search else None),
    )


def load_settings() -> Settings:
    """Settings from .env, with any choice saved in the admin panel on top."""
    base = Settings.from_env()
    saved = load_saved(base.model_settings_file)
    return apply(base, saved) if saved else base


def key_hint(key: str | None) -> str | None:
    """Enough of a key to recognise it, never enough to use it."""
    if not key:
        return None
    return f"…{key[-4:]}" if len(key) > 8 else "set"


def public_view(settings: Settings, saved: dict[str, Any] | None) -> dict[str, Any]:
    """What the admin panel may see: everything except the keys themselves."""
    return {
        "chat": {
            "provider": settings.provider,
            "model": settings.model,
            "base_url": settings.api_base_url,
            "aws_region": settings.aws_region,
            "input_price": settings.input_price_per_million_tokens,
            "output_price": settings.output_price_per_million_tokens,
            "key_hint": key_hint(settings.api_key),
        },
        "search": {
            "provider": settings.embedding_provider,
            "model": settings.embedding_model,
            "base_url": settings.embedding_base_url,
            "key_hint": key_hint(settings.embedding_api_key),
        },
        # "admin panel" when a saved choice is in use, ".env" otherwise.
        "source": "admin panel" if saved else ".env",
        "saved_at": saved.get("saved_at") if saved else None,
        "providers": {"chat": CHAT_PROVIDERS, "search": SEARCH_PROVIDERS},
    }


__all__ = [
    "CHAT_PROVIDERS",
    "EMBEDDING_PROVIDERS",
    "SEARCH_PROVIDERS",
    "apply",
    "key_hint",
    "load_saved",
    "load_settings",
    "public_view",
    "save",
]
