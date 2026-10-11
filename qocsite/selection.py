"""The definition of a "QOC paper" — shared by the arXiv harvester and the site.

A paper counts as a quantum-control paper if
  * it is listed in quant-ph, or in a NEIGHBOUR category and its title or
    abstract contains the word "quantum", and
  * its title or abstract contains one of the TERMS (whole-phrase match), and
  * it is not a known false positive (EXCLUDE: "quantum control" in the sense
    of controlled operations or indefinite causal order), unless it also talks
    about optimal control or pulses.

Changing TERMS changes historical counts: re-run the full harvest afterwards
(python tools/fetch_arxiv.py --since 2020-01-01).
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
]
CATEGORIES = ["quant-ph"]
NEIGHBOURS = ["physics.chem-ph", "physics.atom-ph", "cond-mat.quant-gas", "math.OC"]
EXCLUDE_PHRASES = ["indefinite causal order", "quantum switch", "causal order",
                   "quantum-controlled operations / gates / unitaries"]

TERM_RE = re.compile(r"\b(?:" + "|".join(re.escape(t) for t in TERMS) + r")\b", re.I)
QUANTUM_RE = re.compile(r"\bquantum\b", re.I)
EXCLUDE_RE = re.compile(r"indefinite causal order|quantum switch|causal order|"
                        r"quantum[- ]controlled (?:operation|gate|unitar)", re.I)
KEEP_ANYWAY_RE = re.compile(r"optimal control|pulse", re.I)


def selected(p: dict) -> bool:
    """True if the arXiv record `p` (title, abstract, categories) is a QOC paper."""
    text = p["title"] + " " + p["abstract"]
    if not TERM_RE.search(text):
        return False
    if not any(c in CATEGORIES for c in p["categories"]) and not QUANTUM_RE.search(text):
        return False
    return not (EXCLUDE_RE.search(text) and not KEEP_ANYWAY_RE.search(text))
