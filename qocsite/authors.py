"""Author identities for the paper tracker: group the spellings of a name that belong to the same person.

arXiv lists authors as free text ("M. H. Goerz", "Michael Goerz", "Michael H. Goerz"). The rule:

* names are compared without diacritics, case and dots ("Müller" = "Mueller" = "Muller"); hyphenated given names stay one name
  ("Zhao-Ming" and "Zhao-Wei" are different people);
* the surname is the last word, together with lowercase particles before it ("van Frank", "de Fouquières");
* two spellings are the same person if surname and first given name agree; middle names are ignored;
* a spelling with only an initial ("M. Goerz") is attached to the full name with that initial and surname, but only
  if that full name is unambiguous: the only one in the archive, or at least 80% of the spellings with full names
  (so that a single typo does not split a person) — otherwise it stays a separate entry.

Different people who share a first name and surname are not distinguished; this is stated on the author page.
"""
from __future__ import annotations

import re
import unicodedata
from collections import Counter, defaultdict

PARTICLES = {"van", "von", "de", "der", "den", "del", "della", "di", "da", "du", "dos", "das", "le", "la", "ten",
             "ter", "zu", "af", "al", "el", "y", "e", "bin"}
SUFFIXES = {"jr", "sr", "ii", "iii", "iv"}
EXTRA = str.maketrans({"ø": "o", "Ø": "O", "ł": "l", "Ł": "L", "đ": "d", "Đ": "D", "ß": "ss", "æ": "ae", "Æ": "AE",
                       "œ": "oe", "Œ": "OE", "ı": "i"})


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.translate(EXTRA))
    return "".join(c for c in s if not unicodedata.combining(c))


def parse(name: str) -> tuple[list[str], str] | None:
    """(given-name tokens, surname) in folded lowercase; None if the name cannot be parsed."""
    tokens = [t.replace("-", "") for t in re.split(r"[\s\.]+", fold(name).replace(",", " ")) if t.strip("-")]
    while tokens and tokens[-1].lower() in SUFFIXES:
        tokens.pop()
    if not tokens:
        return None
    i = len(tokens) - 1
    while i > 0 and tokens[i - 1].lower() in PARTICLES and i - 1 > 0:
        i -= 1
    surname = umlauts(" ".join(tokens[i:]).lower())
    given = [umlauts(t.lower()) for t in tokens[:i]]
    return given, surname


def umlauts(s: str) -> str:
    """Müller, Mueller and Muller are written interchangeably on arXiv: compare them as one (keys only)."""
    return s.replace("ue", "u").replace("oe", "o").replace("ae", "a")


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", fold(s).lower()).strip("-") or "author"


def build_identities(papers: list[dict]) -> tuple[dict[str, str], dict[str, dict]]:
    """Map every author string to an identity key; return (string -> key, key -> {name, slug, count})."""
    spellings: Counter = Counter(a for p in papers for a in p["authors"])
    parsed = {s: parse(s) for s in spellings}

    # full first names known per (initial, surname)
    full_by_initial: dict[tuple[str, str], Counter] = defaultdict(Counter)
    for s, pr in parsed.items():
        if pr and pr[0] and len(pr[0][0]) > 1:
            full_by_initial[(pr[0][0][0], pr[1])][pr[0][0]] += spellings[s]

    key_of: dict[str, str] = {}
    for s, pr in parsed.items():
        if not pr:
            key_of[s] = "x:" + s.lower()
            continue
        given, surname = pr
        if not given:
            key_of[s] = f"{surname}|"
            continue
        first = given[0]
        if len(first) == 1:                       # initial only
            fulls = full_by_initial.get((first, surname))
            if fulls:
                best, n = fulls.most_common(1)[0]
                if len(fulls) == 1 or n >= 0.8 * sum(fulls.values()):
                    first = best
        key_of[s] = f"{surname}|{first}"

    # display name: the most frequent spelling, preferring full first names and longer forms on ties
    variants: dict[str, Counter] = defaultdict(Counter)
    for s, n in spellings.items():
        variants[key_of[s]][s] += n
    ids: dict[str, dict] = {}
    used_slugs: set[str] = set()
    for key in sorted(variants):
        v = variants[key]
        def rank(s):
            pr = parsed.get(s)
            full = bool(pr and pr[0] and len(pr[0][0]) > 1)
            return (full, v[s], len(s))
        name = max(v, key=rank)
        surname, _, first = key.partition("|")
        slug = slugify(f"{first} {surname}") if first else slugify(surname)
        base, k = slug, 2
        while slug in used_slugs:
            slug, k = f"{base}-{k}", k + 1
        used_slugs.add(slug)
        ids[key] = {"name": name, "slug": slug, "variants": sorted(v), "count": sum(v.values())}
    return key_of, ids
