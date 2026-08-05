#!/usr/bin/env python3
"""pdf.py — markdown → branded ShikshaLokam PDF, via headless Chrome. No deps.

Usage:
    python tools/assets/pdf.py <input.md> [--out FILE.pdf] [--title "Doc title"]
"""
import argparse, html, re, subprocess, sys, tempfile
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

DOC_CSS = """
@page{ size:A4; margin:22mm 20mm; }
*{box-sizing:border-box;}
body{font-family:"Segoe UI","Inter",Helvetica,Arial,sans-serif;color:#1e293b;
  font-size:11.5pt;line-height:1.55;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
h1{font-size:23pt;color:#3b2a7a;letter-spacing:-.01em;margin:0 0 6pt;}
h2{font-size:15pt;color:#15123b;margin:20pt 0 6pt;border-bottom:2px solid #2dd4bf;padding-bottom:3pt;}
h3{font-size:12.5pt;color:#3b2a7a;margin:14pt 0 4pt;}
p{margin:0 0 8pt;}
ul,ol{margin:0 0 8pt 18pt;} li{margin:0 0 3pt;}
blockquote{margin:0 0 8pt;padding:8pt 14pt;border-left:3px solid #7c5cff;
  background:#f6f4fb;color:#334155;}
table{border-collapse:collapse;width:100%;margin:0 0 10pt;font-size:10.5pt;}
th,td{border:1px solid #d8dae5;padding:6pt 8pt;text-align:left;vertical-align:top;}
th{background:#f1eefb;color:#15123b;}
hr{border:none;border-top:1px solid #e2e8f0;margin:14pt 0;}
a{color:#7c5cff;}
code{background:#f1f5f9;padding:1pt 4pt;border-radius:3px;font-size:10pt;}
.docfoot{margin-top:18pt;padding-top:8pt;border-top:1px solid #e2e8f0;color:#94a3b8;font-size:9pt;}
"""

def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"<i>\1</i>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', s)
    return s

def md_to_html(md):
    lines = md.splitlines(); out = []; i = 0; lst = None
    def close():
        nonlocal lst
        if lst: out.append(f"</{lst}>"); lst = None
    while i < len(lines):
        s = lines[i].rstrip()
        if s.startswith("|") and i + 1 < len(lines) and set(lines[i+1].strip()) <= set("|-: "):
            close()
            hdr = [c.strip() for c in s.strip().strip("|").split("|")]; i += 2; rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            t = "<table><tr>" + "".join(f"<th>{inline(h)}</th>" for h in hdr) + "</tr>"
            for r in rows:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
            out.append(t + "</table>"); continue
        if not s.strip(): close(); i += 1; continue
        m = re.match(r"(#{1,3})\s+(.*)", s)
        if m:
            close(); out.append(f"<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>")
        elif s.strip() in ("---", "***", "___"):
            close(); out.append("<hr>")
        elif s.startswith("> "):
            close(); out.append(f"<blockquote>{inline(s[2:])}</blockquote>")
        elif re.match(r"\s*[-*]\s+", s):
            if lst != "ul": close(); out.append("<ul>"); lst = "ul"
            out.append(f"<li>{inline(re.sub(r'^\s*[-*]\s+','',s))}</li>")
        elif re.match(r"\s*\d+\.\s+", s):
            if lst != "ol": close(); out.append("<ol>"); lst = "ol"
            out.append(f"<li>{inline(re.sub(r'^\s*\d+\.\s+','',s))}</li>")
        else:
            close(); out.append(f"<p>{inline(s)}</p>")
        i += 1
    close()
    return "\n".join(out)

def chrome():
    for c in CHROME_CANDIDATES:
        if Path(c).exists(): return c
    sys.exit("No Chrome/Edge found.")

def opath(p): return str(Path(p).resolve()).replace("\\", "/")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--out")
    ap.add_argument("--title")
    a = ap.parse_args()
    src = Path(a.src)
    md = src.read_text(encoding="utf-8")
    body = md_to_html(md)
    title = a.title or src.stem
    foot = '<div class="docfoot">ShikshaLokam · generated from the content brain</div>'
    htmlpage = (f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(title)}</title>"
                f"<style>{DOC_CSS}</style></head><body>{body}{foot}</body></html>")
    out = Path(a.out) if a.out else src.with_suffix(".pdf")
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="slpdf_"))
    hp = tmp / "doc.html"; hp.write_text(htmlpage, encoding="utf-8")
    run = [chrome(), "--headless=new", "--disable-gpu", "--no-first-run",
           "--no-default-browser-check", f"--user-data-dir={tmp}",
           "--no-pdf-header-footer", f"--print-to-pdf={opath(out)}", furl(hp)]
    subprocess.run(run, check=True, capture_output=True)
    print(f"PDF: {out.resolve()}")

def furl(p): return "file:///" + opath(p)

if __name__ == "__main__":
    main()
