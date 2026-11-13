"""Rechner-App: vier Grundrechenarten, Prozent, Vorzeichen."""

import tkinter as tk

from .. import theme


def build(parent, ctx):
    frame = tk.Frame(parent, bg=theme.color("window"))
    frame.pack(fill="both", expand=True)

    display_var = tk.StringVar(value="0")
    tk.Label(frame, textvariable=display_var, bg=theme.color("window"),
             fg=theme.color("text"), font=(theme.FONT, 26, "bold"), anchor="e"
             ).pack(fill="x", padx=14, pady=(14, 6))

    expr = {"value": "", "error": False}

    def press(k):
        if expr["error"] and k != "C":
            expr["value"] = ""
            expr["error"] = False
        if k == "C":
            expr["value"] = ""
        elif k == "←":
            expr["value"] = expr["value"][:-1]
        elif k == "±":
            expr["value"] = expr["value"].lstrip("-")
            if expr["value"]:
                expr["value"] = "-" + expr["value"]
        elif k == "=":
            try:
                js = (expr["value"].replace("÷", "/").replace("×", "*")
                      .replace("−", "-").replace("%", "/100"))
                if not js or not all(c in "0123456789+-*/.() " for c in js):
                    raise ValueError
                val = eval(js, {"__builtins__": {}})  # noqa: S307 – Eingabe ist gefiltert
                result = str(round(float(val), 10))
                if "." in result:
                    result = result.rstrip("0").rstrip(".")
                expr["value"] = result
            except Exception:  # noqa: BLE001
                expr["error"] = True
                expr["value"] = ""
                display_var.set("Fehler")
                return
        else:
            expr["value"] += k
        display_var.set(expr["value"] or "0")

    grid = tk.Frame(frame, bg=theme.color("window"))
    grid.pack(fill="both", expand=True, padx=8, pady=8)
    keys = ["C", "←", "%", "÷", "7", "8", "9", "×", "4", "5", "6", "−",
            "1", "2", "3", "+", "±", "0", ".", "="]
    for i, k in enumerate(keys):
        is_op = k in ("÷", "×", "−", "+", "%")
        is_eq = k == "="
        tk.Button(grid, text=k, relief="flat", bd=0, cursor="hand2",
                  bg=theme.color("accent") if is_eq else (theme.color("hover") if is_op else theme.color("card")),
                  fg="#ffffff" if is_eq else theme.color("text"),
                  activebackground=theme.color("taskbar_hover"),
                  font=(theme.FONT, 13), command=lambda c=k: press(c)
                  ).grid(row=i // 4, column=i % 4, sticky="nsew", padx=2, pady=2)
    for i in range(4):
        grid.columnconfigure(i, weight=1)
    for i in range(5):
        grid.rowconfigure(i, weight=1)
