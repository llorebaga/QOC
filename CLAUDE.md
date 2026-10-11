# QOC — notes for working on this repo

Static website about quantum optimal control. See README.md (structure) and ROADMAP.md (phases).

## Working agreement
- Build in phases, one at a time, and finish each properly before moving on. Quality over speed.
- Scientific content must be accurate and sourced. Never invent references, DOIs, arXiv ids,
  group details or coordinates. Verify them, or leave them out and flag them.
- The repo stays **private** until Phase 7. Do not enable GitHub Pages before then (Pages sites are public).

## Build & preview
- `python build.py --serve` → http://localhost:8000 (auto-rebuild). `.claude/launch.json` has the `qoc-site` config.
- `python build.py --base QOC` is what CI runs (served under /QOC/).
- The build validates `data/taxonomy.yaml` (unique ids, valid families, valid `related` refs). Keep it passing.

## Conventions
- Topic ids in `data/taxonomy.yaml` are permanent keys (URLs + data references). Rename only with a migration.
- Colours: use CSS tokens from `static/css/main.css` `:root`; every taxonomy family has `--fam-<id>` in
  both light and dark blocks. A new family needs both.
- Pages that use LaTeX include `partials/katex.html` in `{% block head %}`. Delimiters: `$$…$$` and `\(…\)`.
- The logo is generated: edit `tools/make_logo.py`, never `templates/partials/logo.html` or `static/img/*.svg` by hand.
- Vanilla JS, no build step. Third-party libraries come from cdn.jsdelivr.net with pinned versions, loaded only where needed.
