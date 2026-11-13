"""Hilfsfunktionen (Gradient-Rendering etc.)."""

import tkinter as tk


def hex2rgb(value: str):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def gradient_photo(widget, width: int, height: int, top: str, bottom: str) -> tk.PhotoImage:
    """Erzeugt ein vertikales Gradient-PhotoImage (für Canvas-Hintergründe)."""
    r1, g1, b1 = hex2rgb(top)
    r2, g2, b2 = hex2rgb(bottom)
    height = max(2, height)
    img = tk.PhotoImage(master=widget, width=1, height=height)
    for y in range(height):
        t = y / max(1, height - 1)
        col = "#%02x%02x%02x" % (
            round(r1 + (r2 - r1) * t),
            round(g1 + (g2 - g1) * t),
            round(b1 + (b2 - b1) * t),
        )
        img.put(col, to=(0, y, 1, y + 1))
    return img.zoom(max(1, width), 1)
