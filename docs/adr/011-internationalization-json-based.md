# ADR-011: JSON-Based Internationalization System

## Status
Accepted

## Context
Unipress games need internationalization (i18n) support to display user-facing messages in multiple languages. We need a solution that is simple, maintainable, and integrates well with our existing TOML settings system.

## Decision
We will implement a **JSON-based internationalization system** with language selection via settings.

## Options Considered

### 1. Python gettext (Standard i18n)
- **Pros**: 
  - Industry standard for Python applications
  - Mature ecosystem with translation tools
  - Built-in pluralization support
  - Unicode handling
- **Cons**: 
  - Complex setup (.po/.mo files)
  - Overkill for simple game messages
  - Requires external tools for translation workflow
  - Not game designer friendly

### 2. babel (Advanced i18n Library)
- **Pros**: 
  - Professional translation workflows
  - Advanced features (pluralization, date/time formatting)
  - Integration with gettext
- **Cons**: 
  - Heavy dependency
  - Complex for simple game UI messages
  - Requires extensive setup

### 3. JSON-based Messages (Chosen Solution)
- **Pros**: 
  - **Simplicity**: Easy to understand and implement
  - **Game Designer Friendly**: Non-technical team members can edit translations
  - **No Dependencies**: Uses standard Python json module
  - **Settings Integration**: Works seamlessly with our TOML settings system
  - **Version Control Friendly**: JSON files merge cleanly in git
  - **Flexible Structure**: Easy to organize by UI sections or game features
- **Cons**: 
  - No built-in pluralization rules (acceptable for game UI)
  - Manual message key management
  - No standard translation tools (but simple format compensates)

## Technical Implementation

### Language Selection
Language is configured via our existing TOML settings system:

**Global settings (`unipress/settings.toml`)**:
```toml
[ui]
language = "pl_PL"  # Default language (Polish)
```

**Game settings override**:
```toml
[ui]
language = "en_US"  # Override for specific game
```

**Constructor override**:
```python
BaseGame(game_name="demo_jump", language="en_US")
```

### Message File Structure
```
unipress/
├── locales/
│   ├── pl_PL/               # Default language
│   │   ├── common.json      # Shared UI messages
│   │   └── games/
│   │       ├── demo_jump.json
│   │       └── jumper.json
│   └── en_US/               # Secondary language
│       ├── common.json
│       └── games/
│           ├── demo_jump.json
│           └── jumper.json
```

### Message File Format
**Common messages (`locales/pl_PL/common.json`)**:
```json
{
  "ui": {
    "score": "Punkty: {score}",
    "lives": "Życia: {current}/{max}",
    "difficulty": "Trudność: {level}/10",
    "game_over": "KONIEC GRY",
    "final_score": "Końcowy wynik: {score}",
    "click_to_start": "Kliknij aby rozpocząć",
    "click_to_restart": "Kliknij aby zrestartować",
    "click_to_continue": "Kliknij aby kontynuować",
    "esc_fullscreen": "ESC: Przełącz tryb pełnoekranowy"
  },
  "system": {
    "loading": "Ładowanie...",
    "error": "Wystąpił błąd"
  }
}
```

**Game-specific messages (`locales/pl_PL/games/demo_jump.json`)**:
```json
{
  "game": {
    "title": "Gra Demo - Skakanie",
    "instructions": "Kliknij aby przeskoczyć czerwone przeszkody!",
    "subtitle": "Wyższa trudność = mniej czasu na reakcję",
    "jump_window_info": "Okno skoku: {distance}px ({duration}s)"
  }
}
```

**English translations (`locales/en_US/common.json`)**:
```json
{
  "ui": {
    "score": "Score: {score}",
    "lives": "Lives: {current}/{max}",
    "difficulty": "Difficulty: {level}/10",
    "game_over": "GAME OVER",
    "final_score": "Final Score: {score}",
    "click_to_start": "Click to start",
    "click_to_restart": "Click to restart",
    "click_to_continue": "Click to continue",
    "esc_fullscreen": "ESC: Toggle fullscreen"
  },
  "system": {
    "loading": "Loading...",
    "error": "Error occurred"
  }
}
```

### Code Integration
```python
class BaseGame:
    def __init__(self, game_name: str, language: str = None, ...):
        # Load settings (language from settings hierarchy)
        self.settings = load_settings(game_name, language=language)
        
        # Load messages for selected language
        self.messages = load_messages(
            language=get_setting(self.settings, "ui.language", "pl_PL"),
            game_name=game_name
        )
    
    def get_message(self, key: str, **kwargs) -> str:
        """Get localized message with parameter substitution."""
        return self.messages.get_message(key, **kwargs)
    
    def draw_ui(self):
        # Use localized messages
        arcade.draw_text(
            self.get_message("ui.score", score=self.score),
            10, self.height - 30, arcade.color.WHITE, 20
        )
```

## Rationale

### Polish as Default
- **Target Audience**: Primary users are Polish speakers
- **Development Context**: Project created in Polish-speaking environment
- **Cultural Relevance**: Polish-first approach for local market
- **Fallback**: English available as secondary language

### Simplicity Over Features
- Game UI messages are typically simple (no complex pluralization needed)
- Easy for translators who aren't programmers
- Minimal learning curve for team members
- Fast implementation and maintenance

### Settings Integration
- Leverages existing TOML settings system
- Consistent configuration approach across project
- Same override hierarchy as other settings

### Maintenance Benefits
- JSON files are human-readable and editable
- Clear separation between common and game-specific messages
- Easy to add new languages by copying and translating JSON files
- Version control friendly (clear diffs)

### Performance
- Messages loaded once at game startup
- Simple dictionary lookup for message retrieval
- No runtime parsing overhead

## Supported Languages
- **pl_PL**: Polish (Poland) - Default
- **en_US**: English (United States) - Secondary language

Additional languages can be added by:
1. Creating new locale directory (e.g., `locales/de_DE/`)
2. Copying and translating JSON files
3. No code changes required

## Future Considerations
- Could add pluralization support if needed for complex messages
- Translation validation tools to check for missing keys
- Automatic fallback to pl_PL for missing translations
- Integration with translation services if project scales

## Implementation Priority
1. Create message loading system
2. Add language setting to TOML configuration  
3. Create pl_PL message files for existing UI
4. Create en_US translations
5. Update BaseGame and demo game to use localized messages
6. Test language switching via settings