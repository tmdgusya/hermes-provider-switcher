# hermes-provider-switcher

[English](README.md) | [한국어](README.ko.md) | **中文**

一个 [Hermes Agent](https://github.com/hermes-ai/hermes-agent) 插件，让你可以通过自然语言使用替代 LLM 提供商（GLM、Kimi、MiniMax 等）来运行 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)。

> "Refactor this project with GLM" → 代理调用 `provider_claude_code(provider="glm", prompt="...")`

## 工作原理

无需通过 shell 函数手动切换环境变量，插件将一切作为工具处理：

1. 用自然语言告诉代理使用哪个提供商
2. 代理使用正确的提供商 slug 调用 `provider_claude_code`
3. 插件构建包含正确 `ANTHROPIC_BASE_URL`、`ANTHROPIC_AUTH_TOKEN` 和模型映射的子进程环境
4. Claude Code 在隔离的子进程中运行——不会污染父进程的环境变量

## 支持的提供商

| 提供商 | Slug | 认证环境变量 | 默认模型 |
|-------|------|------------|---------|
| GLM (Z.ai) | `glm` | `GT_GLM_AUTH_TOKEN` | glm-4.7-flash / glm-5-turbo / glm-5.1 |
| Kimi (Moonshot) | `kimi` | `GT_KIMI_AUTH_TOKEN` | kimi-k2.5 |
| MiniMax | `minimax` | `GT_MINIMAX_AUTH_TOKEN` | MiniMax-M2.5 / MiniMax-M2.7 |
| Claude（原生） | `claude` | (OAuth) | Anthropic 默认模型 |

可通过 `config.yaml` 添加自定义提供商。

## 安装

### 前置要求

- [Hermes Agent](https://github.com/hermes-ai/hermes-agent) v0.3.0+
- [Claude Code](https://github.com/anthropics/claude-code): `npm install -g @anthropic-ai/claude-code`

### 方法 1：Hermes CLI（推荐）

使用 Hermes 插件命令直接安装：

```bash
# 从 GitHub 安装
hermes plugins install https://github.com/tmdgusya/hermes-provider-switcher.git

# 或使用简写（GitHub 仓库）
hermes plugins install tmdgusya/hermes-provider-switcher
```

### 方法 2：手动安装

如果你偏好手动安装或需要自定义：

```bash
git clone https://github.com/tmdgusya/hermes-provider-switcher.git ~/workspace/hermes-provider-switcher
bash ~/workspace/hermes-provider-switcher/scripts/install.sh
```

### 方法 3：pip 安装

用于开发或作为 Python 包使用：

```bash
pip install git+https://github.com/tmdgusya/hermes-provider-switcher.git
```

### 设置 API 密钥

添加到 `~/.zshrc` 或 `~/.bashrc`：

```bash
# GLM (Z.ai)
export GT_GLM_AUTH_TOKEN="your-glm-api-key"

# Kimi (Moonshot)
export GT_KIMI_AUTH_TOKEN="your-kimi-api-key"

# MiniMax
export GT_MINIMAX_AUTH_TOKEN="your-minimax-api-key"
```

### 验证安装

```bash
hermes plugins list
```

应该看到 `hermes-provider-switcher`，包含 2 个工具和 1 个钩子。

## 使用方法

用自然语言与 Hermes 对话即可：

```
"Refactor this file with GLM"
"Write test code with Kimi"
"Analyze this bug with MiniMax"
"What providers are available?"
```

### 工具

#### `provider_claude_code`

使用指定的提供商运行 Claude Code。

| 参数 | 类型 | 必需 | 描述 |
|-----|------|------|------|
| `provider` | string | ✅ | 提供商 slug：`glm`、`kimi`、`minimax`、`claude` |
| `prompt` | string | ✅ | 发送给 Claude Code 的任务提示 |
| `workdir` | string | ❌ | 工作目录（默认：当前目录） |
| `model` | string | ❌ | 覆盖默认模型 |
| `dangerously_skip_permissions` | bool | ❌ | 自动批准所有更改（默认：true） |

#### `provider_list`

列出所有可用的提供商及其 API 密钥配置状态。

## 配置

编辑 `~/.hermes/plugins/hermes-provider-switcher/config.yaml`：

```yaml
# 子进程超时时间（秒）
timeout: 600

# 添加自定义提供商
custom_providers:
  deepseek:
    name: "DeepSeek"
    slug: "deepseek"
    base_url_env: "GT_DEEPSEEK_BASE_URL"
    auth_token_env: "GT_DEEPSEEK_AUTH_TOKEN"
    base_url_default: "https://api.deepseek.com/anthropic"
    default_model_default: "deepseek-r1"
    emoji: "🔵"
    description: "通过 Anthropic 兼容代理的 DeepSeek 模型"
```

### 模型覆盖环境变量

按提供商覆盖默认模型：

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

## 更新

### 通过 Hermes CLI

```bash
hermes plugins update hermes-provider-switcher
```

### 手动更新

```bash
bash ~/workspace/hermes-provider-switcher/scripts/install.sh --update
```

## 与 gt.sh 的区别

| 功能 | gt.sh（shell 函数） | 本插件 |
|-----|-------------------|-------|
| 切换方式 | 手动 `gt g` 命令 | 自然语言 |
| 环境变量范围 | 污染当前 shell | 隔离的子进程 |
| tmux 同步 | teammate 必需 | 不需要 |
| 代理集成 | 无 | 原生工具 |
| 自定义提供商 | 修改 shell 脚本 | config.yaml |
| 模型覆盖 | 按提供商环境变量 | 每次调用的 `model` 参数 + 环境变量 |

## 许可证

MIT
