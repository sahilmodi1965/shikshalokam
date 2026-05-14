---
name: shikshalokam-query
description: Read-only Q&A over the brain's wiki/. Triggers on "what do you know about X" / "what have we said about Y" / "remind me about Z". Returns answer + wikilink citations to wiki/sources/. Never writes. Honours _status — surfaces "research-seeded" caveats when relevant. Falls back honestly with "_status: not-in-brain" when the topic isn't covered.
---

# shikshalokam-query

## When this fires
- User asks a knowledge question framed as recall ("what do you know," "what have we said," "remind me," "what's our position on").
- Does NOT fire on draft requests (→ `shikshalokam-write`) or correction signals (→ `shikshalokam-feedback`).

## What it reads
- `wiki/index.md` (already auto-injected at SessionStart).
- `wiki/_index/topic-summaries.md` (already auto-injected).
- Drill into up to **4 specific `wiki/**.md` files** via wikilink match against the user's question. Index-first; never `Glob wiki/**/*.md`.
- Never reads `wiki/voice/**`.

## What it does
1. **Match the question to wikilinks in the index.** If no match, do NOT guess — return "_status: not-in-brain" honestly.
2. **Drill into up to 4 files** that the index points to.
3. **Synthesise an answer** that cites: (a) each wiki file by name, (b) the `[[source]]` wikilinks within those files.
4. **Surface `_status:` caveats.** If the matched files are mostly `research-seeded`, prepend: *"Heads up — most of what I have on this is research-seeded, not yet validated by you. Treat as starting context."*
5. **Honour `chat_shield`:**
   - `true`: Phrase citations as *"this comes from the program notes you confirmed in March"* — no file paths.
   - `false`: Cite directly: *"per `wiki/concepts/shiksha-chaupals.md`, last validated 2026-05-10"*.

## What it must not do
- Do not write anywhere.
- Do not exceed 6,000 tokens total prompt assembly.
- Do not invent claims. If the brain doesn't cover it, say so explicitly — *"That's not in the brain yet. Want me to flag it as a topic to add?"* — and offer to route to `shikshalokam-feedback` if the user wants the gap captured.
- Do not read `wiki/voice/**` (that's `shikshalokam-write`'s budget).

## Output format
- Concise answer (≤300 words).
- Citations at the end: `Sources: [[s1]] (research-seeded) · [[s2]] (user-validated) · [[s3]] (user-validated)`.
- If `not-in-brain`: state it directly and offer the gap-capture next step.
