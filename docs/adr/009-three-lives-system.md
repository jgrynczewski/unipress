# ADR-009: Three Lives System Standard

## Status
Accepted

## Context
Games should provide players with multiple chances to improve their performance while maintaining engagement. A lives system allows players to learn from mistakes without immediately losing all progress.

## Decision
All Unipress games will implement a **3-lives system by default** where:
- Players start with 3 lives
- Each failure/death loses 1 life and restarts the game state
- Score is maintained across life losses
- Final game over occurs only when all lives are exhausted

## Implementation Details

### Lives Configuration
- **Default**: 3 lives per game
- **Configurable**: Games can override via `BaseGame(lives=N)` parameter
- **Display**: Lives shown in UI as "Lives: 2/3" format
- **Persistence**: Lives count decreases on death, score persists

### Game State Management
- **Life Loss**: `lose_life()` method decreases lives and calls `reset_game()`
- **Score Persistence**: Score maintained across deaths within same session
- **Game Reset**: Only game state resets, not score or lives remaining
- **Final Game Over**: Triggered only when `lives <= 0`

### Method Usage
- **Games should call**: `self.lose_life()` on player death/failure
- **Deprecated method**: `self.end_game()` (immediately ends game)
- **Automatic handling**: BaseGame manages lives logic and UI display

## Rationale

### Player Experience
- **Learning Opportunity**: Multiple chances to improve and learn patterns
- **Reduced Frustration**: Immediate game over can be discouraging
- **Progress Persistence**: Maintaining score provides sense of advancement
- **Fair Challenge**: Balances difficulty with reasonable retry chances

### Arcade Game Tradition
- **Classic Pattern**: Traditional arcade games used lives systems
- **Familiar Mechanic**: Players understand lives concept intuitively
- **Engagement**: Provides tension without being punitive
- **Replayability**: Encourages "just one more try" mentality

### Implementation Benefits
- **Consistent Experience**: All games behave identically
- **Simple Integration**: Built into BaseGame, automatic for all games
- **Configurable**: Games can adjust lives count if needed
- **Clear UI**: Lives display provides immediate feedback

## Consequences

### Positive
- **Better Player Experience**: More forgiving and engaging gameplay
- **Consistent UX**: Uniform behavior across all games
- **Score Progression**: Players see cumulative progress across attempts
- **Developer Simplicity**: One method call (`lose_life()`) handles everything

### Considerations
- **Game Balance**: Must ensure games aren't too easy with 3 lives
- **UI Space**: Lives display takes additional screen real estate
- **Different Game Types**: Some games might not suit lives system perfectly

## Technical Implementation
- Added `lives` and `max_lives` attributes to BaseGame
- Added configurable `lives: int = 3` parameter to constructor
- Implemented `lose_life()` method with automatic state management
- Updated UI to display lives count prominently
- Modified game start logic to reset lives and score

## Game Integration
Games should replace `self.end_game()` calls with `self.lose_life()` for proper lives system behavior. The BaseGame handles all lives logic automatically.

## Future Considerations
- Could add bonus life mechanics for high scores
- Possible lives refill items or power-ups in specific games
- May add different lives counts for different difficulty levels