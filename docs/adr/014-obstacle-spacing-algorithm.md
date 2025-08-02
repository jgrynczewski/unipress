# ADR-014: Obstacle Spacing Algorithm

## Status
Accepted

## Context
Games like jumper require carefully calculated obstacle spacing to ensure fair gameplay. Players need sufficient time between obstacles to react and perform consecutive jumps, especially at higher difficulty levels. Without proper spacing algorithm, the game becomes either too easy (obstacles too far apart) or unfairly difficult (obstacles too close together).

The spacing must:
- Scale appropriately with player physics (jump duration)
- Account for human reaction time limitations
- Maintain challenge while ensuring fairness
- Work consistently across different difficulty levels

## Decision
Implement a physics-based obstacle spacing algorithm that calculates minimum safe intervals based on jump mechanics and adds safety margins for human reaction time.

### Algorithm Components

1. **Jump Duration Calculation**
   ```
   jump_duration = 2 * sqrt(2 * jump_height / gravity)
   ```
   - Physics-based calculation for complete jump cycle
   - Accounts for variable jump heights across difficulty levels

2. **Safety Margin**
   ```
   min_safe_interval = jump_duration * 1.44  // 44% safety margin
   ```
   - Started with 20% margin (1.2x multiplier)
   - Increased to 44% margin (1.44x multiplier) after user feedback
   - Provides buffer time for consecutive jumps

3. **Base Minimum**
   ```
   base_interval = max(min_safe_interval, 2.5)  // At least 2.5 seconds
   ```
   - Ensures absolute minimum 2.5 second spacing
   - Prevents extremely fast obstacle sequences

4. **Randomization**
   ```
   final_interval = base_interval * random.uniform(0.8, 2.5)
   ```
   - Adds unpredictability to gameplay
   - Range: 80% to 250% of base interval
   - Prevents monotonous patterns

### Implementation
- Applied in `JumperGame.__init__()` for initial obstacle
- Recalculated in `JumperGame.on_update()` after each obstacle spawn
- Uses current difficulty level for jump height calculation

## Rationale
- **Physics-based**: Grounded in actual jump mechanics, not arbitrary values
- **Scalable**: Automatically adjusts to different difficulty levels and jump heights
- **Human-centered**: Includes reaction time buffers for fair gameplay
- **Tested**: Refined through gameplay feedback (20% increase in spacing)
- **Maintainable**: Clear mathematical formula, easy to adjust safety margins

## Consequences

### Positive
- Consistent, fair obstacle spacing across all difficulty levels
- Mathematically guaranteed minimum safe distance
- Easy to tune by adjusting safety margin multiplier
- Prevents impossible obstacle sequences
- Maintains game challenge through randomization

### Negative
- More complex than fixed time intervals
- Requires physics calculations on each spawn
- May need further tuning based on user feedback
- Safety margin is somewhat arbitrary (requires empirical testing)

## Related
- ADR-004: Game Design Standards (difficulty system)
- ADR-009: Three Lives System (failure recovery)
- Commit history: "feat: 🎸 implement random obstacle spawning with safe minimum intervals"
- Recent refinement: "feat: 🎸 increase minimum obstacle spacing by 20%"