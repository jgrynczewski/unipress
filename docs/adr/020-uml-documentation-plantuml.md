# ADR 020: UML Documentation with PlantUML

## Status

Accepted

## Context

The Unipress project has grown in complexity with the introduction of:
- HTTP server architecture for game management
- Docker containerization with audio/graphics passthrough
- Multiple game implementations with shared base classes
- Client-server communication patterns
- Process management and lifecycle handling

We need a standardized way to document the system architecture, class relationships, deployment structure, and data flows to:
- Help new developers understand the system quickly
- Maintain architectural consistency as the project evolves
- Provide clear documentation for technical decisions
- Support code reviews and architectural discussions

## Decision

We will use **PlantUML** for creating and maintaining UML diagrams in the project, with diagrams stored as `.puml` files in the `docs/uml/` directory.

### Diagram Types to Create

1. **Architecture Overview** - High-level system architecture showing component relationships
2. **Game Lifecycle** - Sequence diagram for game launch to completion
3. **Class Hierarchy** - Detailed class diagram with inheritance and composition
4. **Deployment Diagram** - System deployment across containers and nodes
5. **Data Flow** - Activity diagram showing data processing patterns

## Consequences

### Positive

- **Text-based format** - Diagrams are version-controlled alongside code
- **Platform independent** - Works on any system with Java runtime
- **Multiple output formats** - PNG, SVG, PDF generation support
- **IDE integration** - Many editors have PlantUML plugins
- **Online rendering** - Can generate diagrams without local installation
- **Consistent styling** - Standardized appearance across all diagrams
- **Easy maintenance** - Changes to diagrams are tracked in git
- **Collaboration friendly** - Text format enables easy code review of diagrams

### Negative

- **Java dependency** - Requires Java runtime for local generation
- **Learning curve** - Team needs to learn PlantUML syntax
- **Tool dependency** - Relies on external tool for diagram generation
- **No visual editing** - Diagrams must be written in text format

### Neutral

- **File size** - `.puml` files are small, but generated images can be large
- **Rendering time** - Complex diagrams may take time to generate

## Alternatives Considered

### 1. Draw.io / diagrams.net
**Pros**: Visual editor, web-based, free
**Cons**: Proprietary format, harder to version control, requires manual export

### 2. Lucidchart
**Pros**: Professional appearance, collaboration features
**Cons**: Commercial tool, proprietary format, external dependency

### 3. Mermaid
**Pros**: Markdown integration, GitHub support, text-based
**Cons**: Limited UML support, fewer diagram types, less mature

### 4. Visio
**Pros**: Industry standard, comprehensive features
**Cons**: Commercial, Windows-only, proprietary format

### 5. Manual drawing tools (Inkscape, GIMP)
**Pros**: Complete control over appearance
**Cons**: Time-consuming, hard to maintain, not version-controlled

## Implementation

### Directory Structure
```
docs/
├── uml/
│   ├── architecture-overview.puml
│   ├── game-lifecycle.puml
│   ├── class-hierarchy.puml
│   ├── deployment-diagram.puml
│   └── data-flow.puml
```

### Diagram Conventions

#### Styling
- **Theme**: Plain theme for clean, professional appearance
- **Background**: White background for consistency
- **Font**: Arial, 11-12pt for readability
- **Colors**: Minimal color usage, focus on clarity

#### Naming Conventions
- **Classes**: PascalCase (e.g., `BaseGame`, `SoundManager`)
- **Methods**: snake_case (e.g., `play_sound_event`, `setup_game`)
- **Variables**: snake_case (e.g., `jump_velocity`, `game_over`)

#### Relationship Types
- **Inheritance**: `--|>` (extends)
- **Composition**: `*--` (contains)
- **Association**: `-->` (uses)
- **Dependency**: `..>` (depends on)

### Generation Methods

#### Command Line
```bash
# Generate PNG images
plantuml -tpng *.puml

# Generate SVG images
plantuml -tsvg *.puml

# Generate PDF documents
plantuml -tpdf *.puml
```

#### Online Generation
- Copy `.puml` content to [PlantUML Online Server](http://www.plantuml.com/plantuml/uml/)
- Generate images without local installation

#### IDE Integration
- **VS Code**: PlantUML extension
- **IntelliJ IDEA**: PlantUML integration plugin
- **Eclipse**: PlantUML plugin

### Maintenance Guidelines

#### When to Update
- New features added to the system
- Architecture changes (new components, removed components)
- API changes (new endpoints, modified interfaces)
- Class structure changes (new classes, inheritance changes)

#### Version Control
- Keep `.puml` files in version control
- Generate images for documentation releases
- Update diagrams with code changes

## Related ADRs

- [ADR 018: Game Server HTTP Architecture](018-game-server-http-architecture.md) - HTTP server design
- [ADR 019: HTTP Server Framework Selection](019-http-server-framework-selection.md) - Flask framework choice
- [ADR 017: Containerization with Docker and UV](017-containerization-docker-uv.md) - Docker deployment

## References

- [PlantUML Official Site](https://plantuml.com/)
- [PlantUML Language Reference](https://plantuml.com/guide)
- [PlantUML Examples](https://plantuml.com/examples)
- [UML 2.5 Specification](https://www.omg.org/spec/UML/2.5/)

