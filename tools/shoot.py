#!/usr/bin/env python3
"""Screenshot the rendered preview at desktop and phone widths."""
import functools, http.server, socketserver, threading, sys, os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PREVIEW = ROOT / "_preview"
SHOTS = ROOT / "_shots"
PORT = 8899

PAGES = [
    ("home", "/"),
    ("publications", "/publications/"),
    ("writing", "/year-archive/"),
    ("preprint", "/posts/2026/07/preview-image-fidelity/"),
    ("toolkit", "/toolkit/"),
    ("cv", "/cv/"),
]


def serve():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(PREVIEW))
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main():
    dark = "--dark" in sys.argv
    SHOTS.mkdir(exist_ok=True)
    httpd = serve()
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--force-color-profile=srgb"])
        for label, width, height, full in (("desktop", 1440, 900, True), ("phone", 390, 844, True)):
            ctx = browser.new_context(viewport={"width": width, "height": height},
                                      device_scale_factor=2 if width < 500 else 1.5)
            page = ctx.new_page()
            for name, url in PAGES:
                page.goto(f"http://127.0.0.1:{PORT}{url}", wait_until="networkidle", timeout=45000)
                if dark:
                    page.evaluate("document.documentElement.setAttribute('data-theme','dark')")
                page.wait_for_timeout(700)
                suffix = "-dark" if dark else ""
                out = SHOTS / f"{name}-{label}{suffix}.png"
                page.screenshot(path=str(out), full_page=full)
                print("  ", out.name, f"{out.stat().st_size/1024:.0f} KB")
            ctx.close()
        browser.close()
    httpd.shutdown()


if __name__ == "__main__":
    main()
