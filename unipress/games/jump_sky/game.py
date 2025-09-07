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
import math
import random

import arcade

from unipress.core.base_game import BaseGame
from unipress.core.logger import log_game_event, log_player_action
from unipress.core.settings import get_setting


class Fruit:
    """Collectible fruit with type-specific properties and fallback visuals."""
    
    def __init__(self, x: float, y: float, fruit_type: str, velocity: float, points: int):
        """Initialize fruit with position and type-specific properties."""
        self.x = x
        self.y = y
        self.fruit_type = fruit_type  # "apple", "banana", "pineapple", "orange"
        self.velocity = velocity      # Movement speed (pixels per second)
        self.points = points          # Score value when collected
        self.size = 16               # Visual size for fallback shapes
        self.collected = False       # Flag to mark for removal
        
    def update(self, delta_time: float) -> None:
        """Update fruit position (moves left)."""
        self.x -= self.velocity * delta_time
        
    def is_off_screen(self) -> bool:
        """Check if fruit has moved off the left side of screen."""
        return self.x < -self.size * 2  # Extra margin for cleanup
        
    def get_collision_rect(self) -> dict:
        """Get collision rectangle for collision detection."""
        return {
            "x": self.x - self.size,
            "y": self.y - self.size,
            "width": self.size * 2,
            "height": self.size * 2
        }
        
    def draw(self, draw_fallback_fruit_func) -> None:
        """Draw fruit using fallback system."""
        if not self.collected:
            draw_fallback_fruit_func(self.x, self.y, self.fruit_type, self.size)


class Bird:
    """Dangerous bird with type-specific properties and fallback visuals."""
    
    def __init__(self, x: float, y: float, bird_type: str, velocity: float):
        """Initialize bird with position and type-specific properties."""
        self.x = x
        self.y = y
        self.bird_type = bird_type    # "bird1", "bird2", "bird3"
        self.velocity = velocity      # Movement speed (pixels per second)
        self.size = 20               # Visual size for fallback shapes
        self.animation_frame = 0.0   # Animation timer for wing flapping
        self.removed = False         # Flag to mark for removal
        
    def update(self, delta_time: float) -> None:
        """Update bird position and animation (moves left with wing flap)."""
        self.x -= self.velocity * delta_time
        self.animation_frame += delta_time * 4  # 4 Hz animation speed
        
    def is_off_screen(self) -> bool:
        """Check if bird has moved off the left side of screen."""
        return self.x < -self.size * 2  # Extra margin for cleanup
        
    def get_collision_rect(self) -> dict:
        """Get collision rectangle for collision detection."""
        return {
            "x": self.x - self.size,
            "y": self.y - self.size,
            "width": self.size * 2,
            "height": self.size * 2
        }
        
    def get_animation_frame(self) -> float:
        """Get normalized animation frame for wing flapping (sine wave)."""
        return math.sin(self.animation_frame)
        
    def draw(self, draw_fallback_bird_func) -> None:
        """Draw bird using fallback system with animation."""
        if not self.removed:
            animation_frame = self.get_animation_frame()
            draw_fallback_bird_func(self.x, self.y, self.bird_type, animation_frame, self.size)


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
        self.fruits: List[Fruit] = []
        self.birds: List[Bird] = []
        
        # Load fruit configuration from settings
        self.fruit_points = get_setting(self.settings, "jump_sky.fruit_points", {
            "apple": 10, "banana": 15, "pineapple": 20, "orange": 25
        })
        self.fruit_velocity_multipliers = get_setting(self.settings, "jump_sky.fruit_velocity_multiplier", {
            "apple": 1.0, "banana": 1.3, "pineapple": 1.6, "orange": 2.0
        })
        self.base_object_speed = get_setting(self.settings, "jump_sky.object_speed_base", 200)
        
        # Load bird configuration from settings
        self.bird_types = get_setting(self.settings, "jump_sky.bird_types", ["bird1", "bird2", "bird3"])
        self.bird_velocity_range = get_setting(self.settings, "jump_sky.bird_velocity_random_range", [0.8, 1.8])
        
        # Animation timing for fallback birds and player
        self.bird_animation_timer = 0.0
        self.player_animation_timer = 0.0
        
        # Test spawning timer (temporary)
        self.test_spawn_timer = 0.0
        self.test_spawn_interval = 2.0  # Spawn every 2 seconds for testing
        
        log_game_event("jump_sky_game_initialized", 
                      difficulty=self.difficulty,
                      jump_velocity=self.jump_velocity,
                      desired_jump_height=desired_jump_height)

    def create_fruit(self, fruit_type: str, x: float, y: float) -> Fruit:
        """Create a fruit with type-specific properties."""
        points = self.fruit_points.get(fruit_type, 10)
        velocity_multiplier = self.fruit_velocity_multipliers.get(fruit_type, 1.0)
        
        # Scale base speed with difficulty and fruit type
        difficulty_speed_multiplier = 1.0 + (self.difficulty - 1) * 0.1  # 1.0x to 1.9x
        final_velocity = self.base_object_speed * velocity_multiplier * difficulty_speed_multiplier
        
        return Fruit(x, y, fruit_type, final_velocity, points)
        
    def create_bird(self, bird_type: str, x: float, y: float) -> Bird:
        """Create a bird with randomized velocity."""
        # Random velocity multiplier between 0.8x and 1.8x
        velocity_multiplier = random.uniform(self.bird_velocity_range[0], self.bird_velocity_range[1])
        
        # Scale base speed with difficulty and random multiplier
        difficulty_speed_multiplier = 1.0 + (self.difficulty - 1) * 0.1  # 1.0x to 1.9x
        final_velocity = self.base_object_speed * velocity_multiplier * difficulty_speed_multiplier
        
        return Bird(x, y, bird_type, final_velocity)
        
    def reset_game(self) -> None:
        """Reset game to initial state."""
        self.fruits.clear()
        self.birds.clear()
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
                angle_rad = math.radians(angle)
                end_x = x + (size - 4) * math.cos(angle_rad)
                end_y = y + (size - 4) * math.sin(angle_rad)
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
            cos_angle = math.cos(math.radians(rotation_angle))
            sin_angle = math.sin(math.radians(rotation_angle))
            
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

    def draw_fallback_player(self, x: float, y: float, is_jumping: bool = False, animation_timer: float = 0.0) -> None:
        """Draw fallback player with simple leg animation when assets are missing."""
        body_width = 32
        body_height = 32
        leg_height = 8
        leg_width = 6
        
        # Draw main body (blue rectangle)
        arcade.draw_lbwh_rectangle_filled(
            x - body_width//2, 
            y - body_height//2, 
            body_width, 
            body_height, 
            arcade.color.BLUE
        )
        
        # Draw body outline
        arcade.draw_lbwh_rectangle_outline(
            x - body_width//2, 
            y - body_height//2, 
            body_width, 
            body_height, 
            arcade.color.DARK_BLUE,
            2
        )
        
        if is_jumping:
            # Jumping: legs together (static)
            leg_x = x - leg_width//2
            leg_y = y - body_height//2 - leg_height
            
            arcade.draw_lbwh_rectangle_filled(
                leg_x, leg_y, leg_width, leg_height, arcade.color.WHITE
            )
            arcade.draw_lbwh_rectangle_outline(
                leg_x, leg_y, leg_width, leg_height, arcade.color.DARK_BLUE, 1
            )
        else:
            # Running: alternating legs animation
            leg_offset = math.sin(animation_timer * 8) * 4  # 8 Hz leg movement, 4px amplitude
            
            # Left leg
            left_leg_x = x - leg_width - 2
            left_leg_y = y - body_height//2 - leg_height + leg_offset
            arcade.draw_lbwh_rectangle_filled(
                left_leg_x, left_leg_y, leg_width, leg_height, arcade.color.WHITE
            )
            arcade.draw_lbwh_rectangle_outline(
                left_leg_x, left_leg_y, leg_width, leg_height, arcade.color.DARK_BLUE, 1
            )
            
            # Right leg (opposite phase)
            right_leg_x = x + 2
            right_leg_y = y - body_height//2 - leg_height - leg_offset
            arcade.draw_lbwh_rectangle_filled(
                right_leg_x, right_leg_y, leg_width, leg_height, arcade.color.WHITE
            )
            arcade.draw_lbwh_rectangle_outline(
                right_leg_x, right_leg_y, leg_width, leg_height, arcade.color.DARK_BLUE, 1
            )


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
        self.update_fruits(delta_time)
        self.update_birds(delta_time)
        
        # Update animation timers
        self.bird_animation_timer += delta_time
        self.player_animation_timer += delta_time
        
        # Test spawning (temporary)
        self.test_spawn_timer += delta_time
        if self.test_spawn_timer >= self.test_spawn_interval:
            self.spawn_test_objects()
            self.test_spawn_timer = 0.0

    def update_fruits(self, delta_time: float) -> None:
        """Update all fruits (movement and cleanup)."""
        for fruit in self.fruits[:]:  # Copy list to avoid modification during iteration
            fruit.update(delta_time)
            
            # Remove off-screen fruits
            if fruit.is_off_screen() or fruit.collected:
                self.fruits.remove(fruit)

    def update_birds(self, delta_time: float) -> None:
        """Update all birds (movement, animation, and cleanup)."""
        for bird in self.birds[:]:  # Copy list to avoid modification during iteration
            bird.update(delta_time)
            
            # Remove off-screen birds
            if bird.is_off_screen() or bird.removed:
                self.birds.remove(bird)

    def spawn_test_objects(self) -> None:
        """Spawn random test objects (fruits and birds) for testing (temporary)."""
        total_objects = len(self.fruits) + len(self.birds)
        
        if total_objects < 3:  # Keep max 3 objects for testing
            # 75% chance for fruit, 25% chance for bird (approximate 1:4 ratio)
            spawn_fruit = random.random() < 0.75
            
            # Height range for all objects
            height_min = get_setting(self.settings, "jump_sky.height_min", 60)
            height_max = get_setting(self.settings, "jump_sky.height_max", 150)
            spawn_y = self.ground_y + random.uniform(height_min, height_max)
            
            if spawn_fruit:
                fruit_types = ["apple", "banana", "pineapple", "orange"]
                fruit_type = random.choice(fruit_types)
                fruit = self.create_fruit(fruit_type, self.width + 50, spawn_y)
                self.fruits.append(fruit)
                
                log_game_event("test_fruit_spawned", fruit_type=fruit_type, 
                              velocity=fruit.velocity, points=fruit.points)
            else:
                bird_type = random.choice(self.bird_types)
                bird = self.create_bird(bird_type, self.width + 50, spawn_y)
                self.birds.append(bird)
                
                log_game_event("test_bird_spawned", bird_type=bird_type, 
                              velocity=bird.velocity)

    def on_draw(self) -> None:
        """Draw the game."""
        self.clear()
        
        # Draw simple background (adequate for emergency fallback)
        arcade.draw_lbwh_rectangle_filled(0, 0, self.width, self.height, arcade.color.SKY_BLUE)
        arcade.draw_lbwh_rectangle_filled(0, 0, self.width, self.ground_y, arcade.color.FOREST_GREEN)
        
        # Draw player with fallback animation
        if self.should_draw_player():
            self.draw_fallback_player(
                self.player_x, 
                self.player_y, 
                self.is_jumping, 
                self.player_animation_timer
            )
        
        # Draw active fruits
        for fruit in self.fruits:
            fruit.draw(self.draw_fallback_fruit)
            
        # Draw active birds (higher Z-order than fruits)
        for bird in self.birds:
            bird.draw(self.draw_fallback_bird)
        
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
            animation_frame = math.sin(self.bird_animation_timer * 4)  # 4 Hz flapping
            
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