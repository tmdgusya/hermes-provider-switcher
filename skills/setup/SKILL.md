---
name: provider-switcher-setup
description: Set up API keys for hermes-provider-switcher plugin (GLM, Kimi, MiniMax). Supports fresh setup or migration from shell rc files.
version: 1.0.0
author: roach
license: MIT
metadata:
  hermes:
    tags: [Provider, Setup, GLM, Kimi, MiniMax, API Key, Migration]
    related_skills: [provider-switcher]
---

# Provider Switcher Setup

Configure API keys for the hermes-provider-switcher plugin. Keys are stored in `~/.hermes/.env`.

## Supported Providers

| Provider | Env Variable | Get API Key |
|----------|--------------|-------------|
| GLM | `GT_GLM_AUTH_TOKEN` | https://open.bigmodel.cn |
| Kimi | `GT_KIMI_AUTH_TOKEN` | https://platform.moonshot.cn |
| MiniMax | `GT_MINIMAX_AUTH_TOKEN` | https://www.minimaxi.com |

---

## Quick Setup

### Check Current Status

```bash
# Check which keys are already configured
bash ~/workspace/hermes-provider-switcher/scripts/check-keys.sh
```

### Option 1: Fresh Setup (New Users)

Add API keys to `~/.hermes/.env`:

```bash
# Edit the env file
cat >> ~/.hermes/.env << 'EOF'
GT_GLM_AUTH_TOKEN=your-glm-key-here
GT_KIMI_AUTH_TOKEN=your-kimi-key-here
GT_MINIMAX_AUTH_TOKEN=your-minimax-key-here
EOF
```

Or use the setup helper:

```bash
bash ~/workspace/hermes-provider-switcher/scripts/setup-keys.sh
```

### Option 2: Migrate from Shell RC (Existing Users)

If you previously set keys in `~/.zshrc` or `~/.bashrc`:

```bash
# Auto-detect and migrate
bash ~/workspace/hermes-provider-switcher/scripts/migrate-keys.sh
```

This will:
1. Check `~/.zshrc` and `~/.bashrc` for existing `GT_*` exports
2. Copy them to `~/.hermes/.env`
3. Optionally remove them from shell rc files

---

## Manual Migration

### Step 1: Check existing keys in shell rc

```bash
# Check ~/.zshrc
grep -E "^export GT_(GLM|KIMI|MINIMAX)" ~/.zshrc 2>/dev/null || echo "No keys in ~/.zshrc"

# Check ~/.bashrc
grep -E "^export GT_(GLM|KIMI|MINIMAX)" ~/.bashrc 2>/dev/null || echo "No keys in ~/.bashrc"
```

### Step 2: Extract and add to ~/.hermes/.env

```bash
# Extract from ~/.zshrc (if exists)
grep -E "^export GT_(GLM|KIMI|MINIMAX)" ~/.zshrc 2>/dev/null | sed 's/^export //' >> ~/.hermes/.env

# Extract from ~/.bashrc (if exists)  
grep -E "^export GT_(GLM|KIMI|MINIMAX)" ~/.bashrc 2>/dev/null | sed 's/^export //' >> ~/.hermes/.env

# Remove duplicates
sort -u ~/.hermes/.env -o ~/.hermes/.env
```

### Step 3: (Optional) Remove from shell rc

```bash
# Remove from ~/.zshrc
sed -i '/^export GT_GLM_AUTH_TOKEN=/d' ~/.zshrc
sed -i '/^export GT_KIMI_AUTH_TOKEN=/d' ~/.zshrc
sed -i '/^export GT_MINIMAX_AUTH_TOKEN=/d' ~/.zshrc

# Remove from ~/.bashrc
sed -i '/^export GT_GLM_AUTH_TOKEN=/d' ~/.bashrc
sed -i '/^export GT_KIMI_AUTH_TOKEN=/d' ~/.bashrc
sed -i '/^export GT_MINIMAX_AUTH_TOKEN=/d' ~/.bashrc
```

---

## Verify Setup

```bash
# Check if keys are loaded
source ~/.hermes/.env 2>/dev/null
env | grep -E "^GT_" || echo "No GT_* keys found"

# Test with provider switcher
hermes provider_list
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Keys not recognized | Run `source ~/.hermes/.env` or restart Hermes |
| Duplicate keys | Check both `~/.hermes/.env` and shell rc files |
| Permission denied | Ensure `~/.hermes/.env` is readable by your user |
| Migration failed | Manually copy keys using the steps above |

---

## Why ~/.hermes/.env?

- **Centralized**: All Hermes-related secrets in one place
- **Secure**: File permissions are typically restricted to user-only
- **Portable**: Works across different shells (bash, zsh, fish)
- **Clean**: Keeps shell rc files uncluttered
