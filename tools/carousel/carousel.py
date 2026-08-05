#!/usr/bin/env python3
"""
carousel.py — ShikshaLokam Research-Insight carousel maker.

Config-driven: feed it a JSON spec (theme + slides) and it renders square
1080x1080 slides as PNGs + a combined PDF (ready for a LinkedIn document post).
Renders via headless Chrome/Edge (same engine the report-maker uses), so we get
real web fonts and pixel-exact 1:1 slides.

House style (matches the team's Canva research-insight template):
  · warm CREAM / linen background (dominant)
  · MAROON accents — centred heading, corner arcs, the » scroll arrow, big stats
  · body text inside a WHITE rounded card;  [[phrase]] -> teal highlight
  · ShikshaLokam logo top-right
Fonts: Nunito = headings, Montserrat = body.

Usage:
  python tools/carousel/carousel.py tools/carousel/aser-2024.json
"""
import base64, html, json, re, subprocess, sys, tempfile, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
LOGO = REPO / ".claude" / "signature-assets" / "logo.png"

CHROME = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

def chrome_path():
    for c in CHROME:
        if Path(c).exists():
            return c
    sys.exit("No Chrome/Edge found for rendering.")

def esc(s):
    return html.escape(str(s))

def b64(p):
    p = Path(p)
    return ("data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()) if p.exists() else ""

THEME = {"cream": "#ebe6dc", "maroon": "#ab3935", "ink": "#2a2320",
         "teal": "#1f7a8c", "card": "#ffffff"}

# subtle linen grain, drawn once as an SVG noise overlay
NOISE = ("data:image/svg+xml;utf8,"
         "<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/>"
         "<feColorMatrix type='saturate' values='0'/></filter>"
         "<rect width='100%25' height='100%25' filter='url(%23n)' opacity='0.5'/></svg>")

def arcs(color, flip=False):
    # three concentric quarter-arcs (the "listening" signal motif)
    rot = "rotate(180 90 90)" if flip else ""
    paths = "".join(
        f"<path d='M {90-r} 90 A {r} {r} 0 0 1 90 {90-r}' fill='none' "
        f"stroke='{color}' stroke-width='6' stroke-linecap='round' opacity='0.55'/>"
        for r in (34, 58, 82))
    return (f"<svg width='180' height='180' viewBox='0 0 180 180'><g transform='{rot}'>"
            f"{paths}</g></svg>")

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Nunito:wght@700;800;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1080px;overflow:hidden}
.slide{width:1080px;height:1080px;position:relative;background:var(--cream);
  font-family:'Montserrat','Segoe UI',system-ui,Arial,sans-serif;overflow:hidden}
.slide::before{content:'';position:absolute;inset:0;background-image:url("__NOISE__");
  background-size:300px 300px;mix-blend-mode:multiply;opacity:.35;pointer-events:none}
.pad{position:absolute;inset:0;padding:92px 84px;display:flex;flex-direction:column;z-index:2}
.logo{position:absolute;top:70px;right:84px;height:52px;z-index:3}
.arc-tl{position:absolute;top:30px;left:30px;z-index:1;opacity:.9}
.arc-br{position:absolute;bottom:150px;right:40px;z-index:1;opacity:.9}
.content{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:26px;padding-top:60px}
.eyebrow{font-family:'Montserrat';font-weight:700;text-transform:uppercase;letter-spacing:.18em;font-size:23px;color:var(--maroon)}
.head{font-family:'Nunito',sans-serif;font-weight:900;line-height:1.08;color:var(--maroon);font-size:56px;max-width:900px}
.stat{font-family:'Nunito',sans-serif;font-weight:900;line-height:1;color:var(--maroon);font-size:158px}
.card{background:var(--card);border-radius:22px;padding:44px 48px;box-shadow:0 18px 44px rgba(70,30,30,.14);
  font-family:'Montserrat';font-weight:500;font-size:29px;line-height:1.5;color:var(--ink);text-align:left}
.card .hi{color:var(--teal);font-weight:600}
.foot{position:absolute;bottom:74px;left:84px;right:84px;display:flex;justify-content:space-between;
  align-items:flex-end;font-family:'Montserrat';font-weight:700;font-size:20px;color:var(--maroon);z-index:3}
.arrow{font-family:'Nunito';font-weight:900;font-size:40px;color:var(--maroon);letter-spacing:-2px}
"""

def fmt_body(text):
    text = esc(text)
    return re.sub(r"\[\[(.+?)\]\]", r"<span class='hi'>\1</span>", text)

def render_slide_html(sl, theme, n, total):
    kind = sl.get("kind", "stat")
    logo = b64(LOGO)
    logo_html = f'<img class="logo" src="{logo}">' if logo else ''
    top = []
    if kind == "stat":
        if sl.get("eyebrow"):
            top.append(f'<div class="eyebrow">{esc(sl["eyebrow"])}</div>')
        if sl.get("big"):
            top.append(f'<div class="stat">{esc(sl["big"])}</div>')
    else:
        if sl.get("eyebrow"):
            top.append(f'<div class="eyebrow">{esc(sl["eyebrow"])}</div>')
        if sl.get("big"):
            top.append(f'<div class="head">{esc(sl["big"])}</div>')
    card = f'<div class="card">{fmt_body(sl["body"])}</div>' if sl.get("body") else ""
    scroll = "Scroll through the slides \u203a" if n == 1 else ""
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>"
            f"{CSS.replace('__NOISE__', NOISE)}</style></head><body>"
            f'<div class="slide" style="--cream:{theme["cream"]};--maroon:{theme["maroon"]};'
            f'--ink:{theme["ink"]};--teal:{theme["teal"]};--card:{theme["card"]}">'
            f'{logo_html}'
            f'<div class="arc-tl">{arcs(theme["maroon"])}</div>'
            f'<div class="arc-br">{arcs(theme["maroon"], flip=True)}</div>'
            f'<div class="pad"><div class="content">{"".join(top)}</div>{card}</div>'
            f'<div class="foot"><span>{scroll}</span>'
            f'<span>{n}/{total} &nbsp; <span class="arrow">\u00bb</span></span></div>'
            f"</div></body></html>")

def render_png(html_str, out_png):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html_str); tmp = f.name
    try:
        subprocess.run([chrome_path(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2", "--window-size=1080,1080",
                        "--virtual-time-budget=5000",
                        f"--screenshot={out_png}", "file:///" + tmp.replace(os.sep, "/")],
                       check=True, capture_output=True, timeout=90)
    finally:
        os.unlink(tmp)

def main(spec_path):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    theme = {**THEME, **spec.get("theme", {})}
    slides = spec["slides"]
    slug = spec.get("slug", "carousel")
    total = len(slides)
    pngs = []
    for i, sl in enumerate(slides, 1):
        out_png = str(OUT / f"{slug}-{i:02d}.png")
        render_png(render_slide_html(sl, theme, i, total), out_png)
        pngs.append(out_png); print("rendered", out_png)
    try:
        from PIL import Image
        imgs = [Image.open(p).convert("RGB") for p in pngs]
        pdf = str(OUT / f"{slug}.pdf")
        imgs[0].save(pdf, save_all=True, append_images=imgs[1:])
        print("PDF:", pdf)
    except Exception as e:
        print("PDF skipped:", e)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(HERE / "aser-2024.json"))
