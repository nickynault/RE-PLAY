# RE-PLAY PyInstaller Build Guide

This guide explains how to build a standalone Windows .exe for RE-PLAY using PyInstaller.

## Prerequisites

1. Python 3.8+ installed
2. All project dependencies installed:
   ```bash
   pip install pygame pyinstaller
   ```

## Build Instructions

### Method 1: Command Line (Recommended)
Run this single command from the project root:

```bash
pyinstaller --onefile --windowed --name "RE-PLAY" --hidden-import=pygame --add-data "games;games" --add-data "systems;systems" replay_launcher.py
```

### Method 2: Using build.spec
Run this command from the project root:

```bash
pyinstaller build.spec
```

## Build Output

- Executable: `dist/RE-PLAY.exe`
- Temporary files: `build/` (can be deleted)
- Spec file: `build.spec` (keep for future builds)

## What the Build Includes

- Main game launcher (`replay_launcher.py`)
- All game modules (`games/` directory)
- System modules (`systems/` directory)
- Pygame library and assets
- Required fonts and resources

## Troubleshooting

### Missing Modules
If PyInstaller can't find modules, add them with `--hidden-import`:
```bash
--hidden-import=pygame --hidden-import=systems.game
```

### Missing Assets
If fonts or assets are missing, add them with `--add-data`:
```bash
--add-data "path/to/assets;assets"
```

### Large File Size
The executable will be ~10-15MB due to Pygame and Python runtime.

## Distribution

1. Copy `dist/RE-PLAY.exe` to your distribution folder
2. Users can run it directly (no Python installation required)
3. Windows Defender SmartScreen may show a warning on first run
4. No additional files or dependencies needed

## Development Notes

- Always test the built executable before distribution
- Clean previous builds: `rmdir /s /q dist build`
- Update version in spec file if needed
- Consider code signing for production releases