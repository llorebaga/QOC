/* QOC — hardware Hamiltonians: catalog filters (URL-synced) and Python/Julia code tabs + copy button. */
(function () {
  "use strict";

  /* ------------------------------------------------------------ index filters */
  const root = document.querySelector("[data-hams]");
  if (root) {
    const buttons = [...root.querySelectorAll("[data-arch]")].filter((el) => el.tagName === "BUTTON");
    const select = root.querySelector("select[name=regime]");
    const input = root.querySelector("input[name=q]");
    const status = root.querySelector("[data-hams-status]");
    const cards = [...root.querySelectorAll("[data-hams-list] > li")];
    const fold = (s) => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
    const haystacks = new Map(cards.map((c) => [c, fold(c.textContent)]));

    const params = new URLSearchParams(location.search);
    let arch = params.get("arch") || "";
    if (!buttons.some((b) => b.dataset.arch === arch)) arch = "";
    if (select && [...select.options].some((o) => o.value === params.get("regime"))) select.value = params.get("regime");
    if (input && params.get("q")) input.value = params.get("q");

    function apply() {
      const regime = select ? select.value : "";
      const rawQ = input ? input.value.trim() : "";
      const terms = rawQ ? fold(rawQ).split(/\s+/).filter(Boolean) : [];
      let shown = 0;
      for (const card of cards) {
        const hay = haystacks.get(card);
        const ok = (!arch || card.dataset.arch === arch) &&
                   (!regime || card.dataset.regimes.split(" ").includes(regime)) &&
                   terms.every((t) => hay.includes(t));
        card.hidden = !ok;
        if (ok) shown++;
      }
      for (const b of buttons) b.setAttribute("aria-pressed", String(b.dataset.arch === arch));
      status.textContent = `${shown} ${shown === 1 ? "model" : "models"}${rawQ ? ` matching “${rawQ}”` : ""}.`;

      const q = new URLSearchParams();
      if (arch) q.set("arch", arch);
      if (regime) q.set("regime", regime);
      if (rawQ) q.set("q", rawQ);
      history.replaceState(null, "", q.toString() ? `?${q}` : location.pathname);
    }

    for (const b of buttons) b.addEventListener("click", () => { arch = b.dataset.arch; apply(); });
    if (select) select.addEventListener("change", apply);
    if (input) input.addEventListener("input", apply);
    root.querySelector("[data-hams-form]").addEventListener("submit", (e) => e.preventDefault());
    apply();
  }

  /* ------------------------------------------------------------ code tabs + copy */
  const codeBox = document.querySelector("[data-code-tabs]");
  if (codeBox) {
    const tabs = [...codeBox.querySelectorAll("[data-lang]")];
    const panels = [...codeBox.querySelectorAll("[data-code-panel]")];
    const copyBtn = codeBox.querySelector("[data-copy-code]");
    let lang = "python";

    function selectLang(next) {
      lang = next;
      tabs.forEach((t) => {
        const on = t.dataset.lang === lang;
        t.setAttribute("aria-selected", String(on));
        t.setAttribute("aria-pressed", String(on));
      });
      panels.forEach((p) => { p.hidden = p.dataset.codePanel !== lang; });
    }

    tabs.forEach((t) => t.addEventListener("click", () => selectLang(t.dataset.lang)));
    if (copyBtn) {
      copyBtn.addEventListener("click", () => {
        const active = panels.find((p) => !p.hidden);
        if (!active) return;
        const text = active.textContent;
        const done = () => {
          copyBtn.textContent = "Copied";
          setTimeout(() => { copyBtn.textContent = "Copy"; }, 1600);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done).catch(() => {});
        }
      });
    }
  }
})();
