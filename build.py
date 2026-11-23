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
import html
import http.server
import subprocess
import sys
import threading
import time
from pathlib import Path

import json
import re

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from markupsafe import Markup

from qocsite.content import ContentError, format_reference, render_article
from qocsite import selection
from qocsite.papers import load_papers, yearly_stats
from qocsite import tracker as paper_tracker
from qocsite.classify import load_rules

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


PROBLEM_STATUS = {"open": "Open", "partial": "Partial progress", "solved": "Solved"}
PROBLEM_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_problems(taxonomy: dict, references: dict, url) -> list[dict]:
    """Render content/problems/<id>.md and validate the front matter (see README)."""
    problems, errors = [], []
    for f in sorted((ROOT / "content" / "problems").glob("*.md")):
        pid = f.stem
        try:
            art = render_article(pid, f.read_text(encoding="utf-8"), references=references,
                                 topics=taxonomy["topics"], url=url)
        except ContentError as exc:
            raise BuildError(str(exc)) from exc
        m = art.meta
        where = f"content/problems/{f.name}"
        if not PROBLEM_ID.match(pid):
            errors.append(f"{where}: bad id (use lowercase words joined by '-')")
        for k in ("title", "question", "status", "topics", "posed_by", "added"):
            if not m.get(k):
                errors.append(f"{where}: missing {k}")
        if m.get("status") not in PROBLEM_STATUS:
            errors.append(f"{where}: status must be one of {', '.join(PROBLEM_STATUS)}")
        if m.get("review", "draft") not in ("draft", "reviewed"):
            errors.append(f"{where}: review must be draft or reviewed")
        for t in m.get("topics") or []:
            if t not in taxonomy["topics"]:
                errors.append(f"{where}: unknown topic '{t}'")
        for p in m.get("posed_by") or []:
            if p.get("key") not in references:
                errors.append(f"{where}: posed_by has unknown key '{p.get('key')}'")
        if errors:
            continue
        # The question and the notes on sources are short Markdown with math, rendered without the outer <p>.
        def inline(text: str) -> Markup:
            out = render_article(pid, text, references=references, topics=taxonomy["topics"], url=url).html
            return Markup(re.sub(r"^<p>(.*)</p>$", r"\1", out.strip(), flags=re.S))

        posed_by = [{"key": p["key"], "where": inline(p.get("where", ""))} for p in m["posed_by"]]
        # Every source that poses the problem is listed with the references, after the cited ones.
        refs = art.citations + [p["key"] for p in posed_by if p["key"] not in art.citations]
        problems.append({"id": pid, "title": m["title"], "question": inline(m["question"]), "status": m["status"],
                         "status_label": PROBLEM_STATUS[m["status"]], "topics": m["topics"],
                         "posed_by": posed_by, "added": m["added"], "updated": m.get("updated", m["added"]),
                         "review": m.get("review", "draft"), "article": art, "refs": refs})
    if errors:
        raise BuildError("open problems:\n  " + "\n  ".join(errors))
    order = list(PROBLEM_STATUS)
    return sorted(problems, key=lambda p: (order.index(p["status"]), p["title"].lower()))


def load_resources(path: Path, taxonomy: dict, references: dict, url) -> dict:
    """Load data/resources.yaml: check every reference key and topic id, render the text fields."""
    if not path.exists():
        return {}
    res = load_yaml(path) or {}
    errors = []

    def inline(text: str, where: str) -> Markup:
        try:
            out = render_article(where, text or "", references=references, topics=taxonomy["topics"], url=url).html
        except ContentError as exc:
            errors.append(str(exc))
            return Markup("")
        return Markup(re.sub(r"^<p>(.*)</p>$", r"\1", out.strip(), flags=re.S))

    def check(item: dict, where: str) -> None:
        for t in item.get("topics", []) or []:
            if t not in taxonomy["topics"]:
                errors.append(f"{where}: unknown topic '{t}'")
        for k in ([item["key"]] if "key" in item else []) + (item.get("refs") or []):
            if k not in references:
                errors.append(f"{where}: unknown reference key '{k}'")

    seen_sw: set[str] = set()
    for g in res.get("software", []):
        for s in g["items"]:
            check(s, f"software '{s['name']}'")
            if not str(s.get("url", "")).startswith("https://"):
                errors.append(f"software '{s['name']}': url must be https")
            base_id = "sw-" + re.sub(r"[^a-z0-9]+", "-", s["name"].lower()).strip("-")
            sid = base_id
            n = 2
            while sid in seen_sw:
                sid = f"{base_id}-{n}"
                n += 1
            seen_sw.add(sid)
            s["id"] = sid
            s["what_html"] = inline(s.get("what", ""), "resources")
    for g in res.get("reading", []):
        for r in g["items"]:
            check(r, f"reading '{r.get('key')}'")
            r["note_html"] = inline(r.get("note", ""), "resources")
    for e in res.get("glossary", []):
        check(e, f"glossary '{e['term']}'")
        e["id"] = re.sub(r"[^a-z0-9]+", "-", e["term"].lower()).strip("-")
        e["def_html"] = inline(e["def"], "resources")
    res["glossary"] = sorted(res.get("glossary", []), key=lambda e: e["term"].lower())
    for e in res.get("timeline", []):
        check(e, f"timeline {e['year']}")
        e["text_html"] = inline(e["text"], "resources")
    seen_bench: set[str] = set()
    for b in res.get("benchmarks", []):
        check(b, f"benchmark '{b['name']}'")
        base_id = "bench-" + re.sub(r"[^a-z0-9]+", "-", b["name"].lower()).strip("-")
        bid = base_id
        n = 2
        while bid in seen_bench:
            bid = f"{base_id}-{n}"
            n += 1
        seen_bench.add(bid)
        b["id"] = bid
        b["model_html"] = inline(b.get("model", ""), "resources")
        b["target_html"] = inline(b.get("target", ""), "resources")
    if errors:
        raise BuildError("resources.yaml:\n  " + "\n  ".join(errors))
    return res


def load_groups(path: Path, taxonomy: dict) -> list[dict]:
    """Load and validate data/groups.yaml (maintained with tools/groups.py)."""
    if not path.exists():
        return []
    groups = load_yaml(path) or []
    errors, seen = [], set()
    for g in groups:
        gid = g.get("id", "?")
        for k in ("id", "name", "pis", "institution", "wikidata", "website", "country", "lat", "lon"):
            if g.get(k) in (None, "", []):
                errors.append(f"group '{gid}': missing {k}")
        if gid in seen:
            errors.append(f"duplicate group id '{gid}'")
        seen.add(gid)
    if errors:
        raise BuildError("groups.yaml (see tools/groups.py):\n  " + "\n  ".join(errors))
    return groups


def groups_data(groups: list[dict], taxonomy: dict, url) -> list[dict]:
    """Compact group records for the map script."""
    return [{"id": g["id"], "name": g["name"], "pis": g["pis"], "institution": g["institution"],
             "place": ", ".join(x for x in (g.get("city"), g["country"]) if x), "lat": g["lat"], "lon": g["lon"],
             "topics": g["topics"], "platforms": g["platforms"],
             "url": url(f"groups/{g['id']}/"),
             "labels": [taxonomy["topics"][t]["label"] for t in g["topics"][:4]]} for g in groups]


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


def _plain(text: str, limit: int = 180) -> str:
    """Strip HTML tags and math delimiters for compact search snippets."""
    s = html.unescape(re.sub(r"<[^>]+>", " ", str(text or "")))
    s = re.sub(r"\\\(|\\\)|\$\$", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return (s[: limit - 1].rstrip() + "…") if len(s) > limit else s


def related_problems_for(pr: dict, problems: list[dict], limit: int = 6) -> tuple[list[dict], bool]:
    """Return up to `limit` other problems, prioritizing shared topics; flag indicates whether any share a topic."""
    mine = set(pr["topics"])
    order = list(PROBLEM_STATUS)
    others = [o for o in problems if o["id"] != pr["id"]]
    scored = sorted(
        others,
        key=lambda o: (-len(mine & set(o["topics"])), order.index(o["status"]), o["title"].lower()),
    )
    has_shared = bool(scored and (mine & set(scored[0]["topics"])))
    return scored[:limit], has_shared


def search_index_data(taxonomy: dict, problems: list[dict], groups: list[dict],
                      resources: dict, references: dict, url) -> list[dict]:
    """Compact site-wide search index covering topics, open problems, groups and resources."""
    items: list[dict] = []
    fam_by_id = {f["id"]: f["title"] for f in taxonomy["families"]}
    tlabel = lambda tid: taxonomy["topics"][tid]["label"]

    for t in taxonomy["topics"].values():
        items.append({
            "k": "topic",
            "t": t["title"],
            "s": t["short"],
            "m": " ".join([fam_by_id[t["family"]], t["label"], *t["aliases"]]),
            "u": url(f"topics/{t['id']}/"),
        })
    for pr in problems:
        items.append({
            "k": "problem",
            "t": pr["title"],
            "s": f"{pr['status_label']} · {_plain(pr['question'], 150)}",
            "m": " ".join([pr["status_label"], *(tlabel(t) for t in pr["topics"])]),
            "u": url(f"open-problems/{pr['id']}/"),
        })
    for g in sorted(groups, key=lambda x: x["name"].lower()):
        place = ", ".join(x for x in (g.get("city"), g["country"]) if x)
        items.append({
            "k": "group",
            "t": g["name"],
            "s": f"{', '.join(g['pis'])} · {g['institution']}, {place}",
            "m": " ".join(tlabel(t) for t in g["topics"]),
            "u": url(f"groups/{g['id']}/"),
        })
    for e in resources.get("glossary", []):
        items.append({
            "k": "glossary",
            "t": e["term"],
            "s": _plain(e["def_html"], 160),
            "m": " ".join(tlabel(t) for t in (e.get("topics") or [])),
            "u": url(f"resources/#g-{e['id']}"),
        })
    for b in resources.get("benchmarks", []):
        items.append({
            "k": "benchmark",
            "t": b["name"],
            "s": f"{b['platform']} · {_plain(b['target_html'], 140)}",
            "m": " ".join([b["platform"], *(tlabel(t) for t in (b.get("topics") or []))]),
            "u": url(f"resources/#{b['id']}"),
        })
    for grp in resources.get("software", []):
        for s in grp["items"]:
            items.append({
                "k": "software",
                "t": s["name"],
                "s": f"{s['lang']} · {_plain(s['what_html'], 140)}",
                "m": " ".join([grp["group"], *(tlabel(t) for t in (s.get("topics") or []))]),
                "u": url(f"resources/#{s['id']}"),
            })
    for grp in resources.get("reading", []):
        for r in grp["items"]:
            ref = references[r["key"]]
            authors = ", ".join(ref.get("authors", [])[:3])
            year = ref.get("year", "")
            note = _plain(r.get("note_html", ""), 120)
            items.append({
                "k": "reading",
                "t": ref.get("title", ""),
                "s": f"{authors} ({year})" + (f" · {note}" if note else ""),
                "m": " ".join([grp["group"], *ref.get("authors", []), *(tlabel(t) for t in (r.get("topics") or []))]),
                "u": url("resources/#reading"),
            })
    return items


def trends_data(tracked: dict, taxonomy: dict, stats: dict, url) -> dict:
    """Annual paper counts per topic for the interactive /papers/trends/ page."""
    first_year = stats["first_year"]
    last_year = max((int(p["date"][:4]) for p in tracked["papers"]), default=dt.date.today().year)
    years = list(range(first_year, last_year + 1))
    yidx = {y: i for i, y in enumerate(years)}
    totals = [0] * len(years)
    by_topic_counts: dict[str, list[int]] = {tid: [0] * len(years) for tid in taxonomy["topics"]}
    for p in tracked["papers"]:
        yi = yidx.get(int(p["date"][:4]))
        if yi is None:
            continue
        totals[yi] += 1
        for tid in p["topics"]:
            by_topic_counts[tid][yi] += 1

    # Compare the last 5 complete years with the 5 years before them
    complete_end = len(years) - 1  # exclude partial last_year
    rec_slice = slice(max(0, complete_end - 5), complete_end)
    prev_slice = slice(max(0, complete_end - 10), max(0, complete_end - 5))
    recent_label = f"{years[rec_slice.start]}–{years[rec_slice.stop - 1]}" if complete_end > 0 else str(last_year)

    fam_by_id = {f["id"]: f["title"] for f in taxonomy["families"]}
    topics = []
    for tid, t in taxonomy["topics"].items():
        c = by_topic_counts[tid]
        recent = sum(c[rec_slice])
        prev = sum(c[prev_slice])
        growth = (recent - prev) / prev if prev >= 5 else None
        topics.append({
            "id": tid,
            "label": t["label"],
            "title": t["title"],
            "family": t["family"],
            "family_title": fam_by_id[t["family"]],
            "counts": c,
            "total": sum(c),
            "recent": recent,
            "growth": round(growth, 3) if growth is not None else None,
            "url": url(f"topics/{tid}/"),
            "papers_url": url(f"papers/?topic={tid}"),
        })
    return {
        "years": years,
        "partial_year": last_year,
        "recent_label": recent_label,
        "totals": totals,
        "topics": topics,
    }


# ------------------------------------------------------------------ building
def make_env(base: str, config: dict, taxonomy: dict) -> Environment:
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=select_autoescape(["html", "xml"]),
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


PAGES: list[str] = []           # site paths of the HTML pages of the current build (for the sitemap)


def render(env: Environment, template: str, out_path: str, **ctx) -> None:
    if out_path.endswith(".html"):
        ctx.setdefault("page_path", out_path.removesuffix("index.html"))
        if ctx.get("page_id") != "404":
            PAGES.append(ctx["page_path"])
    write(OUT / out_path, env.get_template(template).render(**ctx).encode("utf-8"))


def write_sitemap(env: Environment) -> None:
    root = env.globals["site"]["url"].rstrip("/")
    locs = [f"  <url><loc>{root}{env.globals['url'](p)}</loc></url>" for p in sorted(PAGES)]
    lines = ['<?xml version="1.0" encoding="utf-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', *locs, "</urlset>", ""]
    write(OUT / "sitemap.xml", "\n".join(lines).encode("utf-8"))


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
    problems = load_problems(taxonomy, references, url)
    problems_by_topic: dict[str, list[dict]] = {}
    for pr in problems:
        for t in pr["topics"]:
            problems_by_topic.setdefault(t, []).append(pr)
    papers = load_papers(ROOT / "data" / "papers")
    totals_file = ROOT / "data" / "quality" / "quantph-totals.json"
    totals = json.loads(totals_file.read_text(encoding="utf-8")) if totals_file.exists() else None
    stats = yearly_stats(papers, quantph_totals=totals)
    rules_file = ROOT / "data" / "classifier.yaml"
    try:
        load_rules(rules_file, set(taxonomy["topics"]))          # validates topic ids
    except ValueError as exc:
        raise BuildError(str(exc)) from exc
    tracked = paper_tracker.prepare(papers, taxonomy, rules_file, ROOT / ".cache" / "topics.json")
    groups = paper_tracker.prepare_groups(load_groups(ROOT / "data" / "groups.yaml", taxonomy), tracked, taxonomy)
    groups_by_topic: dict[str, list[dict]] = {}
    for g in groups:
        for t in g["topics"]:
            groups_by_topic.setdefault(t, []).append(g)
    for t, glist in groups_by_topic.items():
        glist.sort(key=lambda g: (-g["topic_counts"].get(t, 0), g["name"].lower()))
    resources = load_resources(ROOT / "data" / "resources.yaml", taxonomy, references, url)
    quality_file = ROOT / "data" / "quality" / "summary.yaml"
    quality = load_yaml(quality_file) if quality_file.exists() else None
    env.globals.update(articles=articles, problems=problems, problems_by_topic=problems_by_topic,
                       groups_by_topic=groups_by_topic,
                       paper_stats=stats, selection=selection, quality=quality, tracked=tracked,
                       fmt_ref=lambda key: Markup(format_reference(references[key])),
                       references=references)

    # Files are written in place (unchanged files are left alone) and stale ones are
    # removed at the end, so a running dev server never serves a half-empty folder.
    WRITTEN.clear()
    PAGES.clear()
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
        if section["id"] == "resources":
            extra = {"res": resources}
        if section["id"] == "groups":
            extra = {"groups": groups,
                     "groups_json": Markup(json.dumps(groups_data(groups, taxonomy, url), ensure_ascii=False)
                                           .replace("</", "<\\/")),
                     "topic_options": sorted({t for g in groups for t in g["topics"]}),
                     "platform_options": sorted({t for g in groups for t in g["platforms"]})}
        render(env, template, f"{section['id']}/index.html", page_id=section["id"], section=section, **extra)

    # One page per topic (with or without an article yet), with its recent papers and a feed
    for family in taxonomy["families"]:
        siblings = family["topics"]
        for i, topic in enumerate(siblings):
            topic_papers = tracked["by_topic"].get(topic["id"], [])
            render(env, "pages/topic.html", f"topics/{topic['id']}/index.html", page_id="map",
                   topic=topic, family=family, article=articles.get(topic["id"]),
                   topic_papers=topic_papers,
                   prev_topic=siblings[i - 1] if i > 0 else None,
                   next_topic=siblings[i + 1] if i + 1 < len(siblings) else None)
            render(env, "feeds/atom.xml", f"topics/{topic['id']}/feed.xml", feed_title=f"QOC — {topic['title']}",
                   feed_id=f"topics/{topic['id']}/", feed_page=f"topics/{topic['id']}/", entries=topic_papers[:30])

    # Open problems: one page each + Atom feed (the list is on the section page)
    for pr in problems:
        related_problems, has_shared_problems = related_problems_for(pr, problems)
        render(env, "pages/problem.html", f"open-problems/{pr['id']}/index.html", page_id="open-problems", pr=pr,
               related_problems=related_problems, has_shared_problems=has_shared_problems)
    problem_feed_entries = sorted(problems, key=lambda p: (str(p["updated"]), str(p["added"]), p["id"]), reverse=True)
    render(env, "feeds/problems.xml", "open-problems/feed.xml", entries=problem_feed_entries)

    # Research groups: one page each (the map and the list are on the section page)
    for g in groups:
        render(env, "pages/group.html", f"groups/{g['id']}/index.html", page_id="groups", g=g)

    # Site-wide search index (loaded on demand when opening search)
    write(OUT / "search-index.json",
          json.dumps(search_index_data(taxonomy, problems, groups, resources, references, url),
                     ensure_ascii=False, separators=(",", ":")).encode("utf-8"))

    # Paper tracker: data for the client, author pages, weekly digest, feed
    write(OUT / "papers" / "data" / "index.json", paper_tracker.index_json(tracked, taxonomy).encode("utf-8"))
    for year, blob in paper_tracker.abstracts_json(tracked).items():
        write(OUT / "papers" / "data" / f"abstracts-{year}.json", blob.encode("utf-8"))
    render(env, "pages/authors.html", "papers/authors/index.html", page_id="papers",
           top_authors=[a for a in tracked["authors"] if a["count"] >= 8])
    render(env, "pages/weekly.html", "papers/weekly/index.html", page_id="papers",
           weeks=paper_tracker.weeks(tracked, 4, dt.date.today()))
    trends = trends_data(tracked, taxonomy, stats, url)
    render(env, "pages/trends.html", "papers/trends/index.html", page_id="papers",
           trends_partial_year=trends["partial_year"], trends_recent_label=trends["recent_label"],
           trends_json=Markup(json.dumps(trends, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")))
    render(env, "feeds/atom.xml", "papers/feed.xml", feed_title="QOC — new quantum control papers",
           feed_id="papers/", feed_page="papers/", entries=tracked["papers"][:50])

    write_sitemap(env)
    remove_stale()
    n = sum(1 for _ in OUT.rglob("*.html"))
    if not quiet:
        print(f"built {n} pages ({len(articles)} articles, {len(problems)} problems, {len(references)} references, "
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
