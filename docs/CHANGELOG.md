# Changelog – FusionOS

## 2.2.2 „Hybrid“ (aktuell)

### Behoben
- **Zweiter Start-Absturz behoben (Python 3.13+/Tk 9):** `-fullscreen` und `overrideredirect(True)` dürfen nicht mehr kombiniert werden – Boot-Splash und Sperrbildschirm nutzen jetzt eine gemeinsame, sichere Vollbild-Hilfsfunktion (`utils.fullscreen_overlay`), die das Fenster einfach auf Bildschirmgröße setzt

## 2.2.1 „Hybrid“

### Behoben
- **Start-Absturz behoben:** `tk.Label` akzeptiert bei den Widget-Optionen `padx`/`pady` keine Tupel – das Uhr-Widget nutzt die Polsterung jetzt korrekt über `pack()` (betroffen war Python 3.13/3.14, dort strenger geprüft)

## 2.2.0 „Hybrid“

### Neu
- **Fenster-Snap:** Fenster an den oberen Rand ziehen = maximieren, an linken/rechten Rand = halbe Bildschirmhälfte (wie Windows Snap). Ziehen löst das Fenster wieder.
- **Desktop-Uhr-Widget:** Uhr mit Datum oben rechts auf dem Desktop (in `config.py` per `DESKTOP_CLOCK` abschaltbar)
- **Explorer: Dateioperationen** – Ordner anlegen (📂 Neu) und Einträge löschen (🗑️ Löschen)

## 2.1.0 „Hybrid“

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
