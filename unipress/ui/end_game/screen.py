"""
End Game Screen UI Component

Provides standardized end game screen with two cycling buttons:
- Play Again: Restart the current game
- Exit: Close the game

Buttons cycle on each click, selected button is highlighted.
"""

from enum import Enum
from typing import Callable

import arcade

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

    def __init__(self, messages: MessageLoader, final_score: int = 0):
        """
        Initialize end game screen.
        
        Args:
            messages: Message loader for localized text
            final_score: Player's final score to display
        """
        self.messages = messages
        self.final_score = final_score
        
        # Button state
        self.selected_button = EndGameAction.PLAY_AGAIN  # Default selection
        self.button_actions = [EndGameAction.PLAY_AGAIN, EndGameAction.EXIT]
        
        # Colors
        self.normal_color = arcade.color.LIGHT_GRAY
        self.selected_color = arcade.color.YELLOW
        self.text_color = arcade.color.BLACK
        
        log_game_event("end_game_screen_shown", final_score=final_score)

    def cycle_selection(self) -> EndGameAction:
        """
        Cycle to next button and return the currently selected action.
        
        Returns:
            Currently selected action after cycling
        """
        current_index = self.button_actions.index(self.selected_button)
        next_index = (current_index + 1) % len(self.button_actions)
        self.selected_button = self.button_actions[next_index]
        
        log_player_action("button_cycle", selected=self.selected_button.value)
        return self.selected_button

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
            0, 0, window_width, window_height, 
            (*arcade.color.BLACK, 180)  # Semi-transparent black
        )
        
        # Draw game over title
        arcade.draw_text(
            self.messages.get_message("ui.game_over"),
            center_x, center_y + 120,
            arcade.color.RED, 48,
            anchor_x="center"
        )
        
        # Draw final score
        arcade.draw_text(
            self.messages.get_message("ui.final_score", score=self.final_score),
            center_x, center_y + 60,
            arcade.color.WHITE, 32,
            anchor_x="center"
        )
        
        # Draw instruction
        arcade.draw_text(
            self.messages.get_message("ui.click_to_select"),
            center_x, center_y + 10,
            arcade.color.WHITE, 18,
            anchor_x="center"
        )
        
        # Draw buttons
        self._draw_button(
            self.messages.get_message("ui.play_again"),
            center_x - 120, center_y - 40,
            200, 50,
            self.selected_button == EndGameAction.PLAY_AGAIN
        )
        
        self._draw_button(
            self.messages.get_message("ui.exit_game"),
            center_x + 120, center_y - 40,
            200, 50,
            self.selected_button == EndGameAction.EXIT
        )
        
        # Draw selection indicator
        selected_text = (
            self.messages.get_message("ui.play_again") 
            if self.selected_button == EndGameAction.PLAY_AGAIN
            else self.messages.get_message("ui.exit_game")
        )
        arcade.draw_text(
            f"► {selected_text}",
            center_x, center_y - 80,
            self.selected_color, 24,
            anchor_x="center"
        )

    def _draw_button(self, text: str, center_x: float, center_y: float, 
                     width: float, height: float, is_selected: bool) -> None:
        """
        Draw a button with optional selection highlighting.
        
        Args:
            text: Button text
            center_x: Button center X coordinate
            center_y: Button center Y coordinate  
            width: Button width
            height: Button height
            is_selected: Whether button is currently selected
        """
        # Button background
        color = self.selected_color if is_selected else self.normal_color
        arcade.draw_lbwh_rectangle_filled(
            center_x - width // 2, 
            center_y - height // 2,
            width, height, 
            color
        )
        
        # Button border
        border_color = arcade.color.WHITE if is_selected else arcade.color.GRAY
        arcade.draw_lbwh_rectangle_outline(
            center_x - width // 2,
            center_y - height // 2, 
            width, height,
            border_color, 3
        )
        
        # Button text
        text_color = arcade.color.BLACK if is_selected else arcade.color.WHITE
        arcade.draw_text(
            text, center_x, center_y,
            text_color, 20,
            anchor_x="center", anchor_y="center"
        )