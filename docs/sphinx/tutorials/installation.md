# Installation Guide

## Prerequisites

Before installing Unipress, ensure you have the following prerequisites:

### System Requirements
- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.12 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 1GB free space
- **Graphics**: OpenGL 3.3+ compatible graphics card

### Required Software
- **Python 3.12+**: [Download from python.org](https://www.python.org/downloads/)
- **Git**: [Download from git-scm.com](https://git-scm.com/)
- **Docker** (optional): [Download from docker.com](https://www.docker.com/)

## Installation Methods

### Method 1: Development Installation (Recommended)

#### 1. Clone the Repository
```bash
git clone https://github.com/jgrynczewski/unipress.git
cd unipress
```

#### 2. Install uv Package Manager
```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv
```

#### 3. Install Dependencies
```bash
# Install all dependencies including development tools
uv sync --group dev

# Or install only runtime dependencies
uv sync
```

#### 4. Verify Installation
```bash
# Check Python version
python --version

# Check uv installation
uv --version

# Run a test game
uv run python main.py
```

### Method 2: Docker Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/jgrynczewski/unipress.git
cd unipress
```

#### 2. Build Docker Image
```bash
docker build -t unipress .
```

#### 3. Run with Docker Compose
```bash
# Start the game with audio and display support
docker-compose up

# Or run specific game
docker-compose run --rm unipress python -m unipress.games.jumper.game
```

#### 4. Run Individual Container
```bash
# Run with X11 forwarding (Linux/macOS)
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd):/app \
  unipress

# Run with audio support
docker run -it --rm \
  --device /dev/snd \
  -v $(pwd):/app \
  unipress
```

## Platform-Specific Instructions

### Linux (Ubuntu/Debian)

#### Install System Dependencies
```bash
sudo apt update
sudo apt install -y \
  python3.12 \
  python3.12-venv \
  python3-pip \
  git \
  libgl1-mesa-glx \
  libglib2.0-0 \
  libsm6 \
  libxext6 \
  libxrender-dev \
  libgomp1
```

#### Audio Support (Optional)
```bash
# Install ALSA for audio
sudo apt install -y alsa-utils

# Test audio
speaker-test -t wav -c 2
```

### macOS

#### Install System Dependencies
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and other dependencies
brew install python@3.12 git
```

#### Audio Support
```bash
# macOS has built-in audio support
# No additional installation required
```

### Windows

#### Install System Dependencies
```bash
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Python and Git
choco install python git
```

#### Audio Support
```bash
# Windows has built-in audio support
# No additional installation required
```

## Configuration

### Initial Setup

#### 1. Create Configuration File
```bash
# Copy default settings
cp unipress/settings.toml ~/.config/unipress/settings.toml
```

#### 2. Customize Settings
Edit `~/.config/unipress/settings.toml`:
```toml
[display]
fullscreen = true
width = 1920
height = 1080

[audio]
enabled = true
volume = 0.8

[game]
difficulty = 3
lives = 3
```

#### 3. Set Up Logging
```bash
# Create log directory
mkdir -p ~/.local/share/unipress/logs
```

### Environment Variables

Set these environment variables for customization:

```bash
# Configuration directory
export UNIPRESS_CONFIG_DIR=~/.config/unipress

# Data directory
export UNIPRESS_DATA_DIR=~/.local/share/unipress

# Log level
export UNIPRESS_LOG_LEVEL=INFO

# Language
export UNIPRESS_LANG=pl_PL
```

## Verification

### Test Installation

#### 1. Run Demo Game
```bash
uv run python main.py
```

#### 2. Run Specific Game
```bash
# Run Jumper game with difficulty 5
uv run python -m unipress.games.jumper.game 5

# Run Demo Jump game
uv run python -m unipress.games.demo_jump.game
```

#### 3. Check Audio
```bash
# Test sound system
uv run python -c "from unipress.core.sound import SoundManager; sm = SoundManager(); sm.play('ui', 'button_click')"
```

#### 4. Verify Dependencies
```bash
# Check all dependencies are installed
uv pip list

# Run tests
uv run pytest tests/
```

## Troubleshooting

### Common Issues

#### Python Version Issues
```bash
# Check Python version
python --version

# If wrong version, use specific version
python3.12 --version

# Update PATH if needed
export PATH="/usr/local/bin:$PATH"
```

#### Audio Issues
```bash
# Check audio devices
aplay -l

# Test audio system
speaker-test -t wav -c 2

# Check ALSA configuration
cat /etc/asound.conf
```

#### Display Issues
```bash
# Check OpenGL support
glxinfo | grep "OpenGL version"

# Check X11 forwarding (for Docker)
echo $DISPLAY
xhost +local:docker
```

#### Permission Issues
```bash
# Fix ownership
sudo chown -R $USER:$USER ~/.config/unipress
sudo chown -R $USER:$USER ~/.local/share/unipress

# Fix permissions
chmod 755 ~/.config/unipress
chmod 755 ~/.local/share/unipress
```

### Getting Help

#### Check Logs
```bash
# View application logs
tail -f ~/.local/share/unipress/logs/unipress.log

# View system logs
journalctl -u unipress -f
```

#### Debug Mode
```bash
# Run with debug logging
UNIPRESS_LOG_LEVEL=DEBUG uv run python main.py

# Run with verbose output
uv run python main.py --verbose
```

#### Community Support
- **GitHub Issues**: [Report bugs and request features](https://github.com/jgrynczewski/unipress/issues)
- **Documentation**: [Read the Docs](https://unipress.readthedocs.io/)
- **Discussions**: [GitHub Discussions](https://github.com/jgrynczewski/unipress/discussions)

## Next Steps

After successful installation:

1. **Read the Documentation**: [Getting Started Guide](quick_start.md)
2. **Try the Games**: Run different games and difficulty levels
3. **Explore the Code**: Review the source code structure
4. **Contribute**: Check the [Contributing Guide](contributing.md)
5. **Report Issues**: Help improve Unipress by reporting bugs

## Uninstallation

### Remove Installation
```bash
# Remove source code
rm -rf ~/unipress

# Remove configuration
rm -rf ~/.config/unipress

# Remove data
rm -rf ~/.local/share/unipress

# Remove uv cache (optional)
rm -rf ~/.cache/uv
```

### Remove Dependencies
```bash
# Remove uv
curl -LsSf https://astral.sh/uv/install.sh | sh -s -- --uninstall

# Remove Docker image
docker rmi unipress
```
