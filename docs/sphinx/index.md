# Unipress Documentation

Welcome to the Unipress documentation! Unipress is a collection of one-button games built with Python and the Arcade framework.

> **Note**: This documentation is also available on [Read the Docs](https://unipress.readthedocs.io/) and [GitHub Pages](https://jgrynczewski.github.io/unipress/).

## 🎮 What is Unipress?

Unipress is a professional-grade game development framework that focuses on **one-button games** - games where players can only send binary signals (click/press) without cursor positioning or element selection. All interactions use timing-based or automatic cycling mechanics.

### Key Features

- **One-Button Constraint**: All games work with single button input only
- **Professional Architecture**: Modern Python development with best practices
- **Extensible Framework**: Easy to add new games with consistent structure
- **Comprehensive Systems**: Settings, sound, logging, internationalization
- **Container Support**: Docker-based deployment with audio/GPU support
- **HTTP Server**: API-based game management for scalable deployment

## 📚 Documentation Sections

### Getting Started
- [Installation Guide](tutorials/installation.md) - How to install and set up Unipress
- [Quick Start](tutorials/quick_start.md) - Run your first game in minutes
- [Development Setup](tutorials/development_setup.md) - Set up development environment

### Game Development
- [Creating Your First Game](tutorials/first_game.md) - Step-by-step guide to creating a new game
- [Game Design Standards](tutorials/game_design.md) - Understanding the one-button constraint
- [Asset Management](tutorials/assets.md) - Working with sprites, sounds, and animations
- [Sound System](tutorials/sound.md) - Adding audio to your games

### API Reference
- [BaseGame Class](api/base_game.md) - Core game framework class
- [Settings System](api/settings.md) - Configuration management
- [Sound Manager](api/sound.md) - Audio system reference
- [Asset Manager](api/assets.md) - Resource management
- [HTTP Server](api/server.md) - Game server API

### Architecture
- [System Overview](architecture/overview.md) - High-level architecture
- [Architecture Decision Records](architecture/decisions.md) - ADR collection and rationale
- [UML Diagrams](architecture/uml.md) - Visual architecture documentation
- [Component Details](architecture/components.md) - Detailed component descriptions
- [Data Flow](architecture/data_flow.md) - How data flows through the system
- [Deployment](architecture/deployment.md) - Deployment strategies

### Advanced Topics
- [Performance Optimization](tutorials/performance.md) - Making your games run smoothly
- [Testing](tutorials/testing.md) - Writing tests for your games
- [Internationalization](tutorials/i18n.md) - Adding multiple language support
- [Docker Deployment](tutorials/docker.md) - Containerized deployment

## 🚀 Quick Start

```bash
# Install dependencies
uv sync

# Run demo game
uv run python main.py

# Run specific game with difficulty
uv run python -m unipress.games.jumper.game 5
```

## 🎯 Available Games

### Demo Jump
Simple jumping game demonstrating core mechanics.

### Jumper
Enhanced sprite-based game with animations and parallax backgrounds.

## 🛠️ Development Tools

- **uv**: Fast Python package manager
- **arcade**: Modern 2D game framework
- **ruff**: Fast Python linter and formatter
- **pytest**: Testing framework
- **mypy**: Static type checking
- **Sphinx**: Documentation generation

## 📖 Contributing

See our [Contributing Guide](tutorials/contributing.md) for information on how to contribute to Unipress.

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](../../LICENSE) file for details.

---

**Need help?** Check out our [FAQ](tutorials/faq.md) or open an issue on GitHub.
