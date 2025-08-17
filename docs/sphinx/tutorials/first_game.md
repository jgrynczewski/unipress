# Creating Your First Game

## Overview

This tutorial will guide you through creating your first one-button game using the Unipress framework.

## Prerequisites

- Complete [Installation Guide](installation.md)
- Basic Python knowledge
- Understanding of [Game Design Standards](game_design.md)

## Game Concept

We'll create a simple jumping game where the player must avoid obstacles by timing their jumps.

## Implementation Steps

### 1. Create Game Class

```python
from unipress.core.base_game import BaseGame
import arcade

class MyFirstGame(BaseGame):
    def setup(self) -> None:
        """Initialize game components."""
        self.player = arcade.Sprite(":resources:images/player.png")
        self.obstacles = arcade.SpriteList()
        self.score = 0
        self.lives = 3
```

### 2. Implement Game Logic

```python
def update(self, delta_time: float) -> None:
    """Update game logic."""
    self.player.update()
    self.obstacles.update()
    
    # Check collisions
    if arcade.check_for_collision_with_list(self.player, self.obstacles):
        self.lives -= 1
        self.play_sound("player", "collision")
```

### 3. Add Rendering

```python
def on_draw(self) -> None:
    """Render the game."""
    arcade.start_render()
    self.player.draw()
    self.obstacles.draw()
    self.draw_ui()
```

## Next Steps

- Add [Asset Management](assets.md) for custom sprites
- Implement [Sound System](sound.md) for audio
- Optimize [Performance](performance.md)
- Add [Testing](testing.md)

## Complete Example

See the [Jumper Game](../../unipress/games/jumper/game.py) for a complete implementation.
