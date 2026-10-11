"""Markdown articles with math, citations and topic cross-links.

Article syntax (on top of standard Markdown + tables + admonitions)
-------------------------------------------------------------------
    $x^2$, \\(x^2\\)       inline math (KaTeX)
    $$ ... $$             display math
    [@key]                citation of data/references.yaml entry `key`
    [@key1; @key2]        several citations
    [[grape]]             link to a topic (text = topic title)
    [[grape|GRAPE's]]     link with custom text

Math and citations are protected from the Markdown processor with
placeholders, so underscores and asterisks inside formulas are safe.
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass, field

import markdown
import yaml


class ContentError(Exception):
    pass


@dataclass
class Article:
    id: str
    meta: dict
    html: str
    toc: list[dict]
    citations: list[str]                 # keys, in order of first citation
    source: str = ""
    word_count: int = 0
    extra: dict = field(default_factory=dict)


FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
DISPLAY_MATH = re.compile(r"\$\$(.+?)\$\$", re.S)
PAREN_MATH = re.compile(r"\\\((.+?)\\\)", re.S)
# inline $...$ may wrap onto the next source line, but never across a blank line
# (as in Pandoc: the closing $ may be followed by letters, e.g. "$N$th", but not by a digit)
INLINE_MATH = re.compile(r"(?<![\\$\w])\$(?!\$)((?:[^$\n]|\n(?![ \t]*\n))+?)(?<![\\\s])\$(?![$\d])")
CITATION = re.compile(r"\[(@[\w-]+(?:\s*[;,]\s*@[\w-]+)*)\]")
TOPIC_LINK = re.compile(r"\[\[([a-z0-9-]+)(?:\|([^\]]+))?\]\]")


def split_front_matter(text: str) -> tuple[dict, str]:
    m = FRONT_MATTER.match(text)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, text[m.end():]


def render_article(article_id: str, text: str, *, references: dict, topics: dict, url) -> Article:
    meta, body = split_front_matter(text)
    stash: list[str] = []
    citations: list[str] = []

    def keep(fragment: str) -> str:
        stash.append(fragment)
        return f"QOCPH{len(stash) - 1}X"

    # 1. math (display first, then \( \), then $ $)
    body = DISPLAY_MATH.sub(lambda m: keep("$$" + html.escape(m.group(1), quote=False) + "$$"), body)
    body = PAREN_MATH.sub(lambda m: keep(r"\(" + html.escape(m.group(1), quote=False) + r"\)"), body)
    body = INLINE_MATH.sub(lambda m: keep(r"\(" + html.escape(m.group(1), quote=False) + r"\)"), body)

    # 2. citations
    def cite(m: re.Match) -> str:
        keys = [k.strip().lstrip("@") for k in re.split(r"[;,]", m.group(1))]
        links = []
        for k in keys:
            if k not in references:
                raise ContentError(f"{article_id}: unknown citation key '{k}'")
            if k not in citations:
                citations.append(k)
            n = citations.index(k) + 1
            links.append(f'<a href="#ref-{k}" class="cite-link" data-ref="{k}">{n}</a>')
        return keep('<span class="cite">[' + ", ".join(links) + "]</span>")

    body = CITATION.sub(cite, body)

    # 3. topic cross-links
    def topic_link(m: re.Match) -> str:
        tid, text = m.group(1), m.group(2)
        if tid not in topics:
            raise ContentError(f"{article_id}: link to unknown topic '{tid}'")
        label = html.escape(text or topics[tid]["title"])
        return keep(f'<a class="topic-link" href="{url("topics/" + tid + "/")}">{label}</a>')

    body = TOPIC_LINK.sub(topic_link, body)

    md = markdown.Markdown(
        extensions=["extra", "admonition", "sane_lists", "smarty", "toc"],
        extension_configs={"toc": {"toc_depth": "2-3"}, "smarty": {"smart_angled_quotes": False}},
        output_format="html5",
    )
    out = md.convert(body)
    # restore placeholders (repeat: a stashed fragment never contains another, but be safe)
    out = re.sub(r"QOCPH(\d+)X", lambda m: stash[int(m.group(1))], out)
    if "QOCPH" in out:
        raise ContentError(f"{article_id}: unresolved placeholder")

    toc = [{"id": t["id"], "name": html.unescape(t["name"]),
            "children": [{"id": c["id"], "name": html.unescape(c["name"])} for c in t.get("children", [])]}
           for t in md.toc_tokens]

    # key_papers: list of keys, or of {key, note} — normalized to dicts
    key_papers = []
    for item in meta.get("key_papers", []) or []:
        item = {"key": item} if isinstance(item, str) else dict(item)
        if item["key"] not in references:
            raise ContentError(f"{article_id}: key_papers contains unknown key '{item['key']}'")
        item.setdefault("note", references[item["key"]].get("note", ""))
        key_papers.append(item)
    meta["key_papers"] = key_papers
    meta.setdefault("software", [])
    meta.setdefault("status", "draft")

    words = len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", out)))
    return Article(id=article_id, meta=meta, html=out, toc=toc, citations=citations, source=text, word_count=words)


# ------------------------------------------------------------------ references
def short_authors(authors: list[str], max_full: int = 6) -> str:
    if not authors:
        return ""
    if len(authors) > max_full:
        return ", ".join(authors[:5]) + ", et al."
    if len(authors) == 1:
        return authors[0]
    return ", ".join(authors[:-1]) + " and " + authors[-1]


def format_reference(e: dict) -> str:
    """HTML for one bibliography entry."""
    parts = [f'<span class="ref-authors">{html.escape(short_authors(e.get("authors", [])))}</span>',
             f'<span class="ref-title">{html.escape(e.get("title", ""))}</span>']
    venue = e.get("journal") or e.get("booktitle")
    if venue:
        v = f"<i>{html.escape(venue)}</i>"
        if e.get("volume"):
            v += f" <b>{html.escape(str(e['volume']))}</b>"
        if e.get("pages"):
            v += f", {html.escape(str(e['pages']))}"
        parts.append(f'<span class="ref-venue">{v} ({e.get("year")})</span>')
    elif e.get("type") == "book":
        parts.append(f'<span class="ref-venue">{html.escape(e.get("publisher", ""))} ({e.get("year")})</span>')
    else:
        parts.append(f'<span class="ref-venue">preprint ({e.get("year")})</span>')
    links = []
    if e.get("doi"):
        links.append(f'<a href="https://doi.org/{html.escape(e["doi"])}" rel="noopener">doi</a>')
    if e.get("arxiv"):
        links.append(f'<a href="https://arxiv.org/abs/{html.escape(e["arxiv"])}" rel="noopener">arXiv:{html.escape(e["arxiv"])}</a>')
    if e.get("url"):
        links.append(f'<a href="{html.escape(e["url"])}" rel="noopener">link</a>')
    if links:
        parts.append('<span class="ref-links">' + " · ".join(links) + "</span>")
    return " ".join(parts)
