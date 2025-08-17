# Quick Start Guide

## Overview

This guide will help you get up and running with Unipress in minutes.

## Prerequisites

- Python 3.12+
- uv package manager
- Git

## Installation

```bash
# Clone the repository
git clone https://github.com/jgrynczewski/unipress.git
cd unipress

# Install dependencies
uv sync

# Run the demo game
uv run python main.py
```

## Your First Game

The demo game demonstrates the core mechanics:

- **Spacebar or Click**: Jump
- **Objective**: Avoid obstacles
- **Lives**: 3 attempts

## Next Steps

- Read the [Installation Guide](installation.md) for detailed setup
- Explore [Game Development](first_game.md) to create your own games
- Check [API Reference](../api/base_game.md) for technical details

## Troubleshooting

If you encounter issues:

1. Check Python version: `python --version`
2. Verify uv installation: `uv --version`
3. Check dependencies: `uv pip list`
4. Review logs in `~/.local/share/unipress/logs/`
