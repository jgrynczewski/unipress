# ADR-008: Fullscreen Display Standard

## Status
Accepted

## Context
One-button games should provide an immersive, focused gaming experience without distractions from desktop environment elements like taskbars, window decorations, or system menus.

## Decision
All Unipress games will start in **fullscreen mode by default** with no system bars or window decorations visible.

## Implementation Details

### Fullscreen Mode
- Games open in true fullscreen (not windowed fullscreen)
- No system taskbars, window titles, or desktop elements visible
- Maximum screen real estate for game content
- Built into BaseGame class with `fullscreen=True` default parameter

### Escape Key Toggle
- **ESC key** toggles between fullscreen and windowed mode
- Enables easy development and testing without restarting
- Allows users to exit fullscreen if needed
- Implemented in BaseGame.on_key_press()

### Configuration
- Games can override fullscreen setting if needed: `BaseGame(fullscreen=False)`
- Default behavior is fullscreen for all games
- Consistent across all Unipress game collection

## Rationale

### Immersive Experience
- Eliminates visual distractions from desktop environment
- Creates focused gaming atmosphere appropriate for one-button games
- Professional presentation suitable for arcade-style games

### Arcade-Style Aesthetics
- Mimics traditional arcade machine experience
- Appropriate visual style for simple, focused games
- Enhances the "pick up and play" nature of one-button games

### Development Flexibility
- ESC key provides easy toggle for development work
- Doesn't interfere with game testing or debugging
- Maintains immersion while allowing practical development needs

### Consistency
- Uniform experience across all games in collection
- Predictable behavior for users
- Simplified game setup (no window size concerns)

## Consequences

### Positive
- **Immersive Experience**: No desktop distractions during gameplay
- **Professional Presentation**: Games look polished and complete
- **Consistent UX**: All games behave identically regarding display
- **Development Friendly**: Easy toggle with ESC key for testing

### Considerations
- Users unfamiliar with ESC toggle might need instruction
- Some development tasks easier in windowed mode (debugging, etc.)
- Requires consideration of different screen resolutions/aspect ratios

## Technical Implementation
- Added `fullscreen: bool = True` parameter to BaseGame.__init__()
- ESC key handler in BaseGame.on_key_press() for toggle functionality
- Arcade framework handles fullscreen mode automatically
- No impact on existing game logic or mechanics

## Future Considerations
- May need aspect ratio handling for different screen sizes
- Could add fullscreen setting to game configuration files
- Possible addition of F11 key as alternative fullscreen toggle (web browser standard)