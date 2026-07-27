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
  InvokED-adjacent ones. Final shape: **6 mains + 4 probes = 10 turns**, Q4 holding 4 of them.
  → https://docs.google.com/spreadsheets/d/1qMhSkrACZb4zmM2cBWDkyhEma_lDBa6_MkHnSsKU2B8/edit#gid=395746484
- **`projects/invoked-impact-survey/`** — new project page + `questions-10turn.json`, the source the
  tab is generated from. Regenerate the tab any time by re-running `sheet-add-tab --replace`.
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
- **Decision needed from Sonal:** can registration data pre-fill role / org / country / editions? If
  yes, Q1+Q2 collapse to a confirm-tap and 2 turns come free — best spent on *"was that collaboration
  with someone you met at InvokED, or someone you already knew?"*, which separates InvokED-caused
  from InvokED-adjacent.
- `Dashboard_Metrics` and `Report_Metrics/Templates` still reference the original 12 questions —
  alignment pass needed before build.
