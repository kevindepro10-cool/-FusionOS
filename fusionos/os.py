"""FusionOS-Hauptklasse: verbindet Shell, Apps und Systemkomponenten."""

import tkinter as tk

from . import theme
from . import config
from .apps import APPS
from .shell.desktop import Desktop
from .shell.taskbar import Taskbar
from .shell.startmenu import StartMenu
from .shell.window import FusionWindow
from .system.boot import BootSplash
from .system.lockscreen import LockScreen
from .system.toast import show_toast


class FusionOS(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("FusionOS")
        self.apps = APPS
        self.windows = {}
        self.startmenu = None
        self.wallpaper_index = 0
        self.wallpapers = config.WALLPAPERS

        try:
            self.state("zoomed")
        except tk.TclError:
            self.attributes("-fullscreen", True)

        self.configure(bg=config.WALLPAPERS[0][1])
        self.desktop = Desktop(self, self)
        self.taskbar = Taskbar(self, self)
        self._bind_keys()

        self.withdraw()
        BootSplash(self, on_done=self._show_lockscreen)

    # ---------------------------------------------------------------- Apps & Fenster
    def open_app(self, app_id: str):
        app = self.apps.get(app_id)
        if not app:
            self.toast(f"App nicht gefunden: {app_id}")
            return
        self.close_startmenu()
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

    def refresh_taskbar(self):
        self.taskbar.refresh()

    # ---------------------------------------------------------------- Startmenü
    def toggle_startmenu(self):
        if self.startmenu:
            self.close_startmenu()
        else:
            self.close_startmenu()
            self.startmenu = StartMenu(self)

    def close_startmenu(self):
        if self.startmenu:
            try:
                self.startmenu.destroy()
            except tk.TclError:
                pass
            self.startmenu = None

    # ---------------------------------------------------------------- Wallpaper & Theme
    def set_wallpaper(self, index: int):
        self.wallpaper_index = index % len(config.WALLPAPERS)
        self.desktop.apply_wallpaper()
        self.toast(f"🖼️ Hintergrund: {config.WALLPAPERS[self.wallpaper_index][0]}")

    def next_wallpaper(self):
        self.set_wallpaper(self.wallpaper_index + 1)

    def set_theme(self, mode_name: str):
        theme.set_mode(mode_name)
        self._rebuild_ui()

    def toggle_theme(self):
        self.set_theme("light" if theme.mode() == "dark" else "dark")

    def _rebuild_ui(self):
        for app_id in list(self.windows):
            self.close_app(app_id)
        self.close_startmenu()
        self.taskbar.destroy()
        self.taskbar = Taskbar(self, self)
        self.desktop.build_icons()
        self.toast("🎨 Design: " + ("Hell ☀️" if theme.mode() == "light" else "Dunkel 🌙"))

    # ---------------------------------------------------------------- System
    def _show_lockscreen(self):
        LockScreen(self, on_login=self.deiconify)

    def lock(self):
        self.close_startmenu()
        self.withdraw()
        self._show_lockscreen()

    def restart(self):
        self.close_startmenu()
        for app_id in list(self.windows):
            self.close_app(app_id)
        self.withdraw()
        BootSplash(self, on_done=self._show_lockscreen)

    def shutdown(self):
        self.close_startmenu()
        self.destroy()

    def toast(self, message: str):
        show_toast(self, message)

    # ---------------------------------------------------------------- Tasten
    def _bind_keys(self):
        self.bind("<Escape>", lambda _e: self.close_startmenu())
        self.bind("<Meta_L>", lambda _e: self.toggle_startmenu())
        self.bind("<Meta_R>", lambda _e: self.toggle_startmenu())
        self.bind("<Control-Alt-t>", lambda _e: self.open_app("terminal"))
