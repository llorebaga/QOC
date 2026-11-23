# Contributing to QOC

Thank you for helping improve **QOC** (the living map of quantum optimal control).
All site content lives in plain Markdown and YAML files, so you do not need any web-development experience to contribute.

## Ways to contribute

If you prefer not to edit files directly, use one of the GitHub issue forms:

- **[Propose an open problem](https://github.com/llorebaga/QOC/issues/new?template=propose-open-problem.yml)** — suggest a new well-posed open problem or report a partial/full resolution.
- **[Add or update a research group](https://github.com/llorebaga/QOC/issues/new?template=add-group.yml)** — add a missing group or update an existing PI/institution/URL.
- **[Report an error or missing reference](https://github.com/llorebaga/QOC/issues/new?template=report-error.yml)** — flag a factual mistake, outdated claim, broken link, or missing citation.

Pull requests are also very welcome!

---

## Editorial standards

1. **Primary sources only.** Every mathematical claim, theorem, or status update in articles (`content/topics/`) and open problems (`content/problems/`) must be grounded in the cited papers.
2. **Never hand-write bibliography entries.** All entries in `data/references.yaml` are generated directly from Crossref or arXiv metadata using:
   ```bash
   python3 tools/refs.py add <key> --doi <DOI>
   # or
   python3 tools/refs.py add <key> --arxiv <ARXIV_ID>
   ```
   After adding or updating references, validate the bibliography:
   ```bash
   python3 tools/refs.py check
   ```
3. **Open problems.** A problem belongs in `content/problems/<problem-id>.md` only if:
   - it can be stated precisely, and
   - a published paper (or peer-reviewed/arXiv manuscript) explicitly poses it as a conjecture, open question, or stated goal.
   - New entries start with `review: draft` in front matter. Solved/refuted problems stay in the list with `status: solved` and the resolving citation.
4. **Research groups.** Entries in `data/groups.yaml` are added via `tools/groups.py`:
   - The group website must load and explicitly name its PIs.
   - Coordinates and location come from the institution's Wikidata item (`tools/groups.py` fetches them).
   - Topics and platforms are computed automatically from the PIs' tracked arXiv papers rather than self-descriptions.
   - Validate with `python3 tools/groups.py check`.

---

## Local build & preview

The site is pure Python (no Node toolchain required):

```bash
pip install -r requirements.txt
python3 tools/refs.py check
python3 build.py
python3 build.py --base QOC    # verify GitHub Pages sub-path build
```

To preview locally with live rebuild on file changes:

```bash
python3 build.py --serve
```

## Licensing

By submitting content (articles, open problems, glossary entries, resources, taxonomy edits), you agree to license your text contributions under **CC BY 4.0** ([LICENSE-CONTENT](LICENSE-CONTENT)) and code contributions under the **MIT Licence** ([LICENSE](LICENSE)).
