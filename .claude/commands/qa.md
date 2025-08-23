# /qa - Quality Assurance Pipeline

Run the complete quality assurance pipeline for the Unipress project.

## Usage

```
/qa
```

## Implementation

Execute all quality checks in the correct order:

1. **Code Linting**
   ```bash
   echo "🔍 Running ruff check..."
   uv run ruff check
   ```

2. **Code Formatting**
   ```bash
   echo "💄 Running ruff format..."
   uv run ruff format
   ```

3. **Type Checking**
   ```bash
   echo "🔒 Running mypy type checking..."
   uv run mypy unipress
   ```

4. **Test Suite**
   ```bash
   echo "🧪 Running pytest..."
   uv run pytest
   ```

5. **Success Summary**
   ```bash
   echo "✅ All quality checks passed!"
   echo "Code is ready for commit and push"
   ```

## Error Handling

- Stop execution on first failure
- Display clear error messages with context
- Suggest fixes for common issues:
  - Linting errors: Show file and line numbers
  - Type errors: Suggest type annotations
  - Test failures: Show failing test details

## Integration

This command implements the quality gates required by:
- CLAUDE.md development standards
- CI/CD pipeline requirements
- Pre-commit validation

## Related Commands

- Use before committing changes
- Required before creating pull requests
- Integrated into CI/CD pipeline checks