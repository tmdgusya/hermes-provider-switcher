#!/usr/bin/env bash
# Migrate API keys from shell rc files to ~/.hermes/.env

# set -e  # Handle errors manually for better UX

HERMES_ENV="${HOME}/.hermes/.env"
ZSHRC="${HOME}/.zshrc"
BASHRC="${HOME}/.bashrc"

echo "🔄 Provider Switcher Key Migration"
echo "==================================="
echo ""

# Ensure .hermes directory exists
mkdir -p "$(dirname "$HERMES_ENV")"
touch "$HERMES_ENV"

migrated_count=0

# Function to migrate key from file
migrate_from_file() {
    local src_file="$1"
    local key_name="$2"
    
    if [ ! -f "$src_file" ]; then
        return 1
    fi
    
    if grep -q "^export ${key_name}=" "$src_file" 2>/dev/null; then
        local key_value
        key_value=$(grep "^export ${key_name}=" "$src_file" | tail -1 | sed 's/^export //' | cut -d= -f2-)
        
        if [ -n "$key_value" ]; then
            # Remove existing key in env file
            if grep -q "^${key_name}=" "$HERMES_ENV" 2>/dev/null; then
                sed -i "/^${key_name}=/d" "$HERMES_ENV"
                echo "  📝 $key_name: Updated in ~/.hermes/.env (was: $src_file)"
            else
                echo "  ✅ $key_name: Migrated from $src_file"
            fi
            
            # Add to env file
            echo "${key_name}=${key_value}" >> "$HERMES_ENV"
            return 0
        fi
    fi
    return 1
}

echo "🔍 Scanning for existing keys..."
echo ""

# Check and migrate from zshrc
if [ -f "$ZSHRC" ]; then
    migrate_from_file "$ZSHRC" "GT_GLM_AUTH_TOKEN" && ((migrated_count++))
    migrate_from_file "$ZSHRC" "GT_KIMI_AUTH_TOKEN" && ((migrated_count++))
    migrate_from_file "$ZSHRC" "GT_MINIMAX_AUTH_TOKEN" && ((migrated_count++))
fi

# Check and migrate from bashrc
if [ -f "$BASHRC" ]; then
    migrate_from_file "$BASHRC" "GT_GLM_AUTH_TOKEN" && ((migrated_count++))
    migrate_from_file "$BASHRC" "GT_KIMI_AUTH_TOKEN" && ((migrated_count++))
    migrate_from_file "$BASHRC" "GT_MINIMAX_AUTH_TOKEN" && ((migrated_count++))
fi

# Remove duplicate empty lines
sed -i '/^[[:space:]]*$/d' "$HERMES_ENV"

if [ "$migrated_count" -eq 0 ]; then
    echo "  ℹ️  No existing keys found in ~/.zshrc or ~/.bashrc"
    echo ""
    echo "💡 To set up new keys, run:"
    echo "  bash ~/workspace/hermes-provider-switcher/scripts/setup-keys.sh"
else
    echo ""
    echo "==================================="
    echo "✅ Migration complete!"
    echo "   $migrated_count key(s) migrated to ~/.hermes/.env"
    echo ""
    
    # Ask if user wants to remove from shell rc
    echo "🧹 Would you like to remove the migrated keys from shell rc files?"
    echo "   (This keeps your shell config clean)"
    read -rp "   Remove from shell rc? [y/N]: " cleanup
    
    if [[ "$cleanup" =~ ^[Yy]$ ]]; then
        echo ""
        echo "🗑️  Cleaning up shell rc files..."
        
        # Clean zshrc
        if [ -f "$ZSHRC" ]; then
            sed -i '/^export GT_GLM_AUTH_TOKEN=/d' "$ZSHRC" 2>/dev/null || true
            sed -i '/^export GT_KIMI_AUTH_TOKEN=/d' "$ZSHRC" 2>/dev/null || true
            sed -i '/^export GT_MINIMAX_AUTH_TOKEN=/d' "$ZSHRC" 2>/dev/null || true
            echo "  ✅ Cleaned ~/.zshrc"
        fi
        
        # Clean bashrc
        if [ -f "$BASHRC" ]; then
            sed -i '/^export GT_GLM_AUTH_TOKEN=/d' "$BASHRC" 2>/dev/null || true
            sed -i '/^export GT_KIMI_AUTH_TOKEN=/d' "$BASHRC" 2>/dev/null || true
            sed -i '/^export GT_MINIMAX_AUTH_TOKEN=/d' "$BASHRC" 2>/dev/null || true
            echo "  ✅ Cleaned ~/.bashrc"
        fi
        
        echo ""
        echo "📝 Note: You may need to restart your terminal or run:"
        echo "   source ~/.zshrc  # or source ~/.bashrc"
    else
        echo ""
        echo "📝 Keys kept in both locations (safe mode)"
    fi
fi

echo ""
echo "==================================="
echo "💡 To verify your setup, run:"
echo "   bash ~/workspace/hermes-provider-switcher/scripts/check-keys.sh"
