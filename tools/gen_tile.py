#!/usr/bin/env python3
"""Generate the typographic cover tile used on the Toolkit card for AtomPub."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
OUT = ROOT / "images" / "tools"

HTML = f"""
<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:"Newsreader"; src:url("file://{FONTS}/newsreader-latin.woff2") format("woff2"); font-weight:200 800; }}
@font-face {{ font-family:"Plex"; src:url("file://{FONTS}/plex-mono-400.woff2") format("woff2"); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:720px; height:405px; background:#F7F5EF; position:relative; overflow:hidden;
        display:flex; flex-direction:column; align-items:center; justify-content:center; }}
.dots {{ position:absolute; inset:0; opacity:.85;
  background-image:radial-gradient(#C4BDAB .7px, transparent .7px); background-size:11px 11px;
  -webkit-mask-image:radial-gradient(ellipse 62% 62% at 50% 50%, transparent 22%, #000 78%); }}
.bar {{ position:absolute; top:0; left:0; right:0; height:6px; background:#6CABDD; }}
h1 {{ font-family:"Newsreader",serif; font-weight:400; font-size:78px; color:#191919;
      letter-spacing:-.025em; position:relative; }}
.sub {{ font-family:"Plex",monospace; font-size:14px; letter-spacing:.24em; text-transform:uppercase;
        color:#868074; margin-top:20px; position:relative; }}
.rule {{ width:44px; height:1px; background:#6CABDD; margin-top:26px; position:relative; }}
</style></head><body>
  <div class="dots"></div><div class="bar"></div>
  <h1>AtomPub</h1>
  <div class="sub">Markdown &middot; In &nbsp; Pages &middot; Out</div>
  <div class="rule"></div>
</body></html>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 720, "height": 405}, device_scale_factor=2)
        pg.set_content(HTML, wait_until="load")
        pg.wait_for_timeout(400)
        png = OUT / "atompub.png"
        pg.screenshot(path=str(png))
        b.close()
    im = Image.open(png).convert("RGB")
    im.thumbnail((1080, 1080), Image.LANCZOS)
    im.save(png, "PNG", optimize=True)
    print(f"  {png.name}  {im.size}  {png.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    main()
