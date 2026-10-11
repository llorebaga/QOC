<p align="center">
  <img src="static/img/logo.svg" alt="QOC" width="320">
</p>

<h3 align="center">Quantum optimal control, mapped.</h3>

<p align="center">
  A living guide to quantum optimal control — the methods, the limits, the people and the
  open questions — with new arXiv papers tracked every day.
</p>

---

> **Status:** private development, Phase 1 of 7 complete. See [ROADMAP.md](ROADMAP.md).

## What's here

| Section | What it is | Status |
|---|---|---|
| **Field map** | Interactive map of the field + one article per topic | Phase 2 — next |
| **Paper tracker** | Daily arXiv fetch, classified into topics, author pages | Phase 3 |
| **Research groups** | World map of groups working on QOC | Phase 4 |
| **Open problems** | Specific, well-posed open questions with status tracking | Phase 5 |
| **Resources** | Software, reviews & tutorials, glossary, timeline | Phase 6 |

## Running it locally

Requires Python ≥ 3.10.

```bash
pip install -r requirements.txt
python build.py --serve          # http://localhost:8000, rebuilds on every change
```

Other commands:

```bash
python build.py                  # build into _site/
python build.py --base QOC       # build for a sub-path, i.e. served under /QOC/ (GitHub Pages)
python tools/make_logo.py        # regenerate the logo and favicon
```

## How the repository is organized

```
config.yaml            site settings, navigation, section descriptions
data/taxonomy.yaml     THE backbone: families and topics of the field (ids are used everywhere)
content/               long-form Markdown content (topic articles, from Phase 2)
templates/             Jinja2 templates — base layout, partials, one file per page type
static/                CSS, JS, images (served as-is)
tools/                 helper scripts (logo generator; later: arXiv fetcher)
build.py               the static-site generator
.github/workflows/     CI (build check; later: daily arXiv update, deployment)
```

### Design principles

- **Plain text first.** All content is Markdown or YAML so that domain experts can edit it
  without touching code.
- **One taxonomy.** Topic ids from `data/taxonomy.yaml` link articles, papers, groups and open
  problems. The build fails if a reference points to a topic that doesn't exist.
- **Static and dependency-light.** No Node toolchain; Python + Jinja2 at build time, vanilla JS in
  the browser, third-party libraries (KaTeX, later Leaflet/D3) loaded only on pages that need them.
- **Accessible and themeable.** Light and dark themes, keyboard navigation, reduced-motion support.
