"""Model providers: the code that actually talks to the AI model."""

from __future__ import annotations

from ..config import ConfigError, Settings
from .anthropic_sdk import AnthropicSDKProvider
from .base import ModelProvider, ModelResponse, ToolCall

__all__ = ["ModelProvider", "ModelResponse", "ToolCall", "create_provider", "create_embedder"]


def create_provider(settings: Settings) -> ModelProvider:
    """Build the provider named in the settings."""
    # The library's own automatic retries are switched off (max_retries=0)
    # because the agent loop does the retrying itself, where every retry can be
    # written to the event log. The timeout stops a stuck request from keeping
    # a customer waiting forever.
    options = {"max_retries": 0, "timeout": settings.request_timeout_seconds}

    if settings.provider == "anthropic":
        from anthropic import Anthropic

        # The key comes from the admin panel's saved settings if one was given
        # there; otherwise the library reads ANTHROPIC_API_KEY from the
        # environment itself. It never appears in code.
        if settings.api_key:
            options["api_key"] = settings.api_key
        client = Anthropic(**options)
        return AnthropicSDKProvider(client, settings.model, settings.max_output_tokens)

    if settings.provider == "bedrock":
        if not settings.aws_region:
            raise ConfigError("Amazon Bedrock needs an AWS region, for example ap-southeast-2.")
        # Imported here so the AWS libraries are only loaded when Bedrock is used.
        from anthropic import AnthropicBedrock

        # Credentials are read from the environment by the library itself: either
        # a Bedrock API key (AWS_BEARER_TOKEN_BEDROCK) or AWS access keys
        # (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY). They never appear in code.
        #
        # This is Bedrock's standard endpoint. The library also has a newer
        # AnthropicBedrockMantle client, but that endpoint does not serve models
        # to every account yet, so the standard one is the safer choice.
        client = AnthropicBedrock(aws_region=settings.aws_region, **options)
        return AnthropicSDKProvider(client, settings.model, settings.max_output_tokens)

    if settings.provider == "openai_compatible":
        from openai import OpenAI

        from .openai_compatible import OpenAICompatibleProvider

        if not settings.api_base_url or not settings.model:
            raise ConfigError("An OpenAI-compatible model needs a web address and a model name.")
        # Local servers (Ollama, LM Studio) need no key, but the library insists
        # on one, so a placeholder is sent; they ignore it.
        client = OpenAI(base_url=settings.api_base_url, api_key=settings.api_key or "not-needed", **options)
        return OpenAICompatibleProvider(client, settings.model, settings.max_output_tokens)

    raise ConfigError(f"Unknown provider '{settings.provider}'.")


def create_embedder(settings: Settings):
    """Build the search (embedding) model named in the settings."""
    if settings.embedding_provider == "openai_compatible":
        from openai import OpenAI

        from ..embeddings import OpenAICompatibleEmbedder

        if not settings.embedding_base_url or not settings.embedding_model:
            raise ConfigError("An OpenAI-compatible search model needs a web address and a model name.")
        client = OpenAI(
            base_url=settings.embedding_base_url,
            api_key=settings.embedding_api_key or "not-needed",
            max_retries=0,
            timeout=settings.request_timeout_seconds,
        )
        return OpenAICompatibleEmbedder(client, settings.embedding_model)

    from ..embeddings import TitanEmbedder

    if not settings.aws_region:
        raise ConfigError(
            "AWS_REGION is not set. The Amazon Titan search model is reached through Bedrock, "
            "so it needs AWS_REGION and AWS sign-in details."
        )
    return TitanEmbedder(settings.aws_region, settings.embedding_model, settings.request_timeout_seconds)
