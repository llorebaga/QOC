"""Harvest quantum-control papers from arXiv into data/papers/<year>.json.

Usage
-----
    python tools/fetch_arxiv.py --since 2010-01-01     # full harvest (month by month)
    python tools/fetch_arxiv.py --since 2010-01-01 --until 2019-12-31   # back-fill a period
    python tools/fetch_arxiv.py --days 10              # daily update: last 10 days (overlap is safe)

How a paper is selected
-----------------------
The definition lives in qocsite/selection.py (shared with the website, which
shows it on the About page). The arXiv API is only used as a pre-filter: one query per category of the form
    cat:X AND (abs:"t1" OR abs:"t2" ...) AND submittedDate:[...]
which returns a superset of the matches (validated against a full download of
all quant-ph papers of September 2026: 0 of 75 matches missed). The exact
selection is then made locally by `selected()`.

The same definition produces the papers-per-year chart, so the chart and the
tracker always agree.

Storage
-------
One JSON file per year (by date of first submission), one paper per line,
sorted by id — small, stable diffs in git.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "papers"
API = "https://export.arxiv.org/api/query"
UA = "QOC-paper-tracker/1.0 (https://github.com/llorebaga/QOC)"
PAGE = 1000
DELAY = 3.2                     # arXiv asks for >= 3 s between requests

sys.path.insert(0, str(ROOT))
from qocsite.selection import CATEGORIES, NEIGHBOURS, TERMS, selected  # noqa: E402  (the shared definition)


def build_query(category: str, start: dt.date, end: dt.date) -> str:
    # Keep this exact shape: more deeply nested queries are mis-parsed by the API.
    # title and abstract: a phrase may appear only in the title
    terms = " OR ".join(f'abs:"{t}" OR ti:"{t}"' for t in TERMS)
    return f"cat:{category} AND ({terms}) AND submittedDate:[{start:%Y%m%d}0000 TO {end:%Y%m%d}2359]"


# ------------------------------------------------------------------ API
def clean(s: str) -> str:
    return " ".join(html.unescape(s).split())


def parse(feed: str) -> tuple[int, list[dict]]:
    total = int(re.search(r"<opensearch:totalResults[^>]*>(\d+)<", feed).group(1))
    papers = []
    for e in feed.split("<entry>")[1:]:
        g = lambda tag: re.search(rf"<{tag}>(.*?)</{tag}>", e, re.S)
        full_id = re.search(r"<id>https?://arxiv.org/abs/(.*?)</id>", e).group(1)
        doi = re.search(r"<arxiv:doi[^>]*>(.*?)</arxiv:doi>", e)
        jref = re.search(r"<arxiv:journal_ref[^>]*>(.*?)</arxiv:journal_ref>", e, re.S)
        papers.append({
            "id": re.sub(r"v\d+$", "", full_id),
            "v": int(re.search(r"v(\d+)$", full_id).group(1)) if re.search(r"v\d+$", full_id) else 1,
            "title": clean(g("title").group(1)),
            "authors": [clean(a) for a in re.findall(r"<name>(.*?)</name>", e)],
            "abstract": clean(g("summary").group(1)),
            "published": g("published").group(1)[:10],
            "updated": g("updated").group(1)[:10],
            "primary": re.search(r'<arxiv:primary_category[^>]*term="([^"]+)"', e).group(1),
            "categories": re.findall(r'<category[^>]*term="([^"]+)"', e),
            **({"doi": doi.group(1).strip()} if doi else {}),
            **({"journal_ref": clean(jref.group(1))} if jref else {}),
        })
    return total, papers


def request(query: str, start: int) -> str:
    params = {"search_query": query, "start": start, "max_results": PAGE,
              "sortBy": "submittedDate", "sortOrder": "ascending"}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers={"User-Agent": UA})
    wait = 15
    for attempt in range(9):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            # 429/503: rate limited — honour Retry-After, otherwise back off exponentially
            retry_after = exc.headers.get("Retry-After") if exc.headers else None
            delay = int(retry_after) if retry_after and retry_after.isdigit() else wait
            print(f"    HTTP {exc.code}; retrying in {delay}s", file=sys.stderr)
            time.sleep(delay)
        except Exception as exc:  # network errors
            print(f"    request failed ({exc}); retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)
        wait = min(wait * 2, 600)
    raise RuntimeError("arXiv API unreachable after repeated retries")


def fetch_window(start: dt.date, end: dt.date) -> list[dict]:
    """Candidate papers submitted in [start, end] from all categories (deduplicated)."""
    got: dict[str, dict] = {}
    for cat in CATEGORIES + NEIGHBOURS:
        for p in fetch_query(build_query(cat, start, end)):
            got[p["id"]] = p
    return list(got.values())


def fetch_query(query: str) -> list[dict]:
    """All results of one query, verified against totalResults."""
    got: dict[str, dict] = {}
    offset, total = 0, None
    while total is None or offset < total:
        for attempt in range(4):           # the API occasionally returns an empty page
            n, papers = parse(request(query, offset))
            time.sleep(DELAY)
            if papers or n == 0 or offset >= n:
                break
            print(f"    empty page at {offset}/{n}, retrying", file=sys.stderr)
        total = n
        if not papers:
            break
        for p in papers:
            got[p["id"]] = p
        offset += len(papers)
    if total and len(got) < total:
        print(f"    ! got {len(got)} of {total} for {query[:40]}...", file=sys.stderr)
    return list(got.values())


# ------------------------------------------------------------------ storage
def load_year(year: int) -> dict[str, dict]:
    f = OUT / f"{year}.json"
    if not f.exists():
        return {}
    return {p["id"]: p for p in json.loads(f.read_text(encoding="utf-8"))}


def save_year(year: int, papers: dict[str, dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [json.dumps(papers[k], ensure_ascii=False, separators=(",", ":")) for k in sorted(papers)]
    (OUT / f"{year}.json").write_text("[\n" + ",\n".join(rows) + "\n]\n", encoding="utf-8", newline="\n")


def merge(papers: list[dict]) -> tuple[int, int]:
    by_year: dict[int, list[dict]] = {}
    for p in papers:
        if selected(p):
            by_year.setdefault(int(p["published"][:4]), []).append(p)
    added = updated = 0
    for year, items in by_year.items():
        store = load_year(year)
        for p in items:
            old = store.get(p["id"])
            if old is None:
                added += 1
            elif old != p:
                updated += 1
            store[p["id"]] = p
        save_year(year, store)
    return added, updated


def months(since: dt.date, until: dt.date):
    cur = since.replace(day=1)
    while cur <= until:
        nxt = (cur.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        yield max(cur, since), min(nxt - dt.timedelta(days=1), until)
        cur = nxt


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--since", type=dt.date.fromisoformat, help="harvest from this date (YYYY-MM-DD) to today")
    ap.add_argument("--until", type=dt.date.fromisoformat, help="with --since: stop at this date instead of today")
    g.add_argument("--days", type=int, help="fetch the last N days")
    g.add_argument("--reselect", action="store_true",
                   help="re-apply the selection rule to the stored archive (after tightening it; no API calls)")
    g.add_argument("--totals", action="store_true",
                   help="refresh the number of all quant-ph papers for every archived year (context for the chart)")
    args = ap.parse_args()

    if args.totals:
        update_totals(sorted(int(f.stem) for f in OUT.glob("*.json")))
        return

    if args.reselect:
        removed = 0
        for f in sorted(OUT.glob("*.json")):
            year = int(f.stem)
            store = load_year(year)
            keep = {k: p for k, p in store.items() if selected(p)}
            removed += len(store) - len(keep)
            save_year(year, keep)
            print(f"{year}: {len(store)} -> {len(keep)}")
        print(f"removed {removed} papers that no longer satisfy the selection rule")
        return

    today = dt.datetime.now(dt.timezone.utc).date()
    since = args.since or today - dt.timedelta(days=args.days)
    until = min(args.until, today) if args.until and args.since else today
    total_added = total_updated = 0
    for a, b in months(since, until):
        papers = fetch_window(a, b)
        added, updated = merge(papers)
        total_added += added
        total_updated += updated
        kept = sum(map(selected, papers))
        print(f"{a} .. {b}: {len(papers):4d} candidates, {kept:4d} selected, {added:4d} new, {updated:4d} updated",
              flush=True)
    print(f"done: {total_added} new, {total_updated} updated")
    update_totals(sorted(set(range(since.year, until.year + 1)) | {today.year}))


TOTALS = ROOT / "data" / "quality" / "quantph-totals.json"


def update_totals(years: list[int]) -> None:
    """Record the number of all quant-ph submissions per year (incl. cross-lists), for the share shown on the site."""
    totals = json.loads(TOTALS.read_text(encoding="utf-8")) if TOTALS.exists() else {}
    for y in years:
        query = f"cat:quant-ph AND submittedDate:[{y}01010000 TO {y}12312359]"
        params = {"search_query": query, "start": 0, "max_results": 1}
        req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            n, _ = parse(r.read().decode("utf-8"))
        totals[str(y)] = n
        print(f"quant-ph total {y}: {n}")
        time.sleep(DELAY)
    TOTALS.parent.mkdir(parents=True, exist_ok=True)
    TOTALS.write_text(json.dumps(dict(sorted(totals.items())), indent=1) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
