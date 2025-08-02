# ADR-016: Comprehensive Sound System Architecture

## Status
Accepted

## Context
The Unipress project needs a comprehensive sound system that provides immersive audio feedback for all game events. Currently, the jumper game has basic sound support, but lacks proper volume control, comprehensive event coverage, and game startup synchronization. 

A standardized sound system is needed that:
- Provides consistent audio feedback across all games
- Supports volume control and user preferences
- Handles game startup synchronization with audio
- Scales to support multiple games with shared and unique sounds
- Maintains performance through proper caching and lazy loading

### Required Sound Events (Jumper Game)
- **Game Start**: Audio cue when game begins
- **Jump Action**: Feedback for successful jump input
- **Success**: Obstacle cleared successfully
- **Failure**: Life lost (collision with obstacle)
- **High Score**: New personal best achieved
- **Game Over**: All lives exhausted
- **UI Navigation**: Menu option cycling (Play Again/Exit)

## Decision
Implement a comprehensive sound system with standardized event types, volume control, and game startup synchronization.

### Architecture Components

#### 1. Sound Event Categories
```python
class SoundCategory(Enum):
    GAME_START = "game_start"
    PLAYER_ACTION = "player_action"    # Jump, attack, etc.
    SUCCESS = "success"                # Obstacle cleared, point scored
    FAILURE = "failure"                # Life lost, game over
    ACHIEVEMENT = "achievement"        # High score, level complete
    UI_FEEDBACK = "ui_feedback"        # Menu navigation, button clicks
    AMBIENT = "ambient"                # Background music, atmosphere
```

#### 2. Centralized Sound Manager
```python
class SoundManager:
    def __init__(self, game_name: str, settings: dict)
    def load_sounds(self) -> None
    def play_sound(self, event: SoundEvent, volume_override: float = None) -> arcade.Sound
    def play_background_music(self, track: str, loop: bool = True) -> None
    def stop_all_sounds(self) -> None
    def set_volume(self, category: SoundCategory, volume: float) -> None
    def wait_for_sound_completion(self, sound: arcade.Sound) -> None
```

#### 3. Volume Control System
- **Master Volume**: Overall audio level
- **SFX Volume**: Sound effects (actions, feedback)
- **Music Volume**: Background music and ambient sounds
- **UI Volume**: Menu and interface sounds

#### 4. Game Startup Synchronization
- Games wait for startup sound completion before accepting input
- Configurable startup delay for audio synchronization
- Non-blocking background music loading

### File Organization Structure
```
unipress/assets/sounds/
├── global/
│   ├── ui/
│   │   ├── button_click.ogg
│   │   ├── menu_cycle.ogg
│   │   └── confirm.ogg
│   ├── achievements/
│   │   ├── new_high_score.ogg
│   │   └── game_complete.ogg
│   └── system/
│       ├── game_start.ogg
│       └── game_over.ogg
└── games/
    └── {game_name}/
        ├── player/
        │   ├── jump_01.ogg
        │   └── collision_01.ogg
        ├── success/
        │   └── obstacle_cleared.ogg
        ├── ambient/
        │   └── background_music.ogg
        └── special/
            └── {game_specific_sounds}
```

### Settings Integration
```toml
[audio]
master_volume = 1.0
sfx_volume = 0.7
music_volume = 0.5
ui_volume = 0.6
startup_delay = true

[game.audio]  # Game-specific overrides
# Game can override global audio settings
```

### Audio Format Requirements
- **Primary Format**: OGG Vorbis (`.ogg`) - recommended for all sound assets
  - Open source, patent-free format
  - Excellent compression with high quality
  - Native support in Python Arcade
  - Consistent cross-platform playback
- **Fallback Formats**: WAV (`.wav`), MP3 (`.mp3`) supported but not recommended
- **Quality Standards**: 
  - Sample Rate: 44.1kHz (CD quality)
  - Bit Depth: 16-bit minimum
  - Compression: Variable bitrate, quality level 6-8
- **File Size Guidelines**:
  - UI sounds: < 100KB (short, crisp feedback)
  - Game actions: < 200KB (jump, collision sounds)
  - Background music: < 5MB (looping tracks)

### BaseGame Integration
```python
class BaseGame:
    def __init__(self, game_name: str, ...):
        self.sound_manager = SoundManager(game_name, self.settings)
        
    def play_sound_event(self, event: SoundEvent) -> arcade.Sound:
        return self.sound_manager.play_sound(event)
        
    def wait_for_game_start_sound(self) -> None:
        if get_setting(self.settings, "audio.startup_delay", True):
            startup_sound = self.play_sound_event(SoundEvent.GAME_START)
            if startup_sound:
                self.sound_manager.wait_for_sound_completion(startup_sound)
```

## Implementation Details

### Sound Event Definitions
```python
@dataclass
class SoundEvent:
    category: SoundCategory
    file_path: str
    volume_multiplier: float = 1.0
    global_sound: bool = False  # Use global sound vs game-specific
    
# Predefined events
SOUND_EVENTS = {
    "game_start": SoundEvent(SoundCategory.GAME_START, "system/game_start.ogg", global_sound=True),
    "jump": SoundEvent(SoundCategory.PLAYER_ACTION, "player/jump_01.ogg"),
    "success": SoundEvent(SoundCategory.SUCCESS, "success/obstacle_cleared.ogg"),
    "failure": SoundEvent(SoundCategory.FAILURE, "player/collision_01.ogg"),
    "high_score": SoundEvent(SoundCategory.ACHIEVEMENT, "achievements/new_high_score.ogg", global_sound=True),
    "game_over": SoundEvent(SoundCategory.FAILURE, "system/game_over.ogg", global_sound=True),
    "ui_cycle": SoundEvent(SoundCategory.UI_FEEDBACK, "ui/menu_cycle.ogg", global_sound=True),
}
```

### Volume Calculation
```python
def calculate_volume(self, event: SoundEvent, override: float = None) -> float:
    if override is not None:
        return override
    
    master = get_setting(self.settings, "audio.master_volume", 1.0)
    category_volumes = {
        SoundCategory.PLAYER_ACTION: get_setting(self.settings, "audio.sfx_volume", 0.7),
        SoundCategory.SUCCESS: get_setting(self.settings, "audio.sfx_volume", 0.7),
        SoundCategory.FAILURE: get_setting(self.settings, "audio.sfx_volume", 0.7),
        SoundCategory.ACHIEVEMENT: get_setting(self.settings, "audio.sfx_volume", 0.7),
        SoundCategory.UI_FEEDBACK: get_setting(self.settings, "audio.ui_volume", 0.6),
        SoundCategory.AMBIENT: get_setting(self.settings, "audio.music_volume", 0.5),
    }
    
    category_volume = category_volumes.get(event.category, 0.7)
    return master * category_volume * event.volume_multiplier
```

## Rationale

### Design Benefits
- **Consistency**: Standardized sound events across all games
- **Maintainability**: Centralized sound management and volume control
- **Performance**: Leverages existing caching system, adds smart loading
- **User Experience**: Proper volume controls and startup synchronization
- **Scalability**: Easy to add new games and sound events
- **Accessibility**: Volume categories for different user preferences

### Technical Benefits
- **Integration**: Builds on existing asset management system
- **Error Handling**: Graceful degradation when sound files missing
- **Settings**: Leverages existing TOML settings hierarchy
- **Logging**: Structured logging for sound events and issues
- **Memory**: Efficient caching and lazy loading of sound assets

## Consequences

### Positive
- Rich audio feedback enhances game experience
- Standardized volume controls across all games
- Professional startup sequence with audio synchronization
- Easy to add new games with consistent sound patterns
- Comprehensive coverage of all game events
- Maintains existing asset loading performance

### Negative
- Increased complexity in game initialization
- Additional sound file assets required (storage overhead)
- Potential audio latency on slower systems
- Dependency on sound file availability for full experience
- More complex testing requirements for audio features

### Implementation Requirements
- Create comprehensive sound asset library
- Implement SoundManager class with volume controls
- Integrate with BaseGame for standardized usage
- Add audio settings to global and game-specific TOML files
- Update existing games to use new sound event system
- Add audio-specific logging and error handling

## Future Considerations
- Dynamic audio (pitch shifting based on game speed/difficulty)
- Spatial audio for multi-dimensional games
- Audio accessibility features (visual sound indicators)
- Procedural audio generation for variety
- Audio compression and streaming for larger music files

## Related
- ADR-010: Settings System TOML (volume control integration)
- ADR-013: Asset Management System (builds on existing caching)
- Existing sound infrastructure in `unipress/core/assets.py`
- Sound placeholders in `ASSET_PLACEHOLDERS.md`