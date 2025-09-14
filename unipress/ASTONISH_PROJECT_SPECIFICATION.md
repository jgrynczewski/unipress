# Astonish Project Specification

## Project Overview

**Astonish** is a new one-button game for the Unipress framework that combines puzzle-solving mechanics with timing-based challenges. The game features a unique "memory revelation" system where players must remember and recreate patterns while managing limited resources and time pressure.

## Core Concept

Players control an **Astronomer** character who must observe and recreate **constellation patterns** in the night sky. The game combines:
- **Memory challenges**: Observe constellation patterns and recreate them
- **Timing mechanics**: Limited time windows for pattern completion
- **Resource management**: Limited "telescope energy" for observations
- **Progressive difficulty**: Patterns become more complex and time windows shorter

## Game Mechanics

### Primary Gameplay Loop

1. **Observation Phase** (3-5 seconds)
   - Constellation pattern appears in the sky
   - Player must memorize the pattern
   - Telescope energy decreases during observation

2. **Recreation Phase** (5-8 seconds)
   - Pattern disappears
   - Player clicks to place stars in the correct positions
   - Time pressure increases with difficulty

3. **Validation Phase** (1 second)
   - Pattern is checked for accuracy
   - Points awarded based on precision and speed
   - New pattern begins

### Constellation System

#### Pattern Types
- **Simple Stars**: 3-4 star patterns (Difficulty 1-3)
- **Complex Constellations**: 5-7 star patterns (Difficulty 4-6)
- **Mythological Figures**: 8-12 star patterns (Difficulty 7-10)

#### Star Properties
- **Brightness**: Affects visibility and point value
- **Color**: Different colors for different star types
- **Size**: Visual indicator of star importance
- **Position**: Precise coordinates for pattern matching

### Resource Management

#### Telescope Energy
- **Starting Energy**: 100 units
- **Observation Cost**: 5-15 units per pattern (scales with complexity)
- **Recharge Rate**: 1 unit per second when not observing
- **Energy Depletion**: Game over when energy reaches 0

#### Time Pressure
- **Observation Time**: 3-5 seconds (decreases with difficulty)
- **Recreation Time**: 5-8 seconds (decreases with difficulty)
- **Bonus Time**: Extra time for perfect patterns

### Scoring System

#### Base Scoring
- **Perfect Match**: 100 points + time bonus
- **Near Perfect**: 75 points (1-2 stars off)
- **Good Match**: 50 points (3-4 stars off)
- **Poor Match**: 25 points (5+ stars off)
- **Failed Pattern**: 0 points + energy penalty

#### Bonus Multipliers
- **Speed Bonus**: Up to 2x for quick completion
- **Energy Efficiency**: Bonus for low energy usage
- **Streak Bonus**: Multiplier for consecutive perfect patterns
- **Difficulty Bonus**: Higher points for harder patterns

## Technical Architecture

### Game Structure

```
astonish/
├── __init__.py
├── game.py              # Main game class
├── settings.toml        # Game-specific configuration
├── constellation.py     # Pattern generation and validation
├── telescope.py         # Energy management system
├── star.py             # Individual star objects
└── patterns/           # Predefined constellation patterns
    ├── simple.json
    ├── complex.json
    └── mythological.json
```

### Core Classes

#### AstonishGame (BaseGame)
- Main game controller
- Manages game states and transitions
- Handles input and UI rendering

#### Constellation
- Pattern generation and storage
- Validation logic for player input
- Difficulty scaling algorithms

#### Telescope
- Energy management system
- Observation mechanics
- Recharge and depletion logic

#### Star
- Individual star properties
- Position and visual representation
- Collision detection for placement

### Settings Configuration

```toml
[astonish]
# Gameplay settings
observation_time_base = 4.0
recreation_time_base = 6.0
energy_start = 100
energy_observation_cost = 10

# Difficulty scaling
time_reduction_per_level = 0.2
energy_cost_increase = 1.5
pattern_complexity_increase = 1.2

# Scoring
perfect_match_points = 100
near_perfect_points = 75
good_match_points = 50
poor_match_points = 25

# Visual settings
star_size_base = 8
constellation_fade_time = 1.0
pattern_reveal_duration = 0.5

# Pattern generation
max_stars_simple = 4
max_stars_complex = 7
max_stars_mythological = 12
```

## Visual Design

### Art Style
- **Celestial Theme**: Deep space background with nebula effects
- **Star Rendering**: Glowing stars with particle effects
- **UI Elements**: Telescope-themed interface
- **Color Palette**: Deep blues, purples, and gold accents

### Visual Effects
- **Star Placement**: Particle burst on successful placement
- **Pattern Completion**: Constellation lines connecting stars
- **Energy Visualization**: Telescope energy bar with glow effects
- **Time Pressure**: Screen edge pulsing as time runs out

### Fallback Graphics
- **Simple Stars**: Colored circles with glow effects
- **Constellation Lines**: Dashed lines connecting stars
- **Background**: Gradient from dark blue to black
- **UI Elements**: Clean, minimalist design

## Audio Design

### Sound Effects
- **Star Placement**: Soft chime for correct placement
- **Pattern Complete**: Triumphant chord progression
- **Energy Low**: Warning beep when energy < 20%
- **Time Warning**: Ticking sound in final 2 seconds
- **Perfect Match**: Special achievement sound

### Music
- **Ambient Space**: Ethereal, atmospheric background music
- **Tension Building**: Music intensity increases with time pressure
- **Victory Theme**: Celebratory music for perfect patterns

## Localization

### Supported Languages
- English (en_US)
- Polish (pl_PL)
- Spanish (es_ES)
- French (fr_FR)

### Key Messages
```json
{
  "ui": {
    "instructions": "Observe the constellation, then recreate it by clicking to place stars!",
    "click_to_start": "Click to start Astonish",
    "observation_phase": "Observe the constellation...",
    "recreation_phase": "Recreate the pattern!",
    "energy_low": "Telescope energy low!",
    "time_warning": "Time running out!",
    "perfect_match": "Perfect constellation!",
    "energy_depleted": "Telescope energy depleted!"
  },
  "gameplay": {
    "star_placed": "Star placed!",
    "pattern_complete": "Constellation complete!",
    "energy_remaining": "Energy: {energy}%",
    "time_remaining": "Time: {time}s",
    "score": "Score: {score}",
    "streak": "Streak: {count}"
  }
}
```

## Difficulty Progression

### Level 1-3: Simple Stars
- 3-4 star patterns
- 4-second observation time
- 6-second recreation time
- 10 energy cost per pattern

### Level 4-6: Complex Constellations
- 5-7 star patterns
- 3.5-second observation time
- 5-second recreation time
- 15 energy cost per pattern

### Level 7-10: Mythological Figures
- 8-12 star patterns
- 3-second observation time
- 4-second recreation time
- 20 energy cost per pattern

## Implementation Roadmap

### Phase 1: Core Framework (Week 1)
- [ ] Set up basic game structure
- [ ] Implement BaseGame inheritance
- [ ] Create basic star placement system
- [ ] Add simple pattern generation

### Phase 2: Game Mechanics (Week 2)
- [ ] Implement constellation system
- [ ] Add energy management
- [ ] Create timing mechanics
- [ ] Build scoring system

### Phase 3: Visual Polish (Week 3)
- [ ] Add visual effects
- [ ] Implement fallback graphics
- [ ] Create UI elements
- [ ] Add animation systems

### Phase 4: Audio & Polish (Week 4)
- [ ] Integrate sound effects
- [ ] Add background music
- [ ] Implement localization
- [ ] Final testing and balancing

## Technical Requirements

### Dependencies
- Python 3.8+
- Arcade 2.6+
- TOML parsing (tomli)
- JSON pattern files

### Performance Targets
- 60 FPS on standard hardware
- < 100MB memory usage
- < 50MB disk space
- < 2 second startup time

### Compatibility
- Windows 10+
- macOS 10.14+
- Linux (Ubuntu 18.04+)
- Fullscreen and windowed modes

## Testing Strategy

### Unit Tests
- Pattern generation algorithms
- Scoring calculations
- Energy management logic
- Collision detection

### Integration Tests
- Game state transitions
- Input handling
- Audio system integration
- Localization loading

### Performance Tests
- Memory usage monitoring
- Frame rate stability
- Load time optimization
- Stress testing with complex patterns

## Future Enhancements

### Potential Features
- **Multiplayer Mode**: Competitive constellation recreation
- **Custom Patterns**: Player-created constellation sharing
- **Achievement System**: Unlockable rewards and milestones
- **Daily Challenges**: Special patterns with unique rewards
- **VR Support**: Immersive 3D constellation recreation

### Modding Support
- Custom pattern file format
- Mod loader integration
- Community pattern sharing
- Visual theme customization

## Success Metrics

### Player Engagement
- Average session length: 5-10 minutes
- Completion rate: 70%+ for simple patterns
- Return rate: 40%+ for repeat play

### Technical Performance
- Crash rate: < 0.1%
- Load time: < 2 seconds
- Memory usage: < 100MB peak

### Accessibility
- Colorblind-friendly design
- Adjustable timing for accessibility
- Clear visual feedback
- Simple one-button control scheme

---

This specification provides a comprehensive foundation for developing the Astonish game within the Unipress framework. The design emphasizes the core one-button gameplay while introducing innovative memory and timing mechanics that will create engaging, challenging gameplay experiences.
