#!/usr/bin/env bash
# Interactive setup for provider switcher API keys

set -e

HERMES_ENV="${HOME}/.hermes/.env"

echo "🔧 Provider Switcher API Key Setup"
echo "==================================="
echo ""
echo "This will add your API keys to ~/.hermes/.env"
echo "Press Enter to skip a provider if you don't have the key yet."
echo ""

# Ensure .hermes directory exists
mkdir -p "$(dirname "$HERMES_ENV")"
touch "$HERMES_ENV"

# Function to add/update key
add_key() {
    local key_name="$1"
    local key_value="$2"
    
    # Remove existing key
    if grep -q "^${key_name}=" "$HERMES_ENV" 2>/dev/null; then
        sed -i "/^${key_name}=/d" "$HERMES_ENV"
    fi
    
    # Add new key
    echo "${key_name}=${key_value}" >> "$HERMES_ENV"
}

# GLM
read -rp "Enter GLM API Key (from https://open.bigmodel.cn): " glm_key
if [ -n "$glm_key" ]; then
    add_key "GT_GLM_AUTH_TOKEN" "$glm_key"
    echo "  ✅ GLM key saved"
else
    echo "  ⏭️  GLM skipped"
fi

# Kimi
read -rp "Enter Kimi API Key (from https://platform.moonshot.cn): " kimi_key
if [ -n "$kimi_key" ]; then
    add_key "GT_KIMI_AUTH_TOKEN" "$kimi_key"
    echo "  ✅ Kimi key saved"
else
    echo "  ⏭️  Kimi skipped"
fi

# MiniMax
read -rp "Enter MiniMax API Key (from https://www.minimaxi.com): " minimax_key
if [ -n "$minimax_key" ]; then
    add_key "GT_MINIMAX_AUTH_TOKEN" "$minimax_key"
    echo "  ✅ MiniMax key saved"
else
    echo "  ⏭️  MiniMax skipped"
fi

# Remove duplicate empty lines
sed -i '/^[[:space:]]*$/d' "$HERMES_ENV"

echo ""
echo "==================================="
echo "✅ Setup complete!"
echo ""
echo "Keys saved to: ~/.hermes/.env"
echo ""
echo "💡 To verify, run:"
echo "  bash ~/workspace/hermes-provider-switcher/scripts/check-keys.sh"
