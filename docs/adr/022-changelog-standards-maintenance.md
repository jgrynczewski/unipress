# ADR-022: Changelog Standards and Maintenance

## Status

Accepted

## Context

The Unipress project needs a standardized approach to documenting changes, releases, and version history. We need to establish:

- A consistent format for changelog entries
- Clear guidelines for what constitutes a changelog entry
- Maintenance responsibilities and processes
- Integration with our existing development workflow
- Standards for version numbering and release management

## Decision

We will use the **Keep a Changelog** format for our changelog, combined with **Semantic Versioning** for version numbering, and establish clear maintenance processes.

### Changelog Format Standards

#### Keep a Changelog Format
- **Header**: Clear version number and date
- **Categories**: Added, Changed, Deprecated, Removed, Fixed, Security
- **Language**: Present tense, imperative mood
- **Structure**: Reverse chronological order (newest first)
- **Unreleased Section**: For ongoing development

#### Version Numbering (Semantic Versioning)
- **Major.Minor.Patch** (e.g., 0.1.0)
- **Major**: Breaking changes or major architectural changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes and minor improvements

### Maintenance Process

#### Entry Guidelines
1. **Use present tense** ("Add feature" not "Added feature")
2. **Use imperative mood** ("Move cursor to..." not "Moves cursor to...")
3. **Reference issues and pull requests** when applicable
4. **Group changes** by type (Added, Changed, Deprecated, Removed, Fixed, Security)
5. **Keep unreleased section** at the top for ongoing development

#### What Gets Documented
- **Added**: New features, capabilities, or functionality
- **Changed**: Changes to existing functionality
- **Deprecated**: Features that will be removed in future versions
- **Removed**: Features that have been removed
- **Fixed**: Bug fixes and corrections
- **Security**: Security-related changes and vulnerabilities

#### What Does NOT Get Documented
- Internal refactoring that doesn't affect users
- Documentation updates (unless significant)
- Minor code style changes
- Test-only changes
- Build system changes (unless they affect users)

## Alternatives Considered

### 1. Conventional Changelog
**Pros:**
- Automated generation from commit messages
- Consistent with conventional commits
- Reduces manual maintenance

**Cons:**
- Less control over entry quality
- May include too much detail
- Requires strict commit message discipline
- Less readable for end users

### 2. GitHub Releases
**Pros:**
- Integrated with GitHub workflow
- Automatic tag-based releases
- Rich formatting support

**Cons:**
- Platform-specific
- Harder to maintain locally
- Less accessible for offline development
- Requires GitHub-specific workflow

### 3. Simple Markdown List
**Pros:**
- Minimal overhead
- Easy to maintain
- No special formatting

**Cons:**
- Inconsistent structure
- Hard to navigate
- No standardized categories
- Poor readability

### 4. Git Log Based
**Pros:**
- Automatic from commit history
- Always up to date
- No manual maintenance

**Cons:**
- Too verbose
- Includes internal changes
- Poor user experience
- No categorization

## Technical Implementation

### File Structure
```
CHANGELOG.md
├── [Unreleased] section (ongoing development)
├── [Version] - YYYY-MM-DD (released versions)
│   ├── Added
│   ├── Changed
│   ├── Deprecated
│   ├── Removed
│   ├── Fixed
│   └── Security
└── Links and references
```

### Integration with Development Workflow

#### Pre-Release Process
1. **Review Unreleased section** before each release
2. **Categorize changes** appropriately
3. **Add version number** and release date
4. **Move Unreleased content** to new version section
5. **Create git tag** for the release

#### During Development
1. **Add entries** to Unreleased section as features are completed
2. **Update immediately** when bugs are fixed
3. **Reference issues** and pull requests
4. **Keep entries concise** but informative

### Maintenance Responsibilities

#### Primary Maintainer
- **Who**: Project maintainer (jgrynczewski)
- **Responsibilities**:
  - Review and approve changelog entries
  - Ensure consistency and quality
  - Maintain version numbering
  - Create release tags

#### Contributors
- **Who**: All project contributors
- **Responsibilities**:
  - Add entries for their changes
  - Follow established format
  - Reference relevant issues/PRs
  - Keep entries user-focused

#### Review Process
- **When**: Before each release
- **Who**: Project maintainer
- **What**: Review all entries for accuracy and completeness
- **How**: Manual review and testing

## Rationale

### Why Keep a Changelog?
- **User-Focused**: Designed for end users, not developers
- **Standardized**: Widely adopted industry standard
- **Readable**: Clear, consistent format
- **Maintainable**: Simple to update and maintain
- **Comprehensive**: Covers all types of changes

### Why Semantic Versioning?
- **Clear Communication**: Version numbers convey meaning
- **Industry Standard**: Widely understood and adopted
- **Automation Friendly**: Works well with tools and CI/CD
- **User Expectations**: Users understand version progression

### Why Manual Maintenance?
- **Quality Control**: Ensures entries are user-relevant
- **Consistency**: Maintains high standards
- **Flexibility**: Allows for custom categorization
- **User Experience**: Focuses on what matters to users

## Consequences

### Positive
- **Professional Appearance**: Standardized, readable changelog
- **User Communication**: Clear information about changes
- **Maintenance**: Structured approach to updates
- **Integration**: Works well with existing workflow
- **Quality**: Ensures only relevant changes are documented

### Considerations
- **Manual Effort**: Requires ongoing maintenance
- **Discipline**: Team must follow established process
- **Review Time**: Regular review needed before releases
- **Training**: New contributors need to learn process

### Implementation Requirements
- Create initial CHANGELOG.md with project history
- Establish review process for releases
- Train team on entry guidelines
- Integrate with release workflow
- Set up automated reminders for maintenance

## Future Considerations
- **Automation**: Could add automated checks for format compliance
- **Integration**: Could integrate with GitHub releases for dual maintenance
- **Templates**: Could create templates for common change types
- **Metrics**: Could track changelog maintenance metrics

## Related Decisions
- [ADR-005: Conventional Commits with git-cz](005-conventional-commits-git-cz.md) - Commit message standards
- [ADR-007: CI/CD Pipeline with GitHub Actions](007-ci-cd-github-actions.md) - Release automation
- [ADR-017: Containerization with Docker and UV](017-containerization-docker-uv.md) - Release packaging

## References
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- [Conventional Changelog](https://github.com/conventional-changelog/conventional-changelog)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
