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


def _install_skills():
    """Copy bundled skills to ~/.hermes/skills/ on first load."""
    try:
        from hermes_cli.config import get_hermes_home
        hermes_home = get_hermes_home()
    except Exception:
        hermes_home = Path.home() / ".hermes"

    skills_source = _PLUGIN_DIR / "skills"
    if not skills_source.exists():
        return

    skills_dest = hermes_home / "skills"

    # Copy each skill directory
    for skill_dir in skills_source.iterdir():
        if not skill_dir.is_dir():
            continue

        dest_skill = skills_dest / skill_dir.name

        # If skill already exists, don't overwrite (preserve user edits)
        if dest_skill.exists():
            logger.debug("Skill %s already exists, skipping", skill_dir.name)
            continue

        try:
            shutil.copytree(skill_dir, dest_skill)
            logger.info("Installed skill: %s", skill_dir.name)
        except Exception as exc:
            logger.warning("Failed to install skill %s: %s", skill_dir.name, exc)


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

    # Install bundled skills
    _install_skills()

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
