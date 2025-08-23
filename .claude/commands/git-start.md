# /git-start - Git Flow Branch Creation

Automate Git Flow branch creation following Unipress project standards.

## Usage

```
/git-start [type] [name]
```

## Parameters

- `type`: Branch type (feat, fix, docs, chore, release)
- `name`: Descriptive branch name (kebab-case)

## Examples

```
/git-start feat new-puzzle-game
/git-start fix collision-detection-bug
/git-start docs planning-standards
/git-start chore dependency-update
```

## Implementation

Execute the following Git Flow process:

1. **Check current status and branch**
   ```bash
   echo "Current branch: $(git branch --show-current)"
   git status --porcelain
   ```

2. **Warn if uncommitted changes**
   - If working tree is not clean, warn user
   - Suggest stashing or committing changes first

3. **Switch to master and update**
   ```bash
   git checkout master
   git pull origin master
   ```

4. **Create and switch to new branch**
   ```bash
   git checkout -b [type]/[name]
   ```

5. **Verify success**
   ```bash
   echo "✅ Created branch: [type]/[name]"
   echo "Ready to work following Git Flow standards"
   git status
   ```

## Branch Type Validation

- **feat/**: New features, games, major enhancements
- **fix/**: Bug fixes, error corrections, issue resolutions  
- **docs/**: Documentation updates, ADRs, README changes
- **chore/**: Build system, dependencies, tooling, refactoring
- **release/**: Release preparation branches

## Error Handling

- Validate branch type is in allowed list
- Check if branch name already exists
- Ensure master branch is up to date
- Handle merge conflicts if they occur

## Related Standards

- Follow conventional commit format when committing
- Create PR when work is complete
- Use git-cz emojis in commit messages
- Pass all quality checks before pushing

This command implements the Git Flow Checklist requirements from CLAUDE.md.