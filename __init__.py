"""hermes-provider-switcher plugin -- run Claude Code with alternative LLM providers.

Entry point: register(ctx) is called by the Hermes plugin loader.
"""

from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

_PLUGIN_DIR = Path(__file__).parent
_config: dict = {}


def _check_prerequisites() -> bool:
    """Check that claude CLI is available."""
    return shutil.which("claude") is not None


def register(ctx) -> None:
    """Entry point called by Hermes plugin loader."""
    global _config

    from .config import load_config
    from .schemas import PROVIDER_CLAUDE_CODE_SCHEMA, PROVIDER_LIST_SCHEMA
    from .tools import handle_provider_claude_code, handle_provider_list
    from . import tools as tools_module

    _config = load_config(_PLUGIN_DIR)
    tools_module._config = _config

    toolset = "provider_switcher"

    ctx.register_tool(
        name="provider_claude_code",
        toolset=toolset,
        schema=PROVIDER_CLAUDE_CODE_SCHEMA,
        handler=handle_provider_claude_code,
        description="Run Claude Code with an alternative LLM provider",
        emoji="🔀",
        check_fn=_check_prerequisites,
    )
    ctx.register_tool(
        name="provider_list",
        toolset=toolset,
        schema=PROVIDER_LIST_SCHEMA,
        handler=handle_provider_list,
        description="List available LLM providers and their status",
        emoji="📋",
        check_fn=_check_prerequisites,
    )

    ctx.register_hook("pre_llm_call", _pre_llm_call)

    logger.info("hermes-provider-switcher plugin registered")


def _pre_llm_call(**kwargs) -> dict | None:
    """Inject provider-switcher context into system prompt."""
    from .providers import list_available_providers

    custom_providers = _config.get("custom_providers", {})
    providers = list_available_providers(custom_providers)
    available = [p for p in providers if p["available"]]

    if not available:
        return None

    lines = [
        "Provider Switcher: You can run Claude Code with alternative LLM providers.",
        "Available providers: " + ", ".join(
            f"{p['emoji']} {p['slug']} ({p['name']})" for p in available
        ),
        "Use provider_claude_code tool to run tasks with a specific provider.",
        "Use provider_list tool to check provider availability.",
    ]
    return {"context": "\n".join(lines)}
