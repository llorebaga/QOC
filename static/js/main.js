/* QOC — site-wide behaviour. No dependencies. */
(function () {
  "use strict";

  const root = document.documentElement;
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)");

  /* ------------------------------------------------------------ theme */
  function currentTheme() {
    return root.dataset.theme || (prefersDark.matches ? "dark" : "light");
  }

  function setTheme(theme) {
    root.dataset.theme = theme;
    try { localStorage.setItem("qoc-theme", theme); } catch (e) { /* storage unavailable */ }
    document.dispatchEvent(new CustomEvent("qoc:theme", { detail: theme }));
  }

  document.querySelectorAll(".theme-toggle").forEach((btn) => {
    btn.addEventListener("click", () => setTheme(currentTheme() === "dark" ? "light" : "dark"));
  });

  /* ------------------------------------------------------------ mobile nav */
  const navToggle = document.querySelector(".nav-toggle");
  if (navToggle) {
    const close = () => {
      document.body.classList.remove("nav-open");
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.setAttribute("aria-label", "Open menu");
    };
    navToggle.addEventListener("click", () => {
      const open = document.body.classList.toggle("nav-open");
      navToggle.setAttribute("aria-expanded", String(open));
      navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });
    window.addEventListener("resize", () => { if (window.innerWidth > 960) close(); });
  }

  /* ------------------------------------------------------------ hero waves
     A few faint wave packets drifting across the hero, echoing the logo. */
  const canvas = document.querySelector(".hero-waves");
  if (canvas && canvas.getContext) {
    const ctx = canvas.getContext("2d");
    const packets = [
      { y: 0.22, amp: 18, sigma: 0.20, k: 0.034, speed: 0.012, phase: 0.0, x0: 0.15 },
      { y: 0.42, amp: 26, sigma: 0.26, k: 0.026, speed: -0.009, phase: 1.3, x0: 0.80 },
      { y: 0.63, amp: 20, sigma: 0.22, k: 0.030, speed: 0.010, phase: 2.1, x0: 0.45 },
      { y: 0.84, amp: 14, sigma: 0.18, k: 0.040, speed: -0.013, phase: 0.7, x0: 0.25 },
    ];
    let w = 0, h = 0, raf = 0, visible = true, t0 = performance.now();

    const resize = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.clientWidth; h = canvas.clientHeight;
      canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    const draw = (time) => {
      const t = (time - t0) / 1000;
      ctx.clearRect(0, 0, w, h);
      const grad = ctx.createLinearGradient(0, 0, w, 0);
      grad.addColorStop(0, "rgba(34,211,238,0)");
      grad.addColorStop(0.2, "rgba(34,211,238,1)");
      grad.addColorStop(0.5, "rgba(124,92,255,1)");
      grad.addColorStop(0.8, "rgba(240,70,155,1)");
      grad.addColorStop(1, "rgba(240,70,155,0)");
      ctx.strokeStyle = grad;
      ctx.lineWidth = 1.4;
      for (const p of packets) {
        // centre wraps around the canvas width (with margin)
        const span = 1.6;
        const cx = ((((p.x0 + p.speed * t) % span) + span) % span - 0.3) * w;
        const cy = p.y * h;
        const sigma = p.sigma * w;
        ctx.beginPath();
        for (let x = 0; x <= w; x += 3) {
          const env = Math.exp(-(((x - cx) / sigma) ** 2));
          const y = cy - p.amp * env * Math.cos(p.k * (x - cx) + p.phase + t * 0.6);
          x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
      if (!reducedMotion && visible) raf = requestAnimationFrame(draw);
    };

    resize();
    window.addEventListener("resize", () => { resize(); if (reducedMotion) draw(t0); });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(([entry]) => {
        visible = entry.isIntersecting;
        cancelAnimationFrame(raf);
        if (visible && !reducedMotion) raf = requestAnimationFrame(draw);
      }).observe(canvas);
    }
    raf = requestAnimationFrame(draw);
  }

  /* ------------------------------------------------------------ papers-per-year chart tooltip */
  document.querySelectorAll("[data-chart]").forEach((fig) => {
    const svg = fig.querySelector("svg");
    const tip = fig.querySelector(".chart-tip");
    const wrap = fig.querySelector(".chart-wrap");
    const fmt = (n) => Number(n).toLocaleString("en-US");
    const show = (bar) => {
      const d = bar.dataset;
      svg.classList.add("has-hover");
      svg.querySelectorAll(".bar").forEach((b) => b.classList.toggle("is-hover", b === bar));
      let html = `<strong>${fmt(d.count)} papers</strong>${d.year}`;
      if (d.partial === "true") {
        html = `<strong>${fmt(d.count)} papers so far</strong>${d.year}, to date`;
        if (d.prevYtd) html += `<br>Same period of ${d.prevYear}: ${fmt(d.prevYtd)}`;
      }
      tip.innerHTML = html;
      tip.hidden = false;
      const br = (bar.querySelector("path") || bar.querySelector(".hit")).getBoundingClientRect();
      const wr = wrap.getBoundingClientRect();
      let x = br.left - wr.left + br.width / 2 - tip.offsetWidth / 2;
      x = Math.max(0, Math.min(wr.width - tip.offsetWidth, x));
      const y = Math.max(0, br.top - wr.top - tip.offsetHeight - 28);   // clear of the value label on the cap
      tip.style.transform = `translate(${x}px, ${y}px)`;
    };
    const hide = () => {
      tip.hidden = true;
      svg.classList.remove("has-hover");
      svg.querySelectorAll(".bar").forEach((b) => b.classList.remove("is-hover"));
    };
    fig.querySelectorAll("[data-chart-bar]").forEach((bar) => {
      bar.addEventListener("mouseenter", () => show(bar));
      bar.addEventListener("focus", () => show(bar));
      bar.addEventListener("mouseleave", hide);
      bar.addEventListener("blur", hide);
    });
  });

  /* ------------------------------------------------------------ piecewise-constant pulse plot */
  const SVG_NS = "http://www.w3.org/2000/svg";
  const el = (name, attrs, text) => {
    const node = document.createElementNS(SVG_NS, name);
    for (const k in attrs) node.setAttribute(k, attrs[k]);
    if (text) node.textContent = text;
    return node;
  };

  document.querySelectorAll("svg[data-pwc]").forEach((svg) => {
    const x0 = 34, x1 = 396, yMid = 98, amp = 76, n = 24;
    // smooth target shape: a sine envelope times a slow carrier
    const u = (s) => Math.sin(Math.PI * s) ** 1.5 * Math.cos(2.5 * Math.PI * (s - 0.45));
    const sx = (s) => x0 + s * (x1 - x0);
    const sy = (v) => yMid - amp * v;

    for (let i = 0; i < n; i++) {
      const s = (i + 0.5) / n;
      const v = u(s);
      const y = sy(v);
      svg.appendChild(el("rect", {
        class: "bar",
        x: sx(i / n).toFixed(2), width: ((x1 - x0) / n).toFixed(2),
        y: Math.min(y, yMid).toFixed(2), height: Math.abs(y - yMid).toFixed(2),
      }));
    }
    let d = "";
    for (let j = 0; j <= 200; j++) {
      const s = j / 200;
      d += (j ? "L" : "M") + sx(s).toFixed(2) + " " + sy(u(s)).toFixed(2);
    }
    svg.appendChild(el("path", { class: "env", d }));
    svg.appendChild(el("line", { class: "axis", x1: x0, x2: x1 + 8, y1: yMid, y2: yMid }));
    svg.appendChild(el("line", { class: "axis", x1: x0, x2: x0, y1: 10, y2: 140 }));
    svg.appendChild(el("text", { x: x0 - 6, y: 22, "text-anchor": "end" }, "u"));
    svg.appendChild(el("text", { x: x0 - 6, y: yMid + 4, "text-anchor": "end" }, "0"));
    svg.appendChild(el("text", { x: x1 + 12, y: yMid + 4 }, "t"));
    svg.appendChild(el("text", { x: x1, y: yMid + 20, "text-anchor": "middle" }, "T"));
  });
})();
