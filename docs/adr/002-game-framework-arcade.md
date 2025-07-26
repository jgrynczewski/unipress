# ADR-002: Use Arcade for Game Framework

## Status
Accepted

## Context
We need to choose a game framework for creating one-button games in Python. Main options:
- **pygame**: Classic, widely used, but older API
- **arcade**: Modern Python game library with clean API
- **pyglet**: Lightweight OpenGL wrapper
- **panda3d**: 3D-focused, overkill for our needs

## Decision
We will use **Arcade** as our game framework.

## Rationale
- **Modern API**: Clean, Pythonic interface designed for modern Python
- **2D Focus**: Perfect for simple one-button games
- **Active Development**: Regularly updated with new features
- **Great Documentation**: Excellent tutorials and examples
- **Performance**: Good performance for 2D games
- **Easy to Learn**: Intuitive API reduces boilerplate code
- **Built-in Features**: Sprite handling, collision detection, sound, etc.

## Consequences
- Clean, readable game code
- Less boilerplate compared to pygame
- Smaller community than pygame (but growing)
- Modern Python features and best practices
- Good performance for our use case

## Implementation
- Use `uv add arcade` to install
- Create game classes inheriting from `arcade.Window`
- Use arcade's sprite and scene systems
- Leverage built-in physics and collision detection