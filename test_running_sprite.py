"""
Simple test script to display running sprite animation using our AssetManager.
"""

import arcade
from unipress.core.assets import load_animation

class RunningTestWindow(arcade.Window):
    """Test window to display running sprite animation."""

    def __init__(self):
        super().__init__(800, 600, "Running Sprite Test")
        arcade.set_background_color(arcade.color.DARK_BLUE)
        
        # Load running animation
        self.running_animation = load_animation("player/running", "jumper")
        
        if self.running_animation:
            print(f"Animation loaded: {self.running_animation.name}")
            print(f"Frame count: {len(self.running_animation.frames)}")
            print("Animation working - sprites should be visible!")
        else:
            print("Failed to load animation")
        
        # Position for sprite
        self.sprite_x = 400
        self.sprite_y = 300

    def on_update(self, delta_time):
        """Update animation."""
        if self.running_animation:
            self.running_animation.update(delta_time)

    def on_draw(self):
        """Draw the running sprite."""
        self.clear()
        
        # Draw info text
        arcade.draw_text("Running Sprite Test", 10, 550, arcade.color.WHITE, 20)
        
        if self.running_animation:
            # Get current frame texture
            texture = self.running_animation.get_current_texture()
            
            # Try different arcade drawing methods
            try:
                # Method 1: Create a temporary sprite
                sprite = arcade.Sprite()
                sprite.texture = texture
                sprite.center_x = self.sprite_x
                sprite.center_y = self.sprite_y
                # Scale up the sprite (2x larger)
                sprite.scale = 2.0
                
                # Draw using sprite list (this should work)
                sprite_list = arcade.SpriteList()
                sprite_list.append(sprite)
                sprite_list.draw()
                
                arcade.draw_text(f"Frame: {self.running_animation.current_frame + 1}/{len(self.running_animation.frames)}", 
                               10, 520, arcade.color.WHITE, 16)
                arcade.draw_text("Using SpriteList method", 10, 490, arcade.color.GREEN, 16)
                
            except Exception as e:
                # Fallback: draw rectangle with frame info
                arcade.draw_lbwh_rectangle_filled(self.sprite_x - 32, self.sprite_y - 32, 64, 64, arcade.color.RED)
                arcade.draw_text(f"Texture draw failed: {str(e)}", 10, 490, arcade.color.RED, 16)
                arcade.draw_text(f"But animation is working! Frame: {self.running_animation.current_frame + 1}", 
                               10, 460, arcade.color.YELLOW, 16)
        else:
            arcade.draw_text("No animation loaded", 10, 490, arcade.color.RED, 16)

    def on_key_press(self, key, modifiers):
        """Handle key presses."""
        if key == arcade.key.ESCAPE:
            self.close()

if __name__ == "__main__":
    print("Starting Running Sprite Test...")
    print("Press ESC to exit")
    window = RunningTestWindow()
    window.run()