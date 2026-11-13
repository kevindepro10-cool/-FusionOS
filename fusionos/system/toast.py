"""Toast-Benachrichtigungen unten rechts (über der Taskbar)."""

import tkinter as tk

from .. import theme
from .. import config


def show_toast(os_ref, message: str):
    toast = tk.Toplevel(os_ref, bg=theme.color("titlebar"))
    toast.overrideredirect(True)
    tk.Label(toast, text=message, bg=theme.color("titlebar"), fg=theme.color("text"),
             font=(theme.FONT, 10), padx=18, pady=12).pack()
    toast.update_idletasks()
    x = os_ref.winfo_screenwidth() - toast.winfo_width() - 20
    y = os_ref.winfo_screenheight() - config.TASKBAR_H - toast.winfo_height() - 16
    toast.geometry(f"+{x}+{y}")
    toast.lift()
    toast.after(2600, toast.destroy)
