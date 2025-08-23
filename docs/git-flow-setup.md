# Git Flow Setup Guide

This guide explains how to configure GitHub repository settings to support our git flow strategy.

## Repository Settings

### 1. Branch Protection Rules

Navigate to **Settings > Branches** and add a branch protection rule for `master`:

#### Required Settings
- ✅ **Require a pull request before merging**
  - Require approvals: `1` (minimum)
  - Dismiss stale PR approvals when new commits are pushed
- ✅ **Require status checks to pass before merging**
  - Require branches to be up to date before merging
  - Status checks: `test` (from CI workflow)
- ✅ **Restrict pushes that create files that bypass pull request reviews**
- ✅ **Require linear history** (enforces squash merging)

#### Optional Settings
- ✅ **Include administrators** (apply rules to admins too)
- ✅ **Restrict deletions** (prevent accidental branch deletion)

### 2. Merge Button Settings

In **Settings > General > Pull Requests**:

- ✅ **Allow squash merging** (recommended)
- ✅ **Allow merge commits** (optional)
- ❌ **Allow rebase merging** (not recommended for our workflow)

### 3. Default Branch

Ensure `master` is set as the default branch in **Settings > General**.

## Workflow Configuration

### Pull Request Template

Create `.github/pull_request_template.md`:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] 🎸 New feature
- [ ] 🐛 Bug fix
- [ ] ✏️ Documentation
- [ ] 🤖 Build/tool changes
- [ ] 💡 Refactoring
- [ ] 💍 Tests
- [ ] 💄 Style changes
- [ ] ⚡ Performance improvements
- [ ] 🏹 Release
- [ ] 🎡 CI/CD changes

## Testing
- [ ] All tests pass (`uv run pytest`)
- [ ] Linting passes (`uv run ruff check`)
- [ ] Code is formatted (`uv run ruff format`)
- [ ] Type checking passes (`uv run mypy unipress`)

## Checklist
- [ ] Code follows project standards
- [ ] Self-review completed
- [ ] Conventional commits used
- [ ] No unrelated changes bundled
- [ ] Documentation updated if needed

## Screenshots (if applicable)
Add screenshots for UI changes
```

### Issue Templates

Create `.github/ISSUE_TEMPLATE/` directory with templates:

#### Bug Report Template (`.github/ISSUE_TEMPLATE/bug_report.md`)
```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. 
2. 
3. 

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.12.0]
- Game: [e.g., jumper, demo_jump]
- Difficulty: [e.g., 5]

## Additional Context
Any other context about the problem
```

#### Feature Request Template (`.github/ISSUE_TEMPLATE/feature_request.md`)
```markdown
## Feature Description
Clear description of the requested feature

## Problem Statement
What problem does this feature solve?

## Proposed Solution
How should this feature work?

## Alternative Solutions
Any alternative approaches considered?

## Additional Context
Any other context about the feature request
```

## Developer Setup

### Local Git Configuration

```bash
# Set up git aliases for common operations
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'

# Configure default branch name
git config --global init.defaultBranch master

# Set up git-cz for conventional commits
npm install -g commitizen cz-conventional-changelog
echo '{ "path": "cz-conventional-changelog" }' > ~/.czrc
```

### Pre-commit Hooks (Optional)

Install pre-commit hooks to enforce standards:

```bash
# Install pre-commit
uv add --dev pre-commit

# Install hooks
uv run pre-commit install

# Run on all files
uv run pre-commit run --all-files
```

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.12

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

## Workflow Examples

### Feature Development

```bash
# 1. Start new feature
git checkout master
git pull origin master
git checkout -b feat/new-game

# 2. Make changes
# ... edit files ...

# 3. Commit with conventional format
git add .
git commit -m "feat: 🎸 add new space shooter game"

# 4. Push and create PR
git push origin feat/new-game
# Create PR on GitHub with template

# 5. After merge, clean up
git checkout master
git pull origin master
git branch -d feat/new-game
```

### Bug Fix

```bash
# 1. Start bug fix
git checkout master
git pull origin master
git checkout -b fix/collision-detection

# 2. Fix the bug
# ... edit files ...

# 3. Commit fix
git add .
git commit -m "fix: 🐛 correct collision detection in jumper game"

# 4. Push and create PR
git push origin fix/collision-detection
# Create PR on GitHub

# 5. After merge, clean up
git checkout master
git pull origin master
git branch -d fix/collision-detection
```

### Documentation Update

```bash
# 1. Start docs update
git checkout master
git pull origin master
git checkout -b docs/update-readme

# 2. Update documentation
# ... edit README.md ...

# 3. Commit changes
git add .
git commit -m "docs: ✏️ update installation instructions"

# 4. Push and create PR
git push origin docs/update-readme
# Create PR on GitHub

# 5. After merge, clean up
git checkout master
git pull origin master
git branch -d docs/update-readme
```

## Troubleshooting

### Common Issues

#### Branch Protection Blocking Merge
- Ensure all CI checks pass
- Ensure branch is up to date with master
- Ensure at least one approval is given

#### Squash Merge Not Available
- Check repository settings for merge options
- Ensure squash merging is enabled
- Check if branch protection allows squash merging

#### Conventional Commits Not Working
- Install commitizen: `npm install -g commitizen`
- Use `git cz` instead of `git commit`
- Or manually format: `type: emoji description`

### Getting Help

- Check [ADR-024: Git Flow Branching Strategy](../adr/024-git-flow-branching-strategy.md)
- Review [Conventional Commits ADR](../adr/005-conventional-commits-git-cz.md)
- Check GitHub documentation for branch protection
