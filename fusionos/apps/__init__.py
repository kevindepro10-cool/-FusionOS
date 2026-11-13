"""App-Registry von FusionOS.

Eigene App hinzufügen:
  1. Neue Datei in fusionos/apps/ anlegen mit Funktion  build(parent, ctx)
  2. Hier importieren und im APPS-Dict registrieren –
     sie erscheint automatisch in Startmenü, Taskbar & Desktop.
Siehe auch docs/APPS_ENTWICKELN.md
"""

from .explorer import build as build_explorer
from .terminal import build as build_terminal
from .editor import build as build_editor
from .rechner import build as build_rechner
from .taskmanager import build as build_taskmanager
from .browser import build as build_browser
from .fotos import build as build_fotos
from .einstellungen import build as build_einstellungen
from .info import build as build_info

APPS = {
    "explorer":      {"name": "Explorer",       "icon": "📁", "size": (760, 480), "build": build_explorer},
    "terminal":      {"name": "Terminal",       "icon": "🖥️", "size": (720, 440), "build": build_terminal},
    "editor":        {"name": "Editor",         "icon": "📝", "size": (620, 460), "build": build_editor},
    "rechner":       {"name": "Rechner",        "icon": "🧮", "size": (320, 440), "build": build_rechner},
    "taskmanager":   {"name": "Task-Manager",   "icon": "📊", "size": (560, 420), "build": build_taskmanager},
    "browser":       {"name": "Fusion Browser", "icon": "🌐", "size": (640, 440), "build": build_browser},
    "fotos":         {"name": "Fotos",          "icon": "🖼️", "size": (560, 420), "build": build_fotos},
    "einstellungen": {"name": "Einstellungen",  "icon": "⚙️", "size": (620, 500), "build": build_einstellungen},
    "info":          {"name": "Über FusionOS",  "icon": "ℹ️", "size": (460, 420), "build": build_info},
}
