# Unipress - One-Button Games Project

## Project Overview
- **Name**: Unipress
- **Purpose**: Collection of games controlled with a single button
- **Language**: Python
- **Target**: Professional code quality with best practices

## Current Status
- ✅ Project setup complete with professional structure
- ✅ Demo game implemented with all systems integrated
- ✅ GitHub repository created and CI/CD pipeline active
- ✅ All code quality checks passing (ruff, mypy, pytest)
- ✅ Fullscreen mode with ESC toggle implemented
- ✅ 3-lives system with pause-after-death mechanics
- ✅ TOML settings system with hierarchical configuration
- ✅ Player blinking effect on life loss
- ✅ Jumper game created as demo copy (needs updates)

## Communication Protocol
- **User writes in Polish or English** 
- **Assistant responds in English only**
- **All code, comments, and documentation in English**

## Key Decisions (ADRs)
1. **Dependency Management**: ✅ uv (fast, modern)
2. **Game Framework**: ✅ arcade (clean API, modern)
3. **Development Tools**: ✅ ruff + pytest (fast linting/formatting + flexible testing)
4. **Game Design Standards**: ✅ Unified difficulty (1-10) + left mouse click input
5. **Commit Standards**: ✅ Conventional commits with git-cz emojis
6. **Type Checking**: ✅ mypy (industry standard, mature)
7. **CI/CD Pipeline**: ✅ GitHub Actions (automatic CI, manual deployment)

## Commit Standards (git-cz)
**Format**: `type(scope): emoji subject` (space after emoji)

**Types & Emojis**:
- `chore: 🤖 Build/tool changes`
- `feat: 🎸 New features`  
- `fix: 🐛 Bug fixes`
- `docs: ✏️ Documentation`
- `style: 💄 Code formatting`
- `refactor: 💡 Code restructuring`
- `test: 💍 Adding tests`
- `perf: ⚡️ Performance improvements`
- `ci: 🎡 CI changes`

**Example**: `feat: 🎸 add new jumping mechanics`

**IMPORTANT COMMIT POLICY**: 
- **Separate commits for unrelated changes** - especially for different bug fixes
- Each commit should address ONE logical change or fix
- Never bundle unrelated fixes into a single commit

Reference: https://www.npmjs.com/package/git-cz#custom-config

## Game Design Standards
**All games must follow these rules:**

### Difficulty System (1-10 scale)
- **1**: Trivial - longest reaction time window
- **10**: Hard but fair - shortest reaction time window
- **Implementation**: Each game adjusts reaction time based on difficulty level
- **Configuration**: `difficulty` parameter in game constructor

### Input Standard
- **Primary**: Left mouse button click
- **Requirement**: Input method easily configurable
- **Implementation**: Abstracted input handling

### Display Standard
- **Fullscreen**: Games start in fullscreen mode by default (no system bars/menus)
- **Escape Key**: ESC toggles fullscreen mode for development/testing
- **Implementation**: Built into BaseGame class

### Lives System
- **Default Lives**: 3 lives per game (configurable via settings or constructor)
- **Life Loss**: Each failure/death loses 1 life and enters pause state
- **Pause After Death**: Game freezes, all objects stop, player blinks red/invisible for 1 second
- **Click to Continue**: After blinking, player must click to restart game state
- **Score Persistence**: Score maintained across life losses within same session
- **Game Over**: Final game over only when all lives exhausted
- **Methods**: Use `lose_life()` instead of `end_game()` for proper behavior
- **Implementation**: Built into BaseGame with life_lost_pause state

### Settings System (TOML-based)
- **Format**: TOML files for human-readable configuration with comments
- **Hierarchy**: Constructor params > Game settings > Global settings > Hardcoded defaults
- **Global Settings**: `unipress/settings.toml` - shared defaults for all games
- **Game Settings**: `unipress/games/{game_name}/settings.toml` - per-game overrides
- **Constructor**: `BaseGame(game_name, difficulty=None, lives=None, fullscreen=None)`
- **Available Settings**: difficulty (1-10), lives (int), fullscreen (bool), blink_duration (float)
- **Loading**: Automatic via `load_settings()` with recursive merge
- **Access**: `get_setting(settings, "game.difficulty", default=5)` dot notation
- **Implementation**: `unipress/core/settings.py` with tomli dependency

### Structure Requirements
- Inherit from BaseGame class with `game_name` parameter
- Support difficulty scaling in reaction time windows  
- Configurable input handling (left mouse click default)
- Fullscreen display by default with ESC toggle
- 3-lives system with pause-after-death and score persistence
- TOML settings integration for all configurable parameters

## Development Commands
- `uv sync` - Install/sync dependencies
- `uv run ruff check` - Run linting
- `uv run ruff format` - Format code
- `uv run mypy unipress` - Run type checking
- `uv run pytest` - Run tests
- `uv run python main.py [difficulty]` - Run demo game
- `uv run python -m unipress.games.GAMENAME` - Run specific game

## Quality Assurance Pipeline
**Pre-commit checks** (run all before committing):
```bash
uv run ruff check && uv run ruff format && uv run mypy unipress && uv run pytest
```

**CI/CD Pipeline**:
- **Automatic**: Tests, linting, formatting, type checking on every push/PR
- **Manual Deployment**: Trigger via GitHub Actions "Run workflow" button
- **Requirements**: All tests must pass before deployment is allowed

## Development Workflow
**MANDATORY WORKFLOW**: 
1. **Immediate commit** - Create atomic commits with proper git-cz format after EACH completed change (feat, fix, docs, chore, etc.)
2. **Push immediately** - Push all commits to GitHub repository after committing
3. **Separate commits** - Never bundle unrelated changes (especially different fixes) into one commit
4. **User confirmation** - Only proceed to next major task after user confirmation
5. **Single author** - Commits should only show user as author, NEVER add co-author lines or Claude attribution

**Example**: If fixing 2 unrelated bugs, create 2 separate commits and push both immediately.

## Next Steps
- Add more one-button games with sprites and sounds
- Implement comprehensive testing
- Add CI/CD pipeline
- Create game launcher/menu system