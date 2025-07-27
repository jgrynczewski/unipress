"""
High Score Persistence System

Manages high scores for all games using JSON file storage.
Provides simple interface for getting, setting, and updating high scores.
"""

import json
from pathlib import Path

from unipress.core.logger import log_error, log_game_event


class HighScoreManager:
    """Manages high scores for all games using JSON file storage."""

    def __init__(self, scores_file: str = "high_scores.json"):
        """
        Initialize high score manager.

        Args:
            scores_file: Path to JSON file for storing high scores
        """
        self.scores_file = Path(scores_file)
        self._scores: dict[str, int] = {}
        self._load_scores()

    def _load_scores(self) -> None:
        """Load high scores from JSON file."""
        try:
            if self.scores_file.exists():
                with open(self.scores_file, encoding="utf-8") as f:
                    self._scores = json.load(f)
                log_game_event("high_scores_loaded", count=len(self._scores))
            else:
                self._scores = {}
                log_game_event("high_scores_file_created", file=str(self.scores_file))
        except Exception as e:
            log_error(e, "Failed to load high scores", file=str(self.scores_file))
            self._scores = {}

    def _save_scores(self) -> None:
        """Save high scores to JSON file."""
        try:
            # Ensure directory exists
            self.scores_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.scores_file, "w", encoding="utf-8") as f:
                json.dump(self._scores, f, indent=2, ensure_ascii=False)
            log_game_event("high_scores_saved", count=len(self._scores))
        except Exception as e:
            log_error(e, "Failed to save high scores", file=str(self.scores_file))

    def get_high_score(self, game_name: str) -> int:
        """
        Get high score for a game.

        Args:
            game_name: Name of the game

        Returns:
            High score for the game (0 if no score recorded)
        """
        return self._scores.get(game_name, 0)

    def set_high_score(self, game_name: str, score: int) -> bool:
        """
        Set high score for a game if it's higher than current record.

        Args:
            game_name: Name of the game
            score: New score to potentially record

        Returns:
            True if new high score was set, False otherwise
        """
        current_high = self.get_high_score(game_name)

        if score > current_high:
            self._scores[game_name] = score
            self._save_scores()
            log_game_event(
                "new_high_score",
                game=game_name,
                new_score=score,
                previous_score=current_high,
            )
            return True

        return False

    def update_score(self, game_name: str, score: int) -> bool:
        """
        Update score and check if it's a new high score.

        Args:
            game_name: Name of the game
            score: Final score from game session

        Returns:
            True if new high score was achieved, False otherwise
        """
        return self.set_high_score(game_name, score)

    def get_all_scores(self) -> dict[str, int]:
        """
        Get all high scores.

        Returns:
            Dictionary mapping game names to high scores
        """
        return self._scores.copy()

    def reset_high_score(self, game_name: str) -> None:
        """
        Reset high score for a specific game.

        Args:
            game_name: Name of the game to reset
        """
        if game_name in self._scores:
            old_score = self._scores[game_name]
            del self._scores[game_name]
            self._save_scores()
            log_game_event("high_score_reset", game=game_name, old_score=old_score)

    def reset_all_scores(self) -> None:
        """Reset all high scores."""
        count = len(self._scores)
        self._scores = {}
        self._save_scores()
        log_game_event("all_high_scores_reset", count=count)


# Global high score manager instance
_high_score_manager: HighScoreManager | None = None


def get_high_score_manager() -> HighScoreManager:
    """
    Get the global high score manager instance.

    Returns:
        Global HighScoreManager instance
    """
    global _high_score_manager
    if _high_score_manager is None:
        _high_score_manager = HighScoreManager()
    return _high_score_manager


# Convenience functions for easy access
def get_high_score(game_name: str) -> int:
    """Get high score for a game."""
    return get_high_score_manager().get_high_score(game_name)


def update_high_score(game_name: str, score: int) -> bool:
    """Update high score if score is higher than current record."""
    return get_high_score_manager().update_score(game_name, score)


def is_new_high_score(game_name: str, score: int) -> bool:
    """Check if score would be a new high score without updating."""
    return score > get_high_score(game_name)
