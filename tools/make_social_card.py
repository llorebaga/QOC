"""Generate the social card (the preview image shown when a page is shared): static/img/social-card.png.

The card is an HTML page (logo, tagline, one line of description) rendered to a 1200x630 PNG by a headless
Chrome or Edge. Run it after changing the logo (tools/make_logo.py) or the tagline in config.yaml.

Run:  python tools/make_social_card.py [--browser PATH]
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "static" / "img" / "social-card.png"
W, H = 1200, 630
BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser", "microsoft-edge",
]

PAGE = """<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Space+Grotesk:wght@600;700&display=swap">
<style>
  html, body {{ margin: 0; width: {w}px; height: {h}px; overflow: hidden; }}
  body {{
    background: #f7f8fc; color: #0e1530; font-family: Inter, sans-serif;
    display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
    background-image:
      radial-gradient(520px 300px at 18% 20%, rgba(34, 211, 238, .16), transparent 70%),
      radial-gradient(560px 320px at 50% 0%, rgba(124, 92, 255, .14), transparent 70%),
      radial-gradient(520px 300px at 85% 85%, rgba(240, 70, 155, .13), transparent 70%);
  }}
  .logo {{ width: 520px; margin-bottom: 34px; }}
  .logo svg {{ width: 100%; height: auto; display: block; }}
  h1 {{ font-family: "Space Grotesk", sans-serif; font-weight: 700; font-size: 64px; letter-spacing: -.02em;
        margin: 0 0 18px; }}
  h1 span {{ background: linear-gradient(100deg, #22d3ee, #7c5cff 50%, #f0469b); -webkit-background-clip: text;
             background-clip: text; color: transparent; }}
  p {{ font-size: 27px; color: #3a4466; margin: 0; max-width: 30em; line-height: 1.4; }}
  .bar {{ position: absolute; left: 0; right: 0; bottom: 0; height: 8px;
          background: linear-gradient(100deg, #22d3ee, #7c5cff 50%, #f0469b); }}
</style></head>
<body>
  <div class="logo">{logo}</div>
  <h1>{title_a} <span>{title_b}</span></h1>
  <p>{lead}</p>
  <div class="bar"></div>
</body></html>
"""


def find_browser(explicit: str | None) -> str:
    for b in ([explicit] if explicit else BROWSERS):
        if Path(b).exists() or shutil.which(b):
            return b
    sys.exit("no Chrome/Edge found; pass --browser PATH")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--browser", help="path of a Chromium-based browser")
    args = ap.parse_args()

    site = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))["site"]
    # The light-theme wordmark: drop the dark-mode rule so the card looks the same everywhere.
    logo = (ROOT / "static" / "img" / "logo.svg").read_text(encoding="utf-8")
    logo = logo.replace("@media (prefers-color-scheme: dark) { svg { --ink: #eef1ff; } }", "")
    head, _, last = site["tagline"].rstrip(".").rpartition(" ")
    html = PAGE.format(w=W, h=H, logo=logo, title_a=head, title_b=last + ".",
                       lead="Methods, limits, people and open questions — with new arXiv papers tracked every day.")

    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "card.html"
        page.write_text(html, encoding="utf-8")
        shot = Path(tmp) / "card.png"
        subprocess.run([find_browser(args.browser), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", f"--window-size={W},{H}", "--virtual-time-budget=4000",
                        f"--screenshot={shot}", page.as_uri()], check=True, capture_output=True, timeout=120)
        OUT.write_bytes(shot.read_bytes())
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
