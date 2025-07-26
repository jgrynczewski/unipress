"""
Demo Jump Game - Simple one-button jumping game.

Click to make the player jump over incoming obstacles.
Difficulty affects how much time you have to react to obstacles.
"""

import random

import arcade

from ..core.base_game import BaseGame


class Obstacle:
    """Simple obstacle that moves from right to left."""

    def __init__(self, x: float, y: float, width: float = 30, height: float = 50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 200  # pixels per second

    def update(self, delta_time: float) -> None:
        """Move obstacle left."""
        self.x -= self.speed * delta_time

    def draw(self) -> None:
        """Draw obstacle as red rectangle."""
        arcade.draw_rectangle_filled(  # type: ignore[attr-defined]
            self.x, self.y + self.height // 2, self.width, self.height, arcade.color.RED
        )

    def collides_with(
        self, player_x: float, player_y: float, player_size: float
    ) -> bool:
        """Check collision with player."""
        return (
            player_x + player_size > self.x
            and player_x < self.x + self.width
            and player_y + player_size > self.y
            and player_y < self.y + self.height
        )


class DemoJumpGame(BaseGame):  # type: ignore[misc]
    """
    Simple jumping game demo.

    - Click to jump
    - Avoid red obstacles
    - Score increases over time
    - Difficulty affects obstacle spacing (reaction time)
    """

    def __init__(self, difficulty: int = 5):
        super().__init__(
            width=800,
            height=600,
            title=f"Demo Jump Game (Difficulty: {difficulty})",
            difficulty=difficulty,
        )

        # Player settings
        self.player_x = 100.0
        self.player_y = 100.0
        self.player_size = 40.0
        self.player_jump_speed = 0.0
        self.player_on_ground = True

        # Game settings based on difficulty
        settings = self.get_difficulty_settings()

        # Obstacle spawn timing based on reaction time
        # More difficult = less time between obstacles
        self.obstacle_spawn_time = settings["reaction_time"] * 1.5
        self.last_obstacle_time = 0.0

        # Game objects
        self.obstacles: list[Obstacle] = []
        self.time_elapsed = 0.0

    def get_difficulty_settings(self) -> dict[str, float | int]:
        """Override to add game-specific difficulty settings."""
        base_settings = super().get_difficulty_settings()

        # Add game-specific settings
        base_settings.update(
            {
                "obstacle_speed": 150
                + (self.difficulty * 20),  # Faster obstacles = harder
                "jump_height": max(
                    200, 350 - (self.difficulty * 15)
                ),  # Lower jumps = harder
            }
        )

        return base_settings

    def reset_game(self) -> None:
        """Reset game state."""
        self.player_y = 100.0
        self.player_jump_speed = 0.0
        self.player_on_ground = True
        self.obstacles.clear()
        self.time_elapsed = 0.0
        self.score = 0
        self.last_obstacle_time = 0.0

    def on_action_press(self) -> None:
        """Handle main action (jump or start/restart game)."""
        if not self.game_started:
            self.start_game()
        elif self.game_over:
            self.start_game()
        elif self.player_on_ground:
            # Jump!
            settings = self.get_difficulty_settings()
            self.player_jump_speed = float(settings["jump_height"])
            self.player_on_ground = False

    def on_update(self, delta_time: float) -> None:
        """Update game logic."""
        if not self.game_started or self.game_over:
            return

        self.time_elapsed += delta_time

        # Update player physics
        if not self.player_on_ground:
            self.player_jump_speed -= 800 * delta_time  # Gravity
            self.player_y += self.player_jump_speed * delta_time

            # Land on ground
            if self.player_y <= 100:
                self.player_y = 100
                self.player_on_ground = True
                self.player_jump_speed = 0

        # Spawn obstacles
        if self.time_elapsed - self.last_obstacle_time > self.obstacle_spawn_time:
            self.obstacles.append(Obstacle(self.width + 50, 100))
            self.last_obstacle_time = self.time_elapsed

            # Adjust spawn timing slightly for variety
            self.obstacle_spawn_time = self.reaction_time * random.uniform(1.2, 1.8)

        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(delta_time)

            # Remove obstacles that are off-screen
            if obstacle.x + obstacle.width < 0:
                self.obstacles.remove(obstacle)
                self.score += 10

            # Check collision
            if obstacle.collides_with(self.player_x, self.player_y, self.player_size):
                self.end_game()

        # Increase score over time
        self.score += int(delta_time * 5)

    def on_draw(self) -> None:
        """Draw the game."""
        self.clear()

        if self.game_started and not self.game_over:
            # Draw ground line
            arcade.draw_line(0, 100, self.width, 100, arcade.color.WHITE, 2)

            # Draw player
            color = (
                arcade.color.BLUE if self.player_on_ground else arcade.color.LIGHT_BLUE
            )
            arcade.draw_rectangle_filled(  # type: ignore[attr-defined]
                self.player_x + self.player_size // 2,
                self.player_y + self.player_size // 2,
                self.player_size,
                self.player_size,
                color,
            )

            # Draw obstacles
            for obstacle in self.obstacles:
                obstacle.draw()

            # Draw reaction time indicator for demo purposes
            reaction_indicator_width = (
                self.reaction_time / 2.0
            ) * 200  # Max width 200px
            arcade.draw_rectangle_filled(  # type: ignore[attr-defined]
                100, 50, reaction_indicator_width, 10, arcade.color.GREEN
            )
            arcade.draw_text(
                f"Reaction window: {self.reaction_time:.1f}s",
                10,
                20,
                arcade.color.WHITE,
                12,
            )

        # Draw UI
        self.draw_ui()


def main() -> None:
    """Run the demo game."""
    # You can change difficulty here (1-10)
    DemoJumpGame(difficulty=5).run()


if __name__ == "__main__":
    main()
