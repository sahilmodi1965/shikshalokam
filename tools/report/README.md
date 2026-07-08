# tools/report — the report engine

Turns report content into a designed, presentation-ready PDF at the NLNF 3.0 benchmark level.
Nobody formats reports by hand any more: the brain writes `report.html` on the design system,
the builder prints it with headless Chrome.

## Use
```
python3 tools/report/build_report.py projects/<slug>/report.html -o out.pdf
```
The builder verifies PDF page count == number of `.page` divs, so silent overflow fails the build.

## Files
- `theme.css` — the ShikshaLokam report design system (palette, typography, every component:
  cover, TOC, section headings, cards, stat tiles, step rows, tables, chart cards, note boxes,
  photo placeholders, back cover). Derived from the NLNF 3.0 benchmark report.
- `build_report.py` — HTML → PDF via headless Chrome (`--print-to-pdf`), plus the overflow check.
- `assets/shikshalokam-logo.png` — transparent logo for covers.
- Reference implementation: `projects/steam-manch-report/report.html`.

## Rules
- A report is a sequence of explicit A4 `.page` divs — full layout control, page by page.
- Charts are inline SVG inside `.chartcard` (single brand colour per chart, benchmark style).
- Missing photos get `.ph` placeholder boxes; drop real images in when the team shares them.
- Per-report palette overrides (joint-collaboration reports) go in that report's HTML
  `<style>` block — never edit theme.css for one report.

The team-facing skill is `.claude/skills/shikshalokam-report/SKILL.md`.
