# ADR-026: Development Documentation Structure

## Status
Accepted

## Date
2025-09-14

## Context
During the development of the Jump Sky game, we created several important working documents:
- Implementation plans (feature specifications)
- Todo lists (progress tracking)
- Testing documents
- Working notes and artifacts

These documents are valuable development artifacts that provide insight into:
- Decision-making processes
- Implementation strategies  
- Progress tracking
- Testing methodologies
- Knowledge transfer for future developers

However, these working documents were scattered in the root `docs/` directory without clear organization, making them difficult to find and manage as the project grows.

## Problem
Without a structured approach to development documentation:
- Working documents become scattered and hard to find
- No clear conventions for naming or organizing development artifacts
- Difficult to track relationships between related documents
- New developers struggle to understand the development process
- Knowledge from completed features gets lost or buried
- No standardized templates for consistent documentation

## Decision
We will implement a structured development documentation system under `docs/development/` with the following organization:

### Directory Structure
```
docs/development/
├── features/           # Feature implementation plans and specifications
├── todos/             # Task lists and progress tracking documents  
├── planning/          # High-level planning documents and strategies
├── testing/           # Test plans, test results, and QA documents
├── templates/         # Templates for consistent document creation
├── README.md          # Documentation structure guide
└── INDEX.md           # Quick overview of active development work
```

### Naming Conventions
- **Features**: `YYYY-MM-DD-feature-name-implementation.md`
- **Todos**: `feature-name-todo.md`
- **Planning**: `YYYY-MM-DD-plan-name.md`
- **Testing**: `feature-name-test-plan.md` or `YYYY-MM-DD-test-results-feature-name.md`

### Document Standards
- All documents include creation date and author
- Cross-references using relative links
- Progress tracking with standardized checkbox format
- Clear status indicators (✅ COMPLETED, 🔄 IN PROGRESS, etc.)
- Consistent priority levels (High, Medium, Low)

### Templates
Standardized templates for:
- Feature implementation plans
- Todo lists with progress tracking
- Test plans and results
- Planning documents

## Consequences

### Positive
- **Organization**: Clear structure for finding and managing development documents
- **Consistency**: Standardized formats and naming conventions
- **Knowledge Preservation**: Important development artifacts are properly organized and preserved
- **Developer Onboarding**: New developers can understand the development process and history
- **Process Improvement**: Templates ensure consistent and complete documentation
- **Scalability**: Structure scales as more features and developers are added
- **Cross-References**: Easy navigation between related documents

### Negative
- **Initial Setup Time**: Need to create templates and organize existing documents
- **Learning Curve**: Developers need to learn the new structure and conventions
- **Maintenance Overhead**: Need to maintain INDEX.md and cross-references
- **Potential Over-Documentation**: Risk of creating too much process overhead

### Neutral
- **File Movement**: Existing documents need to be moved to new locations (one-time migration)
- **Link Updates**: Some existing links may need updating

## Implementation
1. ✅ Create `docs/development/` directory structure
2. ✅ Move existing working documents to appropriate locations
3. ✅ Create README.md with structure documentation
4. ✅ Create INDEX.md for quick reference
5. ✅ Create templates for consistent document creation
6. [ ] Update any broken cross-references
7. [ ] Add this structure to main project README
8. [ ] Train team on new conventions

## Related Decisions
- **ADR-025**: Development Planning Standards - Established need for structured planning
- **ADR-022**: CHANGELOG Standards - Similar documentation standardization approach
- **ADR-021**: Developer Documentation Tools - Part of overall documentation strategy

## Examples
- Jump Sky game documents moved to new structure:
  - `docs/development/features/2025-09-06-jump-sky-game-implementation.md`
  - `docs/development/todos/jump-sky-todo.md`

## Alternatives Considered
1. **Keep documents in root docs/**: Simple but doesn't scale, hard to organize
2. **Use existing plans/ directory**: Too generic, doesn't handle different document types
3. **Per-game subdirectories**: More complex, harder to find cross-cutting concerns
4. **Wiki-based approach**: External dependency, not version controlled with code

## Notes
This structure is designed to grow with the project and can be adapted as new document types or organizational needs emerge. The key principle is maintaining clear separation of concerns while preserving relationships between related documents.