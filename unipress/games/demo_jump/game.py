"""
Demo Jump Game - Simple one-button jumping game.

Click to make the player jump over incoming obstacles.
Difficulty affects how much time you have to react to obstacles.
"""

import random

import arcade

from unipress.core.base_game import BaseGame
from unipress.core.logger import log_game_event


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
        arcade.draw_lbwh_rectangle_filled(
            self.x, self.y, self.width, self.height, arcade.color.RED
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

    def __init__(self, difficulty: int = None):
        super().__init__(
            game_name="demo_jump",
            width=800,
            height=600,
            title="Demo Jump Game",
            difficulty=difficulty,
        )

        # Update title to show actual difficulty from settings
        self.set_caption(
            f"{self.get_message('game.title')} (Difficulty: {self.difficulty})"
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
        # Base interval should be longer to allow recovery time
        base_interval = settings["reaction_time"] * 2.5  # Increased from 1.5
        self.obstacle_spawn_time = base_interval * random.uniform(
            0.8, 1.5
        )  # Add initial randomness
        self.last_obstacle_time = 0.0

        # Game objects
        self.obstacles: list[Obstacle] = []
        self.time_elapsed = 0.0

    def get_difficulty_settings(self) -> dict[str, float | int]:
        """Override to add game-specific difficulty settings."""
        base_settings = super().get_difficulty_settings()

        # Add game-specific settings
        # Jump height must be enough to clear 50px obstacles + safety margin
        # Base jump height ensures obstacle clearance, difficulty adds extra height
        obstacle_height = 50
        base_jump_height = obstacle_height + 100  # 100px safety margin above obstacle
        difficulty_bonus = (
            11 - self.difficulty
        ) * 20  # More height on easier difficulties

        base_settings.update(
            {
                "obstacle_speed": 100
                + (self.difficulty * 15),  # Faster obstacles = harder
                "jump_height": base_jump_height
                + difficulty_bonus,  # Guaranteed clearance
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
        # Check if we're in life lost pause first
        if self.handle_life_lost_continue():
            return

        if not self.game_started:
            self.start_game()
        elif self.game_over:
            self.start_game()
        elif self.player_on_ground:
            # Jump!
            settings = self.get_difficulty_settings()
            desired_jump_height = float(settings["jump_height"])
            gravity = 800
            # Calculate initial velocity needed to reach desired height
            # Using physics: max_height = (initial_velocity^2) / (2 * gravity)
            self.player_jump_speed = (2 * gravity * desired_jump_height) ** 0.5
            self.player_on_ground = False

            # Log jump action with physics details
            log_game_event(
                "player_jump",
                jump_height=desired_jump_height,
                jump_speed=self.player_jump_speed,
                gravity=gravity,
                difficulty=self.difficulty,
            )

    def on_update(self, delta_time: float) -> None:
        """Update game logic."""
        # Always update life lost effects for blinking
        self.update_life_lost_effects(delta_time)

        # Update end game screen for automatic cycling
        if self.show_end_screen and self.end_game_screen:
            self.end_game_screen.update(delta_time)

        # Pause game logic during life lost pause
        if self.is_game_paused():
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

            # Adjust spawn timing with more variety and longer intervals
            base_interval = self.reaction_time * 2.5
            self.obstacle_spawn_time = base_interval * random.uniform(
                0.7, 2.0
            )  # Much more variation

        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(delta_time)

            # Remove obstacles that are off-screen
            if obstacle.x + obstacle.width < 0:
                self.obstacles.remove(obstacle)
                self.score += 10
                log_game_event("obstacle_cleared", score=self.score)

            # Check collision
            if obstacle.collides_with(self.player_x, self.player_y, self.player_size):
                log_game_event(
                    "obstacle_collision",
                    player_x=self.player_x,
                    player_y=self.player_y,
                    obstacle_x=obstacle.x,
                    obstacle_y=obstacle.y,
                    score=self.score,
                )
                self.lose_life()

        # Increase score over time
        self.score += int(delta_time * 5)

    def on_draw(self) -> None:
        """Draw the game."""
        self.clear()

        if self.game_started and not self.game_over:
            # Draw ground line
            arcade.draw_line(0, 100, self.width, 100, arcade.color.WHITE, 2)

            # Draw player (with blinking effect during life lost)
            if self.should_draw_player():
                if self.life_lost_pause:
                    color = arcade.color.RED
                else:
                    color = (
                        arcade.color.BLUE
                        if self.player_on_ground
                        else arcade.color.LIGHT_BLUE
                    )

                arcade.draw_lbwh_rectangle_filled(
                    self.player_x,
                    self.player_y,
                    self.player_size,
                    self.player_size,
                    color,
                )

            # Draw obstacles
            for obstacle in self.obstacles:
                obstacle.draw()

            # Draw jump window indicator
            # Calculate the distance where jump is still possible
            # This is based on obstacle speed and jump duration
            settings = self.get_difficulty_settings()
            obstacle_speed = settings["obstacle_speed"]

            # Jump takes time to reach peak and come back down
            # Total jump time = 2 * sqrt(2 * jump_height / gravity)
            jump_height = settings["jump_height"]
            gravity = 800
            jump_duration = 2 * (jump_height / gravity) ** 0.5

            # Distance an obstacle travels during jump
            jump_window_distance = obstacle_speed * jump_duration

            # Draw the jump window as a green zone on screen
            jump_zone_start = self.player_x + self.player_size
            jump_zone_width = min(jump_window_distance, 200)  # Cap at 200px for display

            arcade.draw_lbwh_rectangle_filled(
                jump_zone_start, 45, jump_zone_width, 10, arcade.color.GREEN
            )
            arcade.draw_text(
                self.get_message(
                    "game.jump_window_info",
                    distance=f"{jump_window_distance:.2f}",
                    duration=f"{jump_duration:.2f}",
                ),
                10,
                20,
                arcade.color.WHITE,
                12,
            )

        # Draw UI
        self.draw_ui()


def main() -> None:
    """Run the demo game."""
    from unipress.core.logger import init_logger

    # Initialize logging for standalone game execution
    init_logger("demo_jump")

    try:
        # You can change difficulty here (1-10)
        DemoJumpGame(difficulty=5).run()
    except Exception as e:
        from unipress.core.logger import log_error

        log_error(e, "Demo game crashed during standalone execution")
        raise


if __name__ == "__main__":
    main()
