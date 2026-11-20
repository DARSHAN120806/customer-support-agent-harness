"""Settings for the agent, read from environment variables.

Nothing secret is ever written in the code. Secrets (such as AWS keys) are read
from the environment by the AWS/Anthropic libraries themselves; this module only
reads the non-secret settings that control how the agent behaves.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# The same model family has a different name on each provider.
#
# On Bedrock the name starts with a routing prefix: "global." works from any
# region, while prefixes such as "us.", "eu." or "au." keep requests inside one
# geography. The Bedrock default is Claude Haiku 4.5 because new AWS accounts are
# often not yet allowed to use the Claude 5 models. Once your account is, set
# SUPPORT_AGENT_MODEL=global.anthropic.claude-haiku-5-5 in your .env file.
DEFAULT_MODELS = {
    "bedrock": "global.anthropic.claude-haiku-4-5-20251001-v1:0",
    "anthropic": "claude-haiku-5-5",
}
DEFAULT_PROVIDER = "bedrock"

DEFAULT_EMBEDDING_MODEL = "amazon.titan-embed-text-v2:0"
DEFAULT_MAX_STEPS = 8
DEFAULT_MAX_OUTPUT_TOKENS = 16000
# A normal question uses 4,000-10,000 tokens, so this leaves plenty of room.
DEFAULT_MAX_TOKENS_PER_MESSAGE = 50_000
DEFAULT_MAX_COST_PER_CONVERSATION_USD = 0.50
# Used only to estimate cost for the limit above. These are the list prices of
# Claude Haiku 4.5 in US dollars per million tokens; check your provider's
# pricing page and change them if you use a different model.
DEFAULT_INPUT_PRICE_PER_MILLION_TOKENS = 1.00
DEFAULT_OUTPUT_PRICE_PER_MILLION_TOKENS = 5.00
# How many times a failed call to the model or the search is tried in total.
DEFAULT_MAX_ATTEMPTS = 3
# How long to wait for one answer from the model before giving up on it.
DEFAULT_REQUEST_TIMEOUT_SECONDS = 60.0


class ConfigError(Exception):
    """Raised when a setting is missing or has a value we cannot use."""


@dataclass(frozen=True)
class Settings:
    provider: str
    model: str
    aws_region: str | None
    max_steps: int
    max_output_tokens: int
    max_tokens_per_message: int
    max_cost_per_conversation_usd: float
    input_price_per_million_tokens: float
    output_price_per_million_tokens: float
    max_attempts: int
    request_timeout_seconds: float
    embedding_model: str
    knowledge_base_dir: Path
    orders_file: Path
    tickets_file: Path
    log_file: Path
    cache_dir: Path

    @classmethod
    def from_env(cls) -> "Settings":
        provider = (_get("SUPPORT_AGENT_PROVIDER") or DEFAULT_PROVIDER).lower()
        if provider not in DEFAULT_MODELS:
            supported = ", ".join(sorted(DEFAULT_MODELS))
            raise ConfigError(
                f"SUPPORT_AGENT_PROVIDER is '{provider}', but the supported values are: {supported}."
            )

        aws_region = _get("AWS_REGION") or _get("AWS_DEFAULT_REGION") or None
        if provider == "bedrock" and not aws_region:
            raise ConfigError(
                "AWS_REGION is not set. Add it to your .env file, for example AWS_REGION=us-east-1."
            )
        if provider == "anthropic" and not (
            _get("ANTHROPIC_API_KEY") or _get("ANTHROPIC_AUTH_TOKEN")
        ):
            raise ConfigError(
                "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and paste your key there."
            )

        return cls(
            provider=provider,
            model=_get("SUPPORT_AGENT_MODEL") or DEFAULT_MODELS[provider],
            aws_region=aws_region,
            max_steps=_get_positive_int("SUPPORT_AGENT_MAX_STEPS", DEFAULT_MAX_STEPS),
            max_output_tokens=_get_positive_int(
                "SUPPORT_AGENT_MAX_OUTPUT_TOKENS", DEFAULT_MAX_OUTPUT_TOKENS
            ),
            max_tokens_per_message=_get_positive_int(
                "SUPPORT_AGENT_MAX_TOKENS_PER_MESSAGE", DEFAULT_MAX_TOKENS_PER_MESSAGE
            ),
            max_cost_per_conversation_usd=_get_positive_float(
                "SUPPORT_AGENT_MAX_COST_USD", DEFAULT_MAX_COST_PER_CONVERSATION_USD
            ),
            input_price_per_million_tokens=_get_positive_float(
                "SUPPORT_AGENT_INPUT_PRICE_PER_MTOK", DEFAULT_INPUT_PRICE_PER_MILLION_TOKENS
            ),
            output_price_per_million_tokens=_get_positive_float(
                "SUPPORT_AGENT_OUTPUT_PRICE_PER_MTOK", DEFAULT_OUTPUT_PRICE_PER_MILLION_TOKENS
            ),
            max_attempts=_get_positive_int("SUPPORT_AGENT_MAX_ATTEMPTS", DEFAULT_MAX_ATTEMPTS),
            request_timeout_seconds=_get_positive_float(
                "SUPPORT_AGENT_REQUEST_TIMEOUT_SECONDS", DEFAULT_REQUEST_TIMEOUT_SECONDS
            ),
            embedding_model=_get("SUPPORT_AGENT_EMBEDDING_MODEL") or DEFAULT_EMBEDDING_MODEL,
            knowledge_base_dir=PROJECT_ROOT / "data" / "knowledge_base",
            orders_file=PROJECT_ROOT / "data" / "orders.json",
            tickets_file=Path(
                _get("SUPPORT_AGENT_TICKETS_FILE") or PROJECT_ROOT / "tickets" / "tickets.jsonl"
            ),
            log_file=Path(_get("SUPPORT_AGENT_LOG_FILE") or PROJECT_ROOT / "logs" / "agent.jsonl"),
            cache_dir=PROJECT_ROOT / ".cache",
        )


def _get(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def _get_positive_int(name: str, default: int) -> int:
    raw = _get(name)
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        raise ConfigError(f"{name} must be a whole number, but it is '{raw}'.") from None
    if value < 1:
        raise ConfigError(f"{name} must be 1 or more, but it is {value}.")
    return value


def _get_positive_float(name: str, default: float) -> float:
    raw = _get(name)
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError:
        raise ConfigError(f"{name} must be a number, but it is '{raw}'.") from None
    if value <= 0:
        raise ConfigError(f"{name} must be more than 0, but it is {value}.")
    return value
