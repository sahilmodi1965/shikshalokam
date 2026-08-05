---
date: 2026-08-05
person: Ayush Tank
project: aao-school-chalein-3
_status: done
---

# ASC 3.0 programme report — built end to end

## What got made
- **An 11-page branded programme report** for *Aao School Chalein 3.0* (SCERT Haryana),
  generated from `tools/report/asc-3-0.json` — no Canva in the loop.
- **24 real photographs** curated from the 22-district Drive folder and placed so each one
  supports the text beside it.
- Published as a page anyone on the team can open, plus the PDF.

## What we learned
- **The photo folder is half paper.** Of 7,368 district photos, roughly half are handwritten
  enrolment registers and data sheets. Usable imagery is the minority — always curate by eye.
- **Photos belong beside their text, not in a gallery.** A 12-tile grid read as decoration;
  moving each image next to the paragraph it evidences fixed it. The Evidences section became
  captioned rows naming the activity and district.
- **One motif, composed many ways.** The nested-arc unit now does real work — bullets, every
  section rule (the unit repeated into a scallop band), cover photo corners — all in one colour.
- **Sections flow continuously.** One-section-per-page left pages half empty; a paginator now
  packs blocks and carries headings with their content.
- **Full-resolution photos made the PDF unopenable** at 16MB. Capping the long edge at 1600px
  halved it with no visible loss.

## Machinery added
- `tools/report/review.py` — serves the report at localhost:8765; hover any element, comment,
  and it auto-saves to `out/<slug>-comments.json` for the brain to read. No export step.
- `tools/report/photo-manifest.json` — records the Drive file id behind every photo used, so
  nobody re-sweeps 7,368 images to find the same pictures again.
- `.gitignore` now excludes `tools/*/out/` and **all programme photographs** — this repo is
  public and the images show identifiable children.

## Still open (needs Ayush / SCERT)
- The targeted-school count ("a list of ___ schools") — blank in the source document too.
- Phase durations for Preparation & Launch / Implementation / Celebration.
- The district enrolment sheet behind the impact chart.
- Photographs of the SCERT felicitation ceremony itself — the ones in use are school-level.

## To improve next
- Quota went overwhelmingly on *looking* at rendered pages. Check by page summary first and
  open only what changed. Written up for the team as a working note.
