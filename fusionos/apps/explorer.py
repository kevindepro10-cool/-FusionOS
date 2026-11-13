"""Explorer-App: Ordner mit Schnellzugriff, Navigation und Dateioperationen."""

import tkinter as tk
from tkinter import simpledialog

from .. import theme

FILESYSTEM = {
    "Desktop": {"Willkommen.txt": "datei", "Projekt FusionOS": "ordner"},
    "Dokumente": {"Lebenslauf.pdf": "datei", "Notizen.txt": "datei", "Rechnungen": "ordner"},
    "Bilder": {"Urlaub.png": "datei", "Familie.jpg": "datei", "Screenshot.png": "datei"},
    "Musik": {"Sommerhit.mp3": "datei", "LoFi-Beat.mp3": "datei"},
    "Downloads": {"fusionos-setup.exe": "datei", "anleitung.pdf": "datei"},
}


def build(parent, ctx):
    main = tk.Frame(parent, bg=theme.color("window"))
    main.pack(fill="both", expand=True)

    sidebar = tk.Frame(main, bg=theme.color("window"), width=170)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="Schnellzugriff", bg=theme.color("window"),
             fg=theme.color("text_dim"), font=(theme.FONT, 9)).pack(anchor="w", padx=12, pady=(10, 4))

    path_row = tk.Frame(main, bg=theme.color("window"))
    path_row.pack(fill="x", padx=12, pady=(10, 2))
    path_label = tk.Label(path_row, text="Dieser PC › Desktop", bg=theme.color("window"),
                          fg=theme.color("text_dim"), font=(theme.FONT, 9), anchor="w")
    path_label.pack(side="left")

    def tool_btn(label, cmd):
        tk.Button(path_row, text=label, relief="flat", bd=0, cursor="hand2",
                  bg=theme.color("window"), fg=theme.color("text"),
                  activebackground=theme.color("hover"), activeforeground=theme.color("text"),
                  font=(theme.FONT, 9), padx=8, pady=3, command=cmd
                  ).pack(side="right", padx=(6, 0))

    def new_folder():
        name = simpledialog.askstring("Neuer Ordner", "Name des neuen Ordners:", parent=parent)
        if name and name.strip():
            FILESYSTEM.setdefault(current["folder"], {})[name.strip()] = "ordner"
            open_folder(current["folder"])
            ctx.toast(f"📂 Ordner „{name.strip()}“ angelegt")

    def delete_item():
        sel = listbox.curselection()
        if not sel:
            ctx.toast("Erst einen Eintrag auswählen.")
            return
        name = listbox.get(sel[0]).split("  ", 1)[1]
        del FILESYSTEM[current["folder"]][name]
        open_folder(current["folder"])
        ctx.toast(f"🗑️ „{name}“ gelöscht")

    tool_btn("📂 Neu", new_folder)
    tool_btn("🗑️ Löschen", delete_item)

    listbox = tk.Listbox(main, bg=theme.color("input"), fg=theme.color("text"),
                         font=(theme.FONT, 11), relief="flat", highlightthickness=0,
                         selectbackground=theme.color("accent"), activestyle="none")
    listbox.pack(fill="both", expand=True, padx=12, pady=(2, 12))

    current = {"folder": "Desktop"}

    def open_folder(name):
        current["folder"] = name
        path_label.config(text=f"Dieser PC › {name}")
        listbox.delete(0, "end")
        for item, kind in FILESYSTEM.get(name, {}).items():
            icon = "📂" if kind == "ordner" else "📄"
            listbox.insert("end", f"{icon}  {item}")

    for folder in FILESYSTEM:
        b = tk.Button(sidebar, text=f"📁  {folder}", anchor="w", relief="flat",
                      bg=theme.color("window"), fg=theme.color("text"),
                      activebackground=theme.color("hover"), activeforeground=theme.color("text"),
                      font=(theme.FONT, 10), bd=0, padx=12, pady=6, cursor="hand2",
                      command=lambda f=folder: open_folder(f))
        b.pack(fill="x", padx=6, pady=1)

    def on_double(_event):
        sel = listbox.curselection()
        if not sel:
            return
        name = listbox.get(sel[0]).split("  ", 1)[1]
        if FILESYSTEM.get(current["folder"], {}).get(name) == "ordner":
            open_folder(name)
        else:
            ctx.toast(f"„{name}“ ist ein Demo-Inhalt und kann nicht geöffnet werden.")

    listbox.bind("<Double-Button-1>", on_double)
    open_folder("Desktop")
