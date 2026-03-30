"""Tool schemas for provider-switcher plugin.

Hermes expects schemas in the format:
{
    "name": "tool_name",
    "description": "...",
    "parameters": {...}
}
"""

PROVIDER_CLAUDE_CODE_SCHEMA = {
    "name": "provider_claude_code",
    "description": (
        "Run Claude Code with an alternative LLM provider backend. "
        "Spawns a `claude -p` subprocess with the correct environment "
        "variables for the chosen provider (GLM, Kimi, MiniMax, or native Claude). "
        "Use this when the user asks to run Claude Code with a specific provider."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "provider": {
                "type": "string",
                "description": (
                    "Which LLM provider to use. "
                    "Built-in: 'glm', 'kimi', 'minimax', 'claude'. "
                    "Custom providers can be added via config.yaml."
                ),
            },
            "prompt": {
                "type": "string",
                "description": "The task prompt to send to Claude Code via -p flag.",
            },
            "workdir": {
                "type": "string",
                "description": (
                    "Working directory for the Claude Code subprocess. "
                    "Defaults to the current working directory."
                ),
            },
            "model": {
                "type": "string",
                "description": (
                    "Override the default model for this provider. "
                    "If omitted, uses the provider's default model mapping."
                ),
            },
            "dangerously_skip_permissions": {
                "type": "boolean",
                "description": (
                    "Pass --dangerously-skip-permissions to auto-approve all "
                    "file changes. Default: true."
                ),
            },
        },
        "required": ["provider", "prompt"],
    },
}


PROVIDER_LIST_SCHEMA = {
    "name": "provider_list",
    "description": (
        "List all available LLM providers and their status. "
        "Shows which providers have API keys configured and are ready to use."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}
