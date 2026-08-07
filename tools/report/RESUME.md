# ASC 3.0 report — where we left off (7 Aug 2026)

Pick this up cold. Everything below is committed; nothing is pushed.

## Open it
```bash
python tools/report/build_report.py tools/report/asc-3-0.json     # -> out/asc-3-0-report.pdf
python tools/report/review.py        tools/report/asc-3-0.json     # comment on it, localhost:8765
```
Live copy (opens anywhere, no build):
<https://claude.ai/code/artifact/2bdab2c0-14b5-473a-afba-527e491c1f9d>
Team note on session cost: <https://claude.ai/code/artifact/1aea0567-8221-4796-b5bb-cdceb6a6e124>

## State
11 pages · 8.6 MB · page fill 157–249 mm of 249 mm, no overflow, no large holes.
Content is faithful to the source `ASC 3.0 Report.pdf` — **nothing invented**.
Layout language adapted from **NLNF 3.0**: phase chips, chevron timeline, icon rows.

## Blocked on Ayush / SCERT
1. The targeted-school count — "a list of ___ schools" is blank in the source too.
2. Phase durations for Preparation & Launch / Implementation / Celebration.
3. The district enrolment sheet behind the impact chart (only prose %s so far).
4. Photographs of the **SCERT felicitation ceremony**. The ones in use are
   school-level felicitations, captioned honestly as such.

## Decisions already made — don't redo these
- **Photos are chosen.** 24 in use, picked from the 22-district Drive folder across two
  sweeps. `photo-manifest.json` holds the Drive id of every one. **Do not sweep again.**
- Photos support the text they sit beside; **never a gallery**.
- One motif colour: SL maroon. One unit, composed (bullets / rules / rings / cover corners).
- No arch-shaped photo frames — tried, rejected.
- Benchmarks other than NLNF 3.0 are out of scope.

## Offered, awaiting a yes
Sections NLNF has that we don't, all of which need **new writing**, not reshaped content:
Foreword with a signatory · Executive Summary · Acknowledgement · a
Challenges / Learnings / Way Forward split (ours folds these into Reflections +
Conclusion) · full-bleed photo dividers (~4 extra pages).

## Careful
- `tools/report/` **collides with Sahil's engine on `origin/main`** (v2.0, HTML-in,
  with `theme.css` + `check_report.py` + a `shikshalokam-report` skill, which shipped the
  STEAM Manch report). Ours is a second, unpushed engine. **Resolve with Sahil before pushing.**
  Local work is pinned at branch `asc-3-0-report-work` / tag `asc-3-0-2026-08-07`.
- **Another session works in this repo concurrently.** On 7 Aug its `pull --rebase` ran while
  this one was committing: HEAD moved mid-command and a pin was dragged onto the wrong commit.
  Nothing was lost, but **re-check `git log` before trusting a pin**, and don't rewrite history
  here — a teammate's commits sit on top of ours.
- Commit `8370bdb` is labelled "line-ending normalisation" but actually carries that other
  session's caption + campaign edits. Left as-is rather than rewriting shared history.
- Never commit programme photographs — this repo is **public** and they show
  identifiable children. `.gitignore` blocks them; the manifest makes them re-fetchable.
- Fonts must stay inlined. A font-CDN `@import` is invisible in headless print.
