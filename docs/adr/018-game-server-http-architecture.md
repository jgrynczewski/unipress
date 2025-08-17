# 018. Game Server HTTP Architecture

## Status

Accepted

## Context

The Unipress project needs a way to run games in a Docker container and allow external processes to launch different games quickly. The current approach of starting a new container for each game is slow and resource-intensive.

## Decision

We will implement a **HTTP server architecture** that runs inside the Docker container and provides REST API endpoints for game management.

## Consequences

### Positive

- **Fast game launching**: Server is always running, games start immediately
- **Resource efficiency**: Single container instance instead of multiple
- **API integration**: Easy integration with other applications
- **Game management**: Ability to stop, check status, and manage running games
- **Scalability**: Easy to add new games without container changes
- **Monitoring**: Built-in health checks and status endpoints
- **Audio support**: Maintains full audio functionality through PipeWire
- **Isolation**: Games run in isolated processes within the container

### Negative

- **Complexity**: Additional layer of HTTP server code
- **Dependencies**: HTTP server library added to project
- **Error handling**: More complex error scenarios to handle
- **Security**: HTTP API exposed (mitigated by localhost-only access)
- **Process management**: Need to handle subprocess lifecycle

## Alternatives Considered

### 1. Unix Domain Sockets
**Pros:**
- Very fast communication
- No network overhead
- Secure (file system permissions)

**Cons:**
- Platform-specific (Linux/Unix only)
- More complex client implementation
- Limited to local communication
- Harder to debug and monitor

### 2. Named Pipes (FIFO)
**Pros:**
- Simple implementation
- Fast communication
- Built into Unix systems

**Cons:**
- One-way communication only
- Complex bidirectional communication setup
- Platform-specific
- Limited error handling

### 3. Message Queues (Redis/RabbitMQ)
**Pros:**
- Robust message handling
- Built-in persistence
- Advanced routing capabilities

**Cons:**
- Additional infrastructure dependency
- Overkill for simple game launching
- Increased complexity
- Resource overhead

### 4. gRPC
**Pros:**
- High performance
- Strong typing
- Bidirectional streaming
- Modern protocol

**Cons:**
- Complex setup and dependencies
- Steep learning curve
- Overkill for simple game management
- Additional build complexity

### 5. WebSocket
**Pros:**
- Real-time bidirectional communication
- Persistent connections
- Good for status updates

**Cons:**
- More complex than REST API
- Overkill for simple request/response
- Connection management overhead
- Not ideal for one-shot operations

## Implementation Details

### Server Architecture
```python
# HTTP server with endpoints:
GET /health              # Server health check
GET /games/list          # List available games
POST /games/run          # Start a game
POST /games/stop         # Stop current game
GET /games/status        # Game status
```

### Client Implementation
```python
# Python client with methods:
client.health_check()
client.list_games()
client.run_game(game, difficulty)
client.stop_game()
client.game_status()
```

### Process Management
- Games run as subprocesses in background threads
- Automatic cleanup of terminated processes
- PID tracking for status monitoring
- Graceful shutdown handling

## Technical Considerations

### Audio Support
- Server maintains audio context and permissions
- Games inherit audio capabilities from server process
- PipeWire socket access preserved through container configuration

### Error Handling
- Comprehensive exception handling in all endpoints
- Detailed error responses with status codes
- Logging of all operations for debugging

### Performance
- Minimal overhead for HTTP communication
- Fast subprocess spawning
- Efficient process monitoring

### Security
- Localhost-only access (no external network exposure)
- Input validation for all parameters
- No authentication needed for local development

## Migration Strategy

1. **Phase 1**: Implement server alongside existing direct execution
2. **Phase 2**: Update documentation to recommend server approach
3. **Phase 3**: Deprecate direct execution (keep for compatibility)
4. **Phase 4**: Remove direct execution code (future)

## Related Decisions

- [017-containerization-docker-uv.md](./017-containerization-docker-uv.md) - Container architecture
- [016-comprehensive-sound-system.md](./016-comprehensive-sound-system.md) - Audio system
- [012-logging-system.md](./012-logging-system.md) - Logging infrastructure
- [019-http-server-framework-selection.md](./019-http-server-framework-selection.md) - HTTP framework choice

## References

- [REST API Design Best Practices](https://restfulapi.net/)
- [Docker Container Communication](https://docs.docker.com/network/)
- [Python subprocess module](https://docs.python.org/3/library/subprocess.html)
