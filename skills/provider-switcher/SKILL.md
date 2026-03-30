---
name: provider-switcher
description: Set up and use the hermes-provider-switcher plugin to run Claude Code with alternative LLM providers (GLM, Kimi, MiniMax).
version: 1.1.0
author: roach
license: MIT
metadata:
  hermes:
    tags: [Provider, Claude-Code, GLM, Kimi, MiniMax, Plugin]
    related_skills: [claude-code, hermes-plugin-dev, provider-switcher-setup]
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

Store API keys in `~/.hermes/.env` (recommended):

```bash
# Quick check
bash ~/workspace/hermes-provider-switcher/scripts/check-keys.sh

# Interactive setup (new users)
bash ~/workspace/hermes-provider-switcher/scripts/setup-keys.sh

# Or migrate from shell rc (existing users)
bash ~/workspace/hermes-provider-switcher/scripts/migrate-keys.sh
```

**Manual setup:**

```bash
cat >> ~/.hermes/.env << 'EOF'
GT_GLM_AUTH_TOKEN=your-glm-key
GT_KIMI_AUTH_TOKEN=your-kimi-key
GT_MINIMAX_AUTH_TOKEN=your-minimax-key
EOF
```

**Get API keys:**
- GLM: https://open.bigmodel.cn
- Kimi: https://platform.moonshot.cn
- MiniMax: https://www.minimaxi.com

### Step 4: Verify

```bash
hermes plugins list
```

## Usage

Once installed, the agent can use these tools:

- `provider_claude_code` — run Claude Code with a specific provider
- `provider_list` — list available providers and their status

### How It Works (Routing Flow)

When you ask the agent to use a specific provider, here's what happens:

```
Natural Language Request (e.g., "GLM으로 리팩토링해줘")
           ↓
    Agent detects provider (GLM)
           ↓
    Load ~/.hermes/.env (Hermes auto-loads)
           ↓
    Map GT_* variables → ANTHROPIC_* variables
           ↓
    Execute: claude -p <prompt> (with modified env)
           ↓
    Return result to you
```

### Environment Variable Mapping

Each provider maps its `GT_*` variables to Claude Code's `ANTHROPIC_*` variables internally:

| Provider | Your `~/.hermes/.env` | Mapped to `ANTHROPIC_*` for Claude Code |
|----------|----------------------|----------------------------------------|
| **GLM** | `GT_GLM_AUTH_TOKEN`<br>`GT_GLM_BASE_URL`<br>`GT_GLM_HAIKU_MODEL`<br>`GT_GLM_SONNET_MODEL`<br>`GT_GLM_OPUS_MODEL` | `ANTHROPIC_AUTH_TOKEN`<br>`ANTHROPIC_BASE_URL`<br>`ANTHROPIC_DEFAULT_HAIKU_MODEL`<br>`ANTHROPIC_DEFAULT_SONNET_MODEL`<br>`ANTHROPIC_DEFAULT_OPUS_MODEL` |
| **Kimi** | `GT_KIMI_AUTH_TOKEN`<br>`GT_KIMI_BASE_URL`<br>`GT_KIMI_MODEL` | `ANTHROPIC_AUTH_TOKEN`<br>`ANTHROPIC_BASE_URL`<br>`ANTHROPIC_MODEL` |
| **MiniMax** | `GT_MINIMAX_AUTH_TOKEN`<br>`GT_MINIMAX_BASE_URL`<br>`GT_MINIMAX_MODEL`<br>`GT_MINIMAX_SMALL_MODEL` | `ANTHROPIC_AUTH_TOKEN`<br>`ANTHROPIC_BASE_URL`<br>`ANTHROPIC_MODEL`<br>`ANTHROPIC_DEFAULT_HAIKU_MODEL` |
| **Claude** | (none — uses `~/.claude/`) | All custom `ANTHROPIC_*` vars are **unset** |

### Natural Language Examples

The agent understands these patterns:
- "GLM으로 이 코드 리팩토링해줘" → Uses GLM provider
- "kimi로 테스트 작성해줘" → Uses Kimi provider  
- "minimax로 문서 작성해줘" → Uses MiniMax provider
- "어떤 프로바이더 쓸 수 있어?" → Lists available providers

### Manual Tool Usage (for debugging)

```bash
# List available providers and their key status
hermes provider_list

# Run Claude Code with specific provider
hermes provider_claude_code provider=glm prompt="Refactor this code"

# With specific model override
hermes provider_claude_code provider=glm model=glm-5-turbo prompt="Hello"
```

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

- **Environment variable loading**: Hermes automatically loads `~/.hermes/.env` at startup. No `source ~/.hermes/.env` needed in the SKILL.
- **API keys must be set as environment variables** (in `~/.hermes/.env`), not in config.yaml
- **The plugin runs Claude Code via `claude -p` (print mode)** — interactive mode is not supported
- **Long tasks may hit the timeout** (default 600s) — increase `timeout` in config.yaml
- **"claude" provider strips all custom env vars** and uses native Anthropic OAuth from `~/.claude/`
- **Variable mapping happens automatically** — you set `GT_GLM_AUTH_TOKEN`, the plugin sets `ANTHROPIC_AUTH_TOKEN` when running Claude
- **If keys were previously in `~/.zshrc` or `~/.bashrc`**, migrate them using `migrate-keys.sh`

## Troubleshooting

### "Provider requires env var 'GT_XXX_AUTH_TOKEN' to be set"

1. Check if the key exists: `grep GT_ ~/.hermes/.env`
2. If missing, add it: `bash ~/workspace/hermes-provider-switcher/scripts/setup-keys.sh`
3. **Important**: Restart Hermes to reload `~/.hermes/.env`

### Provider shows as unavailable

```bash
# Check current status
bash ~/workspace/hermes-provider-switcher/scripts/check-keys.sh

# Verify Hermes loaded the env
hermes provider_list
```
