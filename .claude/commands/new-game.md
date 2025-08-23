# /new-game - Game Scaffolding

Create a new game with complete structure following Unipress standards.

## Usage

```
/new-game [name]
```

## Parameters

- `name`: Game name in snake_case (e.g., puzzle_challenge, rhythm_master)

## Example

```
/new-game puzzle_challenge
```

## Implementation

1. **Validate game name**
   - Check snake_case format
   - Ensure name doesn't exist
   - Validate follows one-button constraint naming

2. **Create game directory structure**
   ```bash
   mkdir -p unipress/games/[name]
   ```

3. **Create core game files**
   - `__init__.py` - Package initialization
   - `game.py` - Main game implementation
   - `settings.toml` - Game-specific configuration

4. **Generate game.py template**
   ```python
   from unipress.core.base_game import BaseGame
   import arcade

   class [ClassName]Game(BaseGame):
       \"\"\"
       [Name] Game - One-button game implementation.
       
       Controls: Left mouse click (binary signal only)
       Difficulty: 1-10 scale affects reaction time windows
       Lives: 3 lives with pause-after-death mechanics
       \"\"\"
       
       def __init__(self, difficulty: int = 5, lives: int = 3, fullscreen: bool = True):
           super().__init__("[name]", difficulty, lives, fullscreen)
           # TODO: Initialize game-specific variables
           
       def setup(self):
           \"\"\"Set up game-specific elements.\"\"\"
           super().setup()
           # TODO: Set up sprites, sounds, initial state
           
       def on_update(self, delta_time: float):
           \"\"\"Update game logic.\"\"\"
           super().on_update(delta_time)
           # TODO: Implement game mechanics
           
       def on_draw(self):
           \"\"\"Render the game.\"\"\"
           super().on_draw()
           # TODO: Draw game-specific elements
           
       def handle_click(self):
           \"\"\"Handle one-button input.\"\"\"
           # TODO: Implement click response
           pass

   if __name__ == "__main__":
       import sys
       difficulty = int(sys.argv[1]) if len(sys.argv) > 1 else 5
       game = [ClassName]Game(difficulty)
       game.run()
   ```

5. **Generate settings.toml**
   ```toml
   [game]
   difficulty = 5  # Override global difficulty (1-10)
   lives = 3       # Override global lives count
   
   [[name]]
   # TODO: Add game-specific settings
   
   [audio]
   # TODO: Configure audio settings if needed
   ```

6. **Create asset directories**
   ```bash
   mkdir -p unipress/assets/images/games/[name]
   mkdir -p unipress/assets/sounds/games/[name]
   ```

7. **Generate localization templates**
   ```bash
   # Create message files for Polish and English
   # unipress/locales/pl_PL/games/[name].json
   # unipress/locales/en_US/games/[name].json
   ```

## Validation

- Ensure follows one-button constraint
- Check BaseGame inheritance
- Validate settings integration
- Confirm asset management setup
- Test localization support

## One-Button Constraint Validation

The generated game template includes comments and validation for:
- Binary signal input only (no cursor positioning)
- Timing-based or automatic cycling interactions
- No direct element selection capability
- Reaction time window scaling with difficulty

## Related Standards

- Inherits from BaseGame class
- Follows TOML settings hierarchy
- Implements internationalization
- Includes professional logging
- Supports sound system integration
- Uses conventional project structure