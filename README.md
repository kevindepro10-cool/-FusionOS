# ◈ FusionOS 1.0 „Hybrid“

**Dein eigenes OS als echte Desktop-App für Windows** — geschrieben in Python, mit dem Look von **Windows 11** und einer Prise macOS. Plus einer Vorstell-Webseite im Ordner `website/`.

---

## 🚀 So startest du FusionOS (Windows)

1. **Python 3.9+ installieren** (falls nicht vorhanden): [python.org/downloads](https://www.python.org/downloads/) → bei der Installation **„Add Python to PATH“ ankreuzen**
2. Dieses Repository herunterladen (**Code → Download ZIP**) und entpacken
3. **Doppelklick auf `run.bat`** — fertig! 🎉

Alternativ in einer Konsole:

```
python main.py
```

> Keine Installation von Paketen nötig — FusionOS nutzt nur die Python-Standardbibliothek (tkinter).

## 🪟 Was ist FusionOS?

Ein kompletter Desktop in einem Fenster — **meistens Windows 11, mit macOS-DNA**:

| Element | Stil |
|---|---|
| Taskbar unten, Icons mittig, Laufend-Punkte | Windows 11 |
| Startmenü mit Suche + angepinnten Apps (⊞ / Win-Taste) | Windows 11 |
| Fenster mit ─ ▢ ✕, Doppelklick auf Titelleiste = Maximieren | Windows 11 |
| Boot-Screen mit ◈-Logo & Ladebalken, Sperrbildschirm | Windows Hello × macOS |
| Gradient-Wallpaper, abgerundete Optik, Glas-Farben | macOS |

### Mitgelieferte Apps (9)

- 📁 **Explorer** — Ordner, Schnellzugriff, Navigation
- 🖥️ **Terminal** — `help`, `dir`, `neofetch`, `open <app>`, `theme`, `shutdown` …
- 📝 **Editor** — Öffnen/Speichern über echte Dateidialoge
- 🧮 **Rechner** — komplett bedienbar
- 📊 **Task-Manager** — laufende Fenster verwalten + CPU/RAM-Anzeige
- 🌐 **Fusion Browser** — öffnet Seiten in deinem Standardbrowser
- 🖼️ **Fotos** — Galerie
- ⚙️ **Einstellungen** — 6 Gradient-Wallpaper, Hell/Dunkel
- ℹ️ **Über FusionOS** — Systeminfos

## ⌨️ Bedienung

- **Win-Taste (⊞)** → Startmenü öffnen/schließen
- **Doppelklick** auf Desktop-Icons → App starten
- **Rechtsklick auf Desktop** → Kontextmenü (Hintergrund, Theme, Terminal, Task-Manager …)
- **Doppelklick auf Fenstertitelleiste** → maximieren/wiederherstellen
- **Escape** → Startmenü schließen

## 🖥️ Terminal-Befehle

`help` · `dir` · `date` · `whoami` · `echo TEXT` · `open <app>` (z.B. `open rechner`) · `neofetch` · `theme` · `cls` · `shutdown`

## 🌐 Vorstell-Webseite

Im Ordner [`website/`](website/) liegt eine komplette Landing-Page für FusionOS (Deutsch, dunkles Design, Features, Quickstart). Einfach `website/index.html` im Browser öffnen — oder den Ordner auf [GitHub Pages](https://pages.github.com/) hosten, dann ist sie öffentlich erreichbar.

## 🛠️ Anpassen (dein eigenes OS!)

- **Name/Logo:** in `main.py` / `apps.py` / `theme.py` nach „FusionOS“ bzw. `◈` suchen
- **Eigene App:** in `apps.py` eine `build_meineapp(parent, ctx)`-Funktion schreiben und im `APPS`-Dict registrieren — sie erscheint automatisch in Startmenü, Taskbar & Desktop
- **Wallpaper:** in `main.py` die Liste `WALLPAPERS` erweitern
- **Farben:** in `theme.py` (`DARK` / `LIGHT`)

## 📁 Projektstruktur

```
├── main.py        # Boot, Login, Desktop, Taskbar, Startmenü, Fenster-Manager
├── apps.py        # Alle 9 Apps
├── theme.py       # Farben (Dunkel/Hell) & Schriften
├── run.bat        # Windows-Doppelklick-Starter
└── website/       # Vorstell-Webseite (index.html + style.css)
```

## ⚠️ Hinweis

FusionOS ist eine **Desktop-Oberfläche als Python-App** — ein „OS im OS“ zum Ausprobieren und Weiterbauen. Windows selbst bleibt dabei dein echtes Betriebssystem darunter.
