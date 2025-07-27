# ADR-010: TOML-Based Settings System

## Status
Accepted

## Context
Unipress games need a configuration system for managing game parameters like difficulty level and number of lives. The system should support:
- Global default settings for all games
- Per-game settings that can override global defaults
- Easy editing by developers and potentially users
- Type safety and validation

## Decision
We will implement a **TOML-based hierarchical settings system** with global and per-game configuration files.

## Settings File Format Comparison

### JSON
- **Pros**: 
  - Native Python support (no dependencies)
  - Hierarchical structure support
  - Type safety (int, bool, string, arrays)
  - Widely known format
- **Cons**: 
  - No comments support
  - More verbose syntax
  - Strict syntax requirements (trailing commas, etc.)

### INI
- **Pros**: 
  - Simple, readable format
  - Comments support
  - Standard in many applications
  - Familiar to users
- **Cons**: 
  - Flat structure (difficult for nested settings)
  - Type ambiguity (everything parsed as string)
  - Limited data types support
  - No arrays or complex structures

### TOML (Chosen Solution)
- **Pros**: 
  - Comments support for documentation
  - Type safety (int, bool, string, arrays, tables)
  - Hierarchical structure with clear syntax
  - Very readable and human-friendly
  - Growing adoption in Python ecosystem
  - Excellent for configuration files
- **Cons**: 
  - External dependency (tomli/tomllib)
  - Less universally known than JSON/INI

## Implementation Architecture

### File Structure
```
unipress/
├── settings.toml                    # Global default settings
├── games/
│   ├── demo_jump/
│   │   └── settings.toml           # Game-specific overrides
│   └── jumper/
│       └── settings.toml           # Game-specific overrides
```

### Settings Priority (Highest to Lowest)
1. **Constructor Parameters**: `BaseGame(difficulty=8, lives=1)`
2. **Game Settings**: `unipress/games/{game_name}/settings.toml`
3. **Global Settings**: `unipress/settings.toml`
4. **Default Values**: Hardcoded in BaseGame class

### TOML Schema Example

**Global Settings (`unipress/settings.toml`)**:
```toml
# Unipress Global Game Settings
# These are default values for all games

[game]
# Difficulty level (1-10): 1=easy, 10=hard
difficulty = 5

# Number of lives per game
lives = 3

# Display settings
fullscreen = true

[ui]
# UI refresh rate and timing
blink_duration = 1.0
```

**Game Settings (`unipress/games/demo_jump/settings.toml`)**:
```toml
# Demo Jump Game Settings
# These override global settings for this specific game

[game]
# This game is easier by default
difficulty = 3

# Keep global lives setting (no override)
# lives will be inherited from global settings

[demo_jump]
# Game-specific settings
obstacle_speed_multiplier = 1.2
jump_height_multiplier = 1.1
```

## Technical Implementation

### Settings Loading Process
```python
def load_settings(game_name: str, **constructor_overrides) -> dict:
    """Load settings with proper priority hierarchy."""
    # 1. Start with default values
    settings = get_default_settings()
    
    # 2. Load global settings
    global_settings = load_toml("unipress/settings.toml")
    settings.update(global_settings)
    
    # 3. Load game-specific settings
    game_settings_path = f"unipress/games/{game_name}/settings.toml"
    if exists(game_settings_path):
        game_settings = load_toml(game_settings_path)
        settings.update(game_settings)
    
    # 4. Apply constructor overrides
    settings.update(constructor_overrides)
    
    return settings
```

### BaseGame Integration
```python
class BaseGame(arcade.Window, ABC, metaclass=GameMeta):
    def __init__(
        self,
        game_name: str,
        width: int = 800,
        height: int = 600,
        title: str = "Unipress Game",
        difficulty: int = None,  # None = use settings
        lives: int = None,       # None = use settings
        **kwargs
    ):
        # Load settings with constructor overrides
        constructor_overrides = {
            k: v for k, v in {"difficulty": difficulty, "lives": lives}.items() 
            if v is not None
        }
        
        self.settings = load_settings(game_name, **constructor_overrides)
        
        # Use settings values
        final_difficulty = self.settings["game"]["difficulty"]
        final_lives = self.settings["game"]["lives"]
        final_fullscreen = self.settings["game"]["fullscreen"]
        
        super().__init__(width, height, title, fullscreen=final_fullscreen)
        # ... rest of initialization
```

## Rationale

### TOML Choice
- **Developer Experience**: Comments allow documentation directly in settings files
- **Type Safety**: Automatic parsing of integers, booleans, and strings
- **Readability**: Much more readable than JSON for configuration
- **Structure**: Supports nested settings while remaining clear
- **Python Ecosystem**: Growing adoption, Python 3.11+ includes tomllib

### Hierarchical Override System
- **Flexibility**: Global defaults with game-specific customization
- **Development**: Easy to test games with different settings
- **Maintenance**: Central place for common settings
- **User Customization**: Future support for user preference files

### File Organization
- **Clear Structure**: Settings co-located with game code
- **Version Control**: Each game's settings tracked with its code
- **Deployment**: Easy to package game-specific configurations

## Dependencies
- **Python 3.11+**: Built-in `tomllib` (read-only)
- **Python < 3.11**: `tomli` package for reading TOML files
- **Future**: `tomli-w` if we need to write TOML files programmatically

## Consequences

### Positive
- **Human Readable**: Easy for developers to edit and understand
- **Type Safe**: Automatic type conversion and validation
- **Documented**: Comments explain each setting's purpose
- **Flexible**: Multiple override levels for different use cases
- **Maintainable**: Clear separation of concerns

### Considerations
- **Dependency**: Requires tomli package for Python < 3.11
- **New Format**: Team may need to learn TOML syntax (minimal learning curve)
- **File Management**: Need to maintain settings files for each game

## Migration Path
1. Add tomli dependency to pyproject.toml
2. Create settings loading module
3. Create global settings file with current defaults
4. Update BaseGame to use settings system
5. Migrate existing games to use settings
6. Create game-specific settings files as needed

## Future Extensions
- Settings validation schemas
- User preference files that override game settings
- Runtime settings modification
- Settings export/import functionality
- GUI settings editor