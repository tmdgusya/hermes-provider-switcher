
A [Hermes Agent](https://github.com/hermes-ai/hermes-agent) plugin that lets you run [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with alternative LLM providers — GLM, Kimi, MiniMax, and more — via natural language.

> "GLM으로 이 프로젝트 리팩토링해줘" → agent calls `provider_claude_code(provider="glm", prompt="...")`

## How It Works

Instead of manually switching environment variables with shell functions, the plugin handles everything as a tool:

1. You tell the agent which provider to use in natural language
2. The agent calls `provider_claude_code` with the right provider slug
3. The plugin builds a subprocess environment with the correct `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`, and model mappings
4. Claude Code runs in an isolated subprocess — no env var pollution in the parent process

## Supported Providers

| Provider | Slug | Auth Env Var | Default Models |
|----------|------|-------------|----------------|
| GLM (Z.ai) | `glm` | `GT_GLM_AUTH_TOKEN` | glm-4.7-flash / glm-5-turbo / glm-5.1 |
| Kimi (Moonshot) | `kimi` | `GT_KIMI_AUTH_TOKEN` | kimi-k2.5 |
| MiniMax | `minimax` | `GT_MINIMAX_AUTH_TOKEN` | MiniMax-M2.5 / MiniMax-M2.7 |
| Claude (native) | `claude` | (OAuth) | Default Anthropic models |

Custom providers can be added via `config.yaml`.

## Installation

### Prerequisites

- [Hermes Agent](https://github.com/hermes-ai/hermes-agent)
- [Claude Code](https://github.com/anthropics/claude-code): `npm install -g @anthropic-ai/claude-code`

### Install

```bash
git clone https://github.com/tmdgusya/hermes-provider-switcher.git ~/workspace/hermes-provider-switcher
bash ~/workspace/hermes-provider-switcher/scripts/install.sh
```

### Set API Keys

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
# GLM (Z.ai)
export GT_GLM_AUTH_TOKEN="your-glm-api-key"

# Kimi (Moonshot)
export GT_KIMI_AUTH_TOKEN="your-kimi-api-key"

# MiniMax
export GT_MINIMAX_AUTH_TOKEN="your-minimax-api-key"
```

### Verify

```bash
hermes plugins list
```

You should see `hermes-provider-switcher` with 2 tools and 1 hook.

## Usage

Just talk to Hermes naturally:

```
"GLM으로 이 파일 리팩토링해줘"
"kimi로 테스트 코드 작성해줘"
"minimax로 이 버그 분석해줘"
"어떤 프로바이더 사용 가능해?"
```

### Tools

#### `provider_claude_code`

Run Claude Code with a specific provider.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `provider` | string | ✅ | Provider slug: `glm`, `kimi`, `minimax`, `claude` |
| `prompt` | string | ✅ | Task prompt for Claude Code |
| `workdir` | string | ❌ | Working directory (default: cwd) |
| `model` | string | ❌ | Override default model |
| `dangerously_skip_permissions` | bool | ❌ | Auto-approve changes (default: true) |

#### `provider_list`

List all available providers and whether their API keys are configured.

## Configuration

Edit `~/.hermes/plugins/hermes-provider-switcher/config.yaml`:

```yaml
# Subprocess timeout in seconds
timeout: 600

# Add custom providers
custom_providers:
  deepseek:
    name: "DeepSeek"
    slug: "deepseek"
    base_url_env: "GT_DEEPSEEK_BASE_URL"
    auth_token_env: "GT_DEEPSEEK_AUTH_TOKEN"
    base_url_default: "https://api.deepseek.com/anthropic"
    default_model_default: "deepseek-r1"
    emoji: "🔵"
    description: "DeepSeek models via Anthropic-compatible proxy"
```

### Environment Variables for Model Overrides

Override default models per provider:

```bash
# GLM
export GT_GLM_HAIKU_MODEL="glm-4.7-flash"
export GT_GLM_SONNET_MODEL="glm-5-turbo"
export GT_GLM_OPUS_MODEL="glm-5.1"

# Kimi
export GT_KIMI_MODEL="kimi-k2.5"

# MiniMax
export GT_MINIMAX_SMALL_MODEL="MiniMax-M2.5"
export GT_MINIMAX_MODEL="MiniMax-M2.7"
```

## Updating

```bash
bash ~/workspace/hermes-provider-switcher/scripts/install.sh --update
```

## How It Differs from gt.sh

| Feature | gt.sh (shell function) | This plugin |
|---------|----------------------|-------------|
| Switching | Manual `gt g` command | Natural language |
| Env scope | Pollutes current shell | Isolated subprocess |
| tmux sync | Required for teammates | Not needed |
| Agent integration | None | Native tool |
| Custom providers | Edit shell script | config.yaml |
| Model override | Per-provider env vars | Per-call `model` param + env vars |

## License

MIT
