"""
Jump Sky Game - One-button fruit collection with bird avoidance.

A game where players jump to collect fruits for points while avoiding flying birds.
Features:
- 4 fruit types with different point values and velocities
- 3 bird types with random velocities
- Height-based collision system
- Fallback visual system for missing assets
- Professional sound integration
"""

from typing import List, Optional
import random

import arcade

from unipress.core.base_game import BaseGame
from unipress.core.logger import log_game_event, log_player_action
from unipress.core.settings import get_setting


class JumpSkyGame(BaseGame):
    """
    Jump Sky game with fruit collection and bird avoidance mechanics.
    
    Players jump to collect fruits (points) while avoiding birds (life loss).
    Birds only cause damage when player is jumping - strategic timing required.
    """

    def __init__(self, difficulty: int = None):
        """Initialize Jump Sky game."""
        super().__init__(
            game_name="jump_sky",
            title="Jump Sky - One-Button Fruit Collection",
            difficulty=difficulty
        )

        # Physics settings - adapted from jumper game
        self.gravity = get_setting(self.settings, "jump_sky.gravity", 800)
        
        # Calculate jump height to guarantee fruit/bird clearance
        object_height = 32  # Default object height
        base_jump_height = get_setting(self.settings, "jump_sky.height_max", 150) + 20  # 20px safety margin above max objects
        difficulty_bonus = (11 - self.difficulty) * 10  # Easier difficulties get higher jumps
        desired_jump_height = base_jump_height + difficulty_bonus
        
        # Convert jump height to initial velocity using physics formula (like jumper game)
        self.jump_velocity = (2 * self.gravity * desired_jump_height) ** 0.5
        
        # Player positioning and physics
        self.ground_y = int(self.height * 0.25)  # Ground at 25% of screen height
        self.player_x = 150
        self.player_y = self.ground_y
        self.player_y_velocity = 0
        self.is_jumping = False
        
        # Game objects
        self.game_objects: List = []
        
        log_game_event("jump_sky_game_initialized", 
                      difficulty=self.difficulty,
                      jump_velocity=self.jump_velocity,
                      desired_jump_height=desired_jump_height)

    def reset_game(self) -> None:
        """Reset game to initial state."""
        self.game_objects.clear()
        self.player_x = 150
        self.player_y = self.ground_y
        self.player_y_velocity = 0
        self.is_jumping = False
        log_game_event("jump_sky_game_reset")

    def on_action_press(self) -> None:
        """Handle jump action."""
        if self.is_game_paused():
            if self.handle_life_lost_continue():
                return
            if self.waiting_for_start_click and not self.waiting_for_sound:
                self.start_game()
                return
            if not self.game_started and not self.waiting_for_sound:
                self.start_game()
            return

        # Jump if on ground (adapted from jumper game)
        if not self.is_jumping:
            self.is_jumping = True
            self.player_y_velocity = self.jump_velocity
            
            # Play jump sound
            self.play_sound_event("jump")
                
            log_player_action("jump", 
                            x=self.player_x, 
                            y=self.player_y, 
                            y_velocity=self.player_y_velocity)

    def update_player(self, delta_time: float) -> None:
        """Update player physics and movement (adapted from jumper game)."""
        if self.is_jumping:
            # Apply gravity
            self.player_y_velocity -= self.gravity * delta_time
            self.player_y += self.player_y_velocity * delta_time

            # Check for landing
            if self.player_y <= self.ground_y:
                self.player_y = self.ground_y
                self.is_jumping = False
                self.player_y_velocity = 0

    def on_resize(self, width: int, height: int) -> None:
        """Handle window resize to maintain proper ground positioning."""
        super().on_resize(width, height)
        
        # Update ground position relative to new window height
        old_ground_y = self.ground_y
        self.ground_y = int(height * 0.25)
        
        # Update player position if not jumping
        if not self.is_jumping:
            self.player_y = self.ground_y
        
        log_game_event("window_resize", width=width, height=height, 
                      old_ground_y=old_ground_y, new_ground_y=self.ground_y)

    def on_update(self, delta_time: float) -> None:
        """Update game state."""
        if self.show_end_screen and self.end_game_screen:
            self.end_game_screen.update(delta_time)
            return

        if self.is_game_paused():
            self.update_sound_timer(delta_time)
            if not self.waiting_for_start_click and not self.waiting_for_sound:
                self.update_life_lost_effects(delta_time)
            return

        # Update periodic cursor positioning
        self.update_cursor_positioning(delta_time)
        
        # Update game physics and objects
        self.update_player(delta_time)

    def on_draw(self) -> None:
        """Draw the game."""
        self.clear()
        
        # Draw background
        arcade.draw_lbwh_rectangle_filled(0, 0, self.width, self.height, arcade.color.SKY_BLUE)
        arcade.draw_lbwh_rectangle_filled(0, 0, self.width, self.ground_y, arcade.color.FOREST_GREEN)
        
        # Draw player (blue rectangle) with physics-based positioning
        if self.should_draw_player():
            arcade.draw_lbwh_rectangle_filled(
                self.player_x - 16, 
                self.player_y - 16, 
                32, 
                32, 
                arcade.color.BLUE
            )
            
        # Draw instruction text
        if not self.game_started:
            instruction_text = self.get_message("ui.instructions")
            arcade.draw_text(
                instruction_text,
                self.width // 2,
                self.height // 2 + 50,
                arcade.color.BLACK,
                20,
                anchor_x="center"
            )
        
        self.draw_ui()


# Test runner for development
if __name__ == "__main__":
    import sys
    from unipress.core.logger import init_logger
    
    # Initialize logging for the game process
    init_logger("jump_sky")
    
    difficulty = 5
    if len(sys.argv) > 1:
        try:
            difficulty = int(sys.argv[1])
            difficulty = max(1, min(10, difficulty))
        except ValueError:
            print("Invalid difficulty. Using default (5).")
    
    print(f"Starting Jump Sky Game (Difficulty: {difficulty})")
    print("Controls: Left click to jump and collect fruits!")
    print("Features: Fruit collection, bird avoidance, fallback visuals")
    
    game = JumpSkyGame(difficulty=difficulty)
    game.run()