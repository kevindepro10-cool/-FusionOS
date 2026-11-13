"""Zentrale Konfiguration von FusionOS."""

# (Name, Farbe oben, Farbe unten) – Gradient-Wallpaper
WALLPAPERS = [
    ("Windows Blau", "#0a1a3f", "#1668dc"),
    ("Bloom Lila", "#1a1035", "#7a3ff2"),
    ("Abendrot", "#2b0f3a", "#ff7a59"),
    ("Wald", "#07130c", "#1d7a46"),
    ("Graphit", "#111114", "#3f3f46"),
    ("Mint", "#04241c", "#0f9d6e"),
]

TASKBAR_H = 52
START_W = 580
START_H = 500
WINDOW_MIN_W = 380
WINDOW_MIN_H = 260

USER_NAME = "Gast"
PROMPT = "C:\\Users\\Gast>"

# Apps, die in der Taskbar angepinnt sind (Reihenfolge = Anzeige)
PINNED_APPS = ("explorer", "terminal", "editor", "browser", "rechner", "einstellungen")

# Apps, die als Icons auf dem Desktop liegen ("trash" = Papierkorb)
DESKTOP_ICONS = [
    ("explorer", "📁", "Explorer"),
    ("terminal", "🖥️", "Terminal"),
    ("editor", "📝", "Editor"),
    ("browser", "🌐", "Browser"),
    ("einstellungen", "⚙️", "Einstellungen"),
    ("trash", "🗑️", "Papierkorb"),
]
