"""
Unipress - One-Button Games Collection

Main entry point for running games.
"""

import sys

from unipress.core.logger import get_logger, init_logger, log_error
from unipress.games.demo_jump import DemoJumpGame


def main():
    """Main entry point."""
    # Initialize logging system
    init_logger()
    logger = get_logger("main")

    difficulty = None  # Use settings by default

    if len(sys.argv) > 1:
        try:
            difficulty = int(sys.argv[1])
            if not 1 <= difficulty <= 10:
                logger.error(
                    "Invalid difficulty level",
                    extra={"provided": sys.argv[1], "valid_range": "1-10"},
                )
                return
        except ValueError as e:
            log_error(e, "Failed to parse difficulty argument", provided=sys.argv[1])
            return

    logger.info("Starting Demo Jump Game")
    logger.info("Game controls: Left click to jump over red obstacles!")
    logger.info("Difficulty affects reaction time - higher = less time to react")

    try:
        game = DemoJumpGame(difficulty=difficulty)
        logger.info(
            "Game initialized",
            extra={
                "difficulty": game.difficulty,
                "lives": game.lives,
                "fullscreen": game.fullscreen,
            },
        )
        game.run()
    except Exception as e:
        log_error(e, "Game crashed during execution", difficulty=difficulty)
        raise


if __name__ == "__main__":
    main()
