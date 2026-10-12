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

## Content & data
- References: only via `python tools/refs.py add KEY --doi ... / --arxiv ...` (Crossref/arXiv metadata). Never hand-type
  bibliographic fields. Keys: `firstauthorYEARword`. Run `refs.py check` after changes.
- Articles: `content/topics/<id>.md`; `[@key]` citations, `[[topic-id]]` links, `$…$`/`$$…$$` math. New articles start as
  `status: draft`; only the user marks them `reviewed`. Verify software URLs (gh api / curl) before listing them.
- Papers: `tools/fetch_arxiv.py`. The selection rule lives in `qocsite/selection.py` (shown on the About page).
  *Widening* it (new TERMS) requires a full re-harvest (`--since 2000-01-01`); *tightening* it only needs
  `--reselect`. Any rule change must be validated: download all quant-ph papers of a few months and check the API
  query misses nothing, then label a sample of the affected papers. arXiv rate-limits: never run other arXiv API calls
  while a harvest is running. Use https://export.arxiv.org.
- Paper-count quality: `tools/paper_quality.py` (precision / recall / share) with hand labels in `data/quality/`;
  `data/quality/summary.yaml` feeds the About page. Re-run after rule changes and update the summary.
- Topics of papers: phrase rules in `data/classifier.yaml` (scoring in `qocsite/classify.py`). After changing rules,
  run `paper_quality.py topics` on the dev labels; report test-set numbers honestly (the test set is for measuring,
  not tuning) and update `summary.yaml`. Classification results are cached in `.cache/` (gitignored).
- Author identities: `qocsite/authors.py` (merging rules in its docstring).
- Research groups: `data/groups.yaml` via `tools/groups.py` (`find` a Wikidata id, `coords`, `check --write`). Never
  type coordinates/cities; only add a group whose website names its PIs. Group
  topics come from the PIs' papers (add `arxiv_names` when a PI publishes under another spelling).
- The dev server rebuilds in a subprocess, so code changes apply without restarting it.

## Conventions
- Topic ids in `data/taxonomy.yaml` are permanent keys (URLs + data references). Rename only with a migration.
- Colours: use CSS tokens from `static/css/main.css` `:root`; every taxonomy family has `--fam-<id>` in
  both light and dark blocks. A new family needs both.
- Pages that use LaTeX include `partials/katex.html` in `{% block head %}`. Delimiters: `$$…$$` and `\(…\)`.
- The logo is generated: edit `tools/make_logo.py`, never `templates/partials/logo.html` or `static/img/*.svg` by hand.
- Vanilla JS, no build step. Third-party libraries come from cdn.jsdelivr.net with pinned versions, loaded only where needed.
