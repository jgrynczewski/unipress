"""
Jumper Game - Enhanced version of demo_jump with sprites, animations and sounds.

A one-button jumping game where the player (animated running character) must jump over
fire obstacles using sprite animations and sound effects with parallax scrolling background.
"""

from typing import List, Optional
import random

import arcade

from unipress.core.assets import Animation, get_sound, load_animation, preload_assets
from unipress.core.base_game import BaseGame
from unipress.core.logger import log_game_event, log_player_action
from unipress.core.sound import STANDARD_SOUND_EVENTS
from unipress.core.settings import get_setting


class BackgroundLayer:
    """Represents a single parallax background layer."""

    def __init__(self, texture: arcade.Texture, scroll_speed: float, z_order: int):
        """
        Initialize background layer.

        Args:
            texture: Background texture
            scroll_speed: Scrolling speed multiplier
            z_order: Drawing order (lower = back, higher = front)
        """
        self.texture = texture
        self.scroll_speed = scroll_speed
        self.z_order = z_order
        self.x_offset = 0.0

    def update(self, delta_time: float, base_speed: float) -> None:
        """Update layer scrolling position."""
        self.x_offset -= base_speed * self.scroll_speed * delta_time
        # Reset when we've scrolled one texture width
        if self.x_offset <= -self.texture.width:
            self.x_offset += self.texture.width

    def draw(self, window_width: int, window_height: int) -> None:
        """Draw the background layer with seamless tiling."""
        if not self.texture:
            return
            
        # Draw texture with tiling to fill the window
        texture_width = self.texture.width
        texture_height = self.texture.height
        
        # Calculate how many tiles we need horizontally
        tiles_needed = (window_width // texture_width) + 2  # +2 for smooth scrolling
        
        # Calculate scale to fit window height
        scale_y = window_height / texture_height
        scaled_width = texture_width * scale_y
        
        # Recalculate tiles needed based on scaled width
        tiles_needed = int((window_width / scaled_width)) + 2
        
        # Draw tiles from left to right
        for i in range(tiles_needed):
            x = i * scaled_width + (self.x_offset * scale_y)
            
            # Create sprite for this tile
            sprite = arcade.Sprite()
            sprite.texture = self.texture
            sprite.center_x = x + scaled_width // 2
            sprite.center_y = window_height // 2  # Center vertically
            sprite.scale = scale_y  # Scale to fit window height
            
            sprite_list = arcade.SpriteList()
            sprite_list.append(sprite)
            sprite_list.draw()


class AnimatedSprite:
    """Sprite with animation support."""

    def __init__(self, x: float, y: float, game_name: str):
        """
        Initialize animated sprite.

        Args:
            x: Initial X position
            y: Initial Y position
            game_name: Game name for asset loading
        """
        self.x = x
        self.y = y
        self.game_name = game_name
        self.current_animation: Optional[Animation] = None
        self.animation_queue: List[str] = []

    def set_animation(self, animation_name: str, force: bool = False) -> bool:
        """
        Set current animation.

        Args:
            animation_name: Name of animation to play
            force: Force change even if same animation is playing

        Returns:
            True if animation was changed
        """
        if not force and self.current_animation and self.current_animation.name == animation_name:
            return False

        animation = load_animation(animation_name, self.game_name)
        if animation:
            self.current_animation = animation
            return True
        return False

    def update(self, delta_time: float) -> None:
        """Update sprite animation."""
        if self.current_animation:
            frame_changed = self.current_animation.update(delta_time)
            
            # Check for animation completion and queue
            if self.current_animation.is_finished and self.current_animation.next_animation:
                self.set_animation(self.current_animation.next_animation)

    def draw(self) -> None:
        """Draw the sprite at current animation frame."""
        if self.current_animation:
            texture = self.current_animation.get_current_texture()
            # Create temporary sprite and draw using SpriteList
            sprite = arcade.Sprite()
            sprite.texture = texture
            sprite.center_x = self.x
            sprite.center_y = self.y
            # Scale up the sprite (2.5x larger)
            sprite.scale = 2.5
            
            sprite_list = arcade.SpriteList()
            sprite_list.append(sprite)
            sprite_list.draw()
        else:
            # Fallback: draw colored rectangle when no animation loaded
            arcade.draw_lbwh_rectangle_filled(self.x - 32, self.y - 32, 64, 64, arcade.color.BLUE)

    def get_hitbox(self) -> dict:
        """Get current hitbox for collision detection."""
        if self.current_animation:
            hitbox = self.current_animation.get_current_hitbox()
            return {
                "x": self.x - hitbox["width"] // 2 + hitbox["x"],
                "y": self.y - hitbox["height"] // 2 + hitbox["y"],
                "width": hitbox["width"],
                "height": hitbox["height"]
            }
        return {"x": self.x, "y": self.y, "width": 64, "height": 64}


class Obstacle:
    """Fire obstacle with animation."""

    def __init__(self, x: float, y: float, speed: float, game_name: str):
        """Initialize obstacle."""
        self.sprite = AnimatedSprite(x, y, game_name)
        self.sprite.set_animation("obstacles/fire/burning")
        self.speed = speed
        self.cleared = False
        
    def draw(self) -> None:
        """Draw the obstacle."""
        if self.sprite.current_animation:
            # Draw actual fire sprite animation
            texture = self.sprite.current_animation.get_current_texture()
            sprite = arcade.Sprite()
            sprite.texture = texture
            sprite.center_x = self.sprite.x
            sprite.center_y = self.sprite.y
            # Scale fire sprites larger for better visibility
            sprite.scale = 2.5
            
            sprite_list = arcade.SpriteList()
            sprite_list.append(sprite)
            sprite_list.draw()
        else:
            # Fallback: draw red rectangle for fire obstacle
            arcade.draw_lbwh_rectangle_filled(self.sprite.x - 32, self.sprite.y - 32, 64, 64, arcade.color.RED)

    def update(self, delta_time: float) -> None:
        """Update obstacle position and animation."""
        self.sprite.x -= self.speed * delta_time
        self.sprite.update(delta_time)

    def is_off_screen(self) -> bool:
        """Check if obstacle is off the left side of screen."""
        return self.sprite.x < -100

    def get_collision_rect(self) -> dict:
        """Get collision rectangle."""
        return self.sprite.get_hitbox()


class JumperGame(BaseGame):
    """
    Jumper game with sprite animations and sound effects.
    
    Enhanced version of demo_jump featuring:
    - Animated running player character
    - Animated fire obstacles
    - Parallax scrolling background
    - Sound effects for actions
    - Sprite-based graphics
    """

    def __init__(self, difficulty: int = None):
        """Initialize Jumper game."""
        super().__init__(
            game_name="jumper",
            title="Jumper - One-Button Jumping Game",
            difficulty=difficulty
        )

        # Game settings - using same calculation as demo_jump for consistent difficulty
        self.player_speed = get_setting(self.settings, "jumper.player_speed", 200)
        
        # Calculate jump height like demo_jump - guarantee obstacle clearance
        obstacle_height = 64  # Fire obstacle height 
        base_jump_height = obstacle_height + 100  # 100px safety margin above obstacle
        difficulty_bonus = (11 - self.difficulty) * 20  # More height on easier difficulties
        desired_jump_height = base_jump_height + difficulty_bonus
        
        self.gravity = get_setting(self.settings, "jumper.gravity", 800)
        
        # Convert jump height to initial velocity using physics formula (like demo_jump)
        self.jump_velocity = (2 * self.gravity * desired_jump_height) ** 0.5
        
        # Load background scroll speed first
        self.background_speed = get_setting(self.settings, "jumper.background_scroll_speed", 100)
        
        # Obstacle speed should match ground layer scroll speed for realistic physics
        ground_scroll_speed = self.background_speed * 1.0  # Ground layer has scroll_speed 1.0
        self.obstacle_speed = ground_scroll_speed
        
        # Calculate initial random spawn interval with safe minimum distance
        jump_duration = 2 * (2 * desired_jump_height / self.gravity) ** 0.5
        min_safe_interval = jump_duration * 1.44  # 44% safety margin (20% increase)  
        base_interval = max(min_safe_interval, 2.5)  # At least 2.5s base
        self.obstacle_spawn_interval = base_interval * random.uniform(0.8, 2.5)

        # Player sprite and physics
        self.ground_y = int(self.height * 0.25)  # Ground at 25% of screen height
        self.player = AnimatedSprite(150, self.ground_y, "jumper")
        self.player_y_velocity = 0
        self.is_jumping = False
        
        # Set initial animation so player is visible from start
        self.player.set_animation("player/running")

        # Game objects
        self.obstacles: List[Obstacle] = []
        self.background_layers: List[BackgroundLayer] = []
        
        # Load background layers
        self.load_background_layers()
        
        # Timing
        self.obstacle_timer = 0.0
        
        # Preload standard sound events
        self.sound_manager.preload_sounds(STANDARD_SOUND_EVENTS)

        # Preload assets
        asset_list = [
            "player/running_anim.json",
            "player/jumping_anim.json", 
            "obstacles/fire/burning_anim.json",
        ]
        preload_assets("jumper", asset_list)

        log_game_event("jumper_game_initialized", difficulty=self.difficulty)

    def load_background_layers(self) -> None:
        """Load background layers from JSON configuration."""
        import json
        import os
        
        try:
            # Load background configuration
            bg_path = os.path.join("unipress", "assets", "images", "games", "jumper", "backgrounds", "forest_background.json")
            if not os.path.exists(bg_path):
                log_game_event("background_config_not_found", path=bg_path)
                return
                
            with open(bg_path, 'r') as f:
                bg_config = json.load(f)
            
            # Load each layer
            for layer_config in bg_config.get("layers", []):
                texture_path = os.path.join("unipress", "assets", "images", "games", "jumper", "backgrounds", layer_config["file"])
                
                if os.path.exists(texture_path):
                    texture = arcade.load_texture(texture_path)
                    layer = BackgroundLayer(
                        texture=texture,
                        scroll_speed=layer_config["scroll_speed"],
                        z_order=layer_config["z_order"]
                    )
                    self.background_layers.append(layer)
                    log_game_event("background_layer_loaded", file=layer_config["file"])
                else:
                    log_game_event("background_layer_not_found", file=texture_path)
                    
        except Exception as e:
            from unipress.core.logger import log_error
            log_error(e, "Failed to load background layers")

    def reset_game(self) -> None:
        """Reset game to initial state."""
        self.obstacles.clear()
        self.player.x = 150
        self.player.y = self.ground_y
        self.player_y_velocity = 0
        self.is_jumping = False
        self.obstacle_timer = 0.0
        
        # Set initial player animation
        self.player.set_animation("player/running")
        
        log_game_event("jumper_game_reset")
    
    def reset_animations(self) -> None:
        """Reset all animations to prevent accumulated time during startup sound."""
        # Reset player animation by setting it fresh
        self.player.set_animation("player/running", force=True)
        
        # Reset all obstacle animations
        for obstacle in self.obstacles:
            obstacle.sprite.set_animation("obstacles/fire/burning", force=True)

    def on_resize(self, width: int, height: int) -> None:
        """Handle window resize to maintain proper ground positioning."""
        super().on_resize(width, height)
        
        # Update ground position relative to new window height
        old_ground_y = self.ground_y
        self.ground_y = int(height * 0.25)
        
        # Update player position if not jumping
        if not self.is_jumping:
            self.player.y = self.ground_y
        
        # Update all existing obstacles positions
        for obstacle in self.obstacles:
            obstacle.sprite.y = self.ground_y - 30
        
        log_game_event("window_resize", width=width, height=height, 
                      old_ground_y=old_ground_y, new_ground_y=self.ground_y)

    def on_action_press(self) -> None:
        """Handle jump action."""
        if self.is_game_paused():
            if self.handle_life_lost_continue():
                return
            # Only allow start_game() if not already waiting for sound completion
            if self.waiting_for_start_click and not self.waiting_for_sound:
                self.start_game()
                return
            if not self.game_started and not self.waiting_for_sound:
                self.start_game()
            return

        # Jump if on ground
        if not self.is_jumping:
            self.is_jumping = True
            self.player_y_velocity = self.jump_velocity
            self.player.set_animation("player/jumping")
            
            # Play jump sound
            self.play_sound_event("jump")
                
            log_player_action("jump", y_velocity=self.player_y_velocity)

    def update_player(self, delta_time: float) -> None:
        """Update player physics and animation."""
        if self.is_jumping:
            # Apply gravity
            self.player_y_velocity -= self.gravity * delta_time
            self.player.y += self.player_y_velocity * delta_time

            # Check for landing
            if self.player.y <= self.ground_y:
                self.player.y = self.ground_y
                self.is_jumping = False
                self.player_y_velocity = 0
                self.player.set_animation("player/running")

        # Update player animation
        self.player.update(delta_time)

    def spawn_obstacle(self) -> None:
        """Spawn a new fire obstacle."""
        obstacle_x = self.width + 50
        obstacle_y = self.ground_y - 30  # Position obstacles on ground level
        obstacle = Obstacle(obstacle_x, obstacle_y, self.obstacle_speed, "jumper")
        self.obstacles.append(obstacle)
        log_game_event("obstacle_spawned", x=obstacle_x)

    def update_obstacles(self, delta_time: float) -> None:
        """Update all obstacles."""
        # Update existing obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(delta_time)
            
            # Remove off-screen obstacles
            if obstacle.is_off_screen():
                if not obstacle.cleared:
                    self.score += 10
                    obstacle.cleared = True
                    self.play_sound_event("success")
                    
                    # Check if new high score was achieved
                    self.check_and_play_high_score_sound(self.score)
                    
                    log_game_event("obstacle_cleared", score=self.score)
                self.obstacles.remove(obstacle)

        # Spawn new obstacles with random intervals
        self.obstacle_timer += delta_time
        if self.obstacle_timer >= self.obstacle_spawn_interval:
            self.spawn_obstacle()
            self.obstacle_timer = 0.0
            
            # Calculate new random spawn interval with safe minimum distance
            # Base interval ensures minimum time for double jumps
            jump_duration = 2 * (2 * (64 + 100 + (11 - self.difficulty) * 20) / self.gravity) ** 0.5
            min_safe_interval = jump_duration * 1.44  # 44% safety margin (20% increase)
            base_interval = max(min_safe_interval, 2.5)  # At least 2.5s base
            
            # Add randomness: 0.8x to 2.5x variation
            self.obstacle_spawn_interval = base_interval * random.uniform(0.8, 2.5)

    def check_collisions(self) -> None:
        """Check for player-obstacle collisions."""
        player_rect = self.player.get_hitbox()
        
        for obstacle in self.obstacles:
            if obstacle.cleared:
                continue
                
            obstacle_rect = obstacle.get_collision_rect()
            
            # Simple AABB collision detection
            if (player_rect["x"] < obstacle_rect["x"] + obstacle_rect["width"] and
                player_rect["x"] + player_rect["width"] > obstacle_rect["x"] and
                player_rect["y"] < obstacle_rect["y"] + obstacle_rect["height"] and
                player_rect["y"] + player_rect["height"] > obstacle_rect["y"]):
                
                # Collision detected
                self.play_sound_event("failure")
                    
                log_game_event("obstacle_collision", score=self.score)
                self.lose_life()
                return

    def update_background(self, delta_time: float) -> None:
        """Update parallax background layers."""
        for layer in self.background_layers:
            layer.update(delta_time, self.background_speed)

    def on_update(self, delta_time: float) -> None:
        """Update game state."""
        if self.show_end_screen and self.end_game_screen:
            self.end_game_screen.update(delta_time)
            return

        if self.is_game_paused():
            # Update sound timer for non-blocking sound completion
            self.update_sound_timer(delta_time)
            
            # Only update life lost effects, don't update animations during waiting for start
            if not self.waiting_for_start_click and not self.waiting_for_sound:
                self.update_life_lost_effects(delta_time)
            return

        self.update_player(delta_time)
        self.update_obstacles(delta_time)
        self.update_background(delta_time)
        self.check_collisions()

    def draw_background(self) -> None:
        """Draw parallax background layers."""
        if self.background_layers:
            # Sort by z_order and draw back to front
            sorted_layers = sorted(self.background_layers, key=lambda l: l.z_order)
            for layer in sorted_layers:
                layer.draw(self.width, self.height)
        else:
            # Fallback: simple gradient background
            arcade.draw_lbwh_rectangle_filled(0, 0, self.width, self.height, arcade.color.SKY_BLUE)
            arcade.draw_lbwh_rectangle_filled(0, 0, self.width, self.ground_y, arcade.color.FOREST_GREEN)

    def draw_game_objects(self) -> None:
        """Draw all game objects."""
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw()

        # Draw player (with blinking effect during life lost)
        if self.should_draw_player():
            self.player.draw()

    def draw_jump_window(self) -> None:
        """Draw jump window indicator like in demo_jump."""
        if not self.game_started or self.game_over:
            return
            
        # Calculate jump duration using same physics as game
        gravity = self.gravity
        obstacle_height = 64
        base_jump_height = obstacle_height + 100
        difficulty_bonus = (11 - self.difficulty) * 20
        jump_height = base_jump_height + difficulty_bonus
        
        # Total jump time = 2 * sqrt(2 * jump_height / gravity)
        jump_duration = 2 * (2 * jump_height / gravity) ** 0.5
        
        # Distance an obstacle travels during jump
        jump_window_distance = self.obstacle_speed * jump_duration
        
        # Draw the jump window as a green zone on screen
        player_size = 64  # Scaled sprite size
        jump_zone_start = self.player.x + player_size // 2
        jump_zone_width = min(jump_window_distance, 200)  # Cap at 200px for display
        
        arcade.draw_lbwh_rectangle_filled(
            jump_zone_start, 45, jump_zone_width, 10, arcade.color.GREEN
        )
        
        # Draw info text centered under jump window
        info_text = f"{jump_window_distance:.0f}px ({jump_duration:.2f}s)"
        text_x = jump_zone_start + jump_zone_width // 2  # Center under jump window
        arcade.draw_text(
            info_text,
            text_x,
            30,  # Position below green indicator
            arcade.color.WHITE,
            12,
            anchor_x="center"  # Center the text horizontally
        )

    def on_draw(self) -> None:
        """Draw the game."""
        self.clear()
        
        self.draw_background()
        self.draw_game_objects()
        self.draw_jump_window()
        self.draw_ui()


# Test runner for development
if __name__ == "__main__":
    import sys
    
    difficulty = 5
    if len(sys.argv) > 1:
        try:
            difficulty = int(sys.argv[1])
            difficulty = max(1, min(10, difficulty))
        except ValueError:
            print("Invalid difficulty. Using default (5).")
    
    print(f"Starting Jumper Game (Difficulty: {difficulty})")
    print("Controls: Left click to jump over fire obstacles!")
    print("Features: Animated sprites, parallax backgrounds, sound effects")
    
    game = JumperGame(difficulty=difficulty)
    game.run()