#!/usr/bin/env python
"""Build the QOC static site into ./_site.

Usage
-----
    python build.py                 # build with the base URL from config.yaml
    python build.py --base QOC      # build for the sub-path /QOC/ (e.g. GitHub Pages)
    python build.py --serve         # build, serve on localhost and rebuild on change

The site is plain HTML/CSS/JS. Content lives in YAML/Markdown files under
data/ and content/, templates under templates/, assets under static/.
"""
from __future__ import annotations

import argparse
import datetime as dt
import functools
import hashlib
import http.server
import subprocess
import sys
import threading
import time
from pathlib import Path

import json

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from markupsafe import Markup

from qocsite.content import ContentError, format_reference, render_article
from qocsite import selection
from qocsite.papers import load_papers, yearly_stats

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_site"
WATCHED = ["config.yaml", "data", "content", "templates", "static", "qocsite"]


class BuildError(Exception):
    pass


# ------------------------------------------------------------------ loading
def load_yaml(path: Path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_taxonomy(path: Path) -> dict:
    """Load and validate the taxonomy; return families with their topics."""
    raw = load_yaml(path)
    families = {f["id"]: {**f, "topics": []} for f in raw["families"]}
    topics: dict[str, dict] = {}
    errors = []

    for t in raw["topics"]:
        tid = t["id"]
        if tid in topics:
            errors.append(f"duplicate topic id '{tid}'")
        if t["family"] not in families:
            errors.append(f"topic '{tid}' has unknown family '{t['family']}'")
        topics[tid] = {**t, "aliases": t.get("aliases", []), "related": t.get("related", [])}

    # Relations are undirected: build symmetric neighbour lists.
    neighbours = {tid: [] for tid in topics}
    edges = set()
    for tid, t in topics.items():
        for rid in t["related"]:
            if rid not in topics:
                errors.append(f"topic '{tid}' relates to unknown topic '{rid}'")
                continue
            if rid == tid:
                errors.append(f"topic '{tid}' relates to itself")
                continue
            edges.add(tuple(sorted((tid, rid))))
    for a, b in sorted(edges):
        neighbours[a].append(b)
        neighbours[b].append(a)

    if errors:
        raise BuildError("taxonomy.yaml:\n  " + "\n  ".join(errors))

    for tid, t in topics.items():
        t["neighbours"] = neighbours[tid]
        t["label"] = t.get("label", t["title"])
        families[t["family"]]["topics"].append(t)

    return {
        "families": list(families.values()),
        "topics": topics,
        "edges": sorted(edges),
    }


def load_articles(taxonomy: dict, references: dict, url) -> dict:
    """Render content/topics/<id>.md for every topic that has one."""
    articles = {}
    for f in sorted((ROOT / "content" / "topics").glob("*.md")):
        tid = f.stem
        if tid not in taxonomy["topics"]:
            raise BuildError(f"content/topics/{f.name}: no topic '{tid}' in taxonomy.yaml")
        try:
            articles[tid] = render_article(tid, f.read_text(encoding="utf-8"), references=references,
                                           topics=taxonomy["topics"], url=url)
        except ContentError as exc:
            raise BuildError(str(exc)) from exc
    return articles


def map_data(taxonomy: dict, articles: dict, url) -> dict:
    """Graph data for the interactive field map."""
    return {
        "families": [{"id": f["id"], "title": f["title"]} for f in taxonomy["families"]],
        "nodes": [{"id": t["id"], "label": t["label"], "title": t["title"], "family": t["family"],
                   "short": t["short"], "url": url(f"topics/{t['id']}/"), "article": t["id"] in articles,
                   "aliases": t["aliases"], "degree": len(t["neighbours"])}
                  for t in taxonomy["topics"].values()],
        "links": [{"source": a, "target": b} for a, b in taxonomy["edges"]],
    }


# ------------------------------------------------------------------ building
def make_env(base: str, config: dict, taxonomy: dict) -> Environment:
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined,
    )
    base = "/" + base.strip("/") + "/" if base.strip("/") else "/"

    def url(path: str = "") -> str:
        """Absolute URL for a site path, respecting the base URL."""
        return base + path.lstrip("/")

    @functools.lru_cache(maxsize=None)
    def asset(path: str) -> str:
        """URL of a static asset with a content hash for cache busting."""
        file = ROOT / "static" / path
        if not file.exists():
            raise BuildError(f"missing static asset: static/{path}")
        digest = hashlib.sha1(file.read_bytes()).hexdigest()[:8]
        return url(f"static/{path}?v={digest}")

    sections = {s["id"]: s for s in config["sections"]}
    env.globals.update(
        site=config["site"],
        nav=config["nav"],
        sections=config["sections"],
        section_by_id=sections,
        taxonomy=taxonomy,
        url=url,
        asset=asset,
        build_date=dt.date.today(),
        build_year=dt.date.today().year,
    )
    return env


WRITTEN: set[Path] = set()      # files produced by the current build


def write(target: Path, data: bytes) -> None:
    """Write only if changed, and remember the file (stale files are removed after the build)."""
    WRITTEN.add(target)
    if target.exists() and target.read_bytes() == data:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def render(env: Environment, template: str, out_path: str, **ctx) -> None:
    write(OUT / out_path, env.get_template(template).render(**ctx).encode("utf-8"))


def copy_static() -> None:
    for src in (ROOT / "static").rglob("*"):
        rel = src.relative_to(ROOT / "static")
        if src.is_file() and not any(p.startswith(("_", ".")) for p in rel.parts):
            write(OUT / "static" / rel, src.read_bytes())


def remove_stale() -> None:
    for f in sorted(OUT.rglob("*"), reverse=True):
        if f.is_file() and f not in WRITTEN:
            f.unlink()
        elif f.is_dir() and not any(f.iterdir()):
            f.rmdir()


def build(base: str | None = None, quiet: bool = False) -> None:
    t0 = time.perf_counter()
    config = load_yaml(ROOT / "config.yaml")
    taxonomy = load_taxonomy(ROOT / "data" / "taxonomy.yaml")
    references = load_yaml(ROOT / "data" / "references.yaml") or {}
    env = make_env(base if base is not None else config["site"]["base_url"], config, taxonomy)
    url = env.globals["url"]
    articles = load_articles(taxonomy, references, url)
    papers = load_papers(ROOT / "data" / "papers")
    stats = yearly_stats(papers)
    env.globals.update(articles=articles, paper_stats=stats, selection=selection,
                       fmt_ref=lambda key: Markup(format_reference(references[key])),
                       references=references)

    # Files are written in place (unchanged files are left alone) and stale ones are
    # removed at the end, so a running dev server never serves a half-empty folder.
    WRITTEN.clear()
    OUT.mkdir(exist_ok=True)
    copy_static()
    write(OUT / ".nojekyll", b"")

    # Pages
    render(env, "pages/home.html", "index.html", page_id="home")
    render(env, "pages/about.html", "about/index.html", page_id="about")
    render(env, "pages/404.html", "404.html", page_id="404")
    for section in config["sections"]:
        template = "pages/section.html" if section["page"] == "placeholder" else f"pages/{section['page']}.html"
        extra = {"graph_json": Markup(json.dumps(map_data(taxonomy, articles, url), ensure_ascii=False)
                                      .replace("</", "<\\/"))} if section["id"] == "map" else {}
        render(env, template, f"{section['id']}/index.html", page_id=section["id"], section=section, **extra)

    # One page per topic (with or without an article yet)
    for family in taxonomy["families"]:
        siblings = family["topics"]
        for i, topic in enumerate(siblings):
            render(env, "pages/topic.html", f"topics/{topic['id']}/index.html", page_id="map",
                   topic=topic, family=family, article=articles.get(topic["id"]),
                   prev_topic=siblings[i - 1] if i > 0 else None,
                   next_topic=siblings[i + 1] if i + 1 < len(siblings) else None)

    remove_stale()
    n = sum(1 for _ in OUT.rglob("*.html"))
    if not quiet:
        print(f"built {n} pages ({len(articles)} articles, {len(references)} references, "
              f"{stats['total']} papers) into {OUT.relative_to(ROOT)}/ in {time.perf_counter() - t0:.2f}s")


# ------------------------------------------------------------------ serving
def snapshot() -> dict[Path, float]:
    files = {}
    for name in WATCHED:
        p = ROOT / name
        if p.is_file():
            files[p] = p.stat().st_mtime
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file():
                    files[f] = f.stat().st_mtime
    return files


def watch(base: str) -> None:
    last = snapshot()
    while True:
        time.sleep(0.8)
        now = snapshot()
        if now != last:
            last = now
            # A fresh process, so edits to build.py / qocsite/ take effect without a restart.
            subprocess.run([sys.executable, str(ROOT / "build.py"), "--base", base or "/"], cwd=ROOT)


def serve(port: int) -> None:
    base = "/"
    build(base)
    threading.Thread(target=watch, args=(base,), daemon=True).start()
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        print(f"serving on http://localhost:{port}/  (rebuilds on change, Ctrl+C to stop)")
        httpd.serve_forever()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", help="base URL path, e.g. QOC for /QOC/ (default: from config.yaml)")
    ap.add_argument("--serve", action="store_true", help="serve locally and rebuild on changes")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    try:
        if args.serve:
            serve(args.port)
        else:
            build(args.base)
    except BuildError as exc:
        sys.exit(f"build error: {exc}")


if __name__ == "__main__":
    main()
