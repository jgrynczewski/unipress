# ADR-024: Git Flow Branching Strategy

## Status
Accepted

## Context
We need to establish a clear and efficient git workflow for the Unipress project. This game development project requires:
- Feature development with clear separation
- Bug fixes that can be deployed quickly
- Release management for game versions
- Code review process through pull requests
- Integration with existing CI/CD pipeline

## Decision
We will implement a **GitHub Flow** variant optimized for small teams, with the following key elements:

### Branch Structure
- **`master`** - Main production branch, always deployable
- **`develop`** - Integration branch for features (optional, can merge directly to master for small team)
- **`feat/*`** - Feature branches for new functionality
- **`fix/*`** - Bug fix branches for critical issues
- **`chore/*`** - Maintenance and tooling changes
- **`docs/*`** - Documentation updates
- **`release/*`** - Release preparation branches

### Workflow Rules
1. **Direct to master** - For small team, features can merge directly to master via pull requests
2. **Branch naming** - Use conventional prefixes: `feat/`, `fix/`, `chore/`, `docs/`
3. **Pull request required** - All changes must go through pull request review
4. **Squash merging** - Use squash merge to keep history clean
5. **Conventional commits** - Follow existing git-cz standard with emojis
6. **Immediate deployment** - Master branch is always deployable

### Branch Protection
- Require pull request reviews
- Require status checks to pass (CI pipeline)
- Require up-to-date branches before merging
- Restrict direct pushes to master

## Consequences

### Positive
- **Clear workflow** - Developers know exactly how to contribute
- **Code review** - All changes are reviewed before merging
- **Clean history** - Squash merging keeps master history linear
- **Fast deployment** - Master is always ready for deployment
- **Flexibility** - Can adapt to team size changes

### Negative
- **Overhead** - Pull request process adds some overhead
- **Learning curve** - New developers need to learn the workflow
- **Branch management** - Need to clean up old branches regularly

### Neutral
- **Tooling** - Requires GitHub branch protection settings
- **Documentation** - Need to maintain workflow documentation

## Implementation

### GitHub Settings
1. Enable branch protection on `master`
2. Require pull request reviews
3. Require status checks to pass
4. Enable squash merging as default

### Developer Workflow
1. Create feature branch from master
2. Make changes with conventional commits
3. Push branch and create pull request
4. Address review feedback
5. Merge via squash merge
6. Delete feature branch

### CI/CD Integration
- All branches trigger CI checks
- Only master triggers deployment
- Pull requests show status checks
- Automated testing on all changes

## Related ADRs
- [ADR-005: Conventional Commits with git-cz](005-conventional-commits-git-cz.md)
- [ADR-007: CI/CD GitHub Actions](007-ci-cd-github-actions.md)
