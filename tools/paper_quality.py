"""Measure how good the paper archive is: precision, recall, and context.

Usage
-----
    python tools/paper_quality.py sample --per-year 20 --seed 20261011 > sample.csv   # draw a sample to label
    python tools/paper_quality.py precision data/quality/precision-labels.csv          # precision per year
    python tools/paper_quality.py recall                                                # vs. papers citing core QOC works
    python tools/paper_quality.py share                                                 # QOC papers / all quant-ph per year

Precision: a stratified random sample of archived papers is labelled by hand
    R  about quantum control (methods, theory, protocols, limits, decoupling, shortcuts, feedback, pulses, hardware)
    Q  quantum-speed-limit theory outside a control context (in scope by design)
    X  false positive (control only mentioned in passing, generic "controllability", device demos, ...)
Recall: arXiv papers (2020+) citing core QOC works (GRAPE, CRAB, dCRAB, Krotov, GOAT, reviews), via the
Semantic Scholar API. Citing a core paper does not make a paper a QOC paper, so this is a lower bound; a labelled
sample of the missed papers gives the correction (see data/quality/README.md).
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import glob
import json
import random
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

SEMINAL = {
    "GRAPE (Khaneja 2005)": "10.1016/j.jmr.2004.11.004",
    "CRAB (Caneva 2011)": "10.1103/PhysRevA.84.022326",
    "dCRAB (Rach 2015)": "10.1103/PhysRevA.92.062343",
    "Krotov (Reich 2012)": "10.1063/1.3691827",
    "GOAT (Machnes 2018)": "10.1103/PhysRevLett.120.150401",
    "QOC roadmap (Koch 2022)": "10.1140/epjqt/s40507-022-00138-x",
    "Training Schrödinger's cat (Glaser 2015)": "10.1140/epjd/e2015-60464-1",
    "STA review (Guéry-Odelin 2019)": "10.1103/RevModPhys.91.045001",
}


def archive() -> dict[str, dict]:
    return {p["id"]: p for f in sorted(glob.glob(str(ROOT / "data" / "papers" / "*.json")))
            for p in json.load(open(f, encoding="utf-8"))}


def get_json(url: str):
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "QOC-quality-check"})
            return json.loads(urllib.request.urlopen(req, timeout=90).read())
        except Exception:
            time.sleep(8 * (attempt + 1))
    raise RuntimeError(f"failed: {url}")


def cmd_sample(per_year: int, seed: int) -> None:
    papers = archive()
    rng = random.Random(seed)
    w = csv.writer(sys.stdout)
    w.writerow(["arxiv_id", "year", "label", "title"])
    years = sorted({p["published"][:4] for p in papers.values()})
    for y in years:
        pool = sorted((p for p in papers.values() if p["published"].startswith(y)), key=lambda p: p["id"])
        for p in rng.sample(pool, min(per_year, len(pool))):
            w.writerow([p["id"], y, "", p["title"]])


def cmd_precision(path: str) -> None:
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    papers = archive()
    by_year = collections.defaultdict(collections.Counter)
    for r in rows:
        if r["arxiv_id"] in papers:          # papers removed by a later, stricter rule no longer count
            by_year[r["year"]][r["label"]] += 1
    tot = collections.Counter()
    print("year   n   R   Q   X   precision(R+Q)")
    for y in sorted(by_year):
        c = by_year[y]; n = sum(c.values()); tot += c
        print(f"{y}  {n:3d} {c['R']:3d} {c['Q']:3d} {c['X']:3d}   {(c['R'] + c['Q']) / n:.0%}")
    n = sum(tot.values())
    p = (tot["R"] + tot["Q"]) / n
    se = (p * (1 - p) / n) ** 0.5
    print(f"all   {n:3d} {tot['R']:3d} {tot['Q']:3d} {tot['X']:3d}   {p:.1%} ± {1.96 * se:.1%} (95% CI)")


def cmd_recall() -> None:
    papers = archive()
    ref: dict[str, int] = {}
    for name, doi in SEMINAL.items():
        offset = 0
        while True:
            d = get_json(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}/citations"
                         f"?fields=externalIds,year&limit=1000&offset={offset}")
            for c in d.get("data", []):
                cp = c["citingPaper"]
                ax = (cp.get("externalIds") or {}).get("ArXiv")
                if ax and cp.get("year") and 2020 <= cp["year"] <= dt.date.today().year:
                    ref[ax.split("v")[0]] = cp["year"]
            if not d.get("next") or offset + 1000 >= 9000:
                break
            offset = d["next"]
            time.sleep(3)
        time.sleep(3)
    hits = {i for i in ref if i in papers}
    print(f"reference set: {len(ref)} arXiv papers citing core QOC works; in archive: {len(hits)} "
          f"-> raw recall {len(hits) / len(ref):.1%}")
    by = collections.defaultdict(lambda: [0, 0])
    for i, y in ref.items():
        by[y][0] += 1; by[y][1] += i in hits
    for y in sorted(by):
        print(f"  {y}: {by[y][0]:4d} reference papers, {by[y][1] / by[y][0]:.0%} in archive")


def cmd_share() -> None:
    import fetch_arxiv as fa
    papers = archive()
    counts = collections.Counter(p["published"][:4] for p in papers.values() if "quant-ph" in p["categories"])
    print("year  QOC(quant-ph-listed)  all quant-ph   share")
    for y in sorted(counts):
        q = f"cat:quant-ph AND submittedDate:[{y}01010000 TO {y}12312359]"
        n, _ = fa.parse(_total(fa, q))
        print(f"{y}  {counts[y]:6d}            {n:7d}      {counts[y] / n:.2%}")
        time.sleep(fa.DELAY)


def _total(fa, q: str) -> str:
    import urllib.parse
    url = fa.API + "?" + urllib.parse.urlencode({"search_query": q, "max_results": 1})
    req = urllib.request.Request(url, headers={"User-Agent": fa.UA})
    return urllib.request.urlopen(req, timeout=120).read().decode()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample"); s.add_argument("--per-year", type=int, default=20); s.add_argument("--seed", type=int, default=1)
    p = sub.add_parser("precision"); p.add_argument("labels")
    sub.add_parser("recall")
    sub.add_parser("share")
    a = ap.parse_args()
    if a.cmd == "sample":
        cmd_sample(a.per_year, a.seed)
    elif a.cmd == "precision":
        cmd_precision(a.labels)
    elif a.cmd == "recall":
        cmd_recall()
    else:
        cmd_share()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
