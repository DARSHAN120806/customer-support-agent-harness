"""Tests for reading settings from environment variables."""

from __future__ import annotations

import pytest

from support_agent.config import ConfigError, Settings
from support_agent.providers import create_provider
from support_agent.providers.anthropic_sdk import AnthropicSDKProvider

ALL_VARIABLES = [
    "SUPPORT_AGENT_PROVIDER",
    "SUPPORT_AGENT_MODEL",
    "SUPPORT_AGENT_MAX_STEPS",
    "SUPPORT_AGENT_MAX_OUTPUT_TOKENS",
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "AWS_REGION",
    "AWS_DEFAULT_REGION",
]


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch):
    """Start every test with none of our settings present."""
    for name in ALL_VARIABLES:
        monkeypatch.delenv(name, raising=False)


def test_bedrock_is_the_default_provider(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    settings = Settings.from_env()

    assert settings.provider == "bedrock"
    assert settings.model == "global.anthropic.claude-haiku-4-5-20251001-v1:0"
    assert settings.aws_region == "us-east-1"
    assert settings.max_steps == 8


def test_anthropic_can_be_selected(monkeypatch):
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "anthropic")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    settings = Settings.from_env()

    assert settings.provider == "anthropic"
    assert settings.model == "claude-haiku-5-5"


def test_model_can_be_overridden(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setenv("SUPPORT_AGENT_MODEL", "anthropic.claude-sonnet-5-5")

    assert Settings.from_env().model == "anthropic.claude-sonnet-5-5"


def test_missing_anthropic_key_is_explained(monkeypatch):
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "anthropic")
    with pytest.raises(ConfigError, match="ANTHROPIC_API_KEY"):
        Settings.from_env()


def test_bedrock_without_a_region_is_explained():
    with pytest.raises(ConfigError, match="AWS_REGION"):
        Settings.from_env()


def test_unknown_provider_is_rejected(monkeypatch):
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "something-else")
    with pytest.raises(ConfigError, match="supported values"):
        Settings.from_env()


@pytest.mark.parametrize("value", ["0", "-2", "many"])
def test_bad_step_limit_is_rejected(monkeypatch, value):
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setenv("SUPPORT_AGENT_MAX_STEPS", value)
    with pytest.raises(ConfigError, match="SUPPORT_AGENT_MAX_STEPS"):
        Settings.from_env()


def test_both_providers_can_be_built_without_contacting_anyone(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    assert isinstance(create_provider(Settings.from_env()), AnthropicSDKProvider)

    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "anthropic")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    assert isinstance(create_provider(Settings.from_env()), AnthropicSDKProvider)
