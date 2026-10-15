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
- [x] Archive of every QOC paper since 2000 in `data/papers/<year>.json` (2020+ harvested first; 2000–2019 back-filled)
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
- [x] World map (Leaflet with Natural Earth country outlines, no tiles; marker clustering) with filters by topic and platform,
      synchronized with the group list; one page per group with topics and recent papers
- [x] Seed: 37 well-known groups in 12 countries
- [x] 29 groups added from the participants of AQuTe25 ("Advances in Quantum Control", MPI-PKS Dresden, July 2025):
      every participant mapped to their PI, added when the PI's tracked papers match and a website names the PI.
      Not added (2026-10-14): Puebla (UC3M), Napolitano (USP), Schlagheck (Liège), Misguich (IPhT) — no group page
      found; Auffèves, Saenz — no matching papers; participants whose PI could not be identified: Candeloro, Cangemi,
      Chakraborty, Gago Encinas, Giergiel, Gupta, Hijano Mendizabal, Iakoupov, Joseph, Kirchberg, Onah, Pagot, Usui,
      Veroni, Zeng
- [ ] Grow the list (candidates still to be verified: Vitanov, Mirrahimi, Sherson, Petersen, Dong,
      Schulte-Herbrüggen, Pupillo, Pechen, Laflamme, Paternostro, …)

## 🚧 Phase 5 — Open problems (first version built)

- [x] `content/problems/<id>.md`: precise statement, why it matters, known results, status (open / partial
      progress / solved) with its justification, topics, and the paper(s) that pose the problem; validated by the build
- [x] Index page with status and topic filters; one page per problem; problems listed on their topic pages
- [x] First four problems, each posed in a published paper — *awaiting expert review*:
      traps in control landscapes for $N \ge 3$ (partial), single-control ensemble controllability beyond qubits
      (open), whether a classical speed limit survives quantization (partial), Agrachev's universal minimum-time gap
      (solved, by combining Gauthier–Rossi 2021 with Gorodski–Lange–Lytchak–Mendes)
- [x] Two more (2026-10-14), after a literature check that they are still open: minimal pulse count of universal
      dynamical decoupling (Θ(K) vs Θ(K²)), and Malvetti's conjecture on time-optimal cooling of two qubits — *awaiting review*
- [ ] More problems (candidates in the Notes below); a "propose a problem" route at launch

## ✅ Phase 6 — Resources (built 2026-10-14)

- [x] Software directory (`data/resources.yaml`): 30 packages, every URL verified (note: Qiskit Dynamics is archived
      and Qiskit Pulse was removed in Qiskit 2.0)
- [x] Essential reading: reviews, tutorials, theses, textbooks, landmark papers
- [x] Glossary of terms and notation (33 terms)
- [x] Timeline of the field
- [ ] Possibly: events (conferences, schools), benchmark problems

## Phase 7 — Public launch

- [x] Licences: CC BY 4.0 for content (`LICENSE-CONTENT`), MIT for code (`LICENSE`); arXiv metadata excluded (2026-10-15)
- [ ] Contribution guide + issue templates ("add a group", "propose an open problem", "report an error")
- [x] Repository public; GitHub Pages deployment at https://llorebaga.github.io/QOC/ (2026-10-14, earlier than planned)
- [ ] Possibly a custom domain
- [x] SEO metadata (descriptions, canonical URLs, Open Graph / Twitter cards), social card
      (`tools/make_social_card.py`), `sitemap.xml` (2026-10-15)
- [ ] Submit the sitemap to search engines (needs the owner's Search Console account)
- [ ] Accessibility audit (automated checks done 2026-10-15: headings, labels, alt text, links; manual pass to do)

---

### Notes & decisions

- **Early publication:** the repository was made public and the site deployed on 2026-10-14, before the rest of
  Phase 7 (licences, contribution guide, SEO, accessibility audit), which is still to do.
- **No Node toolchain:** the build is pure Python so that it runs anywhere with `pip install`.
- **Open problems — candidates to verify next** (each needs a paper that poses it): minimal number of controls for
  ensemble controllability with several unknown parameters (Koch et al. 2022, §2.3); simultaneous *operator*
  controllability with adiabatic methods (ibid., §2.2.5); reachable sets of Markovian vs non-Markovian open systems
  (ibid., §2.3); controllability criteria under thermodynamically consistent dissipation (ibid., §5); whether many-body
  control requires cooling (ibid., §2.3, conjecture after Il'in & Lychkovskiy 2021).
- **Open problems — checked and rejected (2026-10-14), so they are not re-researched:** O(D) vs O(D²) speed-up of
  feedback purification of qudits (Combes et al. 2010) — solved, O(D²), Combes & Wiseman PRX 2011; linear-time GZZ
  gates (Baßler–Heinrich–Kliesch 2024, Conjecture 16) — refuted with a counterexample, Garcia de Andoin PRR 2026;
  error scaling of universally robust DD (Genov et al. 2017) — proved for even n, D'Alessandro et al. 2026;
  necessity of the "infection" criterion for spin networks and global optimality of the Jandura–Pupillo Rydberg CZ
  gate — not posed as open problems in the literature. Possible future "solved" entries: the first two.
