# ADR-001: Use uv for Dependency Management

## Status
Accepted

## Context
We need to choose a dependency management tool for the Unipress project. The main options are:
- **uv**: New, extremely fast package manager written in Rust
- **poetry**: Mature, popular dependency management tool
- **pipenv**: Official Python packaging authority recommended tool

## Decision
We will use **uv** for dependency management.

## Rationale
- **Performance**: uv is significantly faster than alternatives (10-100x faster)
- **Modern**: Built with modern Python packaging standards in mind
- **Simplicity**: Clean, intuitive CLI interface
- **Future-proof**: Rapidly becoming the new standard in Python ecosystem
- **Compatibility**: Works well with existing Python packaging ecosystem

## Consequences
- Faster dependency resolution and installation
- Modern project configuration
- May require team members to install uv (but it's easy)
- Less mature ecosystem compared to poetry, but rapidly growing

## Implementation
- Use `uv init` to initialize project
- Use `uv add` for adding dependencies
- Use `uv run` for running scripts
- Use `uv sync` for installing dependencies