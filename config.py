"""Configuration loading for provider-switcher plugin."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

_DEFAULTS: Dict[str, Any] = {
    "timeout": 600,
    "custom_providers": {},
}


def load_config(plugin_dir: Path) -> Dict[str, Any]:
    """Load config.yaml from the plugin directory, with defaults."""
    config = dict(_DEFAULTS)
    config_path = plugin_dir / "config.yaml"

    if config_path.exists():
        try:
            import yaml
            data = yaml.safe_load(config_path.read_text()) or {}
            config.update(data)
        except ImportError:
            # Fallback: simple line parser for flat YAML
            for line in config_path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    key, _, val = line.partition(":")
                    val = val.strip().strip('"').strip("'")
                    if val.isdigit():
                        val = int(val)
                    config[key.strip()] = val
        except Exception as exc:
            logger.warning("Failed to parse config.yaml: %s", exc)

    return config
