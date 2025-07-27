"""
End Game Screen UI Component

Provides standardized end game screen with two cycling buttons:
- Play Again: Restart the current game
- Exit: Close the game

Buttons cycle on each click, selected button is highlighted.
"""

from enum import Enum

import arcade

from unipress.core.high_scores import get_high_score, is_new_high_score
from unipress.core.logger import log_game_event, log_player_action
from unipress.core.messages import MessageLoader


class EndGameAction(Enum):
    """Available actions on end game screen."""

    PLAY_AGAIN = "play_again"
    EXIT = "exit"


class EndGameScreen:
    """
    Standardized end game screen with cycling buttons.

    Features:
    - Two buttons: Play Again / Exit
    - Buttons cycle on each click
    - Selected button is highlighted
    - Shared across all games with override capability
    """

    def __init__(
        self,
        messages: MessageLoader,
        final_score: int = 0,
        cycle_time: float = 2.0,
        game_name: str = "",
    ):
        """
        Initialize end game screen.

        Args:
            messages: Message loader for localized text
            final_score: Player's final score to display
            cycle_time: Time in seconds between automatic button cycling
            game_name: Name of the game for high score lookup
        """
        self.messages = messages
        self.final_score = final_score
        self.cycle_time = cycle_time
        self.game_name = game_name

        # Button state
        self.selected_button = EndGameAction.PLAY_AGAIN  # Default selection
        self.button_actions = [EndGameAction.PLAY_AGAIN, EndGameAction.EXIT]

        # Timing for automatic cycling
        self.time_since_last_cycle = 0.0

        # Colors
        self.normal_color = arcade.color.LIGHT_GRAY
        self.selected_color = arcade.color.YELLOW
        self.text_color = arcade.color.BLACK

        log_game_event("end_game_screen_shown", final_score=final_score)

    def update(self, delta_time: float) -> None:
        """
        Update the end game screen (handles automatic cycling).

        Args:
            delta_time: Time elapsed since last update in seconds
        """
        self.time_since_last_cycle += delta_time

        if self.time_since_last_cycle >= self.cycle_time:
            # Cycle to next button
            current_index = self.button_actions.index(self.selected_button)
            next_index = (current_index + 1) % len(self.button_actions)
            self.selected_button = self.button_actions[next_index]

            # Reset timer
            self.time_since_last_cycle = 0.0

            log_player_action("button_auto_cycle", selected=self.selected_button.value)

    def get_selected_action(self) -> EndGameAction:
        """Get currently selected action without cycling."""
        return self.selected_button

    def draw(self, window_width: int, window_height: int) -> None:
        """
        Draw the end game screen.

        Args:
            window_width: Width of the game window
            window_height: Height of the game window
        """
        center_x = window_width // 2
        center_y = window_height // 2

        # Draw semi-transparent overlay
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            window_width,
            window_height,
            (0, 0, 0, 180),  # Semi-transparent black (R, G, B, A)
        )

        # Draw game over title
        arcade.draw_text(
            self.messages.get_message("ui.game_over"),
            center_x,
            center_y + 140,
            arcade.color.RED,
            56,  # Larger title
            anchor_x="center",
            font_name="Arial",
        )

        # Draw final score with high score comparison
        high_score = get_high_score(self.game_name) if self.game_name else 0
        is_new_record = (
            is_new_high_score(self.game_name, self.final_score)
            if self.game_name
            else False
        )

        if is_new_record:
            score_text = f"Nowy rekord: {self.final_score}!"
            score_color = arcade.color.GOLD
        else:
            score_text = f"Wynik: {self.final_score} / Rekord: {high_score}"
            score_color = arcade.color.WHITE

        arcade.draw_text(
            score_text,
            center_x,
            center_y + 80,
            score_color,
            36,  # Larger score
            anchor_x="center",
            font_name="Arial",
        )

        # Draw instruction (more spacing from buttons)
        arcade.draw_text(
            self.messages.get_message("ui.click_to_select"),
            center_x,
            center_y + 20,  # More space above buttons
            arcade.color.LIGHT_GRAY,
            20,  # Larger, softer color
            anchor_x="center",
            font_name="Arial",
        )

        # Draw buttons (larger, more spaced out)
        button_y = center_y - 80  # Move buttons further down
        self._draw_button(
            self.messages.get_message("ui.play_again"),
            center_x - 150,
            button_y,
            280,
            70,  # Larger buttons
            self.selected_button == EndGameAction.PLAY_AGAIN,
        )

        self._draw_button(
            self.messages.get_message("ui.exit_game"),
            center_x + 150,
            button_y,
            280,
            70,  # Larger buttons
            self.selected_button == EndGameAction.EXIT,
        )

    def _draw_button(
        self,
        text: str,
        center_x: float,
        center_y: float,
        width: float,
        height: float,
        is_selected: bool,
    ) -> None:
        """
        Draw a rounded button with optional selection highlighting.

        Args:
            text: Button text
            center_x: Button center X coordinate
            center_y: Button center Y coordinate
            width: Button width
            height: Button height
            is_selected: Whether button is currently selected
        """
        # Button colors
        if is_selected:
            bg_color = (255, 215, 0)  # Gold for selected
            text_color = (0, 0, 0)  # Black text
        else:
            bg_color = (70, 70, 70)  # Dark gray for unselected
            text_color = (255, 255, 255)  # White text

        # Draw rounded rectangle (simulate with multiple rectangles and circles)
        corner_radius = 15
        left = center_x - width // 2
        bottom = center_y - height // 2
        right = center_x + width // 2
        top = center_y + height // 2

        # Main rectangle body
        arcade.draw_lbwh_rectangle_filled(
            left + corner_radius, bottom, width - 2 * corner_radius, height, bg_color
        )
        arcade.draw_lbwh_rectangle_filled(
            left, bottom + corner_radius, width, height - 2 * corner_radius, bg_color
        )

        # Corner circles
        arcade.draw_circle_filled(
            left + corner_radius, bottom + corner_radius, corner_radius, bg_color
        )
        arcade.draw_circle_filled(
            right - corner_radius, bottom + corner_radius, corner_radius, bg_color
        )
        arcade.draw_circle_filled(
            left + corner_radius, top - corner_radius, corner_radius, bg_color
        )
        arcade.draw_circle_filled(
            right - corner_radius, top - corner_radius, corner_radius, bg_color
        )

        # Button text (larger font)
        arcade.draw_text(
            text,
            center_x,
            center_y,
            text_color,
            24,  # Larger font
            anchor_x="center",
            anchor_y="center",
            font_name="Arial",  # Better font
        )


# Test runner for standalone execution
if __name__ == "__main__":
    import arcade

    from unipress.core.logger import init_logger
    from unipress.core.messages import load_messages

    class EndGameScreenTest(arcade.Window):
        """Test window for end game screen component."""

        def __init__(self):
            super().__init__(800, 600, "End Game Screen Test")
            init_logger()
            self.messages = load_messages("pl_PL", "demo_jump")
            self.end_game_screen = EndGameScreen(self.messages, final_score=12345)
            arcade.set_background_color(arcade.color.DARK_BLUE)
            print(
                "Buttons auto-cycle every 2s, click to execute selected action, "
                "ESC to exit"
            )

        def on_update(self, delta_time):
            self.end_game_screen.update(delta_time)

        def on_draw(self):
            self.clear()
            arcade.draw_text(
                "TEST BACKGROUND",
                self.width // 2,
                self.height // 2 + 200,
                arcade.color.GRAY,
                24,
                anchor_x="center",
            )
            self.end_game_screen.draw(self.width, self.height)

        def on_mouse_press(self, x, y, button, modifiers):
            if button == arcade.MOUSE_BUTTON_LEFT:
                action = self.end_game_screen.get_selected_action()
                print(f"Executed action: {action.value}")
                if action == EndGameAction.EXIT:
                    self.close()

        def on_key_press(self, key, modifiers):
            if key == arcade.key.ESCAPE:
                self.close()

    print("End Game Screen Test - Click to cycle, ESC to exit")
    EndGameScreenTest().run()
