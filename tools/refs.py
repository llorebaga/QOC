"""Manage the bibliography in data/references.yaml.

Every entry is created from authoritative metadata (Crossref for DOIs, the
arXiv API for preprints), never typed by hand, so titles, author lists, venues
and identifiers are exact.

Usage
-----
    python tools/refs.py add KEY --doi 10.1103/PhysRevLett.106.190501
    python tools/refs.py add KEY --arxiv 1003.3750
    python tools/refs.py add KEY --arxiv 2209.05790 --doi 10.1103/g4fb-xm13
    python tools/refs.py show KEY
    python tools/refs.py check            # offline: schema + duplicates
    python tools/refs.py check --online   # also re-verify every DOI / arXiv id

When both --doi and --arxiv are given, the journal metadata comes from Crossref
and the arXiv id is cross-checked against the title. With only --arxiv, a DOI
listed by arXiv (published version) is followed automatically.

Keys: lowercase `firstauthorYEARword`, e.g. `khaneja2005grape`.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "data" / "references.yaml"
UA = "QOC-bibliography/1.0 (https://github.com/llorebaga/QOC)"
KEY_RE = re.compile(r"^[a-z][a-z0-9-]*\d{4}[a-z0-9-]*$")

HEADER = """\
# QOC bibliography — one entry per work, cited from articles as [@key].
#
# Entries are generated with tools/refs.py from Crossref / arXiv metadata.
# Do not hand-edit bibliographic fields; you may add or edit `note` (a short
# description of why the work matters, shown in "Key papers" lists).
"""


# ------------------------------------------------------------------ fetching
def http_get(url: str, accept: str = "application/json") -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as exc:  # network hiccups, rate limits
            if attempt == 3:
                raise
            time.sleep(3 * (attempt + 1))
    raise RuntimeError("unreachable")


def clean(s: str) -> str:
    s = html.unescape(re.sub(r"<[^>]+>", "", s))   # Crossref titles may contain JATS tags
    return " ".join(s.split())


def from_crossref(doi: str) -> dict:
    data = json.loads(http_get("https://api.crossref.org/works/" + urllib.parse.quote(doi)))["message"]
    authors = []
    for a in data.get("author", []):
        name = " ".join(p for p in (a.get("given"), a.get("family")) if p) or a.get("name", "")
        if name:
            authors.append(clean(name))
    if not authors:
        for e in data.get("editor", []):
            authors.append(clean(" ".join(p for p in (e.get("given"), e.get("family")) if p)))
    issued = (data.get("published-print") or data.get("published-online") or data.get("issued"))["date-parts"][0]
    container = data.get("container-title") or [""]
    short = data.get("short-container-title") or []
    kind = data.get("type", "")
    entry = {
        "type": {"journal-article": "article", "book": "book", "monograph": "book",
                 "book-chapter": "chapter", "proceedings-article": "proceedings"}.get(kind, kind or "misc"),
        "title": clean(data["title"][0]) if data.get("title") else "",
        "authors": authors,
        "year": int(issued[0]),
        "journal": clean(short[0] if short else container[0]) if kind == "journal-article" else None,
        "booktitle": clean(container[0]) if kind in ("book-chapter", "proceedings-article") and container else None,
        "publisher": clean(data["publisher"]) if kind in ("book", "monograph", "book-chapter") else None,
        "volume": data.get("volume"),
        "issue": None,
        "pages": data.get("page") or data.get("article-number"),
        "doi": data["DOI"].lower(),
    }
    return {k: v for k, v in entry.items() if v not in (None, "", [])}


def from_arxiv(arxiv_id: str) -> dict:
    x = http_get("https://export.arxiv.org/api/query?id_list=" + arxiv_id, accept="application/atom+xml").decode()
    entries = x.split("<entry>")[1:]
    if not entries or "<title>Error</title>" in x:
        raise SystemExit(f"arXiv id not found: {arxiv_id}")
    e = entries[0]
    get = lambda tag: clean(re.search(rf"<{tag}>(.*?)</{tag}>", e, re.S).group(1))
    full_id = re.search(r"<id>http://arxiv.org/abs/(.*?)</id>", e).group(1)
    base_id = re.sub(r"v\d+$", "", full_id)
    doi = re.search(r"<arxiv:doi[^>]*>(.*?)</arxiv:doi>", e)
    jref = re.search(r"<arxiv:journal_ref[^>]*>(.*?)</arxiv:journal_ref>", e, re.S)
    return {
        "type": "preprint",
        "title": get("title"),
        "authors": [clean(a) for a in re.findall(r"<name>(.*?)</name>", e)],
        "year": int(get("published")[:4]),
        "arxiv": base_id,
        "_doi": doi.group(1).strip().lower() if doi else None,
        "_journal_ref": clean(jref.group(1)) if jref else None,
    }


def norm_title(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\$[^$]*\$", "", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def build_entry(doi: str | None, arxiv: str | None) -> dict:
    ax = from_arxiv(arxiv) if arxiv else None
    doi = doi or (ax or {}).get("_doi")
    if doi:
        entry = from_crossref(doi)
        if ax:
            a, b = norm_title(ax["title"]), norm_title(entry["title"])
            if a[:40] != b[:40]:
                print(f"  ! title mismatch between arXiv and DOI:\n    arXiv: {ax['title']}\n    DOI:   {entry['title']}",
                      file=sys.stderr)
            entry["arxiv"] = ax["arxiv"]
            # Crossref sometimes lacks authors for older items; arXiv list is complete.
            if not entry.get("authors"):
                entry["authors"] = ax["authors"]
    else:
        entry = {k: v for k, v in ax.items() if not k.startswith("_")}
    return entry


# ------------------------------------------------------------------ file I/O
def load() -> dict:
    if not REFS.exists():
        return {}
    return yaml.safe_load(REFS.read_text(encoding="utf-8")) or {}


def dump_entry(key: str, entry: dict) -> str:
    order = ["type", "title", "authors", "journal", "booktitle", "publisher", "volume", "issue",
             "pages", "year", "doi", "arxiv", "url", "note"]
    ordered = {k: entry[k] for k in order if k in entry}
    ordered.update({k: v for k, v in entry.items() if k not in ordered})
    text = yaml.safe_dump({key: ordered}, sort_keys=False, allow_unicode=True, width=100)
    return text


def add(key: str, doi: str | None, arxiv: str | None, note: str | None, force: bool) -> None:
    if not KEY_RE.match(key):
        raise SystemExit(f"bad key '{key}': use lowercase firstauthorYEARword, e.g. khaneja2005grape")
    refs = load()
    if key in refs and not force:
        raise SystemExit(f"key '{key}' already exists (use --force to replace)")
    entry = build_entry(doi, arxiv)
    for k, e in refs.items():
        if k == key:
            continue
        if entry.get("doi") and e.get("doi") == entry["doi"] or entry.get("arxiv") and e.get("arxiv") == entry["arxiv"]:
            raise SystemExit(f"this work is already in the bibliography as '{k}'")
    if note:
        entry["note"] = note
    if key in refs:
        refs[key] = entry
        body = "".join(dump_entry(k, v) + "\n" for k, v in refs.items())
        REFS.write_text(HEADER + "\n" + body, encoding="utf-8", newline="\n")
    else:
        if not REFS.exists():
            REFS.write_text(HEADER + "\n", encoding="utf-8", newline="\n")
        with REFS.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(dump_entry(key, entry) + "\n")
    print(f"{key}: {fmt(entry)}")


def fmt(e: dict) -> str:
    a = e.get("authors", [])
    who = ", ".join(a[:3]) + (" et al." if len(a) > 3 else "")
    venue = e.get("journal") or e.get("booktitle") or e.get("publisher") or ("arXiv:" + e["arxiv"] if e.get("arxiv") else "")
    vol = f" {e['volume']}" if e.get("volume") else ""
    pg = f", {e['pages']}" if e.get("pages") else ""
    return f"{who}, \"{e.get('title')}\", {venue}{vol}{pg} ({e.get('year')})"


def check(online: bool) -> int:
    refs = load()
    problems = 0
    seen: dict[str, str] = {}
    for key, e in refs.items():
        msgs = []
        if not KEY_RE.match(key):
            msgs.append("bad key format")
        for field in ("type", "title", "authors", "year"):
            if not e.get(field):
                msgs.append(f"missing {field}")
        if not (e.get("doi") or e.get("arxiv") or e.get("url")):
            msgs.append("no identifier (doi / arxiv / url)")
        for ident in ("doi", "arxiv"):
            if e.get(ident):
                if e[ident] in seen:
                    msgs.append(f"duplicate {ident} of '{seen[e[ident]]}'")
                seen[e[ident]] = key
        if online and not msgs:
            try:
                fresh = build_entry(e.get("doi"), e.get("arxiv"))
                if norm_title(fresh["title"]) != norm_title(e["title"]):
                    msgs.append("title differs from source")
            except Exception as exc:
                msgs.append(f"lookup failed: {exc}")
            time.sleep(1)
        if msgs:
            problems += 1
            print(f"{key}: " + "; ".join(msgs))
    print(f"{len(refs)} entries, {problems} with problems")
    return 1 if problems else 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("key")
    a.add_argument("--doi")
    a.add_argument("--arxiv")
    a.add_argument("--note")
    a.add_argument("--force", action="store_true")
    s = sub.add_parser("show")
    s.add_argument("key")
    c = sub.add_parser("check")
    c.add_argument("--online", action="store_true")
    args = ap.parse_args()

    if args.cmd == "add":
        if not (args.doi or args.arxiv):
            raise SystemExit("give --doi and/or --arxiv")
        add(args.key, args.doi, args.arxiv, args.note, args.force)
    elif args.cmd == "show":
        e = load().get(args.key)
        print(dump_entry(args.key, e) if e else f"no entry '{args.key}'")
    else:
        sys.exit(check(args.online))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
