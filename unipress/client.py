"""
Unipress Game Client
Client for communicating with the game server running in Docker container.
"""

import json
import time
from typing import Any, Dict, Optional

import requests


class UnipressClient:
    """Client for Unipress game server."""
    
    def __init__(self, server_url: str = "http://localhost:5000"):
        """
        Initialize client.
        
        Args:
            server_url: URL of the game server (default: http://localhost:5000)
        """
        self.server_url = server_url.rstrip("/")
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check server health."""
        try:
            response = self.session.get(f"{self.server_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "status": "unhealthy"}
    
    def list_games(self) -> Dict[str, Any]:
        """List available games."""
        try:
            response = self.session.get(f"{self.server_url}/games/list")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def run_game(self, game: str, difficulty: int = 5) -> Dict[str, Any]:
        """
        Run a specific game.
        
        Args:
            game: Game name or module (e.g., "jumper", "demo_jump")
            difficulty: Difficulty level 1-10 (default: 5)
        """
        try:
            # Map game names to modules
            game_modules = {
                "jumper": "unipress.games.jumper.game",
                "demo_jump": "unipress.games.demo_jump.game",
            }
            
            game_module = game_modules.get(game, game)
            
            data = {
                "game": game_module,
                "difficulty": difficulty
            }
            
            response = self.session.post(
                f"{self.server_url}/games/run",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def stop_game(self) -> Dict[str, Any]:
        """Stop currently running game."""
        try:
            response = self.session.post(f"{self.server_url}/games/stop")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def game_status(self) -> Dict[str, Any]:
        """Get current game status."""
        try:
            response = self.session.get(f"{self.server_url}/games/status")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def wait_for_game_completion(self, timeout: int = 300) -> bool:
        """
        Wait for current game to complete.
        
        Args:
            timeout: Maximum time to wait in seconds (default: 300)
            
        Returns:
            True if game completed, False if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.game_status()
            
            if "error" in status:
                print(f"Error checking game status: {status['error']}")
                return False
            
            if not status.get("game_running", False):
                return True
            
            time.sleep(1)
        
        return False


def main():
    """Example usage of the client."""
    client = UnipressClient()
    
    # Check server health
    health = client.health_check()
    print(f"Server health: {health}")
    
    if "error" in health:
        print("Server is not available. Make sure the Docker container is running.")
        return
    
    # List available games
    games = client.list_games()
    print(f"Available games: {json.dumps(games, indent=2)}")
    
    # Run jumper game with difficulty 7
    result = client.run_game("jumper", difficulty=7)
    print(f"Game start result: {result}")
    
    # Wait for game to complete
    print("Waiting for game to complete...")
    completed = client.wait_for_game_completion(timeout=60)
    
    if completed:
        print("Game completed!")
    else:
        print("Game did not complete within timeout")
        # Stop the game
        stop_result = client.stop_game()
        print(f"Stop result: {stop_result}")


if __name__ == "__main__":
    main()
