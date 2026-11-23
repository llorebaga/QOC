#!/usr/bin/env python3
"""Editorial status & coverage report for QOC.

Usage:
    python3 tools/status.py          # human-readable summary
    python3 tools/status.py --json   # machine-readable JSON output
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build as site_build  # noqa: E402
from qocsite import tracker as paper_tracker  # noqa: E402
from qocsite.papers import load_papers  # noqa: E402


def collect() -> dict:
    taxonomy = site_build.load_taxonomy(ROOT / "data" / "taxonomy.yaml")
    references = site_build.load_yaml(ROOT / "data" / "references.yaml") or {}
    url = lambda p="": "/" + p.lstrip("/")
    articles = site_build.load_articles(taxonomy, references, url)
    problems = site_build.load_problems(taxonomy, references, url)
    resources = site_build.load_resources(ROOT / "data" / "resources.yaml", taxonomy, references, url)
    hamiltonians = site_build.load_hamiltonians(ROOT / "data" / "hamiltonians.yaml", taxonomy, references, url)
    papers = load_papers(ROOT / "data" / "papers")
    tracked = paper_tracker.prepare(papers, taxonomy, ROOT / "data" / "classifier.yaml", ROOT / ".cache" / "topics.json")
    groups = paper_tracker.prepare_groups(site_build.load_groups(ROOT / "data" / "groups.yaml", taxonomy), tracked, taxonomy)

    # Topic coverage
    groups_by_topic: dict[str, int] = Counter(t for g in groups for t in g["topics"])
    problems_by_topic: dict[str, int] = Counter(t for pr in problems for t in pr["topics"])

    art_review = Counter(a.meta.get("status", "draft") for a in articles.values())
    prob_review = Counter(pr["review"] for pr in problems)
    prob_status = Counter(pr["status"] for pr in problems)
    demos = sorted(tid for tid, a in articles.items() if a.meta.get("demo"))

    # Reference usage across articles, problems, hamiltonians and resources
    used_refs: set[str] = set()
    for a in articles.values():
        used_refs.update(a.citations)
        used_refs.update(kp["key"] for kp in a.meta.get("key_papers", []))
    for pr in problems:
        used_refs.update(pr["refs"])
    for h in hamiltonians:
        used_refs.update(h["refs"])
    for grp in resources.get("software", []):
        for s in grp["items"]:
            used_refs.update(s.get("refs") or [])
    for grp in resources.get("reading", []):
        for r in grp["items"]:
            used_refs.add(r["key"])
    for e in resources.get("timeline", []):
        used_refs.update(e.get("refs") or [])
    unused_refs = sorted(set(references) - used_refs)

    topics_without_groups = sorted(tid for tid in taxonomy["topics"] if groups_by_topic[tid] == 0)
    topics_without_problems = sorted(tid for tid in taxonomy["topics"] if problems_by_topic[tid] == 0)
    shortest_articles = sorted(
        ((a.word_count, tid) for tid, a in articles.items()),
    )[:5]

    return {
        "articles": {
            "total": len(articles),
            "topics_total": len(taxonomy["topics"]),
            "review": dict(art_review),
            "total_words": sum(a.word_count for a in articles.values()),
            "avg_words": round(sum(a.word_count for a in articles.values()) / max(1, len(articles))),
            "with_demo": demos,
            "shortest": [{"topic": tid, "words": w} for w, tid in shortest_articles],
        },
        "problems": {
            "total": len(problems),
            "status": dict(prob_status),
            "review": dict(prob_review),
            "topics_covered": len(problems_by_topic),
        },
        "hamiltonians": {
            "total": len(hamiltonians),
            "architectures": len({h["architecture"] for h in hamiltonians}),
        },
        "groups": {
            "total": len(groups),
            "countries": len({g["country"] for g in groups}),
            "topics_covered": len(groups_by_topic),
            "topics_without_groups": topics_without_groups,
        },
        "resources": {
            "software": sum(len(g["items"]) for g in resources.get("software", [])),
            "reading": sum(len(g["items"]) for g in resources.get("reading", [])),
            "glossary": len(resources.get("glossary", [])),
            "timeline": len(resources.get("timeline", [])),
        },
        "papers": {"total": len(tracked["papers"]), "authors": len(tracked["authors"])},
        "references": {
            "total": len(references),
            "used": len(used_refs),
            "unused_count": len(unused_refs),
            "unused": unused_refs,
        },
        "topics_without_problems_count": len(topics_without_problems),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="output JSON")
    args = ap.parse_args()
    data = collect()
    if args.json:
        print(json.dumps(data, indent=2))
        return

    a, p, h, g, r, refs = (
        data["articles"], data["problems"], data["hamiltonians"], data["groups"], data["resources"], data["references"]
    )
    print("QOC editorial & coverage status")
    print("=" * 48)
    print(f"Articles      : {a['total']}/{a['topics_total']} topics | review={a['review']} | "
          f"avg {a['avg_words']} words ({a['total_words']:,} total)")
    print(f"  Interactive : {len(a['with_demo'])} topics ({', '.join(a['with_demo'])})")
    print(f"  Shortest    : " + ", ".join(f"{x['topic']} ({x['words']}w)" for x in a["shortest"]))
    print(f"Open problems : {p['total']} | status={p['status']} | review={p['review']} | "
          f"{p['topics_covered']}/{a['topics_total']} topics covered")
    print(f"Hamiltonians  : {h['total']} models across {h['architectures']} architectures")
    print(f"Groups        : {g['total']} in {g['countries']} countries | "
          f"{g['topics_covered']}/{a['topics_total']} topics covered")
    if g["topics_without_groups"]:
        print(f"  No groups   : {', '.join(g['topics_without_groups'])}")
    print(f"Resources     : {r['software']} software, {r['reading']} reading, "
          f"{r['glossary']} glossary, {r['timeline']} timeline")
    print(f"Papers        : {data['papers']['total']:,} tracked ({data['papers']['authors']:,} authors)")
    print(f"References    : {refs['total']} total ({refs['used']} cited, {refs['unused_count']} unused)")


if __name__ == "__main__":
    main()
