# RE:PLAY — Development Notes

This document exists to keep the project scoped, shippable, and sane.

---

## 🎯 Project Scope
RE:PLAY is a **polished collection**, not a full engine.

Goals:
- Finish games
- Keep systems reusable but simple
- Ship installers regularly

Avoid:
- Overengineering
- Feature creep
- Engine rewrites

---

## 🧱 Architecture
- One launcher application
- Shared systems:
  - Input
  - Audio
  - Settings
  - Save data
- Each game lives in its own module
- Games implement a common interface:
  - init()
  - update()
  - draw()
  - shutdown()

---

## 📦 Distribution Strategy
- Compile with **Nuitka** for stability and performance
- Bundle assets into the build
- Create installer with **Inno Setup**
- Desktop shortcut + uninstall support

Why:
- No Python install required
- Familiar user experience
- Clean removal

---

## 🛠️ Tools (Recommended)
- **VS Code** — debugging and refactoring
- **Pygame** — fast iteration
- **Nuitka** — fewer AV false positives than PyInstaller
- **Inno Setup** — lightweight installer
- **GitHub Releases** — versioned builds

---

## 🧠 Rules to Stay on Task
- One game at a time
- Finish > expand
- Polish before adding features
- If a feature doesn’t improve feel, cut it

---

## 🏠 Project Homepage
Planned:
- GitHub Pages
- Screenshots + short gifs
- Download link
- Short feature list
