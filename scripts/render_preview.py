#!/usr/bin/env python3
"""Render GitHub-like previews of README.md into preview/.

Needs Playwright (pip install playwright && playwright install chromium).
Serves the repo over localhost so the SVGs load as <img> exactly as on
GitHub, then screenshots the page at several moments of the animation and
records a short video of the hero.

    python3 scripts/render_preview.py
"""

from __future__ import annotations

import functools
import http.server
import subprocess
import threading
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "preview"
PORT = 8765

GH = {
    "dark": dict(bg="#0d1117", fg="#e6edf3", muted="#8d96a0", border="#30363d", box="#0d1117", head="#161b22"),
    "light": dict(bg="#ffffff", fg="#1f2328", muted="#59636e", border="#d1d9e0", box="#ffffff", head="#f6f8fa"),
}


def page_html(theme: str, mobile: bool) -> str:
    c = GH[theme]
    readme = (ROOT / "README.md").read_text()
    side = "" if mobile else f"""
      <aside style="width:296px;flex:none">
        <div style="width:296px;height:296px;border-radius:50%;background:{c['head']};border:1px solid {c['border']}"></div>
        <div style="font-size:24px;font-weight:600;margin-top:16px">Abduaziz Umarov</div>
        <div style="font-size:20px;color:{c['muted']};font-weight:300">azizu06</div>
      </aside>"""
    return f"""<!doctype html><html><head><meta charset="utf-8">
<base href="/">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
 body{{margin:0;background:{c['bg']};color:{c['fg']};font:14px -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif}}
 .wrap{{display:flex;gap:24px;max-width:1280px;margin:0 auto;padding:{'16px' if mobile else '32px 24px'}}}
 .box{{flex:1;min-width:0;border:1px solid {c['border']};border-radius:6px;background:{c['box']}}}
 .head{{padding:8px 16px;font-size:12px;color:{c['muted']};border-bottom:1px solid {c['border']}}}
 article{{padding:{'16px' if mobile else '24px'}}}
 article p{{margin:0 0 16px}} img{{max-width:100%;vertical-align:middle}}
</style></head><body><div class="wrap">{side}
<div class="box"><div class="head">azizu06 / README.md</div><article>{readme}</article></div></div></body></html>"""


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

    handler = functools.partial(Quiet, directory=str(ROOT))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    OUT.mkdir(exist_ok=True)
    for theme in ("dark", "light"):
        for mobile in (False, True):
            (OUT / f"_page-{theme}{'-m' if mobile else ''}.html").write_text(page_html(theme, mobile))
    srv = serve()
    base = f"http://127.0.0.1:{PORT}/preview"
    with sync_playwright() as p:
        b = p.chromium.launch()
        # full-page screenshots, taken after the shell finishes (static end state)
        for theme in ("dark", "light"):
            for mobile in (False, True):
                vp = dict(width=390, height=844) if mobile else dict(width=1280, height=900)
                ctx = b.new_context(viewport=vp, color_scheme=theme, device_scale_factor=2)
                pg = ctx.new_page()
                pg.goto(f"{base}/_page-{theme}{'-m' if mobile else ''}.html")
                pg.wait_for_timeout(30000 if mobile else 32000)
                name = f"{'mobile' if mobile else 'desktop'}-{theme}.png"
                pg.screenshot(path=str(OUT / name), full_page=True)
                ctx.close()
                print("wrote", name)
        # animation frames of the desktop dark hero
        ctx = b.new_context(viewport=dict(width=1280, height=900), color_scheme="dark",
                            device_scale_factor=2, record_video_dir=str(OUT / "_video"),
                            record_video_size=dict(width=1280, height=900))
        pg = ctx.new_page()
        t0 = time.time()
        pg.goto(f"{base}/_page-dark.html")
        hero = pg.locator("article img").first
        for i, at in enumerate([2.6, 4.4, 12.0, 19.0, 29.0]):
            pg.wait_for_timeout(max(0, (at - (time.time() - t0)) * 1000))
            hero.screenshot(path=str(OUT / f"frame-{i + 1}-t{at:g}s.png"))
            print("frame", at)
        pg.wait_for_timeout(max(0, (36.5 - (time.time() - t0)) * 1000))
        video = pg.video.path()
        box = hero.bounding_box()
        ctx.close()
        b.close()
    srv.shutdown()
    x, y, w, h = (int(box[k]) for k in ("x", "y", "width", "height"))
    w, h = w - w % 2, h - h % 2
    mp4 = OUT / "hero-dark.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-vf",
                    f"crop={w}:{h}:{x}:{y}", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "20", str(mp4)], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(OUT / "hero-dark.gif")], check=True)
    for f in (OUT / "_video").glob("*"):
        f.unlink()
    (OUT / "_video").rmdir()
    print("wrote hero-dark.mp4 and hero-dark.gif")


if __name__ == "__main__":
    main()
