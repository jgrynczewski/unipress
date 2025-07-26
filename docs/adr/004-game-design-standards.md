# ADR-004: Game Design Standards

## Status
Accepted

## Context
We need consistent standards across all one-button games in the Unipress collection to ensure:
- Unified difficulty system
- Consistent input handling
- Easy configuration and modification

## Decision
All games must follow these design standards:

### 1. Difficulty System
- **Scale**: 1-10 difficulty levels
  - **1**: Trivial (longest reaction time)
  - **10**: Hard but fair (shortest reaction time)
- **Implementation**: Each game defines reaction time windows based on difficulty
- **Configuration**: Easily changeable via game constructor parameter

### 2. Input Standard
- **Primary Input**: Left mouse button click
- **Requirement**: Input method must be easily configurable
- **Implementation**: Input handling abstracted to allow easy modification

### 3. Game Structure
- All games inherit from base game class
- Consistent difficulty and input configuration
- Clear separation of game logic from input/difficulty settings

## Rationale
- **Accessibility**: Players can adjust difficulty to their skill level
- **Consistency**: Unified experience across all games
- **Flexibility**: Easy to modify for different input devices or difficulty curves
- **Scalability**: New games automatically follow established patterns

## Consequences
- All games must implement difficulty scaling
- Base game framework provides consistent structure
- Input handling is abstracted and configurable
- Easier testing with different difficulty levels

## Implementation
- Create `BaseGame` class with difficulty and input parameters
- Difficulty affects reaction time windows (higher = shorter time)
- Input method configurable via game settings
- All games extend `BaseGame` and implement difficulty-specific logic