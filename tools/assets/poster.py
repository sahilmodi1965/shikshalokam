#!/usr/bin/env python3
"""poster.py — a poster spec (JSON) → branded 1:1 PNG, via headless Chrome.

Usage:
    python tools/assets/poster.py tools/assets/posters/mitra-poster.json [--out DIR]

Spec: { name, size:[w,h], eyebrow, hero:[lines], subhead, details, cta, register_link, footer, logos:[paths] }
- QR: real QR when register_link is a live URL (http…), else a labelled placeholder.
- Logos: if `logos` paths exist they're embedded; else the `footer` text is shown.
- Brand: drop a tools/assets/brand/brand.css (e.g. @font-face) and it's applied here + in carousels.
"""
import argparse, base64, html, json, subprocess, sys, tempfile
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import qrcode

ASSETS = Path(__file__).resolve().parent
CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

CSS = """
:root{--violet:#7c5cff;--teal:#2dd4bf;--soft:rgba(255,255,255,.80);}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:__W__px;height:__H__px;}
.p{width:__W__px;height:__H__px;display:flex;flex-direction:column;justify-content:space-between;
  padding:88px 84px;color:#fff;overflow:hidden;
  background:radial-gradient(130% 130% at 100% 0%, #5b3aa6 0%, #3b2a7a 48%, #15123b 100%);
  font-family:"Segoe UI","Inter","Helvetica Neue",Arial,sans-serif;
  -webkit-print-color-adjust:exact;print-color-adjust:exact;}
.eyebrow{font-size:30px;letter-spacing:.2em;text-transform:uppercase;color:var(--teal);font-weight:600;}
.flow{display:flex;gap:12px;align-items:center;margin-top:26px;}
.flow .bar{width:10px;border-radius:6px;background:var(--teal);opacity:.9;}
.flow .card{width:26px;height:26px;border-radius:6px;background:rgba(255,255,255,.22);}
.hero{font-size:118px;line-height:1.02;font-weight:800;letter-spacing:-.03em;}
.sub{font-size:40px;line-height:1.3;color:var(--soft);margin-top:34px;font-weight:400;}
.details{font-size:31px;color:var(--soft);margin-top:30px;letter-spacing:.01em;}
.bottom{display:flex;align-items:flex-end;justify-content:space-between;}
.left{display:flex;flex-direction:column;gap:26px;}
.cta{font-size:38px;font-weight:700;color:#15123b;background:var(--teal);
  padding:26px 46px;border-radius:999px;align-self:flex-start;}
.link{font-size:24px;color:var(--soft);}
.logos{font-size:26px;color:var(--soft);font-weight:600;letter-spacing:.02em;}
.logos img{height:52px;margin-right:26px;vertical-align:middle;}
.qr{width:188px;height:188px;border-radius:20px;background:#fff;overflow:hidden;display:flex;
  align-items:center;justify-content:center;color:#15123b;font-weight:700;font-size:24px;text-align:center;}
.qr small{display:block;font-weight:500;color:#64748b;font-size:18px;margin-top:6px;}
.qr svg{width:188px;height:188px;}
"""

def esc(s): return html.escape(str(s))
def furl(p): return "file:///" + str(Path(p).resolve()).replace("\\", "/")
def opath(p): return str(Path(p).resolve()).replace("\\", "/")

def chrome():
    for c in CHROME_CANDIDATES:
        if Path(c).exists(): return c
    sys.exit("No Chrome/Edge found.")

def brand_css():
    f = ASSETS / "brand" / "brand.css"
    return f.read_text(encoding="utf-8") if f.exists() else ""

def qr_svg(data, px=188):
    q = qrcode.QRCode(border=2, box_size=1); q.add_data(data); q.make(fit=True)
    m = q.get_matrix(); n = len(m); cell = px / n
    rects = "".join(f'<rect x="{x*cell:.2f}" y="{y*cell:.2f}" width="{cell:.2f}" height="{cell:.2f}"/>'
                    for y, row in enumerate(m) for x, v in enumerate(row) if v)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {px} {px}">'
            f'<rect width="{px}" height="{px}" fill="#fff"/><g fill="#15123b">{rects}</g></svg>')

def logo_html(paths):
    out = []
    for p in paths or []:
        p = Path(p)
        if p.exists():
            mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
            b = base64.b64encode(p.read_bytes()).decode()
            out.append(f'<img src="data:{mime};base64,{b}">')
    return "".join(out)

def build_html(spec):
    w, h = spec.get("size", [1080, 1080])
    hero = "".join(f"<div>{esc(l)}</div>" for l in spec.get("hero", []))
    link = spec.get("register_link", "")
    if str(link).startswith("http"):
        qr = f'<div class="qr">{qr_svg(link)}</div>'
    else:
        qr = '<div class="qr">QR<small>scan to register</small></div>'
    logos = logo_html(spec.get("logos")) or esc(spec.get("footer", ""))
    bars = "".join(f'<div class="bar" style="height:{14+i*10}px"></div>' for i in range(5))
    flow = f'<div class="flow">{bars}<div class="card"></div><div class="card"></div><div class="card"></div></div>'
    inner = f"""<div class="p">
      <div><div class="eyebrow">{esc(spec.get('eyebrow',''))}</div>{flow}</div>
      <div>
        <div class="hero">{hero}</div>
        <div class="sub">{esc(spec.get('subhead',''))}</div>
        <div class="details">{esc(spec.get('details',''))}</div>
      </div>
      <div class="bottom">
        <div class="left">
          <div class="cta">{esc(spec.get('cta','Register'))} &rarr;</div>
          <div class="link">{esc(link)}</div>
          <div class="logos">{logos}</div>
        </div>
        {qr}
      </div>
    </div>"""
    css = CSS.replace("__W__", str(w)).replace("__H__", str(h)) + brand_css()
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{inner}</body></html>", (w, h)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out")
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    out = Path(a.out) if a.out else ASSETS / "out" / spec["name"]
    out.mkdir(parents=True, exist_ok=True)
    page, (w, h) = build_html(spec)
    hp = out / f"{spec['name']}.html"; hp.write_text(page, encoding="utf-8")
    png = out / f"{spec['name']}.png"
    tmp = tempfile.mkdtemp(prefix="slpost_")
    subprocess.run([chrome(), "--headless=new", "--disable-gpu", "--no-first-run",
                    "--no-default-browser-check", f"--user-data-dir={tmp}", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=3000", f"--screenshot={opath(png)}",
                    f"--window-size={w},{h}", furl(hp)], check=True, capture_output=True)
    print(f"poster: {png.resolve()}")

if __name__ == "__main__":
    main()
