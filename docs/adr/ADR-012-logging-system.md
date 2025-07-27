# ADR-012: Logging System

## Status
Proposed

## Context
The current codebase uses basic `print()` statements for output and debugging. For a professional game development project, we need a proper logging system that:

- Provides structured logging with appropriate levels
- Integrates with our existing TOML-based settings system
- Supports both development debugging and production monitoring
- Handles log rotation and file management
- Follows Python logging best practices

## Decision
We will implement a logging system using **Loguru** as the primary logging library with the following architecture:

### Library Choice: Loguru
- **Rationale**: Simpler API than stdlib logging, thread-safe by default, built-in rotation
- **Features**: Automatic JSON support, excellent exception handling, minimal configuration
- **Trade-off**: Additional dependency vs significant reduction in setup complexity

### Configuration Integration
- Logging settings will be part of the TOML settings hierarchy
- Global logging settings in `unipress/settings.toml`
- Per-game logging overrides in `unipress/games/<game>/settings.toml`
- Configuration supports: log level, file paths, rotation settings, output format

### Log Levels Strategy
- **DEBUG**: Development-only diagnostic information
- **INFO**: General game events, player actions, system status
- **WARNING**: Potential issues that don't break functionality
- **ERROR**: Errors affecting gameplay but not crashing the game
- **CRITICAL**: Fatal errors requiring immediate attention

### Output Formats
- **Development**: Human-readable console output with colors
- **Production**: Structured JSON format for analysis and monitoring
- **File logging**: Always JSON format for consistency and parsing

### Log Rotation and Management
- **Size-based rotation**: 10MB per file with 5 backup files
- **Automatic cleanup**: Remove logs older than 30 days
- **Compression**: Gzip compression for archived logs
- **File naming**: `unipress-{time:YYYY-MM-DD}.log`

## Implementation Plan

### Settings Schema
```toml
[logging]
level = "INFO"
console_enabled = true
file_enabled = true
file_path = "logs/unipress-{time:YYYY-MM-DD}.log"
rotation = "10 MB"
retention = "30 days"
compression = "gz"
format = "json"  # "json" or "human"
```

### Integration Points
1. **BaseGame class**: Add logger instance and common logging methods
2. **Settings system**: Extend to load and apply logging configuration
3. **Main entry point**: Initialize logging before game startup
4. **Error handling**: Replace print statements with appropriate log calls

### Performance Considerations
- Lazy evaluation of log messages using f-strings or .format()
- Conditional logging checks for expensive operations
- Asynchronous logging for high-frequency events if needed

### Exception Handling Rules
- **ALL exceptions must be logged with full traceback**
- Use `log_error()` function for consistent exception logging
- Include relevant context information with each exception
- Log exceptions at the point where they are caught, not just at top level

## Consequences

### Positive
- Professional-grade logging suitable for production deployment
- Structured logs enable advanced analysis and monitoring
- Automatic rotation prevents disk space issues
- Consistent logging across all games and components
- Better debugging capabilities during development

### Negative
- Additional dependency (loguru)
- Slight learning curve for team members unfamiliar with structured logging
- Minor performance overhead compared to print statements

### Neutral
- Configuration complexity increases but remains manageable
- Log files require periodic maintenance in production environments

## Alternatives Considered

### Python Standard Library Logging
- **Pros**: No additional dependencies, highly customizable
- **Cons**: Complex configuration, verbose setup, poor defaults
- **Verdict**: Rejected due to setup complexity for game development workflow

### StructLog
- **Pros**: Excellent structured logging, multiple backend support
- **Cons**: More complex than needed, requires additional configuration
- **Verdict**: Rejected as overkill for current project scope

### Print Statements (Status Quo)
- **Pros**: Simple, no configuration needed
- **Cons**: Not suitable for production, no structure, no rotation
- **Verdict**: Rejected for professional development standards

## References
- [Loguru Documentation](https://loguru.readthedocs.io/)
- [Python Logging Best Practices](https://docs.python.org/3/howto/logging.html)
- [Structured Logging Standards](https://engineering.grab.com/structured-logging)