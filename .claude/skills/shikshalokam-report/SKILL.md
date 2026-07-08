---
name: shikshalokam-report
description: Produce a designed, presentation-ready PDF report at benchmark quality — the brand-formatted programme reports (NLNF/ASC/STEAM-style) that used to take days of manual Canva work. Triggers on "make this a report", "format this report", "design the X report", "turn this doc/content into a PDF report". Uses the report design system in tools/report/ (theme.css + build_report.py). Content comes from the brain or whatever the person drops; formatting is fully automated HTML→PDF.
---

# shikshalokam-report

Formatting reports was the team's biggest time sink: content exists, but making it look like the
benchmark (NLNF 3.0-level design) took days in Canva. This skill removes that step entirely —
the brain writes the report as HTML on the house design system and prints a pixel-exact PDF.

## When this fires
- Someone has report **content** (a Google Doc, pasted text, a PDF export, brain content) and wants
  the **designed deliverable**: "make this a report", "format the ASC report", "STEAM-Manch style".
- Not for prose-only drafting (→ `shikshalokam-write`) — this is for the designed PDF artifact.

## The design system (never re-invent it)
- `tools/report/theme.css` — the complete ShikshaLokam report language, derived from the NLNF 3.0
  benchmark: brick-red/orange/blue/green palette, Montserrat, huge section headings with two-tone
  underline bars, check-circle h2s, double-chevron h3s, left-bar cards, quote cards, stat tiles,
  numbered step rows, branded data tables, SVG chart cards, cream note boxes, photo grids,
  cover band + motif tiles + tri-colour strip, maroon back cover.
- `tools/report/assets/shikshalokam-logo.png` — transparent SL logo for covers.
- `projects/steam-manch-report/report.html` — the reference implementation. **Read it before
  writing a new report**; copy its structure and component usage.

## How to produce a report
1. **Get the full content.** Read the source doc/PDF completely. Never summarize away substance —
   the report carries every table, number, name, and caveat from the source. Preserve data-source
   caveats verbatim (they are deliberate).
2. **Write `projects/<report-slug>/report.html`** as explicit A4 `.page` divs on `theme.css`
   (relative path `../../tools/report/theme.css`). One idea per page; benchmark pacing is
   generous white space, not cramming. Charts are hand-written inline SVG in a `.chartcard`.
   Photos: if images aren't supplied yet, use `.ph` placeholder boxes — never fake images.
3. **Build:** `python3 tools/report/build_report.py projects/<slug>/report.html -o <out>.pdf`
   The builder fails loudly if content overflows a page (PDF pages ≠ `.page` divs).
4. **Look at every page** (Read the PDF) and fix collisions/overflow before calling it done.
   The last visual pass is what makes it benchmark-level; never skip it.
5. Report source lives in the repo (content lane, publishes every session). The PDF is an
   artifact — regenerate on demand; attach to email/Drive only through the normal approval gates.

## Palette rule (from the team's requirements doc)
Default to the SL palette in theme.css. For joint-collaboration reports, derive an accent palette
from the partner's visual identity but keep it complementary to the SL brand — override the CSS
variables (`--maroon`, `--orange`, …) in a `<style>` block in that report's HTML only; never edit
theme.css for one report.
