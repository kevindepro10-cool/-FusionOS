"""Fotos-App: bunte Demo-Galerie."""

import tkinter as tk

from .. import theme

TILES = ["🌅", "🏔️", "🌊", "🌸", "🍂", "❄️", "🌴", "🌇", "🦋", "🌻", "🐬", "🍄"]
PALETTE = ["#e8734a", "#4a7de8", "#3aa8c9", "#d96fb8", "#c98a3a", "#7fb3d9",
           "#3a8a5f", "#d9694a", "#8a6fd9", "#b3c93a", "#3a6fc9", "#a86f3a"]


def build(parent, ctx):
    frame = tk.Frame(parent, bg=theme.color("window"))
    frame.pack(fill="both", expand=True)
    grid = tk.Frame(frame, bg=theme.color("window"))
    grid.pack(fill="both", expand=True, padx=12, pady=12)
    for i, emoji in enumerate(TILES):
        tk.Button(grid, text=emoji, relief="flat", bd=0, cursor="hand2",
                  bg=PALETTE[i % len(PALETTE)],
                  activebackground=theme.color("hover"),
                  font=(theme.FONT, 26),
                  command=lambda e=emoji: ctx.toast(f"🖼️ {e} angesehen (Demo)")
                  ).grid(row=i // 4, column=i % 4, sticky="nsew", padx=4, pady=4)
    for i in range(4):
        grid.columnconfigure(i, weight=1)
    for i in range(3):
        grid.rowconfigure(i, weight=1)
