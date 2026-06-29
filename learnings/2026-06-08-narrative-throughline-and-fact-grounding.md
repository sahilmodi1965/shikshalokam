---
name: narrative-throughline-and-fact-grounding
description: Sonal's second round of feedback on the Masthanaiah portrait — story over report wasn't enough; narrative pieces also need an explicit throughline, a real hook paragraph, diplomatic connective tone, and every dramatized beat checked against the source
metadata:
  type: feedback
---

# Learning — narrative pieces need a throughline, a hook, a diplomatic register, and grounded beats

## What Sonal said (verbatim)

On the v2 recompile of the Masthanaiah portrait ("The dropout who refused to leave"):

> "The tone should be diplomatic. The narrative of education leadership and how it works to change
> system should be brought in. (Currently it seems fragmented)"
>
> "Mistakes like a room with a room and quoting the instance as depiction which did not happen in
> real life (The room watched)"
>
> "Cross verification of instance and lines (He turned around and never paid those fees)"
>
> "Currently I have feel instances etc are just quotes or said without proper connectors in
> between."
>
> "The shift from one paragraph to another paragraph should be smooth which carries on the overall
> narrative of the story forward."
>
> "The hook para is missing."

## Why this is structural, not a one-off

[[2026-05-27-story-over-report]] already taught the brain "story over report" — build an arc, slow
at human moments, show the cost. The v2 rewrite did all of that, beat by beat, and Sonal *still*
called it fragmented. That's the signal: an arc made of well-told beats is not yet a story if the
beats don't visibly serve **one idea**. The fix isn't more craft per paragraph — it's a throughline
that the hook states and the close answers, with every transition in between explicitly carrying it
forward. This generalizes past this one portrait to every narrative piece the brain drafts.

Two of Sonal's flags are also a fact-grounding problem, not a voice problem: a dramatized image
("The room watched the room") and a dramatized causal beat ("He turned around and never paid those
fees") that the source doesn't actually support. "Story over report" pushed the first draft to add
texture — but texture invented to fill a gap is worse than texture left out. The source
([[../wiki/sources/interview-masthanaiah-2026-04-20]]) is the only ground truth; anything vivid that
isn't traceable to it has to be cut or rewritten to what the source actually says, however duller
that is.

## The four additions to "story over report" (binding for narrative pieces)

1. **Name the throughline before you draft, then write the hook to state it.** Every portrait /
   coffee-book story / long blog needs one sentence the whole piece is *about* — not "his career,"
   but the specific claim the career proves (e.g., "a system changed because the person it nearly
   failed refused to let it fail anyone else"). The hook paragraph states that claim up front, in
   the brain's own voice, before the backstory starts. The close then answers it. If you can't
   write that one sentence before drafting, the piece will read as a list no matter how well each
   item is told.
2. **Every paragraph break must carry the throughline forward, not just the chronology.** Replace
   neutral chapter-markers ("Then began the years inside...", "Then, in 1996, he did the thing his
   name is still spoken for...") with sentences that say *why this chapter is the next expression of
   the same idea* ("That same instinct... travelled with him to Hyderabad" / "Three years later, he
   took on something larger still"). A transition that would work for any leader's biography is not
   doing its job — it should only fit *this* throughline.
3. **Diplomatic register in connective tissue, not just human moments.** "Story over report" said
   to slow at human moments; it didn't say how to narrate institutional friction. Default to
   measured, motive-explaining language over combative staging: "Teacher groups pushed back, he
   held the line" reads like a fight; "Teachers' associations resisted the change. He stayed with
   it, because he believed the children were owed the whole day" keeps the cost and explains the
   *why* without casting anyone as an antagonist. Apply the same lens Sonal already gave for "the
   Fest asked them" → "the Fest encouraged them": prefer language that explains motive over
   language that stages conflict, even when describing real friction.
4. **Cross-check every vivid beat against the source before it ships.** If a sentence sounds *too*
   good — a clean image, a clean turn, a clean irony — that's exactly the sentence to re-read
   against the transcript. "The room watched the room" was invented to land a beat; the transcript
   doesn't support it, and it doesn't even parse. "He turned around and never paid those fees"
   dramatizes a moment the transcript records quite differently (a B.Ed admission learned of
   mid-walk, a separate teacher selection in his MSc first year). When the source is genuinely
   ambiguous, write only the part that's clearly supported — duller and true beats vivid and
   invented, every time.

## What changed (landed same-session)

- `projects/portraits/page.md` § Masthanaiah portrait — full v3 rewrite: added the hook paragraph,
  rewired every chapter transition to carry one stated throughline, replaced "The room watched the
  room" with a grounded description, replaced "He turned around and never paid those fees" with the
  source-supported "He chose the post over finishing the degree," resolved the "room with a room"
  duplication by turning it into a deliberate echo, and softened combative connective phrasing
  ("held the line," "the press came for him," "muttering his surname like a warning") into
  motive-explaining diplomatic language. New status note: `v3 — recompiled 2026-06-08`.
- `projects/portraits/chatlog.md` — feedback session appended.
- `wiki/voice/styleguide.md` § Story over report — the pending 2026-05-27 snippet is pasted in
  (it had been sitting as `pending-maintainer-hand-edit` though `wiki/voice/**` carries no
  Write/Edit gate — see correction below), with this learning's four additions appended directly
  beneath it as binding extensions.

## Correction to a prior learning

[[2026-05-27-story-over-report]] recorded `promoted: pending-maintainer-hand-edit` with the note
"`wiki/voice/**` is Write/Edit deny-listed per CLAUDE.md rule 8." Checking `.claude/settings.json`
directly: only `docs/**` carries a deny rule; `wiki/voice/**` is fully writable
(`shikshalokam-feedback` SKILL.md confirms — "including `wiki/voice/**`, it's the team's own voice;
no gate"). That belief sat un-actioned for twelve days. Corrected here, and the snippet is pasted
in this same session — per the rule itself: don't defer a clear structural fix to "later."

## Related

- [[2026-05-27-story-over-report]] — predecessor rule this one extends (arc, human moments,
  em-dashes, cost, gaps-section)
- [[2026-05-26-movement-frame-people-actors]] — the "Fest asked them" → "Fest encouraged them"
  precedent this learning's diplomatic-register rule generalizes from
