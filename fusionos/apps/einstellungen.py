"""Einstellungen: Wallpaper, Design (Hell/Dunkel), Systeminfos."""

import tkinter as tk

from .. import theme
from .. import __version__


def build(parent, ctx):
    frame = tk.Frame(parent, bg=theme.color("window"))
    frame.pack(fill="both", expand=True, padx=16, pady=14)

    tk.Label(frame, text="🖼️  Hintergrund", bg=theme.color("window"), fg=theme.color("text"),
             font=(theme.FONT, 12, "bold")).pack(anchor="w")
    grid = tk.Frame(frame, bg=theme.color("window"))
    grid.pack(fill="x", pady=8)
    for i, (name, top, _bottom) in enumerate(ctx.wallpapers):
        tk.Button(grid, text=name, relief="flat", bd=2, cursor="hand2",
                  bg=top, fg="#ffffff", font=(theme.FONT, 9), highlightthickness=0,
                  command=lambda idx=i: ctx.set_wallpaper(idx)
                  ).grid(row=i // 3, column=i % 3, sticky="nsew", padx=4, pady=4, ipady=10)
    for i in range(3):
        grid.columnconfigure(i, weight=1)

    tk.Label(frame, text="🎨  Design", bg=theme.color("window"), fg=theme.color("text"),
             font=(theme.FONT, 12, "bold")).pack(anchor="w", pady=(14, 6))
    mode_var = tk.StringVar(value=theme.mode())

    def set_mode():
        ctx.set_theme(mode_var.get())

    for value, label in (("dark", "🌙 Dunkel (Standard)"), ("light", "☀️ Hell")):
        tk.Radiobutton(frame, text=label, variable=mode_var, value=value, command=set_mode,
                       bg=theme.color("window"), fg=theme.color("text"),
                       selectcolor=theme.color("input"), activebackground=theme.color("window"),
                       activeforeground=theme.color("text"), font=(theme.FONT, 10),
                       highlightthickness=0).pack(anchor="w")

    tk.Label(frame, text="ℹ️  System", bg=theme.color("window"), fg=theme.color("text"),
             font=(theme.FONT, 12, "bold")).pack(anchor="w", pady=(14, 6))
    info = tk.Frame(frame, bg=theme.color("card"))
    info.pack(fill="x")
    for k, v in (("Version", f"FusionOS {__version__} „Hybrid“"),
                 ("Konzept", "Windows 11 × macOS"),
                 ("Kernel", "Fusion 6.1-py (Python/tkinter)"),
                 ("Abhängigkeiten", "keine – nur Python-Standardbibliothek")):
        row = tk.Frame(info, bg=theme.color("card"))
        row.pack(fill="x", padx=12, pady=3)
        tk.Label(row, text=k, bg=theme.color("card"), fg=theme.color("text_dim"),
                 font=(theme.FONT, 10), width=16, anchor="w").pack(side="left")
        tk.Label(row, text=v, bg=theme.color("card"), fg=theme.color("text"),
                 font=(theme.FONT, 10)).pack(side="left")
