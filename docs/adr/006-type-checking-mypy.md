# ADR-006: Use mypy for Static Type Checking

## Status
Accepted

## Context
We need static type checking to catch type-related bugs early, improve code quality, and enhance developer experience. Several options are available:

### Type Checking Options
1. **mypy** - Original static type checker for Python
2. **pyright/pylance** - Microsoft's type checker (used in VS Code)
3. **pyre** - Facebook's type checker
4. **pytype** - Google's type checker

## Decision
We will use **mypy** for static type checking.

## Comparison

### mypy
- **Pros**: 
  - Industry standard, most mature
  - Excellent Python ecosystem integration
  - Great documentation and community support
  - Configurable strictness levels
  - Works well with CI/CD
- **Cons**: 
  - Can be slower on large codebases
  - Some edge cases with complex typing

### pyright/pylance
- **Pros**: 
  - Very fast performance
  - Excellent IDE integration (VS Code)
  - Modern type inference
- **Cons**: 
  - Less mature than mypy
  - Primarily focused on IDE experience
  - Node.js dependency

### pyre
- **Pros**: 
  - Fast incremental checking
  - Good for large codebases
- **Cons**: 
  - Less community adoption
  - Facebook-specific optimizations
  - More complex setup

### pytype
- **Pros**: 
  - Can infer types without annotations
  - Good error messages
- **Cons**: 
  - Google-specific, less universal
  - Limited community support
  - Slower adoption of new Python features

## Rationale
- **Maturity**: mypy is the most established and battle-tested
- **Ecosystem**: Best integration with Python tooling (pytest, CI/CD, etc.)
- **Standards**: Widely adopted industry standard
- **Documentation**: Excellent docs and learning resources
- **Flexibility**: Configurable strictness allows gradual adoption
- **CI/CD**: Proven in automated environments

## Consequences
- Industry-standard type checking
- Good integration with our existing toolchain (ruff, pytest)
- Gradual typing adoption possible
- Excellent error reporting
- Some performance overhead on large codebases (not relevant for our project size)

## Implementation
- Add mypy as dev dependency
- Configure in pyproject.toml with appropriate strictness
- Include in CI/CD pipeline
- Add to development workflow commands