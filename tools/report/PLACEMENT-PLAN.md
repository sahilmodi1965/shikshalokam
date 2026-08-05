# ASC 3.0 Report — Design + Picture Placement Plan
*Planning doc, 2026-07-28. Builds on the existing `tools/report/build_report.py` + `asc-3-0.json`.*

## 1. Design system (already built — confirming it matches the ask)

**Palette** (in `asc-3-0.json` → `theme`):
- **Dept blue `#183090`** — lead colour (from the Haryana Education Dept / SCERT logo)
- **SL maroon `#ab3935`** — headings + section accents
- **Brand pink `#ffaea8`** — highlights / callouts
- **Cream `#fff9e4`** + **white** — backgrounds · **ink `#2a2320` / black** — text
- *No green* (removed for this report)

**Type:** Montserrat (headings) + Nunito (body). **Motif:** arc / ring / arch SVGs (`arcs()`), used on headers and image tops. **Cover:** "Cover C" — framed, centred, image-rich (3-tile photo strip). Section kickers are numbered maroon chips.

*Action: none on design — it's done. We wire real photos into the placeholder slots and fill the content gaps.*

## 2. Picture placement — slot by slot

Photos come from the 22 district folders now uploading to **Aao School Chalein 3.0**. Files are foldered by district only (no content labels), so to pick by activity I'll use the **sheet's URL → Task-Remark map** (enrolment data / SMC meeting / working committee / door-to-door / enrolment drive / community engagement).

| # | Section | Slot (block) | Photos | What to place | Source |
|---|---------|--------------|--------|---------------|--------|
| — | **Cover C** | `cover_photos` | 3 | Hero: enrolment rally w/ "GO TO SCHOOL" posters · morning assembly · community gathering | Best of Gurugram, Nuh, Kaithal (high-impact) |
| — | **Contents** | toc hero | 1 | One strong wide shot — children heading to school | Any strong landscape |
| 1 | Program details | `split` | 1 | Community mobilisation — parents + teachers meeting / door-to-door | door-to-door / SMC meeting |
| 2 | Timelines | `figure` | 0 | Keep as a **designed 3-phase timeline graphic** (not a photo) | — |
| 3 | Program phases | add 1 `figure` per phase | 3 | P1 orientation (meeting) · P2 door-to-door / community drive · P3 felicitation | orientation · door-to-door · ceremony |
| 4 | Outreach practices | `split` | 1 | On-ground Sehyogi support OR a WhatsApp/poster (Monday Motivation) | community engagement / social asset |
| 6 | Impact analysis | `chart` + `stats` | 0 | **Rebuild** enrolment table + Top/Lowest performers as **native branded charts** (not the dashboard screenshots) | data from sheet |
| 7 | **Evidences** | `photos` grid | 6–9 | The gallery — one per activity type × spread of districts | all content types, ≥6 districts |
| 8 | Felicitation | `split` | 2–4 | SCERT ceremony (Sunil Bajaj leading; Samwartak Singh virtual) | ⚠ **event photos — likely NOT in field folders; need separately** |
| 9 | Conclusion | `figure` | 1 | Warm close — full assembly / a child in class | strongest single image |

**Selection rules:** landscape, in-focus, activity legible, faces OK but no close-up minors as hero; **skip** photos of enrolment registers / data sheets for hero slots (use at most one small one in Evidences). Prefer the districts the report already praises (Nuh, Gurugram, Kaithal, Sohna block).

## 3. Content gaps to fill (blanks in the current draft)
- Program details: **"list of ___ schools"** — need the targeted-school count.
- Timelines table: **phase durations are empty** — need dates for Prep/Launch, Implementation, Celebration.
- Impact: wire real enrolment numbers (sheet has district 2024→2025 + % growth) into native charts.

## 4. Open items for Ayush
1. **Felicitation photos** — are the SCERT ceremony images in a separate folder? (Field evidence folders won't have them.)
2. The **# of targeted schools** + **phase dates** for the two blanks.
3. Confirm: rebuild Impact as native charts (cleaner) vs. keep dashboard screenshots.

## 5. Sequence once photos land
1. Finish district upload (running).
2. Curate per the table above via the sheet's content map → copy chosen files into `tools/report/assets/photos/<slot>/`.
3. Wire filenames into `asc-3-0.json` image slots; fill content gaps.
4. `python tools/report/build_report.py` → review HTML/PDF.
