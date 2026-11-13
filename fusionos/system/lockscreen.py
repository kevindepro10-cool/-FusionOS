"""Sperrbildschirm mit Uhr, Avatar und Passwortfeld (beliebiges Passwort)."""

import datetime
import tkinter as tk

from .. import theme
from .. import config
from ..utils import fullscreen_overlay

WEEKDAYS = {"Monday": "Montag", "Tuesday": "Dienstag", "Wednesday": "Mittwoch",
            "Thursday": "Donnerstag", "Friday": "Freitag", "Saturday": "Samstag",
            "Sunday": "Sonntag"}
MONTHS = {"January": "Januar", "February": "Februar", "March": "März", "May": "Mai",
          "June": "Juni", "July": "Juli", "October": "Oktober", "December": "Dezember"}


def _german_date(now: datetime.datetime) -> str:
    text = now.strftime("%A, %d. %B")
    for en, de in {**WEEKDAYS, **MONTHS}.items():
        text = text.replace(en, de)
    return text


class LockScreen(tk.Toplevel):

    def __init__(self, root, on_login):
        super().__init__(root, bg="#10131c")
        fullscreen_overlay(self, root)
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()

        canvas = tk.Canvas(self, bg="#10131c", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        time_label = tk.Label(canvas, text="", bg="#10131c", fg="#ffffff",
                              font=(theme.FONT, 64, "bold"))
        date_label = tk.Label(canvas, text="", bg="#10131c", fg="#dddddd", font=(theme.FONT, 16))

        def tick():
            if not self.winfo_exists():
                return
            now = datetime.datetime.now()
            time_label.config(text=now.strftime("%H:%M"))
            date_label.config(text=_german_date(now))
            self.after(1000, tick)

        tick()
        canvas.create_window(sw // 2, sh // 3, window=time_label)
        canvas.create_window(sw // 2, sh // 3 + 60, window=date_label)
        canvas.create_oval(sw // 2 - 44, sh // 2 - 20, sw // 2 + 44, sh // 2 + 68,
                           fill=theme.color("accent"), outline="")
        canvas.create_text(sw // 2, sh // 2 + 24, text="🙂", font=(theme.FONT, 34))
        canvas.create_text(sw // 2, sh // 2 + 100, text=config.USER_NAME,
                           fill="#ffffff", font=(theme.FONT, 16, "bold"))

        pw = tk.Entry(canvas, show="•", justify="center", bg="#2a2a35", fg="#ffffff",
                      relief="flat", font=(theme.FONT, 12), width=24, insertbackground="#ffffff")
        canvas.create_window(sw // 2, sh // 2 + 150, window=pw, height=36)
        canvas.create_text(sw // 2, sh // 2 + 190,
                           text="Beliebiges Passwort eingeben + Enter",
                           fill="#888899", font=(theme.FONT, 9))

        def login(_event=None):
            self.destroy()
            on_login()

        pw.bind("<Return>", login)
        pw.focus_set()
