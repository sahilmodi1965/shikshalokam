#!/usr/bin/env python3
"""Brand + layout checks for a ShikshaLokam report. The engine's memory.

Every rule here exists because a human once had to point the mistake out.
A correction that lives only in an email will recur; a correction encoded
here cannot ship twice. When new feedback arrives, add a RULE — don't just
fix the one report.

    python3 tools/report/check_report.py projects/<slug>/report.html [--pdf out.pdf]

Rules
  R1  page-count     PDF pages == .page divs (no silent overflow)
  R2  half-empty     no page leaves a large dead band above its footer
                     [Aquib, 2026-07-10: "content occupying only half the
                      page, leaving large areas of unused white space"]
  R3  no-green+maroon a theme must not use maroon and green together
                     [Brand Guidelines p.9]
  R4  role-classes   report HTML must not name colours in class names
                     (.hl-maroon can't survive a palette swap; .hl-1 can)
  R5  var-url        url() inside a CSS custom property must be a data: URI
                     (Chrome resolves it against the HTML, not the CSS)
  R6  theme-identity a report must not link another programme's theme
"""
import argparse, os, re, subprocess, sys, tempfile

MM_PER_IN = 25.4
DEAD_BAND_MM = 45.0        # flag pages whose content stops this far above the footer
FOOTER_BAND_MM = 20.0      # bottom strip that holds the page footer
COLOUR_WORDS = ("maroon", "orange", "green", "blue", "cream", "violet", "cyan", "indigo")


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def fail(rule, msg):
    print(f"  FAIL [{rule}] {msg}")
    return 1


def ok(rule, msg):
    print(f"  ok   [{rule}] {msg}")
    return 0


def r1_page_count(html_path, pdf_path):
    divs = len(re.findall(r'class="page[ "]', open(html_path, encoding="utf-8").read()))
    out = sh(["pdfinfo", pdf_path]).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    if not m:
        return ok("R1", "pdfinfo unavailable; skipped")
    pages = int(m.group(1))
    if pages != divs:
        return fail("R1", f"{pages} PDF pages but {divs} .page divs — content is overflowing")
    return ok("R1", f"{pages} pages == {divs} .page divs")


def r2_half_empty(pdf_path):
    """Render each page and find the lowest non-white pixel above the footer band."""
    from PIL import Image
    bad = []
    with tempfile.TemporaryDirectory() as td:
        dpi = 60
        sh(["pdftoppm", "-r", str(dpi), "-png", pdf_path, os.path.join(td, "p")])
        pages = sorted(f for f in os.listdir(td) if f.endswith(".png"))
        for i, fn in enumerate(pages, start=1):
            im = Image.open(os.path.join(td, fn)).convert("L")
            w, h = im.size
            px_per_mm = h / 297.0
            footer_top = int(h - FOOTER_BAND_MM * px_per_mm)
            body = im.crop((0, 0, w, footer_top))
            # a row is "inked" if any pixel is clearly darker than paper
            bw, bh = body.size
            data = body.load()
            last_ink = 0
            step = 2
            for y in range(0, bh, step):
                for x in range(0, bw, step):
                    if data[x, y] < 235:
                        last_ink = y
                        break
            gap_mm = (footer_top - last_ink) / px_per_mm
            if gap_mm > DEAD_BAND_MM:
                bad.append((i, round(gap_mm)))
    if bad:
        detail = ", ".join(f"p{n} ({g}mm dead)" for n, g in bad)
        return fail("R2", f"half-empty pages: {detail}")
    return ok("R2", "no page leaves a dead band above the footer")


def r7_footer_overlap(pdf_path, flush_pages=(1,)):
    """Content must not paint into the bottom margin / under the footer.

    R2 alone has a blind spot: a block that overflows the page bottom leaves
    NO dead band, so a half-empty page and an overflowing one look identical
    from the top. This rule catches the other side.
    Page padding-bottom is 22mm, so a normal page must be clean below 275mm
    except for the footer itself (thin, grey, ~2% ink).
    """
    from PIL import Image
    bad = []
    with tempfile.TemporaryDirectory() as td:
        dpi = 60
        sh(["pdftoppm", "-r", str(dpi), "-png", pdf_path, os.path.join(td, "p")])
        pages = sorted(f for f in os.listdir(td) if f.endswith(".png"))
        for i, fn in enumerate(pages, start=1):
            if i in flush_pages or i == len(pages):   # cover + back cover bleed by design
                continue
            im = Image.open(os.path.join(td, fn)).convert("L")
            w, h = im.size
            px_per_mm = h / 297.0
            band = im.crop((0, int(275 * px_per_mm), w, h))
            px = list(band.getdata())
            inked = sum(1 for v in px if v < 200) / len(px)
            if inked > 0.06:
                bad.append((i, round(inked * 100)))
    if bad:
        detail = ", ".join(f"p{n} ({pct}% ink in bottom margin)" for n, pct in bad)
        return fail("R7", f"content overflows into the footer margin: {detail}")
    return ok("R7", "no page paints into the bottom margin")


def _hexes(css):
    return [h.lower() for h in re.findall(r"#([0-9A-Fa-f]{6})", css)]


def _is_green(h):
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    mx = max(r, g, b)
    return g == mx and g - max(r, b) > 24 and mx > 40


def _is_maroon(h):
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return r == max(r, g, b) and r - max(g, b) > 40 and r > 90


def r3_no_green_maroon(theme_paths):
    rc = 0
    for p in theme_paths:
        css = open(p, encoding="utf-8").read()
        # only the palette block, not the prose comment
        block = re.search(r":root\s*\{(.*?)\}", css, re.S)
        if not block:
            continue
        hs = _hexes(block.group(1))
        greens = [h for h in hs if _is_green(h)]
        maroons = [h for h in hs if _is_maroon(h)]
        name = os.path.basename(p)
        if greens and maroons:
            rc |= fail("R3", f"{name} pairs maroon (#{maroons[0]}) with green (#{greens[0]}) — Brand p.9 forbids this")
        else:
            rc |= ok("R3", f"{name} palette respects the maroon/green rule")
    return rc


def r4_role_classes(html_path):
    html = open(html_path, encoding="utf-8").read()
    hits = set()
    for cls in re.findall(r'class="([^"]+)"', html):
        for token in cls.split():
            if any(w in token for w in COLOUR_WORDS):
                hits.add(token)
    if hits:
        return fail("R4", f"colour-named classes in report HTML: {sorted(hits)} — use numbered accent roles")
    return ok("R4", "no colour-named classes; palette can be swapped")


def r5_var_url(theme_paths):
    rc = 0
    for p in theme_paths:
        css = open(p, encoding="utf-8").read()
        bad = re.findall(r"(--[a-z-]+)\s*:\s*url\((?!\s*[\"']?data:)", css)
        name = os.path.basename(p)
        if bad:
            rc |= fail("R5", f"{name}: custom props {bad} use a file-relative url(); Chrome resolves it against the HTML. Inline a data: URI.")
        else:
            rc |= ok("R5", f"{name}: motif url()s are data: URIs")
    return rc


def r6_theme_identity(html_path):
    html = open(html_path, encoding="utf-8").read()
    slug = os.path.basename(os.path.dirname(os.path.abspath(html_path)))
    themes = re.findall(r'href="[^"]*themes/([a-z0-9-]+)\.css"', html)
    if not themes:
        return fail("R6", "report links no theme — it must link base.css + its own themes/<name>.css")
    linked = themes[0]
    if linked == "nlnf" and not slug.startswith("nlnf"):
        return fail("R6", f"'{slug}' links the NLNF theme — every programme needs its own identity (Aquib, 2026-07-10)")
    return ok("R6", f"'{slug}' links its own theme: themes/{linked}.css")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--pdf")
    args = ap.parse_args()

    html = os.path.abspath(args.html)
    pdf = os.path.abspath(args.pdf) if args.pdf else os.path.splitext(html)[0] + ".pdf"
    root = os.path.dirname(os.path.abspath(__file__))
    # Only the theme(s) THIS report links are held to the brand rules. nlnf.css
    # is a faithful record of the old benchmark (which does pair maroon+green);
    # rewriting it would falsify history. New themes must comply.
    linked = re.findall(r'href="[^"]*themes/([a-z0-9-]+)\.css"', open(html, encoding="utf-8").read())
    themes = [os.path.join(root, "themes", f"{t}.css") for t in linked]
    themes = [t for t in themes if os.path.exists(t)]

    print(f"checking {os.path.relpath(html)}")
    rc = 0
    rc |= r4_role_classes(html)
    rc |= r6_theme_identity(html)
    rc |= r3_no_green_maroon(themes)
    rc |= r5_var_url(themes)
    if os.path.exists(pdf):
        rc |= r1_page_count(html, pdf)
        rc |= r2_half_empty(pdf)
        rc |= r7_footer_overlap(pdf)
    else:
        print(f"  --   no PDF at {os.path.relpath(pdf)}; skipped R1/R2/R7")

    print("PASS" if rc == 0 else "FAIL")
    sys.exit(rc)


if __name__ == "__main__":
    main()
