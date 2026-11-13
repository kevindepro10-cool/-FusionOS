"""Startmenü im Windows-11-Stil: Suche, angepinnte Apps, Benutzer, Power."""

import tkinter as tk

from .. import theme
from .. import config


class StartMenu(tk.Toplevel):

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
        tk.Label(footer, text=f"🙂  {config.USER_NAME}", bg=theme.color("start"),
                 fg=theme.color("text"), font=(theme.FONT, 10, "bold")).pack(side="left")

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
        w, h = config.START_W, min(config.START_H, sh - config.TASKBAR_H - 40)
        self.geometry(f"{w}x{h}+{max(10, (sw - w) // 2)}+{sh - config.TASKBAR_H - h - 8}")

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
