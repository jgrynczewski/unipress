# BaseGame Class

## Overview

The `BaseGame` class is the abstract base class that provides the foundation for all games in the Unipress framework. It implements the core game loop, input handling, asset management, and common functionality that all one-button games share.

## Class Definition

```python
class BaseGame(arcade.Window):
    """Abstract base class for all Unipress games."""
```

## Inheritance

- **Parent Class**: `arcade.Window`
- **Abstract Methods**: Must be implemented by subclasses
- **Concrete Methods**: Common functionality provided by base class

## Core Features

### One-Button Input Constraint
All games inherit the strict one-button input constraint, ensuring accessibility and simplicity across the entire game collection.

### Asset Management
Integrated asset loading and caching for sprites, sounds, and animations with JSON metadata support.

### Sound System
Event-driven audio system with OGG format support and volume control.

### Settings Integration
Hierarchical TOML-based configuration system with game-specific settings.

### Logging
Structured JSON logging with Loguru for debugging and monitoring.

## Abstract Methods

### `setup()`
**Signature**: `def setup(self) -> None`

**Description**: Initialize game-specific components and state.

**Required Implementation**: Yes

**Example**:
```python
def setup(self) -> None:
    """Initialize game-specific components."""
    self.player = arcade.Sprite(":resources:images/player.png")
    self.obstacles = arcade.SpriteList()
    self.score = 0
    self.lives = 3
```

### `update(delta_time: float)`
**Signature**: `def update(self, delta_time: float) -> None`

**Description**: Update game logic and state.

**Parameters**:
- `delta_time` (float): Time elapsed since last update in seconds

**Required Implementation**: Yes

**Example**:
```python
def update(self, delta_time: float) -> None:
    """Update game logic."""
    self.player.update()
    self.obstacles.update()
    
    # Check collisions
    if arcade.check_for_collision_with_list(self.player, self.obstacles):
        self.lives -= 1
        self.sound_manager.play("player", "collision")
```

### `on_draw()`
**Signature**: `def on_draw(self) -> None`

**Description**: Render the game screen.

**Required Implementation**: Yes

**Example**:
```python
def on_draw(self) -> None:
    """Render the game screen."""
    arcade.start_render()
    
    # Draw background
    arcade.draw_lrwh_rectangle_textured(
        0, 0, self.width, self.height, self.background
    )
    
    # Draw game objects
    self.player.draw()
    self.obstacles.draw()
    
    # Draw UI
    self.draw_ui()
```

## Concrete Methods

### Input Handling

#### `on_key_press(key: int, modifiers: int)`
**Signature**: `def on_key_press(self, key: int, modifiers: int) -> None`

**Description**: Handle key press events. Implements one-button constraint.

**Parameters**:
- `key` (int): Key code
- `modifiers` (int): Modifier keys (Ctrl, Alt, etc.)

**Implementation**: Provided by base class

**Behavior**:
- Only responds to spacebar and mouse clicks
- Ignores all other input
- Logs input events for debugging

#### `on_mouse_press(x: int, y: int, button: int, modifiers: int)`
**Signature**: `def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None`

**Description**: Handle mouse press events.

**Parameters**:
- `x` (int): Mouse X coordinate
- `y` (int): Mouse Y coordinate
- `button` (int): Mouse button
- `modifiers` (int): Modifier keys

**Implementation**: Provided by base class

### Asset Management

#### `load_assets()`
**Signature**: `def load_assets(self) -> None`

**Description**: Load game assets using the asset manager.

**Implementation**: Provided by base class

**Features**:
- Automatic asset discovery
- JSON metadata loading
- Caching for performance
- Error handling for missing assets

#### `get_sprite(name: str) -> arcade.Sprite`
**Signature**: `def get_sprite(self, name: str) -> arcade.Sprite`

**Description**: Get a sprite from the asset manager.

**Parameters**:
- `name` (str): Asset name

**Returns**: `arcade.Sprite` - Loaded sprite

**Example**:
```python
player_sprite = self.get_sprite("player_idle")
```

### Sound Management

#### `play_sound(category: str, name: str)`
**Signature**: `def play_sound(self, category: str, name: str) -> None`

**Description**: Play a sound effect.

**Parameters**:
- `category` (str): Sound category (e.g., "player", "ui")
- `name` (str): Sound name

**Example**:
```python
self.play_sound("player", "jump")
self.play_sound("ui", "button_click")
```

#### `set_volume(volume: float)`
**Signature**: `def set_volume(self, volume: float) -> None`

**Description**: Set master volume (0.0 to 1.0).

**Parameters**:
- `volume` (float): Volume level

### Settings Management

#### `get_setting(section: str, key: str, default=None)`
**Signature**: `def get_setting(self, section: str, key: str, default=None) -> Any`

**Description**: Get a setting value.

**Parameters**:
- `section` (str): Settings section
- `key` (str): Setting key
- `default`: Default value if not found

**Returns**: Setting value

**Example**:
```python
difficulty = self.get_setting("game", "difficulty", 3)
volume = self.get_setting("audio", "volume", 0.8)
```

#### `set_setting(section: str, key: str, value: Any)`
**Signature**: `def set_setting(self, section: str, key: str, value: Any) -> None`

**Description**: Set a setting value.

**Parameters**:
- `section` (str): Settings section
- `key` (str): Setting key
- `value`: Setting value

### Game State Management

#### `start_game()`
**Signature**: `def start_game(self) -> None`

**Description**: Start the game.

**Implementation**: Provided by base class

**Features**:
- Initialize game state
- Start game loop
- Load assets
- Set up logging

#### `end_game()`
**Signature**: `def end_game(self) -> None`

**Description**: End the game.

**Implementation**: Provided by base class

**Features**:
- Save high scores
- Clean up resources
- Log game statistics

#### `reset_game()`
**Signature**: `def reset_game(self) -> None`

**Description**: Reset game state.

**Implementation**: Provided by base class

**Features**:
- Reset score and lives
- Clear game objects
- Restart game loop

### UI Rendering

#### `draw_ui()`
**Signature**: `def draw_ui(self) -> None`

**Description**: Draw user interface elements.

**Implementation**: Provided by base class

**Features**:
- Score display
- Lives counter
- Game status
- Consistent styling

#### `draw_text(text: str, x: int, y: int, color: arcade.Color, size: int = 20)`
**Signature**: `def draw_text(self, text: str, x: int, y: int, color: arcade.Color, size: int = 20) -> None`

**Description**: Draw text with consistent styling.

**Parameters**:
- `text` (str): Text to draw
- `x` (int): X coordinate
- `y` (int): Y coordinate
- `color` (arcade.Color): Text color
- `size` (int): Font size

### Logging

#### `log_event(event: str, data: dict = None)`
**Signature**: `def log_event(self, event: str, data: dict = None) -> None`

**Description**: Log a game event.

**Parameters**:
- `event` (str): Event name
- `data` (dict): Event data

**Example**:
```python
self.log_event("player_jump", {"height": jump_height})
self.log_event("obstacle_hit", {"obstacle_type": "fire"})
```

## Configuration

### Settings Structure

The BaseGame class expects the following settings structure:

```toml
[display]
fullscreen = true
width = 1920
height = 1080

[audio]
enabled = true
volume = 0.8

[game]
difficulty = 3
lives = 3

[logging]
level = "INFO"
format = "json"
```

### Asset Structure

Assets should be organized as follows:

```
assets/
├── games/
│   └── game_name/
│       ├── sprites/
│       ├── sounds/
│       └── animations/
└── global/
    ├── ui/
    └── system/
```

## Usage Example

```python
from unipress.core.base_game import BaseGame
import arcade

class MyGame(BaseGame):
    def setup(self) -> None:
        """Initialize game components."""
        self.player = self.get_sprite("player")
        self.obstacles = arcade.SpriteList()
        self.score = 0
        
    def update(self, delta_time: float) -> None:
        """Update game logic."""
        self.player.update()
        self.obstacles.update()
        
        # Game logic here
        
    def on_draw(self) -> None:
        """Render the game."""
        arcade.start_render()
        self.player.draw()
        self.obstacles.draw()
        self.draw_ui()

def main():
    """Run the game."""
    game = MyGame()
    game.run()

if __name__ == "__main__":
    main()
```

## Best Practices

### 1. Implement Required Methods
Always implement `setup()`, `update()`, and `on_draw()` methods.

### 2. Use Asset Manager
Load assets through the asset manager for consistent handling.

### 3. Follow One-Button Constraint
Only respond to spacebar and mouse clicks.

### 4. Use Settings System
Access configuration through the settings system.

### 5. Log Important Events
Log game events for debugging and analytics.

### 6. Handle Errors Gracefully
Use try-catch blocks for asset loading and game logic.

## Related Classes

- [AssetManager](assets.md) - Asset loading and management
- [SoundManager](sound.md) - Audio system
- [SettingsManager](settings.md) - Configuration management
- [Logger](logger.md) - Logging system
