"""Fusion Browser: öffnet Adressen im Standardbrowser des Systems."""

import tkinter as tk
import webbrowser

from .. import theme

QUICK_LINKS = (("GitHub", "https://github.com"),
               ("Wikipedia", "https://wikipedia.org"),
               ("Python", "https://python.org"))


def build(parent, ctx):
    frame = tk.Frame(parent, bg=theme.color("window"))
    frame.pack(fill="both", expand=True)

    bar = tk.Frame(frame, bg=theme.color("titlebar"))
    bar.pack(fill="x")
    url_var = tk.StringVar(value="https://github.com/kevindepro10-cool/FusionOS")
    entry = tk.Entry(bar, textvariable=url_var, bg=theme.color("input"), fg=theme.color("text"),
                     font=(theme.FONT, 11), relief="flat", highlightthickness=1,
                     highlightbackground=theme.color("border"), insertbackground=theme.color("text"))
    entry.pack(side="left", fill="x", expand=True, padx=(10, 6), pady=8, ipady=5)

    def go():
        url = url_var.get().strip()
        if url and not url.startswith(("http://", "https://")):
            url = "https://" + url
        if url:
            webbrowser.open(url)
            ctx.toast("🌐 Wird im Standardbrowser geöffnet…")

    tk.Button(bar, text="Öffnen ➜", relief="flat", bd=0, cursor="hand2", bg=theme.color("accent"),
              fg="#ffffff", font=(theme.FONT, 10, "bold"), padx=14, command=go
              ).pack(side="left", padx=(0, 10), pady=8)
    entry.bind("<Return>", lambda _e: go())

    body = tk.Frame(frame, bg=theme.color("window"))
    body.pack(fill="both", expand=True)
    tk.Label(body, text="◈", font=(theme.FONT, 54), bg=theme.color("window"),
             fg=theme.color("accent")).pack(pady=(60, 4))
    tk.Label(body, text="Fusion Browser", font=(theme.FONT, 16, "bold"),
             bg=theme.color("window"), fg=theme.color("text")).pack()
    tk.Label(body, text="Gib oben eine Adresse ein – die Seite öffnet sich in deinem\n"
                        "Standardbrowser (Edge, Chrome, …). So bist du immer voll kompatibel.",
             justify="center", bg=theme.color("window"), fg=theme.color("text_dim"),
             font=(theme.FONT, 10)).pack(pady=10)

    quick = tk.Frame(body, bg=theme.color("window"))
    quick.pack(pady=6)
    for name, url in QUICK_LINKS:
        tk.Button(quick, text=name, relief="flat", bd=0, cursor="hand2", bg=theme.color("card"),
                  fg=theme.color("text"), font=(theme.FONT, 10), padx=12, pady=5,
                  command=lambda u=url: (url_var.set(u), go())).pack(side="left", padx=4)
