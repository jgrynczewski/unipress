# Unipress - One-Button Games

[![Documentation Status](https://readthedocs.org/projects/unipress/badge/?version=latest)](https://unipress.readthedocs.io/en/latest/?badge=latest)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-blue?style=flat&logo=github)](https://jgrynczewski.github.io/unipress/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Arcade](https://img.shields.io/badge/Game%20Engine-Arcade-green.svg)](https://arcade.academy/)

A collection of simple, engaging games controlled with just one button. Built with Python and Arcade.

> **Note**: These are true one-button games - players can only send binary signals (click/press) without cursor positioning or element selection. All interactions use timing-based or automatic cycling mechanics.

## 📚 Documentation

### Developer Documentation

- **📚 Read the Docs**: [unipress.readthedocs.io](https://unipress.readthedocs.io/)
- **🔧 API Reference**: [API Documentation](https://unipress.readthedocs.io/en/latest/api/)
- **🏗️ Architecture**: [Architecture Guide](https://unipress.readthedocs.io/en/latest/architecture/)
- **📖 Tutorials**: [Development Tutorials](https://unipress.readthedocs.io/en/latest/tutorials/)

### Local Documentation

To build documentation locally:

```bash
# Install documentation dependencies
uv sync --group dev

# Build documentation
cd docs/sphinx
uv run sphinx-build -b html . _build/html

# View documentation
open _build/html/index.html
```

## 🎮 Available Games

### Demo Jump Game
Simple jumping game where you avoid red obstacles by clicking to jump.
- **Controls**: Left mouse click to jump
- **Difficulty**: 1-10 scale (affects reaction time window)
- **Lives**: 3 lives system - lose a life on collision, keep score
- **Features**: Physics-based jumping, collision detection, scoring, high score tracking

### Jumper Game
Enhanced sprite-based jumping game with animated characters and fire obstacles.
- **Controls**: Left mouse click to jump over fire obstacles
- **Difficulty**: 1-10 scale (affects obstacle speed and jump height)
- **Lives**: 3 lives system with score persistence
- **Features**: 
  - Animated running player character (8-frame sprite animation)
  - Animated fire obstacles (5-frame burning animation)
  - Smooth jumping animation (6-frame sequence)
  - Jump window indicator showing optimal timing
  - 2x sprite scaling for better visibility
  - Physics-based jump mechanics matching demo_jump
  - Professional sound system with 7 different audio events
  - Parallax scrolling background with 5 layers
  - Non-blocking audio with volume control system
- **Assets**: Professional sprite-based graphics with animation metadata + OGG audio files
- **Run**: `uv run python -m unipress.games.jumper.game [difficulty]`

## 🖱️ Game Controls

- **Left Mouse Click**: Primary action (jump, start game, restart, continue after life loss)
- **ESC Key**: Toggle fullscreen mode (for development/testing)
- **Lives System**: 3 lives by default, pause after death with player blinking
- **Difficulty System**: Affects reaction time windows
  - Level 1: 2.0 seconds reaction time (trivial)
  - Level 10: 0.2 seconds reaction time (challenging)
- **Display Mode**: Games start in fullscreen by default (no system bars/menus)
- **Cursor Positioning**: Automatic periodic repositioning to bottom-right corner (prevents cursor drift)
  - Repositions every 3 seconds by default (configurable)
  - Positions at 98% width, 2% height with 2% margin from edges
- **Settings**: Configurable via TOML files (global and per-game)

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

# Run specific games directly (recommended simplest form)
uv run python -m unipress.games.jumper.game 5
uv run python -m unipress.games.demo_jump.game 5
```

## 🐳 Game Server Architecture

The project supports a server-based architecture for faster game launching:

### Architecture Overview

```
┌─────────────────┐    HTTP API    ┌──────────────────┐
│   Python Client │ ──────────────► │  Docker Container │
│   (on host)     │                │  (Game Server)   │
└─────────────────┘                └──────────────────┘
                                           │
                                           ▼
                                    ┌──────────────────┐
                                    │   Arcade Games   │
                                    │  (jumper, demo)  │
                                    └──────────────────┘
```

### Quick Server Setup

```bash
# 1. Build the container
docker build --target runtime -t unipress:latest .

# 2. Start the server
docker compose up game-server -d

# 3. Check server health
curl http://localhost:5000/health

# 4. Run games via CLI
uv run python unipress_cli.py list
uv run python unipress_cli.py run jumper --difficulty 7
uv run python unipress_cli.py status
uv run python unipress_cli.py stop
```

### API Endpoints

- `GET /health` - Server health check
- `GET /games/list` - List available games
- `POST /games/run` - Start a game
- `POST /games/stop` - Stop current game
- `GET /games/status` - Game status

### Python Client

```python
from unipress.client import UnipressClient

client = UnipressClient("http://localhost:5000")
result = client.run_game("jumper", difficulty=8)
completed = client.wait_for_game_completion(timeout=300)
```

## 🐳 Containers (Docker)

### Prerequisites
- Docker and Docker Compose
- Linux desktop with X11 (Wayland works via XWayland; Xorg is often smoother)
- Allow X11 from local containers (once per session):

```bash
xhost +si:localuser:$(whoami)
```

### Build image
```bash
# Build runtime image (recommended for production)
docker build --target runtime -t unipress:latest .

# Build dev image (includes QA checks)
docker build --target dev -t unipress:dev .
```

### Run Game Server (Recommended)

The project now uses a server-based architecture for faster game launching:

```bash
# Start the game server
docker compose up game-server -d

# Check server health
curl http://localhost:5000/health

# Run games via CLI
uv run python unipress_cli.py list
uv run python unipress_cli.py run jumper --difficulty 7
```

### Legacy Direct Game Running (Deprecated)

For direct game execution without the server:

```bash
# Run with Docker Compose (legacy)
docker compose up --build run

# Run specific difficulty
docker compose run --rm run 7

# Run different game directly
docker run --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -v "$(pwd)/high_scores.json:/app/high_scores.json" \
  --device /dev/snd --device /dev/dri \
  --group-add audio \
  --group-add $(getent group video | cut -d: -f3) \
  --group-add $(getent group render | cut -d: -f3) \
  unipress:latest uv run python -m unipress.games.demo_jump.game 5
```

### Audio and GPU Support
- **Audio**: Container maps `/dev/snd` and adds `audio` group. Full PipeWire support for game sound effects.
- **OGG decoding**: Enabled via ffmpeg in the image.
- **GPU**: Mesa DRI drivers included; `/dev/dri` mapped via compose. On NVIDIA, use NVIDIA Container Toolkit and `--gpus all`.
- **Wayland**: If you see DRI3 errors or choppy rendering, try an Xorg session or set `LIBGL_DRI3_DISABLE=1` in compose.

### Troubleshooting
- **Black window / no UI**: Ensure `xhost +si:localuser:$(whoami)` and that `DISPLAY` and `/tmp/.X11-unix` are mounted.
- **"No decoders for .ogg"**: Ensure you use the provided Dockerfile (ffmpeg present).
- **"Permission denied: logs"**: Don't override the container user in compose.
- **GLX/DRI errors or low FPS**: Ensure `/dev/dri` is mapped and host `video`/`render` GIDs are added; try Xorg session.
- **Server not responding**: Check `docker compose logs game-server` and ensure the server is running with `docker compose ps`.

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

[ui]
cursor_reposition_interval = 3.0  # Cursor repositioning frequency (seconds)

[audio]
master_volume = 1.0  # Global volume control
sfx_volume = 0.7     # Sound effects volume
music_volume = 0.5   # Background music volume
ui_volume = 0.6      # UI sound volume

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
- **End Game Screen**: Standardized UI with cycling Play Again/Exit buttons
- **Settings Integration**: TOML-based configuration with per-game overrides
- **Internationalization**: JSON-based messages with Polish default, English fallback
- **Professional Logging**: Structured logging with Loguru, ALL exceptions logged with traceback
- **Sound System**: Professional audio with OGG format, event-based architecture, volume control
- **Base Class**: Inherit from `BaseGame` for standardized structure
- **Professional Code**: Follow ruff linting, type hints, documentation
- **High Score Tracking**: Persistent JSON-based high score storage with automatic new record detection

## 📁 Project Structure

```
unipress/
├── unipress/                 # Main package
│   ├── core/                # Core game framework
│   │   ├── base_game.py     # Base game class with all systems
│   │   ├── settings.py      # TOML-based hierarchical settings
│   │   ├── messages.py      # JSON-based internationalization
│   │   ├── logger.py        # Loguru-based structured logging
│   │   ├── high_scores.py   # JSON-based high score persistence
│   │   ├── sound.py         # Professional sound system with events
│   │   └── assets.py        # Asset management for images and sounds
│   ├── ui/                  # Shared UI components
│   │   └── end_game/        # End game screen component
│   │       └── screen.py    # Standardized end game UI
│   ├── games/               # Individual game implementations
│   │   ├── demo_jump/       # Demo jumping game folder
│   │   │   ├── __init__.py  # Package initialization
│   │   │   ├── game.py      # Game implementation
│   │   │   └── settings.toml # Game-specific settings
│   │   └── jumper/          # Sprite-based jumping game
│   │       ├── __init__.py  # Package initialization
│   │       ├── game.py      # Enhanced game with animations
│   │       └── settings.toml # Game-specific settings
│   ├── locales/             # Internationalization messages
│   │   ├── pl_PL/           # Polish (default)
│   │   └── en_US/           # English (fallback)
│   ├── settings.toml        # Global configuration
│   └── assets/              # Game assets
│       ├── images/          # Sprite graphics and animations
│       │   └── games/       # Per-game asset organization
│       │       └── jumper/  # Jumper game sprites
│       │           ├── player/      # Player animations
│       │           └── obstacles/   # Fire obstacle animations
│       └── sounds/          # OGG audio files
│           ├── global/      # Shared sounds across all games
│           └── games/       # Per-game sound organization
│               └── jumper/  # Jumper game specific sounds
├── logs/                    # Log files (auto-created)
├── high_scores.json         # High score storage (auto-created)
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
- **Sound System**: Professional audio with OGG format, event categories, volume control
- **Difficulty System**: Standardized 1-10 scale affecting gameplay timing
- **Lives System**: 3-lives with pause-after-death and score persistence
- **Input Abstraction**: Configurable input handling (default: left mouse click)
- **High Score System**: JSON-based persistent high score tracking per game

### System Documentation (UML Diagrams)

The project includes comprehensive UML documentation using PlantUML to visualize system architecture:

#### Available Diagrams
- **Architecture Overview** (`docs/uml/ArchitectureOverview.png`) - High-level system architecture showing component relationships
- **Game Lifecycle** (`docs/uml/GameLifecycle.png`) - Sequence diagram for game launch to completion
- **Class Hierarchy** (`docs/uml/ClassHierarchy.png`) - Detailed class diagram with inheritance and composition
- **Deployment Diagram** (`docs/uml/DeploymentDiagram.png`) - System deployment across containers and nodes
- **Data Flow** (`docs/uml/DataFlow.png`) - Activity diagram showing data processing patterns

#### Generating Diagrams
```bash
# Generate all diagrams (requires PlantUML and Java)
plantuml -tpng docs/uml/*.puml

# Generate specific diagram
plantuml -tpng docs/uml/architecture-overview.puml

# Generate SVG format
plantuml -tsvg docs/uml/*.puml
```

#### Diagram Conventions
- **Theme**: Plain theme for clean, professional appearance
- **Background**: White background for consistency
- **Font**: Arial, 11-12pt for readability
- **Colors**: Minimal color usage, focus on clarity
- **Naming**: PascalCase for classes, snake_case for methods/variables

#### Maintenance
- Diagrams are version-controlled as `.puml` text files
- Update diagrams when adding new features or changing architecture
- Generated images are included in documentation releases
- All diagrams follow consistent styling and naming conventions

### Architecture Decision Records (ADRs)
The project maintains detailed Architecture Decision Records in [docs/adr/](docs/adr/) documenting key technical decisions:

#### Key Decisions
- **ADR-001**: Dependency Management with `uv` (fast, modern package manager)
- **ADR-002**: Game Framework using `arcade` (clean API, modern Python)
- **ADR-004**: Game Design Standards (one-button constraint, difficulty system)
- **ADR-010**: TOML-based Settings System (hierarchical configuration)
- **ADR-011**: JSON-based Internationalization (Polish default, English fallback)
- **ADR-012**: Loguru-based Logging System (structured, professional)
- **ADR-013**: Asset Management System (sprites, sounds, animations)
- **ADR-016**: Comprehensive Sound System (OGG format, event-based)
- **ADR-017**: Docker Containerization (multi-stage builds, audio support)
- **ADR-018**: HTTP Server Architecture (Flask-based game management)

#### ADR Benefits
- **Transparency**: All major decisions documented with rationale
- **Consistency**: Ensures architectural coherence across the project
- **Onboarding**: New developers can understand design decisions quickly
- **Maintenance**: Clear reasoning for technology choices and patterns
- **Evolution**: Track how architecture decisions evolve over time

### Game Framework Features
- Consistent difficulty scaling across all games
- Standardized game lifecycle (start, update, draw, reset)
- Common UI elements (score, lives, difficulty indicator)
- Standardized end game screen with cycling Play Again/Exit buttons
- Automatic fullscreen mode with ESC toggle
- Professional sound system with event-based audio and volume control
- Professional logging for all game events, player actions, and errors
- Complete internationalization support for all user-facing text
- Shared UI components with per-game customization capability
- Professional code structure with type hints and comprehensive documentation
- Persistent high score tracking with automatic record detection and display

## 🤝 Contributing

## 🔄 Git Flow

### Branching Strategy
We use a **GitHub Flow** variant optimized for small teams:

#### Branch Types
- **`master`** - Main production branch, always deployable
- **`feat/*`** - Feature branches for new functionality
- **`fix/*`** - Bug fix branches for critical issues
- **`chore/*`** - Maintenance and tooling changes
- **`docs/*`** - Documentation updates
- **`release/*`** - Release preparation branches

#### Workflow Rules
1. **Direct to master** - Features merge directly to master via pull requests
2. **Pull request required** - All changes must go through review
3. **Squash merging** - Use squash merge to keep history clean
4. **Branch protection** - Master branch is protected with required reviews and CI checks

### Commit Standards
We use conventional commits with git-cz emojis:
- `feat: 🎸` - New features
- `fix: 🐛` - Bug fixes
- `docs: ✏️` - Documentation
- `chore: 🤖` - Build/tool changes
- `refactor: 💡` - Code refactoring
- `test: 💍` - Adding or updating tests
- `style: 💄` - Code style changes (formatting, etc.)
- `perf: ⚡` - Performance improvements
- `release: 🏹` - Create a release commit
- `ci: 🎡` - CI/CD changes

### Development Workflow
1. **Create feature branch** from master: `git checkout -b feat/new-feature`
2. **Make changes** with conventional commits: `git commit -m "feat: 🎸 add new game feature"`
3. **Push branch** and create pull request
4. **Address review feedback** if needed
5. **Merge via squash merge** to keep history clean
6. **Delete feature branch** after merge

### Branch Protection
- ✅ Require pull request reviews
- ✅ Require status checks to pass (CI pipeline)
- ✅ Require up-to-date branches before merging
- ✅ Restrict direct pushes to master
- ✅ Enable squash merging as default

### Quick Commands
```bash
# Start new feature
git checkout master
git pull origin master
git checkout -b feat/new-feature

# Make changes and commit
git add .
git commit -m "feat: 🎸 add new game feature"

# Push and create PR
git push origin feat/new-feature
# Then create PR on GitHub

# After merge, clean up
git checkout master
git pull origin master
git branch -d feat/new-feature
```

## 📄 License

GNU General Public License v3.0 - See LICENSE file for details

This project is licensed under the GNU GPL v3, which ensures that:
- The software remains free and open source
- Derivative works must also be open source (copyleft)
- Users have the freedom to use, modify, and distribute the software
- All modifications must be shared under the same license