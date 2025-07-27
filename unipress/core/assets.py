"""
Asset Management System

Handles loading, caching, and management of game assets including:
- Sprite images and animations
- Sound effects and music
- Background images and parallax layers
- UI elements and fonts
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import arcade

from unipress.core.logger import log_error, log_game_event


class AnimationFrame:
    """Represents a single frame in an animation sequence."""

    def __init__(self, texture: arcade.Texture, duration: float, hitbox: Optional[Dict[str, int]] = None):
        """
        Initialize animation frame.

        Args:
            texture: Arcade texture for this frame
            duration: How long to display this frame (seconds)
            hitbox: Optional collision box {"x": int, "y": int, "width": int, "height": int}
        """
        self.texture = texture
        self.duration = duration
        self.hitbox = hitbox or {"x": 0, "y": 0, "width": texture.width, "height": texture.height}


class Animation:
    """Manages a sequence of animation frames with timing and metadata."""

    def __init__(self, name: str, frames: List[AnimationFrame], loop: bool = True, next_animation: Optional[str] = None):
        """
        Initialize animation.

        Args:
            name: Animation identifier
            frames: List of animation frames
            loop: Whether animation should loop
            next_animation: Name of animation to play after this one finishes
        """
        self.name = name
        self.frames = frames
        self.loop = loop
        self.next_animation = next_animation
        
        # Playback state
        self.current_frame = 0
        self.frame_time = 0.0
        self.is_finished = False

    def update(self, delta_time: float) -> bool:
        """
        Update animation playback.

        Args:
            delta_time: Time elapsed since last update

        Returns:
            True if animation changed frames
        """
        if self.is_finished:
            return False

        self.frame_time += delta_time
        current_frame_duration = self.frames[self.current_frame].duration

        if self.frame_time >= current_frame_duration:
            self.frame_time -= current_frame_duration
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.is_finished = True

            return True

        return False

    def get_current_texture(self) -> arcade.Texture:
        """Get texture for current frame."""
        return self.frames[self.current_frame].texture

    def get_current_hitbox(self) -> Dict[str, int]:
        """Get hitbox for current frame."""
        return self.frames[self.current_frame].hitbox

    def reset(self) -> None:
        """Reset animation to beginning."""
        self.current_frame = 0
        self.frame_time = 0.0
        self.is_finished = False


class AssetManager:
    """Central manager for all game assets with caching and lazy loading."""

    def __init__(self, base_path: Path = None):
        """
        Initialize asset manager.

        Args:
            base_path: Base path for assets (defaults to unipress/assets)
        """
        if base_path is None:
            base_path = Path(__file__).parent.parent / "assets"
        
        self.base_path = base_path
        self._texture_cache: Dict[str, arcade.Texture] = {}
        self._animation_cache: Dict[str, Animation] = {}
        self._sound_cache: Dict[str, arcade.Sound] = {}
        
        log_game_event("asset_manager_initialized", base_path=str(base_path))

    def get_texture(self, path: str, game_name: str = None) -> Optional[arcade.Texture]:
        """
        Load and cache a texture.

        Args:
            path: Relative path to image file
            game_name: Game name for game-specific assets (None for global)

        Returns:
            Loaded texture or None if failed
        """
        cache_key = f"{game_name or 'global'}:{path}"
        
        if cache_key in self._texture_cache:
            return self._texture_cache[cache_key]

        try:
            if game_name:
                full_path = self.base_path / "images" / "games" / game_name / path
            else:
                full_path = self.base_path / "images" / "global" / path

            if not full_path.exists():
                log_error(None, f"Texture file not found: {full_path}")
                return None

            texture = arcade.load_texture(str(full_path))
            self._texture_cache[cache_key] = texture
            
            log_game_event("texture_loaded", path=str(full_path), cache_key=cache_key)
            return texture

        except Exception as e:
            log_error(e, f"Failed to load texture: {path}", game_name=game_name)
            return None

    def load_animation(self, animation_name: str, game_name: str) -> Optional[Animation]:
        """
        Load animation from JSON metadata and image files.

        Args:
            animation_name: Name of animation (matches JSON filename without _anim.json)
            game_name: Game name for asset location

        Returns:
            Loaded animation or None if failed
        """
        cache_key = f"{game_name}:{animation_name}"
        
        if cache_key in self._animation_cache:
            # Return a fresh copy for independent playback
            original = self._animation_cache[cache_key]
            return Animation(original.name, original.frames, original.loop, original.next_animation)

        try:
            # Load animation metadata
            metadata_path = self.base_path / "images" / "games" / game_name / f"{animation_name}_anim.json"
            
            if not metadata_path.exists():
                log_error(None, f"Animation metadata not found: {metadata_path}")
                return None

            with open(metadata_path, encoding="utf-8") as f:
                metadata = json.load(f)

            # Load animation frames
            frames = []
            base_dir = metadata_path.parent

            for frame_data in metadata["frames"]:
                texture_path = base_dir / frame_data["file"]
                
                if not texture_path.exists():
                    log_error(None, f"Animation frame not found: {texture_path}")
                    continue

                texture = arcade.load_texture(str(texture_path))
                frame = AnimationFrame(
                    texture=texture,
                    duration=frame_data["duration"],
                    hitbox=frame_data.get("hitbox")
                )
                frames.append(frame)

            if not frames:
                log_error(None, f"No valid frames loaded for animation: {animation_name}")
                return None

            animation = Animation(
                name=metadata["name"],
                frames=frames,
                loop=metadata.get("loop", True),
                next_animation=metadata.get("next_animation")
            )

            self._animation_cache[cache_key] = animation
            log_game_event("animation_loaded", animation=animation_name, frames=len(frames))
            
            # Return a fresh copy
            return Animation(animation.name, animation.frames, animation.loop, animation.next_animation)

        except Exception as e:
            log_error(e, f"Failed to load animation: {animation_name}", game_name=game_name)
            return None

    def get_sound(self, path: str, game_name: str = None) -> Optional[arcade.Sound]:
        """
        Load and cache a sound effect.

        Args:
            path: Relative path to sound file
            game_name: Game name for game-specific sounds (None for global)

        Returns:
            Loaded sound or None if failed
        """
        cache_key = f"{game_name or 'global'}:{path}"
        
        if cache_key in self._sound_cache:
            return self._sound_cache[cache_key]

        try:
            if game_name:
                full_path = self.base_path / "sounds" / "games" / game_name / path
            else:
                full_path = self.base_path / "sounds" / "global" / path

            if not full_path.exists():
                log_error(None, f"Sound file not found: {full_path}")
                return None

            sound = arcade.load_sound(str(full_path))
            self._sound_cache[cache_key] = sound
            
            log_game_event("sound_loaded", path=str(full_path), cache_key=cache_key)
            return sound

        except Exception as e:
            log_error(e, f"Failed to load sound: {path}", game_name=game_name)
            return None

    def preload_game_assets(self, game_name: str, asset_list: List[str]) -> None:
        """
        Preload a list of assets for a game to improve performance.

        Args:
            game_name: Name of the game
            asset_list: List of asset paths to preload
        """
        log_game_event("preloading_assets", game_name=game_name, count=len(asset_list))
        
        for asset_path in asset_list:
            if asset_path.endswith(("_anim.json", "_anim")):
                # Animation
                anim_name = asset_path.replace("_anim.json", "").replace("_anim", "")
                self.load_animation(anim_name, game_name)
            elif asset_path.endswith((".png", ".jpg", ".jpeg")):
                # Texture
                self.get_texture(asset_path, game_name)
            elif asset_path.endswith((".ogg", ".wav", ".mp3")):
                # Sound
                self.get_sound(asset_path, game_name)

    def clear_cache(self, game_name: str = None) -> None:
        """
        Clear cached assets to free memory.

        Args:
            game_name: Clear only assets for specific game (None clears all)
        """
        if game_name:
            # Clear specific game assets
            keys_to_remove = [key for key in self._texture_cache.keys() if key.startswith(f"{game_name}:")]
            for key in keys_to_remove:
                del self._texture_cache[key]
                
            keys_to_remove = [key for key in self._animation_cache.keys() if key.startswith(f"{game_name}:")]
            for key in keys_to_remove:
                del self._animation_cache[key]
                
            keys_to_remove = [key for key in self._sound_cache.keys() if key.startswith(f"{game_name}:")]
            for key in keys_to_remove:
                del self._sound_cache[key]
                
            log_game_event("game_assets_cleared", game_name=game_name)
        else:
            # Clear all assets
            self._texture_cache.clear()
            self._animation_cache.clear()
            self._sound_cache.clear()
            log_game_event("all_assets_cleared")

    def get_cache_info(self) -> Dict[str, int]:
        """Get information about cached assets."""
        return {
            "textures": len(self._texture_cache),
            "animations": len(self._animation_cache),
            "sounds": len(self._sound_cache)
        }


# Global asset manager instance
_asset_manager: Optional[AssetManager] = None


def get_asset_manager() -> AssetManager:
    """
    Get the global asset manager instance.

    Returns:
        Global AssetManager instance
    """
    global _asset_manager
    if _asset_manager is None:
        _asset_manager = AssetManager()
    return _asset_manager


# Convenience functions for easy access
def get_texture(path: str, game_name: str = None) -> Optional[arcade.Texture]:
    """Get texture from global asset manager."""
    return get_asset_manager().get_texture(path, game_name)


def load_animation(animation_name: str, game_name: str) -> Optional[Animation]:
    """Load animation from global asset manager."""
    return get_asset_manager().load_animation(animation_name, game_name)


def get_sound(path: str, game_name: str = None) -> Optional[arcade.Sound]:
    """Get sound from global asset manager."""
    return get_asset_manager().get_sound(path, game_name)


def preload_assets(game_name: str, asset_list: List[str]) -> None:
    """Preload assets using global asset manager."""
    get_asset_manager().preload_game_assets(game_name, asset_list)


def clear_assets(game_name: str = None) -> None:
    """Clear assets using global asset manager."""
    get_asset_manager().clear_cache(game_name)