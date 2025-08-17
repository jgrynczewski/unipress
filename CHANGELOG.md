# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive Sphinx documentation infrastructure with Myst-Parser
- Complete API documentation with autodoc for all modules and docstrings
- Interactive UML diagrams with clickable links for detailed viewing
- Architecture Decision Records (ADRs) collection and rationale
- Installation guide and development tutorials
- Documentation hosting on Read the Docs and GitHub Pages
- Professional project badges (license, Python version, Arcade engine)
- Navigation structure with toctree for easy browsing
- ADR-021: Developer Documentation Tools Selection
- ADR-022: Changelog Standards and Maintenance
- ADR-023: Documentation Hosting Platform Selection
- GNU GPL v3 license for copyleft protection
- TODO.md roadmap for professional development
- UML documentation with PlantUML diagrams
- ADR-020: UML Documentation with PlantUML

### Changed
- Updated README.md with comprehensive documentation sections and badges
- Enhanced project structure with professional documentation standards
- Improved documentation navigation and user experience
- Replaced default GitHub Pages workflow with custom Sphinx build

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

- **Internationalization**
  - JSON-based message system with Polish default, English fallback
  - Support for variable substitution in messages

- **Logging System**
  - Loguru-based structured logging with JSON format
  - Automatic log rotation and compression
  - Exception tracking with full tracebacks

- **Sound System**
  - Comprehensive audio with OGG format support
  - Event-based architecture with 7 sound categories
  - Volume control hierarchy (master, sfx, music, ui)
  - Non-blocking audio with game startup synchronization

- **Asset Management**
  - Sprite animation system with JSON metadata
  - Organized asset structure (global/game-specific)
  - Lazy loading with caching for performance

- **High Score System**
  - JSON-based persistent high score storage
  - Automatic new record detection and display
  - Per-game high score tracking

- **Development Tools**
  - uv for fast dependency management
  - arcade game framework
  - ruff for linting and formatting
  - pytest for testing framework
  - mypy for type checking
  - Conventional commits with git-cz emojis

- **CI/CD Pipeline**
  - GitHub Actions with automated testing
  - Linting, formatting, type checking, and test execution
  - Manual deployment workflow

- **Containerization**
  - Docker multi-stage builds with audio/GPU support
  - Docker Compose for easy development
  - Non-root user and health checks

- **HTTP Server Architecture**
  - Flask-based game management API
  - REST endpoints for game control
  - Process management and status monitoring

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
  - 22 Architecture Decision Records (ADRs)
  - 5 UML diagrams (Architecture, Class Hierarchy, Data Flow, Deployment, Game Lifecycle)
  - Professional project structure and standards

### Technical Features
- **Performance**: Physics-based obstacle spacing algorithm
- **Accessibility**: Standardized end game screen with cycling buttons
- **Responsive**: Game objects scale with window size changes
- **Professional**: Type hints, comprehensive error handling, structured logging

## [Pre-0.1.0] - Development Phase

### Initial Development
- Project setup and basic architecture
- Core game mechanics implementation
- Asset system development
- Sound system integration
- Testing infrastructure setup

---



---



## Links

- [GitHub Repository](https://github.com/jgrynczewski/unipress)
- [Architecture Decision Records](docs/adr/) - Detailed technical decisions and rationale
- [UML Documentation](docs/uml/)
- [Developer Documentation](docs/sphinx/)

## Architecture Decisions

For detailed technical decisions and rationale behind the implementation choices, see the [Architecture Decision Records](docs/adr/):

- **ADR-001**: Dependency Management with `uv`
- **ADR-002**: Game Framework using `arcade`
- **ADR-003**: Development Tools (ruff, pytest)
- **ADR-004**: Game Design Standards
- **ADR-005**: Conventional Commits with git-cz
- **ADR-006**: Type Checking with mypy
- **ADR-007**: CI/CD Pipeline with GitHub Actions
- **ADR-010**: TOML-based Settings System
- **ADR-011**: JSON-based Internationalization
- **ADR-012**: Loguru-based Logging System
- **ADR-013**: Asset Management System
- **ADR-014**: Obstacle Spacing Algorithm
- **ADR-016**: Comprehensive Sound System
- **ADR-017**: Docker Containerization
- **ADR-018**: HTTP Server Architecture
- **ADR-019**: Flask Framework Selection
- **ADR-020**: UML Documentation with PlantUML
- **ADR-021**: Developer Documentation Tools
- **ADR-022**: Changelog Standards and Maintenance
