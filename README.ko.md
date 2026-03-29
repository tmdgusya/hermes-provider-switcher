# hermes-provider-switcher

[English](README.md) | **한국어** | [中文](README.cn.md)

[Hermes Agent](https://github.com/hermes-ai/hermes-agent) 플러그인으로, [Claude Code](https://docs.anthropic.com/en/docs/claude-code)를 대체 LLM 프로바이더(GLM, Kimi, MiniMax 등)로 자연어를 통해 실행할 수 있습니다.

> "GLM으로 이 프로젝트 리팩토링해줘" → 에이전트가 `provider_claude_code(provider="glm", prompt="...")`를 호출

## 동작 방식

셸 함수로 환경변수를 수동 전환하는 대신, 플러그인이 도구로 모든 것을 처리합니다:

1. 에이전트에게 자연어로 사용할 프로바이더를 알려줍니다
2. 에이전트가 적절한 프로바이더 slug로 `provider_claude_code`를 호출합니다
3. 플러그인이 `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`, 모델 매핑이 설정된 서브프로세스 환경을 구성합니다
4. Claude Code가 격리된 서브프로세스에서 실행됩니다 — 부모 프로세스의 환경변수가 오염되지 않습니다

## 지원 프로바이더

| 프로바이더 | Slug | 인증 환경변수 | 기본 모델 |
|-----------|------|-------------|----------|
| GLM (Z.ai) | `glm` | `GT_GLM_AUTH_TOKEN` | glm-4.7-flash / glm-5-turbo / glm-5.1 |
| Kimi (Moonshot) | `kimi` | `GT_KIMI_AUTH_TOKEN` | kimi-k2.5 |
| MiniMax | `minimax` | `GT_MINIMAX_AUTH_TOKEN` | MiniMax-M2.5 / MiniMax-M2.7 |
| Claude (네이티브) | `claude` | (OAuth) | Anthropic 기본 모델 |

`config.yaml`을 통해 커스텀 프로바이더를 추가할 수 있습니다.

## 설치

### 사전 요구사항

- [Hermes Agent](https://github.com/hermes-ai/hermes-agent)
- [Claude Code](https://github.com/anthropics/claude-code): `npm install -g @anthropic-ai/claude-code`

### 설치 방법

```bash
git clone https://github.com/tmdgusya/hermes-provider-switcher.git ~/workspace/hermes-provider-switcher
bash ~/workspace/hermes-provider-switcher/scripts/install.sh
```

### API 키 설정

`~/.zshrc` 또는 `~/.bashrc`에 추가:

```bash
# GLM (Z.ai)
export GT_GLM_AUTH_TOKEN="your-glm-api-key"

# Kimi (Moonshot)
export GT_KIMI_AUTH_TOKEN="your-kimi-api-key"

# MiniMax
export GT_MINIMAX_AUTH_TOKEN="your-minimax-api-key"
```

### 설치 확인

```bash
hermes plugins list
```

`hermes-provider-switcher`가 2개의 도구와 1개의 훅과 함께 표시되어야 합니다.

## 사용법

Hermes에게 자연어로 말하면 됩니다:

```
"GLM으로 이 파일 리팩토링해줘"
"kimi로 테스트 코드 작성해줘"
"minimax로 이 버그 분석해줘"
"어떤 프로바이더 사용 가능해?"
```

### 도구

#### `provider_claude_code`

특정 프로바이더로 Claude Code를 실행합니다.

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `provider` | string | ✅ | 프로바이더 slug: `glm`, `kimi`, `minimax`, `claude` |
| `prompt` | string | ✅ | Claude Code에 전달할 작업 프롬프트 |
| `workdir` | string | ❌ | 작업 디렉토리 (기본값: 현재 디렉토리) |
| `model` | string | ❌ | 기본 모델 오버라이드 |
| `dangerously_skip_permissions` | bool | ❌ | 변경사항 자동 승인 (기본값: true) |

#### `provider_list`

사용 가능한 프로바이더와 API 키 설정 여부를 조회합니다.

## 설정

`~/.hermes/plugins/hermes-provider-switcher/config.yaml` 편집:

```yaml
# 서브프로세스 타임아웃 (초)
timeout: 600

# 커스텀 프로바이더 추가
custom_providers:
  deepseek:
    name: "DeepSeek"
    slug: "deepseek"
    base_url_env: "GT_DEEPSEEK_BASE_URL"
    auth_token_env: "GT_DEEPSEEK_AUTH_TOKEN"
    base_url_default: "https://api.deepseek.com/anthropic"
    default_model_default: "deepseek-r1"
    emoji: "🔵"
    description: "Anthropic 호환 프록시를 통한 DeepSeek 모델"
```

### 모델 오버라이드 환경변수

프로바이더별 기본 모델 오버라이드:

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

## 업데이트

```bash
bash ~/workspace/hermes-provider-switcher/scripts/install.sh --update
```

## gt.sh와의 차이점

| 기능 | gt.sh (셸 함수) | 이 플러그인 |
|-----|----------------|-----------|
| 전환 방식 | 수동 `gt g` 명령 | 자연어 |
| 환경변수 범위 | 현재 셸 오염 | 격리된 서브프로세스 |
| tmux 동기화 | teammate용 필수 | 불필요 |
| 에이전트 통합 | 없음 | 네이티브 도구 |
| 커스텀 프로바이더 | 셸 스크립트 수정 | config.yaml |
| 모델 오버라이드 | 프로바이더별 환경변수 | 호출별 `model` 파라미터 + 환경변수 |

## 라이선스

MIT
