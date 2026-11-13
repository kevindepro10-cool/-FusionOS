"""Explorer-App: Ordner mit Schnellzugriff und Navigation (Demo-Dateisystem)."""

import tkinter as tk

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

    path_label = tk.Label(main, text="Dieser PC › Desktop", bg=theme.color("window"),
                          fg=theme.color("text_dim"), font=(theme.FONT, 9), anchor="w")
    path_label.pack(fill="x", padx=12, pady=(10, 2))

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
