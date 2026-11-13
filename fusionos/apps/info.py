"""Über-App: Systeminfos von FusionOS."""

import tkinter as tk

from .. import theme
from .. import __version__, APP_NAME, LOGO


def build(parent, ctx):
    frame = tk.Frame(parent, bg=theme.color("window"))
    frame.pack(fill="both", expand=True)
    tk.Label(frame, text=LOGO, font=(theme.FONT, 52), bg=theme.color("window"),
             fg=theme.color("accent")).pack(pady=(34, 0))
    tk.Label(frame, text=APP_NAME, font=(theme.FONT, 20, "bold"),
             bg=theme.color("window"), fg=theme.color("text")).pack()
    tk.Label(frame, text=f"Version {__version__} „Hybrid“", bg=theme.color("window"),
             fg=theme.color("text_dim"), font=(theme.FONT, 10)).pack(pady=(0, 14))
    rows = [("Konzept", "Windows 11 × macOS"),
            ("Taskbar & Start", "Windows 11"),
            ("Kernel", "Fusion 6.1-py"),
            ("Sprache", "Python 3 + tkinter"),
            ("Auflösung", f"{ctx.root.winfo_screenwidth()} × {ctx.root.winfo_screenheight()}")]
    for k, v in rows:
        row = tk.Frame(frame, bg=theme.color("window"))
        row.pack()
        tk.Label(row, text=k, bg=theme.color("window"), fg=theme.color("text_dim"),
                 font=(theme.FONT, 10), width=16, anchor="e").pack(side="left", padx=6)
        tk.Label(row, text=v, bg=theme.color("window"), fg=theme.color("text"),
                 font=(theme.FONT, 10, "bold"), anchor="w", width=26).pack(side="left")
    tk.Label(frame, text="\nWin-Taste = Startmenü · Rechtsklick auf Desktop = Menü",
             bg=theme.color("window"), fg=theme.color("text_dim"), font=(theme.FONT, 9)).pack()
