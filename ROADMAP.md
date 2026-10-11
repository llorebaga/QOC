# QOC roadmap

The project is built in phases. Each phase is finished and reviewed before the next starts.

---

## ✅ Phase 1 — Foundations

- [x] Private GitHub repository
- [x] Logo: "QOC" wordmark with a control pulse running through the letters (`tools/make_logo.py`)
- [x] Design system: colour tokens (light/dark), typography, components, one colour per taxonomy family
- [x] Static-site generator (`build.py`): Jinja2 templates, YAML data, taxonomy validation, dev server
- [x] Home page, About page with roadmap, placeholder pages for every section, 404
- [x] Draft taxonomy of the field (`data/taxonomy.yaml`) — **10 families, 42 topics** — shown on `/map/`
- [x] CI: build check on every push

## 🚧 Phase 2 — Field map & knowledge base (in progress)

Goal: the reference part of the site. Someone new to the field can start at the map and
understand any area; an expert can use it as a quick reference.

- [x] Taxonomy v1 — checked against ~2000 recent arXiv control papers; 8 topics added
      (QCPOP, propagation methods, Floquet engineering, Lyapunov/MPC, linear quantum systems,
      bosonic control, pulse-level compilation, control electronics) → **10 families, 50 topics**
- [x] Bibliography system: `data/references.yaml`, entries generated from Crossref/arXiv by
      `tools/refs.py` (never typed by hand); `refs.py check` validates
- [x] Article format: `content/topics/<id>.md` — Markdown + LaTeX, `[@key]` citations,
      `[[topic]]` cross-links, key papers, software; the build fails on unknown keys/topics
- [x] Topic pages for all 50 topics (article or "not written yet" + related topics)
- [x] Interactive field map (D3 force layout, family clusters, hover neighbours, search, zoom)
- [x] **Algorithms family written** (10 articles) — *awaiting expert review*
- [ ] Review of the Algorithms articles
- [ ] Remaining families, one at a time, each reviewed before the next:
      Foundations → Speed limits → Robust → Analytic → Learning → Open systems → Many-body → Tasks → Platforms

## 🚧 Phase 3 — arXiv paper tracker (data pipeline running)

- [x] `tools/fetch_arxiv.py`: month-by-month harvest of arXiv, validated query strategy
      (API used as a superset pre-filter; 0/75 misses against a full month of quant-ph)
- [x] Transparent selection rule in `qocsite/selection.py`, documented on the About page
- [x] Archive of every QOC paper since 2020 in `data/papers/<year>.json`
- [x] Daily GitHub Action (`.github/workflows/papers.yml`) fetching the last 14 days and committing
- [x] Papers-per-year chart on the home page, regenerated at every build
- [ ] Topic classifier (taxonomy aliases → evaluated against a hand-labelled sample)
- [ ] Papers page: latest first, filter by topic/date, full-text search
- [ ] Author pages: click any author → all their tracked papers (with name normalization)
- [ ] RSS/Atom feed per topic; weekly digest page

## Phase 4 — Research groups map

- [ ] `data/groups.yaml`: PI(s), institution, city, coordinates, website, topics, platforms,
      theory/experiment
- [ ] World map (Leaflet + OpenStreetMap tiles, marker clustering), filters by topic/platform
- [ ] Group list view and group pages, linked to their papers in the tracker
- [ ] Seed with well-known groups; every entry checked against the group's own website

## Phase 5 — Open problems

- [ ] `content/problems/<id>.md`: precise statement, background, why it matters, known partial
      results, references, status (open / partial progress / solved), topics, proposer
- [ ] Index page with status and topic filters; per-problem pages
- [ ] Seed list of specific problems (to be curated carefully)

## Phase 6 — Resources

- [ ] Software directory (QuTiP, Krotov, QuOCS, C3, Juqbox, QuantumControl.jl, Piccolo.jl,
      Quandary, Boulder Opal, Dynamiqs, Qiskit Dynamics, Spinach, …)
- [ ] Essential reading: reviews, tutorials, theses, textbooks, landmark papers
- [ ] Glossary of terms and notation
- [ ] Timeline of the field
- [ ] Possibly: events (conferences, schools), benchmark problems

## Phase 7 — Public launch

- [ ] Choose licences (suggestion: CC BY 4.0 for content, MIT for code)
- [ ] Contribution guide + issue templates ("add a group", "propose an open problem", "report an error")
- [ ] Make repository public, enable GitHub Pages deployment (or custom domain)
- [ ] SEO metadata, social cards, sitemap; accessibility audit

---

### Notes & decisions

- **Why GitHub Pages is not enabled yet:** on non-Enterprise plans, a Pages site is *public* even
  when the repository is private. Deployment is switched on at launch (Phase 7).
- **No Node toolchain:** the build is pure Python so that it runs anywhere with `pip install`.
