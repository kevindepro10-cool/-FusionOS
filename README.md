<div align="center">

# ◈ FusionOS

### *Dein eigenes OS für Windows — Windows 11 trifft macOS*

![Python](https://img.shields.io/badge/Python-3.9%2B-0a84ff?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/Abh%C3%A4ngigkeiten-0-success)
![Platform](https://img.shields.io/badge/Plattform-Windows%2010%2F11-0078d4?logo=windows&logoColor=white)
![License](https://img.shields.io/badge/Lizenz-MIT-green)
![Version](https://img.shields.io/badge/Version-2.2.0%20%E2%80%9EHybrid%E2%80%9C-7a3ff2)

**[Quickstart](#-quickstart-3-minuten) · [Features](#-features) · [Bedienung](#-bedienung) · [Eigene Apps](#-eigene-apps-schreiben) · [FAQ](#-faq)**

Eine echte **Desktop-App in Python** — kein Browser-Spiel, kein Setup, keine Abhängigkeiten.
Boot-Screen, Sperrbildschirm, Taskbar, Startmenü, 9 Apps. Alles drin.

</div>

---

## 🚀 Quickstart (3 Minuten)

```bash
# 1. Python 3.9+ installieren („Add Python to PATH“ ankreuzen!)
#    https://www.python.org/downloads/

# 2. FusionOS laden
#    GitHub → Code → Download ZIP → entpacken

# 3. Starten
run.bat        # Windows: einfach doppelklicken
# oder:
python main.py
```

Dann: Boot-Balken abwarten → am Sperrbildschirm ein **beliebiges Passwort** eingeben → **Enter** → dein Desktop startet. 🎉

> 📦 Detaillierte Anleitung mit Fehlerbehebung: [docs/INSTALLATION.md](docs/INSTALLATION.md)

---

## ✨ Features

### 🪟 Windows 11 (der Hauptteil)

| Feature | Beschreibung |
|---|---|
| **Taskbar** | Unten, Icons mittig, Start-Button ⊞, Laufend-Punkte unter aktiven Apps |
| **Startmenü** | Suche mit Live-Filter, angepinnte App-Kacheln, Benutzer & Power-Menü |
| **Fenster** | ─ ▢ ✕ Buttons, verschieben, an der Ecke skalieren, Doppelklick = maximieren, **Snap** an Bildschirmränder |
| **Task-Manager** | Laufende Fenster beenden + live CPU/RAM-Anzeige |
| **Terminal** | Eigene Shell `fsh` mit 13 Befehlen — inklusive `neofetch` |
| **Akzentfarbe** | Windows-Blau durchgängig (Buttons, Auswahl, Laufend-Punkte) |

### 🍎 macOS (die DNA)

| Feature | Beschreibung |
|---|---|
| **Boot-Erlebnis** | ◈-Logo mit Ladebalken wie beim echten Systemstart |
| **Gradient-Wallpaper** | 6 handgemachte Verläufe (Windows Blau, Bloom Lila, Abendrot …) |
| **Design-Welt** | Glas-Farben, sanfte Hover-Effekte, clean & reduziert |
| **Hell & Dunkel** | Komplettes Zwei-Farben-Theme, jederzeit umschaltbar |

### 📦 Mitgelieferte Apps (9)

| App | Was sie kann |
|---|---|
| 📁 **Explorer** | Schnellzugriff, Navigation, Ordner anlegen & löschen |
| 🖥️ **Terminal** | Eigene Shell: `dir`, `open rechner`, `neofetch`, `theme`, `shutdown` … |
| 📝 **Editor** | Echte Öffnen-/Speichern-Dialoge, Undo |
| 🧮 **Rechner** | Grundrechenarten, Prozent, Vorzeichen, Fehlerbehandlung |
| 📊 **Task-Manager** | Fenster verwalten + CPU/RAM-Simulation |
| 🌐 **Fusion Browser** | Adressen im Standardbrowser öffnen, Quick-Links |
| 🖼️ **Fotos** | Bunte Demo-Galerie |
| ⚙️ **Einstellungen** | Wallpaper, Hell/Dunkel, Systeminfos |
| ℹ️ **Über FusionOS** | Versions- & Systeminfos |

---

## 🎮 Bedienung

| Eingabe | Wirkung |
|---|---|
| `Win`-Taste (⊞) | Startmenü öffnen/schließen |
| `Strg` + `Alt` + `T` | Terminal starten |
| `Esc` | Startmenü schließen |
| Doppelklick Desktop-Icon | App starten |
| Rechtsklick Desktop | Kontextmenü (Hintergrund, Theme, Apps …) |
| Doppelklick Titelleiste | Maximieren/wiederherstellen |

Vollständige Übersicht: [docs/BEDIENUNG.md](docs/BEDIENUNG.md)

---

## 📁 Projektstruktur

```
FusionOS/
├── main.py                     # Startpunkt (3 Zeilen)
├── run.bat                     # Windows-Doppelklick-Starter
├── requirements.txt            # absichtlich leer: 0 Abhängigkeiten
│
├── fusionos/                   # Das "Betriebssystem"
│   ├── __init__.py             # Name, Logo, Version
│   ├── config.py               # Wallpaper, Taskbar, Icons, Benutzer
│   ├── theme.py                # Farben (Dunkel/Hell) & Schriften
│   ├── utils.py                # Gradient-Rendering
│   ├── os.py                   # Hauptklasse: verbindet alles
│   │
│   ├── shell/                  # Die Desktop-Oberfläche
│   │   ├── desktop.py          # Wallpaper, Icons, Kontextmenü
│   │   ├── taskbar.py          # Start-Button, Icons, Uhr
│   │   ├── startmenu.py        # Suche, Kacheln, Power-Menü
│   │   └── window.py           # Fensterverwaltung (─ ▢ ✕)
│   │
│   ├── system/                 # Systemkomponenten
│   │   ├── boot.py             # Boot-Splash mit Ladebalken
│   │   ├── lockscreen.py       # Sperrbildschirm
│   │   └── toast.py            # Benachrichtigungen
│   │
│   └── apps/                   # Eine Datei pro App
│       ├── __init__.py         # App-Registry (hier neue Apps eintragen!)
│       ├── explorer.py         ├── terminal.py
│       ├── editor.py           ├── rechner.py
│       ├── taskmanager.py      ├── browser.py
│       ├── fotos.py            ├── einstellungen.py
│       └── info.py
│
├── docs/                       # Dokumentation
│   ├── INSTALLATION.md         # Setup + Fehlerbehebung
│   ├── BEDIENUNG.md            # Alle Kürzel & Befehle
│   ├── APPS_ENTWICKELN.md      # Tutorial: eigene Apps bauen
│   └── CHANGELOG.md            # Was hat sich geändert
│
└── website/                    # Vorstell-Webseite
    ├── index.html              # Landing-Page (Features, Mix, Quickstart)
    └── style.css
```

---

## 🛠️ Eigene Apps schreiben

In 3 Schritten zur eigenen App — Beispiel **Uhr**:

```python
# fusionos/apps/uhr.py
import datetime
import tkinter as tk
from .. import theme

def build(parent, ctx):
    label = tk.Label(parent, bg=theme.color("window"), fg=theme.color("text"),
                     font=(theme.FONT, 48, "bold"))
    label.pack(expand=True)

    def tick():
        if label.winfo_exists():
            label.config(text=datetime.datetime.now().strftime("%H:%M:%S"))
            label.after(1000, tick)
    tick()
```

```python
# fusionos/apps/__init__.py – registrieren:
from .uhr import build as build_uhr
APPS = { ..., "uhr": {"name": "Uhr", "icon": "🕐", "size": (360, 220), "build": build_uhr} }
```

Fertig — die App erscheint automatisch im Startmenü, in der Suche und im Terminal (`open uhr`).

**Vollständiges Tutorial:** [docs/APPS_ENTWICKELN.md](docs/APPS_ENTWICKELN.md)

Weitere Anpasspunkte:

| Was | Wo |
|---|---|
| Wallpaper hinzufügen | `fusionos/config.py` → `WALLPAPERS` |
| Taskbar/Icons ändern | `fusionos/config.py` → `PINNED_APPS` / `DESKTOP_ICONS` |
| Farben ändern | `fusionos/theme.py` → `DARK` / `LIGHT` |
| Benutzername ändern | `fusionos/config.py` → `USER_NAME` |

---

## 🌐 Vorstell-Webseite

Im Ordner [`website/`](website/) liegt eine fertige Landing-Page (dunkles Design, Feature-Karten, Terminal-Demo).
Lokal ansehen: `website/index.html` öffnen. Öffentlich hosten: [GitHub Pages](https://pages.github.com/) aktivieren (Settings → Pages → Branch `main`, Ordner `/website`).

---

## 🗺️ Roadmap

- [x] Eigene Ordner im Explorer anlegen/löschen *(2.2)*
- [x] Widgets (Uhr) auf dem Desktop *(2.2)*
- [x] Fenster-Snap (an Bildschirmränder andocken) *(2.2)*
- [ ] Sound-Feedback & Startmenü-Animationen
- [ ] Fusion Store: Apps aus einer JSON-Datei nachladen

---

## ❓ FAQ

**Ist das ein echtes Betriebssystem?**
Es ist eine Desktop-Oberfläche als Python-App — ein „OS im OS“. Windows läuft darunter weiter. Ein bootfähiges OS (C/Assembler) wäre ein eigenes, deutlich größeres Projekt.

**Brauche ich Internet?**
Nein. FusionOS läuft komplett offline. (Nur der Fusion Browser öffnet natürlich echte Webseiten.)

**Warum tkinter?**
Weil es in Python eingebaut ist — dadurch startet FusionOS **ohne eine einzige Installation** per `pip`. Einfach Python haben, `run.bat` doppelklicken, fertig.

**Kann ich mitmachen?**
Ja! Fork das Repo, baue eine App ([Tutorial](docs/APPS_ENTWICKELN.md)) und öffne einen Pull Request.

---

<div align="center">

**◈ FusionOS** — gebaut mit Python & tkinter · [MIT-Lizenz](LICENSE) · gemacht von [kevindepro10-cool](https://github.com/kevindepro10-cool)

</div>
