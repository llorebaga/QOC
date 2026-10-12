/* QOC — paper tracker: search, filters and author pages, on top of the server-rendered lists.
   Data: papers/data/index.json (all papers, newest first, without abstracts) and
   papers/data/abstracts-<year>.json (loaded only when an abstract is opened or the search needs it). */
(function () {
  "use strict";

  const root = document.querySelector("[data-tracker]");
  if (!root) return;

  const PAGE = 50;
  const mode = root.dataset.mode || "papers";
  const base = root.dataset.base;
  const list = root.querySelector("[data-tracker-list]");
  const more = root.querySelector("[data-tracker-more]");
  const abstracts = {};                 // year -> {id: abstract}
  const loading = {};                   // year -> Promise
  let data = null;                      // {topics, authors, papers}
  let results = [];
  let shown = 0;

  /* ------------------------------------------------------------ helpers */
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fold = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  const params = () => new URLSearchParams(window.location.search);

  function loadAbstracts(year) {
    if (abstracts[year]) return Promise.resolve(abstracts[year]);
    if (!loading[year]) {
      loading[year] = fetch(root.dataset.abstracts + year + ".json")
        .then((r) => (r.ok ? r.json() : {}))
        .then((d) => (abstracts[year] = d))
        .catch(() => (abstracts[year] = {}));
    }
    return loading[year];
  }

  function paperHTML(p, maxAuthors) {
    const [id, date, title, authorIdx, topicIdx, primary] = p;
    const authors = authorIdx.slice(0, maxAuthors).map((i) => {
      const [name, slug] = data.authors[i];
      return `<a href="${base}papers/authors/?a=${encodeURIComponent(slug)}">${esc(name)}</a>`;
    }).join(", ") + (authorIdx.length > maxAuthors ? ` <span class="muted">+${authorIdx.length - maxAuthors} more</span>` : "");
    const topics = topicIdx.map((i) => {
      const [tid, label, fam] = data.topics[i];
      return `<li><a class="topic-chip" href="${base}papers/?topic=${tid}" style="--fam: var(--fam-${fam})">${esc(label)}</a></li>`;
    }).join("");
    return `<li class="paper" data-id="${esc(id)}">
  <div class="paper-meta"><time datetime="${date}">${date}</time>
    <a class="paper-id" href="https://arxiv.org/abs/${esc(id)}" rel="noopener">arXiv:${esc(id)}</a>
    ${primary ? `<span class="paper-cat">${esc(primary)}</span>` : ""}</div>
  <h3 class="paper-title"><a href="https://arxiv.org/abs/${esc(id)}" rel="noopener">${esc(title)}</a></h3>
  <p class="paper-authors">${authors}</p>
  ${topics ? `<ul class="paper-topics">${topics}</ul>` : ""}
  <details class="paper-abstract" data-year="${date.slice(0, 4)}"><summary>Abstract</summary><p></p></details>
</li>`;
  }

  // Abstracts are filled in when opened (server-rendered ones already contain text).
  root.addEventListener("toggle", (e) => {
    const d = e.target;
    if (!(d instanceof HTMLDetailsElement) || !d.open || !d.classList.contains("paper-abstract")) return;
    const p = d.querySelector("p");
    if (p.textContent.trim()) return;
    p.textContent = "Loading…";
    const id = d.closest(".paper").dataset.id;
    loadAbstracts(d.dataset.year).then((a) => { p.textContent = a[id] || "Abstract not available."; });
  }, true);

  function renderMore() {
    const next = results.slice(shown, shown + PAGE);
    list.insertAdjacentHTML("beforeend", next.map((p) => paperHTML(p, 12)).join(""));
    shown += next.length;
    if (more) more.hidden = shown >= results.length;
  }

  function renderResults(items) {
    results = items;
    shown = 0;
    list.innerHTML = "";
    renderMore();
  }

  if (more) more.addEventListener("click", renderMore);

  /* ------------------------------------------------------------ papers page */
  function initPapers() {
    const form = root.querySelector("[data-tracker-form]");
    const status = root.querySelector("[data-tracker-status]");
    const topicPos = Object.fromEntries(data.topics.map((t, i) => [t[0], i]));
    const haystack = data.papers.map((p) => fold(p[2] + " " + p[3].map((i) => data.authors[i][0]).join(" ")));
    let timer = 0, run = 0;

    const p0 = params();
    ["q", "topic", "year"].forEach((k) => { if (p0.get(k) && form.elements[k]) form.elements[k].value = p0.get(k); });

    async function apply(pushURL) {
      const id = ++run;
      const q = form.elements.q.value.trim();
      const topic = form.elements.topic.value;
      const year = form.elements.year.value;
      const tokens = fold(q).split(/\s+/).filter(Boolean);
      const ti = topic in topicPos ? topicPos[topic] : -1;

      let idx = [];
      data.papers.forEach((p, i) => {
        if (ti >= 0 && !p[4].includes(ti)) return;
        if (year && !p[1].startsWith(year)) return;
        idx.push(i);
      });

      if (tokens.length) {
        // titles and authors first; abstracts of the remaining candidates are loaded on demand
        const years = [...new Set(idx.map((i) => data.papers[i][1].slice(0, 4)))];
        const missing = years.filter((y) => !abstracts[y]);
        if (missing.length) {
          status.textContent = "Searching abstracts…";
          await Promise.all(missing.map(loadAbstracts));
          if (id !== run) return;
        }
        idx = idx.filter((i) => {
          const p = data.papers[i];
          const text = haystack[i] + " " + fold((abstracts[p[1].slice(0, 4)] || {})[p[0]] || "");
          return tokens.every((t) => text.includes(t));
        });
      }

      renderResults(idx.map((i) => data.papers[i]));
      const parts = [];
      if (topic) parts.push(`in ${data.topics[ti] ? data.topics[ti][1] : topic}`);
      if (year) parts.push(`from ${year}`);
      if (q) parts.push(`matching “${q}”`);
      status.textContent = `${idx.length.toLocaleString("en")} paper${idx.length === 1 ? "" : "s"}${parts.length ? " " + parts.join(", ") : ""}, newest first.`;

      if (pushURL) {
        const u = new URLSearchParams();
        if (q) u.set("q", q);
        if (topic) u.set("topic", topic);
        if (year) u.set("year", year);
        const qs = u.toString();
        history.replaceState(null, "", window.location.pathname + (qs ? "?" + qs : ""));
      }
    }

    form.addEventListener("submit", (e) => { e.preventDefault(); apply(true); });
    form.addEventListener("input", (e) => {
      clearTimeout(timer);
      timer = setTimeout(() => apply(true), e.target.name === "q" ? 250 : 0);
    });
    form.addEventListener("reset", () => setTimeout(() => apply(true), 0));
    apply(false);
  }

  /* ------------------------------------------------------------ authors page */
  function initAuthors() {
    const input = root.querySelector("[data-author-search]");
    const out = root.querySelector("[data-author-results]");
    const counts = new Array(data.authors.length).fill(0);
    data.papers.forEach((p) => p[3].forEach((i) => counts[i]++));
    const names = data.authors.map((a) => fold(a[0]));
    const link = (i) => `<a href="?a=${encodeURIComponent(data.authors[i][1])}">${esc(data.authors[i][0])}</a>`;

    input.disabled = false;
    input.addEventListener("input", () => {
      const q = fold(input.value.trim());
      if (q.length < 2) { out.innerHTML = ""; return; }
      const tokens = q.split(/\s+/);
      const hits = [];
      names.forEach((n, i) => { if (tokens.every((t) => n.includes(t))) hits.push(i); });
      hits.sort((a, b) => counts[b] - counts[a]);
      out.innerHTML = hits.length
        ? hits.slice(0, 25).map((i) => `<li>${link(i)} <span class="muted">${counts[i]}</span></li>`).join("")
        : `<li class="muted">No author found.</li>`;
    });

    const slug = params().get("a");
    if (!slug) return;
    const ai = data.authors.findIndex((a) => a[1] === slug);
    const title = root.ownerDocument.querySelector("[data-author-title]");
    const lead = root.ownerDocument.querySelector("[data-author-lead]");
    if (ai < 0) {
      lead.textContent = "No tracked paper has an author with this name.";
      return;
    }
    const papers = data.papers.filter((p) => p[3].includes(ai));
    const name = data.authors[ai][0];
    const years = papers.map((p) => p[1].slice(0, 4));
    title.textContent = name;
    document.title = `${name} — QOC papers`;
    lead.textContent = `${papers.length} tracked paper${papers.length === 1 ? "" : "s"}` +
      (years.length ? `, ${years[years.length - 1]}–${years[0]}.` : ".");

    const topicCount = {}, coCount = {};
    papers.forEach((p) => {
      p[4].forEach((t) => (topicCount[t] = (topicCount[t] || 0) + 1));
      p[3].forEach((c) => { if (c !== ai) coCount[c] = (coCount[c] || 0) + 1; });
    });
    const top = (o, n) => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, n);
    root.querySelector("[data-author-topics]").innerHTML = top(topicCount, 10).map(([t, n]) => {
      const [tid, label, fam] = data.topics[t];
      return `<li><a class="topic-chip" href="${base}topics/${tid}/" style="--fam: var(--fam-${fam})">${esc(label)}</a> <span class="muted">${n}</span></li>`;
    }).join("") || `<li class="muted">None classified.</li>`;
    root.querySelector("[data-author-coauthors]").innerHTML =
      top(coCount, 12).map(([c, n]) => `<li>${link(+c)} <span class="muted">${n}</span></li>`).join("") ||
      `<li class="muted">No co-authors.</li>`;

    root.querySelector("[data-author-top]").hidden = true;
    root.querySelector("[data-author-view]").hidden = false;
    renderResults(papers);
  }

  /* ------------------------------------------------------------ start */
  fetch(root.dataset.index)
    .then((r) => r.json())
    .then((d) => { data = d; (mode === "authors" ? initAuthors : initPapers)(); })
    .catch(() => {
      const status = root.querySelector("[data-tracker-status]");
      if (status) status.textContent = "The paper index could not be loaded; showing the most recent papers.";
    });
})();
