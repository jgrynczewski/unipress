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

### 2. Input Standard - ONE-BUTTON CONSTRAINT
- **Primary Input**: Left mouse button click (BINARY SIGNAL ONLY)
- **CRITICAL CONSTRAINT**: Players CANNOT move cursors, select UI elements, or target coordinates
- **Required Mechanics**: All interactions via timing, automatic cycling, or sequences
- **Implementation**: Input handling abstracted for binary signals only

**FUNDAMENTAL PRINCIPLE**: This is a one-button game collection. Players can only send a binary signal (press/release) and cannot perform any cursor-based interactions, targeting, or selection. Every game mechanic and UI element must be designed around this absolute constraint.

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

## End Game Screen Standard
**Decision**: All games use standardized end game screen with cycling buttons.

**Rationale**:
- Consistent user experience across all games
- Reduces development effort through shared components
- Professional appearance with proper UX patterns
- Supports internationalization and future customization

**Implementation**:
- Shared UI component in `unipress/ui/end_game/screen.py`
- Two cycling buttons: "Play Again" and "Exit"
- Click cycles between options, selected button highlighted
- Integrated into BaseGame, automatically shown on game over
- Fully localized with Polish/English support
- Foundation for per-game asset customization