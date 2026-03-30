#!/usr/bin/env bash
# Check provider switcher API key status

# set -e  # Don't exit on error - we want to show all status

HERMES_ENV="${HOME}/.hermes/.env"
ZSHRC="${HOME}/.zshrc"
BASHRC="${HOME}/.bashrc"

echo "🔍 Provider Switcher API Key Status"
echo "===================================="
echo ""

# Function to check if key exists
check_key() {
    local file="$1"
    local key="$2"
    local location="$3"
    
    if [ -f "$file" ] && grep -q "^${key}=" "$file" 2>/dev/null; then
        local value
        value=$(grep "^${key}=" "$file" | tail -1 | cut -d= -f2-)
        if [ -n "$value" ]; then
            echo "  ✅ $key: SET ($location)"
            return 0
        fi
    fi
    echo "  ❌ $key: NOT SET"
    return 1
}

echo "📁 ~/.hermes/.env:"
if [ -f "$HERMES_ENV" ]; then
    check_key "$HERMES_ENV" "GT_GLM_AUTH_TOKEN" "env file"
    check_key "$HERMES_ENV" "GT_KIMI_AUTH_TOKEN" "env file"
    check_key "$HERMES_ENV" "GT_MINIMAX_AUTH_TOKEN" "env file"
else
    echo "  ⚠️  ~/.hermes/.env not found"
fi

echo ""
echo "🐚 Shell RC files:"

# Check zshrc
if [ -f "$ZSHRC" ]; then
    has_zsh_key=false
    if grep -q "^export GT_GLM_AUTH_TOKEN=" "$ZSHRC" 2>/dev/null || \
       grep -q "^export GT_KIMI_AUTH_TOKEN=" "$ZSHRC" 2>/dev/null || \
       grep -q "^export GT_MINIMAX_AUTH_TOKEN=" "$ZSHRC" 2>/dev/null; then
        has_zsh_key=true
    fi
    
    if [ "$has_zsh_key" = true ]; then
        echo "  ~/.zshrc:"
        grep "^export GT_.*_AUTH_TOKEN=" "$ZSHRC" 2>/dev/null | while read -r line; do
            key=$(echo "$line" | sed 's/^export //' | cut -d= -f1)
            echo "    • $key: SET"
        done
    else
        echo "  ~/.zshrc: No GT_* keys found"
    fi
else
    echo "  ~/.zshrc: Not found"
fi

# Check bashrc
if [ -f "$BASHRC" ]; then
    has_bash_key=false
    if grep -q "^export GT_GLM_AUTH_TOKEN=" "$BASHRC" 2>/dev/null || \
       grep -q "^export GT_KIMI_AUTH_TOKEN=" "$BASHRC" 2>/dev/null || \
       grep -q "^export GT_MINIMAX_AUTH_TOKEN=" "$BASHRC" 2>/dev/null; then
        has_bash_key=true
    fi
    
    if [ "$has_bash_key" = true ]; then
        echo "  ~/.bashrc:"
        grep "^export GT_.*_AUTH_TOKEN=" "$BASHRC" 2>/dev/null | while read -r line; do
            key=$(echo "$line" | sed 's/^export //' | cut -d= -f1)
            echo "    • $key: SET"
        done
    else
        echo "  ~/.bashrc: No GT_* keys found"
    fi
else
    echo "  ~/.bashrc: Not found"
fi

echo ""
echo "===================================="
echo ""
echo "💡 Next steps:"
echo "  • Setup new keys: bash ~/workspace/hermes-provider-switcher/scripts/setup-keys.sh"
echo "  • Migrate existing: bash ~/workspace/hermes-provider-switcher/scripts/migrate-keys.sh"
