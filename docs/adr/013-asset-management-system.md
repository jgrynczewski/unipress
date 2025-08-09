# ADR-013: Asset Management System

## Status
Accepted

## Context
The Jumper game requires comprehensive asset management for sprites, animations, sounds, and backgrounds. We need a standardized system that can be reused across all games in the Unipress collection.

## Decision

### Asset Directory Structure
```
unipress/assets/
├── images/
│   ├── global/                    # Shared across all games
│   │   ├── ui/                   # UI elements (buttons, icons)
│   │   └── backgrounds/          # Reusable backgrounds
│   └── games/
│       └── {game_name}/          # Per-game assets
│           ├── player/           # Player character sprites
│           │   ├── idle/         # Idle animation frames
│           │   ├── running/      # Running animation frames
│           │   ├── jumping/      # Jumping animation frames
│           │   └── collision/    # Collision/death animation frames
│           ├── obstacles/        # Obstacle sprites
│           │   ├── {obstacle_type}/  # Each obstacle type
│           │   │   ├── idle/     # Static/idle frames
│           │   │   └── active/   # Active/animated frames
│           └── backgrounds/      # Game-specific backgrounds
│               ├── layers/       # Parallax scrolling layers
│               └── tiles/        # Tileable background elements
├── sounds/
│   ├── global/                   # Shared sound effects
│   │   ├── ui/                  # UI sounds (clicks, transitions)
│   │   └── music/               # Background music
│   └── games/
│       └── {game_name}/         # Per-game sounds
│           ├── player/          # Player action sounds
│           ├── obstacles/       # Obstacle-related sounds
│           └── ambient/         # Background/ambient sounds
└── fonts/                       # Custom fonts (if needed)
    ├── global/                  # Shared fonts
    └── games/                   # Game-specific fonts
```

### Asset Naming Conventions

#### Image Assets
- **Format**: PNG for sprites, JPG for backgrounds (if no transparency needed)
- **Naming**: `{element}_{action}_{frame_number}.png`
  - Examples: `player_running_001.png`, `fire_burning_003.png`
- **Frame numbering**: Zero-padded 3 digits (001, 002, 003...)
- **Resolution**: Base resolution 64x64 for sprites, scalable for backgrounds

#### Sound Assets
- **Format**: OGG Vorbis (open source, good compression)
- **Naming**: `{action}_{variant}.ogg`
  - Examples: `jump_01.ogg`, `collision_01.ogg`, `success_02.ogg`
- **Variants**: Multiple versions of same sound for variety

#### Animation Configuration
- **Format**: JSON metadata files alongside sprites
- **Naming**: `{element}_{action}_anim.json`
- **Contains**: Frame duration, loop settings, next animation

### Animation System Standards

#### Animation Metadata Format
```json
{
  "name": "player_running",
  "frames": [
    {
      "file": "player_running_001.png",
      "duration": 0.1,
      "hitbox": {"x": 16, "y": 16, "width": 32, "height": 48}
    },
    {
      "file": "player_running_002.png", 
      "duration": 0.1,
      "hitbox": {"x": 16, "y": 16, "width": 32, "height": 48}
    }
  ],
  "loop": true,
  "next_animation": null,
  "sound_triggers": {
    "frame_0": "footstep_01.ogg"
  }
}
```

#### Background System Standards
```json
{
  "name": "forest_background",
  "layers": [
    {
      "file": "sky_layer.png",
      "scroll_speed": 0.1,
      "repeat": "horizontal"
    },
    {
      "file": "trees_far.png", 
      "scroll_speed": 0.3,
      "repeat": "horizontal"
    },
    {
      "file": "trees_near.png",
      "scroll_speed": 0.8, 
      "repeat": "horizontal"
    }
  ]
}
```

## Asset Loading System

### Core Components
1. **AssetManager**: Central asset loading and caching
2. **AnimationSystem**: Handles sprite animation playback
3. **SoundManager**: Audio playback and management
4. **BackgroundRenderer**: Parallax scrolling backgrounds

### Performance Considerations
- **Lazy Loading**: Load assets only when needed
- **Caching**: Keep frequently used assets in memory
- **Preloading**: Load next level assets during gameplay
- **Compression**: Use appropriate compression for asset types

## Game Integration

### BaseGame Extensions
- Add asset loading methods to BaseGame
- Provide animation and sound utilities
- Handle asset cleanup on game end

### Settings Integration
- Asset quality settings (high/medium/low)
- Sound volume controls
- Animation frame rate settings

## Rationale

### Benefits
- **Consistency**: Standardized structure across all games
- **Reusability**: Shared assets reduce duplication
- **Scalability**: Easy to add new games and asset types
- **Performance**: Efficient loading and caching system
- **Flexibility**: JSON metadata allows complex animations

### Trade-offs
- **Complexity**: More complex than simple image loading
- **Memory**: Caching may use more memory
- **Setup**: Initial setup overhead for each game

## Implementation Plan

1. Create asset directory structure
2. Implement AssetManager core class
3. Add animation system with JSON metadata
4. Integrate sound management
5. Create background rendering system
6. Update BaseGame with asset utilities
7. Implement Jumper game as first test case

## Future Considerations

- Asset compression and optimization tools
- Runtime asset generation for procedural elements
- Asset streaming for larger games
- Integration with external asset pipelines
- Asset versioning and updates

## Appendix: Asset Libraries (References)

- https://craftpix.net/ — Curated 2D game assets (sprites, UI, tilesets). License varies by pack; verify per asset/library (commercial-friendly packs available).