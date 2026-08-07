#!/usr/bin/env python3
"""ShikshaLokam report-maker (v1).

Input:  a content JSON (the report's structured content — see asc-3-0.json).
Output: a brand-styled, multi-page PDF (no Canva), via headless Chrome.

    python tools/report/build_report.py tools/report/asc-3-0.json

Brand: Earth Maroon #ab3935 · Violet #391949 · Vienna Dawn #f6efef · Dynamic Grey
#1e1e1e · cream #fff9e4 · accents green #43a53f / coral #ffaea8 · Montserrat + Nunito.

v2 (next): read the content straight from a Google Doc via tools/gsuite/gs.py so the
team only edits a Doc. This v1 proves the template + PDF pipeline.
"""
import base64, html, json, math, subprocess, sys
from urllib.parse import quote
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
ASSETS = HERE / "assets"
LOGO = REPO / ".claude" / "signature-assets" / "logo.png"
SCERT = ASSETS / "scert-haryana.png"

CHROME = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

def chrome_path():
    for c in CHROME:
        if Path(c).exists():
            return c
    sys.exit("No Chrome/Edge found for PDF rendering.")

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml"}

def rp(p):
    """Resolve a content path: relative paths hang off tools/report/, not the cwd."""
    p = Path(p)
    return p if p.is_absolute() else (HERE / p)

MAX_EDGE = 1600   # a photo wider than this adds file size, not print detail
CACHE = HERE / ".imgcache"

def _fit(p):
    """Downscale an oversized photo once and reuse it. A 4624px camera frame is
    ~5MB embedded and prints no better than 1600px — full-res photos were making
    the PDF 16MB, too big for some viewers to open."""
    if p.suffix.lower() not in (".jpg", ".jpeg", ".png"):
        return p.read_bytes(), MIME.get(p.suffix.lower(), "image/png")
    try:
        from PIL import Image
    except ImportError:
        return p.read_bytes(), MIME.get(p.suffix.lower(), "image/png")
    st = p.stat()
    CACHE.mkdir(exist_ok=True)
    key = CACHE / f"{p.stem}-{int(st.st_mtime)}-{st.st_size}-{MAX_EDGE}.jpg"
    if key.exists():
        return key.read_bytes(), "image/jpeg"
    im = Image.open(p)
    if max(im.size) <= MAX_EDGE:
        return p.read_bytes(), MIME.get(p.suffix.lower(), "image/png")
    im = im.convert("RGB")
    im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
    im.save(key, "JPEG", quality=86, optimize=True)
    return key.read_bytes(), "image/jpeg"

def b64(p):
    p = rp(p)
    data, mime = _fit(p)
    return f"data:{mime};base64," + base64.b64encode(data).decode()

def b64_opt(p):
    return b64(p) if rp(p).exists() else ""

def esc(s):
    return html.escape(str(s))

# ---- theme (per-report colour mix) — dept blue (lead) · SL maroon · brand pink -
# Mapped onto the stylesheet's existing role-vars so a new report only swaps hexes:
#   --maroon = dominant (department blue) · --violet = SL maroon (headings/accents)
#   --green  = maroon (green removed)     · --coral  = brand pink (highlight)
DEFAULT_THEME = {"primary": "#183090", "secondary": "#ab3935", "accent": "#ffaea8",
                 "cream": "#fff9e4", "tint": "#eef1f7", "ink": "#2a2320"}

def theme_style(doc):
    t = {**DEFAULT_THEME, **doc.get("theme", {})}
    return (":root{"
            f"--maroon:{t['primary']};"
            f"--violet:{t['secondary']};"
            f"--green:{t['secondary']};"
            f"--coral:{t['accent']};"
            f"--cream:{t['cream']};--dawn:{t['tint']};--ink:{t['ink']};"
            # one colour for every motif piece, inline SVG and CSS alike
            f"--motif:{t['secondary']};--coral2:#c2564f;"
            "}")

# ---- SL motif kit — the nested corner-arcs UNIT, composed into a system:
#      arcs()  = the raw quarter unit (rotatable to any corner)
#      ring()  = four units => concentric rings (frames, watermarks, bullets)
#      arch()  = two units => an arch / rainbow (headers, image tops)
def _arc_paths(color, size, sw, radii, quads):
    """quads: which quarter-turns to draw (0..3). 0=bottom-right of origin."""
    out = ""
    cx = cy = size / 2
    for q in quads:
        a0 = math.radians(q * 90)
        for f in radii:
            r = f * size / 2
            x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
            x1, y1 = cx + r * math.cos(a0 + math.pi / 2), cy + r * math.sin(a0 + math.pi / 2)
            out += (f'<path d="M {x0:.1f} {y0:.1f} A {r:.1f} {r:.1f} 0 0 1 {x1:.1f} {y1:.1f}" '
                    f'fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')
    return out

NS = 'xmlns="http://www.w3.org/2000/svg"'

def _svg(inner, size, op):
    return (f'<svg {NS} width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
            f'style="opacity:{op};overflow:visible">{inner}</svg>')

def arcs(color, size=200, sw=16, radii=(0.6, 1.2, 1.8), op=1.0, rot=0):
    # single corner unit: place at a corner, arcs sweeping inward
    p = ""
    for f in radii:
        r = f * size / 2
        p += (f'<path d="M {r:.1f} 0 A {r:.1f} {r:.1f} 0 0 1 0 {r:.1f}" fill="none" '
              f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')
    return (f'<svg {NS} width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
            f'style="opacity:{op};transform:rotate({rot}deg);overflow:visible">{p}</svg>')

def ring(color, size=200, sw=14, radii=(0.34, 0.62, 0.9), op=1.0):
    return _svg(_arc_paths(color, size, sw, radii, (0, 1, 2, 3)), size, op)

def arch(color, size=200, sw=14, radii=(0.34, 0.62, 0.9), op=1.0):
    return _svg(_arc_paths(color, size, sw, radii, (2, 3)), size, op)

def wave(color, n=7, unit=26, sw=3.6, radii=(0.4, 0.7, 1.0), op=1.0):
    """The unit repeated along a line — a scallop band. Used for every rule and
    divider, so the same shape that decorates the cover also separates sections."""
    w, h = n * unit, unit / 2 + sw
    inner = ""
    for i in range(n):
        cx = i * unit + unit / 2
        for f in radii:
            r = f * unit / 2
            inner += (f'<path d="M {cx - r:.1f} {h - sw / 2:.1f} A {r:.1f} {r:.1f} 0 0 1 '
                      f'{cx + r:.1f} {h - sw / 2:.1f}" fill="none" stroke="{color}" '
                      f'stroke-width="{sw}" stroke-linecap="round"/>')
    return (f'<svg {NS} width="{w}" height="{h:.1f}" viewBox="0 0 {w} {h:.1f}" '
            f'style="opacity:{op};overflow:visible">{inner}</svg>')

def data_uri(svg):
    # base64 rather than percent-encoding: no quoting traps with '#' in hex colours
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode()

def motif_style():
    """Motif pieces that have to live in CSS (bullets, watermarks) — same unit,
    just composed differently and handed to the stylesheet as data URIs."""
    bullet = data_uri(arcs("#ab3935", 20, 4.2, radii=(0.5, 1.0, 1.5)))
    band = data_uri(wave("#ab3935", 40, 22, 3.2))
    return (f'.motif-bullet{{--u:url("{bullet}")}}'
            f'.motif-band{{--u:url("{band}")}}'
            f'ul.b li::before{{background-image:url("{bullet}")}}'
            f'.rulewrap{{background-image:url("{band}")}}'
            f'.callout::after{{background-image:url("{bullet}")}}')

FONTS = ASSETS / "fonts"

def font_face():
    """Inline the faces. An @import to a font CDN is invisible in headless print
    (and blocked outright when the page is published), so it must not be relied on."""
    out = ""
    for f in sorted(FONTS.glob("*.woff2")):
        fam, wt = f.stem.rsplit("-", 1)
        fam = "Montserrat" if fam.startswith("Montserrat") else fam
        b = base64.b64encode(f.read_bytes()).decode()
        out += (f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{wt};"
                f"font-display:block;src:url(data:font/woff2;base64,{b}) format('woff2');}}")
    return out

def trim_alpha(p):
    """Crop a logo's transparent margin. The SL mark carries 25% empty space on top,
    SCERT's is padded evenly — sized by file height they end up different optical
    sizes sitting at different heights. Cropping to the ink lets them align."""
    p = rp(p)
    try:
        from PIL import Image
    except ImportError:
        return p
    CACHE.mkdir(exist_ok=True)
    st = p.stat()
    key = CACHE / f"trim-{p.stem}-{int(st.st_mtime)}-{st.st_size}.png"
    if not key.exists():
        im = Image.open(p).convert("RGBA")
        box = im.split()[-1].getbbox()
        (im.crop(box) if box else im).save(key, "PNG")
    return key

def cobrand_lockup(h=64):
    # SCERT is a round seal; a disc reads smaller than a wordmark at equal height,
    # so it takes a little more to sit level with the ShikshaLokam mark.
    scert = (f'<span class="dv"></span>'
             f'<img class="seal" src="{b64(trim_alpha(SCERT))}" alt="SCERT Haryana">'
             if SCERT.exists() else "")
    return (f'<span class="lockup" style="--lh:{h}px">'
            f'<img src="{b64(trim_alpha(LOGO))}" alt="ShikshaLokam">{scert}</span>')

def divider():
    return '<div class="rulewrap"></div>'

# ---- brand + print stylesheet ------------------------------------------------
CSS = """
:root{
  --maroon:#ab3935; --violet:#391949; --dawn:#f6efef; --grey:#1e1e1e;
  --cream:#fff9e4; --green:#43a53f; --coral:#ffaea8; --ink:#2a2320; --muted:#6b625f;
}
*{box-sizing:border-box; margin:0; padding:0;}
@page{ size:A4; margin:0; }
html{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body{ font-family:'Nunito',system-ui,Arial,sans-serif; color:var(--ink); font-size:11.2pt; line-height:1.55; }
h1,h2,h3,h4{ font-family:'Montserrat',system-ui,Arial,sans-serif; color:var(--violet);
  line-height:1.15; text-wrap:balance; }
.page{ position:relative; width:210mm; min-height:297mm; padding:22mm 20mm 24mm; page-break-after:always; overflow:hidden; }
.page:last-child{ page-break-after:auto; }
.flowpage{ height:297mm; min-height:0; }
.flowpage .fbody{ display:flow-root; }
.fitem{ break-inside:avoid; }
#flow{ position:absolute; visibility:hidden; width:170mm; left:-9999px; }

/* cover */
.cover{ background:var(--maroon); color:#fff; padding:0; display:flex; flex-direction:column; }
.cover .band{ flex:1; padding:26mm 20mm; display:flex; flex-direction:column; }
.cover .logo-chip{ background:#fff; border-radius:14px; padding:12px 16px; align-self:flex-start; box-shadow:0 6px 24px rgba(0,0,0,.18); }
.cover .logo-chip img{ height:52px; display:block; }
.cover .eyebrow{ margin-top:auto; font-family:'Montserrat'; font-weight:600; letter-spacing:.14em; text-transform:uppercase; font-size:10.5pt; color:var(--coral); }
.cover h1{ color:#fff; font-size:40pt; font-weight:800; margin:10px 0 6px; }
.cover .sub{ font-size:15pt; color:#ffe7e5; font-weight:600; font-family:'Montserrat'; }
.cover .meta{ margin-top:20px; font-size:11pt; color:#ffd9d6; line-height:1.8; }
.cover .foot{ background:var(--violet); color:#fff; padding:10mm 20mm; font-family:'Montserrat'; font-weight:600; font-size:10.5pt; display:flex; justify-content:space-between; }

/* section chrome */
.kicker{ display:flex; align-items:center; gap:10px; margin-bottom:14px; }
.kicker .num{ background:var(--maroon); color:#fff; font-family:'Montserrat'; font-weight:700; font-size:12pt; width:30px; height:30px; border-radius:8px; display:flex; align-items:center; justify-content:center; }
.kicker h2{ font-size:20pt; font-weight:700; }
.rule{ height:9px; width:78px; background:none; background-repeat:no-repeat;
  background-size:auto 100%; margin:2px 0 16px; }
.rulewrap{ height:14px; width:106px; background-repeat:no-repeat; background-size:auto 100%;
  margin:6px 0 12px; }
.lockup{ display:inline-flex; gap:20px; align-items:center; }
.lockup img{ height:var(--lh,50px); width:auto; display:block; }
.lockup img.seal{ height:calc(var(--lh,50px)*1.12); }
.lockup .dv{ width:1px; height:calc(var(--lh,50px)*0.82); background:#0000001f; }
/* Cover C — framed / centered, image-rich */
.coverc{ background:var(--cream); display:flex; flex-direction:column; align-items:center; text-align:center; padding:22mm 22mm 0; overflow:hidden; }
.coverc .cc{ position:absolute; line-height:0; pointer-events:none; }
.coverc .cc-tl{ left:-34mm; top:-34mm; } .coverc .cc-br{ right:-34mm; bottom:-34mm; }
.coverc .lock{ margin-bottom:9mm; }
.coverc .eye{ font-family:'Montserrat'; font-weight:600; letter-spacing:.16em; text-transform:uppercase; font-size:10.5pt; color:var(--violet); }
.coverc h1{ color:var(--maroon); font-size:32pt; font-weight:800; margin:8px 0 6px; }
.coverc .sub{ font-family:'Montserrat'; font-weight:600; font-size:12.5pt; color:var(--violet); }
.coverc .meta{ color:#6b625f; font-size:10.4pt; line-height:1.8; margin-top:7mm; }
.cphotos{ display:grid; grid-template-columns:repeat(3,1fr); gap:9px; width:100%; margin:9mm 0 0; }
.cphotos .ct{ aspect-ratio:1/1; border-radius:10px; overflow:hidden; box-shadow:0 6px 18px rgba(0,0,0,.12); }
/* the arc unit as a photo frame — top corners rounded into the motif's sweep */
.cphotos .ct:nth-child(1){ border-radius:26mm 10px 10px 10px; }
.cphotos .ct:nth-child(6){ border-radius:10px 10px 26mm 10px; }
/* full-bleed foot band — the department colour closes the page */
.cband{ margin-top:auto; width:calc(100% + 44mm); margin-left:-22mm; background:var(--maroon); color:#fff;
        padding:8mm 22mm; display:flex; justify-content:space-between; align-items:center; text-align:left;
        font-family:'Montserrat'; font-weight:600; font-size:10.5pt; }
.cband .r{ text-align:right; opacity:.85; font-weight:500; }
.cphotos .ct img{ width:100%; height:100%; object-fit:cover; display:block; }
.cphotos .ph{ background:var(--dawn); display:flex; align-items:center; justify-content:center; color:#9aa4bf; font-family:'Montserrat'; font-weight:700; font-size:8.5pt; }
/* Section — number rail (S1) */
.page.sec{ padding:0; }
.sec .rail{ position:absolute; left:0; top:0; bottom:0; width:26mm; background:var(--maroon); overflow:hidden; }
.sec .rail .rnum{ position:absolute; left:6mm; top:20mm; font-family:'Montserrat'; font-weight:800; color:#fff; font-size:40pt; line-height:1; }
.sec .rail .rarcs{ position:absolute; left:-14mm; bottom:-14mm; }
.sec .secbody{ padding:22mm 20mm 24mm 40mm; }
.sec .secbody h2{ font-size:21pt; color:var(--violet); }
.sec .pfoot{ left:40mm; }
p{ margin:0 0 8px; text-wrap:pretty; }
.section-lead{ color:var(--muted); }

/* toc */
.toc-item{ display:flex; align-items:center; gap:14px; padding:11px 0; border-bottom:1px dashed #e4d7d6; }
.toc-item .n{ font-family:'Montserrat'; font-weight:700; color:var(--maroon); width:34px; }
.toc-item .t{ font-family:'Montserrat'; font-weight:600; color:var(--violet); font-size:12.5pt; }

/* lists */
ul.b{ list-style:none; margin:5px 0 10px; }
ul.b li{ position:relative; padding-left:22px; margin:6px 0; }
ul.b li::before{ content:''; position:absolute; left:0; top:5px; width:13px; height:13px;
  background-repeat:no-repeat; background-size:contain; }

/* tables */
table{ width:100%; border-collapse:collapse; margin:6px 0 12px; font-size:10.6pt; }
th{ background:var(--maroon); color:#fff; text-align:left; padding:10px 13px;
  font-family:'Montserrat'; font-weight:600; letter-spacing:.01em; }
td{ padding:10px 13px; border-bottom:1px solid #ece2e0; vertical-align:top; }
tr:nth-child(even) td{ background:color-mix(in srgb, var(--dawn) 62%, #fff); }
td.k{ font-weight:700; color:var(--violet); width:34%; background:#fff; }

/* callouts */
.callouts{ display:flex; flex-direction:column; gap:10px; }
.callout{ position:relative; overflow:hidden; border-left:4px solid var(--violet);
  background:var(--dawn); padding:11px 14px; border-radius:0 8px 8px 0; }
.callout::after{ content:''; position:absolute; right:9px; top:9px; width:15px; height:15px;
  background-repeat:no-repeat; background-size:contain; opacity:.5; transform:rotate(180deg); }
.callout h4{ font-size:12pt; margin-bottom:3px; color:var(--maroon); }
.callout p{ margin:0; color:var(--ink); font-size:10.6pt; }

/* stat cards */
.stats{ display:flex; gap:12px; flex-wrap:wrap; margin:6px 0 14px; }
.stat{ position:relative; overflow:hidden; flex:1; min-width:120px; background:var(--violet);
  color:#fff; border-radius:12px; padding:14px 16px; }
.stat .v{ font-variant-numeric:tabular-nums; font-family:'Montserrat'; font-weight:800; font-size:22pt; color:var(--cream); }
.stat .l{ font-size:9.6pt; color:#e9dcf0; margin-top:2px; }

/* bar chart */
.chart{ font-variant-numeric:tabular-nums; margin:6px 0 14px; }
.chart .row{ display:flex; align-items:center; gap:10px; margin:7px 0; }
.chart .lab{ width:34%; font-family:'Montserrat'; font-weight:600; font-size:10pt; color:var(--violet); }
.chart .track{ flex:1; background:var(--dawn); border-radius:6px; height:20px; overflow:hidden; }
.chart .fill{ height:100%; background:var(--maroon); border-radius:6px; }
.chart .val{ width:66px; text-align:right; font-family:'Montserrat'; font-weight:700; font-size:10pt; color:var(--maroon); }

/* evidence photo grid */
.grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin:8px 0; }
.ph{ aspect-ratio:4/3; background:var(--dawn); border-radius:10px; display:flex; align-items:center; justify-content:center; color:#9aa4bf; font-size:9pt; font-weight:700; font-family:'Montserrat'; }
.pht{ aspect-ratio:4/3; border-radius:10px; overflow:hidden; box-shadow:0 4px 14px rgba(0,0,0,.10); }
.phtwrap{ display:flex; flex-direction:column; gap:5px; }
.phtcap{ font-size:8.4pt; color:var(--muted); line-height:1.35; }
.evlist{ margin:0; }
.evrow + .evrow{ margin-top:8px; }
.evrow{ display:flex; gap:14px; align-items:stretch; margin:0; }
.fitem.evlist + .fitem.evlist{ margin-top:8px; }
.evthumb{ flex:0 0 45mm; aspect-ratio:4/3; border-radius:10px; overflow:hidden;
  background:var(--dawn); box-shadow:0 4px 14px rgba(0,0,0,.10); }
.evthumb img{ width:100%; height:100%; object-fit:cover; display:block; }
.evtext{ flex:1; display:flex; flex-direction:column; justify-content:center; }
.evtext h4{ font-size:11.5pt; color:var(--violet); margin-bottom:3px; }
.evtext p{ font-size:10.2pt; color:var(--ink); margin:0; }
.pht img{ width:100%; height:100%; object-fit:cover; display:block; }
.fig.arch{ border-radius:44% 44% 12px 12px / 17% 17% 4px 4px; }
.pht.arch{ border-radius:44% 44% 10px 10px / 20% 20% 4px 4px; }
.note{ background:var(--cream); border:1px solid #f0e4b8; border-radius:10px; padding:12px 15px; color:#7a6a2e; font-size:10.6pt; }

/* ---- borrowed layout vocabulary ---- */
.chip{ display:inline-flex; align-items:baseline; gap:9px; background:var(--c); color:#fff;
  font-family:'Montserrat'; font-weight:700; font-size:10pt; letter-spacing:.06em;
  text-transform:uppercase; padding:6px 13px; border-radius:4px; margin:2px 0 8px; }
.chip .cs{ font-weight:600; opacity:.85; letter-spacing:.03em; text-transform:none; font-size:9.4pt; }
.chvrow{ display:flex; align-items:stretch; gap:0; margin:4px 0 12px; }
.chv{ flex:1; border-top:4px solid var(--c); background:var(--dawn); border-radius:3px;
  padding:10px 12px 12px; }
.chv-h{ font-family:'Montserrat'; font-weight:700; font-size:10.5pt; color:var(--c); margin-bottom:3px; }
.chv-b{ font-size:9.8pt; color:var(--ink); line-height:1.45; }
.chv-a{ flex:0 0 22px; align-self:center; height:9px; position:relative; }
.chv-a::after{ content:''; position:absolute; left:4px; top:0; width:9px; height:9px;
  border-top:2px solid var(--muted); border-right:2px solid var(--muted); transform:rotate(45deg); }
.irows{ display:flex; flex-direction:column; gap:7px; margin:4px 0 12px; }
.irow{ display:flex; align-items:center; gap:11px; background:var(--dawn);
  border-left:3px solid var(--c); border-radius:0 6px 6px 0; padding:8px 12px; }
.ir-m{ flex:0 0 22px; line-height:0; }
.ir-t{ font-size:10.4pt; color:var(--ink); }
.pcts{ display:flex; flex-direction:column; gap:8px; margin:4px 0 12px; }
.pct{ display:flex; align-items:baseline; gap:12px; }
.pct .pv{ flex:0 0 auto; min-width:74px; font-family:'Montserrat'; font-weight:800; font-size:14pt;
  color:var(--c); font-variant-numeric:tabular-nums; }
.pct .pt{ font-size:10.5pt; color:var(--ink); }
/* subtle section number + header */
.shead{ display:flex; align-items:baseline; gap:12px; margin-bottom:2px; }
.shead .sn{ font-family:'Montserrat'; font-weight:700; font-size:11.5pt; color:var(--coral); }
.shead h2{ font-size:24pt; font-weight:800; letter-spacing:-.012em; }
.fitem.sec-start{ margin-top:11mm; }
.fbody > .fitem.sec-start:first-child{ margin-top:0; }
.subhead{ color:var(--maroon); font-size:12.5pt; margin:16px 0 3px; font-family:'Montserrat';
  font-weight:700; letter-spacing:.005em; }
.subhead + p, .subhead + ul.b, .subhead + .split{ margin-top:0; }
/* text-beside-image + figures */
.split{ display:flex; gap:18px; align-items:stretch; margin:6px 0 10px; }
.split>.c{ flex:1; min-width:0; }
.split>.figwrap{ flex:0 0 54mm; display:flex; flex-direction:column; }
.fig{ border-radius:12px; overflow:hidden; position:relative; flex:1; box-shadow:0 8px 20px rgba(24,48,144,.10); }
.fig img{ width:100%; height:100%; object-fit:cover; display:block; }
.figph{ width:100%; height:100%; min-height:52mm; background:var(--dawn); display:flex; align-items:center; justify-content:center; color:#9aa4bf; font-family:'Montserrat'; font-weight:700; font-size:8.5pt; text-align:center; padding:10px; }
.figcap{ font-size:8.6pt; color:var(--muted); margin-top:5px; font-family:'Montserrat'; }
/* toc hero image */
.toc-hero{ width:100%; height:60mm; border-radius:14px; overflow:hidden; margin:6px 0 9mm; background:var(--dawn); display:flex; align-items:center; justify-content:center; color:#9aa4bf; font-family:'Montserrat'; font-weight:700; box-shadow:0 8px 20px rgba(24,48,144,.10); }
.toc-hero img{ width:100%; height:100%; object-fit:cover; }
.shead .cont{ font-size:11pt; font-weight:600; color:var(--muted); }
.secmotif{ position:absolute; line-height:0; pointer-events:none; }

/* footer */
.pfoot{ font-variant-numeric:tabular-nums; position:absolute; left:20mm; right:20mm; bottom:12mm; display:flex; justify-content:space-between; font-family:'Montserrat'; font-size:8.5pt; color:var(--muted); border-top:1px solid #eadddb; padding-top:6px; }
"""

# ---- block renderers ---------------------------------------------------------
def r_paragraph(b): return f"<p>{esc(b['text'])}</p>"
def r_lead(b): return f"<p class='section-lead'>{esc(b['text'])}</p>"
def r_bullets(b):
    return "<ul class='b'>" + "".join(f"<li>{esc(x)}</li>" for x in b["items"]) + "</ul>"
def r_subhead(b): return f"<div class='subhead'>{esc(b['text'])}</div>"

def _fig_inner(img):
    img = img or {}
    src = img.get("src")
    if src and rp(src).exists():
        return f'<img src="{b64(src)}">'
    return f'<div class="figph">{esc(img.get("placeholder","PHOTO"))}</div>'

def r_figure(b):
    cap = f'<div class="figcap">{esc(b["caption"])}</div>' if b.get("caption") else ""
    h = b.get("h", "60mm")
    shape = " arch" if b.get("shape") == "arch" else ""
    return f'<div class="fig{shape}" style="height:{h}">{_fig_inner(b)}</div>{cap}'

def r_split(b):
    text = render_blocks(b["blocks"])
    cap = f'<div class="figcap">{esc(b["image"]["caption"])}</div>' if b.get("image", {}).get("caption") else ""
    figwrap = f'<div class="figwrap"><div class="fig">{_fig_inner(b.get("image"))}</div>{cap}</div>'
    col = f'<div class="c">{text}</div>'
    order = (col + figwrap) if b.get("side", "right") == "right" else (figwrap + col)
    return f'<div class="split">{order}</div>'
def r_table(b):
    head = ""
    if b.get("headers"):
        head = "<tr>" + "".join(f"<th>{esc(h)}</th>" for h in b["headers"]) + "</tr>"
    rows = ""
    for row in b["rows"]:
        if b.get("keyed"):
            rows += f"<tr><td class='k'>{esc(row[0])}</td><td>{esc(row[1])}</td></tr>"
        else:
            rows += "<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>"
    return f"<table>{head}{rows}</table>"
def r_callouts(b):
    items = "".join(f"<div class='callout'><h4>{esc(x['head'])}</h4><p>{esc(x['body'])}</p></div>" for x in b["items"])
    return f"<div class='callouts'>{items}</div>"
def r_stats(b):
    return "<div class='stats'>" + "".join(f"<div class='stat'><div class='v'>{esc(x['value'])}</div><div class='l'>{esc(x['label'])}</div></div>" for x in b["items"]) + "</div>"
def r_chart(b):
    mx = max(abs(float(x["value"])) for x in b["bars"]) or 1
    rows = ""
    for x in b["bars"]:
        w = max(3, abs(float(x["value"])) / mx * 100)
        rows += (f"<div class='row'><div class='lab'>{esc(x['label'])}</div>"
                 f"<div class='track'><div class='fill' style='width:{w:.1f}%'></div></div>"
                 f"<div class='val'>{esc(x['value'])}{esc(b.get('unit',''))}</div></div>")
    title = f"<h4 style='color:var(--violet);font-size:12pt;margin-bottom:4px'>{esc(b['title'])}</h4>" if b.get("title") else ""
    return f"<div class='chart'>{title}{rows}</div>"
def r_photos(b):
    srcs = [s for s in b.get("srcs", []) if rp(s).exists()]
    if srcs:
        cols = b.get("cols", 3)
        caps = b.get("captions", [])
        tiles = ""
        for i, src in enumerate(srcs):
            cap = (f"<div class='phtcap'>{esc(caps[i])}</div>"
                   if i < len(caps) and caps[i] else "")
            tiles += f"<div class='phtwrap'><div class='pht'><img src=\"{b64(src)}\"></div>{cap}</div>"
        style = f" style='grid-template-columns:repeat({cols},1fr)'" if cols != 3 else ""
        return f"<div class='grid'{style}>{tiles}</div>"
    n = b.get("count", 6)
    return "<div class='grid'>" + "".join(f"<div class='ph'>{esc(b.get('label','photo'))}</div>" for _ in range(n)) + "</div>"
def _ev_row(it):
    img = (f'<div class="evthumb"><img src="{b64(it["src"])}"></div>'
           if it.get("src") and rp(it["src"]).exists() else '<div class="evthumb"></div>')
    return (f'<div class="evrow">{img}<div class="evtext">'
            f'<h4>{esc(it["head"])}</h4><p>{esc(it["body"])}</p></div></div>')

def r_evidence(b):
    """Evidence as documented rows — a thumbnail answering to a named activity,
    not a wall of pictures."""
    rows = ""
    for it in b["items"]:
        img = (f'<div class="evthumb"><img src="{b64(it["src"])}"></div>'
               if it.get("src") and rp(it["src"]).exists() else '<div class="evthumb"></div>')
        rows += (f'<div class="evrow">{img}<div class="evtext">'
                 f'<h4>{esc(it["head"])}</h4><p>{esc(it["body"])}</p></div></div>')
    return f'<div class="evlist">{rows}</div>'


# ---- layout vocabulary borrowed from the NLNF 3.0 report ---------------------
# Phase chips, a chevron timeline, icon rows and percentage bullets. Same shapes,
# ASC's own content — nothing here invents a claim the source doesn't make.
CYC = ("var(--maroon)", "var(--violet)", "var(--coral2)")

def r_chip(b):
    i = int(b.get("tone", 0)) % len(CYC)
    sub = f'<span class="cs">{esc(b["sub"])}</span>' if b.get("sub") else ""
    return f'<div class="chip" style="--c:{CYC[i]}">{esc(b["label"])}{sub}</div>'

def r_chevrons(b):
    n = len(b["items"])
    cells = ""
    for i, it in enumerate(b["items"]):
        c = CYC[i % len(CYC)]
        arrow = '<div class="chv-a"></div>' if i < n - 1 else ""
        cells += (f'<div class="chv" style="--c:{c}"><div class="chv-h">{esc(it["label"])}</div>'
                  f'<div class="chv-b">{esc(it["body"])}</div></div>{arrow}')
    return f'<div class="chvrow">{cells}</div>'

def r_iconrows(b):
    rows = ""
    for i, it in enumerate(b["items"]):
        c = CYC[i % len(CYC)]
        rows += (f'<div class="irow" style="--c:{c}">'
                 f'<span class="ir-m">{arcs("var(--c)", 22, 4.6, radii=(0.5,1.0,1.5))}</span>'
                 f'<span class="ir-t">{esc(it)}</span></div>')
    return f'<div class="irows">{rows}</div>'

def r_pctbullets(b):
    rows = ""
    for i, it in enumerate(b["items"]):
        c = CYC[i % len(CYC)]
        rows += (f'<div class="pct" style="--c:{c}"><span class="pv">{esc(it["value"])}</span>'
                 f'<span class="pt">{esc(it["text"])}</span></div>')
    return f'<div class="pcts">{rows}</div>'

def r_note(b): return f"<div class='note'>{esc(b['text'])}</div>"

RENDER = {"paragraph": r_paragraph, "lead": r_lead, "bullets": r_bullets, "subhead": r_subhead,
          "table": r_table, "callouts": r_callouts, "stats": r_stats, "chart": r_chart,
          "photos": r_photos, "note": r_note, "evidence": r_evidence,
          "chip": r_chip, "chevrons": r_chevrons, "iconrows": r_iconrows,
          "pctbullets": r_pctbullets, "figure": r_figure, "split": r_split}

def render_blocks(blocks):
    return "\n".join(RENDER[b["type"]](b) for b in blocks)

# ---- page builders -----------------------------------------------------------
def cover(meta):
    m = "".join(f"<div>{esc(x)}</div>" for x in meta.get("meta_lines", []))
    photos = meta.get("cover_photos", [])
    n = max(6, len(photos))
    tiles = ""
    for i in range(n):
        if i < len(photos) and rp(photos[i]).exists():
            tiles += f'<div class="ct"><img src="{b64(photos[i])}"></div>'
        else:
            tiles += '<div class="ct ph">PROGRAM PHOTO</div>'
    return f"""
    <div class="page coverc">
      <div class="cc cc-tl">{arcs('var(--motif)', 280, 20)}</div>
      <div class="lock">{cobrand_lockup(84)}</div>
      <div class="eye">{esc(meta.get('eyebrow','Program Report'))}</div>
      <h1>{esc(meta['title'])}</h1>
      <div class="sub">{esc(meta.get('subtitle',''))}</div>
      <div style="margin:7mm 0 1mm">{ring('var(--motif)', 52, 3.2, op=.9)}</div>
      <div class="cphotos">{tiles}</div>
      <div class="meta">{m}</div>
      <div class="cband">
        <span>{esc(meta.get('foot_left',''))}</span>
        <span class="r">{esc(meta.get('foot_right',''))}</span>
      </div>
    </div>"""

def toc(sections, program="", pno=1, hero_src=None):
    items = "".join(
        f"<div class='toc-item'><div class='n'>{i:02d}</div><div class='t'>{esc(s['title'])}</div></div>"
        for i, s in enumerate(sections, 1))
    hero = (f'<div class="toc-hero"><img src="{b64(hero_src)}"></div>'
            if hero_src and rp(hero_src).exists()
            else '<div class="toc-hero">CONTENTS HERO PHOTO</div>')
    return f"""<div class="page"><div class="shead"><span class="sn">·</span><h2>Contents</h2></div>{divider()}
      {hero}{items}
      <div class="pfoot"><span>{esc(program)}</span><span>Page {pno:02d}</span></div></div>"""

def _secmotif():
    return f'<div class="secmotif" style="right:-32mm;bottom:-32mm">{arcs("var(--motif)",160,11,op=.14,rot=180)}</div>'

def split_blocks(blocks):
    """A {"type":"pagebreak"} block starts a new physical page inside one section.
    A .page is a fixed 297mm box, so a section that overflows it strands its footer
    mid-page — this keeps every page's content inside its own box."""
    groups, cur = [], []
    for b in blocks:
        if b.get("type") == "pagebreak":
            groups.append(cur); cur = []
        else:
            cur.append(b)
    groups.append(cur)
    return [g for g in groups if g] or [[]]

def section_flow(i, s):
    """One section as a continuous run of items — no page box. The paginator packs
    these onto pages, so a new section starts wherever the last one ended."""
    out = [f'<div class="fitem shead-wrap sec-start" data-keep="1">'
           f'<div class="shead"><span class="sn">{i:02d}</span><h2>{esc(s["title"])}</h2></div>'
           f'{divider()}</div>']
    for b in s["blocks"]:
        if b.get("type") == "pagebreak":
            out.append('<div class="fitem" data-break="1"></div>')
            continue
        if b["type"] == "evidence":      # rows flow individually across pages
            out += [f'<div class="fitem evlist">{_ev_row(it)}</div>' for it in b["items"]]
            continue
        keep = ' data-keep="1"' if b["type"] in ("subhead", "lead", "chip") else ""
        out.append(f'<div class="fitem"{keep}>{RENDER[b["type"]](b)}</div>')
    return "".join(out)

# Chrome runs this before printing, so the PDF gets the packed result.
PAGINATE_JS = """
<script>
// Wait for the inlined faces: measuring with fallback metrics gives wrong heights,
// and the page then overflows once the real font paints. Chrome's print waits for
// this to settle because of --virtual-time-budget.
document.fonts.ready.then(function(){
  const FOOT_L = "__FOOT__", START = __START__;
  const probe = document.createElement('div');
  probe.style.cssText = 'position:absolute;visibility:hidden;height:100mm';
  document.body.appendChild(probe);
  const mm = probe.getBoundingClientRect().height / 100;
  probe.remove();
  const MAXH = 249 * mm;                 // 297 - 22 top - 24 bottom, less rounding slack
  const SECGAP = 11 * mm;                // the air above a new section heading

  const flow = document.getElementById('flow');
  const host = document.getElementById('pages');
  if(!flow || !host) return;
  const items = Array.from(flow.children);

  // Measure every block ONCE, while they are still laid out at the content width.
  // Packing from known heights is predictable; the old approach appended, detected
  // overflow and moved things back, which stranded whole sections and left holes.
  const H = items.map(el => {
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return r.height + parseFloat(cs.marginTop || 0) + parseFloat(cs.marginBottom || 0);
  });
  flow.remove();

  let page = null, body = null, used = 0, n = START - 1;
  function newPage(){
    n++;
    page = document.createElement('div');
    page.className = 'page flowpage';
    page.innerHTML = '__MOTIF__<div class="fbody"></div>' +
      '<div class="pfoot"><span>' + FOOT_L + '</span><span>Page ' +
      String(n).padStart(2,'0') + '</span></div>';
    host.appendChild(page);
    body = page.querySelector('.fbody');
    used = 0;
  }
  newPage();

  const isSec = i => items[i].classList.contains('sec-start');
  // a heading at the top of a page doesn't need the section gap above it
  const costOf = (i, atTop) => H[i] - (atTop && isSec(i) ? SECGAP : 0);

  for(let i = 0; i < items.length; i++){
    if(items[i].dataset.break){ if(body.children.length) newPage(); continue; }

    const atTop = body.children.length === 0;
    let cost = costOf(i, atTop);

    // keep-with-next, following the whole chain: a heading followed by a lead
    // followed by cards must ALL fit, or the heading goes over with them.
    // Checking only the next item stranded headings on their own page.
    let need = cost;
    let j = i;
    while(items[j].dataset.keep && j + 1 < items.length && !items[j+1].dataset.break){
      j++;
      need += H[j];
      if(!items[j].dataset.keep) break;
    }
    if(!atTop && used + need > MAXH){
      newPage();
      cost = costOf(i, true);
    }

    body.appendChild(items[i]);

    // Predicted heights decide WHERE to break; the real box decides whether it fit.
    // Trusting the prediction alone let pages run past A4 and clip their last block.
    let real = body.getBoundingClientRect().height;
    if(real > MAXH && body.children.length > 1){
      body.removeChild(items[i]);
      newPage();
      body.appendChild(items[i]);
      real = body.getBoundingClientRect().height;
    }
    used = real;
  }

  Array.from(host.querySelectorAll('.flowpage')).forEach(p => {
    if(!p.querySelector('.fbody').children.length) p.remove();
  });
  let num = START;
  host.querySelectorAll('.flowpage .pfoot span:last-child').forEach(s => {
    s.textContent = 'Page ' + String(num++).padStart(2,'0');
  });
});
</script>
"""

def build_html(doc):
    meta = doc["meta"]
    program = meta.get("foot_left", "")
    flow = "".join(section_flow(i, s) for i, s in enumerate(doc["sections"], 1))
    js = (PAGINATE_JS.replace("__FOOT__", esc(program).replace('"', '\\"'))
                     .replace("__START__", "2")
                     # raw HTML: it contains no single quotes, so it is safe inside
                     # the JS string literal — escaping it would break the class attr
                     .replace("__MOTIF__", _secmotif()))
    body = (cover(meta) + toc(doc["sections"], program, 1, meta.get("toc_hero"))
            + f'<div id="pages"></div><div id="flow">{flow}</div>' + js)
    return ("<!doctype html><html><head><meta charset='utf-8'>"
            f"<style>{font_face()}{CSS}{theme_style(doc)}{motif_style()}</style></head><body>{body}</body></html>")

# ============================ REVIEW MODE ====================================
# Renders the real designed report on screen and lets the reviewer pin a comment
# to any part (cover, section, chart, table…), then export every comment as JSON
# to hand back for revision. Comments persist in localStorage so nothing is lost.

REVIEW_CSS = """
body{ background:#e7e1e0; }
.screenbar{ position:sticky; top:0; z-index:50; background:var(--violet); color:#fff;
  display:flex; align-items:center; gap:14px; padding:10px 18px; font-family:'Montserrat'; }
.screenbar b{ font-weight:700; } .screenbar .sp{ flex:1; }
.screenbar button{ font-family:'Montserrat'; font-weight:600; border:0; border-radius:8px;
  padding:8px 14px; cursor:pointer; background:var(--maroon); color:#fff; font-size:10.5pt; }
.screenbar button.ghost{ background:rgba(255,255,255,.15); }
.screenbar #status{ font-size:9.6pt; opacity:.9; font-weight:500; }
.screenbar .count{ background:var(--coral); color:#3a1a1a; border-radius:20px; padding:3px 10px; font-weight:700; font-size:10pt; }
.wrap{ padding:22px 0 80px; }
.page{ margin:0 auto 20px; box-shadow:0 10px 34px rgba(0,0,0,.18); background:#fff; }
.cx{ position:relative; }
/* any tagged element is commentable; the innermost one under the cursor wins */
.ct-el{ position:relative; }
/* .ct-el must not steal positioning from elements that place themselves */
.page > .pfoot{ font-variant-numeric:tabular-nums; position:absolute; }
.ct-el.hot{ outline:2px dashed rgba(171,57,53,.55); outline-offset:3px; background:rgba(255,174,168,.13); }
.ct-el.has{ outline:2px solid rgba(24,48,144,.45); outline-offset:3px; }
.addc{ position:absolute; width:26px; height:26px; border-radius:50%; background:var(--maroon);
  color:#fff; border:2px solid #fff; align-items:center; justify-content:center; cursor:pointer;
  font-size:15px; line-height:1; box-shadow:0 3px 10px rgba(0,0,0,.3); z-index:70; }
.pin{ position:absolute; top:-11px; left:-11px; min-width:20px; height:20px; padding:0 5px; border-radius:10px;
  background:var(--maroon); color:#fff; font-family:'Montserrat'; font-weight:700; font-size:10px;
  display:flex; align-items:center; justify-content:center; border:2px solid #fff; z-index:6; }
.pop{ position:absolute; z-index:60; width:300px; background:#fff; border-radius:12px; padding:12px;
  box-shadow:0 14px 44px rgba(0,0,0,.28); border:1px solid #e3d6d5; }
.pop .lab{ font-family:'Montserrat'; font-weight:700; color:var(--violet); font-size:10pt; margin-bottom:6px; }
.pop textarea{ width:100%; height:78px; border:1px solid #d9cbc9; border-radius:8px; padding:8px;
  font-family:'Nunito'; font-size:10.5pt; resize:vertical; }
.pop .row{ display:flex; gap:8px; justify-content:flex-end; margin-top:8px; }
.pop .ex{ display:flex; gap:6px; align-items:flex-start; background:var(--dawn); border-radius:7px;
  padding:6px 8px; margin-bottom:6px; font-size:10pt; }
.pop .ex b{ color:#b23; cursor:pointer; font-size:12pt; line-height:1; }
.pop button{ font-family:'Montserrat'; font-weight:600; border:0; border-radius:8px; padding:7px 12px; cursor:pointer; font-size:10pt; }
.pop .save{ background:var(--maroon); color:#fff; } .pop .cancel{ background:#eee; color:#333; }
.panel{ position:fixed; top:64px; right:16px; width:300px; max-height:78vh; overflow:auto; z-index:55;
  background:#fff; border-radius:14px; box-shadow:0 14px 44px rgba(0,0,0,.2); border:1px solid #e3d6d5; padding:12px; }
.panel h3{ font-size:12pt; color:var(--violet); margin-bottom:8px; }
.panel .empty{ color:var(--muted); font-size:10pt; }
.ci{ border-left:3px solid var(--green); background:var(--dawn); border-radius:0 8px 8px 0; padding:8px 10px; margin-bottom:8px; }
.ci .cl{ font-family:'Montserrat'; font-weight:700; font-size:8.6pt; color:var(--maroon); text-transform:uppercase; letter-spacing:.04em; }
.ci .ct-txt{ font-size:10pt; margin:2px 0 4px; }
.ci .cx-del{ font-size:8.6pt; color:#b23; cursor:pointer; font-family:'Montserrat'; font-weight:700; }
.panel.hidden{ display:none; }
@media print{ .screenbar,.panel,.addc,.pin,.pop{ display:none!important; }
  body{ background:#fff; } .ct-el.hot,.ct-el.has{ outline:none; background:none; } }
"""

REVIEW_JS = """
<script>
const SLUG = "__SLUG__";
const KEY  = "report-review:" + SLUG;
let data = {};        // cid -> [{label, text, ts}]
let serverOK = false; // true when served by review.py (auto-save); else localStorage

/* Every meaningful element is commentable — leaves win over their containers,
   because mouseover fires on the innermost tagged node. */
const SEL = [
  'h1','h2','h4','p','li','td','th','.pht','.ct','.stat','.callout','.chart .row',
  '.figcap','.fig','.toc-item','.toc-hero','.cband','.meta','.eye','.sub','.subhead',
  '.note','.section-lead','table','ul.b','.grid','.cphotos','.lockup','.pfoot'
].join(',');

const FRIENDLY = {
  'li':'bullet', 'td':'table cell', 'th':'table header', 'p':'paragraph',
  'h1':'title', 'h2':'heading', 'h4':'callout heading', 'table':'table',
  'ul':'bullet list', 'div':'block', 'span':'text', 'img':'image'
};
const CLASSNAME = {
  'pht':'photo', 'ct':'cover photo', 'stat':'stat tile', 'callout':'callout',
  'row':'chart bar', 'figcap':'caption', 'fig':'image', 'toc-item':'contents row',
  'toc-hero':'contents photo', 'cband':'cover foot band', 'meta':'cover meta lines',
  'eye':'eyebrow', 'sub':'subtitle', 'subhead':'sub-heading', 'note':'note',
  'section-lead':'lead line', 'grid':'photo grid', 'cphotos':'cover photo grid',
  'lockup':'logo lockup', 'pfoot':'page footer'
};

function norm(s){ return (s||'').replace(/\\s+/g,' ').trim(); }
function esc(s){ const d=document.createElement('div'); d.textContent=s; return d.innerHTML; }

function kindOf(el){
  const c = (el.className && String(el.className).split(' ')[0]) || '';
  return CLASSNAME[c] || FRIENDLY[el.tagName.toLowerCase()] || el.tagName.toLowerCase();
}
function pageTitleOf(el){
  const pg = el.closest('.page'); if(!pg) return 'Report';
  if(pg.classList.contains('coverc')) return 'Cover';
  let title = 'Contents';                       // pages can hold several sections now
  document.querySelectorAll('.shead h2').forEach(h => {
    if(h.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING) title = norm(h.textContent);
  });
  return title;
}

/* Stable id: section + kind + the element's own text. Survives a rebuild as long
   as the wording does, so comments stay pinned across regenerations. */
function tagAll(){
  const seen = {};
  document.querySelectorAll(SEL).forEach(el=>{
    if(el.closest('.screenbar,.panel,.pop')) return;
    const txt  = norm(el.textContent).slice(0,60);
    const kind = kindOf(el);
    const sect = pageTitleOf(el);
    const key  = sect+'|'+kind+'|'+txt;
    seen[key] = (seen[key]||0)+1;
    el.classList.add('ct-el');
    el.dataset.cid   = key + '#' + seen[key];
    el.dataset.label = sect + ' › ' + kind + (txt ? ' — "' + txt.slice(0,44) + (txt.length>44?'…':'') + '"' : '');
  });
}

/* ---- storage ---------------------------------------------------------- */
function setStatus(s, ok){
  const el=document.getElementById('status');
  el.textContent=s; el.style.opacity=ok===false?.75:1;
}
async function pull(){
  try{
    const r = await fetch('comments', {cache:'no-store'});
    if(r.ok){ data = (await r.json()) || {}; serverOK = true;
      setStatus('Auto-saving to file ✓'); render(); return; }
  }catch(e){}
  serverOK = false;
  try{ data = JSON.parse(localStorage.getItem(KEY)) || {}; }catch(e){ data = {}; }
  setStatus('Not served by review.py — use Export ↓', false);
  render();
}
async function save(){
  render();
  if(serverOK){
    try{
      await fetch('comments', {method:'POST', headers:{'Content-Type':'application/json'},
                               body: JSON.stringify(data)});
      setStatus('Saved ✓ — Claude can read it now'); return;
    }catch(e){ serverOK=false; }
  }
  localStorage.setItem(KEY, JSON.stringify(data));
  setStatus('Saved in this browser — use Export ↓', false);
}

/* ---- rendering -------------------------------------------------------- */
function render(){
  document.querySelectorAll('.ct-el').forEach(el=>{
    const arr = data[el.dataset.cid];
    el.classList.toggle('has', !!(arr && arr.length));
    let pin = el.querySelector(':scope > .pin');
    if(arr && arr.length){
      if(!pin){ pin=document.createElement('div'); pin.className='pin'; el.appendChild(pin); }
      pin.textContent = arr.length;
    } else if(pin){ pin.remove(); }
  });
  const all = Object.entries(data).flatMap(([cid,arr])=>arr.map((c,i)=>({cid,i,...c})));
  document.getElementById('count').textContent = all.length;
  const list = document.getElementById('list');
  list.innerHTML = all.length
    ? all.map(c=>`<div class="ci"><div class="cl">${esc(c.label)}</div>`+
                 `<div class="ct-txt">${esc(c.text)}</div>`+
                 `<div class="cx-del" onclick="del('${c.cid.replace(/'/g,"\\\\'")}',${c.i})">Delete</div></div>`).join('')
    : '<div class="empty">No comments yet. Hover anything in the report — a ● appears at its corner. Click it, type, done.</div>';
}
function del(cid,i){ data[cid].splice(i,1); if(!data[cid].length) delete data[cid]; save(); }

/* ---- hover target + popup --------------------------------------------- */
let current=null, hideT=null;
const btn = document.createElement('div');
btn.className='addc'; btn.textContent='+'; btn.style.display='none';
document.body.appendChild(btn);

function showBtn(el){
  clearTimeout(hideT); current = el;
  document.querySelectorAll('.ct-el.hot').forEach(x=>x.classList.remove('hot'));
  el.classList.add('hot');
  const r = el.getBoundingClientRect();
  btn.style.top  = (window.scrollY + r.top - 13) + 'px';
  btn.style.left = (window.scrollX + r.right - 13) + 'px';
  btn.style.display = 'flex';
}
function hideBtn(){
  hideT = setTimeout(()=>{
    btn.style.display='none';
    document.querySelectorAll('.ct-el.hot').forEach(x=>x.classList.remove('hot'));
  }, 260);
}
document.addEventListener('mouseover', e=>{
  const el = e.target.closest && e.target.closest('.ct-el');
  if(el){ showBtn(el); } else if(e.target !== btn){ hideBtn(); }
});
btn.addEventListener('mouseenter', ()=>clearTimeout(hideT));
btn.addEventListener('mouseleave', hideBtn);
btn.addEventListener('click', e=>{ e.stopPropagation(); if(current) openPop(current); });

let pop=null;
function openPop(el){
  closePop();
  const cid=el.dataset.cid, label=el.dataset.label;
  const existing = (data[cid]||[]).map((c,i)=>
    `<div class="ex"><span>${esc(c.text)}</span><b onclick="del('${cid.replace(/'/g,"\\\\'")}',${i})">×</b></div>`).join('');
  pop=document.createElement('div'); pop.className='pop';
  pop.innerHTML = `<div class="lab">${esc(label)}</div>${existing}
    <textarea placeholder="What would you change here?"></textarea>
    <div class="row"><button class="cancel">Cancel</button><button class="savebtn">Add comment</button></div>`;
  document.body.appendChild(pop);
  const r=el.getBoundingClientRect();
  pop.style.top  = (window.scrollY + r.top) + 'px';
  pop.style.left = (window.scrollX + Math.min(r.right+14, window.innerWidth-330)) + 'px';
  const ta=pop.querySelector('textarea'); ta.focus();
  const commit=()=>{ const t=ta.value.trim();
    if(t){ (data[cid]=data[cid]||[]).push({label,text:t,ts:Date.now()}); save(); }
    closePop(); };
  pop.querySelector('.cancel').onclick=closePop;
  pop.querySelector('.savebtn').onclick=commit;
  ta.addEventListener('keydown', ev=>{
    if(ev.key==='Enter' && (ev.metaKey||ev.ctrlKey)) commit();
    if(ev.key==='Escape') closePop();
  });
}
function closePop(){ if(pop){ pop.remove(); pop=null; } }
document.addEventListener('click', e=>{
  if(pop && !pop.contains(e.target) && e.target!==btn) closePop();
});

function exportComments(){
  const all=Object.entries(data).flatMap(([cid,arr])=>arr.map(c=>({cid,label:c.label,text:c.text,ts:new Date(c.ts).toISOString()})));
  const out={ report:SLUG, exported:new Date().toISOString(), count:all.length, comments:all };
  const blob=new Blob([JSON.stringify(out,null,2)],{type:'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=SLUG+'-comments.json'; a.click();
}
function clearAll(){ if(confirm('Delete all comments?')){ data={}; save(); } }
function togglePanel(){ document.getElementById('panel').classList.toggle('hidden'); }

tagAll();
pull();
</script>
"""

def render_blocks_review(blocks, sid, section_title):
    out = []
    for n, b in enumerate(blocks, 1):
        if b["type"] == "pagebreak":   # a print-only hint; the review page scrolls
            continue
        inner = RENDER[b["type"]](b)
        cid = f"{sid}-b{n}"
        label = f"{section_title} › {b['type']}"
        out.append(f'<div class="cx" data-cid="{cid}" data-label="{esc(label)}">{inner}</div>')
    return "\n".join(out)

def cover_review(meta):
    inner = cover(meta)
    return f'<div class="cx" data-cid="cover" data-label="Cover page">{inner}</div>'

def section_page_review(i, s, program, pno):
    sid = f"sec-{i:02d}"
    header = (f'<div class="cx" data-cid="{sid}-h" data-label="{esc(s["title"])} › heading">'
              f'<div class="shead"><span class="sn">{i:02d}</span><h2>{esc(s["title"])}</h2></div>'
              f'{divider()}</div>')
    body = render_blocks_review(s["blocks"], sid, s["title"])
    return (f'<div class="page">{_secmotif()}{header}{body}'
            f'<div class="pfoot"><span>{esc(program)}</span><span>Page {pno:02d}</span></div></div>')

def build_review_html(doc):
    meta = doc["meta"]; program = meta.get("foot_left", "")
    flow = "".join(section_flow(i, s) for i, s in enumerate(doc["sections"], 1))
    paginate = (PAGINATE_JS.replace("__FOOT__", esc(program).replace('"', '\\"'))
                           .replace("__START__", "2")
                           .replace("__MOTIF__", _secmotif()))
    pages = [cover_review(meta), toc(doc["sections"], program, 1, meta.get("toc_hero")),
             f'<div id="pages"></div><div id="flow">{flow}</div>', paginate]
    bar = ('<div class="screenbar"><b>Review — ' + esc(meta["title"]) + '</b>'
           '<span class="count" id="count">0</span> comments'
           '<span id="status">…</span><div class="sp"></div>'
           '<button class="ghost" onclick="togglePanel()">Comments</button>'
           '<button class="ghost" onclick="clearAll()">Clear</button>'
           '<button onclick="exportComments()">Export ↓</button></div>')
    panel = ('<div class="panel" id="panel"><h3>Comments</h3><div id="list"></div></div>')
    js = REVIEW_JS.replace("__SLUG__", meta["slug"])
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{font_face()}{CSS}{REVIEW_CSS}{theme_style(doc)}{motif_style()}</style></head>"
            f"<body>{bar}{panel}<div class='wrap'>{''.join(pages)}</div>{js}</body></html>")


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: build_report.py <content.json> [--review]")
    doc = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    slug = doc["meta"]["slug"]
    if "--review" in sys.argv:
        rp = OUT / f"{slug}-review.html"
        rp.write_text(build_review_html(doc), encoding="utf-8")
        print(f"REVIEW: {rp}")
        return
    hp = OUT / f"{slug}.html"; hp.write_text(build_html(doc), encoding="utf-8")
    pdf = OUT / f"{slug}.pdf"
    url = "file:///" + str(hp).replace("\\", "/")
    subprocess.run([chrome_path(), "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                    "--virtual-time-budget=15000", url], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"HTML: {hp}")
    print(f"PDF:  {pdf}")

if __name__ == "__main__":
    main()
