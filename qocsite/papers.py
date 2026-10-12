"""Read the arXiv paper archive (data/papers/<year>.json) and compute statistics."""
from __future__ import annotations

import datetime as dt
import json
from collections import Counter
from pathlib import Path


def load_papers(folder: Path) -> list[dict]:
    papers: list[dict] = []
    for f in sorted(folder.glob("*.json")):
        papers.extend(json.loads(f.read_text(encoding="utf-8")))
    return papers


def yearly_stats(papers: list[dict], first_year: int | None = None, today: dt.date | None = None,
                 quantph_totals: dict | None = None) -> dict:
    """Papers per year by date of first submission, with a like-for-like comparison
    for the current (incomplete) year, and the share of all quant-ph papers when totals are known."""
    today = today or dt.date.today()
    dates = [dt.date.fromisoformat(p["published"]) for p in papers]
    first_year = first_year or min((d.year for d in dates), default=today.year)   # the archive's first year
    years = list(range(first_year, today.year + 1))
    per_year = Counter(d.year for d in dates)
    # same calendar window (1 Jan .. today's month/day) for every year, for the YTD comparison
    def ytd(year: int) -> int:
        try:
            cutoff = today.replace(year=year)
        except ValueError:                         # 29 Feb
            cutoff = today.replace(year=year, day=28)
        return sum(1 for d in dates if d.year == year and d <= cutoff)

    qph = Counter(dt.date.fromisoformat(p["published"]).year for p in papers if "quant-ph" in p.get("categories", []))
    totals = {int(k): v for k, v in (quantph_totals or {}).items()}

    def share(y: int):
        return qph.get(y, 0) / totals[y] if totals.get(y) else None

    rows = [{"year": y, "count": per_year.get(y, 0), "partial": y == today.year, "ytd": ytd(y), "share": share(y)}
            for y in years]
    complete = [r for r in rows if not r["partial"]]
    latest = max(dates) if dates else None
    current = rows[-1] if rows else None
    prev = rows[-2] if len(rows) > 1 else None
    chart = column_chart(rows)
    return {
        "chart": chart,
        "rows": rows,
        "total": len(papers),
        "first_year": first_year,
        "latest_date": latest.isoformat() if latest else None,
        "max_count": max((r["count"] for r in rows), default=0),
        "growth_since_first": (complete[-1]["count"] / complete[0]["count"] - 1) if len(complete) > 1 and complete[0]["count"] else None,
        "ytd_change": (current["ytd"] / prev["ytd"] - 1) if current and prev and prev["ytd"] else None,
        "today": today.isoformat(),
        "share_range": (min(r["share"] for r in rows if r["share"] is not None),
                        max(r["share"] for r in rows if r["share"] is not None))
                       if any(r["share"] is not None for r in rows) else None,
        "share_latest": complete[-1]["share"] if complete else None,
        "share_first": complete[0]["share"] if complete else None,
        "share_recent": (lambda rec: (min(rec), max(rec)) if rec else None)(
            [r["share"] for r in complete[-10:] if r["share"] is not None]),
        "years_span": len(rows),
    }


def nice_step(max_value: int, target_ticks: int = 4) -> int:
    """A clean tick step (1, 2, 2.5, 5 x 10^k) giving about `target_ticks` gridlines."""
    if max_value <= 0:
        return 1
    raw = max_value / target_ticks
    mag = 10 ** (len(str(int(raw))) - 1)
    for m in (1, 2, 2.5, 5, 10):
        if m * mag >= raw:
            return int(m * mag)
    return int(10 * mag)


def column_chart(rows: list[dict], width: int = 640, height: int = 280) -> dict:
    """Geometry for the papers-per-year column chart (rendered as SVG at build time).

    Marks follow the QOC chart spec: columns <= 24px, 4px rounded data-end and a square
    base, hairline gridlines at clean ticks, values labelled selectively.
    """
    left, right, top, bottom = 52, 12, 30, 48
    pw, ph = width - left - right, height - top - bottom
    vmax = max((r["count"] for r in rows), default=0)
    step = nice_step(vmax)
    ymax = max(step, -(-vmax // step) * step)
    if ymax - vmax < step * 0.25:            # leave headroom for the cap labels
        ymax += step
    slot = pw / max(len(rows), 1)
    bar_w = min(24.0, slot * 0.5)
    y = lambda v: top + ph * (1 - v / ymax)
    peak = max(rows, key=lambda r: (r["count"] if not r["partial"] else -1)) if rows else None
    # axis labels: every year for short ranges, every other year for medium ones, round years (2000, 2005, …)
    # for long ones — always including the latest year
    def show_year(i: int) -> bool:
        if len(rows) <= 10:
            return True
        if len(rows) <= 20:
            return (len(rows) - 1 - i) % 2 == 0
        y = rows[i]["year"]
        last = rows[-1]["year"]
        return y == last or (y % 5 == 0 and last - y >= 3)
    bars = []
    for i, r in enumerate(rows):
        cx = left + slot * (i + 0.5)
        x0, x1 = cx - bar_w / 2, cx + bar_w / 2
        yt, yb = y(r["count"]), y(0)
        rad = min(4.0, max(0.0, yb - yt))
        path = (f"M{x0:.1f} {yb:.1f}V{yt + rad:.1f}Q{x0:.1f} {yt:.1f} {x0 + rad:.1f} {yt:.1f}"
                f"H{x1 - rad:.1f}Q{x1:.1f} {yt:.1f} {x1:.1f} {yt + rad:.1f}V{yb:.1f}Z") if r["count"] else ""
        label = i == 0 or r["partial"] or r is peak
        bars.append({**r, "cx": round(cx, 1), "path": path, "label_y": round(yt - 8, 1), "show_label": label,
                     "show_year": show_year(i),
                     "hit_x": round(left + slot * i, 1), "hit_w": round(slot, 1)})
    ticks = [{"value": v, "y": round(y(v), 1)} for v in range(0, ymax + 1, step)]
    return {"width": width, "height": height, "left": left, "right": width - right, "top": top,
            "baseline": round(y(0), 1), "bars": bars, "ticks": ticks, "plot_top": top, "plot_h": ph}
