# Unipress - One-Button Games Project

## Project Overview
- **Name**: Unipress
- **Purpose**: Collection of games controlled with a single button
- **Language**: Python
- **Target**: Professional code quality with best practices

## 🔴 FUNDAMENTAL DESIGN PRINCIPLE (CRITICAL)
**ONE-BUTTON INPUT ONLY**: Players can ONLY send a binary signal (click/press). They CANNOT:
- Move or aim cursors
- Select specific UI elements
- Target specific screen areas
- Use precise positioning

ALL game mechanics and UI must work with timing-based or automatic cycling interactions, never requiring cursor positioning or direct element selection. This is the core constraint that defines every aspect of game design.

## Current Status
- ✅ Project setup complete with professional structure
- ✅ Demo game implemented with all systems integrated
- ✅ Jumper game implemented with sprite animations and enhanced features
- ✅ Asset management system with animation metadata support
- ✅ GitHub repository created and CI/CD pipeline active
- ✅ All code quality checks passing (ruff, mypy, pytest)
- ✅ Fullscreen mode with ESC toggle implemented
- ✅ 3-lives system with pause-after-death mechanics
- ✅ TOML settings system with hierarchical configuration
- ✅ Player blinking effect on life loss  
- ✅ Jump window indicator showing optimal timing
- ✅ High score system with persistent JSON storage
- ✅ Comprehensive sound system with professional audio events
- ✅ Parallax scrolling backgrounds with responsive positioning
- ✅ UI styling with clean black text on light backgrounds

## Communication Protocol
- **User writes in Polish or English** 
- **Assistant responds in English only**
- **All code, comments, and documentation in English**

### Assistant Action Approval Policy (MANDATORY)
To ensure full user control and transparency, the assistant MUST follow this approval policy for EVERY action (including read-only tool calls, code edits, commands, and configuration changes):

- Before executing any action, present a short proposal containing:
  - Intent: one-sentence summary of what will be done and why
  - Exact steps: list of commands to run (verbatim) and/or files to edit
  - File edits: precise description per file; when possible, include a minimal diff/edits preview
  - Risks/Side-effects: brief note (e.g., may restart app, long-running, modifies state)
- Wait for explicit user approval before proceeding. Accepted approval phrases: "Approve", "Proceed", or "OK" (case-insensitive). No action should be taken without this approval.
- If the plan changes meaningfully after approval, re-propose the updated steps and request approval again.
- Batch small actions into a single proposal when appropriate to reduce approval overhead, but keep steps explicit and reviewable.
- If blocked or uncertain, ask a clarifying question instead of guessing.

Exceptions: None by default. Even read-only diagnostics should be proposed first unless the user explicitly grants a temporary exception.

## Key Decisions (ADRs)
1. **Dependency Management**: ✅ uv (fast, modern)
2. **Game Framework**: ✅ arcade (clean API, modern)
3. **Development Tools**: ✅ ruff + pytest (fast linting/formatting + flexible testing)
4. **Game Design Standards**: ✅ Unified difficulty (1-10) + left mouse click input
5. **Commit Standards**: ✅ Conventional commits with git-cz emojis
6. **Type Checking**: ✅ mypy (industry standard, mature)
7. **CI/CD Pipeline**: ✅ GitHub Actions (automatic CI, manual deployment)
8. **Fullscreen Display**: ✅ Games start fullscreen by default with ESC toggle
9. **Lives System**: ✅ 3-lives with pause-after-death and score persistence
10. **Settings System**: ✅ TOML-based hierarchical configuration
11. **Internationalization**: ✅ JSON-based with Polish default, English fallback
12. **Logging System**: ✅ Loguru-based with structured JSON logging
13. **End Game Screen**: ✅ Standardized UI with cycling Play Again/Exit buttons
14. **Responsive Positioning**: ✅ Game objects scale with window size changes (fullscreen toggle)
15. **AI Development Tools**: ✅ Claude Code selected for development assistance (ADR-015)
16. **Sound System**: ✅ Comprehensive audio with OGG format and event-based architecture (ADR-016)

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

### Input Standard (ONE-BUTTON ONLY)
- **Primary**: Left mouse button click (binary signal only)
- **Constraint**: NO cursor positioning, targeting, or selection allowed
- **Requirement**: All interactions via timing, cycling, or automatic systems
- **Implementation**: Abstracted input handling for binary signals only

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

### Internationalization System (i18n)
- **Format**: JSON message files with dot notation access (e.g., "ui.score")
- **Default Language**: Polish (pl_PL) with English (en_US) fallback
- **Message Files**: `unipress/locales/{language}/common.json` and `games/{game}.json`
- **Integration**: Built into BaseGame via `get_message(key, **kwargs)` method
- **Settings**: Configurable via `ui.language` in TOML settings
- **Parameters**: Support for variable substitution (e.g., score={score})

### Logging System (Professional-grade)
- **Library**: Loguru for structured logging with simple API
- **Configuration**: TOML-based settings with hierarchical overrides
- **Formats**: JSON for production/files, human-readable for development console
- **Levels**: DEBUG/INFO/WARNING/ERROR/CRITICAL with configurable filtering
- **Rotation**: Size-based (10MB) with 30-day retention and gzip compression
- **Exception Rule**: **ALL exceptions MUST be logged with full traceback**
- **Game Events**: Structured logging for player actions, game events, performance metrics
- **Files**: Logs stored in `logs/unipress-{date}.log` with automatic cleanup
- **Integration**: Built into BaseGame and all components

### End Game Screen (Standardized UI)
- **Component**: Shared UI component in `unipress/ui/end_game/screen.py`
- **Buttons**: Two cycling options - "Play Again" and "Exit"  
- **Interaction**: Click cycles between buttons, selected button highlighted
- **Actions**: Play Again restarts game, Exit closes application
- **Visuals**: Professional overlay with semi-transparent background
- **Localization**: Fully internationalized with Polish/English support
- **Customization**: Foundation for per-game asset overrides (future)
- **Integration**: Automatically displayed when all lives lost

### Sound System (Professional Audio)
- **Architecture**: Comprehensive sound system with event-based audio (ADR-016)
- **Format**: OGG Vorbis files only (cross-platform compatibility, patent-free)
- **Categories**: 7 sound event types - game_start, player_action, success, failure, achievement, ui_feedback, ambient
- **Volume Control**: 4-level hierarchy (master, sfx, music, ui) with per-event multipliers
- **File Organization**: 
  - Global sounds: `unipress/assets/sounds/global/` (shared across games)
  - Game-specific: `unipress/assets/sounds/games/{game_name}/` (per-game sounds)
- **Sound Events**: Standardized events (game_start.ogg, jump.ogg, success.ogg, failure.ogg, etc.)
- **Integration**: Built into BaseGame with `play_sound_event(event_name)` method
- **Performance**: Sound caching, lazy loading, optional preloading for better performance
- **Settings**: Full TOML configuration with hierarchical volume control
- **Non-blocking Audio**: Games wait for sound completion without freezing gameplay
- **Error Handling**: Graceful degradation when sound files missing
- **Implementation**: `unipress/core/sound.py` with full SoundManager class
- **Usage**: Active in jumper game with 7 different sound events
- **Status**: ✅ Complete and fully implemented with professional-grade features

### Code Standards
- **Import Style**: Always use absolute imports (e.g., `from unipress.core.base_game import BaseGame`)
- **Never use relative imports** (no `from .module` or `from ..module`)
- **Rationale**: Absolute imports are clearer, more maintainable, and avoid path confusion

### Structure Requirements
- Inherit from BaseGame class with `game_name` parameter
- Support difficulty scaling in reaction time windows  
- Configurable input handling (left mouse click default)
- Fullscreen display by default with ESC toggle
- 3-lives system with pause-after-death and score persistence
- TOML settings integration for all configurable parameters
- Internationalization support for all user-facing text
- Professional logging throughout with structured events
- Standardized end game screen with cycling Play Again/Exit buttons
- Responsive positioning system that scales with window size changes
- Physics-based obstacle spacing with safety margins (ADR-014)
- Sound event integration with professional audio feedback

## Development Commands
- `uv sync` - Install/sync dependencies
- `uv run ruff check` - Run linting
- `uv run ruff format` - Format code
- `uv run mypy unipress` - Run type checking
- `uv run pytest` - Run tests
- `uv run python main.py [difficulty]` - Run demo game
- `uv run python -m unipress.games.GAMENAME.game` - Run specific game
- `PYTHONPATH=/path/to/project uv run python unipress/games/jumper/game.py` - Run jumper game directly

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
1. **Complete features first** - Always commit and push finished feature before starting new work
2. **Immediate commit** - Create atomic commits with proper git-cz format after EACH completed change (feat, fix, docs, chore, etc.)
3. **Push immediately** - Push all commits to GitHub repository after committing
4. **Separate commits** - Never bundle unrelated changes (especially different fixes) into one commit
5. **User confirmation** - Only proceed to next major task after user confirmation
6. **Single author** - Commits should only show user as author, NEVER add co-author lines or Claude attribution

**Example**: If fixing 2 unrelated bugs, create 2 separate commits and push both immediately.

## Available Games

### Demo Jump Game (demo_jump)
- **Purpose**: Reference implementation demonstrating core game framework
- **Features**: Basic geometric sprites, physics-based jumping, collision detection
- **Assets**: Geometric shapes (rectangles) with color coding
- **Jump Window**: Visual indicator showing optimal timing for obstacle clearance
- **Status**: Complete and serving as development reference

### Jumper Game (jumper) 
- **Purpose**: Enhanced sprite-based jumping game with professional assets
- **Features**: 
  - Animated running player character (8-frame sprite sequence)
  - Animated fire obstacles (5-frame burning animation) 
  - Smooth jumping animation (6-frame sequence synchronized with physics)
  - Jump window indicator matching demo_jump functionality
  - 2x sprite scaling for better visibility
  - Asset management system with JSON animation metadata
  - Comprehensive sound system with 7 different audio events (jump, success, failure, high score, etc.)
  - Full parallax scrolling background with 5 layers (sky, mountains, far trees, near trees, ground)
  - Responsive positioning system - game objects scale properly with window resize
  - Physics-based obstacle spacing synchronized with ground layer movement
  - Non-blocking audio system with game startup sound delays
- **Assets**: Professional sprite graphics with frame-by-frame animations + OGG audio files
- **Physics**: Identical mechanics to demo_jump for consistent difficulty
- **Animation System**: JSON-based metadata with precise timing synchronization
- **Sound System**: Full implementation of professional audio events with volume control
- **Status**: Complete with sprite animations, parallax backgrounds, responsive scaling, and professional sound

## Asset Management System
- **Structure**: Organized by game in `unipress/assets/images/games/{game_name}/` and `unipress/assets/sounds/`
- **Animation Format**: JSON metadata files with frame sequences, durations, and hitboxes
- **Sound Format**: OGG Vorbis files organized by event categories and games
- **Asset Loading**: Lazy loading with caching for performance (images and sounds)
- **Sound Support**: Complete implementation with global and per-game audio assets
- **Scaling**: Configurable sprite scaling (currently 2x for better visibility)
- **Audio Organization**: Global sounds + game-specific sounds with proper directory structure
- **Documentation**: Full ADRs in `docs/adr/013-asset-management-system.md` and `docs/adr/016-comprehensive-sound-system.md`

## Next Steps
- Add more one-button games with different mechanics
- Implement comprehensive testing for asset system and sound system
- Create game launcher/menu system with sound effects
- Consider procedural background generation for variety
- Expand sound library with more audio assets
- Add music background tracks for ambient category