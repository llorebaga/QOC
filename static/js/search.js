/* QOC — unified site-wide search palette (/ or Cmd/Ctrl+K). No dependencies. */
(function () {
  "use strict";

  const dialog = document.getElementById("site-search");
  if (!dialog) return;

  const input = dialog.querySelector("[data-search-input]");
  const list = dialog.querySelector("[data-search-results]");
  const status = dialog.querySelector("[data-search-status]");
  const papersLink = dialog.querySelector("[data-search-papers]");
  const indexUrl = dialog.dataset.searchUrl;
  const papersBase = dialog.dataset.papersUrl;

  const KINDS = {
    topic: "Topic",
    problem: "Open problem",
    group: "Group",
    glossary: "Glossary",
    software: "Software",
    reading: "Reading",
  };
  const KIND_PRIORITY = { topic: 6, problem: 5, group: 4, glossary: 3, software: 2, reading: 1 };

  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fold = (s) => String(s || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();

  let index = null;
  let loading = null;
  let active = -1;

  function loadIndex() {
    if (index) return Promise.resolve(index);
    if (!loading) {
      status.textContent = "Loading index…";
      loading = fetch(indexUrl)
        .then((r) => {
          if (!r.ok) throw new Error(r.statusText);
          return r.json();
        })
        .then((rows) => {
          index = rows.map((r) => ({
            ...r,
            ft: fold(r.t),
            fm: fold(r.m),
            fs: fold(r.s),
          }));
          return index;
        })
        .catch(() => {
          loading = null;
          status.textContent = "Could not load search index.";
          return [];
        });
    }
    return loading;
  }

  function score(item, terms, whole) {
    let s = 0;
    if (item.ft === whole) s += 120;
    else if (item.ft.startsWith(whole)) s += 70;
    else if (item.ft.includes(whole)) s += 40;

    for (const term of terms) {
      if (item.ft.includes(term)) s += 24;
      else if (item.fm.includes(term)) s += 14;
      else if (item.fs.includes(term)) s += 7;
      else return -1;
    }
    return s + (KIND_PRIORITY[item.k] || 0);
  }

  function setActive(i) {
    const links = list.querySelectorAll("a");
    if (!links.length) {
      active = -1;
      return;
    }
    active = ((i % links.length) + links.length) % links.length;
    links.forEach((a, idx) => {
      const on = idx === active;
      a.classList.toggle("is-active", on);
      a.setAttribute("aria-selected", String(on));
      if (on) a.scrollIntoView({ block: "nearest" });
    });
  }

  function render() {
    const raw = input.value.trim();
    if (raw) {
      papersLink.href = `${papersBase}?q=${encodeURIComponent(raw)}`;
      papersLink.textContent = `Search tracked papers for “${raw}” →`;
    } else {
      papersLink.href = papersBase;
      papersLink.textContent = "Search all tracked papers →";
    }

    if (!index) return;
    if (!raw) {
      active = -1;
      status.textContent = "Try “GRAPE”, “barren plateaus”, “Rydberg”, “QuTiP”, “Lindblad”…";
      list.innerHTML = "";
      return;
    }

    const whole = fold(raw);
    const terms = whole.split(/\s+/).filter(Boolean);
    const hits = [];
    for (const item of index) {
      const sc = score(item, terms, whole);
      if (sc > 0) hits.push([sc, item]);
    }
    hits.sort((a, b) => b[0] - a[0] || a[1].t.localeCompare(b[1].t));
    const top = hits.slice(0, 14);

    if (!top.length) {
      active = -1;
      status.textContent = `No matches for “${raw}”. Try the paper tracker link below.`;
      list.innerHTML = "";
      return;
    }

    status.textContent = `${hits.length} ${hits.length === 1 ? "result" : "results"}${hits.length > top.length ? ` (showing top ${top.length})` : ""}`;
    list.innerHTML = top.map(([, r]) =>
      `<li role="option"><a href="${esc(r.u)}" class="search-item">` +
      `<span class="search-item-head"><span class="search-item-title">${esc(r.t)}</span>` +
      `<span class="search-badge search-badge-${esc(r.k)}">${esc(KINDS[r.k] || r.k)}</span></span>` +
      (r.s ? `<span class="search-item-sub">${esc(r.s)}</span>` : "") +
      `</a></li>`
    ).join("");
    setActive(0);
  }

  function openSearch() {
    if (dialog.open) return;
    if (typeof dialog.showModal === "function") dialog.showModal();
    else dialog.setAttribute("open", "");
    input.focus();
    input.select();
    loadIndex().then(render);
  }

  function closeSearch() {
    if (!dialog.open) return;
    if (typeof dialog.close === "function") dialog.close();
    else dialog.removeAttribute("open");
  }

  document.querySelectorAll("[data-search-open]").forEach((btn) => {
    btn.addEventListener("click", openSearch);
  });
  dialog.querySelector("[data-search-close]").addEventListener("click", closeSearch);
  dialog.addEventListener("click", (e) => {
    if (e.target === dialog) closeSearch();
  });
  input.addEventListener("input", render);
  input.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive(active + 1);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive(active - 1);
    } else if (e.key === "Enter" && active >= 0) {
      const link = list.querySelectorAll("a")[active];
      if (link) {
        e.preventDefault();
        closeSearch();
        window.location.href = link.getAttribute("href");
      }
    }
  });
  list.addEventListener("click", (e) => {
    if (e.target.closest("a")) closeSearch();
  });

  document.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      dialog.open ? closeSearch() : openSearch();
      return;
    }
    if (e.key === "/" && !e.metaKey && !e.ctrlKey && !e.altKey) {
      const el = document.activeElement;
      const inField = el && (el.tagName === "INPUT" || el.tagName === "TEXTAREA" || el.tagName === "SELECT" || el.isContentEditable);
      if (!inField && !dialog.open) {
        e.preventDefault();
        openSearch();
      }
    }
  });
})();
