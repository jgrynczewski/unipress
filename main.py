"""
Unipress - One-Button Games Collection

Main entry point for running games.
"""

import sys

from unipress.games.demo_jump import DemoJumpGame


def main():
    """Main entry point."""
    difficulty = None  # Use settings by default
    
    if len(sys.argv) > 1:
        try:
            difficulty = int(sys.argv[1])
            if not 1 <= difficulty <= 10:
                print("Difficulty must be between 1 and 10")
                return
        except ValueError:
            print("Difficulty must be a number between 1 and 10")
            return

    print("Starting Demo Jump Game")
    print("Left click to jump over red obstacles!")
    print("Higher difficulty = less reaction time")

    game = DemoJumpGame(difficulty=difficulty)
    print(f"Loaded with Difficulty: {game.difficulty}, Lives: {game.lives}")
    game.run()


if __name__ == "__main__":
    main()
