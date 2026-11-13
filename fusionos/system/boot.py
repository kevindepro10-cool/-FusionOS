"""Boot-Splash: ◈-Logo mit Ladebalken, danach Login."""

import random
import tkinter as tk
from tkinter import ttk

from .. import theme
from ..utils import fullscreen_overlay


class BootSplash(tk.Toplevel):

    def __init__(self, root, on_done):
        super().__init__(root, bg="#000000")
        self._on_done = on_done
        fullscreen_overlay(self, root)

        canvas = tk.Canvas(self, bg="#000000", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        canvas.create_text(sw // 2, sh // 2 - 90, text="◈", fill="#ffffff", font=(theme.FONT, 64))
        canvas.create_text(sw // 2, sh // 2, text="F u s i o n O S", fill="#ffffff", font=(theme.FONT, 22))

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Boot.Horizontal.TProgressbar", troughcolor="#333333",
                        background="#ffffff", borderwidth=0, thickness=5)
        self._bar = ttk.Progressbar(self, style="Boot.Horizontal.TProgressbar", maximum=100, value=0)
        self._bar.place(x=sw // 2 - 110, y=sh // 2 + 50, width=220)

        self._step(0)

    def _step(self, value):
        if not self.winfo_exists():
            return
        value = min(100, value + 7 + random.randint(0, 9))
        self._bar["value"] = value
        if value >= 100:
            self.destroy()
            self._on_done()
            return
        self.after(130, lambda: self._step(value))
