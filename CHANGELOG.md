# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive Sphinx documentation infrastructure with Myst-Parser
- ADR-021: Developer Documentation Tools Selection
- GNU GPL v3 license for copyleft protection
- TODO.md roadmap for professional development
- UML documentation with PlantUML diagrams
- ADR-020: UML Documentation with PlantUML

### Changed
- Updated README.md with UML diagrams and ADR documentation sections
- Enhanced project structure with comprehensive documentation

## [0.1.0] - 2024-08-17

### Added
- **Core Game Framework**
  - BaseGame abstract class with standardized game lifecycle
  - 3-lives system with pause-after-death mechanics
  - Fullscreen display with ESC toggle
  - Difficulty system (1-10 scale) affecting reaction time windows
  - One-button input constraint (left mouse click only)

- **Settings System**
  - TOML-based hierarchical configuration (global → game → constructor)
  - Configurable difficulty, lives, fullscreen, and audio settings
  - ADR-010: TOML-based Settings System

- **Internationalization**
  - JSON-based message system with Polish default, English fallback
  - Support for variable substitution in messages
  - ADR-011: JSON-based Internationalization System

- **Logging System**
  - Loguru-based structured logging with JSON format
  - Automatic log rotation and compression
  - Exception tracking with full tracebacks
  - ADR-012: Logging System

- **Sound System**
  - Comprehensive audio with OGG format support
  - Event-based architecture with 7 sound categories
  - Volume control hierarchy (master, sfx, music, ui)
  - Non-blocking audio with game startup synchronization
  - ADR-016: Comprehensive Sound System

- **Asset Management**
  - Sprite animation system with JSON metadata
  - Organized asset structure (global/game-specific)
  - Lazy loading with caching for performance
  - ADR-013: Asset Management System

- **High Score System**
  - JSON-based persistent high score storage
  - Automatic new record detection and display
  - Per-game high score tracking

- **Development Tools**
  - uv for fast dependency management (ADR-001)
  - arcade game framework (ADR-002)
  - ruff for linting and formatting (ADR-003)
  - pytest for testing framework
  - mypy for type checking (ADR-006)
  - Conventional commits with git-cz emojis (ADR-005)

- **CI/CD Pipeline**
  - GitHub Actions with automated testing
  - Linting, formatting, type checking, and test execution
  - Manual deployment workflow
  - ADR-007: CI/CD Pipeline

- **Containerization**
  - Docker multi-stage builds with audio/GPU support
  - Docker Compose for easy development
  - Non-root user and health checks
  - ADR-017: Containerization with Docker and UV

- **HTTP Server Architecture**
  - Flask-based game management API
  - REST endpoints for game control
  - Process management and status monitoring
  - ADR-018: Game Server HTTP Architecture
  - ADR-019: HTTP Server Framework Selection

- **Games**
  - Demo Jump: Reference implementation with geometric sprites
  - Jumper: Enhanced sprite-based game with animations
    - 8-frame running animation
    - 5-frame fire obstacle animation
    - 6-frame jumping animation
    - Parallax scrolling background (5 layers)
    - Professional sound system (7 audio events)
    - Responsive positioning system

- **Documentation**
  - Comprehensive README.md (434 lines)
  - 21 Architecture Decision Records (ADRs)
  - 5 UML diagrams (Architecture, Class Hierarchy, Data Flow, Deployment, Game Lifecycle)
  - Professional project structure and standards

### Technical Features
- **Performance**: Physics-based obstacle spacing algorithm (ADR-014)
- **Accessibility**: Standardized end game screen with cycling buttons
- **Responsive**: Game objects scale with window size changes
- **Professional**: Type hints, comprehensive error handling, structured logging

### Development Standards
- **Code Quality**: ruff linting, mypy type checking, pytest testing
- **Documentation**: Comprehensive docstrings, ADRs, UML diagrams
- **Version Control**: Conventional commits with git-cz emojis
- **Architecture**: Clean separation of concerns, extensible design

## [Pre-0.1.0] - Development Phase

### Initial Development
- Project setup and basic architecture
- Core game mechanics implementation
- Asset system development
- Sound system integration
- Testing infrastructure setup

---

## Version History

### Version Numbering
- **Major.Minor.Patch** (e.g., 0.1.0)
- **Major**: Breaking changes or major architectural changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes and minor improvements

### Release Schedule
- **Development**: Continuous development with feature branches
- **Releases**: Tagged releases for stable versions
- **Documentation**: Updated with each significant change

### Breaking Changes
- None in current version (0.1.0 is initial release)

### Deprecations
- None currently

---

## Contributing

When adding entries to this changelog, please follow these guidelines:

1. **Use present tense** ("Add feature" not "Added feature")
2. **Use imperative mood** ("Move cursor to..." not "Moves cursor to...")
3. **Reference issues and pull requests** when applicable
4. **Group changes** by type (Added, Changed, Deprecated, Removed, Fixed, Security)
5. **Keep unreleased section** at the top for ongoing development

## Links

- [GitHub Repository](https://github.com/jgrynczewski/unipress)
- [Architecture Decision Records](docs/adr/)
- [UML Documentation](docs/uml/)
- [Developer Documentation](docs/sphinx/)
