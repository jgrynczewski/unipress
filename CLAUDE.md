# Unipress - One-Button Games Project

## Project Overview
- **Name**: Unipress
- **Purpose**: Collection of games controlled with a single button
- **Language**: Python
- **Target**: Professional code quality with best practices

## Current Status
- ✅ Project setup complete with professional structure
- ✅ Demo game implemented with difficulty system
- Ready for GitHub repository creation

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

### Structure Requirements
- Inherit from BaseGame class
- Support difficulty scaling in reaction time windows
- Configurable input handling

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
**Important**: After completing any medium/large change and receiving user approval:
1. Create atomic commits with proper git-cz format
2. Push changes to GitHub repository
3. Only proceed to next task after user confirmation

## Next Steps
- Add more one-button games with sprites and sounds
- Implement comprehensive testing
- Add CI/CD pipeline
- Create game launcher/menu system