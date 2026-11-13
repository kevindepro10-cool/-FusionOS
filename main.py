"""FusionOS 1.0 „Hybrid“ – Python-Desktop-App (Windows 11 × macOS Mix).

Start:  python main.py   (oder Doppelklick auf run.bat unter Windows)
Benoetigt nur die Python-Standardbibliothek (tkinter).
"""

import datetime
import random
import tkinter as tk
from tkinter import ttk

import theme
from apps import APPS

WALLPAPERS = [
    ("Windows Blau", "#0a1a3f", "#1668dc"),
    ("Bloom Lila", "#1a1035", "#7a3ff2"),
    ("Abendrot", "#2b0f3a", "#ff7a59"),
    ("Wald", "#07130c", "#1d7a46"),
    ("Graphit", "#111114", "#3f3f46"),
    ("Mint", "#04241c", "#0f9d6e"),
]

TASKBAR_H = 52
START_W, START_H = 580, 500


def hex2rgb(value: str):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def gradient_photo(widget, width: int, height: int, top: str, bottom: str) -> tk.PhotoImage:
    r1, g1, b1 = hex2rgb(top)
    r2, g2, b2 = hex2rgb(bottom)
    img = tk.PhotoImage(master=widget, width=1, height=max(2, height))
    for y in range(max(2, height)):
        t = y / max(1, height - 1)
        col = "#%02x%02x%02x" % (
            round(r1 + (r2 - r1) * t),
            round(g1 + (g2 - g1) * t),
            round(b1 + (b2 - b1) * t),
        )
        img.put(col, to=(0, y, 1, y + 1))
    return img.zoom(max(1, width), 1)


class FusionWindow(tk.Toplevel):
    """Fenster im Windows-11-Stil: eigener Titelbalken, ─ □ ✕, Resize-Grip."""

    MIN_W, MIN_H = 380, 260

    def __init__(self, master, app_id: str, app: dict, ctx):
        super().__init__(master)
        self.app_id = app_id
        self.ctx = ctx
        self.minimized = False
        self.maximized = False
        self._restore = None

        self.configure(bg=theme.color("window"), bd=0, highlightthickness=1,
                       highlightbackground=theme.color("border"))
        self.overrideredirect(True)

        w, h = app["size"]
        sw, sh = ctx.root.winfo_screenwidth(), ctx.root.winfo_screenheight()
        w, h = min(w, sw - 80), min(h, sh - TASKBAR_H - 80)
        offset = len(ctx.windows) * 28
        x = max(20, (sw - w) // 2 + offset)
        y = max(10, (sh - TASKBAR_H - h) // 2 + offset - 30)
        self.geometry(f"{w}x{h}+{x}+{y}")

        titlebar = tk.Frame(self, bg=theme.color("titlebar"), height=38)
        titlebar.pack(fill="x", side="top")
        titlebar.pack_propagate(False)

        icon_label = tk.Label(titlebar, text=app["icon"], bg=theme.color("titlebar"),
                              fg=theme.color("titlebar_text"), font=(theme.FONT, 11))
        icon_label.pack(side="left", padx=(10, 4))
        title_label = tk.Label(titlebar, text=app["name"], bg=theme.color("titlebar"),
                               fg=theme.color("titlebar_text"), font=(theme.FONT, 10))
        title_label.pack(side="left")

        btns = tk.Frame(titlebar, bg=theme.color("titlebar"))
        btns.pack(side="right")
        for glyph, cmd, hover in (("─", self.do_minimize, theme.color("taskbar_hover")),
                                  ("▢", self.do_maximize, theme.color("taskbar_hover")),
                                  ("✕", self.do_close, theme.color("close_hover"))):
            b = tk.Label(btns, text=glyph, width=4, bg=theme.color("titlebar"),
                         fg=theme.color("titlebar_text"), font=(theme.FONT, 10), cursor="hand2")
            b.pack(side="left", fill="y", ipady=9)
            b.bind("<Button-1>", lambda _e, c=cmd: c())
            b.bind("<Enter>", lambda _e, l=b, hc=hover: l.config(bg=hc))
            b.bind("<Leave>", lambda _e, l=b: l.config(bg=theme.color("titlebar")))

        for widget in (titlebar, icon_label, title_label):
            widget.bind("<Button-1>", self._drag_start)
            widget.bind("<B1-Motion>", self._drag_move)
            widget.bind("<Double-Button-1>", lambda _e: self.do_maximize())

        self.content = tk.Frame(self, bg=theme.color("window"))
        self.content.pack(fill="both", expand=True)

        grip = tk.Label(self, text="◢", bg=theme.color("window"), fg=theme.color("border"),
                        font=(theme.FONT, 9), cursor="size_nwse_se")
        grip.place(relx=1.0, rely=1.0, anchor="se")
        grip.bind("<Button-1>", self._resize_start)
        grip.bind("<B1-Motion>", self._resize_move)

        self.bind("<Button-1>", lambda _e: self.lift())
        self.protocol("WM_DELETE_WINDOW", self.do_close)

    # -- Drag ------------------------------------------------------------
    def _drag_start(self, event):
        if self.maximized:
            return
        self._dx, self._dy = event.x, event.y

    def _drag_move(self, event):
        if self.maximized:
            return
        self.geometry(f"+{event.x_root - self._dx}+{event.y_root - self._dy}")

    # -- Resize ----------------------------------------------------------
    def _resize_start(self, event):
        self._rw, self._rh = self.winfo_width(), self.winfo_height()
        self._rx, self._ry = event.x_root, event.y_root

    def _resize_move(self, event):
        new_w = max(self.MIN_W, self._rw + event.x_root - self._rx)
        new_h = max(self.MIN_H, self._rh + event.y_root - self._ry)
        self.geometry(f"{new_w}x{new_h}")

    # -- Aktionen ----------------------------------------------------------
    def do_minimize(self):
        self.minimized = True
        self.withdraw()
        self.ctx.refresh_taskbar()

    def do_maximize(self):
        sw = self.ctx.root.winfo_screenwidth()
        sh = self.ctx.root.winfo_screenheight() - TASKBAR_H
        if self.maximized:
            self.geometry(self._restore)
            self.maximized = False
        else:
            self._restore = self.geometry()
            self.geometry(f"{sw}x{sh}+0+0")
            self.maximized = True
        self.lift()

    def do_close(self):
        self.ctx.close_app(self.app_id)

    def restore(self):
        self.minimized = False
        self.deiconify()
        self.lift()
        self.ctx.refresh_taskbar()


class StartMenu(tk.Toplevel):
    """Startmenü im Windows-11-Stil: Suche, angepinnte Apps, Benutzer, Power."""

    def __init__(self, ctx):
        super().__init__(ctx.root)
        self.ctx = ctx
        self.configure(bg=theme.color("start"), bd=0)
        self.overrideredirect(True)

        tk.Frame(self, bg=theme.color("border"), height=1).pack(fill="x")
        inner = tk.Frame(self, bg=theme.color("start"))
        inner.pack(fill="both", expand=True, padx=20, pady=16)

        self.search_var = tk.StringVar()
        search = tk.Entry(inner, textvariable=self.search_var, bg=theme.color("input"),
                          fg=theme.color("text"), font=(theme.FONT, 11), relief="flat",
                          highlightthickness=1, highlightbackground=theme.color("border"),
                          insertbackground=theme.color("text"))
        search.pack(fill="x", ipady=7)
        search.bind("<KeyRelease>", lambda _e: self._fill())
        search.bind("<Return>", self._open_first)
        search.bind("<Escape>", lambda _e: self.hide())
        self._search = search

        tk.Label(inner, text="Angepinnt", bg=theme.color("start"), fg=theme.color("text"),
                 font=(theme.FONT, 10, "bold")).pack(anchor="w", pady=(16, 6))

        self.grid_frame = tk.Frame(inner, bg=theme.color("start"))
        self.grid_frame.pack(fill="both", expand=True)

        footer = tk.Frame(inner, bg=theme.color("start"))
        footer.pack(fill="x", side="bottom", pady=(10, 0))
        tk.Label(footer, text="🙂  Gast", bg=theme.color("start"), fg=theme.color("text"),
                 font=(theme.FONT, 10, "bold")).pack(side="left")

        power = tk.Menubutton(footer, text="⏻", relief="flat", bd=0, cursor="hand2",
                              bg=theme.color("start"), fg=theme.color("text"),
                              activebackground=theme.color("start_hover"), font=(theme.FONT, 12))
        menu = tk.Menu(power, tearoff=0, bg=theme.color("start"), fg=theme.color("text"),
                       activebackground=theme.color("accent"), activeforeground="#ffffff",
                       font=(theme.FONT, 10), bd=0)
        menu.add_command(label="🔒  Sperren", command=ctx.lock)
        menu.add_command(label="🔄  Neustart", command=ctx.restart)
        menu.add_command(label="⏻  Herunterfahren", command=ctx.shutdown)
        power["menu"] = menu
        power.pack(side="right")

        self._fill()
        self._position()
        self.lift()
        search.focus_set()

    def _position(self):
        self.update_idletasks()
        sw = self.ctx.root.winfo_screenwidth()
        sh = self.ctx.root.winfo_screenheight()
        w, h = START_W, min(START_H, sh - TASKBAR_H - 40)
        self.geometry(f"{w}x{h}+{max(10, (sw - w) // 2)}+{sh - TASKBAR_H - h - 8}")

    def _fill(self):
        for child in self.grid_frame.winfo_children():
            child.destroy()
        query = self.search_var.get().strip().lower()
        i = 0
        for app_id, app in self.ctx.apps.items():
            if query and query not in app["name"].lower():
                continue
            b = tk.Button(self.grid_frame, text=f"{app['icon']}\n{app['name']}",
                          relief="flat", bd=0, cursor="hand2", bg=theme.color("start"),
                          fg=theme.color("text"), activebackground=theme.color("start_hover"),
                          font=(theme.FONT, 9), width=9, height=3,
                          command=lambda a=app_id: self._launch(a))
            b.grid(row=i // 6, column=i % 6, padx=3, pady=3)
            i += 1
        if i == 0:
            tk.Label(self.grid_frame, text="Keine App gefunden.", bg=theme.color("start"),
                     fg=theme.color("text_dim"), font=(theme.FONT, 10)).grid(row=0, column=0, pady=20)

    def _open_first(self, _event=None):
        query = self.search_var.get().strip().lower()
        for app_id, app in self.ctx.apps.items():
            if not query or query in app["name"].lower():
                self._launch(app_id)
                return

    def _launch(self, app_id):
        self.hide()
        self.ctx.open_app(app_id)

    def hide(self):
        self.ctx.startmenu = None
        self.destroy()


class FusionOS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FusionOS 1.0")
        self.apps = APPS
        self.windows = {}
        self.startmenu = None
        self.wallpaper_index = 0
        self._wall_img = None

        try:
            self.state("zoomed")
        except tk.TclError:
            self.attributes("-fullscreen", True)

        self.configure(bg="#0a1a3f")
        self._build_desktop()
        self._build_taskbar()
        self._bind_keys()
        self._tick_clock()

        self.withdraw()
        self._boot_splash()

    # ---------------------------------------------------------------- Desktop
    def _build_desktop(self):
        self.desktop = tk.Canvas(self, highlightthickness=0, bd=0)
        self.desktop.pack(fill="both", expand=True)
        self.desktop.bind("<Button-1>", lambda _e: self._close_startmenu())
        self.desktop.bind("<Button-3>", self._desktop_menu)
        self._apply_wallpaper()
        self._build_desktop_icons()

    def _apply_wallpaper(self):
        name, top, bottom = WALLPAPERS[self.wallpaper_index]
        self._wall_img = gradient_photo(self.desktop, max(800, self.winfo_screenwidth()),
                                        max(600, self.winfo_screenheight() - TASKBAR_H), top, bottom)
        self.desktop.delete("all")
        self.desktop.create_image(0, 0, image=self._wall_img, anchor="nw")
        self.desktop.create_text(24, self.winfo_screenheight() - TASKBAR_H - 28, anchor="sw",
                                 text=f"◈ FusionOS 1.0 „Hybrid“  ·  {name}",
                                 fill="#ffffff", font=(theme.FONT, 11),
                                 stipple="gray50")

    def _build_desktop_icons(self):
        self.desktop.delete("deskicon")
        icons = [("explorer", "📁", "Explorer"), ("terminal", "🖥️", "Terminal"),
                 ("editor", "📝", "Editor"), ("browser", "🌐", "Browser"),
                 ("einstellungen", "⚙️", "Einstellungen"), ("trash", "🗑️", "Papierkorb")]
        for i, (app_id, emoji, label) in enumerate(icons):
            x, y = 70, 60 + i * 96
            self.desktop.create_text(x, y, text=emoji, font=(theme.FONT, 28),
                                     tags=("deskicon", f"icon{i}"))
            self.desktop.create_text(x, y + 36, text=label, fill="#ffffff",
                                     font=(theme.FONT, 9), tags=("deskicon", f"icon{i}"))
            if app_id == "trash":
                cmd = lambda: self.toast("Der Papierkorb ist leer.")
            else:
                cmd = lambda a=app_id: self.open_app(a)
            self.desktop.tag_bind(f"icon{i}", "<Double-Button-1>", lambda _e, c=cmd: c())
            self.desktop.tag_bind(f"icon{i}", "<Button-3>", self._desktop_menu)

    def _desktop_menu(self, event):
        menu = tk.Menu(self, tearoff=0, bg=theme.color("start"), fg=theme.color("text"),
                       activebackground=theme.color("accent"), activeforeground="#ffffff",
                       font=(theme.FONT, 10), bd=0)
        menu.add_command(label="🖼️  Nächster Hintergrund", command=self.next_wallpaper)
        menu.add_command(label="🎨  Hell/Dunkel umschalten", command=self.toggle_theme)
        menu.add_separator()
        menu.add_command(label="🖥️  Terminal öffnen", command=lambda: self.open_app("terminal"))
        menu.add_command(label="⚙️  Einstellungen", command=lambda: self.open_app("einstellungen"))
        menu.add_command(label="📊  Task-Manager", command=lambda: self.open_app("taskmanager"))
        menu.add_separator()
        menu.add_command(label="🔄  Desktop aktualisieren", command=self._build_desktop_icons)
        menu.tk_popup(event.x_root, event.y_root)

    def set_wallpaper(self, index: int):
        self.wallpaper_index = index % len(WALLPAPERS)
        self._apply_wallpaper()
        self.toast(f"🖼️ Hintergrund: {WALLPAPERS[self.wallpaper_index][0]}")

    def next_wallpaper(self):
        self.set_wallpaper(self.wallpaper_index + 1)

    # ---------------------------------------------------------------- Taskbar
    def _build_taskbar(self):
        self.taskbar = tk.Frame(self, bg=theme.color("taskbar"), height=TASKBAR_H)
        self.taskbar.pack(fill="x", side="bottom")
        self.taskbar.pack_propagate(False)

        center = tk.Frame(self.taskbar, bg=theme.color("taskbar"))
        center.place(relx=0.5, rely=0.5, anchor="center")

        self.start_btn = tk.Label(center, text="⊞", width=3, bg=theme.color("taskbar"),
                                  fg=theme.color("text"), font=(theme.FONT, 16), cursor="hand2")
        self.start_btn.pack(side="left", fill="y", ipady=8)
        self.start_btn.bind("<Button-1>", lambda _e: self.toggle_startmenu())
        self.start_btn.bind("<Enter>", lambda _e: self.start_btn.config(bg=theme.color("taskbar_hover")))
        self.start_btn.bind("<Leave>", lambda _e: self.start_btn.config(bg=theme.color("taskbar")))

        self.pinned = {}
        for app_id in ("explorer", "terminal", "editor", "browser", "rechner", "einstellungen"):
            app = self.apps[app_id]
            item = tk.Frame(center, bg=theme.color("taskbar"))
            item.pack(side="left", padx=1)
            btn = tk.Label(item, text=app["icon"], width=3, bg=theme.color("taskbar"),
                           fg=theme.color("text"), font=(theme.FONT, 14), cursor="hand2")
            btn.pack(fill="y", ipady=8)
            btn.bind("<Button-1>", lambda _e, a=app_id: self.toggle_app(a))
            btn.bind("<Enter>", lambda _e, l=btn: l.config(bg=theme.color("taskbar_hover")))
            btn.bind("<Leave>", lambda _e, l=btn: l.config(bg=theme.color("taskbar")))
            dot = tk.Frame(item, bg=theme.color("taskbar"), height=3, width=18)
            dot.pack(side="bottom")
            self.pinned[app_id] = dot

        tray = tk.Frame(self.taskbar, bg=theme.color("taskbar"))
        tray.place(relx=1.0, rely=0.5, anchor="e", x=-12)
        tk.Label(tray, text="📶 🔊 🔋", bg=theme.color("taskbar"), fg=theme.color("text"),
                 font=(theme.FONT, 10)).pack(side="left", padx=8)
        self.clock_label = tk.Label(tray, text="", bg=theme.color("taskbar"), fg=theme.color("text"),
                                    font=(theme.FONT, 9), justify="center")
        self.clock_label.pack(side="left", padx=(0, 6))

        self.refresh_taskbar()

    def refresh_taskbar(self):
        for app_id, dot in self.pinned.items():
            running = app_id in self.windows
            dot.config(bg=theme.color("accent") if running else theme.color("taskbar"),
                       height=3 if running else 3)

    # ---------------------------------------------------------------- Startmenü
    def toggle_startmenu(self):
        if self.startmenu:
            self._close_startmenu()
        else:
            self._close_startmenu()
            self.startmenu = StartMenu(self)

    def _close_startmenu(self):
        if self.startmenu:
            try:
                self.startmenu.destroy()
            except tk.TclError:
                pass
            self.startmenu = None

    # ---------------------------------------------------------------- Fenster
    def open_app(self, app_id: str):
        app = self.apps.get(app_id)
        if not app:
            self.toast(f"App nicht gefunden: {app_id}")
            return
        self._close_startmenu()
        win = self.windows.get(app_id)
        if win:
            if win.minimized:
                win.restore()
            else:
                win.lift()
            return
        win = FusionWindow(self, app_id, app, self)
        self.windows[app_id] = win
        app["build"](win.content, self)
        win.lift()
        self.refresh_taskbar()

    def toggle_app(self, app_id: str):
        win = self.windows.get(app_id)
        if win and not win.minimized:
            win.minimized = True
            win.withdraw()
            self.refresh_taskbar()
        else:
            self.open_app(app_id)

    def close_app(self, app_id: str):
        win = self.windows.pop(app_id, None)
        if win:
            try:
                win.destroy()
            except tk.TclError:
                pass
        self.refresh_taskbar()

    # ---------------------------------------------------------------- Theme
    def set_theme(self, mode_name: str):
        theme.set_mode(mode_name)
        self.toast("🎨 Design wird angewendet…")
        self._rebuild_ui()

    def toggle_theme(self):
        self.set_theme("light" if theme.mode() == "dark" else "dark")

    def _rebuild_ui(self):
        for app_id in list(self.windows):
            self.close_app(app_id)
        if self.startmenu:
            self._close_startmenu()
        self.taskbar.destroy()
        self._build_taskbar()
        self._build_desktop_icons()
        self.toast("🎨 Design: " + ("Hell ☀️" if theme.mode() == "light" else "Dunkel 🌙"))

    # ---------------------------------------------------------------- Boot / Lock / Shutdown
    def _boot_splash(self, then_lock=True):
        splash = tk.Toplevel(self, bg="#000000")
        splash.overrideredirect(True)
        splash.attributes("-fullscreen", True)
        canvas = tk.Canvas(splash, bg="#000000", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        canvas.create_text(sw // 2, sh // 2 - 90, text="◈", fill="#ffffff", font=(theme.FONT, 64))
        canvas.create_text(sw // 2, sh // 2, text="F u s i o n O S", fill="#ffffff", font=(theme.FONT, 22))
        bar_style = ttk.Style(splash)
        bar_style.theme_use("clam")
        bar_style.configure("Boot.Horizontal.TProgressbar", troughcolor="#333333",
                            background="#ffffff", borderwidth=0, thickness=5)
        bar = ttk.Progressbar(splash, style="Boot.Horizontal.TProgressbar", maximum=100, value=0)
        bar.place(x=sw // 2 - 110, y=sh // 2 + 50, width=220)

        def step(value=0):
            if not splash.winfo_exists():
                return
            value = min(100, value + 7 + random.randint(0, 9))
            bar["value"] = value
            if value >= 100:
                splash.destroy()
                if then_lock:
                    self._lock_screen()
                else:
                    self.deiconify()
                return
            splash.after(130, lambda: step(value))

        step()

    def _lock_screen(self):
        lock = tk.Toplevel(self, bg="#10131c")
        lock.overrideredirect(True)
        lock.attributes("-fullscreen", True)
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        canvas = tk.Canvas(lock, bg="#10131c", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        time_label = tk.Label(lock, text="", bg="#10131c", fg="#ffffff", font=(theme.FONT, 64, "bold"))
        date_label = tk.Label(lock, text="", bg="#10131c", fg="#dddddd", font=(theme.FONT, 16))

        def tick():
            if not lock.winfo_exists():
                return
            now = datetime.datetime.now()
            time_label.config(text=now.strftime("%H:%M"))
            date_label.config(text=now.strftime("%A, %d. %B").replace("Monday", "Montag")
                              .replace("Tuesday", "Dienstag").replace("Wednesday", "Mittwoch")
                              .replace("Thursday", "Donnerstag").replace("Friday", "Freitag")
                              .replace("Saturday", "Samstag").replace("Sunday", "Sonntag")
                              .replace("January", "Januar").replace("February", "Februar")
                              .replace("March", "März").replace("April", "April")
                              .replace("May", "Mai").replace("June", "Juni").replace("July", "Juli")
                              .replace("August", "August").replace("September", "September")
                              .replace("October", "Oktober").replace("November", "November")
                              .replace("December", "Dezember"))
            lock.after(1000, tick)

        tick()
        canvas.create_window(sw // 2, sh // 3, window=time_label)
        canvas.create_window(sw // 2, sh // 3 + 60, window=date_label)
        canvas.create_oval(sw // 2 - 44, sh // 2 - 20, sw // 2 + 44, sh // 2 + 68,
                           fill="#0a84ff", outline="")
        canvas.create_text(sw // 2, sh // 2 + 24, text="🙂", font=(theme.FONT, 34))
        canvas.create_text(sw // 2, sh // 2 + 100, text="Gast", fill="#ffffff", font=(theme.FONT, 16, "bold"))

        pw = tk.Entry(lock, show="•", justify="center", bg="#2a2a35", fg="#ffffff",
                      relief="flat", font=(theme.FONT, 12), width=24, insertbackground="#ffffff")
        canvas.create_window(sw // 2, sh // 2 + 150, window=pw, height=36)
        canvas.create_text(sw // 2, sh // 2 + 190, text="Beliebiges Passwort eingeben + Enter",
                           fill="#888899", font=(theme.FONT, 9))

        def login(_event=None):
            lock.destroy()
            self.deiconify()

        pw.bind("<Return>", login)
        pw.focus_set()

    def lock(self):
        self._close_startmenu()
        self.withdraw()
        self._lock_screen()

    def restart(self):
        self._close_startmenu()
        for app_id in list(self.windows):
            self.close_app(app_id)
        self.withdraw()
        self._boot_splash(then_lock=True)

    def shutdown(self):
        self._close_startmenu()
        self.destroy()

    # ---------------------------------------------------------------- Toast & Uhr
    def toast(self, message: str):
        toast = tk.Toplevel(self, bg=theme.color("titlebar"))
        toast.overrideredirect(True)
        label = tk.Label(toast, text=message, bg=theme.color("titlebar"), fg=theme.color("text"),
                         font=(theme.FONT, 10), padx=18, pady=12)
        label.pack()
        toast.update_idletasks()
        x = self.winfo_screenwidth() - toast.winfo_width() - 20
        y = self.winfo_screenheight() - TASKBAR_H - toast.winfo_height() - 16
        toast.geometry(f"+{x}+{y}")
        toast.lift()
        toast.after(2600, toast.destroy)

    def _tick_clock(self):
        now = datetime.datetime.now()
        try:
            self.clock_label.config(text=f"{now.strftime('%H:%M')}\n{now.strftime('%d.%m.%Y')}")
        except tk.TclError:
            return
        self.after(1000, self._tick_clock)

    # ---------------------------------------------------------------- Tasten
    def _bind_keys(self):
        self.bind("<Escape>", lambda _e: self._close_startmenu())
        self.bind("<Meta_L>", self._win_key)
        self.bind("<Meta_R>", self._win_key)
        self.bind("<Control-Alt-t>", lambda _e: self.open_app("terminal"))

    def _win_key(self, _event):
        self.toggle_startmenu()


def main():
    app = FusionOS()
    app.mainloop()


if __name__ == "__main__":
    main()
