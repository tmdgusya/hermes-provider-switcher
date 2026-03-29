"""Provider definitions for Claude Code backend switching.

Each provider maps to a set of environment variables that Claude Code
reads to route requests to the alternative backend.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ProviderConfig:
    """Configuration for a single LLM provider."""

    name: str
    slug: str                       # short key: "glm", "kimi", "minimax", "claude"
    base_url_env: str               # env var holding the base URL
    auth_token_env: str             # env var holding the API key
    base_url_default: str = ""      # fallback if env var not set
    haiku_model_env: str = ""       # env var for haiku model override
    sonnet_model_env: str = ""      # env var for sonnet model override
    opus_model_env: str = ""        # env var for opus model override
    default_model_env: str = ""     # env var for the default model
    haiku_model_default: str = ""
    sonnet_model_default: str = ""
    opus_model_default: str = ""
    default_model_default: str = ""
    extra_env: Dict[str, str] = field(default_factory=dict)
    emoji: str = ""
    description: str = ""


# ── Built-in provider presets ─────────────────────────────────────────────

BUILTIN_PROVIDERS: Dict[str, ProviderConfig] = {
    "glm": ProviderConfig(
        name="GLM (Z.ai)",
        slug="glm",
        base_url_env="GT_GLM_BASE_URL",
        auth_token_env="GT_GLM_AUTH_TOKEN",
        base_url_default="https://api.z.ai/api/anthropic",
        haiku_model_env="GT_GLM_HAIKU_MODEL",
        sonnet_model_env="GT_GLM_SONNET_MODEL",
        opus_model_env="GT_GLM_OPUS_MODEL",
        haiku_model_default="glm-4.7-flash",
        sonnet_model_default="glm-5-turbo",
        opus_model_default="glm-5.1",
        default_model_default="glm-5.1",
        emoji="🔹",
        description="GLM models via Z.ai Anthropic-compatible proxy",
    ),
    "kimi": ProviderConfig(
        name="Kimi (Moonshot)",
        slug="kimi",
        base_url_env="GT_KIMI_BASE_URL",
        auth_token_env="GT_KIMI_AUTH_TOKEN",
        base_url_default="https://api.kimi.com/coding/",
        default_model_env="GT_KIMI_MODEL",
        default_model_default="kimi-k2.5",
        emoji="🟣",
        description="Kimi models via Moonshot Anthropic-compatible proxy",
    ),
    "minimax": ProviderConfig(
        name="MiniMax",
        slug="minimax",
        base_url_env="GT_MINIMAX_BASE_URL",
        auth_token_env="GT_MINIMAX_AUTH_TOKEN",
        base_url_default="https://api.minimax.io/anthropic",
        haiku_model_env="GT_MINIMAX_SMALL_MODEL",
        sonnet_model_env="GT_MINIMAX_MODEL",
        opus_model_env="GT_MINIMAX_MODEL",
        default_model_env="GT_MINIMAX_MODEL",
        haiku_model_default="MiniMax-M2.5",
        sonnet_model_default="MiniMax-M2.7",
        opus_model_default="MiniMax-M2.7",
        default_model_default="MiniMax-M2.7",
        extra_env={"CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"},
        emoji="🟢",
        description="MiniMax models via Anthropic-compatible proxy",
    ),
    "claude": ProviderConfig(
        name="Claude (Anthropic)",
        slug="claude",
        base_url_env="",
        auth_token_env="",
        emoji="🔸",
        description="Native Anthropic Claude (uses default ~/.claude/ OAuth)",
    ),
}


def build_env_for_provider(
    provider_slug: str,
    model_override: Optional[str] = None,
    custom_providers: Optional[Dict] = None,
) -> Dict[str, str]:
    """Build a subprocess environment dict for the given provider.

    Starts from os.environ, then layers on provider-specific variables.
    For "claude" provider, strips all ANTHROPIC_ overrides so native auth is used.
    """
    providers = {**BUILTIN_PROVIDERS}
    if custom_providers:
        providers.update(custom_providers)

    provider = providers.get(provider_slug)
    if provider is None:
        raise ValueError(
            f"Unknown provider: {provider_slug!r}. "
            f"Available: {', '.join(sorted(providers.keys()))}"
        )

    env = dict(os.environ)

    if provider_slug == "claude":
        # Strip all custom provider vars so native auth kicks in
        for key in [
            "ANTHROPIC_AUTH_TOKEN",
            "ANTHROPIC_BASE_URL",
            "ANTHROPIC_VERSION",
            "ANTHROPIC_MODEL",
            "API_TIMEOUT_MS",
            "ANTHROPIC_DEFAULT_HAIKU_MODEL",
            "ANTHROPIC_DEFAULT_SONNET_MODEL",
            "ANTHROPIC_DEFAULT_OPUS_MODEL",
            "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC",
        ]:
            env.pop(key, None)
        return env

    # Base URL
    base_url = os.environ.get(provider.base_url_env, provider.base_url_default)
    if base_url:
        env["ANTHROPIC_BASE_URL"] = base_url

    # Auth token
    auth_token = os.environ.get(provider.auth_token_env, "")
    if auth_token:
        env["ANTHROPIC_AUTH_TOKEN"] = auth_token
    else:
        raise ValueError(
            f"Provider {provider.name} requires env var "
            f"{provider.auth_token_env!r} to be set"
        )

    # Model mapping
    if model_override:
        env["ANTHROPIC_MODEL"] = model_override
        env["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = model_override
        env["ANTHROPIC_DEFAULT_SONNET_MODEL"] = model_override
        env["ANTHROPIC_DEFAULT_OPUS_MODEL"] = model_override
    else:
        haiku = os.environ.get(provider.haiku_model_env, provider.haiku_model_default)
        sonnet = os.environ.get(provider.sonnet_model_env, provider.sonnet_model_default)
        opus = os.environ.get(provider.opus_model_env, provider.opus_model_default)
        default = os.environ.get(provider.default_model_env, provider.default_model_default)

        if haiku:
            env["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = haiku
        if sonnet:
            env["ANTHROPIC_DEFAULT_SONNET_MODEL"] = sonnet
        if opus:
            env["ANTHROPIC_DEFAULT_OPUS_MODEL"] = opus
        if default:
            env["ANTHROPIC_MODEL"] = default
        elif opus:
            env["ANTHROPIC_MODEL"] = opus

    # Timeout
    env["API_TIMEOUT_MS"] = os.environ.get("GT_API_TIMEOUT_MS", "3000000")

    # Extra env
    for k, v in provider.extra_env.items():
        env[k] = v

    # Clean up version override for most proxies
    env.pop("ANTHROPIC_VERSION", None)

    return env


def list_available_providers(custom_providers: Optional[Dict] = None) -> List[Dict]:
    """Return info about all configured providers."""
    providers = {**BUILTIN_PROVIDERS}
    if custom_providers:
        providers.update(custom_providers)

    result = []
    for slug, p in providers.items():
        has_key = True
        if p.auth_token_env:
            has_key = bool(os.environ.get(p.auth_token_env))

        result.append({
            "slug": slug,
            "name": p.name,
            "emoji": p.emoji,
            "description": p.description,
            "available": has_key,
            "auth_env_var": p.auth_token_env or "(native auth)",
        })
    return result
