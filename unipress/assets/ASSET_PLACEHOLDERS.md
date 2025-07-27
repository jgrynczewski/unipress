# Asset Placeholders

This file documents the expected asset files for the Jumper game. 
These are placeholders that need to be replaced with actual artwork and sounds.

## Required Image Assets

### Player Sprites (64x64 pixels, PNG format)
**Running Animation (8 frames):**
- `player/running/player_running_001.png` - Running animation frame 1
- `player/running/player_running_002.png` - Running animation frame 2  
- `player/running/player_running_003.png` - Running animation frame 3
- `player/running/player_running_004.png` - Running animation frame 4
- `player/running/player_running_005.png` - Running animation frame 5
- `player/running/player_running_006.png` - Running animation frame 6
- `player/running/player_running_007.png` - Running animation frame 7
- `player/running/player_running_008.png` - Running animation frame 8

**Jumping Animation (6 frames):**
- `player/jumping/player_jumping_001.png` - Jump start frame
- `player/jumping/player_jumping_002.png` - Jump takeoff frame
- `player/jumping/player_jumping_003.png` - Jump mid-air frame 1
- `player/jumping/player_jumping_004.png` - Jump mid-air frame 2
- `player/jumping/player_jumping_005.png` - Jump landing preparation frame
- `player/jumping/player_jumping_006.png` - Jump landing frame

**Collision Animation:**
- `player/collision/player_collision_001.png` - Collision/death frame

### Obstacle Sprites (64x64 pixels, PNG format)
**Fire Animation (5 frames):**
- `obstacles/fire/active/fire_burning_001.png` - Fire animation frame 1
- `obstacles/fire/active/fire_burning_002.png` - Fire animation frame 2
- `obstacles/fire/active/fire_burning_003.png` - Fire animation frame 3
- `obstacles/fire/active/fire_burning_004.png` - Fire animation frame 4
- `obstacles/fire/active/fire_burning_005.png` - Fire animation frame 5

### Background Layers (Scrollable width, 600px height, PNG format)
- `backgrounds/layers/sky_layer.png` - Back layer (clouds, sky)
- `backgrounds/layers/mountains_far.png` - Far mountains
- `backgrounds/layers/trees_far.png` - Distant trees
- `backgrounds/layers/trees_near.png` - Near trees  
- `backgrounds/layers/ground_layer.png` - Ground/grass layer

## Required Sound Assets

### Player Sounds (OGG format)
- `player/jump_01.ogg` - Jump sound effect
- `player/footstep_01.ogg` - Footstep sound 1
- `player/footstep_02.ogg` - Footstep sound 2
- `player/collision_01.ogg` - Collision/death sound

### Obstacle Sounds (OGG format)  
- `obstacles/fire_crackle_01.ogg` - Fire crackling sound
- `obstacles/fire_whoosh_01.ogg` - Fire whoosh when jumped over

### Ambient Sounds (OGG format)
- `ambient/forest_ambience.ogg` - Background forest sounds
- `ambient/success_chord.ogg` - Success/score sound

## Global Assets (Shared)

### UI Sounds (OGG format)
- `sounds/global/ui/button_click.ogg` - Button click sound
- `sounds/global/ui/game_over.ogg` - Game over sound
- `sounds/global/ui/new_high_score.ogg` - New high score celebration

### UI Images (PNG format)
- `images/global/ui/button_background.png` - Standard button background
- `images/global/ui/lives_icon.png` - Lives indicator icon
- `images/global/ui/score_icon.png` - Score indicator icon

## Asset Creation Guidelines

1. **Sprites**: 64x64 base resolution, can be scaled up
2. **Backgrounds**: Tileable horizontally for seamless scrolling
3. **Sounds**: Short (< 2 seconds) for effects, longer for ambient
4. **Format**: PNG for images (transparency support), OGG for sounds
5. **Style**: Consistent pixel art or cartoon style across all assets
6. **Colors**: Bright, contrasting colors for good visibility

## Implementation Notes

- All assets will be loaded through the AssetManager system
- Animations defined in JSON metadata files (_anim.json)
- Missing assets will log errors but won't crash the game
- Placeholder colored rectangles used until real assets available