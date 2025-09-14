# Jump Sky Game Implementation - Revised Plan

**Date**: 2025-09-06  
**Plan Type**: Major Feature - New Game Development  
**Status**: Revised  
**Game Name**: jump_sky

## Project Overview

### Game Concept
One-button fruit collection game where players jump to catch fruits while avoiding flying birds. Players collect fruits for points and must avoid birds to preserve lives.

### Core Mechanics
- **Fruit Collection**: Jump to collect fruits and earn points
- **Bird Avoidance**: Birds fly at jump height - collision occurs ONLY when jumping
- **Strategic Timing**: Players must decide when to jump (for fruits) vs stay grounded (to avoid birds)

## Game Specifications

### Collision Detection (CRITICAL)

#### Bird Collision
- **Trigger**: Player sprite collides with bird sprite ONLY when player is jumping
- **Height Range**: Birds positioned at variable heights within jump range (same as fruits)
- **Effect**: Player loses one life (standard 3-lives system)
- **Priority**: Birds have higher Z-order than fruits

#### Fruit Collision  
- **Trigger**: Player sprite collides with fruit sprite throughout jump arc
- **Height Range**: Fruits positioned at variable heights within jump reach
- **Effect**: Fruit disappears, player gains points based on fruit type
- **Timing**: Collision detection active throughout entire jump arc (not just at peak)

#### Height System (Both Birds and Fruits)
- **Range**: Variable heights within 1.5x player sprite height to full jump height
- **Per-Object**: Each individual bird/fruit has fixed height, but varies across different spawns
- **Collision**: Player must jump to appropriate height to collect fruits or collide with birds

#### Velocity System
- **Fruit Velocity**: Based on point value - higher points = higher velocity (thrown effect)
  - Apple (10pts): Slower velocity
  - Banana (15pts): Medium velocity  
  - Pineapple (20pts): Higher velocity
  - Orange (25pts): Highest velocity
- **Bird Velocity**: Random variation per spawn (independent of other factors)
- **Bird Types**: Multiple bird types with different animations, randomly selected per spawn
- **Effect**: Creates dynamic "thrown fruit" feel, unpredictable bird movement, and visual variety

#### Collision Priority
- **Bird > Fruit**: If player collides with both simultaneously, bird collision takes priority
- **Result**: Player loses life, fruit remains (or disappears - needs testing)

### Scoring System
- **Apple**: 10 points
- **Banana**: 15 points  
- **Pineapple**: 20 points
- **Orange**: 25 points
- **No Survival Points**: Points only from fruit collection

### Spawn System

#### Spawn Ratio
- **Base Ratio**: 1 bird per 4 fruits (configurable)
- **Safe Zones**: Periods with only fruits, no birds
- **Maximum Objects**: 4 simultaneous objects on screen
- **Frequency Control**: Bird frequency relative to fruit frequency (parametrized)

#### Height Distribution
- **Both Birds & Fruits**: Variable heights within jump range (1.5x player height to full jump height)
- **Range**: Approximately 60-150 pixels above ground (configurable based on player sprite size and jump height)
- **Per-Object**: Each spawn gets random height within valid range
- **Ground Level**: Player runs at Y=0 (ground level)

### Difficulty System
- **Scale**: 1-10 (standard Unipress scale)
- **Method**: Speed-based - higher difficulty = faster base object movement
- **Effect**: Less reaction time for jump decisions
- **Velocity Interaction**: Difficulty affects base speed, which is then modified by fruit type or bird randomization

## Technical Implementation

### Simplified Architecture

#### Core Classes
```python
class JumpSkyGame(BaseGame):
    """Main game class with integrated spawn management"""
    
class Bird:
    """Animated flying obstacle with multiple types and animations"""
    # Properties: bird_type, animation, velocity
    # Types: Multiple bird types for visual variety (randomly selected)
    
class Fruit:
    """Static collectible with configurable fruit type and velocity"""
    # Properties: fruit_type, points, velocity, image
    # Types: apple, banana, pineapple, orange
    # Velocity: Based on point value (higher points = higher velocity)
```

#### Removed Over-Engineering
- ❌ Separate SpawnManager class (integrated into main game)
- ❌ Individual fruit subclasses (single Fruit class with type parameter)
- ❌ Excessive configuration parameters (reduced to essentials)

### Project Structure
```
unipress/games/jump_sky/
├── __init__.py
├── game.py                    # Main JumpSkyGame class
├── settings.toml             # Simplified configuration (6-8 parameters)

unipress/assets/images/games/jump_sky/
├── player/                   # Copied from jumper
├── birds/                   # Bird animation frames (user provided)
│   ├── bird1/               # First bird type animation
│   │   ├── bird1_01.png
│   │   ├── bird1_02.png
│   │   ├── bird1_03.png
│   │   └── bird1_04.png
│   ├── bird2/               # Second bird type animation  
│   │   ├── bird2_01.png
│   │   ├── bird2_02.png
│   │   ├── bird2_03.png
│   │   └── bird2_04.png
│   └── bird3/               # Third bird type animation
│       ├── bird3_01.png
│       ├── bird3_02.png
│       ├── bird3_03.png
│       └── bird3_04.png
└── fruits/                  # Static fruit images (user provided)
    ├── apple.png
    ├── banana.png
    ├── pineapple.png
    └── orange.png

unipress/assets/sounds/games/jump_sky/
├── jump.ogg                 # Jump_sky specific sound (user provided)
├── success.ogg             # Used for fruit_catch (user provided)
├── failure.ogg             # Used for bird_touched (user provided)
├── game_start.ogg          # Used for game start (user provided)
└── high_score.ogg          # Used for high score (user provided)

unipress/locales/
├── pl_PL/games/jump_sky.json    # Basic message set
└── en_US/games/jump_sky.json    # English fallback
```

### Simplified Configuration

#### Essential Settings Only (games/jump_sky/settings.toml)
```toml
[jump_sky]
# Physics
gravity = 800
jump_height = 150
object_speed_base = 200

# Spawn system  
fruit_spawn_interval = 3.0
bird_to_fruit_ratio = 0.25     # 1 bird per 4 fruits
max_objects = 4

# Height ranges (both birds and fruits use same range)
height_min = 60               # 1.5x player sprite height
height_max = 150              # Full jump height

# Velocity system
fruit_velocity_multiplier = { apple = 1.0, banana = 1.3, pineapple = 1.6, orange = 2.0 }
bird_velocity_random_range = [0.8, 1.8]  # Random multiplier range for birds

# Bird variety
bird_types = ["bird1", "bird2", "bird3"]  # Available bird types (randomly selected)

# Scoring
fruit_points = { apple = 10, banana = 15, pineapple = 20, orange = 25 }
```

## Development Timeline - MVP Approach

### Phase 1: Core Mechanics (3-4 days)
**Focus**: Get basic gameplay working

**Deliverables**:
- Basic JumpSkyGame class setup with placeholder rectangles
- Player movement and physics (copy from jumper)
- Simple spawn system (fruits and birds as colored rectangles)
- Variable velocity system (fruits by points, birds random)
- Multiple bird types with random selection (different colored rectangles initially)
- Collision detection implementation with correct mechanics
- Basic scoring system

**Asset Requirements**:
- None (use procedural fallback shapes - see Fallback System section)

**Acceptance Criteria**:
- Player can jump and collect rectangle "fruits" for points
- Player loses life when jumping into rectangle "birds"
- Spawn ratio approximately 1 bird per 4 fruits
- Higher-value fruits move faster (thrown effect visible)
- Birds have varying speeds across different spawns
- Different bird types spawn randomly (visible as different colored triangles with animation)
- Fallback visual system works (recognizable fruit shapes, animated bird triangles)
- Score displays correctly

### Phase 2: Assets & Polish (3-4 days)
**Focus**: Replace placeholders with real assets and add polish

**Deliverables**:
- Replace placeholders with user-provided assets
- Bird animation system integration
- Sound event integration  
- UI improvements and feedback
- Settings system integration

**Asset Requirements (User Provided)**:

**Bird Animations** (Multiple Types for Variety):
- Location: `unipress/assets/images/games/jump_sky/birds/`
- **Bird Type 1**: `bird1/bird1_01.png`, `bird1_02.png`, `bird1_03.png`, `bird1_04.png`  
- **Bird Type 2**: `bird2/bird2_01.png`, `bird2_02.png`, `bird2_03.png`, `bird2_04.png`
- **Bird Type 3**: `bird3/bird3_01.png`, `bird3_02.png`, `bird3_03.png`, `bird3_04.png`
- Requirements: 4-frame flying animation per type, consistent size/style across all types
- Selection: Random bird type chosen for each spawn
- Animation metadata will be auto-generated for each type

**Fruit Images**:
- Location: `unipress/assets/images/games/jump_sky/fruits/`
- Files: `apple.png`, `banana.png`, `pineapple.png`, `orange.png`  
- Requirements: Static images, recognizable fruit shapes, consistent style/size

**Player Assets**: Will be copied from jumper game or use fallback shapes

**Sound Assets**: User provided or fallback to global sounds

**Acceptance Criteria**:
- All assets display correctly with proper animations
- Sound events trigger at appropriate times
- Professional visual and audio feedback

### Phase 3: Testing & Integration (2-3 days)
**Focus**: Quality assurance and final integration

**Deliverables**:
- Comprehensive testing across difficulty levels
- Performance optimization
- End game screen integration
- High score system integration
- Final balancing and polish

**Asset Requirements**:
- None (all assets from Phase 2)

**Acceptance Criteria**:
- Balanced gameplay across all difficulty levels (1-10)
- Stable performance with maximum objects
- Proper integration with Unipress framework
- All quality checks pass

## Asset Integration Strategy

### User Asset Delivery Points
1. **Phase 1 → Phase 2 Transition**: User provides all required assets
2. **Asset Specifications**: Provided during Phase 1 after placeholder testing
3. **Integration Support**: Step-by-step guidance for asset placement

### Asset Quality Requirements
- **Bird Frames**: PNG format, transparent background, 64x64 or 128x128 pixels per type
- **Bird Variety**: 3 different bird types (e.g., different species, colors, or sizes) for visual variety
- **Fruit Images**: PNG format, transparent background, similar size to birds
- **Style Consistency**: Cartoon/stylized matching existing jumper game aesthetic across all assets

### Fallback System (Missing Assets)

#### Visual Asset Fallbacks
**Fruits (if images missing)**:
- **Apple**: Green circle with red border (simple, recognizable)
- **Banana**: Yellow crescent shape
- **Pineapple**: Orange diamond/rhombus shape
- **Orange**: Orange circle with small texture lines

**Birds (if animations missing)**:
- **Bird1**: Red triangle pointing right with simple wing flap (rotate slightly for animation)
- **Bird2**: Blue triangle pointing right with wing flap
- **Bird3**: Purple triangle pointing right with wing flap
- **Animation**: Simple 2-frame flap (triangle + triangle rotated 15°)

**Player (if sprites missing)**:
- **Running**: Blue rectangle with simple "legs" animation (white rectangles moving)
- **Jumping**: Same blue rectangle with legs together

**Background Layers (if textures missing)**:
- **Sky**: Light blue gradient (#87CEEB to #B0E0E6)
- **Mountains**: Dark gray triangular shapes (#696969)
- **Far Trees**: Dark green rectangles (#228B22)
- **Near Trees**: Green rectangles (#32CD32)
- **Ground**: Brown rectangle (#8B4513)

#### Audio Asset Fallbacks
**Sound Events (if OGG files missing)**:
- **Simple Approach**: Silent fallback (no crash)
- **Implementation**: Graceful degradation - if sound file missing, continue without audio
- **User Responsibility**: Provide sound assets for full audio experience

#### Fallback Implementation Strategy
```python
# Example fallback approach
def load_fruit_texture(fruit_type):
    try:
        return load_texture(f"fruits/{fruit_type}.png")
    except FileNotFoundError:
        return create_fallback_fruit_shape(fruit_type)

def create_fallback_fruit_shape(fruit_type):
    # Generate procedural shapes as backup
    shapes = {
        "apple": draw_circle_with_border(GREEN, RED),
        "banana": draw_crescent_shape(YELLOW),
        "pineapple": draw_diamond_shape(ORANGE),
        "orange": draw_textured_circle(ORANGE)
    }
    return shapes.get(fruit_type, draw_circle(GRAY))
```

#### Development Benefits
- **No Asset Dependency**: Development can proceed without waiting for assets
- **Easy Testing**: Immediate visual feedback with fallback shapes
- **Gradual Migration**: Replace fallbacks with real assets incrementally
- **Error Resilience**: Game never crashes due to missing assets

## Risk Management

### Simplified Risk Profile
- **Medium Risk**: Asset quality and bird animation timing
- **Low Risk**: Core mechanics (similar to proven jumper game)
- **Very Low Risk**: Missing assets (comprehensive fallback system)
- **Mitigation**: Fallback-first development approach with graceful asset loading

### Success Metrics
- **Technical**: All quality checks pass, 60+ FPS performance
- **Gameplay**: Balanced difficulty progression, engaging fruit collection
- **Timeline**: Completed within 8-10 days

## Future Enhancements (Post-MVP)
- Additional bird types with different flying patterns
- Special fruits with unique effects
- Power-ups and temporary abilities
- Enhanced particle effects
- Background music integration

---

**Plan Status**: Ready for Implementation  
**Estimated Timeline**: 8-10 days (3 phases)  
**Key Success Factors**: Simple architecture, user-provided assets, MVP focus

This revised plan addresses all critical review issues while maintaining focus on delivering a working game quickly and efficiently.