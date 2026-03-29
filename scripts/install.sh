#!/usr/bin/env bash
# hermes-provider-switcher installer
# Usage:
#   bash scripts/install.sh            # fresh install
#   bash scripts/install.sh --update   # update plugin files, preserve config
#   bash scripts/install.sh --check    # check installed version vs repo
set -euo pipefail

MODE="install"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --update)  MODE="update"; shift ;;
        --check)   MODE="check"; shift ;;
        -h|--help)
            echo "Usage: bash scripts/install.sh [--update|--check]"
            echo "  (default)  Fresh install"
            echo "  --update   Update plugin files, preserve config"
            echo "  --check    Show installed vs repo version"
            exit 0 ;;
        *) shift ;;
    esac
done

# ── Paths ─────────────────────────────────────────────────────────────────
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
PLUGIN_DIR="$HERMES_HOME/plugins/hermes-provider-switcher"
SKILLS_DIR="$HERMES_HOME/skills/provider-switcher"
SRC_DIR="$REPO_DIR/src/hermes_provider_switcher"

log()  { printf "[INFO]  %s\n" "$*" >&2; }
warn() { printf "[WARN]  %s\n" "$*" >&2; }
err()  { printf "[ERROR] %s\n" "$*" >&2; exit 1; }

# ── Check mode ────────────────────────────────────────────────────────────
if [[ "$MODE" == "check" ]]; then
    if [[ ! -f "$PLUGIN_DIR/plugin.yaml" ]]; then
        echo "Not installed" >&2
        exit 1
    fi
    installed_ver=$(grep '^version:' "$PLUGIN_DIR/plugin.yaml" | head -1 | sed 's/^version:[[:space:]]*//' | tr -d '"')
    repo_ver=$(grep '^version:' "$SRC_DIR/plugin.yaml" | head -1 | sed 's/^version:[[:space:]]*//' | tr -d '"')
    echo "Installed: $installed_ver"
    echo "Repo:      $repo_ver"
    if [[ "$installed_ver" == "$repo_ver" ]]; then
        echo "Up to date."
    else
        echo "Update available."
    fi
    exit 0
fi

# ── Prerequisites ─────────────────────────────────────────────────────────
command -v claude &>/dev/null || warn "claude CLI not found. Install: npm install -g @anthropic-ai/claude-code"

# ── Install / Update ─────────────────────────────────────────────────────
if [[ "$MODE" == "update" ]]; then
    [[ -d "$REPO_DIR/.git" ]] && {
        log "Pulling latest..."
        (cd "$REPO_DIR" && git pull --ff-only 2>&1) >&2 || warn "git pull failed"
    }
fi

# Plugin files (always overwrite source, preserve config)
mkdir -p "$PLUGIN_DIR"
for f in __init__.py providers.py schemas.py tools.py config.py plugin.yaml; do
    if [[ -f "$SRC_DIR/$f" ]]; then
        cp "$SRC_DIR/$f" "$PLUGIN_DIR/$f"
    fi
done

# Config (no-clobber)
if [[ ! -f "$PLUGIN_DIR/config.yaml" ]]; then
    cp "$SRC_DIR/config.yaml.example" "$PLUGIN_DIR/config.yaml"
    log "Created config.yaml from example (edit as needed)"
fi

# Skills (no-clobber)
if [[ -d "$REPO_DIR/skills" ]]; then
    # Install skill into the skills directory
    mkdir -p "$SKILLS_DIR"
    cp -rn "$REPO_DIR/skills/"* "$SKILLS_DIR/" 2>/dev/null || true
    log "Skills installed to $SKILLS_DIR"
fi

log "Done! Plugin installed to $PLUGIN_DIR"
log "Verify: hermes plugins list"
log ""
log "Set your API keys as environment variables:"
log "  export GT_GLM_AUTH_TOKEN='your-key'"
log "  export GT_KIMI_AUTH_TOKEN='your-key'"
log "  export GT_MINIMAX_AUTH_TOKEN='your-key'"
