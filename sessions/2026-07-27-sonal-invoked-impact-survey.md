---
date: 2026-07-27
person: Sonal Bhasin
project: invoked-impact-survey
---

# InvokED Impact Survey cut to 10 turns — and the engine learned to write Sheet tabs

## What got made
- **`Questions_Revised_10`** — a new tab in Sonal's InvokED MItra template, holding the redesigned
  questionnaire: 12 mains + ~25 follow-ups (~30 turns) → **10 turns total, probes included**.
  Original `Questions` tab untouched, so the two stay comparable. Structured as **7 main questions
  + 3 probes**, with probes in the follow-up column against their parent — Sonal's correction: a
  probe numbered as its own question ("Q3 says Q4 is its probe") fights the sheet's columns.
  Then Sonal cut the Stories & Recognition question as no longer aligned; its three report fields
  (story willingness, Awards nomination, follow-up contact) move to the post-close consent screen,
  which costs no turn. The freed turn went into a **third probe on Q4** — the attribution question
  ("met at InvokED, or already knew them?"), separating InvokED-caused collaborations from
  InvokED-adjacent ones. Finally Sonal raised the **future-readiness** listening mission; we added
  one turn for it (how leaders define the term + what they're doing about it) and funded it by
  cutting editions-attended, the weakest and most pre-fillable turn. Final shape: **6 mains + 4
  probes = 10 turns**, Q3 (action) holding 4 of them.
  → https://docs.google.com/spreadsheets/d/1qMhSkrACZb4zmM2cBWDkyhEma_lDBa6_MkHnSsKU2B8/edit#gid=1181288946
- **`Dashboard_Metrics_Revised`** and **`Report_Metrics_Revised`** — both re-sourced to the new
  question numbering. Not just renumbering: **two metrics were retired** (the measured perception
  baseline, and network continuity as a single %) because no question feeds them honestly any more;
  **repeat participation is orphaned** until pre-fill or a post-close tap ships; and **four metrics
  are new**, led by **InvokED-caused vs InvokED-adjacent** — the split between partners met at
  InvokED and partners already known, which is the most defensible number in the survey and should
  lead the Impact Report. A methodology block on self-selection went into the report tab.
- **`projects/invoked-impact-survey/`** — project page + three JSON sources (`questions-10turn`,
  `dashboard-metrics`, `report-metrics`). Every revised tab regenerates from these with
  `gs.py sheet-add-tab --replace`, so the sheet is never hand-edited.
- **`gs.py sheet-add-tab`** — new engine command: creates a tab and fills it from a JSON file, with
  header bolding, freeze rows and column widths. Refuses to overwrite an existing tab without
  `--replace`; never touches other tabs. Wired into the gsuite SKILL.md + engine README.

## The design call
The requirement doc names post-event **action & collaboration** the most critical capture area, so
3 of the 10 turns went there (Q5–Q7) — that block is the only one producing Action Stories
(who / what / outcome), which the Impact Report is built from. Paid for by cutting the "before
InvokED" baseline (senior respondents reconstruct baselines poorly, and the shift is what gets
reported), the profile clarifier probes, and the standalone network question — then merging four
questions into two.

## The call on future readiness
Sonal asked whether the "listen to a million voices on future readiness" mission should ride inside
this survey or stand alone. **Both** — a separate instrument for the mission itself (different
audience, scale and language; 150–250 alumni will never be a million voices), plus **one turn here**,
because this audience is different in kind: they're the people whose *definition* shapes how the
sector uses the term. Their answers are narrative source material, not a representative measure.

## What we learned
- **`sheet-update`'s `--values` can't carry real content.** It splits on `|` and `;;`, and any
  question with a branch (`If yes … | If no …`) breaks it. That gap is why `sheet-add-tab` takes
  JSON — a file-based path was the only honest fix, not an escaping workaround.
- **A brain launched outside its own directory is a stranger to itself.** This session started in
  `~` rather than `~/shikshalokam`, so CLAUDE.md and all ten skills stayed unloaded. The brain told
  Sonal it "had no Sheets tool" and offered her an Apps Script to paste — while `sheet-read` /
  `sheet-update` sat in `tools/gsuite/`. She had to push back twice ("how do the abilities and
  features build are getting lost by you") before it went looking. **Capability the brain can't see
  is capability it doesn't have.** NOT filed as an ops issue — `gh` isn't installed on this
  machine, so the architecture lane is unavailable here. Someone with `gh` should file it:
  *session start should detect it's running outside the brain directory and say so.*
- **Sonal's standing rule on sheets, now recorded:** her own sheets are edited directly, no asking.
  Other people's sheets are read-only unless she specifically says otherwise.

## Next
- **Load-bearing decision:** can registration data pre-fill role / org / country / **editions
  attended**? Editions no longer has a turn, so pre-fill (or a post-close tap) is now the only way
  that credibility metric survives. If neither is possible, reinstate it and drop Q5 (continuity).
- **Bot system prompt** — persona, tone and the probing rules turned into actual instructions for
  the LLM. Not started; the rules currently live only as sheet columns.
- **A separate future-readiness listening survey: NOT being built for now** (Sonal, 2026-07-27).
  Consequence to hold onto — Q6 is the only future-readiness data there is, so the Impact Report
  must frame it as 150–250 senior leaders, never as sector-wide listening.
