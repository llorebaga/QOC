"""Data for the paper tracker pages: classified papers, author identities, per-topic lists, weekly digests."""
from __future__ import annotations

import datetime as dt
import json
from collections import Counter, defaultdict
from pathlib import Path

from qocsite.authors import build_identities
from qocsite.classify import classify_all


def prepare(papers: list[dict], taxonomy: dict, rules_path: Path, cache_path: Path | None) -> dict:
    topics_of = classify_all(papers, rules_path, cache_path)
    key_of, ids = build_identities(papers)
    order = sorted(papers, key=lambda p: (p["published"], p["id"]), reverse=True)

    records = []
    by_topic: dict[str, list[dict]] = defaultdict(list)
    by_author: dict[str, list[dict]] = defaultdict(list)
    for p in order:
        authors = [(ids[key_of[a]]["name"], ids[key_of[a]]["slug"], a) for a in p["authors"]]
        rec = {
            "id": p["id"], "title": p["title"], "abstract": p["abstract"], "date": p["published"],
            "updated": p.get("updated", p["published"]), "primary": p.get("primary", ""),
            "authors": authors, "topics": [t for t in topics_of[p["id"]] if t in taxonomy["topics"]],
            "doi": p.get("doi"), "journal_ref": p.get("journal_ref"),
        }
        records.append(rec)
        for t in rec["topics"]:
            by_topic[t].append(rec)
        for _, slug, _ in authors:
            by_author[slug].append(rec)

    author_list = sorted(ids.values(), key=lambda a: (-a["count"], a["name"]))
    return {
        "papers": records,
        "by_topic": by_topic,
        "by_author": by_author,
        "authors": author_list,
        "identities": ids,
        "unclassified": sum(1 for r in records if not r["topics"]),
    }


def index_json(data: dict, taxonomy: dict) -> str:
    """Compact index for the client: papers newest first, with author and topic indices (no abstracts)."""
    topic_ids = list(taxonomy["topics"])
    tpos = {t: i for i, t in enumerate(topic_ids)}
    authors: list[list[str]] = []
    apos: dict[str, int] = {}
    rows = []
    for r in data["papers"]:
        ai = []
        for name, slug, _ in r["authors"]:
            if slug not in apos:
                apos[slug] = len(authors)
                authors.append([name, slug])
            ai.append(apos[slug])
        rows.append([r["id"], r["date"], r["title"], ai, [tpos[t] for t in r["topics"]], r["primary"],
                     r["doi"] or "", r["journal_ref"] or ""])
    topics = [[t, taxonomy["topics"][t]["label"], taxonomy["topics"][t]["family"]] for t in topic_ids]
    return json.dumps({"topics": topics, "authors": authors, "papers": rows},
                      ensure_ascii=False, separators=(",", ":"))


def abstracts_json(data: dict) -> dict[int, str]:
    """One JSON file of abstracts per year, loaded by the client only when needed."""
    by_year: dict[int, dict] = defaultdict(dict)
    for r in data["papers"]:
        by_year[int(r["date"][:4])][r["id"]] = r["abstract"]
    return {y: json.dumps(v, ensure_ascii=False, separators=(",", ":")) for y, v in by_year.items()}


def weeks(data: dict, n: int, today: dt.date) -> list[dict]:
    """The last n ISO weeks (Monday-Sunday), newest first, papers grouped by topic family."""
    monday = today - dt.timedelta(days=today.weekday())
    out = []
    for k in range(n):
        start = monday - dt.timedelta(weeks=k)
        end = start + dt.timedelta(days=6)
        items = [r for r in data["papers"] if start.isoformat() <= r["date"] <= end.isoformat()]
        iso = start.isocalendar()
        out.append({"start": start, "end": end, "label": f"{iso[0]}-W{iso[1]:02d}", "papers": items,
                    "current": k == 0, "topics": Counter(t for r in items for t in r["topics"])})
    return out


def prepare_groups(groups: list[dict], data: dict, taxonomy: dict) -> list[dict]:
    """Attach the PIs' author pages, papers and most frequent topics to each research group."""
    from qocsite.authors import identity_key
    ids = data["identities"]
    out = []
    for g in groups:
        pis = []
        papers: dict[str, dict] = {}
        for name in g["pis"]:
            slug, best = None, 0
            for alias in [name] + list(g.get("arxiv_names", {}).get(name, [])):     # every spelling counts
                key = identity_key(alias)
                if key in ids:
                    s = ids[key]["slug"]
                    mine = data["by_author"].get(s, [])
                    for r in mine:
                        papers[r["id"]] = r
                    if len(mine) > best:                 # link the author page with most papers
                        slug, best = s, len(mine)
            pis.append({"name": name, "slug": slug})
        plist = sorted(papers.values(), key=lambda r: (r["date"], r["id"]), reverse=True)
        counts = Counter(t for r in plist for t in r["topics"])
        topics = [t for t, n in counts.most_common() if n >= 2][:8]
        platforms = [t for t in topics if taxonomy["topics"][t]["family"] == "platforms"]
        out.append({**g, "pi_links": pis, "papers": plist, "topic_counts": counts, "topics": topics,
                    "platforms": platforms})
    return out
