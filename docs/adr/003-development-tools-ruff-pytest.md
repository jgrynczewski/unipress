# ADR-003: Use Ruff and Pytest for Development Tools

## Status
Accepted

## Context
We need to choose development tools for code quality and testing:

**Linting & Formatting Options:**
- **ruff**: Modern, fast Rust-based tool (all-in-one)
- **black + flake8**: Traditional, mature combination
- **black + pylint**: More detailed analysis
- **autopep8 + flake8**: Older stack

**Testing Options:**
- **pytest**: Modern, flexible testing framework
- **unittest**: Built-in Python testing
- **nose2**: Legacy alternative

## Decision
We will use **Ruff** for linting and formatting, and **pytest** for testing.

## Rationale

### Ruff
- **Performance**: 10-100x faster than flake8/black combination
- **All-in-one**: Single tool for both linting and formatting
- **Modern**: Built for modern Python, supports latest features
- **Compatibility**: Drop-in replacement for flake8/black
- **Future-proof**: Rapidly becoming the new standard in Python ecosystem
- **Simpler config**: Less configuration overhead
- **Fast CI/CD**: Significantly reduces build times

### Pytest
- **Flexibility**: Simple syntax, powerful features
- **Fixtures**: Excellent dependency injection system
- **Plugins**: Rich ecosystem of plugins
- **Assertions**: Clear, readable assertion failures
- **Industry standard**: Widely adopted in Python community

## Consequences
- Much faster linting and formatting (important for CI/CD)
- Single tool to learn instead of multiple
- Modern Python development practices
- Potential learning curve for teams used to black+flake8
- Excellent test organization and maintainability

## Implementation
- Use `uv add --dev ruff pytest` to install
- Configure ruff in `pyproject.toml`
- Use `uv run ruff check` for linting
- Use `uv run ruff format` for formatting
- Use `uv run pytest` for testing