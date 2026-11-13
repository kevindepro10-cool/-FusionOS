# Changelog – FusionOS

## 2.1.0 „Hybrid“ (aktuell)

### Neu
- Projekt in saubere Paketstruktur umgezogen:
  - `fusionos/` Kernpaket mit `shell/` (Desktop, Taskbar, Startmenü, Fenster), `system/` (Boot, Sperrbildschirm, Toasts) und `apps/` (eine Datei pro App)
  - `config.py` für alle zentralen Einstellungen (Wallpaper, Taskbar, Desktop-Icons, Benutzer)
  - `docs/` mit Bedienungsanleitung, App-Entwickler-Guide und Changelog
- Terminal: neue Befehle `apps`, `wallpaper`, `ver`
- `LICENSE` (MIT) und `requirements.txt` ergänzt

### Verbessert
- README komplett neu geschrieben (Badges, Tabellen, Struktur, Roadmap, FAQ)
- Terminal zeigt jetzt echte Versionsnummer an

## 2.0.0 „Hybrid“

### Neu
- Kompletter Umbau: native **Python-Desktop-App** (tkinter) statt Webseite
- Windows-11-Look: Taskbar mit mittigen Icons + Start-Button ⊞, Startmenü mit Suche, Fenster mit ─ ▢ ✕
- 9 Apps: Explorer, Terminal, Editor, Rechner, Task-Manager, Browser, Fotos, Einstellungen, Über
- Boot-Splash, Sperrbildschirm, Toast-Benachrichtigungen
- 6 Gradient-Wallpaper, Hell-/Dunkelmodus
- `run.bat` für Doppelklick-Start unter Windows
- Vorstell-Webseite in `website/`

## 1.0.0 „Hybrid“

- Erste Version: Web-Desktop (HTML/CSS/JS) mit macOS-Dock, Startmenü, Spotlight und 8 Apps
