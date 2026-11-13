"""Taskbar im Windows-11-Stil: Start-Button, mittige Icons, Tray & Uhr."""

import datetime
import tkinter as tk

from .. import theme
from .. import config


class Taskbar(tk.Frame):

    def __init__(self, master, os_ref):
        super().__init__(master, bg=theme.color("taskbar"), height=config.TASKBAR_H)
        self.os = os_ref
        self.pinned = {}
        self.pack(fill="x", side="bottom")
        self.pack_propagate(False)

        center = tk.Frame(self, bg=theme.color("taskbar"))
        center.place(relx=0.5, rely=0.5, anchor="center")

        self.start_btn = tk.Label(center, text="⊞", width=3, bg=theme.color("taskbar"),
                                  fg=theme.color("text"), font=(theme.FONT, 16), cursor="hand2")
        self.start_btn.pack(side="left", fill="y", ipady=8)
        self.start_btn.bind("<Button-1>", lambda _e: os_ref.toggle_startmenu())
        self.start_btn.bind("<Enter>", lambda _e: self.start_btn.config(bg=theme.color("taskbar_hover")))
        self.start_btn.bind("<Leave>", lambda _e: self.start_btn.config(bg=theme.color("taskbar")))

        for app_id in config.PINNED_APPS:
            app = os_ref.apps[app_id]
            item = tk.Frame(center, bg=theme.color("taskbar"))
            item.pack(side="left", padx=1)
            btn = tk.Label(item, text=app["icon"], width=3, bg=theme.color("taskbar"),
                           fg=theme.color("text"), font=(theme.FONT, 14), cursor="hand2")
            btn.pack(fill="y", ipady=8)
            btn.bind("<Button-1>", lambda _e, a=app_id: os_ref.toggle_app(a))
            btn.bind("<Enter>", lambda _e, l=btn: l.config(bg=theme.color("taskbar_hover")))
            btn.bind("<Leave>", lambda _e, l=btn: l.config(bg=theme.color("taskbar")))
            dot = tk.Frame(item, bg=theme.color("taskbar"), height=3, width=18)
            dot.pack(side="bottom")
            self.pinned[app_id] = dot

        tray = tk.Frame(self, bg=theme.color("taskbar"))
        tray.place(relx=1.0, rely=0.5, anchor="e", x=-12)
        tk.Label(tray, text="📶 🔊 🔋", bg=theme.color("taskbar"), fg=theme.color("text"),
                 font=(theme.FONT, 10)).pack(side="left", padx=8)
        self.clock_label = tk.Label(tray, text="", bg=theme.color("taskbar"), fg=theme.color("text"),
                                    font=(theme.FONT, 9), justify="center")
        self.clock_label.pack(side="left", padx=(0, 6))

        self.refresh()
        self.tick_clock()

    def refresh(self):
        for app_id, dot in self.pinned.items():
            running = app_id in self.os.windows
            dot.config(bg=theme.color("accent") if running else theme.color("taskbar"), height=3)

    def tick_clock(self):
        now = datetime.datetime.now()
        try:
            self.clock_label.config(text=f"{now.strftime('%H:%M')}\n{now.strftime('%d.%m.%Y')}")
        except tk.TclError:
            return
        self.after(1000, self.tick_clock)
