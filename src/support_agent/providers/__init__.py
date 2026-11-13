"""Model providers: the code that actually talks to the AI model."""

from __future__ import annotations

from ..config import ConfigError, Settings
from .anthropic_sdk import AnthropicSDKProvider
from .base import ModelProvider, ModelResponse, ToolCall

__all__ = ["ModelProvider", "ModelResponse", "ToolCall", "create_provider"]


def create_provider(settings: Settings) -> ModelProvider:
    """Build the provider named in the settings."""
    if settings.provider == "anthropic":
        from anthropic import Anthropic

        # The API key is read from the ANTHROPIC_API_KEY environment variable by
        # the library itself. It never appears in code.
        client = Anthropic()
        return AnthropicSDKProvider(client, settings.model, settings.max_output_tokens)

    if settings.provider == "bedrock":
        # Imported here so the AWS libraries are only loaded when Bedrock is used.
        from anthropic import AnthropicBedrock

        # Credentials are read from the environment by the library itself: either
        # a Bedrock API key (AWS_BEARER_TOKEN_BEDROCK) or AWS access keys
        # (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY). They never appear in code.
        #
        # This is Bedrock's standard endpoint. The library also has a newer
        # AnthropicBedrockMantle client, but that endpoint does not serve models
        # to every account yet, so the standard one is the safer choice.
        client = AnthropicBedrock(aws_region=settings.aws_region)
        return AnthropicSDKProvider(client, settings.model, settings.max_output_tokens)

    raise ConfigError(f"Unknown provider '{settings.provider}'.")
