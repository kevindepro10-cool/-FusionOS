"""Task-Manager: laufende Fenster verwalten + CPU/RAM-Simulation."""

import random
import tkinter as tk
from tkinter import ttk

from .. import theme


def build(parent, ctx):
    frame = tk.Frame(parent, bg=theme.color("window"))
    frame.pack(fill="both", expand=True)

    stats = tk.Frame(frame, bg=theme.color("window"))
    stats.pack(fill="x", padx=12, pady=10)
    ttk.Style(parent).configure("Fusion.Horizontal.Trough", background=theme.color("input"),
                                borderwidth=0)

    for label_text, initial in (("CPU", 12), ("RAM", 46)):
        row = tk.Frame(stats, bg=theme.color("window"))
        row.pack(fill="x", pady=3)
        tk.Label(row, text=label_text, width=5, bg=theme.color("window"), fg=theme.color("text_dim"),
                 font=(theme.FONT, 9)).pack(side="left")
        var = tk.DoubleVar(value=initial)
        ttk.Progressbar(row, variable=var, maximum=100, style="Fusion.Horizontal.Trough"
                        ).pack(side="left", fill="x", expand=True, padx=8)
        pct = tk.Label(row, text=f"{initial} %", width=6, bg=theme.color("window"),
                       fg=theme.color("text"), font=(theme.FONT, 9), anchor="e")
        pct.pack(side="left")

        def tick(v=var, l=pct):
            if not v.winfo_exists():
                return
            new = max(3, min(97, v.get() + random.uniform(-9, 9)))
            v.set(new)
            l.config(text=f"{int(new)} %")
            l.after(1200, tick)
        tick()

    tk.Label(frame, text="Aktive Fenster", bg=theme.color("window"), fg=theme.color("text_dim"),
             font=(theme.FONT, 9)).pack(anchor="w", padx=12)
    listbox = tk.Listbox(frame, bg=theme.color("input"), fg=theme.color("text"),
                         font=(theme.FONT, 11), relief="flat", highlightthickness=0,
                         selectbackground=theme.color("accent"), activestyle="none")
    listbox.pack(fill="both", expand=True, padx=12, pady=(4, 6))

    def refresh():
        listbox.delete(0, "end")
        for app_id, win in ctx.windows.items():
            marker = " (minimiert)" if getattr(win, "minimized", False) else ""
            listbox.insert("end", f"{ctx.apps[app_id]['icon']}  {ctx.apps[app_id]['name']}{marker}")

    def kill():
        sel = listbox.curselection()
        if sel:
            app_id = list(ctx.windows.keys())[sel[0]]
            ctx.close_app(app_id)
            refresh()

    btns = tk.Frame(frame, bg=theme.color("window"))
    btns.pack(fill="x", padx=12, pady=(0, 12))
    tk.Button(btns, text="Beenden", relief="flat", bd=0, cursor="hand2", bg=theme.color("accent"),
              fg="#ffffff", font=(theme.FONT, 10), padx=14, pady=6, command=kill).pack(side="left")
    tk.Button(btns, text="Aktualisieren", relief="flat", bd=0, cursor="hand2",
              bg=theme.color("card"), fg=theme.color("text"), font=(theme.FONT, 10),
              padx=14, pady=6, command=refresh).pack(side="left", padx=8)
    refresh()
