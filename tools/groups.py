"""Manage data/groups.yaml — the research groups shown on the world map.

Rules (as for the bibliography): nothing that can be looked up is typed by hand.
  * Each group has a website, which must load and mention every PI by surname (`check`).
  * The location comes from the institution's Wikidata entry (`wikidata: Q...`): coordinates (P625),
    city (P131 / P159 chain) and country (P17) are filled in by `coords`, never typed.
  * Research topics are not stored: the site derives them from the PIs' tracked papers.

Usage
-----
    python tools/groups.py find "Freie Universität Berlin"   # candidate Wikidata entries with coordinates
    python tools/groups.py coords                           # fill city/country/lat/lon from Wikidata
    python tools/groups.py check                            # websites load and name the PIs; locations match
    python tools/groups.py check --write                    # ... and record today's date as `checked`
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import ssl
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
GROUPS = ROOT / "data" / "groups.yaml"
UA = "QOC-groups/1.0 (https://github.com/llorebaga/QOC; research-group directory)"
WD_API = "https://www.wikidata.org/w/api.php"
GENERATED = ["city", "country", "lat", "lon"]

HEADER = """\
# Research groups on the QOC world map.
#
# Hand-written: id, name, pis, institution, wikidata (the institution's Wikidata id), website, kind (optional:
#   theory | experiment | both — only when the group's own website says so), arxiv_names (optional: other spellings
#   of a PI's name on arXiv, to link the right author page), note (optional).
# Generated — do not edit by hand: city, country, lat, lon (python tools/groups.py coords) and checked
#   (python tools/groups.py check --write: the website loaded and named every PI on that date).
# Topics are not stored here: the site derives them from the PIs' papers in the tracker.
"""


try:
    import certifi
    SSL = ssl.create_default_context(cafile=certifi.where())
except ImportError:           # fall back to the system store
    SSL = ssl.create_default_context()


def get(url: str, params: dict | None = None, accept: str = "application/json") -> bytes:
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=45, context=SSL) as r:
                return r.read()
        except urllib.error.URLError as exc:
            if isinstance(exc.reason, ssl.SSLCertVerificationError) and "local issuer" in str(exc.reason):
                # some servers send an incomplete certificate chain; curl (system store) completes it — still verified
                return subprocess.run(["curl", "-sSL", "--max-time", "45", "-A", UA, url],
                                      check=True, capture_output=True).stdout
            if attempt == 3:
                raise
            time.sleep(3 * (attempt + 1))
        except Exception:
            if attempt == 3:
                raise
            time.sleep(3 * (attempt + 1))
    raise RuntimeError("unreachable")


def fold(s: str) -> str:
    s = s.translate(str.maketrans({"ø": "o", "ł": "l", "ß": "ss"}))
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()


def load() -> list[dict]:
    return yaml.safe_load(GROUPS.read_text(encoding="utf-8")) or [] if GROUPS.exists() else []


def save(groups: list[dict]) -> None:
    order = ["id", "name", "pis", "arxiv_names", "institution", "wikidata", "website", "kind", "note"] + GENERATED + ["checked"]
    chunks = []
    for g in sorted(groups, key=lambda g: g["id"]):
        d = {k: g[k] for k in order if g.get(k) not in (None, "")}
        d.update({k: v for k, v in g.items() if k not in d and v not in (None, "")})
        chunks.append(yaml.safe_dump([d], allow_unicode=True, sort_keys=False, width=110).rstrip())
    GROUPS.write_text(HEADER + "\n" + "\n\n".join(chunks) + "\n", encoding="utf-8", newline="\n")


# ------------------------------------------------------------------ Wikidata
def entities(ids: list[str]) -> dict:
    out = {}
    for i in range(0, len(ids), 40):
        d = json.loads(get(WD_API, {"action": "wbgetentities", "ids": "|".join(ids[i:i + 40]), "format": "json",
                                    "props": "labels|descriptions|claims", "languages": "en"}))
        out.update(d.get("entities", {}))
        time.sleep(0.5)
    return out


def label(e: dict) -> str:
    return e.get("labels", {}).get("en", {}).get("value", "")


def claim_values(e: dict, prop: str) -> list:
    vals = []
    for c in e.get("claims", {}).get(prop, []):
        dv = c.get("mainsnak", {}).get("datavalue")
        if dv:
            vals.append(dv["value"])
    return vals


def location(qid: str) -> dict:
    """Coordinates, city and country of an institution, from Wikidata."""
    e = entities([qid])[qid]
    coords = claim_values(e, "P625")
    if not coords:
        raise SystemExit(f"{qid} ({label(e)}): no coordinates (P625) on Wikidata")
    c = coords[0]
    out = {"lat": round(c["latitude"], 4), "lon": round(c["longitude"], 4), "_label": label(e)}
    country = claim_values(e, "P17")
    if country:
        out["country"] = label(entities([country[0]["id"]])[country[0]["id"]])
    # city: start from "headquarters location" (P159) or "located in" (P131) and climb the P131 chain until the
    # place is described as a settlement (a building or district is not a city)
    queue = [v["id"] for v in claim_values(e, "P159") + claim_values(e, "P131")]
    for _ in range(4):
        if not queue:
            break
        pe = entities([queue[0]])[queue[0]]
        desc = pe.get("descriptions", {}).get("en", {}).get("value", "").lower()
        if re.search(r"\b(city|town|commune|capital|municipality|village|borough)\b", desc):
            out["city"] = label(pe)
            break
        queue = [v["id"] for v in claim_values(pe, "P131")] or queue[1:]
    return out


def cmd_find(name: str) -> None:
    d = json.loads(get(WD_API, {"action": "wbsearchentities", "search": name, "language": "en", "format": "json",
                                "type": "item", "limit": 7}))
    ids = [r["id"] for r in d.get("search", [])]
    ents = entities(ids) if ids else {}
    for r in d.get("search", []):
        e = ents.get(r["id"], {})
        c = claim_values(e, "P625")
        where = f"{c[0]['latitude']:.4f}, {c[0]['longitude']:.4f}" if c else "no coordinates"
        print(f"{r['id']:>11}  {r.get('label', '')}  — {r.get('description', '')}  [{where}]")


def cmd_coords() -> None:
    groups = load()
    for g in groups:
        loc = location(g["wikidata"])
        print(f"{g['id']}: {loc['_label']} -> {loc.get('city')}, {loc.get('country')} ({loc['lat']}, {loc['lon']})")
        for k in GENERATED:
            if k in loc:
                g[k] = loc[k]
    save(groups)


# ------------------------------------------------------------------ check
def page_text(url: str) -> str:
    raw = get(url, accept="text/html,application/xhtml+xml").decode("utf-8", "replace")
    raw = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", raw)
    return fold(html.unescape(re.sub(r"<[^>]+>", " ", raw)))


def surname(pi: str) -> str:
    parts = pi.replace(".", " ").split()
    particles = {"van", "von", "de", "der", "del", "di", "da", "du", "le", "la"}
    i = len(parts) - 1
    while i > 0 and parts[i - 1].lower() in particles:
        i -= 1
    return " ".join(parts[i:])


def cmd_check(write: bool) -> int:
    groups = load()
    problems = 0
    ids = set()
    today = dt.date.today().isoformat()
    for g in groups:
        msgs = []
        for k in ("id", "name", "pis", "institution", "wikidata", "website"):
            if not g.get(k):
                msgs.append(f"missing {k}")
        if g.get("id") in ids:
            msgs.append("duplicate id")
        ids.add(g.get("id"))
        if g.get("kind") not in (None, "theory", "experiment", "both"):
            msgs.append(f"bad kind {g.get('kind')!r}")
        if any(g.get(k) is None for k in ("lat", "lon")):
            msgs.append("no coordinates (run: tools/groups.py coords)")
        try:
            text = page_text(g["website"])
            missing = [p for p in g["pis"] if fold(surname(p)) not in text]
            if missing:
                msgs.append(f"website does not mention {missing}")
            words = {"theory": ["theor"], "experiment": ["experiment"], "both": ["theor", "experiment"]}
            for w in words.get(g.get("kind"), []):
                if w not in text:
                    msgs.append(f"kind '{g['kind']}' but the website does not say '{w}…'")
            if fold(g["name"]) not in text and not g["name"].endswith(" group"):
                print(f"  (note: {g.get('id')}: the name '{g['name']}' is not on the website)")
        except Exception as exc:
            msgs.append(f"website failed: {exc}")
        try:
            loc = location(g["wikidata"])
            if g.get("lat") is not None and (abs(loc["lat"] - g["lat"]) > 1e-3 or abs(loc["lon"] - g["lon"]) > 1e-3):
                msgs.append("coordinates differ from Wikidata (run coords)")
        except SystemExit as exc:
            msgs.append(str(exc))
        if msgs:
            problems += 1
            print(f"✗ {g.get('id')}: " + "; ".join(msgs))
        else:
            print(f"✓ {g['id']}")
            if write:
                g["checked"] = today
        time.sleep(1)
    if write:
        save(groups)
    print(f"{len(groups)} groups, {problems} with problems")
    return 1 if problems else 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find"); f.add_argument("name")
    sub.add_parser("coords")
    c = sub.add_parser("check"); c.add_argument("--write", action="store_true")
    a = ap.parse_args()
    if a.cmd == "find":
        cmd_find(a.name)
    elif a.cmd == "coords":
        cmd_coords()
    else:
        sys.exit(cmd_check(a.write))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
