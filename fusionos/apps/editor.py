"""Editor-App: Textbearbeitung mit echten Öffnen-/Speichern-Dialogen."""

import tkinter as tk
from tkinter import filedialog

from .. import theme


def build(parent, ctx):
    bar = tk.Frame(parent, bg=theme.color("titlebar"))
    bar.pack(fill="x")

    text = tk.Text(parent, bg=theme.color("input"), fg=theme.color("text"),
                   font=(theme.FONT_MONO, 11), relief="flat", bd=0, highlightthickness=0,
                   insertbackground=theme.color("text"), undo=True, wrap="word")
    text.pack(fill="both", expand=True)

    def btn(label, cmd):
        tk.Button(bar, text=label, relief="flat", bd=0, cursor="hand2",
                  bg=theme.color("titlebar"), fg=theme.color("text"),
                  activebackground=theme.color("hover"), activeforeground=theme.color("text"),
                  font=(theme.FONT, 9), padx=10, pady=5, command=cmd).pack(side="left", padx=(6, 0), pady=4)

    def save():
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Textdatei", "*.txt"), ("Alle Dateien", "*.*")])
        if path:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text.get("1.0", "end"))
            ctx.toast(f"💾 Gespeichert: {path}")

    def open_file():
        path = filedialog.askopenfilename(filetypes=[("Textdatei", "*.txt"), ("Alle Dateien", "*.*")])
        if path:
            text.delete("1.0", "end")
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                text.insert("1.0", fh.read())

    btn("📝 Neu", lambda: text.delete("1.0", "end"))
    btn("📂 Öffnen", open_file)
    btn("💾 Speichern", save)
