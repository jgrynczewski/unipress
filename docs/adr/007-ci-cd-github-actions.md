# ADR-007: GitHub Actions for CI/CD Pipeline

## Status
Accepted

## Context
We need automated testing, quality checks, and deployment pipeline for the project. Several CI/CD options are available:

### CI/CD Platform Options
1. **GitHub Actions** - Integrated with GitHub
2. **GitLab CI** - GitLab's built-in CI/CD
3. **Jenkins** - Self-hosted solution
4. **CircleCI** - Cloud-based CI/CD
5. **Travis CI** - GitHub integration

## Decision
We will use **GitHub Actions** for our CI/CD pipeline with manual deployment trigger.

## Pipeline Design

### Automatic CI (on push/PR):
- **Code Quality**: ruff linting and formatting checks
- **Type Safety**: mypy static type checking
- **Testing**: pytest unit tests
- **Integration**: game startup verification
- **Multi-version**: Python 3.12 matrix testing

### Manual Deployment:
- **Trigger**: Manual workflow dispatch only
- **Prerequisites**: All tests must pass
- **Process**: Build artifacts, mock deployment, create release packages
- **Artifacts**: Release packages with 30-day retention

## Rationale

### GitHub Actions chosen because:
- **Integration**: Native GitHub integration, no external setup
- **Cost**: Free for public repositories
- **Ecosystem**: Excellent action marketplace
- **Modern**: YAML-based, easy to maintain
- **Features**: Matrix builds, artifact storage, manual triggers
- **uv Support**: Official astral-sh/setup-uv action available

### Manual Deployment because:
- **Control**: Prevents accidental deployments
- **Quality Gate**: Ensures human verification before release
- **Flexibility**: Deploy when ready, not on every commit
- **Safety**: Reduces risk of broken deployments

### Pipeline Structure:
- **Separation**: Clear separation between CI (automatic) and CD (manual)
- **Dependencies**: Deployment requires successful tests
- **Efficiency**: Fast feedback on code quality issues
- **Artifacts**: Preserve release packages for distribution

## Consequences
- **Automated Quality**: Every commit/PR is automatically validated
- **Type Safety**: mypy catches type errors early
- **Manual Control**: Deployments happen only when intentionally triggered
- **Fast Feedback**: Developers get quick CI results
- **Release Management**: Clear artifact creation and storage
- **GitHub Dependency**: Tied to GitHub ecosystem (acceptable trade-off)

## Implementation
- `.github/workflows/ci.yml` with test and deploy jobs
- uv-based dependency management in CI
- Comprehensive quality checks (ruff, mypy, pytest)
- Manual deployment trigger with `workflow_dispatch`
- Artifact creation and storage for releases