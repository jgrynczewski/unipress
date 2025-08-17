# Architecture Decision Records (ADRs)

## Overview

Architecture Decision Records (ADRs) are documents that capture important architectural decisions made during the development of Unipress. Each ADR provides context, decision rationale, and consequences to help future developers understand why certain choices were made.

## ADR Structure

Each ADR follows a consistent format:

- **Title**: Clear, descriptive title
- **Status**: Accepted, Deprecated, Superseded, etc.
- **Context**: Problem or situation requiring a decision
- **Decision**: The architectural decision made
- **Consequences**: Positive and negative outcomes
- **References**: Related documents and resources

## Decision Categories

### Development Tools & Standards

#### ADR-001: Dependency Management with uv
- **Decision**: Use `uv` as the primary package manager
- **Rationale**: Fast, modern Rust-based tool with excellent dependency resolution
- **Impact**: Faster dependency installation, better lock file management

#### ADR-002: Game Framework Selection (Arcade)
- **Decision**: Use Arcade framework for game development
- **Rationale**: Modern Python game library with good performance and ease of use
- **Impact**: Simplified game development, good documentation and community

#### ADR-003: Development Tools (Ruff, Pytest, MyPy)
- **Decision**: Ruff for linting/formatting, Pytest for testing, MyPy for type checking
- **Rationale**: Fast, modern tools that work well together
- **Impact**: Consistent code quality, fast feedback loops

#### ADR-005: Conventional Commits with git-cz
- **Decision**: Use conventional commits with git-cz for standardized commit messages
- **Rationale**: Clear commit history, automated changelog generation
- **Impact**: Better project history, easier releases

#### ADR-006: Type Checking with MyPy
- **Decision**: Implement comprehensive type checking
- **Rationale**: Catch errors early, improve code quality and documentation
- **Impact**: Better IDE support, fewer runtime errors

### Game Design & Architecture

#### ADR-004: Game Design Standards
- **Decision**: Strict one-button input constraint for all games
- **Rationale**: Ensures accessibility and simplicity across all games
- **Impact**: Consistent user experience, easier game development

#### ADR-008: Fullscreen Display Standard
- **Decision**: All games run in fullscreen mode by default
- **Rationale**: Immersive gaming experience, consistent across platforms
- **Impact**: Better user experience, simplified display management

#### ADR-009: Three Lives System
- **Decision**: Standard three-lives system for all games
- **Rationale**: Familiar gaming pattern, provides challenge without frustration
- **Impact**: Consistent game mechanics, predictable difficulty curve

#### ADR-014: Obstacle Spacing Algorithm
- **Decision**: Implement adaptive obstacle spacing based on difficulty
- **Rationale**: Ensures fair and engaging gameplay progression
- **Impact**: Better game balance, scalable difficulty

### Configuration & Data Management

#### ADR-010: Settings System with TOML
- **Decision**: Use TOML for hierarchical configuration
- **Rationale**: Human-readable, supports complex nested structures
- **Impact**: Easy configuration management, good developer experience

#### ADR-011: Internationalization with JSON
- **Decision**: JSON-based i18n with Polish default, English fallback
- **Rationale**: Simple, flexible localization system
- **Impact**: Easy to add new languages, maintainable translations

#### ADR-012: Logging System with Loguru
- **Decision**: Use Loguru for structured JSON logging
- **Rationale**: Excellent performance, structured output, easy configuration
- **Impact**: Better debugging, production monitoring capabilities

### Asset & Media Management

#### ADR-013: Asset Management System
- **Decision**: Centralized asset management with JSON metadata
- **Rationale**: Organized resource management, easy to extend
- **Impact**: Consistent asset handling, better performance

#### ADR-016: Comprehensive Sound System
- **Decision**: Event-driven audio system with OGG format
- **Rationale**: High-quality audio, efficient event handling
- **Impact**: Rich audio experience, good performance

### Infrastructure & Deployment

#### ADR-017: Containerization with Docker and uv
- **Decision**: Docker-based deployment with uv package management
- **Rationale**: Consistent environments, easy deployment
- **Impact**: Reproducible builds, simplified deployment

#### ADR-018: HTTP Server Architecture
- **Decision**: Flask-based HTTP server for game management
- **Rationale**: Lightweight, Python-native, easy to extend
- **Impact**: API-based game management, scalable architecture

#### ADR-019: HTTP Server Framework Selection
- **Decision**: Flask over FastAPI for simplicity and maturity
- **Rationale**: Simpler learning curve, sufficient features for current needs
- **Impact**: Faster development, easier maintenance

### Documentation & Quality

#### ADR-020: UML Documentation with PlantUML
- **Decision**: Use PlantUML for generating UML diagrams
- **Rationale**: Text-based diagrams, version control friendly
- **Impact**: Maintainable documentation, clear architecture visualization

#### ADR-021: Developer Documentation with Sphinx
- **Decision**: Sphinx with Myst-Parser for comprehensive documentation
- **Rationale**: Excellent Python documentation tool, Markdown support
- **Impact**: Professional documentation, good developer experience

#### ADR-022: Changelog Standards and Maintenance
- **Decision**: Follow "Keep a Changelog" and Semantic Versioning
- **Rationale**: Standardized change tracking, clear release history
- **Impact**: Better project transparency, easier releases

#### ADR-023: Documentation Hosting Platform
- **Decision**: Read the Docs primary, GitHub Pages backup
- **Rationale**: Professional hosting, good integration with GitHub
- **Impact**: Reliable documentation access, good SEO

## Decision Making Process

### When to Create an ADR

Create an ADR when making decisions about:

- **Technology choices**: Frameworks, libraries, tools
- **Architectural patterns**: Design patterns, system structure
- **Standards**: Coding standards, naming conventions
- **Infrastructure**: Deployment, hosting, CI/CD
- **Process changes**: Development workflow, release process

### ADR Lifecycle

1. **Proposed**: Initial draft for review
2. **Accepted**: Decision approved and implemented
3. **Deprecated**: Decision no longer relevant
4. **Superseded**: Replaced by newer decision

### Review Process

- All ADRs are reviewed by the development team
- Decisions are documented before implementation
- Regular review of existing ADRs for relevance
- Updates made when circumstances change

## Benefits of ADRs

### For Current Development
- **Context preservation**: Why decisions were made
- **Consistency**: Standardized approach across the project
- **Onboarding**: New developers understand project choices

### For Future Maintenance
- **Historical record**: Evolution of the architecture
- **Change tracking**: How and why systems evolved
- **Risk mitigation**: Understanding consequences of changes

### For Project Management
- **Transparency**: Clear decision-making process
- **Accountability**: Documented rationale for choices
- **Communication**: Shared understanding across team

## Related Resources

- [ADR Directory](../adr/) - Complete collection of ADRs
- [UML Diagrams](uml.md) - Visual architecture documentation
- [Development Standards](../tutorials/development_standards.md) - Coding and process guidelines
- [Contributing Guide](../tutorials/contributing.md) - How to contribute to the project
