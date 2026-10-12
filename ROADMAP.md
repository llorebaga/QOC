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
- [x] **Foundations family written** (5 articles: controllability, problem formulation & figures of merit,
      Pontryagin's maximum principle, geometric & time-optimal control, control landscapes) — *awaiting review*
- [x] **Speed limits & complexity family written** (2 articles: quantum speed limits, control complexity) — *awaiting review*
- [x] **Robust control family written** (4 articles: robust & ensemble control, composite pulses,
      dynamical decoupling, filter functions) — *awaiting review*
- [x] **Analytic & adiabatic design family written** (5 articles: shortcuts to adiabaticity, adiabatic passage,
      DRAG, Floquet engineering, Lyapunov/tracking/MPC) — *awaiting review*
- [x] **Learning & closed-loop family written** (3 articles: closed-loop & in-situ optimization,
      reinforcement & machine learning, system identification) — *awaiting review*
- [x] **Open systems & feedback family written** (4 articles: open-system control, reservoir engineering,
      measurement-based feedback, linear quantum systems & coherent feedback) — *awaiting review*
- [x] **Many-body & large systems family written** (3 articles: many-body optimal control, variational
      algorithms & QAOA as control, bosonic & continuous-variable control) — *awaiting review*
- [x] **Tasks family written** (6 articles: gate synthesis, state preparation & transfer, sensing & metrology,
      quantum thermodynamics, quantum error correction, pulse-level compilation) — *awaiting review*
- [x] **Platforms family written** (8 articles: superconducting circuits, trapped ions, neutral atoms & Rydberg
      arrays, ultracold atoms, spins, molecules, photonics & optomechanics, control electronics) — *awaiting review*
- [x] **Every topic of the map has an article (50)**
- [ ] Review of the written articles (all 50 are drafts)

## 🚧 Phase 3 — arXiv paper tracker (built; awaiting review)

- [x] `tools/fetch_arxiv.py`: month-by-month harvest of arXiv, validated query strategy
      (API used as a superset pre-filter; 0/75 misses against a full month of quant-ph)
- [x] Transparent selection rule in `qocsite/selection.py`, documented on the About page
- [x] Archive of every QOC paper since 2010 in `data/papers/<year>.json` (2020+ harvested first; 2010–2019 back-filled)
- [x] Daily GitHub Action (`.github/workflows/papers.yml`) fetching the last 14 days and committing
- [x] Papers-per-year chart on the home page, regenerated at every build
- [x] Topic classifier: phrase rules per topic (`data/classifier.yaml`, `qocsite/classify.py`), tuned on 60
      hand-labelled papers, evaluated blind on 120 others — 60% precision, 82% recall, 89% of papers with ≥1 correct topic
- [x] Papers page: newest first, filters by topic and year, full-text search (abstracts loaded on demand)
- [x] Author pages: every author → all their tracked papers, topics and co-authors (name variants merged when unambiguous)
- [x] Atom feeds (all papers and one per topic); weekly digest page; recent papers on every topic page

## 🚧 Phase 4 — Research groups map (first version built)

- [x] `data/groups.yaml`, maintained with `tools/groups.py`: PIs, institution, website;
      city, country and coordinates generated from the institution's Wikidata entry (never typed by hand)
- [x] Every entry checked automatically: the website loads and names every PI (`groups.py check`)
- [x] Topics and platforms derived from the PIs' tracked papers (not self-descriptions); PIs linked to author pages
- [x] World map (Leaflet + OpenStreetMap tiles, marker clustering) with filters by topic and platform,
      synchronized with the group list; one page per group with topics and recent papers
- [x] Seed: 32 well-known groups in 11 countries
- [ ] Grow the list (candidates still to be verified: Sugny, Vitanov, Muga, Boscain & Sigalotti, Mirrahimi,
      Sherson, Biercuk, Petersen, Dong, Yuan, Xi Chen, Schulte-Herbrüggen, Pupillo, Pechen, Laflamme, …); contribution form at launch

## Phase 5 — Open problems

- [ ] `content/problems/<id>.md`: precise statement, background, why it matters, known partial
      results, references, status (open / partial progress / solved), topics, proposer
- [ ] Index page with status and topic filters; per-problem pages
- [ ] Seed list of specific problems (to be curated carefully)

## Phase 6 — Resources

- [ ] Software directory (QuTiP, Krotov, QuOCS, C3, Juqbox, QuantumControl.jl, Piccolo.jl,
      Quandary, Boulder Opal, Dynamiqs, Spinach, …; note: Qiskit Dynamics is archived and Qiskit Pulse was
      removed in Qiskit 2.0)
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
