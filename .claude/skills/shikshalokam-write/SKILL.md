---
name: shikshalokam-write
description: Produce content (post, email, blurb, blog, deck, fundraising letter, caption) in ShikshaLokam's voice. Triggers on "draft me X", "write a Y about Z", "give me a LinkedIn/newsletter/email/etc." Loads the FULL voice styleguide + every matched exemplar + every relevant source — uncapped — and works like a sharp creative partner, not a vending machine. Output lands in output/ if brain.yml output_channel != "none", else in the chat reply.
---

# shikshalokam-write

The whole reason this brain exists: produce content so good the team uses it as-is — clearly
better than a blank Claude chat. Quality is the point. **Load context generously. Never ration,
cap, or degrade to save tokens** — a thinner draft is the only real failure here.

## When this fires
- The person wants a produced piece: "post," "email," "thread," "blurb," "blog," "deck,"
  "fundraising letter," "caption," "draft me…", "write…".
- Not for knowledge questions (→ `shikshalokam-query`) or pure ingestion (→ `shikshalokam-ingest`).

## What it loads — FULLY, no caps
Load all of this every time. There is no token budget to protect here; optimize cost later, never
by withholding context.
1. **The complete `wiki/voice/styleguide.md`** — the whole thing, every register and rule. (This is
   the one skill that reads the voice layer.)
2. **Every exemplar in `wiki/voice/exemplars/`** that could match the format/audience — read them in
   full, not headers. When in doubt, read it; matching voice to a real sample is the signature move.
3. **Every relevant `wiki/**` file** — drill the index + topic-summaries for anything touching the
   brief's subject, angle, people, programs, or claims, and read them in full. Sources, entities,
   concepts, synthesis — pull them all if they bear on the piece.
4. **Anything the person just dropped** this session (`raw/<date>.md`, pasted text, a link).

If the brief is **evidence-anchored** (makes a claim that should cite) and no `wiki/sources/research-*.md`
covers the angle, run **`shikshalokam-research`** first — it verifies external studies, files them,
and returns the wikilink to cite. Citing is the default; the person doesn't have to ask.

## How it behaves — a creative partner, not a form
1. **Open by thinking with them, briefly.** If the brief is rich, go straight to a draft. If it's
   thin or could go several good ways, offer **2–3 distinct angles in a line each** and ask the
   **one question that most improves the piece** (audience? the feeling it should leave? the one
   thing it must land?). One sharp question — then draft. Never interrogate.
2. **Draft at full quality.** Apply the voice in full. Match a real exemplar's shape where one fits.
   Make it specific, human, and ready to paste — not a hedged outline.
3. **Riff, don't just deliver.** Where there's a stronger hook, a tighter close, or a better structure,
   offer it as an alternative the team can take or leave. Surface the choice; let them own it.
4. **Cite real claims.** Footnote substantive/factual claims with the `wiki/sources/<slug>` behind
   them. Flag verifiability only where the brain genuinely couldn't confirm exact wording. Never
   invent a fact or a quote — if it's not in the brain, say so and offer to find it.
5. **Absorb what's good, in the moment.** If the person shares or approves strong material (a sample,
   an approved invite, a phrasing they love), integrate it into the brain's typed memory this session
   — sourced and `_status`-tracked (see the operating note) — so the next draft is sharper. Good
   content makes the brain smarter immediately; it does not sit in a queue.

## Output
- If `brain.yml: output_channel` is `github-pages`/`drive`: write `output/<date>-<slug>.md` with
  frontmatter `_status: draft`, `sources: [[…]]`, `voice_pulls: [styleguide §…, exemplar/<slug>]`,
  and reply with the draft + its path. If `none`: the draft lives in the chat reply.
- After the draft: `**Sources:** [[s1]] · [[s2]] …` · `**Voice:** matched <exemplar>, applied <rule>`
  · `**Gaps:** <anything the brain couldn't support>`.
- The session's `sessions/<date>-<person>.md` records what was produced (privacy-safe digest).

## What it must not do
- Don't ration, cap, or shorten to save tokens. Load fully.
- Don't hallucinate facts or quotes. Mark gaps; offer to research.
- Don't pull from sibling brains (`cross_brain_wall: true`).
- Don't voice-ify content the person asked to keep raw ("just the bullets").
