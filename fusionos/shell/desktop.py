"""Desktop-Fläche: Gradient-Wallpaper, Icons, Kontextmenü."""

import tkinter as tk

from .. import theme
from .. import config
from ..utils import gradient_photo


class Desktop(tk.Canvas):

    def __init__(self, master, os_ref):
        super().__init__(master, highlightthickness=0, bd=0)
        self.os = os_ref
        self._wall_img = None
        self.bind("<Button-1>", lambda _e: os_ref.close_startmenu())
        self.bind("<Button-3>", self._context_menu)
        self.apply_wallpaper()
        self.build_icons()

    # -- Wallpaper -----------------------------------------------------------
    def apply_wallpaper(self):
        name, top, bottom = config.WALLPAPERS[self.os.wallpaper_index]
        self._wall_img = gradient_photo(self, max(800, self.winfo_screenwidth()),
                                        max(600, self.winfo_screenheight() - config.TASKBAR_H),
                                        top, bottom)
        self.delete("all")
        self.create_image(0, 0, image=self._wall_img, anchor="nw")

    # -- Icons -----------------------------------------------------------
    def build_icons(self):
        self.delete("deskicon")
        for i, (app_id, emoji, label) in enumerate(config.DESKTOP_ICONS):
            x, y = 70, 60 + i * 96
            self.create_text(x, y, text=emoji, font=(theme.FONT, 28),
                             tags=("deskicon", f"icon{i}"))
            self.create_text(x, y + 36, text=label, fill="#ffffff",
                             font=(theme.FONT, 9), tags=("deskicon", f"icon{i}"))
            if app_id == "trash":
                cmd = lambda: self.os.toast("Der Papierkorb ist leer.")  # noqa: E731
            else:
                cmd = lambda a=app_id: self.os.open_app(a)  # noqa: E731
            self.tag_bind(f"icon{i}", "<Double-Button-1>", lambda _e, c=cmd: c())
            self.tag_bind(f"icon{i}", "<Button-3>", self._context_menu)

    # -- Kontextmenü -----------------------------------------------------------
    def _context_menu(self, event):
        os_ref = self.os
        menu = tk.Menu(self, tearoff=0, bg=theme.color("start"), fg=theme.color("text"),
                       activebackground=theme.color("accent"), activeforeground="#ffffff",
                       font=(theme.FONT, 10), bd=0)
        menu.add_command(label="🖼️  Nächster Hintergrund", command=os_ref.next_wallpaper)
        menu.add_command(label="🎨  Hell/Dunkel umschalten", command=os_ref.toggle_theme)
        menu.add_separator()
        menu.add_command(label="🖥️  Terminal öffnen", command=lambda: os_ref.open_app("terminal"))
        menu.add_command(label="⚙️  Einstellungen", command=lambda: os_ref.open_app("einstellungen"))
        menu.add_command(label="📊  Task-Manager", command=lambda: os_ref.open_app("taskmanager"))
        menu.add_separator()
        menu.add_command(label="🔄  Desktop aktualisieren", command=self.build_icons)
        menu.tk_popup(event.x_root, event.y_root)
