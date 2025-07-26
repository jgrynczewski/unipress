# ADR-005: Use Conventional Commits with git-cz Standard

## Status
Accepted

## Context
We need consistent commit message format for better project history, automated tooling, and clear communication of changes.

## Decision
We will use **Conventional Commits** with **git-cz** emoji standard for all commits.

## Commit Format
```
<type>(<scope>): <emoji><subject>

[optional body]

[optional footer(s)]
```

## Types and Emojis (git-cz standard)
- `chore: 🤖` - Build process or auxiliary tool changes
- `ci: 🎡` - CI related changes
- `docs: ✏️` - Documentation only changes
- `feat: 🎸` - A new feature
- `fix: 🐛` - A bug fix
- `perf: ⚡️` - A code change that improves performance
- `refactor: 💡` - A code change that neither fixes a bug or adds a feature
- `release: 🏹` - Create a release commit
- `style: 💄` - Markup, white-space, formatting, missing semi-colons...
- `test: 💍` - Adding missing tests

## Examples
- `feat: 🎸 add difficulty system to base game class`
- `fix: 🐛 resolve collision detection in jump game`
- `docs: ✏️ update README with installation instructions`
- `chore: 🤖 add comprehensive Python .gitignore`

## Rationale
- **Consistency**: Standardized format across all commits
- **Automation**: Enables automated changelog generation
- **Clarity**: Clear communication of change types
- **Visual**: Emojis make commit history more readable
- **Tooling**: Compatible with semantic-release and other tools

## Implementation
- All commits must follow this format
- Use appropriate emoji for commit type
- Keep descriptions concise and clear
- Reference: https://www.npmjs.com/package/git-cz#custom-config