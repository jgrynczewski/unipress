"""
Base game class that all Unipress games must inherit from.
Provides standardized difficulty system and input handling.
"""

from abc import ABC, ABCMeta, abstractmethod
from typing import Any

import arcade


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
        width: int = 800,
        height: int = 600,
        title: str = "Unipress Game",
        difficulty: int = 5,
        input_key: int = arcade.MOUSE_BUTTON_LEFT,
        fullscreen: bool = True,
        lives: int = 3,
    ):
        """
        Initialize base game.

        Args:
            width: Window width in pixels (ignored if fullscreen=True)
            height: Window height in pixels (ignored if fullscreen=True)
            title: Game window title
            difficulty: Difficulty level 1-10 (1=easy, 10=hard)
            input_key: Input key/button (default: left mouse click)
            fullscreen: Whether to start in fullscreen mode (default: True)
            lives: Number of lives player starts with (default: 3)
        """
        super().__init__(width, height, title, fullscreen=fullscreen)

        # Validate difficulty range
        if not 1 <= difficulty <= 10:
            raise ValueError("Difficulty must be between 1 and 10")

        self.difficulty = difficulty
        self.input_key = input_key

        # Calculate reaction time window based on difficulty
        # Difficulty 1: 2.0 seconds, Difficulty 10: 0.2 seconds
        self.reaction_time = 2.2 - (difficulty * 0.2)

        # Game state
        self.game_started = False
        self.game_over = False
        self.life_lost_pause = False
        self.score = 0
        self.lives = lives
        self.max_lives = lives

        # Visual feedback for life lost
        self.blink_timer = 0.0
        self.blink_duration = 1.0  # Blink for 1 second
        self.show_player = True

        arcade.set_background_color(arcade.color.BLACK)

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
            self.on_action_press()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Handle keyboard events (if needed for alternative input)."""
        if key == arcade.key.ESCAPE:
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
        self.game_started = True
        self.game_over = False
        self.lives = self.max_lives
        self.score = 0
        self.reset_game()

    def lose_life(self) -> None:
        """Player loses a life. Pause game and wait for click to continue."""
        self.lives -= 1
        if self.lives <= 0:
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
            f"Score: {self.score}", 10, self.height - 30, arcade.color.WHITE, 20
        )

        # Lives display
        arcade.draw_text(
            f"Lives: {self.lives}/{self.max_lives}",
            10,
            self.height - 60,
            arcade.color.WHITE,
            20,
        )

        # Difficulty indicator
        arcade.draw_text(
            f"Difficulty: {self.difficulty}/10",
            10,
            self.height - 90,
            arcade.color.WHITE,
            16,
        )

        # Game over screen
        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                self.width // 2,
                self.height // 2,
                arcade.color.RED,
                50,
                anchor_x="center",
            )
            arcade.draw_text(
                f"Final Score: {self.score}",
                self.width // 2,
                self.height // 2 - 60,
                arcade.color.WHITE,
                30,
                anchor_x="center",
            )
            arcade.draw_text(
                "Click to restart",
                self.width // 2,
                self.height // 2 - 100,
                arcade.color.WHITE,
                20,
                anchor_x="center",
            )

        # Start screen
        elif not self.game_started:
            arcade.draw_text(
                "Click to start",
                self.width // 2,
                self.height // 2,
                arcade.color.WHITE,
                30,
                anchor_x="center",
            )
