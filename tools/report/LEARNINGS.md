# Report engine — learnings log

The engine's memory. Every entry is a piece of human feedback converted into a
rule the engine enforces, so the same note never has to be given twice.

**The discipline:** feedback → find the layer where it can be *enforced* → encode
it there → record it here. A correction that lives only in an email will recur.
Remembering is the weakest form of learning; a check that fails the build is the
strongest.

Layers, weakest to strongest:
1. **Prose** (this file, the skill) — context a human needs.
2. **Theme / CSS** — makes the right thing the default.
3. **Checker** (`check_report.py`) — makes the wrong thing *fail*.
4. **Fitter** (`autofit.py`) — removes the class of error entirely.

---

## v2.0 — 2026-07-10 · Aquib Rizwan (with Sonal, Ayush, Neeraj)

Feedback on STEAM Manch v1, given in the requirements doc and by email.

| # | Feedback | Root cause | Encoded as |
|---|----------|-----------|------------|
| 1 | "The report feels very similar to NLNF 3.0 … it should have a more distinct design language." | `theme.css` welded the NLNF palette to the layout. A new report could not inherit structure without inheriting identity. | Split into `base.css` (structure, no colour) + `themes/<name>.css`. Checker **R6** fails any report that links another programme's theme. |
| 2 | "The colour palette appears to have been directly carried over … adopt a unique palette drawn from ThinkTac and SCERT." | Palette was eyeballed from the printed NLNF PDF (`#A6413C`), not derived from the brand doc (`#ab3935`) or the partner logos. | `themes/steam.css` derives the palette by the brand's own partner rule (Guidelines p.13). Partner hues sampled programmatically from the supplied logo files. Derivation is written into the theme header. |
| 3 | "Motifs, icons and coloured boxes mirror NLNF … the report should have its own contextualised visual language." | Cover was a 12-tile grid of generic STEM icons, straight from NLNF. | Real brand motifs (spiral, soil wave, braid — Guidelines p.15–16) generated as SVG in `assets/motifs/`, carried by theme variables. Cover rebuilt as a photo-led composition. |
| 4 | "Front and back covers … feel quite basic." | — | Covers rebuilt: four real partner logos (optically balanced), motif wash in the title band, full-width soil wave on the back cover. |
| 5 | "Several pages have content occupying only half the page … for example, Page 9." | No one was measuring. It was nine pages, not one. | Checker **R2** flags any page leaving a dead band above its footer. **R7** flags the opposite failure (content overflowing into the footer). `autofit.py` solves the layout numerically. |
| 6 | "Explore more creative ways of presenting visuals — collages, varied image grids — instead of standard image placements." | One repeated 2-up placeholder grid. | `.collage` mosaic in `base.css`; composition deliberately varies down the report. |

### Rules the brand doc gave us that nothing was checking

- **Maroon and green must never appear in the same asset** (Guidelines p.9). The
  NLNF theme pairs them. That is now checker **R3** — for *new* themes. `nlnf.css`
  is left as a faithful record of the old benchmark; rewriting it would falsify
  history. **Worth raising with the team: the NLNF 3.0 benchmark itself breaks
  this rule.**
- **Typography is Nunito (headings) + Montserrat (body)** (p.10). v1 used
  Montserrat throughout.
- **The colour logo may not sit on a background close to its own maroon** (p.3).
  The back cover now gives it a white plate.

### Engineering traps found (encoded so they can't recur)

- `url()` inside a **CSS custom property** resolves against the *HTML document*,
  not the stylesheet. Every motif silently 404'd. → motifs are inlined as `data:`
  URIs; checker **R5** enforces it.
- `fill="var(--c1)"` as an **SVG presentation attribute** does not resolve in
  Chrome. Must be `style="fill:var(--c1)"`, or chart ink won't follow the theme.
- `background-position: 116%` slides a motif *out of view* on a large element
  (image-% aligns to container-%). Use length offsets.
- Colour-named CSS classes (`.hl-maroon`) cannot survive a palette swap.
  Numbered accent roles (`.hl-1`) can. Checker **R4**.

### Still open
- Programme photographs not yet supplied (requested 2026-07-08; Aquib confirmed
  2026-07-10 they are being collected — proceed on placeholders).
- ASC 3.0 report content received but not yet built.

---

## v1.0 — 2026-07-08

First build. Content complete and accurate (every table, number and note from the
source doc). Design derived from the NLNF 3.0 benchmark — which is precisely what
v2 had to undo. **Lesson: "match the benchmark" is the wrong instruction; the
right one is "match the brand, contextualise the programme."**
