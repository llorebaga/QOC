"""The definition of a "QOC paper" — shared by the arXiv harvester and the site.

A paper counts as a quantum-control paper if
  * it is listed in quant-ph, or in a NEIGHBOUR category and its title or
    abstract contains the word "quantum", and
  * its title or abstract contains one of the TERMS (whole-phrase match), and
  * it is not a known false positive (EXCLUDE: "quantum control" in the sense
    of controlled operations or indefinite causal order), unless it also talks
    about optimal control or pulses.

Changing TERMS changes historical counts: re-run the full harvest afterwards
(python tools/fetch_arxiv.py --since 2000-01-01).
"""
from __future__ import annotations

import re

TERMS = [
    "optimal control", "quantum control", "coherent control", "control pulse", "control pulses",
    "pulse optimization", "pulse optimisation", "optimized pulse", "optimized pulses", "optimal pulse",
    "optimal pulses", "pulse shaping", "pulse engineering", "pulse design", "GRAPE", "Krotov",
    "chopped random basis", "shortcut to adiabaticity", "shortcuts to adiabaticity", "counterdiabatic",
    "counter-diabatic", "quantum speed limit", "quantum speed limits", "composite pulse", "composite pulses",
    "dynamical decoupling", "controllability", "control landscape", "control landscapes",
    "feedback control", "Lyapunov control", "robust control",
    # added 2026-10-11 after a recall analysis (papers citing core QOC works); aligned with field-map topics.
    # ("Floquet engineering" and "Hamiltonian engineering" were tried and dropped: ~40-50% precision in a
    #  hand-labelled sample, since both also name large physics subfields that are not about control.)
    "dynamic decoupling", "adiabatic passage", "STIRAP",
    "inverse engineering", "time-optimal", "pulse-level", "derivative removal", "quantum feedback",
    "coherent feedback", "measurement-based feedback", "shaped pulse", "shaped pulses",
    "control protocol", "control protocols",
]
CATEGORIES = ["quant-ph"]
NEIGHBOURS = ["physics.chem-ph", "physics.atom-ph", "cond-mat.quant-gas", "math.OC"]
EXCLUDE_PHRASES = ["indefinite causal order", "quantum switch", "causal order",
                   "quantum-controlled operations / gates / unitaries"]

def _phrase(t: str) -> str:
    """Regex for a phrase in which spaces and hyphens are interchangeable ("shortcut-to-adiabaticity")."""
    return r"[\s-]+".join(re.escape(w) for w in re.split(r"[\s-]+", t))


TERM_RE = re.compile(r"\b(?:" + "|".join(_phrase(t) for t in TERMS) + r")\b", re.I)
QUANTUM_RE = re.compile(r"\bquantum\b", re.I)
EXCLUDE_RE = re.compile(r"indefinite causal order|quantum switch|causal order|"
                        r"quantum[- ]controlled (?:operation|gate|unitar)|"
                        r"quantum control flow|control-flow|quantum control machine", re.I)
KEEP_ANYWAY_RE = re.compile(r"optimal control|pulse", re.I)
# "controllability" alone is often used loosely ("the flexibility and controllability of the platform").
# Papers whose only matching term is "controllability" are kept only if the text has control-theoretic context.
# (Validated on a hand-labelled sample of 140 papers: removes 6 false positives for 1 genuine paper.)
CONTROL_CONTEXT_RE = re.compile(r"\b(?:control (?:field|fields|problem|problems|theory|system|systems|law|laws|"
                                r"protocol|protocols|scheme|strategy)|controls\b|lie algebra|bilinear|reachab|steer)",
                                re.I)


def selected(p: dict) -> bool:
    """True if the arXiv record `p` (title, abstract, categories) is a QOC paper."""
    text = p["title"] + " " + p["abstract"]
    matched = {m.group(0).lower() for m in TERM_RE.finditer(text)}
    if not matched:
        return False
    if not any(c in CATEGORIES for c in p["categories"]) and not QUANTUM_RE.search(text):
        return False
    if matched == {"controllability"} and not CONTROL_CONTEXT_RE.search(text):
        return False
    return not (EXCLUDE_RE.search(text) and not KEEP_ANYWAY_RE.search(text))
