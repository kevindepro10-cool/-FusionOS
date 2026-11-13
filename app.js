/* ============ FusionOS – Systemlogik ============ */
"use strict";

/* ---------- App-Registry ---------- */
const APPS = {
  files:      { name: "Explorer",  icon: "📁", w: 640, h: 420, render: renderFiles },
  terminal:   { name: "Terminal",  icon: "🖥️", w: 620, h: 400, render: renderTerminal },
  editor:     { name: "Editor",    icon: "📝", w: 560, h: 420, render: renderEditor },
  settings:   { name: "Einstellungen", icon: "⚙️", w: 560, h: 460, render: renderSettings },
  calculator: { name: "Rechner",   icon: "🧮", w: 300, h: 420, render: renderCalc },
  browser:    { name: "Fusion Browser", icon: "🌐", w: 760, h: 520, render: renderBrowser },
  photos:     { name: "Fotos",     icon: "🖼️", w: 560, h: 420, render: renderPhotos },
  about:      { name: "Über FusionOS", icon: "ℹ️", w: 420, h: 380, render: renderAbout },
};

const WALLPAPERS = ["wall-aurora", "wall-ocean", "wall-sunset", "wall-forest", "wall-graphite", "wall-mint"];
const WALL_LABELS = { "wall-aurora": "Aurora", "wall-ocean": "Ozean", "wall-sunset": "Sonnenuntergang", "wall-forest": "Wald", "wall-graphite": "Graphit", "wall-mint": "Mint" };

/* ---------- Zustand ---------- */
let wallpaperIndex = 0;
let zCounter = 10;
let openWindows = new Map();   // appId -> window element
let activeAppId = null;
let booted = false;

const $ = (sel) => document.querySelector(sel);

/* ---------- Boot & Login ---------- */
function bootSequence() {
  const fill = $(".boot-fill");
  let p = 0;
  const iv = setInterval(() => {
    p += 8 + Math.random() * 14;
    fill.style.width = Math.min(100, p) + "%";
    if (p >= 100) {
      clearInterval(iv);
      setTimeout(() => {
        $("#boot-screen").classList.add("hidden");
        $("#lock-screen").classList.remove("hidden");
        $("#lock-password").focus();
      }, 350);
    }
  }, 220);
}

$("#lock-form").addEventListener("submit", (e) => {
  e.preventDefault();
  $("#lock-screen").classList.add("hidden");
  $("#desktop").classList.remove("hidden");
  if (!booted) {
    booted = true;
    initDesktop();
    openApp("about");
    toast("Willkommen bei FusionOS! 👋");
  }
});

/* ---------- Uhrzeit ---------- */
function tickClock() {
  const now = new Date();
  const hh = String(now.getHours()).padStart(2, "0");
  const mm = String(now.getMinutes()).padStart(2, "0");
  $("#mb-clock").textContent = `${WEEKDAYS_SHORT[now.getDay()]} ${hh}:${mm}`;
  $("#lock-time").textContent = `${hh}:${mm}`;
  $("#lock-date").textContent = now.toLocaleDateString("de-DE", { weekday: "long", day: "numeric", month: "long" });
}
const WEEKDAYS_SHORT = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"];
setInterval(tickClock, 1000);
tickClock();

/* ---------- Desktop initialisieren ---------- */
function initDesktop() {
  document.body.classList.add(WALLPAPERS[wallpaperIndex]);
  buildDock();
  buildStartMenu();
  buildDesktopIcons();
}

/* ---------- Dock ---------- */
function buildDock() {
  const dock = $("#dock");
  dock.innerHTML = "";
  for (const [id, app] of Object.entries(APPS)) {
    const el = document.createElement("div");
    el.className = "dock-item";
    el.dataset.app = id;
    el.innerHTML = `<span>${app.icon}</span><span class="tooltip">${app.name}</span><span class="dot"></span>`;
    el.addEventListener("click", () => toggleApp(id));
    dock.appendChild(el);
  }
  const sep = document.createElement("div");
  sep.className = "dock-sep";
  dock.appendChild(sep);
  const trash = document.createElement("div");
  trash.className = "dock-item";
  trash.innerHTML = `<span>🗑️</span><span class="tooltip">Papierkorb</span>`;
  trash.addEventListener("click", () => toast("Der Papierkorb ist leer."));
  dock.appendChild(trash);
}

function updateDockDots() {
  document.querySelectorAll(".dock-item[data-app]").forEach((el) => {
    el.classList.toggle("running", openWindows.has(el.dataset.app));
  });
}

function bounceDock(appId) {
  const el = document.querySelector(`.dock-item[data-app="${appId}"]`);
  if (el) { el.classList.add("bounce"); setTimeout(() => el.classList.remove("bounce"), 1100); }
}

/* ---------- Startmenü ---------- */
function buildStartMenu(filter = "") {
  const grid = $("#sm-grid");
  grid.innerHTML = "";
  const f = filter.trim().toLowerCase();
  for (const [id, app] of Object.entries(APPS)) {
    if (f && !app.name.toLowerCase().includes(f)) continue;
    const el = document.createElement("div");
    el.className = "sm-app";
    el.innerHTML = `<span class="emoji">${app.icon}</span><span class="label">${app.name}</span>`;
    el.addEventListener("click", () => { openApp(id); closePopups(); });
    grid.appendChild(el);
  }
}

$("#sm-search-input").addEventListener("input", (e) => buildStartMenu(e.target.value));

/* ---------- Desktop-Icons ---------- */
function buildDesktopIcons() {
  const wrap = $("#desktop-icons");
  wrap.innerHTML = "";
  const icons = [
    { app: "files", label: "Explorer", emoji: "📁" },
    { app: "terminal", label: "Terminal", emoji: "🖥️" },
    { app: "browser", label: "Browser", emoji: "🌐" },
    { app: "settings", label: "Einstellungen", emoji: "⚙️" },
  ];
  for (const ic of icons) {
    const el = document.createElement("div");
    el.className = "desk-icon";
    el.innerHTML = `<span class="emoji">${ic.emoji}</span><span class="label">${ic.label}</span>`;
    el.addEventListener("dblclick", () => openApp(ic.app));
    wrap.appendChild(el);
  }
}

/* ---------- Fenster-Manager ---------- */
function openApp(appId) {
  const app = APPS[appId];
  if (!app) return;
  if (openWindows.has(appId)) {
    const win = openWindows.get(appId);
    if (win.dataset.minimized === "true") {
      win.style.display = "flex";
      win.dataset.minimized = "false";
    }
    focusWindow(win);
    return;
  }
  bounceDock(appId);
  const win = document.createElement("div");
  win.className = "window";
  win.dataset.app = appId;
  const w = Math.min(app.w, window.innerWidth - 60);
  const h = Math.min(app.h, window.innerHeight - 140);
  const offset = openWindows.size * 26;
  win.style.width = w + "px";
  win.style.height = h + "px";
  win.style.left = Math.max(10, (window.innerWidth - w) / 2 + offset) + "px";
  win.style.top = Math.max(44, (window.innerHeight - 100 - h) / 2 + offset - 20) + "px";

  win.innerHTML = `
    <div class="win-titlebar">
      <div class="traffic-lights">
        <button class="tl tl-close" title="Schließen"></button>
        <button class="tl tl-min" title="Minimieren"></button>
        <button class="tl tl-max" title="Maximieren"></button>
      </div>
      <div class="win-title">${app.icon} ${app.name}</div>
      <div class="spacer"></div>
    </div>
    <div class="win-content"></div>
    <div class="resize-handle"></div>
  `;
  $("#windows-layer").appendChild(win);

  app.render(win.querySelector(".win-content"), win);

  // Fenster-Buttons (macOS Traffic Lights)
  win.querySelector(".tl-close").addEventListener("click", () => closeWindow(appId, win));
  win.querySelector(".tl-min").addEventListener("click", () => {
    win.style.display = "none";
    win.dataset.minimized = "true";
  });
  win.querySelector(".tl-max").addEventListener("click", () => toggleMaximize(win));

  win.addEventListener("mousedown", () => focusWindow(win));
  makeDraggable(win, win.querySelector(".win-titlebar"));
  makeResizable(win, win.querySelector(".resize-handle"));

  openWindows.set(appId, win);
  focusWindow(win);
  updateDockDots();
  setMenuAppName(app.name);
}

function closeWindow(appId, win) {
  win.remove();
  openWindows.delete(appId);
  updateDockDots();
  if (activeAppId === appId) setMenuAppName("FusionOS");
}

function toggleMaximize(win) {
  if (win.dataset.maximized === "true") {
    const s = JSON.parse(win.dataset.restore);
    Object.assign(win.style, s);
    win.dataset.maximized = "false";
  } else {
    win.dataset.restore = JSON.stringify({
      left: win.style.left, top: win.style.top, width: win.style.width, height: win.style.height,
    });
    Object.assign(win.style, { left: "0px", top: "0px", width: "100vw", height: "calc(100vh - 30px)" });
    win.dataset.maximized = "true";
  }
}

function focusWindow(win) {
  zCounter += 1;
  win.style.zIndex = zCounter;
  activeAppId = win.dataset.app;
  setMenuAppName(APPS[activeAppId].name);
}

function makeDraggable(win, handle) {
  let sx = 0, sy = 0, ox = 0, oy = 0, dragging = false;
  handle.addEventListener("mousedown", (e) => {
    if (e.target.classList.contains("tl")) return;
    dragging = true;
    sx = e.clientX; sy = e.clientY;
    ox = win.offsetLeft; oy = win.offsetTop;
    e.preventDefault();
  });
  window.addEventListener("mousemove", (e) => {
    if (!dragging) return;
    win.style.left = ox + e.clientX - sx + "px";
    win.style.top = Math.max(0, oy + e.clientY - sy) + "px";
  });
  window.addEventListener("mouseup", () => { dragging = false; });
}

function makeResizable(win, handle) {
  let sx = 0, sy = 0, ow = 0, oh = 0, resizing = false;
  handle.addEventListener("mousedown", (e) => {
    resizing = true;
    sx = e.clientX; sy = e.clientY;
    ow = win.offsetWidth; oh = win.offsetHeight;
    e.preventDefault(); e.stopPropagation();
  });
  window.addEventListener("mousemove", (e) => {
    if (!resizing) return;
    win.style.width = Math.max(320, ow + e.clientX - sx) + "px";
    win.style.height = Math.max(200, oh + e.clientY - sy) + "px";
  });
  window.addEventListener("mouseup", () => { resizing = false; });
}

function toggleApp(appId) {
  if (openWindows.has(appId)) {
    const win = openWindows.get(appId);
    if (win.dataset.minimized !== "true" && activeAppId === appId) {
      win.style.display = "none";
      win.dataset.minimized = "true";
    } else {
      win.style.display = "flex";
      win.dataset.minimized = "false";
      focusWindow(win);
    }
  } else {
    openApp(appId);
  }
}

function setMenuAppName(name) { $("#mb-appname").textContent = name; }

/* ---------- Popups verwalten ---------- */
function closePopups() {
  ["#startmenu", "#controlcenter", "#spotlight", "#contextmenu", "#fusionmenu"].forEach((s) => $(s).classList.add("hidden"));
}

document.addEventListener("mousedown", (e) => {
  const insidePopup = e.target.closest("#startmenu, #controlcenter, #spotlight, #contextmenu, #fusionmenu, #menubar");
  if (!insidePopup) closePopups();
});

/* ---------- Startmenü / Kontrollzentrum / Spotlight Buttons ---------- */
$("#spotlight-btn").addEventListener("click", (e) => {
  e.stopPropagation();
  const sp = $("#spotlight");
  sp.classList.toggle("hidden");
  $("#controlcenter").classList.add("hidden");
  $("#startmenu").classList.add("hidden");
  $("#fusionmenu").classList.add("hidden");
  if (!sp.classList.contains("hidden")) { $("#spotlight-input").value = ""; runSpotlight(""); $("#spotlight-input").focus(); }
});

$("#controlcenter-btn").addEventListener("click", (e) => {
  e.stopPropagation();
  $("#controlcenter").classList.toggle("hidden");
  $("#startmenu").classList.add("hidden");
  $("#spotlight").classList.add("hidden");
  $("#fusionmenu").classList.add("hidden");
});

$("#apple-menu-btn").addEventListener("click", (e) => {
  e.stopPropagation();
  const fm = $("#fusionmenu");
  fm.classList.toggle("hidden");
  fm.style.left = "8px";
  fm.style.top = "34px";
  $("#startmenu").classList.add("hidden");
  $("#controlcenter").classList.add("hidden");
  $("#spotlight").classList.add("hidden");
});

// Windows-typisch: Startmenü über die "Windows-Taste" (Meta) oder Klick aufs Logo? Startmenü öffnet mit Meta-Taste.
document.addEventListener("keydown", (e) => {
  if (e.key === "Meta" || (e.ctrlKey && e.key === "Escape")) {
    e.preventDefault();
    const sm = $("#startmenu");
    const open = sm.classList.contains("hidden");
    closePopups();
    if (open) { sm.classList.remove("hidden"); $("#sm-search-input").value = ""; buildStartMenu(); $("#sm-search-input").focus(); }
  }
  if (e.ctrlKey && e.code === "Space") {
    e.preventDefault();
    $("#spotlight-btn").click();
  }
  if (e.key === "Escape") closePopups();
});

/* ---------- Spotlight-Suche ---------- */
function runSpotlight(q) {
  const res = $("#spotlight-results");
  res.innerHTML = "";
  const f = q.trim().toLowerCase();
  for (const [id, app] of Object.entries(APPS)) {
    if (f && !app.name.toLowerCase().includes(f)) continue;
    const el = document.createElement("div");
    el.className = "spot-item";
    el.innerHTML = `<span class="emoji">${app.icon}</span><span>${app.name}</span>`;
    el.addEventListener("click", () => { openApp(id); closePopups(); });
    res.appendChild(el);
  }
}
$("#spotlight-input").addEventListener("input", (e) => runSpotlight(e.target.value));
$("#spotlight-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    const first = $("#spotlight-results .spot-item");
    if (first) first.click();
  }
});

/* ---------- Kontrollzentrum ---------- */
document.querySelectorAll(".cc-toggle").forEach((btn) => {
  btn.addEventListener("click", () => {
    btn.classList.toggle("active");
    const on = btn.classList.contains("active");
    const small = btn.querySelector("small");
    const labels = { wifi: "verbunden", bluetooth: "an", dnd: "an" };
    const labelsOff = { wifi: "getrennt", bluetooth: "aus", dnd: "aus" };
    const key = btn.dataset.toggle;
    small.textContent = " " + (on ? labels[key] : labelsOff[key]);
    toast(`${btn.textContent.trim().split("\n")[0]}: ${on ? "an" : "aus"}`);
  });
});

$("#cc-brightness").addEventListener("input", (e) => {
  $("#brightness-overlay").style.opacity = (100 - e.target.value) / 100 * 0.65;
});
$("#cc-volume").addEventListener("input", (e) => {
  toast(`🔊 Lautstärke: ${e.target.value}%`);
});
$("#cc-theme-btn").addEventListener("click", () => toggleTheme());

function toggleTheme() {
  document.body.classList.toggle("light");
  document.body.classList.toggle("dark");
  toast(document.body.classList.contains("light") ? "☀️ Helles Design" : "🌙 Dunkles Design");
}

/* ---------- Kontextmenü (Rechtsklick) ---------- */
$("#desktop-area").addEventListener("contextmenu", (e) => {
  if (e.target.closest(".window")) return;
  e.preventDefault();
  const cm = $("#contextmenu");
  cm.classList.remove("hidden");
  cm.style.left = Math.min(e.clientX, window.innerWidth - 240) + "px";
  cm.style.top = Math.min(e.clientY, window.innerHeight - 260) + "px";
});

document.querySelectorAll("#contextmenu .ctx-item").forEach((el) => {
  el.addEventListener("click", () => {
    const a = el.dataset.action;
    closePopups();
    if (a === "wallpaper") nextWallpaper();
    if (a === "theme") toggleTheme();
    if (a === "terminal") openApp("terminal");
    if (a === "settings") openApp("settings");
    if (a === "refresh") toast("Desktop aktualisiert");
  });
});

document.querySelectorAll("#fusionmenu .ctx-item").forEach((el) => {
  el.addEventListener("click", () => {
    const a = el.dataset.action;
    closePopups();
    if (a === "about") openApp("about");
    if (a === "settings") openApp("settings");
    if (a === "lock") {
      $("#desktop").classList.add("hidden");
      $("#lock-screen").classList.remove("hidden");
      $("#lock-password").value = "";
    }
    if (a === "shutdown") shutdownSequence();
  });
});

function nextWallpaper() {
  document.body.classList.remove(WALLPAPERS[wallpaperIndex]);
  wallpaperIndex = (wallpaperIndex + 1) % WALLPAPERS.length;
  document.body.classList.add(WALLPAPERS[wallpaperIndex]);
  toast(`🖼️ Hintergrund: ${WALL_LABELS[WALLPAPERS[wallpaperIndex]]}`);
}

function shutdownSequence() {
  closePopups();
  const bs = $("#boot-screen");
  bs.classList.remove("hidden");
  $(".boot-fill").style.width = "100%";
  $(".boot-logo").textContent = "⏻";
  $(".boot-name").textContent = "FusionOS wird neu gestartet…";
  setTimeout(() => location.reload(), 1800);
}

/* ---------- Toast ---------- */
let toastTimer = null;
function toast(msg) {
  const t = $("#toast");
  t.textContent = msg;
  t.classList.remove("hidden");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.add("hidden"), 2000);
}

/* ================= APPS ================= */

/* ---------- Explorer (Dateien) ---------- */
const FILESYSTEM = {
  Desktop: { type: "folder", children: {
    "Willkommen.txt": { type: "file", emoji: "📄" },
    "Projekt FusionOS": { type: "folder", children: { "ideen.txt": { type: "file", emoji: "📄" }, "roadmap.md": { type: "file", emoji: "📘" } } },
  }},
  Dokumente: { type: "folder", children: {
    "Lebenslauf.pdf": { type: "file", emoji: "📕" },
    "Notizen.txt": { type: "file", emoji: "📄" },
    "Rechnungen": { type: "folder", children: { "2025.pdf": { type: "file", emoji: "📕" } } },
  }},
  Bilder: { type: "folder", children: {
    "Urlaub.png": { type: "file", emoji: "🏞️" }, "Familie.jpg": { type: "file", emoji: "🖼️" }, "Screenshot.png": { type: "file", emoji: "🖼️" },
  }},
  Musik: { type: "folder", children: {
    "Sommerhit.mp3": { type: "file", emoji: "🎵" }, "LoFi-Beat.mp3": { type: "file", emoji: "🎵" },
  }},
  Downloads: { type: "folder", children: {
    "fusionos-setup.exe": { type: "file", emoji: "⚙️" }, "anleitung.pdf": { type: "file", emoji: "📕" },
  }},
};

function renderFiles(content) {
  content.innerHTML = `<div class="app-files">
    <div class="files-sidebar"></div>
    <div class="files-main">
      <div class="files-path"></div>
      <div class="files-grid"></div>
    </div>
  </div>`;
  const sidebar = content.querySelector(".files-sidebar");
  const grid = content.querySelector(".files-grid");
  const pathEl = content.querySelector(".files-path");
  let current = "Desktop";

  function show(folder) {
    current = folder;
    sidebar.querySelectorAll("div").forEach((d) => d.classList.toggle("active", d.textContent === folder));
    pathEl.textContent = "Dieser PC › " + folder;
    grid.innerHTML = "";
    const node = FILESYSTEM[folder];
    if (!node || !node.children) return;
    for (const [name, item] of Object.entries(node.children)) {
      const el = document.createElement("div");
      el.className = "file-item";
      const emoji = item.type === "folder" ? "📂" : item.emoji;
      el.innerHTML = `<span class="emoji">${emoji}</span><span>${name}</span>`;
      el.addEventListener("dblclick", () => {
        if (item.type === "folder") toast(`📂 ${name} ist (in dieser Demo) leer`);
        else toast(`"${name}" konnte nicht geöffnet werden (Demo-Inhalt)`);
      });
      grid.appendChild(el);
    }
  }

  for (const folder of Object.keys(FILESYSTEM)) {
    const el = document.createElement("div");
    el.textContent = folder;
    el.addEventListener("click", () => show(folder));
    sidebar.appendChild(el);
  }
  show("Desktop");
}

/* ---------- Terminal ---------- */
function renderTerminal(content) {
  content.innerHTML = `<div class="app-terminal"><div class="t-out"></div><div class="t-line"><span class="t-prompt">gast@fusionos:~$</span> <input type="text" autofocus></div></div>`;
  const term = content.querySelector(".app-terminal");
  const out = content.querySelector(".t-out");
  const input = content.querySelector("input");

  function print(html) {
    const div = document.createElement("div");
    div.className = "t-line";
    div.innerHTML = html;
    out.appendChild(div);
    term.scrollTop = term.scrollHeight;
  }

  print("FusionOS Terminal v1.0 — <span style='color:#4ade80'>Willkommen!</span>");
  print("Tippe <b>help</b> für eine Liste aller Befehle.");

  const commands = {
    help: () => print("Verfügbare Befehle:\n  help      – diese Hilfe\n  ls        – Ordnerinhalt anzeigen\n  date      – Datum & Uhrzeit\n  whoami    – aktueller Benutzer\n  echo TEXT – Text ausgeben\n  open APP  – App starten (z.B. open rechner)\n  neofetch  – Systeminfos\n  clear     – Bildschirm leeren\n  shutdown  – FusionOS neu starten"),
    ls: () => print(Object.keys(FILESYSTEM).join("  ")),
    date: () => print(new Date().toLocaleString("de-DE")),
    whoami: () => print("gast"),
    clear: () => { out.innerHTML = ""; },
    shutdown: () => shutdownSequence(),
    neofetch: () => print(
      `<span style="color:#4ade80">        ◈◈◈        </span>  gast@fusionos\n` +
      `<span style="color:#4ade80">      ◈◈◈◈◈◈      </span>  ---------------\n` +
      `<span style="color:#4ade80">    ◈◈◈    ◈◈◈    </span>  OS: FusionOS 1.0 (Windows × macOS Mix)\n` +
      `<span style="color:#4ade80">  ◈◈◈        ◈◈◈  </span>  Kernel: Fusion 6.1-web\n` +
      `<span style="color:#4ade80">  ◈◈◈        ◈◈◈  </span>  Shell: fsh 1.0\n` +
      `<span style="color:#4ade80">    ◈◈◈    ◈◈◈    </span>  DE: FusionShell (Aqua + Fluent)\n` +
      `<span style="color:#4ade80">      ◈◈◈◈◈◈      </span>  Auflösung: ${window.innerWidth}x${window.innerHeight}\n` +
      `<span style="color:#4ade80">        ◈◈◈        </span>  Theme: ${document.body.classList.contains("light") ? "Hell" : "Dunkel"}`),
  };

  input.addEventListener("keydown", (e) => {
    if (e.key !== "Enter") return;
    const raw = input.value.trim();
    input.value = "";
    print(`<span class="t-prompt">gast@fusionos:~$</span> ${raw}`);
    if (!raw) return;
    const [cmd, ...args] = raw.split(/\s+/);
    const c = cmd.toLowerCase();
    if (c === "echo") { print(args.join(" ")); return; }
    if (c === "open") {
      const key = (args[0] || "").toLowerCase();
      const map = { explorer: "files", dateien: "files", rechner: "calculator", editor: "editor", einstellungen: "settings", browser: "browser", fotos: "photos" };
      const appId = map[key] || key;
      if (APPS[appId]) { openApp(appId); print(`Starte ${APPS[appId].name}…`); }
      else print(`App nicht gefunden: ${args[0]}`);
      return;
    }
    if (commands[c]) { commands[c](); return; }
    print(`fsh: Befehl nicht gefunden: ${cmd}`);
  });

  term.addEventListener("click", () => input.focus());
}

/* ---------- Editor ---------- */
function renderEditor(content) {
  content.innerHTML = `<div class="app-editor">
    <div class="ed-bar">
      <button class="ed-save">💾 Speichern</button>
      <button class="ed-clear">🗑️ Leeren</button>
      <span style="font-size:12px; color:var(--text-dim); align-self:center;">Speichert im Browser (localStorage)</span>
    </div>
    <textarea placeholder="Schreib etwas… (z.B. Ideen für dein eigenes OS)"></textarea>
  </div>`;
  const ta = content.querySelector("textarea");
  ta.value = localStorage.getItem("fusionos-note") || "Meine FusionOS-Notizen:\n- ";
  content.querySelector(".ed-save").addEventListener("click", () => {
    localStorage.setItem("fusionos-note", ta.value);
    toast("💾 Gespeichert!");
  });
  content.querySelector(".ed-clear").addEventListener("click", () => { ta.value = ""; ta.focus(); });
}

/* ---------- Einstellungen ---------- */
function renderSettings(content) {
  content.innerHTML = `<div class="app-settings">
    <div class="settings-section">
      <h3>🖼️ Hintergrund</h3>
      <div class="wall-grid"></div>
    </div>
    <div class="settings-section">
      <h3>🎨 Design</h3>
      <div class="setting-row"><span>Erscheinungsbild</span><button class="btn-theme">Hell / Dunkel wechseln</button></div>
    </div>
    <div class="settings-section">
      <h3>ℹ️ System</h3>
      <div class="setting-row"><span>Version</span><span>FusionOS 1.0 „Hybrid“</span></div>
      <div class="setting-row" style="margin-top:6px"><span>Design-Mix</span><span>macOS Dock & Menüleiste + Windows Startmenü</span></div>
    </div>
  </div>`;
  const grid = content.querySelector(".wall-grid");
  WALLPAPERS.forEach((wp, i) => {
    const sw = document.createElement("div");
    sw.className = "wall-swatch " + wp + (i === wallpaperIndex ? " selected" : "");
    sw.title = WALL_LABELS[wp];
    sw.addEventListener("click", () => {
      document.body.classList.remove(WALLPAPERS[wallpaperIndex]);
      wallpaperIndex = i;
      document.body.classList.add(wp);
      grid.querySelectorAll(".wall-swatch").forEach((s) => s.classList.remove("selected"));
      sw.classList.add("selected");
      toast(`🖼️ Hintergrund: ${WALL_LABELS[wp]}`);
    });
    grid.appendChild(sw);
  });
  content.querySelector(".btn-theme").addEventListener("click", toggleTheme);
}

/* ---------- Rechner ---------- */
function renderCalc(content) {
  content.innerHTML = `<div class="app-calc">
    <div class="calc-display">0</div>
    <div class="calc-grid"></div>
  </div>`;
  const display = content.querySelector(".calc-display");
  const grid = content.querySelector(".calc-grid");
  let expr = "";
  const keys = ["C", "←", "%", "÷", "7", "8", "9", "×", "4", "5", "6", "−", "1", "2", "3", "+", "0", ".", "±", "="];
  keys.forEach((k) => {
    const b = document.createElement("button");
    b.textContent = k;
    if (["÷", "×", "−", "+", "%"].includes(k)) b.className = "op";
    if (k === "=") b.className = "eq";
    b.addEventListener("click", () => press(k));
    grid.appendChild(b);
  });
  function press(k) {
    if (k === "C") expr = "";
    else if (k === "←") expr = expr.slice(0, -1);
    else if (k === "±") expr = expr.startsWith("-") ? expr.slice(1) : "-" + expr;
    else if (k === "=") {
      try {
        const js = expr.replace(/÷/g, "/").replace(/×/g, "*").replace(/−/g, "-").replace(/%/g, "/100");
        if (!/^[0-9+\-*/.() ]+$/.test(js)) throw new Error("bad");
        const val = Function('"use strict"; return (' + js + ')')();
        expr = String(Math.round(val * 1e10) / 1e10);
      } catch { expr = "Fehler"; }
    } else {
      if (expr === "Fehler") expr = "";
      expr += k;
    }
    display.textContent = expr === "" ? "0" : expr;
  }
}

/* ---------- Browser ---------- */
function renderBrowser(content) {
  content.innerHTML = `<div class="app-browser">
    <div class="browser-bar">
      <button class="b-home" title="Startseite">🏠</button>
      <input type="text" placeholder="URL eingeben (z.B. example.com)">
      <button class="b-go" title="Los">➜</button>
    </div>
    <iframe srcdoc="<body style='font-family:sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;height:90vh;background:#f4f4f8'><h1 style='font-size:60px;margin:0'>◈</h1><h2>Fusion Browser</h2><p style='color:#666'>Gib oben eine URL ein.<br>Hinweis: Viele Seiten (Google, YouTube …) verbieten das Einbetten und bleiben leer.</p></body>"></iframe>
  </div>`;
  const iframe = content.querySelector("iframe");
  const urlInput = content.querySelector("input");
  function go() {
    let u = urlInput.value.trim();
    if (!u) return;
    if (!/^https?:\/\//.test(u)) u = "https://" + u;
    urlInput.value = u;
    iframe.removeAttribute("srcdoc");
    iframe.src = u;
  }
  content.querySelector(".b-go").addEventListener("click", go);
  urlInput.addEventListener("keydown", (e) => { if (e.key === "Enter") go(); });
  content.querySelector(".b-home").addEventListener("click", () => {
    iframe.removeAttribute("src");
    iframe.srcdoc = "<body style='font-family:sans-serif;text-align:center;padding-top:80px'><h1 style='font-size:60px'>◈</h1><h2>Fusion Browser</h2></body>";
  });
}

/* ---------- Fotos ---------- */
function renderPhotos(content) {
  const tiles = ["🌅", "🏔️", "🌊", "🌸", "🍂", "❄️", "🌴", "🌇", "🦋", "🌻", "🐬", "🍄"];
  content.innerHTML = `<div class="app-photos"><div class="photo-grid"></div></div>`;
  const grid = content.querySelector(".photo-grid");
  tiles.forEach((t, i) => {
    const el = document.createElement("div");
    el.className = "photo-tile";
    el.style.background = `linear-gradient(${i * 30}deg, hsl(${i * 30},70%,55%), hsl(${i * 30 + 60},70%,45%))`;
    el.textContent = t;
    el.addEventListener("click", () => toast("🖼️ Foto angesehen (Demo)"));
    grid.appendChild(el);
  });
}

/* ---------- Über ---------- */
function renderAbout(content) {
  content.innerHTML = `<div class="app-about">
    <div class="big-logo">◈</div>
    <h2>FusionOS</h2>
    <div class="ver">Version 1.0 „Hybrid“</div>
    <table class="about-table">
      <tr><td>Konzept</td><td>Windows 11 × macOS</td></tr>
      <tr><td>Dock & Menüleiste</td><td>macOS</td></tr>
      <tr><td>Startmenü</td><td>Windows 11</td></tr>
      <tr><td>Kernel</td><td>Fusion 6.1-web</td></tr>
      <tr><td>Speicher</td><td>${(navigator.deviceMemory || 8)} GB (Demo)</td></tr>
      <tr><td>Auflösung</td><td>${window.screen.width} × ${window.screen.height}</td></tr>
    </table>
    <p style="margin-top:18px; font-size:12px; color:var(--text-dim)">◈ + Ctrl+Space = Spotlight · Meta (Win-Taste) = Startmenü</p>
  </div>`;
}

/* ---------- Start ---------- */
bootSequence();
