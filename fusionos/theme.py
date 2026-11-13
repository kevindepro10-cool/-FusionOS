"""Farben & Schriften von FusionOS (Windows 11 inspired)."""

FONT = "Segoe UI"
FONT_MONO = "Consolas"

DARK = {
    "taskbar": "#1f1f1f",
    "taskbar_hover": "#333333",
    "start": "#252525",
    "start_hover": "#333333",
    "window": "#202020",
    "titlebar": "#2b2b2b",
    "titlebar_text": "#ffffff",
    "text": "#ffffff",
    "text_dim": "#9a9a9a",
    "border": "#3a3a3a",
    "input": "#2d2d2d",
    "hover": "#2f2f2f",
    "accent": "#0a84ff",
    "close_hover": "#c42b1c",
    "terminal_bg": "#0c0c0c",
    "terminal_fg": "#cccccc",
    "terminal_accent": "#4ade80",
    "card": "#2a2a2a",
}

LIGHT = {
    "taskbar": "#f3f3f3",
    "taskbar_hover": "#e2e2e2",
    "start": "#f9f9f9",
    "start_hover": "#e9e9e9",
    "window": "#f6f6f6",
    "titlebar": "#eeeeee",
    "titlebar_text": "#1a1a1a",
    "text": "#1a1a1a",
    "text_dim": "#6b6b6b",
    "border": "#c9c9c9",
    "input": "#ffffff",
    "hover": "#e6e6e6",
    "accent": "#0067c0",
    "close_hover": "#c42b1c",
    "terminal_bg": "#0c0c0c",
    "terminal_fg": "#cccccc",
    "terminal_accent": "#4ade80",
    "card": "#ffffff",
}

_mode = "dark"


def set_mode(mode_name: str) -> None:
    global _mode
    _mode = "light" if mode_name == "light" else "dark"


def mode() -> str:
    return _mode


def color(key: str) -> str:
    palette = LIGHT if _mode == "light" else DARK
    return palette.get(key, "#ff00ff")
