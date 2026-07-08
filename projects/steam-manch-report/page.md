---
project: steam-manch-report
title: "STEAM Manch 2025–26 — designed programme report (report-engine pilot)"
_status: user-validated
last_updated: 2026-07-08
maintainer: Sahil Modi
daily_user: Aquib Rizwan
page_budget_tokens: 8000
sources:
  - "Aquib's Drive folder 'AI Report Task' (benchmarks: NLNF 3.0, PBL, VAM · content: ASC 3.0, STEAM Manch · requirements doc), shared 2026-07-08"
voice: "Formal programme-report register, as in the source content — data-faithful, caveats preserved verbatim"
---

# STEAM Manch 2025–26 — designed programme report

The pilot for the **report engine** (`tools/report/`): the team's biggest bottleneck was manually
formatting programme reports to benchmark (NLNF 3.0) quality — Canva attempts weren't landing.
This workspace holds the first fully generated one.

## Status
- **v1 built 2026-07-08** — 23-page A4 PDF, full STEAM Manch 2025–26 content (exec summary,
  context/design, participation data + charts, STEAM Mela, teacher evaluation + top-11 table,
  challenges, spotlight, recommendations, conclusion, appendix), in the ShikshaLokam benchmark
  design language. Source: `report.html` (build: `python3 tools/report/build_report.py …`).
- Sent to Aquib (same email thread) as v1 for review.

## Open items
- **Photos**: Aquib hasn't shared programme images yet (asked in thread 2026-07-08). `.ph`
  placeholder boxes mark every slot; drop images in and rebuild.
- **Partner logos**: SCERT Haryana / सक्षम हरियाणा / ThinkTac logos are text chips on the cover
  until the team shares the real assets.
- Known source-data quirk, preserved as-is: exec summary says **519** teachers across all 4 cycles
  (evaluation dataset) while participation records say **598** — the source report carries both
  with the distinction; do not "fix" one to the other without Aquib's word.
- v2 direction after Aquib/Sonal feedback; then run the engine on ASC 3.0 (content has gaps —
  blank school count, missing timeline durations — needs Aquib's numbers first).
