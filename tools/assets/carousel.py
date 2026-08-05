#!/usr/bin/env python3
"""carousel.py — ShikshaLokam asset factory: a slide spec (JSON) → branded
PNG slides + a combined PDF, via headless Chrome. No external deps.

Usage:
    python tools/assets/carousel.py tools/assets/carousels/mitra-impact.json [--out DIR] [--square]

Slide JSON: { "name", "size":[w,h], "slides":[ {type, kicker, headline, big, label, sub, cta} ] }
Types: cover | stat | close (anything else renders like cover).
"""
import argparse, html, json, re, subprocess, sys, tempfile
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ASSETS = Path(__file__).resolve().parent

def brand_css():
    f = ASSETS / "brand" / "brand.css"
    return f.read_text(encoding="utf-8") if f.exists() else ""

def parse_md(path, name=None, after="Carousel slides:", size=(1080, 1350)):
    """Heuristically turn a brain 'Carousel slides:' numbered list into a slide spec —
    so the deck comes straight from page.md, no hand-written JSON."""
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if after.lower() in l.lower()), None)
    if start is None:
        sys.exit(f"Couldn't find '{after}' in {path}")
    slides = []
    for l in lines[start + 1:]:
        m = re.match(r"\s*\d+\.\s+(.*)", l)
        if not m:
            if slides and not l.strip():
                break  # blank line ends the list once we've started
            continue
        raw = m.group(1).strip().strip("*").strip()
        low = raw.lower()
        def dequote(s): return s.strip().strip('"').strip("“”").strip()
        if low.startswith("cover"):
            body = raw.split(":", 1)[1] if ":" in raw else raw
            parts = [p.strip() for p in body.split("·")]
            slides.append({"type": "cover", "headline": dequote(parts[0]),
                           "sub": dequote(parts[1]) if len(parts) > 1 else ""})
        elif "register" in low:
            parts = [p.strip() for p in raw.split("·")]
            cta = next((p for p in parts if "register" in p.lower()), "")
            cta = re.sub(r"(?i)register:?\s*", "Register → ", cta)
            sub = next((p for p in parts[1:] if "register" not in p.lower()), "")
            slides.append({"type": "close", "headline": dequote(parts[0]),
                           "sub": dequote(sub), "cta": cta})
        elif re.match(r'"?[\d][\d.,]*', raw):
            num = re.match(r'"?([\d][\d.,]*(?:\s*(?:lakh|crore))?)\s+(.*)', dequote(raw))
            if num:
                big, rest = num.group(1).strip(), num.group(2).strip()
                seg = re.split(r"\s*[—–-]\s*", rest, maxsplit=1)
                slides.append({"type": "stat", "big": big,
                               "label": seg[0].strip(),
                               "sub": dequote(seg[1]) if len(seg) > 1 else ""})
            else:
                slides.append({"type": "cover", "headline": dequote(raw)})
        else:
            slides.append({"type": "cover", "headline": dequote(raw)})
    return {"name": name or (Path(path).stem + "-carousel"), "size": list(size), "slides": slides}

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

CSS = """
:root{
  --indigo:#15123b; --purple:#3b2a7a; --violet:#7c5cff; --teal:#2dd4bf;
  --ink:#ffffff; --soft:rgba(255,255,255,.78); --offwhite:#f7f4ef;
}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:__W__px;height:__H__px;}
.slide{
  width:__W__px;height:__H__px;display:flex;flex-direction:column;
  justify-content:space-between;padding:96px 92px;
  background:radial-gradient(120% 120% at 0% 0%, #5b3aa6 0%, #3b2a7a 45%, #15123b 100%);
  color:var(--ink);
  font-family:"Segoe UI","Inter","Helvetica Neue",Arial,sans-serif;
  -webkit-print-color-adjust:exact;print-color-adjust:exact;overflow:hidden;
}
.top{font-size:30px;letter-spacing:.18em;text-transform:uppercase;color:var(--teal);font-weight:600;}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center;}
.cover-h{font-size:88px;line-height:1.06;font-weight:700;letter-spacing:-.02em;}
.sub{font-size:40px;line-height:1.3;color:var(--soft);margin-top:34px;font-weight:400;}
.big{font-size:230px;line-height:.9;font-weight:800;letter-spacing:-.03em;
  background:linear-gradient(120deg,#ffffff 0%, #c9b8ff 55%, var(--teal) 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent;}
.label{font-size:62px;font-weight:600;margin-top:18px;letter-spacing:-.01em;}
.close-h{font-size:104px;line-height:1.05;font-weight:800;letter-spacing:-.03em;}
.cta{display:inline-block;margin-top:48px;font-size:38px;font-weight:600;color:#15123b;
  background:var(--teal);padding:26px 44px;border-radius:999px;align-self:flex-start;}
.footer{display:flex;align-items:center;justify-content:space-between;}
.wordmark{font-size:34px;font-weight:700;letter-spacing:.02em;}
.wordmark .dot{color:var(--teal);}
.dots{display:flex;gap:14px;}
.dots span{width:16px;height:16px;border-radius:50%;background:rgba(255,255,255,.28);}
.dots span.on{background:var(--teal);}
"""

def esc(s):
    return html.escape(str(s)).replace("\n", "<br>")

def slide_html(slide, idx, total, size, standalone=True):
    w, h = size
    t = slide.get("type", "cover")
    kicker = slide.get("kicker", "")
    top = f'<div class="top">{esc(kicker)}</div>' if kicker else '<div class="top"></div>'
    if t == "stat":
        mid = (f'<div class="mid"><div class="big">{esc(slide.get("big",""))}</div>'
               f'<div class="label">{esc(slide.get("label",""))}</div>'
               f'<p class="sub">{esc(slide.get("sub",""))}</p></div>')
    elif t == "close":
        cta = f'<div class="cta">{esc(slide.get("cta",""))}</div>' if slide.get("cta") else ""
        mid = (f'<div class="mid"><h1 class="close-h">{esc(slide.get("headline",""))}</h1>'
               f'<p class="sub">{esc(slide.get("sub",""))}</p>{cta}</div>')
    else:
        mid = (f'<div class="mid"><h1 class="cover-h">{esc(slide.get("headline",""))}</h1>'
               f'<p class="sub">{esc(slide.get("sub",""))}</p></div>')
    dots = "".join(f'<span class="{"on" if i==idx else ""}"></span>' for i in range(total))
    footer = (f'<div class="footer"><span class="wordmark">MItra<span class="dot">.</span></span>'
              f'<span class="dots">{dots}</span></div>')
    inner = f'<div class="slide">{top}{mid}{footer}</div>'
    if not standalone:
        return inner
    css = CSS.replace("__W__", str(w)).replace("__H__", str(h)) + brand_css()
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{inner}</body></html>"

def opath(p: Path):
    return str(p.resolve()).replace("\\", "/")

def furl(p: Path):
    return "file:///" + opath(p)

def chrome():
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    sys.exit("No Chrome/Edge found.")

def run(args):
    subprocess.run(args, check=True, capture_output=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", help="a .json slide spec, or a .md file to auto-pull slides from")
    ap.add_argument("--out")
    ap.add_argument("--name", help="deck name when reading a .md")
    ap.add_argument("--after", default="Carousel slides:", help="heading the slide list follows in the .md")
    ap.add_argument("--square", action="store_true", help="also render 1080x1080")
    a = ap.parse_args()
    if a.spec.lower().endswith(".md"):
        spec = parse_md(a.spec, name=a.name, after=a.after)
    else:
        spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    name = spec["name"]
    size = spec.get("size", [1080, 1350])
    slides = spec["slides"]
    out = Path(a.out) if a.out else Path("tools/assets/out") / name
    out.mkdir(parents=True, exist_ok=True)
    ch = chrome()
    tmp = tempfile.mkdtemp(prefix="slfx_")
    base = [ch, "--headless=new", "--disable-gpu", "--no-first-run",
            "--no-default-browser-check", f"--user-data-dir={tmp}"]

    # PNG per slide
    pngs = []
    for i, s in enumerate(slides):
        hp = out / f"slide_{i+1}.html"
        hp.write_text(slide_html(s, i, len(slides), size), encoding="utf-8")
        png = out / f"slide_{i+1}.png"
        run(base + ["--hide-scrollbars", "--force-device-scale-factor=1",
             "--run-all-compositor-stages-before-draw", "--virtual-time-budget=3000",
             f"--screenshot={opath(png)}", f"--window-size={size[0]},{size[1]}", furl(hp)])
        pngs.append(png)
        print(f"  slide {i+1}: {png.name}")

    # combined PDF (one page per slide, exact slide size)
    w_in, h_in = size[0] / 96, size[1] / 96
    page_css = (f"@page{{size:{w_in:.4f}in {h_in:.4f}in;margin:0;}}"
                ".sheet{break-after:page;}" + CSS.replace("__W__", str(size[0])).replace("__H__", str(size[1])) + brand_css())
    sheets = "".join(f'<div class="sheet">{slide_html(s,i,len(slides),size,standalone=False)}</div>'
                     for i, s in enumerate(slides))
    stacked = out / "_stacked.html"
    stacked.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{page_css}</style></head><body>{sheets}</body></html>", encoding="utf-8")
    pdf = out / f"{name}.pdf"
    run(base + ["--no-pdf-header-footer", f"--print-to-pdf={opath(pdf)}", furl(stacked)])
    print(f"  pdf:    {pdf.name}")
    print(f"\nOutput → {out.resolve()}")

if __name__ == "__main__":
    main()
