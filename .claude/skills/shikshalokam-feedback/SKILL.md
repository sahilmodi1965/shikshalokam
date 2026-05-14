---
name: shikshalokam-feedback
description: Capture daily-user corrections — "this isn't right" / "not my voice" / "too corporate" / "wrong angle" / "feels off" — into learnings/<date>-<topic>.md. Decides one-off vs structural per INTENT principle 6. Never edits wiki/ directly. The weekly-reviewer promotes structural learnings; one-offs stay as record. Routes silently when chat_shield: true.
---

# shikshalokam-feedback

## When this fires
- User expresses dissatisfaction with the brain's output: "this isn't quite right," "not my voice," "too corporate," "wrong angle," "stiff," "meh," "try again," "feels like a stranger wrote this," "ugh no."
- ALSO fires on positive but qualified signals: "the second paragraph works but the rest needs rework" — that's a structural signal.
- Does NOT fire on user requests for a different draft entirely ("give me a shorter version") — that's a `shikshalokam-write` re-invocation.

## What it does
1. **Capture verbatim** what the user said. Field 1 of the learnings entry is the user's actual words (or very close paraphrase). "User pushed back" is insufficient — quote them.
2. **Decide one-off vs structural** per INTENT principle 6:
   - **One-off** = a specific phrase/sentence/example that needs fixing in this draft only. The voice rule was correctly applied; this is a creative miss.
   - **Structural** = the brain's understanding of voice / mission / audience / a concept is wrong. Fixing this draft is not enough; the relevant `wiki/**.md` file needs editing.
   - **When in doubt, ask the user.** *"Should I just fix this draft, or does this point to something in the brain that's set up wrong?"* Their answer drives the routing.
3. **Write `learnings/<YYYY-MM-DD>-<topic>.md`.** Format:
   ```
   ---
   user_words: |
     <verbatim or close paraphrase>
   classification: one-off | structural
   target_files: [wiki/voice/styleguide.md, wiki/concepts/x.md]   # filled if structural
   suggested_change: |
     <plain-English description of what should change in target files>
   promoted: false                                                # weekly-reviewer flips to true after promotion
   promoted_at: null
   promoted_commit: null
   created: YYYY-MM-DD
   ---

   ## Context
   <what was being drafted / asked when correction surfaced>

   ## Promotion path
   <what the weekly-reviewer should do; concrete steps>
   ```
4. **Apply the one-off fix in chat NOW** if classification is one-off. If structural, regenerate the draft applying the user's correction inline AND note in the chat reply that the structural pattern was captured.
5. **`chat_shield: true` behaviour:** never mention the file written. Say *"I'll flag this — next time you ask about this, it'll be sharper."* Then carry on.
6. **LEDGER entry** records the learning slug, classification, target files (if structural).

## What it must not do
- Do not edit `wiki/**.md` directly. The weekly-reviewer promotes; mid-session writes break the integration discipline.
- Do not write to `wiki/voice/**`. Voice changes go through weekly review or maintainer commits, always with the learnings slug cited.
- Do not exceed 4,000 tokens total prompt assembly.

## Output format
- Inline draft fix (if one-off) OR regenerated draft with structural-correction noted (if structural).
- If `chat_shield: true`: human reply only, no slugs.
- If `chat_shield: false`: brief note: *"Captured to `learnings/2026-05-14-chaupal-moment.md`. Friday review will fold this in."*
