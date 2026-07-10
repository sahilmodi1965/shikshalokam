---
name: shikshalokam-report
description: Produce a designed, presentation-ready PDF report at benchmark quality — the brand-formatted programme reports (NLNF/ASC/STEAM-style) that used to take days of manual Canva work. Triggers on "make this a report", "format this report", "design the X report", "turn this doc/content into a PDF report". Uses the report engine in tools/report/ (base.css + themes/ + build_report.py + autofit.py + check_report.py). Content comes from the brain or whatever the person drops; formatting is fully automated HTML→PDF.
---

# shikshalokam-report

Formatting reports was the team's biggest time sink: content exists, but making it look right took
days in Canva. This skill removes that step — the brain writes the report as HTML on the house
design system and prints a pixel-exact PDF.

**Engine v2.0.** Read `tools/report/README.md` and `tools/report/LEARNINGS.md` before starting.
`LEARNINGS.md` is the record of every correction the team has given; it exists so no note has to
be given twice.

## When this fires
- Someone has report **content** (a Google Doc, pasted text, a PDF export, brain content) and wants
  the **designed deliverable**: "make this a report", "format the ASC report".
- Not for prose-only drafting (→ `shikshalokam-write`) — this is for the designed PDF artifact.

## The one rule that governs everything
**Every programme gets its own visual identity.** Structure is shared; palette, motifs and
typography are *derived per report*. Do not copy another programme's look — v1 of the STEAM report
was rejected for exactly that ("the report currently feels very similar to the NLNF 3.0 report").

## Architecture
```
tools/report/base.css           structure only — no colour, no typefaces
tools/report/themes/<name>.css  palette + typefaces + motifs, one per programme
tools/report/assets/motifs/     brand motifs: spiral, soil wave, braid
tools/report/theme.css          compat shim for old reports. Do not extend.
```
Accent roles are **numbered** (`--c1`…`--c4`, `.hl-1`, `.q-2`, `.s-3`), never named after a colour.

## How to produce a report
1. **Get the full content.** Read the source completely. Never summarize away substance — the report
   carries every table, number, name and caveat. Preserve data-source caveats verbatim.
2. **Derive the theme.** Copy `themes/steam.css` → `themes/<programme>.css`, then apply the brand's
   own partner rule (Brand Guidelines p.13, in `assets/brand/`):
   - Common hue between ShikshaLokam and the partner? Use it (ideally Earth Maroon `#ab3935`).
   - Otherwise one colour from the partner's palette + one from ShikshaLokam's.
   - **Sample the partner's real hues from their logo files**, don't guess them.
   - **Never maroon + green in the same asset** (Guidelines p.9).
   - Headings Nunito, body Montserrat (p.10).
   - Write the derivation into the theme's header comment so it can be audited.
3. **Write `projects/<slug>/report.html`** as explicit A4 `.page` divs, linking
   `../../tools/report/base.css` **and** `../../tools/report/themes/<programme>.css`.
   - Charts: inline SVG in `.chartcard`, using `style="fill:var(--c1)"` — *not* `fill="var(--c1)"`.
   - Photos not supplied? Use `.ph.ph--motif` placeholders (they carry the motif wash, so the page
     still reads as designed). Never fake images.
   - Vary visual rhythm with `.collage`; tag each `data-fit="<pdf page>"`.
4. **Build:** `python3 tools/report/build_report.py projects/<slug>/report.html -o <out>.pdf`
5. **Auto-fit:** `python3 tools/report/autofit.py projects/<slug>/report.html` — sizes collages so
   no page is half-empty and none overflows.
6. **Check:** `python3 tools/report/check_report.py projects/<slug>/report.html --pdf <out>.pdf`
   Seven rules (R1–R7). It must PASS. Never ship a report that fails a rule.
7. **Look at every page** (Read the PDF). The checker catches known failures; only your eyes catch
   new ones. This pass is what makes it benchmark-level — never skip it.
8. Report source lives in the repo (content lane). The PDF is an artifact — regenerate on demand;
   attach to email/Drive only through the normal approval gates.

## When feedback arrives
Fix the **layer**, not the one report:
- makes the right thing default → the theme / `base.css`
- makes the wrong thing impossible → a rule in `check_report.py`
- removes the error class entirely → `autofit.py`

Then log it in `LEARNINGS.md` (feedback → root cause → where encoded). A correction that lives only
in chat will recur. Remembering is the weakest form of learning; a failing check is the strongest.
