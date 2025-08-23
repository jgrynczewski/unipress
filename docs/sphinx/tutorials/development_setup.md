# Development Setup

## Overview

This guide covers setting up a development environment for contributing to Unipress.

## Prerequisites

- Python 3.12+
- uv package manager
- Git
- Code editor (VS Code, PyCharm, etc.)

## Development Installation

```bash
# Clone the repository
git clone https://github.com/jgrynczewski/unipress.git
cd unipress

# Install development dependencies
uv sync --group dev

# Install pre-commit hooks
uv run pre-commit install
```

## Development Tools

### Code Quality
- **Ruff**: Linting and formatting
- **MyPy**: Type checking
- **Pytest**: Testing framework

### Commands
```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy unipress/

# Run tests
uv run pytest tests/
```

## Project Structure

```
unipress/
├── core/           # Core framework
├── games/          # Game implementations
├── assets/         # Game assets
├── docs/           # Documentation
├── tests/          # Test suite
└── unipress_cli.py # Command line interface
```

## Development Planning

### When to Create Plans
Create formal development plans for:
- **Major Features**: New games, system enhancements
- **Architecture Changes**: Core system modifications
- **Tool Adoption**: New development tools or frameworks
- **Process Changes**: Workflow or quality standard updates

### Plan Management Workflow

```bash
# 1. Create plan document
touch docs/plans/YYYY-MM-DD-plan-name.md

# 2. Write plan following template in docs/plans/README.md
# Include: Executive Summary, Phases, Metrics, Risks, Resources

# 3. Update plan status in docs/plans/README.md
# Status: Draft → Approved → In Progress → Completed/Cancelled

# 4. Reference plan in related ADRs and TODO.md updates
```

### Claude Code Development Tools

Essential slash commands for Unipress development:

```bash
# Start new feature with proper Git Flow
/git-start feat new-feature-name

# Run complete quality assurance pipeline  
/qa

# Generate test coverage report and identify gaps
/test-coverage

# Scaffold new game with proper structure
/new-game puzzle_challenge
```

### Git Flow Requirements

All development work must follow Git Flow standards:

1. **Start from master**: Always create branches from updated master
2. **Proper naming**: Use `feat/`, `fix/`, `docs/`, `chore/` prefixes
3. **Conventional commits**: Use git-cz format with emojis
4. **Quality checks**: All commits must pass `/qa` pipeline
5. **Pull requests**: All changes require PR review before merge

## Contributing

1. Fork the repository
2. Follow Git Flow: create properly named feature branch
3. Create development plan if needed (major changes)
4. Make your changes following coding standards
5. Run `/qa` command to validate quality
6. Submit a pull request with plan reference (if applicable)

## Next Steps

- Read [Contributing Guide](contributing.md) for detailed guidelines
- Check [Development Standards](development_standards.md) for coding standards
- Review [Architecture Overview](../architecture/overview.md) for system design
