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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Next Steps

- Read [Contributing Guide](contributing.md) for detailed guidelines
- Check [Development Standards](development_standards.md) for coding standards
- Review [Architecture Overview](../architecture/overview.md) for system design
