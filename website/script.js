/* FusionOS – Webseite: Animationen & Interaktion */

// ---------- Scroll-Reveal ----------
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll(".reveal").forEach((el) => observer.observe(el));

// ---------- Nav: Schatten beim Scrollen ----------
const nav = document.getElementById("nav");
window.addEventListener("scroll", () => {
  nav.classList.toggle("scrolled", window.scrollY > 10);
}, { passive: true });

// ---------- Mobiles Menü ----------
const burger = document.getElementById("burger");
const links = document.getElementById("nav-links");
burger.addEventListener("click", () => links.classList.toggle("open"));
links.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => links.classList.remove("open")));

// ---------- Zähler-Animation (Stats) ----------
function animateCount(el) {
  const target = parseInt(el.dataset.count, 10);
  if (!target) { el.textContent = target; return; }
  const dur = 1100;
  const start = performance.now();
  function frame(now) {
    const t = Math.min(1, (now - start) / dur);
    const eased = 1 - Math.pow(1 - t, 3);
    el.textContent = Math.round(target * eased);
    if (t < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}
const statObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll("[data-count]").forEach(animateCount);
      statObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.4 });
const stats = document.querySelector(".stats");
if (stats) statObserver.observe(stats);

// ---------- Terminal: Tipp-Animation ----------
const termOut = document.getElementById("term-out");
if (termOut) {
  const SCRIPT = [
    { text: "C:\\Users\\Gast> ", cls: "green", type: "instant" },
    { text: "neofetch", cls: "green", type: "typed" },
    { text: "\n", type: "instant" },
    { text: "        ◈◈◈          FusionOS „Hybrid“\n", cls: "green", type: "instant" },
    { text: "      ◈◈◈◈◈◈        -------------------------\n", cls: "green", type: "instant" },
    { text: "    ◈◈◈     ◈◈◈      OS:      FusionOS 2.1 (Windows × macOS)\n", cls: "green", type: "instant" },
    { text: "    ◈◈◈     ◈◈◈      Kernel:  Fusion 6.1-py\n", cls: "green", type: "instant" },
    { text: "      ◈◈◈◈◈◈        Shell:   fsh 1.0\n", cls: "green", type: "instant" },
    { text: "        ◈◈◈          DE:      FusionShell (Fluent)\n", cls: "green", type: "instant" },
    { text: "                       Auflösung: 1920x1080\n", type: "instant" },
    { text: "                       Theme:   Dunkel\n", type: "instant" },
    { text: "\nC:\\Users\\Gast> ", cls: "green", type: "instant" },
    { text: "open rechner", type: "typed" },
    { text: "\nStarte Rechner…", type: "instant" },
    { text: "\n\nC:\\Users\\Gast> ", cls: "green", type: "instant" },
  ];

  let started = false;
  const termObserver = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && !started) {
      started = true;
      play();
      termObserver.disconnect();
    }
  }, { threshold: 0.35 });
  termObserver.observe(termOut);

  function span(text, cls) {
    const s = document.createElement("span");
    s.textContent = text;
    if (cls) s.className = cls;
    termOut.appendChild(s);
    return s;
  }

  function play() {
    let i = 0;
    function next() {
      if (i >= SCRIPT.length) {
        const cur = span("▊", "cursor");
        setInterval(() => { cur.style.opacity = cur.style.opacity === "0" ? "1" : "0"; }, 600);
        return;
      }
      const step = SCRIPT[i++];
      if (step.type === "typed") {
        const s = span("", step.cls);
        let c = 0;
        const iv = setInterval(() => {
          s.textContent = step.text.slice(0, ++c);
          if (c >= step.text.length) { clearInterval(iv); setTimeout(next, 350); }
        }, 70);
      } else {
        span(step.text, step.cls);
        setTimeout(next, 60);
      }
    }
    next();
  }
}
