---
name: shikshalokam-feedback
description: Handle corrections — "this isn't right" / "not my voice" / "too corporate" / "wrong angle" / "feels off." Fixes the draft now, and when the miss points to something the brain has wrong, updates the relevant wiki/ file in the same session (sourced, with a learnings record for provenance) — no weekly-review queue.
---

# shikshalokam-feedback

When someone pushes back, two things happen immediately: the draft gets fixed, and if the brain
itself was wrong, the brain gets fixed too — this session. Feedback makes the brain smarter now.

## When this fires
- Dissatisfaction with output: "not quite right," "not my voice," "too corporate," "stiff," "wrong
  angle," "feels like a stranger wrote this," "ugh no" — or qualified signals ("para 2 works, rest
  doesn't").
- Not for "give me a shorter version" (that's a `shikshalokam-write` re-run).

## What it does
1. **Hear it exactly.** Capture the person's actual words — quote them, don't paraphrase to "they
   pushed back."
2. **One-off or structural?**
   - **One-off** = a phrase/example that missed in this draft only. Fix it in the draft now. Done.
   - **Structural** = the brain's understanding of voice / a person / a concept / the audience is
     off. Fixing the draft isn't enough — the brain is wrong.
   - When genuinely unsure, ask one line: *"Just fix this draft, or is this something the brain has
     set up wrong?"*
3. **For structural feedback, fix the brain in-session.** Update the relevant `wiki/**` file now —
   including `wiki/voice/**` (it's the team's own voice; no gate):
   - integrate the correction into the file, keep the frontmatter contract + a valid `_status`,
   - set `_status: user-validated` (a teammate just told us how it should be),
   - cite provenance: write a short `learnings/<date>-<topic>.md` recording the verbatim feedback and
     what changed, and reference it in the file's `corrected_by:`. The learning is the audit trail of
     *why* the brain changed — not a queue the change waits in.
4. **Regenerate** the draft applying the correction, and say plainly what you also taught the brain:
   *"Fixed it — and updated how we sound so it lands right next time too."*
5. The session digest records the correction and what it changed.

## What it must not do
- Don't silently overwrite a user-validated fact with no record — always leave the `learnings/`
  provenance + `corrected_by:` link.
- Don't defer a clear structural fix to "later/weekly" — absorb it now (structure stays enforced by
  lint, so this is safe).
- Don't pull from sibling brains (`cross_brain_wall: true`).
