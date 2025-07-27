"""
Base game class that all Unipress games must inherit from.
Provides standardized difficulty system and input handling.
"""

from abc import ABC, ABCMeta, abstractmethod
from typing import Any

import arcade

from unipress.core.logger import get_logger, log_error, log_game_event, log_player_action
from unipress.core.messages import load_messages
from unipress.core.settings import get_setting, load_settings


class GameMeta(type(arcade.Window), ABCMeta):  # type: ignore[misc]
    """Metaclass that combines arcade.Window and ABC metaclasses."""

    pass


class BaseGame(arcade.Window, ABC, metaclass=GameMeta):  # type: ignore[misc]
    """
    Base class for all one-button games in Unipress.

    Provides:
    - Standardized difficulty system (1-10 scale)
    - Configurable input handling (default: left mouse click)
    - Consistent game structure
    """

    def __init__(
        self,
        game_name: str,
        width: int = 800,
        height: int = 600,
        title: str = "Unipress Game",
        difficulty: int = None,
        input_key: int = arcade.MOUSE_BUTTON_LEFT,
        fullscreen: bool = None,
        lives: int = None,
        language: str = None,
    ):
        """
        Initialize base game.

        Args:
            game_name: Name of the game for settings loading
            width: Window width in pixels (ignored if fullscreen=True)
            height: Window height in pixels (ignored if fullscreen=True)
            title: Game window title
            difficulty: Difficulty level 1-10 (None = use settings)
            input_key: Input key/button (default: left mouse click)
            fullscreen: Whether to start in fullscreen mode (None = use settings)
            lives: Number of lives player starts with (None = use settings)
            language: Language code for messages (None = use settings)
        """
        # Load settings with constructor overrides
        self.settings = load_settings(
            game_name,
            difficulty=difficulty,
            fullscreen=fullscreen,
            lives=lives,
            language=language,
        )

        # Use settings values
        final_difficulty = get_setting(self.settings, "game.difficulty", 5)
        final_lives = get_setting(self.settings, "game.lives", 3)
        final_fullscreen = get_setting(self.settings, "game.fullscreen", True)
        final_language = get_setting(self.settings, "ui.language", "pl_PL")

        # Load localized messages
        self.messages = load_messages(final_language, game_name)

        # Initialize game logger
        self.logger = get_logger(game_name)

        super().__init__(width, height, title, fullscreen=final_fullscreen)

        # Validate difficulty range
        if not 1 <= final_difficulty <= 10:
            raise ValueError("Difficulty must be between 1 and 10")

        self.difficulty = final_difficulty
        self.input_key = input_key

        # Calculate reaction time window based on difficulty
        # Difficulty 1: 2.0 seconds, Difficulty 10: 0.2 seconds
        self.reaction_time = 2.2 - (final_difficulty * 0.2)

        # Game state
        self.game_started = False
        self.game_over = False
        self.life_lost_pause = False
        self.score = 0
        self.lives = final_lives
        self.max_lives = final_lives

        # Visual feedback for life lost
        self.blink_timer = 0.0
        self.blink_duration = get_setting(self.settings, "ui.blink_duration", 1.0)
        self.show_player = True

        arcade.set_background_color(arcade.color.BLACK)

        # Log game initialization
        log_game_event(
            "game_initialized",
            game_name=game_name,
            difficulty=self.difficulty,
            lives=self.lives,
            fullscreen=final_fullscreen,
            language=final_language,
        )

    def get_difficulty_settings(self) -> dict[str, Any]:
        """
        Get difficulty-specific settings for the game.
        Override this method to customize difficulty scaling.

        Returns:
            Dictionary with difficulty-specific game settings
        """
        return {
            "reaction_time": self.reaction_time,
            "difficulty": self.difficulty,
        }

    def get_message(self, key: str, **kwargs) -> str:
        """Get localized message with parameter substitution."""
        return self.messages.get_message(key, **kwargs)

    def update_life_lost_effects(self, delta_time: float) -> None:
        """Update visual effects during life lost pause."""
        if self.life_lost_pause and self.blink_timer < self.blink_duration:
            self.blink_timer += delta_time
            # Blink effect: toggle visibility every 0.1 seconds
            if int(self.blink_timer * 10) % 2 == 0:
                self.show_player = True
            else:
                self.show_player = False

            # After blinking duration, keep player visible
            if self.blink_timer >= self.blink_duration:
                self.show_player = True

    def should_draw_player(self) -> bool:
        """Check if player should be drawn (handles blinking effect)."""
        return self.show_player

    def is_game_paused(self) -> bool:
        """Check if game is currently paused (life lost or game over)."""
        return self.life_lost_pause or self.game_over or not self.game_started

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        """Handle mouse press events."""
        if button == self.input_key:
            log_player_action("mouse_click", button=button, x=x, y=y)
            try:
                self.on_action_press()
            except Exception as e:
                log_error(e, "Error handling mouse press", button=button, x=x, y=y)
                raise

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Handle keyboard events (if needed for alternative input)."""
        if key == arcade.key.ESCAPE:
            log_player_action("key_press", key="ESCAPE", operation="toggle_fullscreen")
            # Toggle fullscreen mode
            self.set_fullscreen(not self.fullscreen)
        # Override in subclass if keyboard input is needed

    def handle_life_lost_continue(self) -> bool:
        """Handle click during life lost pause - continue game."""
        if self.life_lost_pause:
            self.life_lost_pause = False
            self.blink_timer = 0.0
            self.show_player = True
            self.reset_game()
            return True
        return False

    @abstractmethod
    def on_action_press(self) -> None:
        """
        Handle the main action (button press/click).
        This is where the core game logic responds to input.
        Must be implemented by each game.
        """
        pass

    @abstractmethod
    def reset_game(self) -> None:
        """
        Reset game to initial state.
        Must be implemented by each game.
        """
        pass

    def start_game(self) -> None:
        """Start the game."""
        log_game_event("game_started", lives=self.max_lives, difficulty=self.difficulty)
        self.game_started = True
        self.game_over = False
        self.lives = self.max_lives
        self.score = 0
        self.reset_game()

    def lose_life(self) -> None:
        """Player loses a life. Pause game and wait for click to continue."""
        self.lives -= 1
        log_game_event("life_lost", lives_remaining=self.lives, score=self.score)

        if self.lives <= 0:
            log_game_event("game_over", final_score=self.score)
            self.game_over = True
        else:
            # Enter life lost pause state
            self.life_lost_pause = True
            self.blink_timer = 0.0
            self.show_player = True

    def end_game(self) -> None:
        """End the game immediately (deprecated - use lose_life instead)."""
        self.lives = 0
        self.game_over = True

    def draw_ui(self) -> None:
        """Draw common UI elements (score, difficulty info, etc.)."""
        # Score
        arcade.draw_text(
            self.get_message("ui.score", score=self.score),
            10,
            self.height - 30,
            arcade.color.WHITE,
            20,
        )

        # Lives display - right top corner
        arcade.draw_text(
            self.get_message("ui.lives", current=self.lives, max=self.max_lives),
            self.width - 150,
            self.height - 30,
            arcade.color.WHITE,
            20,
        )

        # Difficulty indicator - right bottom corner
        arcade.draw_text(
            self.get_message("ui.difficulty", level=self.difficulty),
            self.width - 200,
            20,
            arcade.color.WHITE,
            16,
        )

        # Game over screen
        if self.game_over:
            arcade.draw_text(
                self.get_message("ui.game_over"),
                self.width // 2,
                self.height // 2,
                arcade.color.RED,
                50,
                anchor_x="center",
            )
            arcade.draw_text(
                self.get_message("ui.final_score", score=self.score),
                self.width // 2,
                self.height // 2 - 60,
                arcade.color.WHITE,
                30,
                anchor_x="center",
            )
            arcade.draw_text(
                self.get_message("ui.click_to_restart"),
                self.width // 2,
                self.height // 2 - 100,
                arcade.color.WHITE,
                20,
                anchor_x="center",
            )

        # Start screen
        elif not self.game_started:
            arcade.draw_text(
                self.get_message("ui.click_to_start"),
                self.width // 2,
                self.height // 2,
                arcade.color.WHITE,
                30,
                anchor_x="center",
            )
