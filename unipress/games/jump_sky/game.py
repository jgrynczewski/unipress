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
import os
import random

import arcade

from unipress.core.base_game import BaseGame
from unipress.core.logger import log_game_event, log_player_action
from unipress.core.settings import get_setting
from unipress.core.assets import get_asset_manager, Animation, load_animation


class AnimatedSprite:
    """Sprite with animation support - reused from jumper game."""

    def __init__(self, x: float, y: float, game_name: str):
        """Initialize animated sprite."""
        self.x = x
        self.y = y
        self.game_name = game_name
        self.current_animation: Optional[Animation] = None
        self.animation_queue: List[str] = []
        # Create reusable sprite list to prevent memory leaks
        self.sprite_list = arcade.SpriteList()

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
            # Clear existing sprites and reuse sprite list
            self.sprite_list.clear()
            
            texture = self.current_animation.get_current_texture()
            # Create sprite and add to reusable sprite list
            sprite = arcade.Sprite()
            sprite.texture = texture
            sprite.center_x = self.x
            sprite.center_y = self.y
            # Scale up the sprite (1.5x for jump_sky - smaller than jumper game)
            sprite.scale = 1.5
            
            self.sprite_list.append(sprite)
            self.sprite_list.draw()
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


class Fruit:
    """Collectible fruit with type-specific properties and sprite visuals."""
    
    def __init__(self, x: float, y: float, fruit_type: str, velocity: float, points: int):
        """Initialize fruit with position and type-specific properties."""
        self.x = x
        self.y = y
        self.fruit_type = fruit_type  # "apple", "banana", "cherry", "orange"
        self.velocity = velocity      # Movement speed (pixels per second)
        self.points = points          # Score value when collected
        self.size = 16               # Visual size for fallback shapes
        self.collected = False       # Flag to mark for removal
        
        # Sprite system for fruit images
        self.texture: Optional[arcade.Texture] = None
        # Scale: cherry is bigger to match other fruits, others scaled down to 32 pixels (64x64 → 32x32)
        self.sprite_scale = 0.7 if fruit_type == "cherry" else 0.5  
        self._load_texture()
        
    def _load_texture(self) -> None:
        """Load fruit texture if available, fallback to geometric shapes."""
        try:
            asset_manager = get_asset_manager()
            texture_path = f"fruits/{self.fruit_type}.png"
            self.texture = asset_manager.get_texture(texture_path, "jump_sky")
            
            if self.texture:
                log_game_event("fruit_sprite_loaded", fruit_type=self.fruit_type, 
                             texture_size=f"{self.texture.width}x{self.texture.height}")
            else:
                log_game_event("fruit_sprite_fallback", fruit_type=self.fruit_type, reason="texture_not_found")
                
        except Exception as e:
            log_game_event("fruit_sprite_error", fruit_type=self.fruit_type, error=str(e))
            self.texture = None
        
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
        """Draw fruit using sprite texture or fallback system."""
        if not self.collected:
            if self.texture:
                # Draw sprite texture with proper scaling
                scaled_width = self.texture.width * self.sprite_scale
                scaled_height = self.texture.height * self.sprite_scale
                
                # Create rect with center position (XYWH uses center anchor by default)
                rect = arcade.types.rect.XYWH(self.x, self.y, scaled_width, scaled_height)
                
                # Draw the texture using correct arcade method
                arcade.draw_texture_rect(self.texture, rect, alpha=255)
            else:
                # Use fallback system for missing sprites
                draw_fallback_fruit_func(self.x, self.y, self.fruit_type, self.size)


class Bird:
    """Dangerous bird with type-specific properties and sprite animations."""
    
    def __init__(self, x: float, y: float, bird_type: str, velocity: float):
        """Initialize bird with position and type-specific properties."""
        self.x = x
        self.y = y
        self.bird_type = bird_type    # "bird1", "bird2", "bird3"
        self.velocity = velocity      # Movement speed (pixels per second)
        self.size = 20               # Visual size for fallback shapes
        self.animation_frame = 0.0   # Animation timer for wing flapping
        self.removed = False         # Flag to mark for removal
        
        # Sprite animation system
        self.animation: Optional[Animation] = None
        self.sprite_scale = 2.0      # 2x scaling like other game sprites
        self._load_animation()
        
    def update(self, delta_time: float) -> None:
        """Update bird position and animation (moves left with wing flap)."""
        self.x -= self.velocity * delta_time
        self.animation_frame += delta_time * 4  # 4 Hz animation speed for fallback
        
        # Update sprite animation if available
        if self.animation:
            self.animation.update(delta_time)
        
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
        
    def _load_animation(self) -> None:
        """Load bird animation if available, fallback to geometric shapes."""
        if self.bird_type in ["bird1", "bird2", "bird3"]:
            # Try to load sprite animation for all bird types
            try:
                asset_manager = get_asset_manager()
                self.animation = asset_manager.load_animation(self.bird_type, "jump_sky")
                
                if self.animation:
                    log_game_event("bird_sprite_loaded", bird_type=self.bird_type, 
                                 frames=len(self.animation.frames))
                    print(f"DEBUG: Successfully loaded {self.bird_type} animation with {len(self.animation.frames)} frames")
                else:
                    log_game_event("bird_sprite_fallback", bird_type=self.bird_type, reason="animation_none")
                    print(f"DEBUG: Failed to load {self.bird_type} animation - returned None")
            except Exception as e:
                log_game_event("bird_sprite_error", bird_type=self.bird_type, error=str(e))
                print(f"DEBUG: Exception loading {self.bird_type} animation: {e}")
                self.animation = None
    
    def draw(self, draw_fallback_bird_func) -> None:
        """Draw bird using sprite animation or fallback system."""
        if not self.removed:
            if self.animation and self.bird_type in ["bird1", "bird2", "bird3"]:
                # Draw sprite animation for all bird types using arcade's draw_texture_rect
                texture = self.animation.get_current_texture()
                
                # Calculate scaled dimensions
                scaled_width = texture.width * self.sprite_scale
                scaled_height = texture.height * self.sprite_scale
                
                # Create rect with center position (XYWH uses center anchor by default)
                rect = arcade.types.rect.XYWH(self.x, self.y, scaled_width, scaled_height)
                
                # Draw the texture using correct arcade method
                arcade.draw_texture_rect(texture, rect, alpha=255)
            else:
                # Use fallback system for missing sprites
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
        self.ground_y = int(self.height * 0.25) - 30  # Ground lowered by ~30px (half player sprite height)
        self.player_x = 150
        self.player_y = self.ground_y
        self.player_y_velocity = 0
        self.is_jumping = False
        
        # UI feedback system
        self.score_display_timer = 0.0
        self.last_score_change = 0
        self.score_popup_text = ""
        self.score_popup_timer = 0.0
        self.jump_indicator_timer = 0.0
        
        # Game objects
        self.fruits: List[Fruit] = []
        self.birds: List[Bird] = []
        self.background_layers: List = []
        
        # Player sprite system (reused from jumper game)
        self.player_sprite = AnimatedSprite(self.player_x, self.player_y, "jump_sky")
        self.player_sprite.set_animation("player/running")  # Set initial animation
        
        # Background system with scroll speed
        self.background_speed = get_setting(self.settings, "jump_sky.background_scroll_speed", 50)
        self.load_background_layers()
        
        # Load fruit configuration from settings
        self.fruit_points = get_setting(self.settings, "jump_sky.fruit_points", {
            "apple": 10, "banana": 15, "cherry": 20, "orange": 25
        })
        self.fruit_velocity_multipliers = get_setting(self.settings, "jump_sky.fruit_velocity_multiplier", {
            "apple": 1.0, "banana": 1.3, "cherry": 1.6, "orange": 2.0
        })
        self.base_object_speed = get_setting(self.settings, "jump_sky.object_speed_base", 200)
        
        # Load bird configuration from settings
        self.bird_types = get_setting(self.settings, "jump_sky.bird_types", ["bird1", "bird2", "bird3"])
        self.bird_velocity_range = get_setting(self.settings, "jump_sky.bird_velocity_random_range", [0.8, 1.8])
        
        # Animation timing for fallback birds and player
        self.bird_animation_timer = 0.0
        self.player_animation_timer = 0.0
        
        # Spawn system with difficulty scaling
        self.spawn_timer = 0.0
        base_spawn_interval = get_setting(self.settings, "jump_sky.fruit_spawn_interval", 3.0)
        # Scale spawn rate with difficulty: easier = longer intervals (slower), harder = shorter intervals (faster)
        difficulty_spawn_multiplier = 1.2 - (self.difficulty - 1) * 0.02  # 1.2x (easy) to 1.02x (hard)
        self.spawn_interval = base_spawn_interval * difficulty_spawn_multiplier
        
        # Bird-to-fruit ratio scales with difficulty: easier = fewer birds, harder = more birds  
        base_bird_ratio = get_setting(self.settings, "jump_sky.bird_to_fruit_ratio", 0.25)
        difficulty_bird_multiplier = 0.5 + (self.difficulty - 1) * 0.06  # 0.5x (easy) to 1.04x (hard)
        self.bird_to_fruit_ratio = base_bird_ratio * difficulty_bird_multiplier
        
        # Max objects increases with difficulty for more challenge
        base_max_objects = get_setting(self.settings, "jump_sky.max_objects", 4)
        difficulty_objects_bonus = (self.difficulty - 1) // 3  # +1 every 3 difficulty levels
        self.max_objects = base_max_objects + difficulty_objects_bonus
        
        # Spawn tracking for ratio maintenance
        self.fruits_spawned = 0
        self.birds_spawned = 0
        
        # Safe zone system with difficulty scaling
        self.safe_zone_active = False
        self.safe_zone_timer = 0.0
        # Easier difficulties get longer safe zones, harder get shorter
        base_safe_duration = 15.0
        difficulty_safe_multiplier = 1.5 - (self.difficulty - 1) * 0.05  # 1.5x (easy) to 1.05x (hard)
        self.safe_zone_duration = base_safe_duration * difficulty_safe_multiplier
        
        # Safe zone cooldown: easier = more frequent, harder = less frequent
        base_safe_cooldown = 30.0
        difficulty_cooldown_multiplier = 0.8 + (self.difficulty - 1) * 0.04  # 0.8x (easy) to 1.16x (hard)
        self.safe_zone_cooldown = base_safe_cooldown * difficulty_cooldown_multiplier
        self.time_since_last_safe_zone = 0.0
        
        log_game_event("jump_sky_game_initialized", 
                      difficulty=self.difficulty,
                      jump_velocity=self.jump_velocity,
                      desired_jump_height=desired_jump_height,
                      spawn_interval=self.spawn_interval,
                      bird_ratio=self.bird_to_fruit_ratio,
                      max_objects=self.max_objects,
                      safe_zone_duration=self.safe_zone_duration,
                      safe_zone_cooldown=self.safe_zone_cooldown)

    def load_background_layers(self) -> None:
        """Load background layers using provided assets."""
        # Define background layers configuration for jump_sky
        layer_configs = [
            {"file": "sky_layer.png", "scroll_speed": 0.1, "z_order": 1},
            {"file": "mountains_far.png", "scroll_speed": 0.3, "z_order": 2},
            {"file": "trees_far.png", "scroll_speed": 0.5, "z_order": 3},
            {"file": "trees_near.png", "scroll_speed": 0.8, "z_order": 4},
            {"file": "ground_layer.png", "scroll_speed": 1.0, "z_order": 5}
        ]
        
        # Import BackgroundLayer class from jumper game module
        try:
            from unipress.games.jumper.game import BackgroundLayer
            
            for layer_config in layer_configs:
                texture_path = os.path.join("unipress", "assets", "images", "games", "jump_sky", "backgrounds", "layers", layer_config["file"])
                
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
            log_error(e, "Failed to load background layers - using fallback")
            self.background_layers = []

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
        
        # Reset spawn tracking
        self.fruits_spawned = 0
        self.birds_spawned = 0
        self.spawn_timer = 0.0
        
        # Reset safe zone system
        self.safe_zone_active = False
        self.safe_zone_timer = 0.0
        self.time_since_last_safe_zone = 0.0
        
        # Reset UI feedback system
        self.score_display_timer = 0.0
        self.last_score_change = 0
        self.score_popup_text = ""
        self.score_popup_timer = 0.0
        self.jump_indicator_timer = 0.0
        
        # Reset player sprite animation
        self.player_sprite.x = self.player_x
        self.player_sprite.y = self.player_y
        self.player_sprite.set_animation("player/running")
        
        log_game_event("jump_sky_game_reset")
        
    def reset_animations(self) -> None:
        """Reset all animations to prevent accumulated time during startup sound."""
        # Reset player animation by setting it fresh
        self.player_sprite.set_animation("player/running", force=True)

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
            # Set jumping animation
            self.player_sprite.set_animation("player/jumping")
            
            # UI feedback for jump action
            self.jump_indicator_timer = 0.5  # Show jump indicator for 0.5 seconds
            
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
                # Set running animation when landing
                self.player_sprite.set_animation("player/running")
        
        # Update player sprite position and animation
        self.player_sprite.x = self.player_x
        self.player_sprite.y = self.player_y
        self.player_sprite.update(delta_time)

    def on_resize(self, width: int, height: int) -> None:
        """Handle window resize to maintain proper ground positioning."""
        super().on_resize(width, height)
        
        # Update ground position relative to new window height
        old_ground_y = self.ground_y
        self.ground_y = int(height * 0.25) - 30  # Ground lowered by ~30px (half player sprite height)
        
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
        elif fruit_type == "cherry":
            # Red circle pair (cherry shape)
            arcade.draw_circle_filled(x - 4, y + 4, size // 2, arcade.color.RED)
            arcade.draw_circle_filled(x + 4, y - 4, size // 2, arcade.color.RED)
            # Add stems
            arcade.draw_line(x - 4, y + 4 + size // 2, x - 2, y + size, arcade.color.DARK_GREEN, 2)
            arcade.draw_line(x + 4, y - 4 + size // 2, x + 2, y + size, arcade.color.DARK_GREEN, 2)
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

    def trigger_score_popup(self, text: str, fruit_type: str) -> None:
        """Trigger a score popup with fruit-specific styling."""
        self.score_popup_text = text
        self.score_popup_timer = 2.0  # Show for 2 seconds
        self.last_score_change = self.score
        
        log_game_event("score_popup_triggered", text=text, fruit_type=fruit_type)

    def update_ui_feedback(self, delta_time: float) -> None:
        """Update UI feedback timers and effects."""
        # Update score popup timer
        if self.score_popup_timer > 0:
            self.score_popup_timer -= delta_time
            
        # Update jump indicator timer
        if self.jump_indicator_timer > 0:
            self.jump_indicator_timer -= delta_time
            
        # Update score display animation
        self.score_display_timer += delta_time

    def draw_ui_enhancements(self) -> None:
        """Draw enhanced UI elements with professional styling."""
        if not self.game_started:
            return
            
        # Draw score popup when active
        if self.score_popup_timer > 0 and self.score_popup_text:
            # Fade effect based on remaining time
            alpha = min(255, int(255 * (self.score_popup_timer / 2.0)))
            
            # Position above player
            popup_x = self.player_x
            popup_y = self.player_y + 80
            
            # Draw popup background
            popup_bg_color = (*arcade.color.BLACK[:3], alpha // 2)
            arcade.draw_circle_filled(popup_x, popup_y, 25, popup_bg_color)
            
            # Draw popup text with color based on score value
            text_color = (*arcade.color.YELLOW[:3], alpha)
            if "+" in self.score_popup_text:
                points = int(self.score_popup_text[1:])  # Remove "+" prefix
                if points >= 20:
                    text_color = (*arcade.color.ORANGE[:3], alpha)
                elif points >= 15:
                    text_color = (*arcade.color.GOLD[:3], alpha)
                else:
                    text_color = (*arcade.color.GREEN[:3], alpha)
                    
            arcade.draw_text(
                self.score_popup_text,
                popup_x,
                popup_y,
                text_color,
                18,
                anchor_x="center",
                anchor_y="center",
                font_name="Arial"
            )
            
        # Draw jump indicator when active
        if self.jump_indicator_timer > 0:
            # Flash effect for jump feedback
            flash_intensity = math.sin(self.jump_indicator_timer * 15) * 0.5 + 0.5
            indicator_alpha = int(255 * flash_intensity)
            
            # Draw jump arc indicator
            arc_color = (*arcade.color.WHITE[:3], indicator_alpha)
            
            # Draw small arc above player
            for i in range(5):
                angle = -45 + (i * 22.5)  # -45 to +45 degrees
                arc_radius = 40
                arc_x = self.player_x + arc_radius * math.cos(math.radians(angle))
                arc_y = self.player_y + 20 + arc_radius * math.sin(math.radians(angle))
                
                arcade.draw_circle_filled(arc_x, arc_y, 2, arc_color)

    def draw_enhanced_safe_zone_indicator(self) -> None:
        """Draw enhanced safe zone visual indicator."""
        if not self.game_started or not self.safe_zone_active:
            return
            
        # Animated safe zone border
        border_pulse = math.sin(self.safe_zone_timer * 3) * 0.3 + 0.7  # 0.4 to 1.0
        border_alpha = int(150 * border_pulse)
        
        # Draw animated border around entire screen
        border_color = (*arcade.color.GREEN[:3], border_alpha)
        border_width = 8
        
        # Top border
        arcade.draw_lbwh_rectangle_filled(
            0, self.height - border_width, self.width, border_width, border_color
        )
        # Bottom border  
        arcade.draw_lbwh_rectangle_filled(
            0, 0, self.width, border_width, border_color
        )
        # Left border
        arcade.draw_lbwh_rectangle_filled(
            0, 0, border_width, self.height, border_color
        )
        # Right border
        arcade.draw_lbwh_rectangle_filled(
            self.width - border_width, 0, border_width, self.height, border_color
        )
        
        # Enhanced safe zone text using localization - upper center (original upper right level)
        remaining_time = self.safe_zone_duration - self.safe_zone_timer
        safe_zone_text = self.get_message("ui.safe_zone", time=f"{remaining_time:.1f}")
        
        # Draw enhanced safe zone text
        arcade.draw_text(
            safe_zone_text,
            self.width // 2,
            self.height - 32,
            arcade.color.LIGHT_BLUE,
            18,
            anchor_x="center",
            anchor_y="center",
            font_name="Arial"
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
        
        # Handle collisions
        self.handle_collisions()
        
        # Update animation timers
        self.bird_animation_timer += delta_time
        self.player_animation_timer += delta_time
        
        # Update UI feedback timers
        self.update_ui_feedback(delta_time)
        
        # Update background scrolling
        self.update_background(delta_time)
        
        # Safe zone system update
        self.update_safe_zones(delta_time)
        
        # Object spawning system
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_object()
            self.spawn_timer = 0.0

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

    def update_safe_zones(self, delta_time: float) -> None:
        """Update safe zone system - periods with only fruits, no birds."""
        if self.safe_zone_active:
            # Currently in safe zone
            self.safe_zone_timer += delta_time
            if self.safe_zone_timer >= self.safe_zone_duration:
                # End safe zone
                self.safe_zone_active = False
                self.safe_zone_timer = 0.0
                self.time_since_last_safe_zone = 0.0
                
                log_game_event("safe_zone_ended", duration=self.safe_zone_duration)
        else:
            # Not in safe zone - check if we should start one
            self.time_since_last_safe_zone += delta_time
            
            # Start safe zone after cooldown (or immediately at game start)
            if (self.time_since_last_safe_zone >= self.safe_zone_cooldown or 
                (self.fruits_spawned + self.birds_spawned == 0 and self.time_since_last_safe_zone > 5.0)):
                self.safe_zone_active = True
                self.safe_zone_timer = 0.0
                
                log_game_event("safe_zone_started", duration=self.safe_zone_duration, 
                              fruits_spawned=self.fruits_spawned, birds_spawned=self.birds_spawned)

    def spawn_object(self) -> None:
        """Spawn object (fruit or bird) based on configured ratio and constraints."""
        total_objects = len(self.fruits) + len(self.birds)
        
        # Check maximum objects constraint
        if total_objects >= self.max_objects:
            return
        
        # Safe zone check - no birds during safe zones
        if self.safe_zone_active:
            spawn_bird = False
        else:
            # Determine if we should spawn a bird based on ratio
            # Target: bird_to_fruit_ratio birds per fruit (e.g., 0.25 = 1 bird per 4 fruits)
            target_birds = self.fruits_spawned * self.bird_to_fruit_ratio
            should_spawn_bird = self.birds_spawned < target_birds
            
            if should_spawn_bird and self.birds_spawned == 0:
                # Force first bird spawn if we haven't spawned any yet and should have one
                spawn_bird = True
            elif should_spawn_bird:
                # 80% chance to spawn bird when we're behind on ratio
                spawn_bird = random.random() < 0.8
            else:
                # 10% chance to spawn bird when ratio is satisfied
                spawn_bird = random.random() < 0.1
        
        # Height randomization for all objects (spawn-002 implemented here)
        height_min = get_setting(self.settings, "jump_sky.height_min", 60)
        height_max = get_setting(self.settings, "jump_sky.height_max", 150)
        spawn_y = self.ground_y + random.uniform(height_min, height_max)
        spawn_x = self.width + 50
            
        if spawn_bird:
            # Spawn bird with random type selection (spawn-005 implemented here)
            bird_type = random.choice(self.bird_types)
            bird = self.create_bird(bird_type, spawn_x, spawn_y)
            self.birds.append(bird)
            self.birds_spawned += 1
            
            log_game_event("bird_spawned", bird_type=bird_type, 
                          velocity=bird.velocity, spawn_ratio=self.birds_spawned/max(1, self.fruits_spawned))
        else:
            # Spawn fruit
            fruit_types = ["apple", "banana", "cherry", "orange"]
            fruit_type = random.choice(fruit_types)
            fruit = self.create_fruit(fruit_type, spawn_x, spawn_y)
            self.fruits.append(fruit)
            self.fruits_spawned += 1
            
            log_game_event("fruit_spawned", fruit_type=fruit_type, 
                          velocity=fruit.velocity, points=fruit.points, spawn_ratio=self.birds_spawned/max(1, self.fruits_spawned))

    def get_player_collision_rect(self) -> dict:
        """Get player collision rectangle using AnimatedSprite hitbox or fallback."""
        # Try to use AnimatedSprite's accurate hitbox first
        if self.player_sprite.current_animation:
            return self.player_sprite.get_hitbox()
        else:
            # Fallback: use traditional collision box including legs with size reduction for fair gameplay
            size_reduction = 4
            return {
                "x": self.player_x - 16 + size_reduction,
                "y": self.player_y - 28 + size_reduction,  # Lower to include legs 
                "width": 32 - (size_reduction * 2),
                "height": 56 - (size_reduction * 2)  # Taller to match sprite hitbox
            }

    def rectangles_overlap(self, rect1: dict, rect2: dict) -> bool:
        """Check if two rectangles overlap."""
        return (rect1["x"] < rect2["x"] + rect2["width"] and
                rect1["x"] + rect1["width"] > rect2["x"] and
                rect1["y"] < rect2["y"] + rect2["height"] and
                rect1["y"] + rect1["height"] > rect2["y"])

    def handle_collisions(self) -> None:
        """Handle all collision detection and responses."""
        if not self.game_started:
            return
            
        player_rect = self.get_player_collision_rect()
        
        # Bird collision detection (collision-002) - Higher priority, only when jumping
        if self.is_jumping:
            for bird in self.birds[:]:
                if not bird.removed:
                    bird_rect = bird.get_collision_rect()
                    if self.rectangles_overlap(player_rect, bird_rect):
                        # Bird collision - lose life (collision-003: bird overrides fruit)
                        bird.removed = True
                        self.lose_life()
                        
                        # Play failure sound
                        self.play_sound_event("failure")
                        
                        log_player_action("bird_collision", 
                                        bird_type=bird.bird_type,
                                        lives_remaining=self.lives,
                                        player_y=self.player_y,
                                        is_jumping=self.is_jumping)
                        return  # Bird collision overrides fruit collection
        
        # Fruit collision detection (collision-001) - Only if no bird collision
        for fruit in self.fruits[:]:
            if not fruit.collected:
                fruit_rect = fruit.get_collision_rect()
                if self.rectangles_overlap(player_rect, fruit_rect):
                    # Collect fruit
                    fruit.collected = True
                    self.score += fruit.points
                    self.check_and_play_high_score_sound(self.score)
                    
                    # UI feedback for score gain
                    self.trigger_score_popup(f"+{fruit.points}", fruit.fruit_type)
                    
                    # Play success sound
                    self.play_sound_event("success")
                    
                    log_player_action("fruit_collected", 
                                    fruit_type=fruit.fruit_type,
                                    points=fruit.points,
                                    total_score=self.score,
                                    player_y=self.player_y,
                                    is_jumping=self.is_jumping)
                    break  # Only collect one fruit per frame

    def update_background(self, delta_time: float) -> None:
        """Update parallax background layers."""
        for layer in self.background_layers:
            layer.update(delta_time, self.background_speed)

    def draw_background(self) -> None:
        """Draw background layers with fallback system."""
        if self.background_layers:
            # Sort by z_order and draw back to front
            sorted_layers = sorted(self.background_layers, key=lambda l: l.z_order)
            for layer in sorted_layers:
                layer.draw(self.width, self.height)
        else:
            # Fallback: simple gradient background when no layers loaded
            arcade.draw_lbwh_rectangle_filled(0, 0, self.width, self.height, arcade.color.SKY_BLUE)
            arcade.draw_lbwh_rectangle_filled(0, 0, self.width, self.ground_y, arcade.color.FOREST_GREEN)

    def on_draw(self) -> None:
        """Draw the game."""
        self.clear()
        
        # Draw background layers with fallback system
        self.draw_background()
        
        # Draw player using AnimatedSprite system with fallback
        if self.should_draw_player():
            self.player_sprite.draw()
            # If AnimatedSprite has no animation, it draws the blue rectangle fallback automatically
        
        # Draw active fruits
        for fruit in self.fruits:
            fruit.draw(self.draw_fallback_fruit)
            
        # Draw active birds (higher Z-order than fruits)
        for bird in self.birds:
            bird.draw(self.draw_fallback_bird)
        
        # Draw enhanced gameplay instructions and tips (when game is started)
        if self.game_started and not self.is_game_paused():
            
            # Enhanced next safe zone countdown (if not in safe zone) - lower center (original lower right level)
            if not self.safe_zone_active:
                next_safe_zone = self.safe_zone_cooldown - self.time_since_last_safe_zone
                if next_safe_zone > 0:
                    countdown_text = self.get_message("ui.next_safe_zone", time=f"{next_safe_zone:.1f}")
                    
                    arcade.draw_text(
                        countdown_text,
                        self.width // 2,
                        20,
                        arcade.color.LIGHT_BLUE,
                        16,
                        anchor_x="center",
                        font_name="Arial"
                    )
            
        # Draw enhanced safe zone indicator
        self.draw_enhanced_safe_zone_indicator()
        
        # Draw UI enhancements (score popups, jump indicators, etc.)
        self.draw_ui_enhancements()
        
        
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
    
    game = JumpSkyGame(difficulty=difficulty)
    game.run()