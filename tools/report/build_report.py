#!/usr/bin/env python3
"""Render a ShikshaLokam report (HTML built on tools/report/theme.css) to PDF.

Usage:
    python3 tools/report/build_report.py path/to/report.html [-o out.pdf]

Uses headless Google Chrome so the PDF is pixel-identical to the HTML preview.
Each report page is an explicit A4 `.page` div; after building, the script
verifies the PDF page count matches the number of `.page` divs so silent
overflow (content spilling onto an extra page) never ships unnoticed.
"""
import argparse
import os
import re
import subprocess
import sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def count_page_divs(html_path):
    with open(html_path, encoding="utf-8") as f:
        return len(re.findall(r'class="page[ "]', f.read()))


def pdf_page_count(pdf_path):
    try:
        out = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True).stdout
        m = re.search(r"Pages:\s+(\d+)", out)
        return int(m.group(1)) if m else None
    except FileNotFoundError:
        return None  # pdfinfo not installed; skip the check


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("-o", "--out")
    args = ap.parse_args()

    html = os.path.abspath(args.html)
    if not os.path.exists(html):
        sys.exit(f"not found: {html}")
    out = os.path.abspath(args.out or os.path.splitext(html)[0] + ".pdf")

    if not os.path.exists(CHROME):
        sys.exit("Google Chrome not found — install it or update CHROME in this script")

    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={out}",
        # give webfonts time to load before printing
        "--virtual-time-budget=15000",
        f"file://{html}",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(out):
        sys.exit(f"Chrome failed to produce a PDF:\n{res.stderr[-2000:]}")

    expected = count_page_divs(html)
    actual = pdf_page_count(out)
    size_mb = os.path.getsize(out) / 1e6
    print(f"built {out} ({size_mb:.1f} MB)")
    if actual is not None:
        if actual == expected:
            print(f"page check OK: {actual} pages = {expected} .page divs")
        else:
            print(f"WARNING: {actual} PDF pages but {expected} .page divs — content is overflowing a page")
            sys.exit(2)


if __name__ == "__main__":
    main()
