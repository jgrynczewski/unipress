"""
Settings management for Unipress games.

Handles hierarchical settings loading with priority:
1. Constructor parameters (highest)
2. Game-specific settings
3. Global settings
4. Default values (lowest)
"""

from pathlib import Path
from typing import Any

import tomli


def get_default_settings() -> dict[str, Any]:
    """Get hardcoded default settings."""
    return {
        "game": {
            "difficulty": 5,
            "lives": 3,
            "fullscreen": True,
        },
        "ui": {
            "blink_duration": 1.0,
            "language": "pl_PL",
        }
    }


def load_toml_file(file_path: str | Path) -> dict[str, Any]:
    """Load TOML file safely, return empty dict if file doesn't exist."""
    try:
        with open(file_path, "rb") as f:
            return tomli.load(f)
    except (FileNotFoundError, tomli.TOMLDecodeError):
        return {}


def merge_settings(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Merge two settings dictionaries recursively."""
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_settings(result[key], value)
        else:
            result[key] = value

    return result


def load_settings(game_name: str, **constructor_overrides) -> dict[str, Any]:
    """
    Load settings with hierarchical priority.
    
    Args:
        game_name: Name of the game (e.g., "demo_jump")
        **constructor_overrides: Settings passed to BaseGame constructor
        
    Returns:
        Merged settings dictionary
    """
    # 1. Start with defaults
    settings = get_default_settings()

    # 2. Load global settings
    global_settings_path = Path("unipress") / "settings.toml"
    global_settings = load_toml_file(global_settings_path)
    if global_settings:
        settings = merge_settings(settings, global_settings)

    # 3. Load game-specific settings
    game_settings_path = Path("unipress") / "games" / game_name / "settings.toml"
    game_settings = load_toml_file(game_settings_path)
    if game_settings:
        settings = merge_settings(settings, game_settings)

    # 4. Apply constructor overrides
    if constructor_overrides:
        # Convert flat constructor params to nested structure
        game_overrides = {}
        for key, value in constructor_overrides.items():
            if value is not None:
                if key in ["difficulty", "lives", "fullscreen"]:
                    if "game" not in game_overrides:
                        game_overrides["game"] = {}
                    game_overrides["game"][key] = value
                elif key in ["blink_duration", "language"]:
                    if "ui" not in game_overrides:
                        game_overrides["ui"] = {}
                    game_overrides["ui"][key] = value

        if game_overrides:
            settings = merge_settings(settings, game_overrides)

    return settings


def get_setting(settings: dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    Get setting value using dot notation.
    
    Args:
        settings: Settings dictionary
        key_path: Dot-separated path (e.g., "game.difficulty")
        default: Default value if key not found
        
    Returns:
        Setting value or default
    """
    keys = key_path.split(".")
    value = settings

    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default

    return value
