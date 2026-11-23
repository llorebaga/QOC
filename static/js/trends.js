/* QOC — interactive topic trends over the arXiv archive (2000–present). Zero dependencies. */
(function () {
  "use strict";

  const root = document.querySelector("[data-trends]");
  const dataEl = document.getElementById("trends-data");
  if (!root || !dataEl) return;

  const data = JSON.parse(dataEl.textContent);
  const byId = new Map(data.topics.map((t) => [t.id, t]));
  const svg = root.querySelector("[data-trends-svg]");
  const wrap = root.querySelector("[data-trends-wrap]");
  const tip = root.querySelector("[data-trends-tip]");
  const activeList = root.querySelector("[data-trends-active]");
  const addSel = root.querySelector("[data-trend-add]");
  const includePartial = root.querySelector("[data-include-partial]");
  const modeBtns = [...root.querySelectorAll("[data-mode]")];
  const tbody = root.querySelector("[data-trends-tbody]");

  const PALETTE = ["#5b3df5", "#0e9aa7", "#e11d74", "#d97706", "#15803d", "#2563eb"];
  const NS = "http://www.w3.org/2000/svg";
  const el = (tag, attrs, text) => {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs) n.setAttribute(k, attrs[k]);
    if (text !== undefined) n.textContent = text;
    return n;
  };
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const PRESETS = {
    platforms: ["superconducting", "trapped-ions", "neutral-atoms", "spins", "photonics"],
    methods: ["grape", "crab", "machine-learning-control", "variational-algorithms", "autodiff-control"],
    tasks: ["gate-synthesis", "state-preparation", "error-correction", "quantum-sensing", "quantum-thermodynamics"],
    rising: [...data.topics]
      .filter((t) => t.recent >= 40)
      .sort((a, b) => (b.growth ?? -1) - (a.growth ?? -1))
      .slice(0, 5)
      .map((t) => t.id),
  };

  let selected = PRESETS.platforms.filter((id) => byId.has(id));
  let mode = "count"; // "count" | "share"
  let sortKey = "recent";
  let sortDir = -1;

  function visibleYears() {
    const n = includePartial.checked ? data.years.length : Math.max(1, data.years.length - 1);
    return {
      n,
      years: data.years.slice(0, n),
      totals: data.totals.slice(0, n),
    };
  }

  function seriesValue(topic, idx, totals) {
    const c = topic.counts[idx] || 0;
    if (mode === "count") return c;
    const tot = totals[idx] || 1;
    return (100 * c) / tot;
  }

  function renderPills() {
    activeList.innerHTML = selected.map((id, i) => {
      const t = byId.get(id);
      const col = PALETTE[i % PALETTE.length];
      return `<li><span class="trend-pill" style="--tc:${col}">` +
        `<span class="trend-swatch"></span><a href="${esc(t.url)}">${esc(t.label)}</a>` +
        `<button type="button" data-remove="${esc(id)}" aria-label="Remove ${esc(t.label)}">×</button></span></li>`;
    }).join("");
  }

  function renderChart() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    const { n, years, totals } = visibleYears();
    const x0 = 52, x1 = 820, y0 = 18, y1 = 296;
    const series = selected.map((id, i) => {
      const t = byId.get(id);
      return {
        topic: t,
        color: PALETTE[i % PALETTE.length],
        vals: years.map((_, k) => seriesValue(t, k, totals)),
      };
    });

    let yMax = 1;
    for (const s of series) for (const v of s.vals) if (v > yMax) yMax = v;
    // Nice ceiling
    const step = mode === "share"
      ? (yMax <= 10 ? 2 : yMax <= 25 ? 5 : 10)
      : (yMax <= 20 ? 5 : yMax <= 60 ? 10 : yMax <= 150 ? 25 : yMax <= 300 ? 50 : 100);
    yMax = Math.ceil((yMax * 1.08) / step) * step;

    const sx = (k) => x0 + (n > 1 ? (k / (n - 1)) * (x1 - x0) : 0);
    const sy = (v) => y1 - (v / yMax) * (y1 - y0);

    // Y grid & labels
    for (let v = 0; v <= yMax + 1e-6; v += step) {
      const y = sy(v);
      svg.appendChild(el("line", { class: "d-grid", x1: x0, x2: x1, y1: y, y2: y }));
      const lbl = mode === "share" ? `${v.toFixed(0)}%` : String(Math.round(v));
      svg.appendChild(el("text", { class: "d-tick", x: x0 - 8, y: y + 4, "text-anchor": "end" }, lbl));
    }
    // X ticks (every 2 or 5 years)
    const xStep = years.length > 18 ? 4 : 2;
    years.forEach((yr, k) => {
      if (k === 0 || k === n - 1 || yr % xStep === 0) {
        const x = sx(k);
        svg.appendChild(el("line", { class: "d-grid", x1: x, x2: x, y1: y0, y2: y1 }));
        svg.appendChild(el("text", { class: "d-tick", x, y: y1 + 18, "text-anchor": "middle" }, String(yr)));
      }
    });
    svg.appendChild(el("line", { class: "d-axis", x1: x0, x2: x1, y1: y1, y2: y1 }));
    svg.appendChild(el("line", { class: "d-axis", x1: x0, x2: x0, y1: y0, y2: y1 }));

    // Curves
    for (const s of series) {
      const d = s.vals.map((v, k) => (k ? "L" : "M") + sx(k).toFixed(1) + " " + sy(v).toFixed(1)).join("");
      svg.appendChild(el("path", { class: "trend-line", d, stroke: s.color }));
    }

    // Hover cursor & invisible hit columns
    const cursor = el("line", { class: "trend-cursor", x1: x0, x2: x0, y1: y0, y2: y1, visibility: "hidden" });
    svg.appendChild(cursor);
    const dots = series.map((s) => {
      const c = el("circle", { r: 4, fill: s.color, stroke: "var(--bg-elev)", "stroke-width": 1.8, visibility: "hidden" });
      svg.appendChild(c);
      return c;
    });

    const colW = n > 1 ? (x1 - x0) / (n - 1) : x1 - x0;
    years.forEach((yr, k) => {
      const x = sx(k);
      const hit = el("rect", {
        x: Math.max(x0, x - colW / 2), y: y0,
        width: colW, height: y1 - y0,
        fill: "transparent", tabindex: "0",
        "aria-label": `${yr}`,
      });
      const show = () => {
        cursor.setAttribute("x1", x);
        cursor.setAttribute("x2", x);
        cursor.setAttribute("visibility", "visible");
        const rows = series
          .map((s, idx) => {
            dots[idx].setAttribute("cx", x);
            dots[idx].setAttribute("cy", sy(s.vals[k]));
            dots[idx].setAttribute("visibility", "visible");
            return { s, v: s.vals[k], raw: s.topic.counts[k] || 0 };
          })
          .sort((a, b) => b.v - a.v);

        const isPartial = yr === data.partial_year;
        const lines = rows.map(({ s, v, raw }) => {
          const valStr = mode === "share" ? `${v.toFixed(1)}% (${raw})` : `${raw}`;
          return `<span class="tt-row"><span class="tt-dot" style="background:${s.color}"></span>${esc(s.topic.label)}: <b>${valStr}</b></span>`;
        }).join("");
        tip.innerHTML = `<strong>${yr}${isPartial ? " (YTD)" : ""} · ${totals[k]} total</strong>${lines}`;
        tip.hidden = false;

        const sr = svg.getBoundingClientRect();
        const wr = wrap.getBoundingClientRect();
        const px = sr.left - wr.left + (x / 840) * sr.width;
        let tx = px + 14;
        if (tx + tip.offsetWidth > wr.width - 8) tx = Math.max(8, px - tip.offsetWidth - 14);
        tip.style.transform = `translate(${tx.toFixed(0)}px, 12px)`;
      };
      const hide = () => {
        cursor.setAttribute("visibility", "hidden");
        dots.forEach((c) => c.setAttribute("visibility", "hidden"));
        tip.hidden = true;
      };
      hit.addEventListener("mouseenter", show);
      hit.addEventListener("focus", show);
      hit.addEventListener("mouseleave", hide);
      hit.addEventListener("blur", hide);
      svg.appendChild(hit);
    });
  }

  function sparkSVG(counts, fam) {
    const vals = counts.slice(0, Math.max(1, counts.length - 1)); // complete years
    const max = Math.max(1, ...vals);
    const w = 96, h = 24;
    const pts = vals.map((v, i) => {
      const x = vals.length > 1 ? (i / (vals.length - 1)) * w : w;
      const y = h - 2 - (v / max) * (h - 4);
      return `${i ? "L" : "M"}${x.toFixed(1)} ${y.toFixed(1)}`;
    }).join("");
    return `<svg class="spark" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" aria-hidden="true">` +
      `<path d="${pts}" fill="none" stroke="var(--fam-${esc(fam)})" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  }

  function renderTable() {
    const rows = [...data.topics].sort((a, b) => {
      if (sortKey === "title") return sortDir * a.title.localeCompare(b.title);
      const av = a[sortKey] ?? -Infinity;
      const bv = b[sortKey] ?? -Infinity;
      return sortDir * (av - bv) || a.title.localeCompare(b.title);
    });
    tbody.innerHTML = rows.map((t) => {
      const gStr = t.growth === null
        ? "—"
        : `${t.growth >= 0 ? "+" : ""}${Math.round(t.growth * 100)}%`;
      const gCls = t.growth === null ? "muted" : t.growth >= 0.5 ? "growth-up" : t.growth < 0 ? "growth-down" : "";
      const active = selected.includes(t.id);
      return `<tr>` +
        `<td><a class="trends-tlink" href="${esc(t.url)}">${esc(t.title)}</a></td>` +
        `<td><span class="fam-dot" style="--fam:var(--fam-${esc(t.family)})"></span> ${esc(t.family_title)}</td>` +
        `<td class="num"><a href="${esc(t.papers_url)}">${t.total.toLocaleString("en-US")}</a></td>` +
        `<td class="num">${t.recent.toLocaleString("en-US")}</td>` +
        `<td class="num ${gCls}">${gStr}</td>` +
        `<td>${sparkSVG(t.counts, t.family)}</td>` +
        `<td class="num"><button type="button" class="trend-toggle" data-toggle="${esc(t.id)}" aria-pressed="${active}">${active ? "Plotted" : "Plot"}</button></td>` +
        `</tr>`;
    }).join("");
  }

  function refresh() {
    renderPills();
    renderChart();
    renderTable();
  }

  modeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      mode = btn.dataset.mode;
      modeBtns.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      renderChart();
    });
  });

  includePartial.addEventListener("change", renderChart);

  root.querySelectorAll("[data-trend-preset]").forEach((btn) => {
    btn.addEventListener("click", () => {
      selected = (PRESETS[btn.dataset.trendPreset] || []).filter((id) => byId.has(id));
      refresh();
    });
  });

  addSel.addEventListener("change", () => {
    const id = addSel.value;
    addSel.value = "";
    if (!id || selected.includes(id)) return;
    if (selected.length >= 6) selected = selected.slice(1);
    selected.push(id);
    refresh();
  });

  activeList.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-remove]");
    if (!btn || selected.length <= 1) return;
    selected = selected.filter((id) => id !== btn.dataset.remove);
    refresh();
  });

  tbody.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-toggle]");
    if (!btn) return;
    const id = btn.dataset.toggle;
    if (selected.includes(id)) {
      if (selected.length > 1) selected = selected.filter((x) => x !== id);
    } else {
      if (selected.length >= 6) selected = selected.slice(1);
      selected.push(id);
    }
    refresh();
  });

  root.querySelectorAll("[data-sort]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const k = btn.dataset.sort;
      if (sortKey === k) sortDir = -sortDir;
      else { sortKey = k; sortDir = k === "title" ? 1 : -1; }
      renderTable();
    });
  });

  refresh();
})();
