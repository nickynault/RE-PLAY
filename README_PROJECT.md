# RE:PLAY - Project Structure

## Overview
Minimal Pygame launcher with modular game architecture.

## Project Structure
```
RE-PLAY/
├── replay_launcher.py    # Main launcher with menu system
├── systems/
│   ├── __init__.py
│   ├── game.py          # Base Game interface
│   └── game_manager.py  # Game state management
├── games/
│   ├── __init__.py
│   └── dummy_game.py    # Sample game implementation
└── README_PROJECT.md    # This file
```

## Architecture
- **Game Interface**: Base class for all games (init, update, draw, shutdown)
- **GameManager**: Handles active game lifecycle and state switching
- **Menu System**: Launcher with game selection
- **Modular Design**: Easy to add new games

## Running
```bash
python replay_launcher.py
```

## Adding New Games
1. Create new game class in `games/` folder
2. Inherit from `Game` interface
3. Implement required methods
4. Add to launcher menu

## Dependencies
- pygame==2.6.1