"""Fenster im Windows-11-Stil: eigener Titelbalken, ─ ▢ ✕, Resize-Grip."""

import tkinter as tk

from .. import theme
from .. import config


class FusionWindow(tk.Toplevel):

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
        w, h = min(w, sw - 80), min(h, sh - config.TASKBAR_H - 80)
        offset = len(ctx.windows) * 28
        x = max(20, (sw - w) // 2 + offset)
        y = max(10, (sh - config.TASKBAR_H - h) // 2 + offset - 30)
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

    # -- Drag --------------------------------------------------------------
    def _drag_start(self, event):
        if self.maximized:
            return
        self._dx, self._dy = event.x, event.y

    def _drag_move(self, event):
        if self.maximized:
            return
        self.geometry(f"+{event.x_root - self._dx}+{event.y_root - self._dy}")

    # -- Resize --------------------------------------------------------------
    def _resize_start(self, event):
        self._rw, self._rh = self.winfo_width(), self.winfo_height()
        self._rx, self._ry = event.x_root, event.y_root

    def _resize_move(self, event):
        new_w = max(config.WINDOW_MIN_W, self._rw + event.x_root - self._rx)
        new_h = max(config.WINDOW_MIN_H, self._rh + event.y_root - self._ry)
        self.geometry(f"{new_w}x{new_h}")

    # -- Aktionen --------------------------------------------------------------
    def do_minimize(self):
        self.minimized = True
        self.withdraw()
        self.ctx.refresh_taskbar()

    def do_maximize(self):
        sw = self.ctx.root.winfo_screenwidth()
        sh = self.ctx.root.winfo_screenheight() - config.TASKBAR_H
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
