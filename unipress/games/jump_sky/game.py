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
        
        # Animation timing for fallback birds
        self.bird_animation_timer = 0.0
        
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

    def draw_fallback_fruit(self, x: float, y: float, fruit_type: str, size: float = 16) -> None:
        """Draw fallback fruit shapes when assets are missing."""
        if fruit_type == "apple":
            # Green circle with red border
            arcade.draw_circle_filled(x, y, size, arcade.color.GREEN)
            arcade.draw_circle_outline(x, y, size, arcade.color.RED, 3)
        elif fruit_type == "banana":
            # Yellow crescent shape
            # Draw as overlapping circles to create crescent
            arcade.draw_circle_filled(x - 4, y, size - 2, arcade.color.YELLOW)
            arcade.draw_circle_filled(x + 6, y, size - 4, arcade.color.SKY_BLUE)  # "Cut out" part
        elif fruit_type == "pineapple":
            # Orange diamond/rhombus shape
            points = [
                (x, y + size),      # top
                (x + size, y),      # right
                (x, y - size),      # bottom
                (x - size, y)       # left
            ]
            arcade.draw_polygon_filled(points, arcade.color.ORANGE)
            arcade.draw_polygon_outline(points, arcade.color.DARK_ORANGE, 2)
        elif fruit_type == "orange":
            # Orange circle with texture lines
            arcade.draw_circle_filled(x, y, size, arcade.color.ORANGE)
            # Add texture lines
            for i in range(6):
                angle = i * 60  # 60 degrees apart
                end_x = x + (size - 4) * arcade.math.cos(arcade.math.radians(angle))
                end_y = y + (size - 4) * arcade.math.sin(arcade.math.radians(angle))
                arcade.draw_line(x, y, end_x, end_y, arcade.color.DARK_ORANGE, 2)

    def draw_fallback_bird(self, x: float, y: float, bird_type: str, animation_frame: float = 0.0, size: float = 20) -> None:
        """Draw fallback bird shapes with rotation animation when assets are missing."""
        # Calculate rotation angle based on animation frame (simple wing flap)
        rotation_angle = animation_frame * 30  # 30 degrees max rotation
        
        # Bird colors by type
        colors = {
            "bird1": arcade.color.RED,
            "bird2": arcade.color.BLUE,
            "bird3": arcade.color.PURPLE
        }
        color = colors.get(bird_type, arcade.color.GRAY)
        
        # Draw triangle pointing right (bird flying right to left)
        # Triangle points: right (nose), top-left (wing), bottom-left (tail)
        base_points = [
            (x + size, y),          # nose (right point)
            (x - size//2, y + size//2),  # top wing
            (x - size//2, y - size//2)   # bottom wing/tail
        ]
        
        # Apply rotation for wing flap animation
        if rotation_angle != 0:
            # Rotate points around center (x, y)
            cos_angle = arcade.math.cos(arcade.math.radians(rotation_angle))
            sin_angle = arcade.math.sin(arcade.math.radians(rotation_angle))
            
            rotated_points = []
            for px, py in base_points:
                # Translate to origin, rotate, translate back
                dx = px - x
                dy = py - y
                new_dx = dx * cos_angle - dy * sin_angle
                new_dy = dx * sin_angle + dy * cos_angle
                rotated_points.append((x + new_dx, y + new_dy))
            
            arcade.draw_polygon_filled(rotated_points, color)
            arcade.draw_polygon_outline(rotated_points, arcade.color.BLACK, 2)
        else:
            arcade.draw_polygon_filled(base_points, color)
            arcade.draw_polygon_outline(base_points, arcade.color.BLACK, 2)

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
        
        # Update bird animation timer
        self.bird_animation_timer += delta_time

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
        
        # Draw fallback fruit examples for testing (when game is started)
        if self.game_started:
            test_y = self.ground_y + 80
            spacing = 100
            start_x = 300
            
            fruits = ["apple", "banana", "pineapple", "orange"]
            for i, fruit in enumerate(fruits):
                x = start_x + (i * spacing)
                self.draw_fallback_fruit(x, test_y, fruit, 16)
                
                # Draw fruit name labels
                arcade.draw_text(
                    fruit.capitalize(),
                    x,
                    test_y - 30,
                    arcade.color.BLACK,
                    12,
                    anchor_x="center"
                )
            
            # Draw fallback bird examples for testing (above fruits)
            bird_test_y = test_y + 60
            bird_types = ["bird1", "bird2", "bird3"]
            
            # Calculate animation frame (sine wave for smooth flapping)
            animation_frame = arcade.math.sin(self.bird_animation_timer * 4)  # 4 Hz flapping
            
            for i, bird_type in enumerate(bird_types):
                x = start_x + (i * spacing) + 50  # Offset from fruits
                self.draw_fallback_bird(x, bird_test_y, bird_type, animation_frame, 20)
                
                # Draw bird type labels
                arcade.draw_text(
                    bird_type.capitalize(),
                    x,
                    bird_test_y - 35,
                    arcade.color.BLACK,
                    12,
                    anchor_x="center"
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