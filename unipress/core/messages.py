"""
Message loading system for internationalization.

Handles loading and merging of JSON message files with fallback support.
"""

import json
from pathlib import Path
from typing import Any


class MessageLoader:
    """Loads and manages localized messages from JSON files."""

    def __init__(self, language: str, game_name: str):
        """
        Initialize message loader.

        Args:
            language: Language code (e.g., "pl_PL", "en_US")
            game_name: Name of the game for game-specific messages
        """
        self.language = language
        self.game_name = game_name
        self.messages: dict[str, Any] = {}
        self.fallback_language = "pl_PL"  # Polish as default fallback

        # Load messages with fallback
        self._load_messages()

    def _load_json_file(self, file_path: Path) -> dict[str, Any]:
        """Load JSON file safely, return empty dict if file doesn't exist."""
        try:
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _merge_messages(
        self, base: dict[str, Any], override: dict[str, Any]
    ) -> dict[str, Any]:
        """Merge two message dictionaries recursively."""
        result = base.copy()

        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._merge_messages(result[key], value)
            else:
                result[key] = value

        return result

    def _load_messages(self) -> None:
        """Load messages for the specified language with fallback."""
        # Base path for locales
        locales_path = Path("unipress") / "locales"

        # Try to load fallback messages first (pl_PL)
        if self.language != self.fallback_language:
            fallback_messages = self._load_language_messages(
                locales_path, self.fallback_language
            )
            self.messages = fallback_messages

        # Load requested language messages (will override fallback)
        language_messages = self._load_language_messages(locales_path, self.language)
        if language_messages:
            if self.messages:
                self.messages = self._merge_messages(self.messages, language_messages)
            else:
                self.messages = language_messages
        elif not self.messages:
            # If no messages loaded at all, try to load fallback
            self.messages = self._load_language_messages(
                locales_path, self.fallback_language
            )

    def _load_language_messages(
        self, locales_path: Path, language: str
    ) -> dict[str, Any]:
        """Load all message files for a specific language."""
        language_path = locales_path / language
        messages = {}

        # Load common messages
        common_file = language_path / "common.json"
        common_messages = self._load_json_file(common_file)
        if common_messages:
            messages = self._merge_messages(messages, common_messages)

        # Load game-specific messages
        game_file = language_path / "games" / f"{self.game_name}.json"
        game_messages = self._load_json_file(game_file)
        if game_messages:
            messages = self._merge_messages(messages, game_messages)

        return messages

    def get_message(self, key: str, **kwargs) -> str:
        """
        Get localized message with parameter substitution.

        Args:
            key: Dot-separated message key (e.g., "ui.score")
            **kwargs: Parameters for string formatting

        Returns:
            Formatted message string, or the key itself if not found
        """
        # Navigate through nested dictionary using dot notation
        keys = key.split(".")
        value = self.messages

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                # Return key as fallback if message not found
                return key

        # If we found a string, format it with provided parameters
        if isinstance(value, str):
            try:
                return value.format(**kwargs)
            except (KeyError, ValueError):
                # If formatting fails, return unformatted string
                return value

        # If value is not a string, return the key
        return key

    def has_message(self, key: str) -> bool:
        """Check if a message key exists."""
        keys = key.split(".")
        value = self.messages

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return False

        return isinstance(value, str)

    def get_available_languages(self) -> list[str]:
        """Get list of available language codes."""
        locales_path = Path("unipress") / "locales"
        if not locales_path.exists():
            return [self.fallback_language]

        languages = []
        for path in locales_path.iterdir():
            if path.is_dir() and (path / "common.json").exists():
                languages.append(path.name)

        return sorted(languages)

    def reload(self, language: str = None, game_name: str = None) -> None:
        """Reload messages with optionally different language or game."""
        if language is not None:
            self.language = language
        if game_name is not None:
            self.game_name = game_name

        self.messages = {}
        self._load_messages()


def load_messages(language: str, game_name: str) -> MessageLoader:
    """
    Convenience function to create and return a MessageLoader.

    Args:
        language: Language code (e.g., "pl_PL", "en_US")
        game_name: Name of the game

    Returns:
        Configured MessageLoader instance
    """
    return MessageLoader(language, game_name)
