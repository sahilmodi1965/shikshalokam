#!/usr/bin/env python3
"""Auto-fit collage heights so every page fills its column without overflowing.

Layout in print is a fixed-point problem: a collage tall enough to kill the
dead band can push past the footer, and shrinking it re-opens the band. Doing
this by eye is what produced "several pages have content occupying only half
the page" in the first place. So we solve it numerically:

    build -> measure each page's ink -> nudge that page's collage -> repeat

Each `.collage` carries data-fit="<pdf page number>". Row height is the knob.
Converges in a handful of iterations; refuses to loop forever.

    python3 tools/report/autofit.py projects/<slug>/report.html
"""
import argparse, os, re, subprocess, sys, tempfile

TARGET_BOTTOM_MM = 272.0   # aim content bottom here (page box ends at 275mm)
TOL_MM = 6.0
MIN_ROW, MAX_ROW = 22.0, 78.0
ROOT = os.path.dirname(os.path.abspath(__file__))


def build(html, pdf):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "build_report.py"), html, "-o", pdf],
                       capture_output=True, text=True)
    if not os.path.exists(pdf):
        sys.exit("build failed:\n" + r.stdout + r.stderr)


def content_bottom_mm(pdf):
    """For every page, the y (in mm) of its lowest inked row, ignoring the footer."""
    from PIL import Image
    out = {}
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdftoppm", "-r", "60", "-png", pdf, os.path.join(td, "p")],
                       capture_output=True)
        for i, fn in enumerate(sorted(f for f in os.listdir(td) if f.endswith(".png")), start=1):
            im = Image.open(os.path.join(td, fn)).convert("L")
            w, h = im.size
            ppm = h / 297.0
            px = im.load()
            # ignore the footer strip: it always has a little grey ink
            limit = int(283 * ppm)
            last = 0
            for y in range(0, min(limit, h), 2):
                for x in range(0, w, 2):
                    if px[x, y] < 200:
                        last = y
                        break
            out[i] = last / ppm
    return out


def read_rows(html_src):
    """page-number -> (row_height, n_rows_in_that_collage)"""
    rows = {}
    for m in re.finditer(r'<div class="collage" data-fit="(\d+)" style="grid-auto-rows:([\d.]+)mm;">(.*?)</div>\s*(?=<div class="(?:page-footer|collage)"|</div>)',
                         html_src, re.S):
        page, h, body = int(m.group(1)), float(m.group(2)), m.group(3)
        nrows = 2 if "tall" in body else 1
        rows[page] = (h, nrows)
    return rows


def set_rows(html_src, page, new_h):
    return re.sub(rf'(<div class="collage" data-fit="{page}" style="grid-auto-rows:)[\d.]+(mm;">)',
                  rf'\g<1>{new_h:.1f}\g<2>', html_src, count=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--pdf")
    ap.add_argument("--max-iters", type=int, default=8)
    args = ap.parse_args()

    html = os.path.abspath(args.html)
    pdf = os.path.abspath(args.pdf or os.path.splitext(html)[0] + ".autofit.pdf")

    for it in range(1, args.max_iters + 1):
        build(html, pdf)
        bottoms = content_bottom_mm(pdf)
        src = open(html, encoding="utf-8").read()
        rows = read_rows(src)
        if not rows:
            sys.exit('no <div class="collage" data-fit="N"> found — tag them first')

        worst, changed = 0.0, 0
        for page, (h, nrows) in sorted(rows.items()):
            b = bottoms.get(page)
            if b is None:
                continue
            delta = TARGET_BOTTOM_MM - b          # +ve => room to grow
            worst = max(worst, abs(delta))
            if abs(delta) <= TOL_MM:
                continue
            new_h = max(MIN_ROW, min(MAX_ROW, h + delta / nrows))
            if abs(new_h - h) >= 0.5:
                src = set_rows(src, page, new_h)
                changed += 1
                print(f"  it{it} p{page}: bottom {b:.0f}mm -> rows {h:.1f} => {new_h:.1f}mm")
        if changed:
            open(html, "w", encoding="utf-8").write(src)
        print(f"iteration {it}: worst deviation {worst:.0f}mm, {changed} collages adjusted")
        if not changed:
            print("converged")
            break
    else:
        print("hit max iterations without full convergence")

    if os.path.exists(pdf) and args.pdf is None:
        os.remove(pdf)


if __name__ == "__main__":
    main()
