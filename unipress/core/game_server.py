"""
Game server for running games in Docker container.
Provides HTTP API for launching different games.
"""

import json
import subprocess
import sys
import threading
import time
from typing import Any, Dict, Optional

from flask import Flask, jsonify, request

from unipress.core.logger import get_logger, log_error, log_game_event

app = Flask(__name__)
logger = get_logger("game_server")

# Global state
current_game_process: Optional[subprocess.Popen] = None
current_game_thread: Optional[threading.Thread] = None


def run_game_in_thread(game_module: str, difficulty: int = 5) -> None:
    """Run game in separate thread to avoid blocking the server."""
    global current_game_process
    
    try:
        log_game_event("game_server_starting_game", game_module=game_module, difficulty=difficulty)
        
        # Kill any existing game
        if current_game_process:
            current_game_process.terminate()
            current_game_process.wait(timeout=5)
        
        # Start new game
        cmd = [sys.executable, "-m", game_module, str(difficulty)]
        current_game_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        log_game_event("game_server_game_started", game_module=game_module, difficulty=difficulty)
        
    except Exception as e:
        log_error(e, "Failed to start game", game_module=game_module, difficulty=difficulty)


@app.route("/health", methods=["GET"])
def health() -> Dict[str, Any]:
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "game_running": current_game_process is not None and current_game_process.poll() is None
    })


@app.route("/games/run", methods=["POST"])
def run_game() -> Dict[str, Any]:
    """Run a specific game."""
    try:
        data = request.get_json()
        game_name = data.get("game", "unipress.games.jumper.game")
        difficulty = data.get("difficulty", 5)
        
        # Validate difficulty
        if not 1 <= difficulty <= 10:
            return jsonify({"error": "Difficulty must be between 1 and 10"}), 400
        
        # Start game in background thread
        thread = threading.Thread(
            target=run_game_in_thread,
            args=(game_name, difficulty),
            daemon=True
        )
        thread.start()
        
        return jsonify({
            "status": "success",
            "message": f"Starting {game_name} with difficulty {difficulty}",
            "game": game_name,
            "difficulty": difficulty
        })
        
    except Exception as e:
        log_error(e, "Error in run_game endpoint")
        return jsonify({"error": str(e)}), 500


@app.route("/games/stop", methods=["POST"])
def stop_game() -> Dict[str, Any]:
    """Stop currently running game."""
    global current_game_process
    
    try:
        if current_game_process and current_game_process.poll() is None:
            current_game_process.terminate()
            current_game_process.wait(timeout=5)
            current_game_process = None
            
            log_game_event("game_server_game_stopped")
            return jsonify({"status": "success", "message": "Game stopped"})
        else:
            return jsonify({"status": "success", "message": "No game running"})
            
    except Exception as e:
        log_error(e, "Error stopping game")
        return jsonify({"error": str(e)}), 500


@app.route("/games/status", methods=["GET"])
def game_status() -> Dict[str, Any]:
    """Get current game status."""
    global current_game_process
    
    is_running = current_game_process is not None and current_game_process.poll() is None
    
    return jsonify({
        "game_running": is_running,
        "pid": current_game_process.pid if is_running else None,
        "return_code": current_game_process.poll() if current_game_process else None
    })


@app.route("/games/list", methods=["GET"])
def list_games() -> Dict[str, Any]:
    """List available games."""
    games = [
        {
            "name": "jumper",
            "module": "unipress.games.jumper.game",
            "description": "Enhanced sprite-based jumping game with animations and sound"
        },
        {
            "name": "demo_jump", 
            "module": "unipress.games.demo_jump.game",
            "description": "Basic geometric jumping game for reference"
        }
    ]
    
    return jsonify({"games": games})


def main() -> None:
    """Start the game server."""
    logger.info("Starting Unipress Game Server")
    
    # Run Flask app
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()
