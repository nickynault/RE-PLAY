# Your rebuild loop (clean & repeatable)

Make code changes

Before rebuilding, do:
rmdir /s /q build
rmdir /s /q dist
in git bash

Run PyInstaller
to build, git bash: pyinstaller RE-PLAY.spec

Test dist/RE-PLAY.exe

Upload to GitHub Release and increment version number
v0.1.1 → bug fixes
v0.2.0 → new game added
