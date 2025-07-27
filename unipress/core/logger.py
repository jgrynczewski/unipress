"""
Logger initialization and configuration for Unipress games.
Provides centralized logging setup using Loguru with TOML configuration.
"""

import sys
from pathlib import Path

from loguru import logger

from .settings import get_setting, load_settings


def init_logger(game_name: str = None, **overrides) -> None:
    """
    Initialize the logger with settings from TOML configuration.

    Args:
        game_name: Name of the game for per-game settings (optional)
        **overrides: Direct setting overrides for logging configuration
    """
    # Load settings with game-specific overrides if provided
    if game_name:
        settings = load_settings(game_name, **overrides)
    else:
        # Load global settings for system-wide logging
        from . import settings as settings_module

        settings = settings_module.get_default_settings()

        # Apply any direct overrides
        for key, value in overrides.items():
            if "." in key:
                # Handle nested keys like "logging.level"
                parts = key.split(".")
                current = settings
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current[parts[-1]] = value
            else:
                settings[key] = value

    # Remove default handler to avoid duplicate logs
    logger.remove()

    # Get logging configuration
    log_level = get_setting(settings, "logging.level", "INFO")
    console_enabled = get_setting(settings, "logging.console_enabled", True)
    file_enabled = get_setting(settings, "logging.file_enabled", True)
    file_path = get_setting(
        settings, "logging.file_path", "logs/unipress-{time:YYYY-MM-DD}.log"
    )
    rotation = get_setting(settings, "logging.rotation", "10 MB")
    retention = get_setting(settings, "logging.retention", "30 days")
    compression = get_setting(settings, "logging.compression", "gz")
    log_format = get_setting(settings, "logging.format", "json")

    # Console handler (human-readable for development)
    if console_enabled:
        if log_format == "human":
            console_format = (
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            )
        else:
            # Structured format for console too
            console_format = (
                '{{"timestamp": "{time:YYYY-MM-DD HH:mm:ss.SSS}", '
                '"level": "{level}", '
                '"logger": "{name}", '
                '"function": "{function}", '
                '"line": {line}, '
                '"message": "{message}"}}'
            )

        logger.add(
            sys.stderr,
            format=console_format,
            level=log_level,
            colorize=(log_format == "human"),
        )

    # File handler (always JSON for structured logging)
    if file_enabled:
        # Ensure logs directory exists
        log_file_path = Path(file_path)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        file_format = (
            '{{"timestamp": "{time:YYYY-MM-DD HH:mm:ss.SSS}", '
            '"level": "{level}", '
            '"logger": "{name}", '
            '"function": "{function}", '
            '"line": {line}, '
            '"process": {process}, '
            '"thread": {thread}, '
            '"message": "{message}"}}'
        )

        logger.add(
            file_path,
            format=file_format,
            level=log_level,
            rotation=rotation,
            retention=retention,
            compression=compression,
            serialize=False,  # We're already formatting as JSON
        )

    # Log the initialization
    logger.info(
        "Logger initialized",
        extra={
            "game_name": game_name,
            "log_level": log_level,
            "console_enabled": console_enabled,
            "file_enabled": file_enabled,
            "file_path": file_path if file_enabled else None,
        },
    )


def get_logger(name: str = None):
    """
    Get a logger instance with optional name binding.

    Args:
        name: Optional name to bind to the logger (e.g., game name, module name)

    Returns:
        Configured logger instance
    """
    if name:
        return logger.bind(logger_name=name)
    return logger


# Convenience functions for common logging patterns
def log_game_event(event: str, **context):
    """Log a game event with structured context."""
    logger.info(f"Game event: {event}", extra=context)


def log_player_action(action: str, **context):
    """Log a player action with structured context."""
    logger.info(f"Player action: {action}", extra=context)


def log_performance(metric: str, value: float, unit: str = "", **context):
    """Log a performance metric."""
    logger.info(
        f"Performance: {metric}",
        extra={"metric": metric, "value": value, "unit": unit, **context},
    )


def log_error(error: Exception, context: str = "", **extra_context):
    """Log an error with full context and traceback."""
    logger.error(
        f"Error: {context}",
        extra={
            "error_type": type(error).__name__,
            "error_message": str(error),
            **extra_context,
        },
    )
    logger.exception("Full traceback:")
