"""Assign field-map topics to papers — shared by the site build and the evaluation tool.

The rules live in data/classifier.yaml (phrases per topic); see the header of that file for the scoring.
The classifier is deliberately simple and transparent: every assignment can be traced to the phrases that
triggered it, and its accuracy is measured against hand-labelled papers (tools/paper_quality.py topics).
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path

import yaml

STRONG, WEAK = 1.5, 1          # a single passing mention of a strong phrase needs support
TITLE_FACTOR = 2
MAX_MENTIONS = 2                 # mentions counted per phrase
THRESHOLD = 2
MAX_TOPICS = 4


def fold(s: str) -> str:
    """Remove diacritics (Schrödinger -> Schrodinger) so that spellings with and without them match."""
    if s.isascii():
        return s
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


WORD = re.compile(r"\w+")


def phrase_key(phrase: str) -> frozenset[str] | None:
    """Words of a phrase, lowercased: a cheap pre-check before running the regex (None: always run).

    Words written together in the text ("counterdiabatic") are not split, so a phrase only matches if every
    one of its words also appears as a word of the text — exactly when the regex can match."""
    if phrase.startswith(("re:", "RE:")):
        return None
    return frozenset(WORD.findall(fold(phrase).lower()))


def phrase_regex(phrase: str) -> re.Pattern:
    if phrase.startswith(("re:", "RE:")):
        return re.compile(phrase[3:], 0 if phrase.startswith("RE:") else re.I)
    phrase = fold(phrase)
    words = re.split(r"[\s-]+", phrase.strip())
    case_sensitive = " " not in phrase and sum(c.isupper() for c in phrase) >= 2
    body = r"[\s-]*".join(re.escape(w) for w in words)
    if words[-1][-1:].isalpha() and not case_sensitive:
        body += r"(?:s|es)?"                         # plurals
    start = r"\b" if words[0][:1].isalnum() else ""
    end = r"\b" if words[-1][-1:].isalnum() else ""
    return re.compile(start + body + end, 0 if case_sensitive else re.I)


def load_rules(path: Path, topic_ids: set[str] | None = None) -> dict[str, list[tuple]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if topic_ids is not None:
        unknown = sorted(set(raw) - topic_ids)
        if unknown:
            raise ValueError(f"{path.name}: unknown topic ids {unknown}")
    rules = {}
    for tid, spec in raw.items():
        rules[tid] = ([(phrase_regex(p), STRONG, p, phrase_key(p)) for p in spec.get("strong") or []] +
                      [(phrase_regex(p), WEAK, p, phrase_key(p)) for p in spec.get("weak") or []])
    return rules


def scores(paper: dict, rules: dict) -> dict[str, float]:
    title, abstract = fold(paper["title"]), fold(paper["abstract"])
    words = set(WORD.findall((title + " " + abstract).lower()))
    words |= {w[:-1] for w in words if w.endswith("s")} | {w[:-2] for w in words if w.endswith("es")}
    out = {}
    for tid, patterns in rules.items():
        total = 0
        for rx, weight, _, key in patterns:
            if key is not None and not key <= words:
                continue
            nt = len(rx.findall(title))
            na = len(rx.findall(abstract))
            if nt or na:
                total += weight * min(MAX_MENTIONS, TITLE_FACTOR * nt + na)
        if total:
            out[tid] = total
    return out


def classify(paper: dict, rules: dict) -> list[str]:
    """Topics of a paper, most strongly supported first."""
    s = scores(paper, rules)
    return [t for t, v in sorted(s.items(), key=lambda kv: (-kv[1], kv[0])) if v >= THRESHOLD][:MAX_TOPICS]


def explain(paper: dict, rules: dict, topic: str) -> list[str]:
    """The phrases that matched for one topic (for debugging rules)."""
    text = fold(paper["title"] + " " + paper["abstract"])
    return [p for rx, _, p, _ in rules.get(topic, []) if rx.search(text)]


def classify_all(papers: list[dict], rules_path: Path, cache_path: Path | None = None) -> dict[str, list[str]]:
    """Topics for every paper (by arXiv id). Results are cached per paper and invalidated when the rules
    or the paper's title/abstract change, so that rebuilding the site stays fast."""
    rules_text = rules_path.read_text(encoding="utf-8")
    rules_hash = hashlib.sha1((rules_text + Path(__file__).read_text(encoding="utf-8")).encode()).hexdigest()[:12]
    cache: dict = {}
    if cache_path and cache_path.exists():
        try:
            stored = json.loads(cache_path.read_text(encoding="utf-8"))
            if stored.get("rules") == rules_hash:
                cache = stored["papers"]
        except (ValueError, KeyError):
            cache = {}
    rules = load_rules(rules_path)
    out, fresh = {}, {}
    for p in papers:
        h = hashlib.sha1((p["title"] + "\n" + p["abstract"]).encode()).hexdigest()[:12]
        hit = cache.get(p["id"])
        topics = hit[1] if hit and hit[0] == h else classify(p, rules)
        out[p["id"]] = topics
        fresh[p["id"]] = [h, topics]
    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps({"rules": rules_hash, "papers": fresh}, separators=(",", ":")),
                              encoding="utf-8")
    return out
