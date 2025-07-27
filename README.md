# Unipress - One-Button Games

A collection of simple, engaging games controlled with just one button. Built with Python and Arcade.

## 🎮 Available Games

### Demo Jump Game
Simple jumping game where you avoid red obstacles by clicking to jump.
- **Controls**: Left mouse click to jump
- **Difficulty**: 1-10 scale (affects reaction time window)
- **Lives**: 3 lives system - lose a life on collision, keep score
- **Features**: Physics-based jumping, collision detection, scoring

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation & Running

```bash
# Clone the repository
git clone https://github.com/jgrynczewski/unipress.git
cd unipress

# Install dependencies
uv sync

# Run demo game (default difficulty: 5)
uv run python main.py

# Run with specific difficulty (1=easy, 10=hard)
uv run python main.py 1   # Easy: 2.0s reaction time
uv run python main.py 10  # Hard: 0.2s reaction time
```

### Game Controls
- **Left Mouse Click**: Primary action (jump, start game, restart, continue after life loss)
- **ESC Key**: Toggle fullscreen mode (for development/testing)
- **Lives System**: 3 lives by default, pause after death with player blinking
- **Difficulty System**: Affects reaction time windows
  - Level 1: 2.0 seconds reaction time (trivial)
  - Level 10: 0.2 seconds reaction time (challenging)
- **Display Mode**: Games start in fullscreen by default (no system bars/menus)
- **Settings**: Configurable via TOML files (global and per-game)

## ⚙️ Configuration

### Settings System
Games use TOML files for configuration with hierarchical priority:

1. **Constructor parameters** (highest priority)
2. **Game-specific settings**: `unipress/games/{game_name}/settings.toml`
3. **Global settings**: `unipress/settings.toml`
4. **Default values** (lowest priority)

Example game-specific settings:
```toml
[game]
difficulty = 3  # Override global difficulty
lives = 5       # Override global lives count

[demo_jump]
obstacle_speed_base = 100
jump_height_base = 150
```

## 🛠️ Development

This project uses modern Python tooling and follows professional standards:
- **uv** for fast dependency management
- **arcade** for clean 2D game development  
- **ruff** for linting and formatting
- **pytest** for testing
- **mypy** for type checking
- **TOML** for human-readable configuration
- **JSON** for internationalization messages
- **Loguru** for structured logging
- **Conventional commits** with git-cz emojis

### Development Setup

```bash
# Install dependencies (including dev tools)
uv sync

# Run linting
uv run ruff check

# Auto-format code
uv run ruff format

# Run tests
uv run pytest

# Run all checks (recommended before commits)
uv run ruff check && uv run ruff format && uv run pytest
```

### Game Development Standards

All games must follow these design principles:
- **Unified Difficulty**: 1-10 scale affecting reaction time windows
- **Consistent Input**: Left mouse click (configurable)
- **Fullscreen Display**: Games start in fullscreen mode by default
- **Lives System**: 3 lives with pause-after-death and score persistence
- **Settings Integration**: TOML-based configuration with per-game overrides
- **Internationalization**: JSON-based messages with Polish default, English fallback
- **Professional Logging**: Structured logging with Loguru, ALL exceptions logged with traceback
- **Base Class**: Inherit from `BaseGame` for standardized structure
- **Professional Code**: Follow ruff linting, type hints, documentation

## 📁 Project Structure

```
unipress/
├── unipress/                 # Main package
│   ├── core/                # Core game framework
│   │   ├── base_game.py     # Base game class with all systems
│   │   ├── settings.py      # TOML-based hierarchical settings
│   │   ├── messages.py      # JSON-based internationalization
│   │   └── logger.py        # Loguru-based structured logging
│   ├── games/               # Individual game implementations
│   │   └── demo_jump/       # Demo jumping game folder
│   │       ├── __init__.py  # Package initialization
│   │       ├── game.py      # Game implementation
│   │       └── settings.toml # Game-specific settings
│   ├── locales/             # Internationalization messages
│   │   ├── pl_PL/           # Polish (default)
│   │   └── en_US/           # English (fallback)
│   ├── settings.toml        # Global configuration
│   └── assets/              # Game assets (future: images, sounds)
├── logs/                    # Log files (auto-created)
├── tests/                   # Test suite
├── docs/                    # Documentation
│   └── adr/                 # Architecture Decision Records
├── main.py                  # Main entry point
├── pyproject.toml          # Project configuration
└── CLAUDE.md               # Development context and decisions
```

## 🏗️ Architecture

### Core Components
- **BaseGame**: Abstract base class providing all standardized systems
- **Settings System**: TOML-based hierarchical configuration (global → game → constructor)
- **Internationalization**: JSON message files with Polish default, English fallback
- **Logging System**: Structured Loguru logging with automatic rotation and exception tracking
- **Difficulty System**: Standardized 1-10 scale affecting gameplay timing
- **Lives System**: 3-lives with pause-after-death and score persistence
- **Input Abstraction**: Configurable input handling (default: left mouse click)

### Game Framework Features
- Consistent difficulty scaling across all games
- Standardized game lifecycle (start, update, draw, reset)
- Common UI elements (score, lives, difficulty indicator, game over screen)
- Automatic fullscreen mode with ESC toggle
- Professional logging for all game events, player actions, and errors
- Complete internationalization support for all user-facing text
- Professional code structure with type hints and comprehensive documentation

## 🤝 Contributing

### Commit Standards
We use conventional commits with git-cz emojis:
- `feat: 🎸` - New features
- `fix: 🐛` - Bug fixes
- `docs: ✏️` - Documentation
- `chore: 🤖` - Build/tool changes

### Development Workflow
1. Create feature branch
2. Follow game design standards
3. Add tests for new functionality
4. Ensure all checks pass (`ruff check && ruff format && pytest`)
5. Use conventional commit messages
6. Create pull request

### Architecture Decision Records
See [docs/adr/](docs/adr/) for detailed project decisions including:
- Technology choices (uv, arcade, ruff)
- Game design standards
- Development tooling
- Commit message format

## 📄 License

MIT License - See LICENSE file for details