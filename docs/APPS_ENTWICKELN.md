# Eigene Apps schreiben – FusionOS

FusionOS ist bewusst so gebaut, dass du in wenigen Minuten eigene Apps ergänzen kannst.
Keine Frameworks, keine Registrierungs-Magie: eine Funktion + ein Eintrag.

## 1. App-Datei anlegen

Lege eine neue Datei in `fusionos/apps/` an, z.B. `fusionos/apps/uhr.py`:

```python
"""Uhr-App: zeigt die aktuelle Uhrzeit groß an."""

import datetime
import tkinter as tk

from .. import theme


def build(parent, ctx):
    label = tk.Label(parent, text="", bg=theme.color("window"),
                     fg=theme.color("text"), font=(theme.FONT, 48, "bold"))
    label.pack(expand=True)

    def tick():
        if not label.winfo_exists():
            return
        label.config(text=datetime.datetime.now().strftime("%H:%M:%S"))
        label.after(1000, tick)

    tick()
```

### Die Signatur

```python
def build(parent, ctx):
```

- `parent` – ein tk.Frame, in den deine Widgets gehören (pack/grid frei)
- `ctx` – das FusionOS-Hauptobjekt mit nützlichen Methoden:

| ctx-Methode | Wirkung |
|---|---|
| `ctx.open_app("rechner")` | Andere App öffnen |
| `ctx.toast("Hallo!")` | Benachrichtigung unten rechts |
| `ctx.set_theme("light")` | Design umschalten |
| `ctx.set_wallpaper(0)` | Hintergrund setzen |
| `ctx.windows` | Dict der offenen Fenster |
| `ctx.apps` | Die App-Registry |
| `ctx.root` | Das Haupt-Tk-Fenster |

## 2. App registrieren

In `fusionos/apps/__init__.py`:

```python
from .uhr import build as build_uhr

APPS = {
    ...
    "uhr": {"name": "Uhr", "icon": "🕐", "size": (360, 220), "build": build_uhr},
}
```

## 3. Fertig

Die App erscheint automatisch:
- im **Startmenü** (und ist über die Suche findbar),
- im **Terminal** via `open uhr`,
- optional in der **Taskbar**: ID in `config.PINNED_APPS` eintragen,
- optional als **Desktop-Icon**: in `config.DESKTOP_ICONS` eintragen.

## Farben immer aus dem Theme lesen

Damit deine App in Hell- **und** Dunkelmodus gut aussieht, niemals Farben hart codieren:

```python
bg = theme.color("window")     # Flächen
fg = theme.color("text")       # Text
dim = theme.color("text_dim")  # Sekundärtext
accent = theme.color("accent") # Akzent (Windows-Blau)
```

## Konventionen

- Modulname = App-ID (klein, keine Umlaute)
- Docstring oben beschreibt die App kurz
- Buttons: `relief="flat"`, `bd=0`, `cursor="hand2"`, Hover über `activebackground`
- Fenstergröße als `(breite, höhe)` im Registry-Eintrag
