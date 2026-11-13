"""FusionOS – alle mitgelieferten Apps.

Jede Build-Funktion erhält (parent, ctx):
  parent = Frame, in den die App ihre Widgets packt
  ctx    = das FusionOS-Hauptobjekt (open_app, toast, set_wallpaper, ...)
"""

import datetime
import random
import tkinter as tk
from tkinter import ttk, filedialog
import webbrowser

import theme


# ---------------------------------------------------------------- Dateisystem (Demo)
FILESYSTEM = {
    "Desktop": {"Willkommen.txt": "datei", "Projekt FusionOS": "ordner"},
    "Dokumente": {"Lebenslauf.pdf": "datei", "Notizen.txt": "datei", "Rechnungen": "ordner"},
    "Bilder": {"Urlaub.png": "datei", "Familie.jpg": "datei", "Screenshot.png": "datei"},
    "Musik": {"Sommerhit.mp3": "datei", "LoFi-Beat.mp3": "datei"},
    "Downloads": {"fusionos-setup.exe": "datei", "anleitung.pdf": "datei"},
}


def build_explorer(parent, ctx):
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


# ---------------------------------------------------------------- Terminal
def build_terminal(parent, ctx):
    frame = tk.Frame(parent, bg=theme.color("terminal_bg"))
    frame.pack(fill="both", expand=True)

    out = tk.Text(frame, bg=theme.color("terminal_bg"), fg=theme.color("terminal_fg"),
                  font=(theme.FONT_MONO, 11), relief="flat", bd=0, highlightthickness=0,
                  insertbackground=theme.color("terminal_fg"), state="disabled", wrap="word")
    out.pack(fill="both", expand=True, padx=10, pady=(10, 0))

    prompt_row = tk.Frame(frame, bg=theme.color("terminal_bg"))
    prompt_row.pack(fill="x", padx=10, pady=(4, 10))
    tk.Label(prompt_row, text="C:\\Users\\Gast>", bg=theme.color("terminal_bg"),
             fg=theme.color("terminal_accent"), font=(theme.FONT_MONO, 11)).pack(side="left")
    entry = tk.Entry(prompt_row, bg=theme.color("terminal_bg"), fg=theme.color("terminal_fg"),
                     font=(theme.FONT_MONO, 11), relief="flat", insertbackground=theme.color("terminal_fg"))
    entry.pack(side="left", fill="x", expand=True)
    entry.focus_set()

    def print_line(text="", color_fg=None):
        out.config(state="normal")
        tag = "c" if color_fg else None
        if color_fg:
            out.tag_config(tag, foreground=color_fg)
        out.insert("end", text + "\n", tag)
        out.see("end")
        out.config(state="disabled")

    def neofetch():
        w, h = ctx.root.winfo_screenwidth(), ctx.root.winfo_screenheight()
        print_line(
            "        ◈◈◈          FusionOS 1.0 „Hybrid“\n"
            "      ◈◈◈◈◈◈        -------------------------\n"
            "    ◈◈◈     ◈◈◈      OS:      FusionOS 1.0 (Windows × macOS)\n"
            "    ◈◈◈     ◈◈◈      Kernel:  Fusion 6.1-py\n"
            "      ◈◈◈◈◈◈        Shell:   fsh 1.0\n"
            "        ◈◈◈          DE:      FusionShell (Fluent)\n"
            f"                       Auflösung: {w}x{h}\n"
            f"                       Theme:   {'Hell' if theme.mode() == 'light' else 'Dunkel'}",
            theme.color("terminal_accent"))

    commands = {
        "help": lambda a: print_line(
            "Verfügbare Befehle:\n"
            "  help       – diese Hilfe\n"
            "  dir        – Ordner anzeigen\n"
            "  date       – Datum & Uhrzeit\n"
            "  whoami     – aktueller Benutzer\n"
            "  echo TEXT  – Text ausgeben\n"
            "  open APP   – App starten (z.B. open rechner)\n"
            "  neofetch   – Systeminfos\n"
            "  theme      – Hell/Dunkel umschalten\n"
            "  cls        – Bildschirm leeren\n"
            "  shutdown   – FusionOS herunterfahren"),
        "dir": lambda a: print_line("  " + "\n  ".join(FILESYSTEM.keys())),
        "date": lambda a: print_line(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")),
        "whoami": lambda a: print_line("fusionos\\gast"),
        "ver": lambda a: print_line("FusionOS 1.0 „Hybrid“ – Kernel Fusion 6.1-py"),
        "cls": lambda a: out.config(state="normal") or out.delete("1.0", "end") or out.config(state="disabled"),
        "neofetch": lambda a: neofetch(),
        "theme": lambda a: ctx.set_theme("light" if theme.mode() == "dark" else "dark"),
        "shutdown": lambda a: ctx.shutdown(),
        "echo": lambda a: print_line(" ".join(a)),
        "open": lambda a: ctx.open_app((a[0] if a else "").lower()) or print_line(f"Starte {a[0] if a else '?'}…"),
    }
    aliases = {"explorer": "explorer", "dateien": "explorer", "editor": "editor",
               "rechner": "rechner", "einstellungen": "einstellungen", "browser": "browser",
               "fotos": "fotos", "taskmanager": "taskmanager", "info": "info"}

    def run(_event=None):
        raw = entry.get().strip()
        entry.delete(0, "end")
        print_line(f"C:\\Users\\Gast> {raw}", theme.color("terminal_accent"))
        if not raw:
            return
        parts = raw.split()
        cmd, args = parts[0].lower(), parts[1:]
        if cmd == "open":
            key = aliases.get(args[0].lower() if args else "", args[0].lower() if args else "")
            if key in ctx.apps:
                ctx.open_app(key)
                print_line(f"Starte {ctx.apps[key]['name']}…")
            else:
                print_line(f"App nicht gefunden: {args[0] if args else ''}")
            return
        fn = commands.get(cmd)
        if fn:
            try:
                fn(args)
            except Exception as exc:  # noqa: BLE001
                print_line(f"Fehler: {exc}")
        else:
            print_line(f"'{cmd}' ist nicht als Befehl erkannt. Tippe 'help'.")

    entry.bind("<Return>", run)
    print_line("FusionOS Terminal [Version 1.0] — © FusionOS", theme.color("terminal_accent"))
    print_line("Tippe 'help' für alle Befehle.\n")


# ---------------------------------------------------------------- Editor
def build_editor(parent, ctx):
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


# ---------------------------------------------------------------- Rechner
def build_rechner(parent, ctx):
    frame = tk.Frame(parent, bg=theme.color("window"))
    frame.pack(fill="both", expand=True)

    display_var = tk.StringVar(value="0")
    display = tk.Label(frame, textvariable=display_var, bg=theme.color("window"),
                       fg=theme.color("text"), font=(theme.FONT, 26, "bold"), anchor="e")
    display.pack(fill="x", padx=14, pady=(14, 6))

    expr = {"value": "", "error": False}

    def press(k):
        if expr["error"] and k not in ("C",):
            expr["value"] = ""
            expr["error"] = False
        if k == "C":
            expr["value"] = ""
        elif k == "←":
            expr["value"] = expr["value"][:-1]
        elif k == "±":
            expr["value"] = expr["value"].lstrip("-")
            if expr["value"]:
                expr["value"] = "-" + expr["value"]
        elif k == "=":
            try:
                js = expr["value"].replace("÷", "/").replace("×", "*").replace("−", "-").replace("%", "/100")
                if not js or not all(c in "0123456789+-*/.() " for c in js):
                    raise ValueError
                val = eval(js, {"__builtins__": {}})  # noqa: S307 – Eingabe ist gefiltert
                result = str(round(float(val), 10))
                if "." in result:
                    result = result.rstrip("0").rstrip(".")
                expr["value"] = result
            except Exception:  # noqa: BLE001
                expr["error"] = True
                expr["value"] = ""
                display_var.set("Fehler")
                return
        else:
            expr["value"] += k
        display_var.set(expr["value"] or "0")

    grid = tk.Frame(frame, bg=theme.color("window"))
    grid.pack(fill="both", expand=True, padx=8, pady=8)
    keys = ["C", "←", "%", "÷", "7", "8", "9", "×", "4", "5", "6", "−", "1", "2", "3", "+", "±", "0", ".", "="]
    for i, k in enumerate(keys):
        is_op = k in ("÷", "×", "−", "+", "%")
        is_eq = k == "="
        tk.Button(grid, text=k, relief="flat", bd=0, cursor="hand2",
                  bg=theme.color("accent") if is_eq else (theme.color("card") if not is_op else theme.color("hover")),
                  fg="#ffffff" if is_eq else theme.color("text"),
                  activebackground=theme.color("taskbar_hover"),
                  font=(theme.FONT, 13), command=lambda c=k: press(c)
                  ).grid(row=i // 4, column=i % 4, sticky="nsew", padx=2, pady=2)
    for i in range(4):
        grid.columnconfigure(i, weight=1)
    for i in range(5):
        grid.rowconfigure(i, weight=1)


# ---------------------------------------------------------------- Task-Manager
def build_taskmanager(parent, ctx):
    frame = tk.Frame(parent, bg=theme.color("window"))
    frame.pack(fill="both", expand=True)

    stats = tk.Frame(frame, bg=theme.color("window"))
    stats.pack(fill="x", padx=12, pady=10)
    cpu_var = tk.DoubleVar(value=12)
    ram_var = tk.DoubleVar(value=46)
    for label, var in (("CPU", cpu_var), ("RAM", ram_var)):
        row = tk.Frame(stats, bg=theme.color("window"))
        row.pack(fill="x", pady=3)
        tk.Label(row, text=label, width=5, bg=theme.color("window"), fg=theme.color("text_dim"),
                 font=(theme.FONT, 9)).pack(side="left")
        ttk.Style(parent).configure("Fusion.Horizontal.Trough", background=theme.color("input"),
                                    borderwidth=0)
        bar = ttk.Progressbar(row, variable=var, maximum=100, style="Fusion.Horizontal.Trough")
        bar.pack(side="left", fill="x", expand=True, padx=8)
        pct = tk.Label(row, text="12 %", width=6, bg=theme.color("window"), fg=theme.color("text"),
                       font=(theme.FONT, 9), anchor="e")
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
            app_id = list(sel(ctx.windows.keys()))[sel[0]]
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


# ---------------------------------------------------------------- Fotos
def build_fotos(parent, ctx):
    frame = tk.Frame(parent, bg=theme.color("window"))
    frame.pack(fill="both", expand=True)
    grid = tk.Frame(frame, bg=theme.color("window"))
    grid.pack(fill="both", expand=True, padx=12, pady=12)
    tiles = ["🌅", "🏔️", "🌊", "🌸", "🍂", "❄️", "🌴", "🌇", "🦋", "🌻", "🐬", "🍄"]
    palette = ["#e8734a", "#4a7de8", "#3aa8c9", "#d96fb8", "#c98a3a", "#7fb3d9",
               "#3a8a5f", "#d9694a", "#8a6fd9", "#b3c93a", "#3a6fc9", "#a86f3a"]
    for i, emoji in enumerate(tiles):
        tile = tk.Button(grid, text=emoji, relief="flat", bd=0, cursor="hand2",
                         bg=palette[i % len(palette)],
                         activebackground=theme.color("hover"),
                         font=(theme.FONT, 26),
                         command=lambda e=emoji: ctx.toast(f"🖼️ {e} angesehen (Demo)"))
        tile.grid(row=i // 4, column=i % 4, sticky="nsew", padx=4, pady=4)
    for i in range(4):
        grid.columnconfigure(i, weight=1)
    for i in range(3):
        grid.rowconfigure(i, weight=1)


# ---------------------------------------------------------------- Browser
def build_browser(parent, ctx):
    frame = tk.Frame(parent, bg=theme.color("window"))
    frame.pack(fill="both", expand=True)

    bar = tk.Frame(frame, bg=theme.color("titlebar"))
    bar.pack(fill="x")
    url_var = tk.StringVar(value="https://github.com/kevindepro10-cool/-FusionOS")
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
              fg="#ffffff", font=(theme.FONT, 10, "bold"), padx=14, command=go).pack(side="left", padx=(0, 10), pady=8)
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
    for name, url in (("GitHub", "https://github.com"), ("Wikipedia", "https://wikipedia.org"),
                      ("Python", "https://python.org")):
        tk.Button(quick, text=name, relief="flat", bd=0, cursor="hand2", bg=theme.color("card"),
                  fg=theme.color("text"), font=(theme.FONT, 10), padx=12, pady=5,
                  command=lambda u=url: (url_var.set(u), go())).pack(side="left", padx=4)


# ---------------------------------------------------------------- Einstellungen
def build_einstellungen(parent, ctx):
    frame = tk.Frame(parent, bg=theme.color("window"))
    frame.pack(fill="both", expand=True, padx=16, pady=14)

    tk.Label(frame, text="🖼️  Hintergrund", bg=theme.color("window"), fg=theme.color("text"),
             font=(theme.FONT, 12, "bold")).pack(anchor="w")
    grid = tk.Frame(frame, bg=theme.color("window"))
    grid.pack(fill="x", pady=8)
    for i, (name, top, _bottom) in enumerate(ctx.wallpapers):
        sw = tk.Button(grid, text=name, relief="flat", bd=2, cursor="hand2",
                       bg=top, fg="#ffffff", font=(theme.FONT, 9),
                       highlightthickness=0,
                       command=lambda idx=i: ctx.set_wallpaper(idx))
        sw.grid(row=i // 3, column=i % 3, sticky="nsew", padx=4, pady=4, ipady=10)
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
    for k, v in (("Version", "FusionOS 1.0 „Hybrid“"),
                 ("Konzept", "Windows 11 × macOS"),
                 ("Kernel", "Fusion 6.1-py (Python/tkinter)"),
                 ("Abhängigkeiten", "keine – nur Python-Standardbibliothek")):
        row = tk.Frame(info, bg=theme.color("card"))
        row.pack(fill="x", padx=12, pady=3)
        tk.Label(row, text=k, bg=theme.color("card"), fg=theme.color("text_dim"),
                 font=(theme.FONT, 10), width=16, anchor="w").pack(side="left")
        tk.Label(row, text=v, bg=theme.color("card"), fg=theme.color("text"),
                 font=(theme.FONT, 10)).pack(side="left")


# ---------------------------------------------------------------- Über
def build_info(parent, ctx):
    frame = tk.Frame(parent, bg=theme.color("window"))
    frame.pack(fill="both", expand=True)
    tk.Label(frame, text="◈", font=(theme.FONT, 52), bg=theme.color("window"),
             fg=theme.color("accent")).pack(pady=(34, 0))
    tk.Label(frame, text="FusionOS", font=(theme.FONT, 20, "bold"),
             bg=theme.color("window"), fg=theme.color("text")).pack()
    tk.Label(frame, text="Version 1.0 „Hybrid“", bg=theme.color("window"),
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


# ---------------------------------------------------------------- Registry
APPS = {
    "explorer":      {"name": "Explorer",      "icon": "📁", "size": (760, 480), "build": build_explorer},
    "terminal":      {"name": "Terminal",      "icon": "🖥️", "size": (720, 440), "build": build_terminal},
    "editor":        {"name": "Editor",        "icon": "📝", "size": (620, 460), "build": build_editor},
    "rechner":       {"name": "Rechner",       "icon": "🧮", "size": (320, 440), "build": build_rechner},
    "taskmanager":   {"name": "Task-Manager",  "icon": "📊", "size": (560, 420), "build": build_taskmanager},
    "browser":       {"name": "Fusion Browser", "icon": "🌐", "size": (640, 440), "build": build_browser},
    "fotos":         {"name": "Fotos",         "icon": "🖼️", "size": (560, 420), "build": build_fotos},
    "einstellungen": {"name": "Einstellungen", "icon": "⚙️", "size": (620, 500), "build": build_einstellungen},
    "info":          {"name": "Über FusionOS", "icon": "ℹ️", "size": (460, 420), "build": build_info},
}
