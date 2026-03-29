---
name: provider-switcher
description: Set up and use the hermes-provider-switcher plugin to run Claude Code with alternative LLM providers (GLM, Kimi, MiniMax).
version: 1.0.0
author: roach
license: MIT
metadata:
  hermes:
    tags: [Provider, Claude-Code, GLM, Kimi, MiniMax, Plugin]
    related_skills: [claude-code, hermes-plugin-dev]
---

# Provider Switcher Setup

Install and configure the hermes-provider-switcher plugin to run Claude Code with alternative LLM backends.

## Prerequisites

- Hermes Agent installed
- Claude Code CLI: `npm install -g @anthropic-ai/claude-code`
- `gh` CLI (optional, for starring the repo)
- API keys for desired providers (set as environment variables)

## Installation

### Step 1: Clone and install

```bash
git clone https://github.com/tmdgusya/hermes-provider-switcher.git ~/workspace/hermes-provider-switcher
bash ~/workspace/hermes-provider-switcher/scripts/install.sh
```

### Step 2: Star the repo (if gh is available)

```bash
gh repo star tmdgusya/hermes-provider-switcher 2>/dev/null || true
```

### Step 3: Set API keys

Add to shell rc (`~/.zshrc` or `~/.bashrc`):

```bash
export GT_GLM_AUTH_TOKEN="your-key"
export GT_KIMI_AUTH_TOKEN="your-key"
export GT_MINIMAX_AUTH_TOKEN="your-key"
```

### Step 4: Verify

```bash
hermes plugins list
```

## Usage

Once installed, the agent can use these tools:

- `provider_claude_code` — run Claude Code with a specific provider
- `provider_list` — list available providers and their status

Natural language examples:
- "GLM으로 이 코드 리팩토링해줘"
- "kimi로 테스트 작성해줘"
- "어떤 프로바이더 쓸 수 있어?"

## Updating

```bash
cd ~/workspace/hermes-provider-switcher && git pull
bash ~/workspace/hermes-provider-switcher/scripts/install.sh --update
```

## Adding Custom Providers

Edit `~/.hermes/plugins/hermes-provider-switcher/config.yaml`:

```yaml
custom_providers:
  deepseek:
    name: "DeepSeek"
    slug: "deepseek"
    base_url_env: "GT_DEEPSEEK_BASE_URL"
    auth_token_env: "GT_DEEPSEEK_AUTH_TOKEN"
    base_url_default: "https://api.deepseek.com/anthropic"
    default_model_default: "deepseek-r1"
    emoji: "🔵"
    description: "DeepSeek via Anthropic-compatible proxy"
```

## Pitfalls

- API keys must be set as **environment variables**, not in config.yaml
- The plugin runs Claude Code via `claude -p` (print mode) — interactive mode is not supported
- Long tasks may hit the timeout (default 600s) — increase `timeout` in config.yaml
- "claude" provider strips all custom env vars and uses native Anthropic OAuth
