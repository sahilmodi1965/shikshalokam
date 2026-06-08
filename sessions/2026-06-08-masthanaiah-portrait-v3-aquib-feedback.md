---
date: 2026-06-08
who: Sahil
slug: masthanaiah-portrait-v3-aquib-feedback
seq: 29
live_urls:
  - https://sahilmodi1965.github.io/shikshalokam/projects/portraits.html
---

# Masthanaiah portrait rebuilt to v3 on Aquib's first review — and a publish-drift gap that had frozen four pages is closed.

Aquib Rizwan — who creates SL content daily and was just looped onto the brain to help with enrichment — gave his first review pass on the Masthanaiah Ed-Leader Portrait, routed through Sonal. Six points, all addressed in v3: the portrait now opens on a **hook paragraph** instead of the interview mechanics; a single education-leadership through-line (refuse to leave anyone out → get the children in → open up transfers → train the leaders the system forgot) is **threaded across every beat** rather than fragmented; the tone is more **diplomatic** (the leader holds his line *and* hears people out, no villains); quotes are **introduced and landed inside the prose** with smooth paragraph seams (the hard chapter rules inside the body are gone). Two integrity fixes mattered most: an **invented depiction** ("the room watched the room") that never happened was deleted, and a **conflated line** ("he turned around and never paid those fees") was cross-checked against the transcript and corrected — it had fused two separate true events (the mid-walk switch was MSc→B.Ed; the teacher selection came later, during his MSc first year). Two further unverified flourishes were cut for the same reason.

What we learned, and taught the brain: these are durable rules for *every* portrait, not one-off edits, so they were promoted into `wiki/voice/styleguide.md` as a new **Long-form Ed-Leader Portrait register** section (hook-first, one through-line, diplomatic tone, no invented scenes, cross-verify every instance, connect the quotes), with provenance recorded in a learnings note.

We also caught and fixed a real publish-drift gap. The site builder only regenerated the `invoked-6` page, so `blogs`, `captions`, `nagaland-coffee-book` and `portraits` were silently frozen behind their source — and because the no-drift check rebuilds through that same builder before diffing, it had been reporting a false "in sync." The portrait would have stayed at v2 on the live page no matter how the source changed. The builder now regenerates **every** project that has a source page, so the drift check finally covers all of them; all five pages were rebuilt (idempotent, faithful to source) and the change is live. To improve next: chase the nine enrichment gaps with Masthanaiah Sir (one named student, the doubt moment, the Medak principals' names, a photo) so v4 can carry the smallest unit of human impact — and get written consent before this goes to print.
