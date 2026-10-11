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

## 🔜 Phase 2 — Field map & knowledge base

Goal: the reference part of the site. Someone new to the field can start at the map and
understand any area; an expert can use it as a quick reference.

- [ ] Review and freeze taxonomy v1 (families, topics, relations)
- [ ] Topic article format (`content/topics/<id>.md` with front matter):
      intuition → formal statement → key equations → variants → when to use it / limitations →
      key papers (with DOI/arXiv) → software → related topics → open problems
- [ ] Topic page template, with KaTeX math, references, "related topics" and family navigation
- [ ] Interactive field map (force-directed graph, coloured by family, click a node → article)
- [ ] Search across topics (client-side index)
- [ ] Write the articles, family by family, starting with **Algorithms** (GRAPE, Krotov, CRAB/dCRAB,
      GOAT, …), then **Speed limits**, **Robust control**, **Many-body** …
- [ ] Bibliography system: `data/references.yaml` (one entry per paper, cited by key from articles)

## Phase 3 — arXiv paper tracker

- [ ] `tools/fetch_arxiv.py`: query the arXiv API daily (quant-ph and related categories) with a
      broad control-related query; store results in `data/papers/YYYY-MM.json`
- [ ] Relevance filter + topic classifier (start with transparent keyword/alias rules from the
      taxonomy; evaluate on a hand-labelled sample; consider embedding-based classification later)
- [ ] GitHub Actions workflow (daily cron) that fetches, classifies, commits and rebuilds
- [ ] Papers page: latest first, filter by topic/date, full-text search
- [ ] Author pages: click any author → all their tracked papers (with name normalization)
- [ ] RSS/Atom feed per topic; weekly digest page
- [ ] Back-fill: seed the archive with the key papers of the field

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
