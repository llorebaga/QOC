/* QOC — interactive physics explorers (DRAG, dynamical decoupling filter functions, counterdiabatic STA).
   Pure vanilla JS + SVG; no dependencies. */
(function () {
  "use strict";

  const NS = "http://www.w3.org/2000/svg";
  const el = (tag, attrs, text) => {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs) n.setAttribute(k, attrs[k]);
    if (text !== undefined) n.textContent = text;
    return n;
  };
  const pathFrom = (pts) => pts.map((p, i) => (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1)).join("");
  const fmtExp = (x) => (x < 1e-6 ? "< 10⁻⁶" : x < 1e-2 ? x.toExponential(2) : x.toFixed(4));
  const fmtPct = (x) => (x * 100).toFixed(2) + "%";

  function clearSvg(svg) {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
  }

  function drawFrame(svg, { x0 = 42, x1 = 366, y0 = 14, y1 = 158, xTicks = [], yTicks = [], xLabel = "", yLabel = "" }) {
    for (const t of yTicks) {
      svg.appendChild(el("line", { class: "d-grid", x1: x0, x2: x1, y1: t.y, y2: t.y }));
      svg.appendChild(el("text", { class: "d-tick", x: x0 - 6, y: t.y + 3.5, "text-anchor": "end" }, t.label));
    }
    for (const t of xTicks) {
      svg.appendChild(el("line", { class: "d-grid", x1: t.x, x2: t.x, y1: y0, y2: y1 }));
      svg.appendChild(el("text", { class: "d-tick", x: t.x, y: y1 + 14, "text-anchor": "middle" }, t.label));
    }
    svg.appendChild(el("line", { class: "d-axis", x1: x0, x2: x1, y1: y1, y2: y1 }));
    svg.appendChild(el("line", { class: "d-axis", x1: x0, x2: x0, y1: y0, y2: y1 }));
    if (xLabel) svg.appendChild(el("text", { class: "d-label", x: (x0 + x1) / 2, y: 185, "text-anchor": "middle" }, xLabel));
    if (yLabel) svg.appendChild(el("text", { class: "d-label", x: 12, y: (y0 + y1) / 2, "text-anchor": "middle", transform: `rotate(-90 12 ${(y0 + y1) / 2})` }, yLabel));
    return { x0, x1, y0, y1 };
  }

  function drawLegend(svg, items, x = 50, y = 20) {
    let cx = x;
    for (const it of items) {
      svg.appendChild(el("line", { class: it.cls, x1: cx, x2: cx + 14, y1: y - 3, y2: y - 3 }));
      svg.appendChild(el("text", { class: "d-legend", x: cx + 18, y: y }, it.label));
      cx += 24 + it.label.length * 6.2;
    }
  }

  function bindPresets(card, update) {
    card.querySelectorAll("[data-preset]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const vals = JSON.parse(btn.dataset.preset);
        for (const [k, v] of Object.entries(vals)) {
          const inp = card.querySelector(`[name="${k}"]`);
          if (inp) inp.value = String(v);
        }
        update();
      });
    });
  }

  /* ================================================================ 1. DRAG */
  function initDrag(card) {
    const svgWave = card.querySelector('[data-svg="wave"]');
    const svgPop = card.querySelector('[data-svg="pop"]');
    const get = (n) => Number(card.querySelector(`[name="${n}"]`).value);
    const out = (n, v) => { const o = card.querySelector(`[data-out="${n}"]`); if (o) o.textContent = v; };
    const stat = (n, v) => { const s = card.querySelector(`[data-stat="${n}"]`); if (s) s.textContent = v; };

    function update() {
      const beta = get("beta");
      const tg = get("tg");
      const deltaMHz = get("delta");
      out("beta", beta.toFixed(2));
      out("tg", `${tg.toFixed(1)} ns`);
      out("delta", `${deltaMHz} MHz`);

      const Delta = (2 * Math.PI * deltaMHz) / 1000; // rad/ns
      const sigma = tg / 4;
      const g0 = Math.exp(-(tg * tg) / (8 * sigma * sigma));
      const steps = 220;
      const dt = tg / steps;

      let rawInt = 0;
      for (let k = 0; k < steps; k++) {
        const u = (k + 0.5) * dt - tg / 2;
        rawInt += (Math.exp(-(u * u) / (2 * sigma * sigma)) - g0) * dt;
      }
      const A = Math.PI / rawInt;

      function fields(t) {
        const u = t - tg / 2;
        const g = Math.exp(-(u * u) / (2 * sigma * sigma));
        const ox = A * (g - g0);
        const dox = A * (-u / (sigma * sigma)) * g;
        const oy = (-beta * dox) / Delta;
        return [ox, oy];
      }

      const s2 = Math.SQRT2;
      // state psi = [r0,i0, r1,i1, r2,i2]
      function deriv(t, y) {
        const [ox, oy] = fields(t);
        const cr = 0.5 * ox, ci = -0.5 * oy; // c = 0.5*(ox - i*oy)
        // H*psi
        const h0r = cr * y[2] - ci * y[3];
        const h0i = cr * y[3] + ci * y[2];
        const h1r = (cr * y[0] + ci * y[1]) + s2 * (cr * y[4] - ci * y[5]);
        const h1i = (cr * y[1] - ci * y[0]) + s2 * (cr * y[5] + ci * y[4]);
        const h2r = s2 * (cr * y[2] + ci * y[3]) + Delta * y[4];
        const h2i = s2 * (cr * y[3] - ci * y[2]) + Delta * y[5];
        // -i * H*psi => (h_i, -h_r)
        return [h0i, -h0r, h1i, -h1r, h2i, -h2r];
      }

      let psi = [1, 0, 0, 0, 0, 0];
      const ts = [], oxs = [], oys = [], p0s = [], p1s = [], p2s = [];
      let p2max = 0;
      for (let k = 0; k <= steps; k++) {
        const t = k * dt;
        const [ox, oy] = fields(t);
        const p0 = psi[0] * psi[0] + psi[1] * psi[1];
        const p1 = psi[2] * psi[2] + psi[3] * psi[3];
        const p2 = psi[4] * psi[4] + psi[5] * psi[5];
        if (p2 > p2max) p2max = p2;
        ts.push(t);
        oxs.push((ox * 1000) / (2 * Math.PI));
        oys.push((oy * 1000) / (2 * Math.PI));
        p0s.push(p0); p1s.push(p1); p2s.push(p2);
        if (k < steps) {
          const k1 = deriv(t, psi);
          const y2 = psi.map((v, i) => v + 0.5 * dt * k1[i]);
          const k2 = deriv(t + 0.5 * dt, y2);
          const y3 = psi.map((v, i) => v + 0.5 * dt * k2[i]);
          const k3 = deriv(t + 0.5 * dt, y3);
          const y4 = psi.map((v, i) => v + dt * k3[i]);
          const k4 = deriv(t + dt, y4);
          psi = psi.map((v, i) => v + (dt / 6) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]));
        }
      }

      const finalP1 = p1s[steps];
      const finalP2 = p2s[steps];
      stat("p1", fmtPct(finalP1));
      stat("p2", fmtExp(finalP2));
      stat("p2max", fmtExp(p2max));
      stat("err", fmtExp(Math.max(0, 1 - finalP1)));

      // Plot 1: waveforms
      clearSvg(svgWave);
      const maxAmp = Math.max(10, ...oxs.map(Math.abs), ...oys.map(Math.abs)) * 1.12;
      const sx = (t) => 44 + (t / tg) * 320;
      const syW = (v) => 86 - (v / maxAmp) * 66;
      drawFrame(svgWave, {
        x0: 44, x1: 364, y0: 14, y1: 158,
        xTicks: [0, 0.5, 1].map((u) => ({ x: sx(u * tg), label: (u * tg).toFixed(0) })),
        yTicks: [-1, 0, 1].map((u) => ({ y: syW(u * maxAmp * 0.8), label: `${Math.round(u * maxAmp * 0.8)}` })),
        xLabel: "time t (ns)", yLabel: "MHz",
      });
      svgWave.appendChild(el("path", { class: "d-line d-c1", d: pathFrom(ts.map((t, i) => [sx(t), syW(oxs[i])])) }));
      svgWave.appendChild(el("path", { class: "d-line d-c2", d: pathFrom(ts.map((t, i) => [sx(t), syW(oys[i])])) }));
      drawLegend(svgWave, [{ cls: "d-line d-c1", label: "Ωx (I)" }, { cls: "d-line d-c2", label: "Ωy (Q)" }], 54, 24);

      // Plot 2: populations
      clearSvg(svgPop);
      const syP = (v) => 158 - Math.min(1.04, Math.max(0, v)) * 140;
      drawFrame(svgPop, {
        x0: 44, x1: 364, y0: 14, y1: 158,
        xTicks: [0, 0.5, 1].map((u) => ({ x: sx(u * tg), label: (u * tg).toFixed(0) })),
        yTicks: [0, 0.5, 1].map((v) => ({ y: syP(v), label: v.toFixed(1) })),
        xLabel: "time t (ns)", yLabel: "pop.",
      });
      svgPop.appendChild(el("path", { class: "d-line d-c3", d: pathFrom(ts.map((t, i) => [sx(t), syP(p0s[i])])) }));
      svgPop.appendChild(el("path", { class: "d-line d-c1", d: pathFrom(ts.map((t, i) => [sx(t), syP(p1s[i])])) }));
      svgPop.appendChild(el("path", { class: "d-line d-c2 d-dash", d: pathFrom(ts.map((t, i) => [sx(t), syP(Math.min(1, 10 * p2s[i]))])) }));
      drawLegend(svgPop, [
        { cls: "d-line d-c3", label: "P0" },
        { cls: "d-line d-c1", label: "P1" },
        { cls: "d-line d-c2 d-dash", label: "10×P2" },
      ], 54, 24);
    }

    card.addEventListener("input", update);
    card.addEventListener("change", update);
    bindPresets(card, update);
    update();
  }

  /* ================================================================ 2. Filter Functions & DD */
  function initFilterFunction(card) {
    const svgSpec = card.querySelector('[data-svg="spec"]');
    const svgCoh = card.querySelector('[data-svg="coh"]');
    const seqSel = card.querySelector('[name="seq"]');
    const nInp = card.querySelector('[name="n"]');
    const wcInp = card.querySelector('[name="wc"]');
    const noiseSel = card.querySelector('[name="noise"]');
    const out = (n, v) => { const o = card.querySelector(`[data-out="${n}"]`); if (o) o.textContent = v; };
    const stat = (n, v) => { const s = card.querySelector(`[data-stat="${n}"]`); if (s) s.textContent = v; };

    function pulseTimes(seq, n) {
      if (seq === "fid" || n <= 0) return [];
      const deltas = [];
      for (let k = 1; k <= n; k++) {
        if (seq === "cpmg") deltas.push((k - 0.5) / n);
        else deltas.push(Math.sin((Math.PI * k) / (2 * n + 2)) ** 2);
      }
      return deltas;
    }

    // Exact filter function F(z) where z = omega * T
    function filterVal(z, deltas) {
      const n = deltas.length;
      if (z < 1e-6) return 0;
      const sgnEnd = n % 2 === 0 ? -1 : 1; // (-1)^(n+1)
      let re = 1 + sgnEnd * Math.cos(z);
      let im = sgnEnd * Math.sin(z);
      for (let k = 0; k < n; k++) {
        const s = k % 2 === 0 ? -2 : 2; // 2*(-1)^(k+1)
        const ang = z * deltas[k];
        re += s * Math.cos(ang);
        im += s * Math.sin(ang);
      }
      return re * re + im * im;
    }

    // Normalized noise PSD S(w) with dimensionless frequency w = omega * T0 (T0 = 1)
    function psd(w, wc, kind) {
      if (kind === "lorentz") return (2 * wc) / (w * w + wc * wc);
      // 1/f with IR floor and sharp UV cutoff at wc (highlights UDD advantage!)
      if (w > wc) return 0;
      return 1.2 / (w + 0.15 * wc);
    }

    function chiAt(tau, deltas, wc, noiseKind) {
      // integrate over log-spaced grid from wMin to wMax
      const wMin = 0.02, wMax = 80, M = 320;
      const lr0 = Math.log(wMin), lr1 = Math.log(wMax), dl = (lr1 - lr0) / M;
      let sum = 0;
      for (let i = 0; i < M; i++) {
        const w = Math.exp(lr0 + (i + 0.5) * dl);
        const dw = w * dl;
        const F = filterVal(w * tau, deltas);
        sum += (psd(w, wc, noiseKind) * F) / (w * w) * dw;
      }
      return sum / Math.PI;
    }

    function update() {
      const seq = seqSel.value;
      const n = seq === "fid" ? 0 : Number(nInp.value);
      const wc = Number(wcInp.value);
      const noiseKind = noiseSel.value;
      nInp.disabled = seq === "fid";
      out("n", String(n));
      out("wc", wc.toFixed(1));

      const deltas = pulseTimes(seq, n);
      // Calibrate noise scale so FID at T=1 has W_FID(1) ~ 0.12 (clear visual contrast)
      const rawFid = chiAt(1.0, [], wc, noiseKind);
      const scale = rawFid > 0 ? 2.1 / rawFid : 1;

      const chi = scale * chiAt(1.0, deltas, wc, noiseKind);
      const chiFid = scale * rawFid;
      const W = Math.exp(-chi);
      const WFid = Math.exp(-chiFid);

      stat("w", fmtPct(W));
      stat("wfid", fmtPct(WFid));
      stat("chi", chi < 1e-3 ? chi.toExponential(2) : chi.toFixed(3));
      const gain = chi > 1e-9 ? chiFid / chi : Infinity;
      stat("gain", gain > 1e4 ? "> 10⁴×" : `${gain.toFixed(1)}×`);

      // Plot 1: Spectrum & filter F(w)/(w^2) vs log10(w) in [0.1, 60]
      clearSvg(svgSpec);
      const l0 = Math.log10(0.1), l1 = Math.log10(60);
      const sx = (w) => 44 + ((Math.log10(w) - l0) / (l1 - l0)) * 320;
      const sy = (v) => 158 - Math.min(1.02, Math.max(0, v)) * 136;
      drawFrame(svgSpec, {
        x0: 44, x1: 364, y0: 14, y1: 158,
        xTicks: [0.1, 1, 10, 50].map((w) => ({ x: sx(w), label: String(w) })),
        yTicks: [0, 0.5, 1].map((v) => ({ y: sy(v), label: v.toFixed(1) })),
        xLabel: "dimensionless frequency ωT (log)", yLabel: "norm.",
      });
      const M = 220;
      const sPts = [], fPts = [];
      let sMax = 0, fMax = 0;
      const ws = [], ss = [], fs = [];
      for (let i = 0; i <= M; i++) {
        const w = Math.pow(10, l0 + (i / M) * (l1 - l0));
        const sv = psd(w, wc, noiseKind);
        const fv = filterVal(w, deltas) / (w * w);
        ws.push(w); ss.push(sv); fs.push(fv);
        if (sv > sMax) sMax = sv;
        if (fv > fMax) fMax = fv;
      }
      if (sMax <= 0) sMax = 1;
      if (fMax <= 0) fMax = 1;
      for (let i = 0; i <= M; i++) {
        sPts.push([sx(ws[i]), sy(ss[i] / sMax)]);
        fPts.push([sx(ws[i]), sy(fs[i] / fMax)]);
      }
      // Shaded noise PSD
      const areaD = `M44 158 ` + sPts.map((p) => `L${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(" ") + ` L364 158 Z`;
      svgSpec.appendChild(el("path", { class: "d-fill-noise", d: areaD }));
      svgSpec.appendChild(el("path", { class: "d-line d-c2", d: pathFrom(sPts) }));
      svgSpec.appendChild(el("path", { class: "d-line d-c1", d: pathFrom(fPts) }));
      drawLegend(svgSpec, [{ cls: "d-line d-c1", label: "Filter F/(ωT)²" }, { cls: "d-line d-c2", label: "Noise S(ω)" }], 54, 24);

      // Plot 2: Pulse timing strip (top) + Coherence decay W(t) vs FID (bottom)
      clearSvg(svgCoh);
      const sxT = (u) => 44 + u * 320;
      const syC = (v) => 158 - v * 108;
      // Pulse timing strip y in [16, 36]
      svgCoh.appendChild(el("line", { class: "d-axis", x1: 44, x2: 364, y1: 30, y2: 30 }));
      svgCoh.appendChild(el("text", { class: "d-tick", x: 38, y: 33, "text-anchor": "end" }, "π"));
      for (const d of deltas) {
        const px = sxT(d);
        svgCoh.appendChild(el("line", { class: "d-pulse", x1: px, x2: px, y1: 16, y2: 34 }));
        svgCoh.appendChild(el("circle", { class: "d-dot", cx: px, cy: 16, r: 2.5 }));
      }
      drawFrame(svgCoh, {
        x0: 44, x1: 364, y0: 48, y1: 158,
        xTicks: [0, 0.5, 1].map((u) => ({ x: sxT(u), label: u === 0 ? "0" : u === 1 ? "T" : "T/2" })),
        yTicks: [0, 0.5, 1].map((v) => ({ y: syC(v), label: v.toFixed(1) })),
        xLabel: "total time t", yLabel: "W(t)",
      });
      const K = 28;
      const cPts = [], fCPts = [];
      for (let i = 0; i <= K; i++) {
        const u = i / K;
        const wSeq = u === 0 ? 1 : Math.exp(-scale * chiAt(u, deltas, wc, noiseKind));
        const wF = u === 0 ? 1 : Math.exp(-scale * chiAt(u, [], wc, noiseKind));
        cPts.push([sxT(u), syC(wSeq)]);
        fCPts.push([sxT(u), syC(wF)]);
      }
      svgCoh.appendChild(el("path", { class: "d-line d-c3 d-dash", d: pathFrom(fCPts) }));
      svgCoh.appendChild(el("path", { class: "d-line d-c1", d: pathFrom(cPts) }));
      drawLegend(svgCoh, [
        { cls: "d-line d-c1", label: seq === "fid" ? "FID" : `${seq.toUpperCase()}-${n}` },
        { cls: "d-line d-c3 d-dash", label: "FID" },
      ], 210, 60);
    }

    card.addEventListener("input", update);
    card.addEventListener("change", update);
    bindPresets(card, update);
    update();
  }

  /* ================================================================ 3. Counterdiabatic STA */
  function initSta(card) {
    const svgFields = card.querySelector('[data-svg="fields"]');
    const svgFid = card.querySelector('[data-svg="fid"]');
    const get = (n) => Number(card.querySelector(`[name="${n}"]`).value);
    const out = (n, v) => { const o = card.querySelector(`[data-out="${n}"]`); if (o) o.textContent = v; };
    const stat = (n, v) => { const s = card.querySelector(`[data-stat="${n}"]`); if (s) s.textContent = v; };

    function evolve(T, lam, D0) {
      const O0 = 1.0;
      const steps = 200;
      const dt = T / steps;
      function fields(t) {
        const u = t / T;
        const s = 3 * u * u - 2 * u * u * u;
        const ds = (6 * u - 6 * u * u) / T;
        const D = D0 * (1 - 2 * s);
        const dD = -2 * D0 * ds;
        const Ocd = -(O0 * dD) / (O0 * O0 + D * D);
        return [D, lam * Ocd, Ocd];
      }
      function ground(D) {
        const th = Math.atan2(O0, D);
        return [-Math.sin(th / 2), Math.cos(th / 2)];
      }
      function deriv(t, y) {
        const [D, Oy] = fields(t);
        // H = 0.5 * [[D, O0 - i*Oy], [O0 + i*Oy, -D]]; dpsi/dt = -i H psi
        const h0r = 0.5 * (D * y[0] + O0 * y[2] + Oy * y[3]);
        const h0i = 0.5 * (D * y[1] + O0 * y[3] - Oy * y[2]);
        const h1r = 0.5 * (O0 * y[0] - Oy * y[1] - D * y[2]);
        const h1i = 0.5 * (O0 * y[1] + Oy * y[0] - D * y[3]);
        return [h0i, -h0r, h1i, -h1r];
      }
      const g0 = ground(D0);
      let psi = [g0[0], 0, g0[1], 0];
      const ts = [], Ds = [], Oys = [], F = [];
      let peak = 0, cost = 0;
      for (let k = 0; k <= steps; k++) {
        const t = k * dt;
        const [D, Oy] = fields(t);
        const g = ground(D);
        const ovR = g[0] * psi[0] + g[1] * psi[2];
        const ovI = g[0] * psi[1] + g[1] * psi[3];
        ts.push(t / T);
        Ds.push(D);
        Oys.push(Oy);
        F.push(ovR * ovR + ovI * ovI);
        if (Math.abs(Oy) > peak) peak = Math.abs(Oy);
        if (k < steps) {
          cost += Math.abs(Oy) * dt;
          const k1 = deriv(t, psi);
          const y2 = psi.map((v, i) => v + 0.5 * dt * k1[i]);
          const k2 = deriv(t + 0.5 * dt, y2);
          const y3 = psi.map((v, i) => v + 0.5 * dt * k2[i]);
          const k3 = deriv(t + 0.5 * dt, y3);
          const y4 = psi.map((v, i) => v + dt * k3[i]);
          const k4 = deriv(t + dt, y4);
          psi = psi.map((v, i) => v + (dt / 6) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]));
        }
      }
      return { ts, Ds, Oys, F, peak, cost };
    }

    function update() {
      const T = get("T");
      const lam = get("lam");
      const D0 = get("D0");
      out("T", T.toFixed(1));
      out("lam", lam.toFixed(2));
      out("D0", D0.toFixed(1));

      const cd = evolve(T, lam, D0);
      const bare = evolve(T, 0, D0);

      stat("fcd", fmtPct(cd.F[cd.F.length - 1]));
      stat("fbare", fmtPct(bare.F[bare.F.length - 1]));
      stat("peak", cd.peak.toFixed(2));
      stat("cost", cd.cost.toFixed(2));

      // Plot 1: fields
      clearSvg(svgFields);
      const maxF = Math.max(D0, cd.peak, 2) * 1.12;
      const sx = (u) => 44 + u * 320;
      const syF = (v) => 86 - (v / maxF) * 66;
      drawFrame(svgFields, {
        x0: 44, x1: 364, y0: 14, y1: 158,
        xTicks: [0, 0.5, 1].map((u) => ({ x: sx(u), label: u === 0 ? "0" : u === 1 ? "T" : "T/2" })),
        yTicks: [-1, 0, 1].map((u) => ({ y: syF(u * maxF * 0.8), label: (u * maxF * 0.8).toFixed(0) })),
        xLabel: "normalized time t / T", yLabel: "Ω₀",
      });
      svgFields.appendChild(el("path", { class: "d-line d-c3", d: pathFrom(cd.ts.map((u, i) => [sx(u), syF(cd.Ds[i])])) }));
      svgFields.appendChild(el("path", { class: "d-line d-c2", d: pathFrom(cd.ts.map((u, i) => [sx(u), syF(cd.Oys[i])])) }));
      drawLegend(svgFields, [{ cls: "d-line d-c3", label: "Δ(t)" }, { cls: "d-line d-c2", label: "λ·ΩCD(t)" }], 54, 24);

      // Plot 2: fidelity
      clearSvg(svgFid);
      const syP = (v) => 158 - Math.min(1.03, Math.max(0, v)) * 138;
      drawFrame(svgFid, {
        x0: 44, x1: 364, y0: 14, y1: 158,
        xTicks: [0, 0.5, 1].map((u) => ({ x: sx(u), label: u === 0 ? "0" : u === 1 ? "T" : "T/2" })),
        yTicks: [0, 0.5, 1].map((v) => ({ y: syP(v), label: v.toFixed(1) })),
        xLabel: "normalized time t / T", yLabel: "F(t)",
      });
      svgFid.appendChild(el("path", { class: "d-line d-c3 d-dash", d: pathFrom(bare.ts.map((u, i) => [sx(u), syP(bare.F[i])])) }));
      svgFid.appendChild(el("path", { class: "d-line d-c1", d: pathFrom(cd.ts.map((u, i) => [sx(u), syP(cd.F[i])])) }));
      drawLegend(svgFid, [
        { cls: "d-line d-c1", label: `With CD (λ=${lam.toFixed(2)})` },
        { cls: "d-line d-c3 d-dash", label: "Bare sweep" },
      ], 54, 146);
    }

    card.addEventListener("input", update);
    card.addEventListener("change", update);
    bindPresets(card, update);
    update();
  }

  document.querySelectorAll("[data-demo]").forEach((card) => {
    const kind = card.dataset.demo;
    if (kind === "drag") initDrag(card);
    else if (kind === "filter-function") initFilterFunction(card);
    else if (kind === "sta") initSta(card);
  });
})();
