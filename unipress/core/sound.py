"""Comprehensive sound system for Unipress games.

This module provides centralized sound management with volume control,
event-based audio feedback, and game startup synchronization.
"""

import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Any

import arcade
from loguru import logger

from unipress.core.assets import get_sound
from unipress.core.settings import get_setting


class SoundCategory(Enum):
    """Sound event categories for volume control and organization."""
    GAME_START = "game_start"
    PLAYER_ACTION = "player_action"
    SUCCESS = "success"
    FAILURE = "failure"
    ACHIEVEMENT = "achievement"
    UI_FEEDBACK = "ui_feedback"
    AMBIENT = "ambient"


@dataclass
class SoundEvent:
    """Definition of a sound event with metadata."""
    category: SoundCategory
    file_path: str
    volume_multiplier: float = 1.0
    global_sound: bool = False
    
    def __post_init__(self):
        """Validate sound event parameters."""
        if not (0.0 <= self.volume_multiplier <= 2.0):
            raise ValueError(f"Volume multiplier must be between 0.0 and 2.0, got {self.volume_multiplier}")


class SoundManager:
    """Centralized sound management for games with volume control and event handling."""
    
    def __init__(self, game_name: str, settings: Dict[str, Any]):
        """Initialize sound manager for a specific game.
        
        Args:
            game_name: Name of the game for asset loading
            settings: Game settings dictionary
        """
        self.game_name = game_name
        self.settings = settings
        self._sound_cache: Dict[str, Optional[arcade.Sound]] = {}
        self._currently_playing: Dict[str, arcade.Sound] = {}
        
        logger.info(f"SoundManager initialized for game: {game_name}")
    
    def calculate_volume(self, event: SoundEvent, volume_override: Optional[float] = None) -> float:
        """Calculate final volume for a sound event.
        
        Args:
            event: Sound event definition
            volume_override: Optional volume override (0.0-1.0)
            
        Returns:
            Final volume level (0.0-1.0)
        """
        if volume_override is not None:
            return max(0.0, min(1.0, volume_override))
        
        master = get_setting(self.settings, "audio.master_volume", 1.0)
        
        # Map categories to settings keys
        category_settings = {
            SoundCategory.PLAYER_ACTION: "audio.sfx_volume",
            SoundCategory.SUCCESS: "audio.sfx_volume",
            SoundCategory.FAILURE: "audio.sfx_volume",
            SoundCategory.ACHIEVEMENT: "audio.sfx_volume",
            SoundCategory.GAME_START: "audio.sfx_volume",
            SoundCategory.UI_FEEDBACK: "audio.ui_volume",
            SoundCategory.AMBIENT: "audio.music_volume",
        }
        
        # Default volumes per category
        category_defaults = {
            SoundCategory.PLAYER_ACTION: 0.7,
            SoundCategory.SUCCESS: 0.7,
            SoundCategory.FAILURE: 0.7,
            SoundCategory.ACHIEVEMENT: 0.8,
            SoundCategory.GAME_START: 0.8,
            SoundCategory.UI_FEEDBACK: 0.6,
            SoundCategory.AMBIENT: 0.5,
        }
        
        setting_key = category_settings.get(event.category, "audio.sfx_volume")
        default_volume = category_defaults.get(event.category, 0.7)
        category_volume = get_setting(self.settings, setting_key, default_volume)
        
        final_volume = master * category_volume * event.volume_multiplier
        return max(0.0, min(1.0, final_volume))
    
    def load_sound(self, event: SoundEvent) -> Optional[arcade.Sound]:
        """Load a sound for the given event.
        
        Args:
            event: Sound event definition
            
        Returns:
            Loaded arcade.Sound or None if loading failed
        """
        cache_key = f"{event.global_sound}:{event.file_path}"
        
        if cache_key in self._sound_cache:
            return self._sound_cache[cache_key]
        
        # Load sound using existing asset system
        game_name = None if event.global_sound else self.game_name
        sound = get_sound(event.file_path, game_name)
        
        self._sound_cache[cache_key] = sound
        
        if sound:
            logger.debug(f"Sound loaded: {event.file_path} (global={event.global_sound})")
        else:
            logger.warning(f"Failed to load sound: {event.file_path} (global={event.global_sound})")
        
        return sound
    
    def play_sound(self, event: SoundEvent, volume_override: Optional[float] = None) -> Optional[arcade.Sound]:
        """Play a sound event with appropriate volume.
        
        Args:
            event: Sound event to play
            volume_override: Optional volume override (0.0-1.0)
            
        Returns:
            Playing arcade.Sound or None if sound unavailable
        """
        sound = self.load_sound(event)
        if not sound:
            return None
        
        volume = self.calculate_volume(event, volume_override)
        
        try:
            played_sound = arcade.play_sound(sound, volume)
            
            # Track currently playing sounds
            event_key = f"{event.category.value}:{event.file_path}"
            self._currently_playing[event_key] = played_sound
            
            logger.debug(f"Sound played: {event.file_path} at volume {volume:.2f}")
            return played_sound
            
        except Exception as e:
            logger.error(f"Failed to play sound {event.file_path}: {e}")
            return None
    
    def wait_for_sound_completion(self, sound: arcade.Sound, timeout: float = 5.0) -> None:
        """Wait for a sound to complete playing.
        
        Args:
            sound: Sound to wait for
            timeout: Maximum wait time in seconds
        """
        if not sound:
            return
        
        start_time = time.time()
        
        try:
            # Note: arcade.Sound doesn't have a direct "is_playing" method
            # This is a simple time-based approach - could be improved with
            # actual sound duration detection
            estimated_duration = min(3.0, timeout)  # Assume most UI sounds are < 3 seconds
            time.sleep(estimated_duration)
            
            logger.debug(f"Sound completion wait finished after {time.time() - start_time:.2f}s")
            
        except Exception as e:
            logger.warning(f"Error waiting for sound completion: {e}")
    
    def stop_all_sounds(self) -> None:
        """Stop all currently playing sounds."""
        try:
            arcade.stop_sound()
            self._currently_playing.clear()
            logger.debug("All sounds stopped")
        except Exception as e:
            logger.error(f"Failed to stop sounds: {e}")
    
    def preload_sounds(self, events: Dict[str, SoundEvent]) -> None:
        """Preload multiple sound events for better performance.
        
        Args:
            events: Dictionary of event_name -> SoundEvent mappings
        """
        loaded_count = 0
        failed_count = 0
        
        for event_name, event in events.items():
            sound = self.load_sound(event)
            if sound:
                loaded_count += 1
            else:
                failed_count += 1
        
        logger.info(f"Sound preloading complete: {loaded_count} loaded, {failed_count} failed")


# Predefined sound events for common game scenarios
STANDARD_SOUND_EVENTS: Dict[str, SoundEvent] = {
    "game_start": SoundEvent(
        SoundCategory.GAME_START, 
        "system/game_start.ogg", 
        volume_multiplier=1.0,
        global_sound=True
    ),
    "jump": SoundEvent(
        SoundCategory.PLAYER_ACTION, 
        "player/jump_01.ogg",
        volume_multiplier=0.8
    ),
    "success": SoundEvent(
        SoundCategory.SUCCESS, 
        "success/obstacle_cleared.ogg",
        volume_multiplier=0.9
    ),
    "failure": SoundEvent(
        SoundCategory.FAILURE, 
        "player/collision_01.ogg",
        volume_multiplier=1.0
    ),
    "high_score": SoundEvent(
        SoundCategory.ACHIEVEMENT, 
        "achievements/new_high_score.ogg",
        volume_multiplier=1.2,
        global_sound=True
    ),
    "game_over": SoundEvent(
        SoundCategory.FAILURE, 
        "system/game_over.ogg",
        volume_multiplier=1.0,
        global_sound=True
    ),
    "ui_cycle": SoundEvent(
        SoundCategory.UI_FEEDBACK, 
        "ui/menu_cycle.ogg",
        volume_multiplier=0.7,
        global_sound=True
    ),
    "ui_confirm": SoundEvent(
        SoundCategory.UI_FEEDBACK, 
        "ui/confirm.ogg",
        volume_multiplier=0.8,
        global_sound=True
    ),
}