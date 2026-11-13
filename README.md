# ◈ FusionOS 1.0 „Hybrid“

Dein eigenes Betriebssystem zum Testen auf Windows — als Mix aus **Windows 11** und **macOS (Apple)**.
Läuft komplett im Browser, keine Installation nötig, funktioniert offline.

## 🚀 So startest du es (Windows)

1. Diesen Ordner (`fusionos`) auf deinen Windows-PC kopieren (z.B. zippen und herunterladen).
2. **Doppelklick auf `index.html`** → öffnet sich in Edge/Chrome/Firefox.
3. Kurz den Boot-Balken abwarten → dann am Sperrbildschirm ein beliebiges „Passwort“ eingeben und Enter drücken. Fertig!

> Optional (runderner): im Ordner eine Konsole öffnen und `python -m http.server` ausführen, dann im Browser `http://localhost:8000` öffnen. Nötig ist das nicht.

## 🍎🪟 Was ist der Windows × Apple Mix?

| Element | Ursprung |
|---|---|
| Menüleiste oben mit App-Namen, Kontrollzentrum, Spotlight | macOS |
| Dock unten mit Lupe-Hover & laufend-Punkten | macOS |
| Startmenü mit angepinnten Apps & Suche (Win-Taste) | Windows 11 |
| Sperrbildschirm mit Uhr & Avatar | Windows Hello / macOS Mix |
| Traffic-Light-Fenster (Schließen/Min/Max) | macOS |
| Terminal, Explorer, Editor, Rechner, Browser, Fotos, Einstellungen | beides 😄 |

## ⌨️ Tastenkürzel

- **Win-Taste (Meta)** → Startmenü öffnen/schließen
- **Strg + Leertaste** → Spotlight-Suche
- **Esc** → alle Popups schließen
- **Rechtsklick auf Desktop** → Kontextmenü (Hintergrund, Theme, Terminal …)

## 🖥️ Terminal-Befehle

`help`, `ls`, `date`, `whoami`, `echo`, `open <app>` (z.B. `open rechner`), `neofetch`, `clear`, `shutdown`

## 🛠️ Anpassen (dein eigenes OS!)

- **Name/Logo ändern:** in `index.html` und `app.js` nach „FusionOS“ bzw. `◈` suchen und ersetzen.
- **Eigene Apps hinzufügen:** in `app.js` im Objekt `APPS` einen neuen Eintrag anlegen und eine `render`-Funktion schreiben.
- **Eigene Hintergründe:** in `style.css` eine neue Klasse `body.wall-<name> { … }` ergänzen und in `app.js` bei `WALLPAPERS` eintragen.
- **Akzentfarbe:** in `style.css` die Variable `--accent` ändern.

## ⚠️ Hinweis

Das ist ein **Desktop-Erlebnis im Browser** (ein „OS in einem OS“) — kein bootfähiges System, das Windows ersetzt. Ein echtes bootfähiges OS zu bauen (C/Assembler, Treiber, ISO) ist ein mehrwöchiges Projekt; diese Web-Variante kannst du sofort testen und weiterentwickeln.
