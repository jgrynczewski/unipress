"""
Base game class that all Unipress games must inherit from.
Provides standardized difficulty system and input handling.
"""

from abc import ABC, ABCMeta, abstractmethod
from typing import Any

import arcade

from unipress.core.high_scores import get_high_score, update_high_score
from unipress.core.logger import (
    get_logger,
    log_error,
    log_game_event,
    log_player_action,
)
from unipress.core.messages import load_messages
from unipress.core.settings import get_setting, load_settings
from unipress.core.sound import SoundManager, SoundEvent, STANDARD_SOUND_EVENTS
from unipress.ui.end_game.screen import EndGameAction, EndGameScreen


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

        # Store game name for high score tracking
        self.game_name = game_name

        # Initialize sound system
        self.sound_manager = SoundManager(game_name, self.settings)
        
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
        self.waiting_for_start_click = True  # New state to prevent updates during startup sound
        self.waiting_for_sound = False  # State for non-blocking sound completion
        self.sound_timer = 0.0  # Timer for sound completion
        self._life_lost_completion_pending = False  # Flag for life lost completion
        self.score = 0
        self.lives = final_lives
        self.max_lives = final_lives
        self.high_score_played_this_game = False  # Track if high score sound played this session

        # End game screen
        self.end_game_screen = None
        self.show_end_screen = False

        # Visual feedback for life lost
        self.blink_timer = 0.0
        self.blink_duration = get_setting(self.settings, "ui.blink_duration", 1.0)
        self.show_player = True

        # Cursor positioning settings
        self.cursor_reposition_interval = get_setting(self.settings, "ui.cursor_reposition_interval", 3.0)
        self.cursor_timer = 0.0

        arcade.set_background_color(arcade.color.BLACK)

        # Position cursor to bottom-right corner with 2% shift toward center after fullscreen initialization
        if final_fullscreen:
            self._position_cursor_bottom_right()

        # Log game initialization
        log_game_event(
            "game_initialized",
            game_name=game_name,
            difficulty=self.difficulty,
            lives=self.lives,
            fullscreen=final_fullscreen,
            language=final_language,
        )

    def _position_cursor_bottom_right(self) -> None:
        """Position cursor to bottom-right corner with 2% shift toward center."""
        try:
            # Calculate position: bottom-right minus 2% of screen dimensions  
            cursor_x = int(self.width * 0.98)
            cursor_y = int(self.height * 0.02)  # 2% from bottom (arcade uses bottom-left origin)
            
            # Use arcade's built-in method to position cursor
            self.set_mouse_position(cursor_x, cursor_y)
            log_game_event("cursor_positioned", x=cursor_x, y=cursor_y)
            
        except Exception as e:
            # Don't fail the game if cursor positioning fails
            log_error(e, "Failed to position cursor")

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
    
    def play_sound_event(self, event_name: str, volume_override: float = None) -> arcade.Sound:
        """Play a standard sound event.
        
        Args:
            event_name: Name of the sound event (from STANDARD_SOUND_EVENTS)
            volume_override: Optional volume override (0.0-1.0)
            
        Returns:
            Playing arcade.Sound or None if sound unavailable
        """
        if event_name in STANDARD_SOUND_EVENTS:
            event = STANDARD_SOUND_EVENTS[event_name]
            return self.sound_manager.play_sound(event, volume_override)
        else:
            log_error(f"Unknown sound event: {event_name}")
            return None
    
    def play_custom_sound_event(self, event: SoundEvent, volume_override: float = None) -> arcade.Sound:
        """Play a custom sound event.
        
        Args:
            event: Custom SoundEvent definition
            volume_override: Optional volume override (0.0-1.0)
            
        Returns:
            Playing arcade.Sound or None if sound unavailable
        """
        return self.sound_manager.play_sound(event, volume_override)
    
    def start_game_sound_timer(self) -> None:
        """Start non-blocking game start sound timer."""
        if get_setting(self.settings, "audio.startup_delay", True):
            startup_sound = self.play_sound_event("game_start")
            if startup_sound:
                self.waiting_for_sound = True
                self.sound_timer = 3.0  # Assume 3 seconds for game start sound
                log_game_event("game_start_sound_started")
            else:
                # No sound to wait for, continue immediately
                self.complete_game_start()
        else:
            # Sound disabled, continue immediately  
            self.complete_game_start()
    
    def update_sound_timer(self, delta_time: float) -> None:
        """Update non-blocking sound timer."""
        if self.waiting_for_sound:
            self.sound_timer -= delta_time
            if self.sound_timer <= 0:
                self.waiting_for_sound = False
                self.sound_timer = 0.0
                log_game_event("game_start_sound_completed")
                
                if self._life_lost_completion_pending:
                    self._life_lost_completion_pending = False
                    self._complete_life_lost_continue()
                else:
                    self.complete_game_start()
    
    def complete_game_start(self) -> None:
        """Complete the game start sequence."""
        self.game_started = True
        self.game_over = False
        self.waiting_for_start_click = False
        self.waiting_for_sound = False
        self.lives = self.max_lives
        self.score = 0
        self.high_score_played_this_game = False  # Reset high score sound flag for new game
        
        # Reset animations to prevent accumulated time during startup sound
        self.reset_animations()
        
        self.reset_game()
    
    def check_and_play_high_score_sound(self, new_score: int) -> None:
        """Check if new score beats high score and play sound once per game."""
        if not self.high_score_played_this_game:
            current_high_score = get_high_score(self.game_name)
            if new_score > current_high_score:
                self.play_sound_event("high_score")
                self.high_score_played_this_game = True
                log_game_event("high_score_sound_played", new_score=new_score, 
                              previous_high_score=current_high_score)
    
    def _complete_life_lost_continue(self) -> None:
        """Complete the life lost continuation sequence."""
        # Visual reset already done, just ensure game can continue
        pass

    def update_cursor_positioning(self, delta_time: float) -> None:
        """Update periodic cursor positioning timer."""
        self.cursor_timer += delta_time
        if self.cursor_timer >= self.cursor_reposition_interval:
            self._position_cursor_bottom_right()
            self.cursor_timer = 0.0

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
        return self.life_lost_pause or self.game_over or not self.game_started or self.waiting_for_start_click or self.waiting_for_sound

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        """Handle mouse press events."""
        if button == self.input_key:
            log_player_action("mouse_click", button=button, x=x, y=y)
            try:
                # Handle end game screen interactions
                if self.show_end_screen and self.end_game_screen and not self.waiting_for_sound:
                    action = self.end_game_screen.get_selected_action()
                    log_player_action("end_screen_action", operation=action.value)
                    if action == EndGameAction.PLAY_AGAIN:
                        self._restart_game()
                    elif action == EndGameAction.EXIT:
                        self._exit_game()
                    return

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
        """Handle click during life lost pause - continue game only after blinking ends."""
        if self.life_lost_pause:
            # Only allow continuation after blinking period is complete and not already processing sound
            if self.blink_timer >= self.blink_duration and not self.waiting_for_sound:
                # Play button click sound
                self.play_sound_event("ui_confirm")
                
                # Reset visual state immediately
                self.life_lost_pause = False
                self.blink_timer = 0.0
                self.show_player = True
                
                # Reset animations and game state visually
                self.reset_animations()
                self.reset_game()
                
                # Start non-blocking game start sound for life continuation
                if get_setting(self.settings, "audio.startup_delay", True):
                    startup_sound = self.play_sound_event("game_start")
                    if startup_sound:
                        self.waiting_for_sound = True
                        self.sound_timer = 3.0  # Assume 3 seconds for game start sound
                        # Set up completion callback for life lost
                        self._life_lost_completion_pending = True
                    else:
                        self._complete_life_lost_continue()
                else:
                    self._complete_life_lost_continue()
                return True
            # During blinking period, ignore clicks
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
    
    def reset_animations(self) -> None:
        """
        Reset all animations to prevent accumulated time.
        Override in subclass if needed.
        """
        pass

    def start_game(self) -> None:
        """Start the game after user clicks."""
        # Play button click sound
        self.play_sound_event("ui_confirm")
        
        log_game_event("game_started", lives=self.max_lives, difficulty=self.difficulty)
        
        # Start non-blocking game start sound timer
        self.start_game_sound_timer()

    def lose_life(self) -> None:
        """Player loses a life. Pause game and wait for click to continue."""
        self.lives -= 1
        log_game_event("life_lost", lives_remaining=self.lives, score=self.score)

        if self.lives <= 0:
            # Update high score when game ends
            is_new_record = update_high_score(self.game_name, self.score)
            
            # Always play game over sound (high score already played during game)
            self.play_sound_event("game_over")
            
            log_game_event(
                "game_over", final_score=self.score, new_high_score=is_new_record
            )
            self.game_over = True
            self.show_end_screen = True
            self.end_game_screen = EndGameScreen(
                self.messages,
                self.score,
                game_name=self.game_name,
                on_cycle=lambda: self.play_sound_event("ui_cycle"),            
            )
        else:
            # Enter life lost pause state
            self.life_lost_pause = True
            self.blink_timer = 0.0
            self.show_player = True

    def end_game(self) -> None:
        """End the game immediately (deprecated - use lose_life instead)."""
        self.lives = 0
        self.game_over = True

    def _restart_game(self) -> None:
        """Restart the game from end screen."""
        log_game_event("game_restarted", previous_score=self.score)
        self.show_end_screen = False
        self.end_game_screen = None
        
        # Play button click sound
        self.play_sound_event("ui_confirm")
        
        # Reset visual state immediately (same as life lost continuation)
        self.game_over = False
        self.lives = self.max_lives
        self.score = 0
        
        # Reset animations and game state visually
        self.reset_animations()
        self.reset_game()
        
        # Start non-blocking game start sound
        if get_setting(self.settings, "audio.startup_delay", True):
            startup_sound = self.play_sound_event("game_start")
            if startup_sound:
                self.waiting_for_sound = True
                self.sound_timer = 3.0  # Assume 3 seconds for game start sound
                # This will trigger complete_game_start() when sound finishes
            else:
                self.complete_game_start()
        else:
            self.complete_game_start()

    def _exit_game(self) -> None:
        """Exit the game from end screen."""
        log_game_event("game_exited", final_score=self.score)
        self.close()

    def draw_heart(self, x: float, y: float, filled: bool = True) -> None:
        """Draw a smooth heart shape at the given position."""
        # Create heart shape using polygon points for smoother curves
        heart_points = [
            (x, y - 12),  # bottom point
            (x - 8, y - 4),   # left bottom curve
            (x - 12, y + 2),  # left side
            (x - 8, y + 8),   # left top curve
            (x - 4, y + 6),   # left top center
            (x, y + 2),       # center dip
            (x + 4, y + 6),   # right top center  
            (x + 8, y + 8),   # right top curve
            (x + 12, y + 2),  # right side
            (x + 8, y - 4),   # right bottom curve
        ]
        
        if filled:
            # Draw filled heart with smooth polygon
            arcade.draw_polygon_filled(heart_points, arcade.color.RED)
        
        # Draw outline for definition
        arcade.draw_polygon_outline(heart_points, arcade.color.DARK_RED, 2)

    def draw_hearts(self) -> None:
        """Draw hearts to represent remaining lives."""
        heart_spacing = 35
        start_x = self.width - 80
        start_y = self.height - 25
        
        for i in range(self.max_lives):
            x = start_x - (i * heart_spacing)
            # Hearts disappear from right to left (reverse order)
            filled = (self.max_lives - 1 - i) < self.lives
            self.draw_heart(x, start_y, filled)

    def draw_ui(self) -> None:
        """Draw common UI elements (score, difficulty info, etc.)."""
        # Score with high score
        high_score = get_high_score(self.game_name)
        score_text = (
            f"{self.get_message('ui.score', score=self.score)} / Record: {high_score}"
        )
        arcade.draw_text(
            score_text,
            10,
            self.height - 30,
            arcade.color.BLACK,  # Simple black text for good contrast
            20,
            font_name="Kenney Pixel Square"  # Keep the nicer font
        )

        # Lives display - hearts in right top corner
        self.draw_hearts()

        # Difficulty indicator - right bottom corner
        difficulty_text = self.get_message("ui.difficulty", level=self.difficulty)
        diff_x = self.width - 200
        diff_y = 20
        
        arcade.draw_text(
            difficulty_text,
            diff_x,
            diff_y,
            arcade.color.LIGHT_BLUE,  # Light blue for consistency
            16,
            font_name="Kenney Pixel Square"
        )

        # End game screen (replaces old game over screen)
        if self.show_end_screen and self.end_game_screen:
            self.end_game_screen.draw(self.width, self.height)

        # Start screen
        elif not self.game_started:
            start_text = self.get_message("ui.click_to_start")
            start_x = self.width // 2
            start_y = self.height // 2
            
            arcade.draw_text(
                start_text,
                start_x,
                start_y,
                arcade.color.BLACK,  # Simple black text for good contrast
                30,
                anchor_x="center",
                font_name="Kenney Pixel Square"
            )
