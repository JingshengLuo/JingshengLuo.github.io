#!/usr/bin/env python3
"""Render 1200x630 preview cards in the site's own visual language.

The point of /posts/2026/07/preview-image-fidelity/ is that a card image
should be the right size and the right shape. These are.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
OUT = ROOT / "images"

TPL = """
<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:"Newsreader"; src:url("file://{fonts}/newsreader-latin.woff2") format("woff2");
              font-weight:200 800; }}
@font-face {{ font-family:"Newsreader"; font-style:italic;
              src:url("file://{fonts}/newsreader-latin-italic.woff2") format("woff2"); font-weight:200 700; }}
@font-face {{ font-family:"Inter"; src:url("file://{fonts}/inter-latin.woff2") format("woff2");
              font-weight:100 900; }}
@font-face {{ font-family:"Plex"; src:url("file://{fonts}/plex-mono-500.woff2") format("woff2"); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1200px; height:630px; background:#F0EEE6; color:#191919;
        font-family:"Inter",sans-serif; position:relative; overflow:hidden; }}
.grain {{ position:absolute; inset:0; opacity:.55; mix-blend-mode:multiply;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='260' height='260'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.82' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='260' height='260' filter='url(%23n)' opacity='0.38'/%3E%3C/svg%3E");
  background-size:260px 260px; }}
.dots {{ position:absolute; inset:0; opacity:.6;
  background-image:radial-gradient(#C4BDAB .6px, transparent .6px); background-size:9px 9px;
  -webkit-mask-image:radial-gradient(ellipse 55% 55% at 82% 82%, #000 10%, transparent 72%); }}
.frame {{ position:absolute; inset:44px; border:1px solid #DCD7C9; }}
.inner {{ position:absolute; inset:0; display:flex; flex-direction:column;
          align-items:center; justify-content:center; text-align:center;
          padding:0 120px; }}
.eyebrow {{ font-size:15px; font-weight:600; letter-spacing:.18em; text-transform:uppercase;
            color:#6CABDD; margin-bottom:28px; }}
h1 {{ font-family:"Newsreader",serif; font-weight:400; letter-spacing:-.02em;
      line-height:1.12; color:#191919; font-size:{size}px; max-width:900px; }}
.rule {{ width:56px; height:2px; background:#6CABDD; margin:30px 0; }}
.sub {{ font-size:17px; color:#56524A; line-height:1.55; max-width:760px; }}
.foot {{ position:absolute; left:0; right:0; bottom:74px; text-align:center;
         font-family:"Plex",monospace; font-size:13px; letter-spacing:.14em;
         text-transform:uppercase; color:#868074; }}
</style></head><body>
  <div class="dots"></div>
  <div class="frame"></div>
  <div class="inner">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{title}</h1>
    <div class="rule"></div>
    <div class="sub">{sub}</div>
  </div>
  <div class="foot">{foot}</div>
  <div class="grain"></div>
</body></html>
"""

CARDS = [
    dict(
        name="og-default",
        eyebrow="Xi&rsquo;an Jiaotong University",
        title="Zhengqian Jin",
        size=76,
        sub="Ph.D. candidate in energy storage — lithium metal batteries, anode-free cells, "
            "interfacial kinetics, and the workflow design that keeps research legible.",
        foot="jingshengluo.github.io",
    ),
    dict(
        name="og-preview-fidelity",
        eyebrow="Preprint · Opinion",
        title="Preview Image Fidelity Across Six Publishing Platforms",
        size=58,
        sub="What image actually reaches a social preview card, and at what resolution? "
            "Presence of an <i>og:image</i> is not the same thing as a legible card.",
        foot="Zhengqian Jin · 26 July 2026",
    ),
]


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        for c in CARDS:
            pg.set_content(TPL.format(fonts=FONTS, **c), wait_until="load")
            pg.wait_for_timeout(500)
            png = OUT / f"{c['name']}.png"
            pg.screenshot(path=str(png))
            im = Image.open(png).convert("RGB")
            jpg = OUT / f"{c['name']}.jpg"
            im.save(jpg, "JPEG", quality=90, optimize=True, progressive=True)
            png.unlink()
            print(f"  {jpg.name}  {im.size}  {jpg.stat().st_size/1024:.0f} KB")
        b.close()


if __name__ == "__main__":
    main()
