#!/usr/bin/env python3
"""Layout explorer — renders a set of COVER and SECTION layout options (A4) into
one PDF so we can pick a direction before building the real report.

    python tools/report/layout_options.py

Motif: the SL 'nested corner-arcs' unit, rebuilt as parametric SVG so it can
radiate from any corner, frame, tile, or ghost behind content.
"""
import base64, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
LOGO = REPO / ".claude" / "signature-assets" / "logo.png"
SCERT = HERE / "assets" / "scert-haryana.png"
CHROME = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
          r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
          r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]

def chrome():
    for c in CHROME:
        if Path(c).exists(): return c
    sys.exit("no chrome/edge")

def b64(p):
    return "data:image/png;base64," + base64.b64encode(Path(p).read_bytes()).decode()

# palette (approved)
BLUE="#183090"; MAROON="#ab3935"; GREEN="#43a53f"; RED="#d81818"
CREAM="#fff9e4"; DAWN="#eef1f7"; GREY="#1e1e1e"

def arcs(color, size=200, sw=16, radii=(0.30,0.60,0.90), op=1.0, rot=0):
    """The motif unit: nested quarter-arcs from a corner. rot rotates the corner."""
    p=""
    for f in radii:
        r=f*size
        p+=(f'<path d="M {r:.1f} 0 A {r:.1f} {r:.1f} 0 0 1 0 {r:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
            f'style="opacity:{op};transform:rotate({rot}deg);overflow:visible">{p}</svg>')

def lockup(h=46, on_dark=False):
    div = "#ffffff55" if on_dark else "#00000022"
    return (f'<span style="display:inline-flex;gap:14px;align-items:center">'
            f'<img src="{b64(LOGO)}" style="height:{h}px">'
            f'<span style="width:1px;height:{h*0.7:.0f}px;background:{div}"></span>'
            f'<img src="{b64(SCERT)}" style="height:{h}px"></span>')

TITLE="Aao School Chalein 3.0"
EYE="Program Report"
SUB="A state-level enrolment drive · Haryana"
META=["School Education Department, Government of Haryana",
      "SCERT Haryana · DIKSHA · Micro-Improvement Approach",
      "In partnership with ShikshaLokam"]

CSS=f"""
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Nunito:wght@400;600;700&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
@page{{size:A4;margin:0}}
html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:'Nunito',sans-serif;color:{GREY};background:#d9d4d3}}
.sheet{{position:relative;width:210mm;height:297mm;background:#fff;overflow:hidden;page-break-after:always}}
h1,h2,h3,.mont{{font-family:'Montserrat',sans-serif}}
.tag{{position:absolute;left:12mm;bottom:8mm;font-family:'Montserrat';font-weight:700;font-size:9pt;color:#9a9390;letter-spacing:.08em;text-transform:uppercase;z-index:9}}
.eye{{font-family:'Montserrat';font-weight:600;letter-spacing:.16em;text-transform:uppercase;font-size:10.5pt}}
.t1{{font-family:'Montserrat';font-weight:800;font-size:34pt;line-height:1.08}}
.sub{{font-family:'Montserrat';font-weight:600;font-size:13pt}}
.meta{{font-size:10.5pt;line-height:1.9;color:#6b625f}}
.corner{{position:absolute;line-height:0}}
.p{{font-size:10.6pt;line-height:1.55;margin:0 0 9px}}
ul{{list-style:none}} ul li{{position:relative;padding-left:18px;margin:5px 0;font-size:10.4pt}}
ul li::before{{content:'';position:absolute;left:2px;top:7px;width:7px;height:7px;border-radius:2px;background:{GREEN}}}
.num{{font-family:'Montserrat';font-weight:800}}
"""

# ---------------- COVER OPTIONS ----------------
def coverA():  # Corner Radiate
    return f"""<div class="sheet">
      <div class="corner" style="right:-40mm;bottom:-40mm">{arcs(MAROON,300,20,op=1,rot=180)}</div>
      <div class="corner" style="right:-24mm;bottom:-24mm">{arcs(BLUE,180,16,op=.9,rot=180)}</div>
      <div style="position:absolute;left:18mm;top:18mm">{lockup(44)}</div>
      <div style="position:absolute;left:18mm;top:120mm;max-width:150mm">
        <div class="eye" style="color:{MAROON}">{EYE}</div>
        <div class="t1" style="color:{BLUE};margin:8px 0 6px">{TITLE}</div>
        <div class="sub" style="color:{MAROON}">{SUB}</div>
        <div class="meta" style="margin-top:16px">{''.join(f'<div>{m}</div>' for m in META)}</div>
      </div>
      <div style="position:absolute;left:0;right:0;bottom:0;height:8mm;background:{BLUE}"></div>
      <div class="tag">Cover · Option A — Corner Radiate</div>
    </div>"""

def coverB():  # Split Panel
    return f"""<div class="sheet">
      <div style="position:absolute;left:0;top:0;bottom:0;width:80mm;background:{BLUE};overflow:hidden">
        <div class="corner" style="left:-30mm;bottom:-30mm">{arcs('#ffffff',220,16,op=.16)}</div>
        <div style="position:absolute;left:14mm;top:16mm;background:#fff;border-radius:12px;padding:12px 14px">{lockup(40)}</div>
        <div style="position:absolute;left:14mm;bottom:20mm;color:#fff">
          <div class="eye" style="color:#ffd9d6">{EYE}</div>
        </div>
      </div>
      <div style="position:absolute;left:92mm;right:16mm;top:60mm">
        <div class="t1" style="color:{BLUE}">{TITLE}</div>
        <div style="height:3px;width:48px;background:{MAROON};border-radius:3px;margin:12px 0"></div>
        <div class="sub" style="color:{MAROON}">{SUB}</div>
        <div class="meta" style="margin-top:16px">{''.join(f'<div>{m}</div>' for m in META)}</div>
      </div>
      <div class="tag">Cover · Option B — Split Panel</div>
    </div>"""

def coverC():  # Framed / Centered (formal)
    return f"""<div class="sheet" style="background:{CREAM}">
      <div class="corner" style="left:-34mm;top:-34mm">{arcs(MAROON,240,18,op=1)}</div>
      <div class="corner" style="right:-34mm;bottom:-34mm">{arcs(BLUE,240,18,op=1,rot=180)}</div>
      <div style="position:absolute;left:0;right:0;top:60mm;text-align:center;padding:0 30mm">
        <div style="display:flex;justify-content:center;margin-bottom:22mm">{lockup(48)}</div>
        <div class="eye" style="color:{MAROON}">{EYE}</div>
        <div class="t1" style="color:{BLUE};margin:10px 0 8px">{TITLE}</div>
        <div class="sub" style="color:{MAROON}">{SUB}</div>
        <div class="meta" style="margin-top:16px">{''.join(f'<div>{m}</div>' for m in META)}</div>
      </div>
      <div class="tag">Cover · Option C — Framed / Centered</div>
    </div>"""

def coverD():  # Top Band Hero + photo slot
    return f"""<div class="sheet">
      <div style="position:absolute;left:0;right:0;top:0;height:160mm;background:{BLUE};overflow:hidden">
        <div class="corner" style="right:-30mm;top:-30mm">{arcs('#ffffff',260,18,op=.14,rot=90)}</div>
        <div style="position:absolute;left:18mm;top:16mm;background:#fff;border-radius:12px;padding:10px 14px">{lockup(38)}</div>
        <div style="position:absolute;left:18mm;bottom:22mm;color:#fff;max-width:150mm">
          <div class="eye" style="color:#ffd9d6">{EYE}</div>
          <div class="t1" style="color:#fff;margin:8px 0 6px">{TITLE}</div>
          <div class="sub" style="color:#ffe7e5">{SUB}</div>
        </div>
      </div>
      <div style="position:absolute;left:0;right:0;top:160mm;bottom:0;background:{DAWN};display:flex">
        <div style="flex:1;padding:16mm 18mm"><div class="meta">{''.join(f'<div>{m}</div>' for m in META)}</div></div>
        <div style="width:70mm;margin:12mm 18mm 12mm 0;border-radius:12px;background:repeating-linear-gradient(45deg,#e3e7f0,#e3e7f0 10px,#d7dcea 10px,#d7dcea 20px);display:flex;align-items:center;justify-content:center;color:#8892ad;font-family:Montserrat;font-weight:700;font-size:9pt">HERO PHOTO</div>
      </div>
      <div class="tag">Cover · Option D — Top Band Hero + Photo</div>
    </div>"""

# ---------------- SECTION OPTIONS ----------------
BODY_P="During this phase, school leaders undertook structured micro-improvement tasks on the DIKSHA App. Each completed task was documented with photo or video evidence, letting officials monitor progress in real time."
BODY_LI=["School-based awareness events","Organised door-to-door visits","Community engagement to enrol out-of-school children","Continuous monitoring via the DIKSHA dashboard"]

def lilist(): return "<ul>"+"".join(f"<li>{x}</li>" for x in BODY_LI)+"</ul>"

def secS1():  # Number rail
    return f"""<div class="sheet">
      <div style="position:absolute;left:0;top:0;bottom:0;width:26mm;background:{BLUE};overflow:hidden">
        <div class="num" style="color:#fff;font-size:44pt;position:absolute;left:6mm;top:20mm">03</div>
        <div class="corner" style="left:-14mm;bottom:-14mm">{arcs('#ffffff',120,12,op=.2)}</div>
      </div>
      <div style="position:absolute;left:40mm;right:18mm;top:22mm">
        <h2 style="color:{MAROON};font-size:22pt">Program phases</h2>
        <div style="height:3px;width:44px;background:{GREEN};border-radius:3px;margin:8px 0 14px"></div>
        <p class="p">{BODY_P}</p>{lilist()}
      </div>
      <div class="tag">Section · Option S1 — Number Rail</div>
    </div>"""

def secS2():  # Header band + corner motif
    return f"""<div class="sheet">
      <div style="position:absolute;left:0;right:0;top:0;height:44mm;background:{DAWN};overflow:hidden">
        <div class="corner" style="right:-16mm;top:-16mm">{arcs(MAROON,120,12,op=.9,rot=90)}</div>
        <div style="position:absolute;left:18mm;top:14mm;display:flex;align-items:center;gap:12px">
          <span class="num" style="background:{BLUE};color:#fff;width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:13pt">03</span>
          <h2 style="color:{BLUE};font-size:20pt">Program phases</h2>
        </div>
      </div>
      <div style="position:absolute;left:18mm;right:18mm;top:56mm">
        <p class="p">{BODY_P}</p>{lilist()}
      </div>
      <div class="tag">Section · Option S2 — Header Band + Corner</div>
    </div>"""

def secS3():  # Ghost number + watermark
    return f"""<div class="sheet">
      <div class="num" style="position:absolute;left:12mm;top:6mm;font-size:130pt;color:{BLUE};opacity:.08">03</div>
      <div class="corner" style="right:-30mm;bottom:-30mm">{arcs(MAROON,220,16,op=.10,rot=180)}</div>
      <div style="position:absolute;left:18mm;right:18mm;top:40mm">
        <h2 style="color:{MAROON};font-size:22pt">Program phases</h2>
        <div style="height:3px;width:44px;background:{GREEN};border-radius:3px;margin:8px 0 14px"></div>
        <p class="p">{BODY_P}</p>{lilist()}
      </div>
      <div class="tag">Section · Option S3 — Ghost Number</div>
    </div>"""

PAGES=[coverA(),coverB(),coverC(),coverD(),secS1(),secS2(),secS3()]
html=f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(PAGES)}</body></html>"
hp=OUT/"layout-options.html"; hp.write_text(html,encoding="utf-8")
pdf=OUT/"layout-options.pdf"
subprocess.run([chrome(),"--headless=new","--disable-gpu","--no-sandbox","--no-pdf-header-footer",
                f"--print-to-pdf={pdf}","--virtual-time-budget=15000","file:///"+str(hp).replace("\\","/")],
               check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print("PDF:",pdf)
