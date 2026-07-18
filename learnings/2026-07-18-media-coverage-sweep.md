# Learning — media coverage sweep (SL & Shikshagraha)

**Date:** 2026-07-18 · **Person:** Aquib

## What happened
Aquib asked for every web/news mention of ShikshaLokam or Shikshagraha in a sheet. Started from a
WebSearch sweep (35 rows), then merged in the two internal Coverage Dossiers (Shikshagraha +
ShikshaLokam Google Sheets) — extracting URLs from hyperlinks hidden under cell text across 34
tabs / 3 layouts. Result: a **2,548-row** deduped Google Sheet (*Media Coverage Tracker*, in
Aquib's private Drive), sorted newest-first, with normalized dates + inferred Type. Ingested a
clean index into `wiki/sources/media-coverage-sweep-2026-07.md` (Sheet = canonical dataset).

## What we learned (provenance for the source entry)
- **Most "coverage" is wire syndication.** The same ANI/PTI release repeats across The Wire,
  Tribune, Business Standard, ThePrint, ANI, Newsvoir, etc. Row count ≠ independent pickup.
- **Genuinely earned pieces are few:** The CSR Universe (×2), Careerindia, HundrED, Societal
  Platform, Synergos, CSRBox, India CSR. These are the citable third-party voices.
- **Sweep is US-indexed only** — paywalled / print / regional-language coverage under-surfaced;
  several pages exposed no publish date.

## How to apply
- When a draft needs "as featured in…" credibility, cite the ★ earned rows in
  [[media-coverage-sweep-2026-07]], not the wire-syndicated bulk.
- `gs.py` has no `sheet-create` — a one-off script reusing `gs.svc()` + the Sheets scope creates
  and fills a sheet, then moves it into the Docs folder via Drive `addParents`. Reusable pattern;
  candidate to fold into `gs.py` as a real `sheet-create` verb (architecture lane).

## Next-pass-to-action
- Optional second sweep with outlet-specific queries (Hindu / TOI / EdTech trades) to close gaps.
- Consider filing a `gs.py sheet-create` feature via the ops lane.
