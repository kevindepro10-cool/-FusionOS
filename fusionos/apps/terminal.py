"""Terminal-App: eigene Shell mit Befehlen."""

import datetime
import tkinter as tk

from .. import theme
from .. import config
from .. import __version__
from .explorer import FILESYSTEM

ALIASES = {"explorer": "explorer", "dateien": "explorer", "editor": "editor",
           "rechner": "rechner", "einstellungen": "einstellungen", "browser": "browser",
           "fotos": "fotos", "taskmanager": "taskmanager", "info": "info", "ueber": "info"}


def build(parent, ctx):
    frame = tk.Frame(parent, bg=theme.color("terminal_bg"))
    frame.pack(fill="both", expand=True)

    out = tk.Text(frame, bg=theme.color("terminal_bg"), fg=theme.color("terminal_fg"),
                  font=(theme.FONT_MONO, 11), relief="flat", bd=0, highlightthickness=0,
                  insertbackground=theme.color("terminal_fg"), state="disabled", wrap="word")
    out.pack(fill="both", expand=True, padx=10, pady=(10, 0))

    prompt_row = tk.Frame(frame, bg=theme.color("terminal_bg"))
    prompt_row.pack(fill="x", padx=10, pady=(4, 10))
    tk.Label(prompt_row, text=config.PROMPT, bg=theme.color("terminal_bg"),
             fg=theme.color("terminal_accent"), font=(theme.FONT_MONO, 11)).pack(side="left")
    entry = tk.Entry(prompt_row, bg=theme.color("terminal_bg"), fg=theme.color("terminal_fg"),
                     font=(theme.FONT_MONO, 11), relief="flat",
                     insertbackground=theme.color("terminal_fg"))
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
            "        ◈◈◈          FusionOS „Hybrid“\n"
            "      ◈◈◈◈◈◈        -------------------------\n"
            "    ◈◈◈     ◈◈◈      OS:      FusionOS (Windows × macOS)\n"
            "    ◈◈◈     ◈◈◈      Kernel:  Fusion 6.1-py\n"
            "      ◈◈◈◈◈◈        Shell:   fsh 1.0\n"
            "        ◈◈◈          DE:      FusionShell (Fluent)\n"
            f"                       Auflösung: {w}x{h}\n"
            f"                       Theme:   {'Hell' if theme.mode() == 'light' else 'Dunkel'}",
            theme.color("terminal_accent"))

    def cmd_help(_args):
        print_line(
            "Verfügbare Befehle:\n"
            "  help       – diese Hilfe\n"
            "  dir        – Ordner anzeigen\n"
            "  date       – Datum & Uhrzeit\n"
            "  whoami     – aktueller Benutzer\n"
            "  echo TEXT  – Text ausgeben\n"
            "  open APP   – App starten (z.B. open rechner)\n"
            "  apps       – alle Apps auflisten\n"
            "  neofetch   – Systeminfos\n"
            "  theme      – Hell/Dunkel umschalten\n"
            "  wallpaper  – nächsten Hintergrund setzen\n"
            "  ver        – Versionsinfo\n"
            "  cls        – Bildschirm leeren\n"
            "  shutdown   – FusionOS herunterfahren")

    def cmd_open(args):
        key = ALIASES.get(args[0].lower() if args else "", args[0].lower() if args else "")
        if key in ctx.apps:
            ctx.open_app(key)
            print_line(f"Starte {ctx.apps[key]['name']}…")
        else:
            print_line(f"App nicht gefunden: {args[0] if args else ''}")

    commands = {
        "help": cmd_help,
        "dir": lambda a: print_line("  " + "\n  ".join(FILESYSTEM.keys())),
        "date": lambda a: print_line(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")),
        "whoami": lambda a: print_line(f"fusionos\\{config.USER_NAME.lower()}"),
        "ver": lambda a: print_line(f"FusionOS {__version__} „Hybrid“ – Kernel Fusion 6.1-py"),
        "apps": lambda a: print_line("\n".join(f"  {app['icon']} {app['name']:14s} → open {aid}"
                                               for aid, app in ctx.apps.items())),
        "cls": lambda a: out.config(state="normal") or out.delete("1.0", "end") or out.config(state="disabled"),
        "neofetch": lambda a: neofetch(),
        "theme": lambda a: ctx.set_theme("light" if theme.mode() == "dark" else "dark"),
        "wallpaper": lambda a: ctx.next_wallpaper(),
        "shutdown": lambda a: ctx.shutdown(),
        "echo": lambda a: print_line(" ".join(a)),
        "open": cmd_open,
    }

    def run(_event=None):
        raw = entry.get().strip()
        entry.delete(0, "end")
        print_line(f"{config.PROMPT} {raw}", theme.color("terminal_accent"))
        if not raw:
            return
        parts = raw.split()
        cmd, args = parts[0].lower(), parts[1:]
        fn = commands.get(cmd)
        if fn:
            try:
                fn(args)
            except Exception as exc:  # noqa: BLE001
                print_line(f"Fehler: {exc}")
        else:
            print_line(f"'{cmd}' ist nicht als Befehl erkannt. Tippe 'help'.")

    entry.bind("<Return>", run)
    print_line(f"FusionOS Terminal [Version {__version__}] — © FusionOS",
               theme.color("terminal_accent"))
    print_line("Tippe 'help' für alle Befehle.\n")
