"""Generate the QOC logo assets.

The mark is the word "QOC" drawn as geometric strokes, with a control pulse
(a Gaussian-envelope wave packet) running through the letters. Where the pulse
crosses a letter, the letter is cut by a thin gap so the pulse appears to pass
*through* it.

Outputs
-------
static/img/logo.svg            standalone wordmark (adapts to light/dark)
static/img/favicon.svg         square icon: the "O" with the pulse through it
templates/partials/logo.html   Jinja macro for inlining the logo (currentColor)

Run:  python tools/make_logo.py
"""
from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- geometry
W, H = 320, 120          # viewBox of the wordmark
CY = 60                  # vertical centre line
R = 36                   # ring radius of every letter
SW = 10                  # letter stroke width
CENTERS = (60, 160, 260) # x-centres of Q, O, C
C_OPEN = 50              # half opening angle of the C, degrees

# pulse: y(x) = CY - A * exp(-((x-x0)/sigma)^2) * cos(2 pi (x-x0)/lam)
PULSE_X = (-6, W + 6)
PULSE_A = 15
PULSE_SIGMA = 120
PULSE_LAMBDA = 28.8         # ring sides (offsets 36, 64, 136 from the centre) sit on zero crossings
PULSE_W = 3.6            # pulse stroke width
GAP = 2.6                # clearance cut into letters on each side of the pulse

# brand colours (kept in sync with static/css/main.css)
INK_LIGHT = "#0e1530"
INK_DARK = "#eef1ff"
GRAD = ("#22d3ee", "#7c5cff", "#f0469b")   # cyan -> violet -> magenta


def f(v: float) -> str:
    """Compact number formatting for path data."""
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def pulse_path(x_from: float, x_to: float, x0: float, amp: float, sigma: float,
               lam: float, cy: float = CY, step: float = 1.0) -> str:
    pts = []
    n = int((x_to - x_from) / step)
    for i in range(n + 1):
        x = x_from + i * step
        env = math.exp(-((x - x0) / sigma) ** 2)
        y = cy - amp * env * math.cos(2 * math.pi * (x - x0) / lam)
        pts.append((x, y))
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)


def ring(cx: float, cy: float, r: float) -> str:
    # two arcs make a full circle as a path (so it can share a stroke style)
    return (f"M{f(cx - r)} {f(cy)} a{f(r)} {f(r)} 0 1 0 {f(2 * r)} 0 "
            f"a{f(r)} {f(r)} 0 1 0 {f(-2 * r)} 0")


def letter_paths() -> list[str]:
    qx, ox, cx = CENTERS
    # Q: ring + diagonal tail
    t0 = (qx + (R - 8) * math.cos(math.radians(45)), CY + (R - 8) * math.sin(math.radians(45)))
    t1 = (qx + (R + 14) * math.cos(math.radians(45)), CY + (R + 14) * math.sin(math.radians(45)))
    q = ring(qx, CY, R) + f" M{f(t0[0])} {f(t0[1])} L{f(t1[0])} {f(t1[1])}"
    # O: ring
    o = ring(ox, CY, R)
    # C: arc open on the right, drawn counter-clockwise (through the top)
    a = math.radians(C_OPEN)
    sx, sy = cx + R * math.cos(-a), CY + R * math.sin(-a)
    ex, ey = cx + R * math.cos(a), CY + R * math.sin(a)
    c = f"M{f(sx)} {f(sy)} A{f(R)} {f(R)} 0 1 0 {f(ex)} {f(ey)}"
    return [q, o, c]


# ---------------------------------------------------------------- builders
def wordmark_body(prefix: str, ink: str) -> str:
    """Inner SVG markup (defs + shapes). `ink` is the letter colour."""
    pulse = pulse_path(*PULSE_X, x0=CENTERS[1], amp=PULSE_A, sigma=PULSE_SIGMA, lam=PULSE_LAMBDA)
    letters = "".join(f'<path d="{d}"/>' for d in letter_paths())
    return f"""<defs>
    <linearGradient id="{prefix}-grad" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{GRAD[0]}" stop-opacity="0"/>
      <stop offset="0.12" stop-color="{GRAD[0]}"/>
      <stop offset="0.5" stop-color="{GRAD[1]}"/>
      <stop offset="0.88" stop-color="{GRAD[2]}"/>
      <stop offset="1" stop-color="{GRAD[2]}" stop-opacity="0"/>
    </linearGradient>
    <mask id="{prefix}-cut" maskUnits="userSpaceOnUse" x="-20" y="-20" width="{W + 40}" height="{H + 40}">
      <rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="#fff"/>
      <path d="{pulse}" fill="none" stroke="#000" stroke-width="{f(PULSE_W + 2 * GAP)}" stroke-linecap="round" stroke-linejoin="round"/>
    </mask>
  </defs>
  <g class="qoc-letters" mask="url(#{prefix}-cut)" fill="none" stroke="{ink}" stroke-width="{SW}" stroke-linecap="round">{letters}</g>
  <path class="qoc-pulse" d="{pulse}" fill="none" stroke="url(#{prefix}-grad)" stroke-width="{PULSE_W}" stroke-linecap="round" stroke-linejoin="round" pathLength="1000"/>"""


def standalone_logo() -> str:
    body = wordmark_body("qoc", "var(--ink)")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">QOC — Quantum Optimal Control</title>
  <style>
    svg {{ --ink: {INK_LIGHT}; }}
    @media (prefers-color-scheme: dark) {{ svg {{ --ink: {INK_DARK}; }} }}
  </style>
  {body}
</svg>
"""


def favicon() -> str:
    # The "O" alone with the pulse through it, on a dark rounded square.
    s = 64
    cx = cy = 32
    r = 19
    sw = 6
    pulse = pulse_path(-2, 66, x0=32, amp=9, sigma=20, lam=10.4, cy=cy, step=0.5)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s} {s}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="{s}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{GRAD[0]}"/>
      <stop offset="0.5" stop-color="{GRAD[1]}"/>
      <stop offset="1" stop-color="{GRAD[2]}"/>
    </linearGradient>
    <mask id="m" maskUnits="userSpaceOnUse" x="0" y="0" width="{s}" height="{s}">
      <rect width="{s}" height="{s}" fill="#fff"/>
      <path d="{pulse}" fill="none" stroke="#000" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>
    </mask>
  </defs>
  <rect width="{s}" height="{s}" rx="14" fill="{INK_LIGHT}"/>
  <path d="{ring(cx, cy, r)}" fill="none" stroke="{INK_DARK}" stroke-width="{sw}" mask="url(#m)"/>
  <path d="{pulse}" fill="none" stroke="url(#g)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


def jinja_macro() -> str:
    body = wordmark_body("{{ id }}", "currentColor")
    return f"""{{#- Generated by tools/make_logo.py — do not edit by hand. -#}}
{{% macro logo(id='qoc', cls='', label='QOC — Quantum Optimal Control') -%}}
<svg class="qoc-logo {{{{ cls }}}}" viewBox="0 0 {W} {H}" role="img" aria-label="{{{{ label }}}}" xmlns="http://www.w3.org/2000/svg">
  {body}
</svg>
{{%- endmacro %}}
"""


def main() -> None:
    out = {
        ROOT / "static/img/logo.svg": standalone_logo(),
        ROOT / "static/img/favicon.svg": favicon(),
        ROOT / "templates/partials/logo.html": jinja_macro(),
    }
    for path, text in out.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
