# tools/report — the report engine

**Engine version: 2.0** (see `LEARNINGS.md` for what each version learned.)

Turns report content into a designed, presentation-ready PDF. Nobody formats reports by
hand: the brain writes `report.html` against the design system, the builder prints it with
headless Chrome, the checker refuses to let known mistakes ship.

> **Every report gets its own identity.** The goal is *not* "make it look like the last
> report." Structure is shared; palette, motifs and typography are derived per programme
> from the ShikshaLokam Brand Guidelines and the partner logos. v1 of the STEAM report
> failed review precisely because it inherited NLNF 3.0's look.

## Use
```bash
# 1. build
python3 tools/report/build_report.py projects/<slug>/report.html -o out.pdf

# 2. let the layout solve itself (fills pages, prevents overflow)
python3 tools/report/autofit.py projects/<slug>/report.html

# 3. gate it — brand + layout rules, exit 1 on any violation
python3 tools/report/check_report.py projects/<slug>/report.html --pdf out.pdf
```

## Architecture
```
base.css              structure, scaffold, type scale.  NO colour, NO typefaces.
themes/<name>.css     palette + typefaces + motifs.     One per programme.
assets/motifs/*.svg   brand motifs (spiral, soil wave, braid) — Guidelines p.15–16
theme.css             compat shim (base + nlnf) for older reports. Do not extend.
```
A report links **`base.css` + its own theme**. Accent roles are numbered
(`--c1`…`--c4`, `.hl-1`, `.q-2`, `.s-3`), never named after a colour — a class called
`.hl-maroon` cannot survive a palette change.

## Starting a new report
1. Copy `themes/steam.css` to `themes/<programme>.css`.
2. **Derive** the palette — don't pick it. Brand Guidelines p.13:
   - Common hue between ShikshaLokam and the partner? Use it (ideally Earth Maroon `#ab3935`).
   - Otherwise: one colour from the partner's palette + one from ShikshaLokam's.
   - Sample the partner's real hues from their logo files rather than guessing.
3. **Never put maroon and green in the same asset** (Guidelines p.9). Checker enforces this.
4. Motifs must be inlined as `data:` URIs — a file-relative `url()` inside a CSS custom
   property resolves against the *HTML*, not the CSS, and silently 404s.
5. Write the derivation into the theme's header comment, so the next person can audit it.

## The checks (`check_report.py`)
| Rule | What it catches |
|------|-----------------|
| R1 | PDF page count ≠ `.page` divs (silent overflow) |
| R2 | a page leaving a large dead band above its footer |
| R3 | a theme pairing maroon with green |
| R4 | colour-named CSS classes in the report HTML |
| R5 | file-relative `url()` in a CSS custom property |
| R6 | a report linking another programme's theme |
| R7 | content overflowing into the footer margin |

R2 and R7 are opposites and must both hold: a block that overruns the page bottom leaves no
dead band, so from the top a half-empty page and an overflowing one look identical.

## Conventions
- A report is a sequence of explicit A4 `.page` divs — full layout control, page by page.
- Charts are inline SVG in `.chartcard`. Use `style="fill:var(--c1)"`, **not**
  `fill="var(--c1)"` — Chrome does not resolve `var()` in SVG presentation attributes.
- Missing photos get `.ph.ph--motif` placeholders that carry the theme's motif wash, so an
  image-less page still reads as designed. Vary composition with `.collage`.
- Tag each `.collage` with `data-fit="<pdf page>"` so `autofit.py` can size it.

## When feedback arrives
Fix the *layer*, not the one report, then log it in `LEARNINGS.md`. If a note could recur,
it belongs in `check_report.py` as a rule — not in someone's memory.

The team-facing skill is `.claude/skills/shikshalokam-report/SKILL.md`.
