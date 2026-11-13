# Installation – FusionOS

## Windows (empfohlen)

1. **Python installieren**: [python.org/downloads](https://www.python.org/downloads/) → im Installer **„Add Python to PATH“ ankreuzen**
2. **FusionOS laden**: auf GitHub **Code → Download ZIP** → entpacken
3. **Starten**: Doppelklick auf `run.bat`

## macOS / Linux

```bash
python3 main.py
```

(Hinweis: FusionOS ist für Windows gestylt – auf anderen Systemen sieht die Schrift leicht anders aus.)

## Probleme?

| Problem | Lösung |
|---|---|
| `run.bat` schließt sofort | Python installieren und „Add to PATH“ ankreuzen, dann Konsole öffnen und `python main.py` ausführen |
| `tkinter not found` | Bei der Python-Installation „tcl/tk“ mitinstallieren (Standard-Installer tut das automatisch) |
| Fenster zu groß/klein | Fenster an der Ecke `◢` ziehen oder Doppelklick auf die Titelleiste |

## Voraussetzungen

- Python **3.9 oder neuer**
- Keine weiteren Pakete – `requirements.txt` ist absichtlich leer
