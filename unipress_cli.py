#!/usr/bin/env python3
"""
Unipress CLI - Command line interface for running games via server.
"""

import argparse
import json
import sys
from typing import Optional

from unipress.client import UnipressClient


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Unipress Game Client")
    parser.add_argument("--server", default="http://localhost:5000", 
                       help="Game server URL (default: http://localhost:5000)")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Health check command
    health_parser = subparsers.add_parser("health", help="Check server health")
    
    # List games command
    list_parser = subparsers.add_parser("list", help="List available games")
    
    # Run game command
    run_parser = subparsers.add_parser("run", help="Run a game")
    run_parser.add_argument("game", choices=["jumper", "demo_jump"], 
                           help="Game to run")
    run_parser.add_argument("--difficulty", "-d", type=int, default=5,
                           help="Difficulty level 1-10 (default: 5)")
    
    # Stop game command
    stop_parser = subparsers.add_parser("stop", help="Stop current game")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Get game status")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    client = UnipressClient(args.server)
    
    try:
        if args.command == "health":
            result = client.health_check()
            print(json.dumps(result, indent=2))
            
        elif args.command == "list":
            result = client.list_games()
            print(json.dumps(result, indent=2))
            
        elif args.command == "run":
            print(f"Starting {args.game} with difficulty {args.difficulty}...")
            result = client.run_game(args.game, args.difficulty)
            print(json.dumps(result, indent=2))
            
        elif args.command == "stop":
            result = client.stop_game()
            print(json.dumps(result, indent=2))
            
        elif args.command == "status":
            result = client.game_status()
            print(json.dumps(result, indent=2))
            
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
