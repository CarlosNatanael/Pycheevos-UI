"""
utils/persistence.py - lightweight JSON config persistence

Saves/loads a small config dict to a file next to main.py.
Used for: last open folder, window geometry, etc.
"""

from __future__ import annotations
import json
import os

# Config lives next to main.py regardless of cwd
_CONFIG_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "pycheevos_ui.json")
)

_DEFAULTS: dict = {
    "last_folder": None,
}


def load() -> dict:
    """Return saved config, falling back to defaults for missing keys."""
    config = dict(_DEFAULTS)
    if os.path.isfile(_CONFIG_PATH):
        try:
            with open(_CONFIG_PATH, "r", encoding="utf-8") as fh:
                saved = json.load(fh)
            config.update(saved)
        except Exception:
            pass
    return config


def save(config: dict) -> None:
    """Persist config dict to disk."""
    try:
        with open(_CONFIG_PATH, "w", encoding="utf-8") as fh:
            json.dump(config, fh, indent=2)
    except Exception as exc:
        print(f"[persistence] could not save config: {exc}")