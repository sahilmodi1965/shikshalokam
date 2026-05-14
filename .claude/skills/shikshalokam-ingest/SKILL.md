---
name: shikshalokam-ingest
description: Capture content the daily user drops into the brain — pasted text, PDFs, URLs, voice notes — into raw/<date>.md. Triggers when the user attaches a file, pastes substantial prose, shares a URL, or says "here's stuff I found" / "remember this" / "add to brain". Always followed by a LEDGER entry. Never compiles to wiki/ directly (that's the compile-step's job, deferred or active per brain.yml).
---

# shikshalokam-ingest

## When this fires
- User pastes ≥200 chars of prose, OR attaches a file, OR shares a URL, OR says explicit ingestion words ("here's stuff," "remember this," "add this," "found this for the brain").
- Does NOT fire on short conversational messages or on draft-feedback (those route to `shikshalokam-write` or `shikshalokam-feedback`).

## What it does
1. **Append-only write to `raw/<YYYY-MM-DD>.md`.** Today's daily log file. Create if absent. Append with a `## <ISO timestamp> — <one-line label>` block followed by the captured content. Never edit prior entries in the file.
2. **Briefly acknowledge in chat.** If `brain.yml: chat_shield: true`, say something like *"Got it — added to today's notes. I'll work it in when you ask."* No file paths, no "I wrote to raw/." If `chat_shield: false`, you can mention: *"Added to today's raw log. Will fold into the wiki on the next pass."*
3. **Note for the LEDGER entry** at session end: the ingest counts toward today's LEDGER `Asked` summary OR is its own one-line entry if no other ask happened.

## What it reads
- The user's message and any attached content.
- `raw/<YYYY-MM-DD>.md` (only if it exists, only to find append point).
- Nothing from `wiki/`. Ingestion is fast and unidirectional.

## What it must not do
- Do not write to `wiki/**.md`. Compile-step does that.
- Do not summarise or re-format the dropped content. Capture faithfully.
- Do not read other `raw/` files (only today's, only for append).
- Do not exceed 8,000 tokens of total prompt assembly (per `TOKEN_BUDGET.md`).

## Output format
- If `chat_shield: true`: natural human reply, no technical language.
- If `chat_shield: false`: short reply naming the file appended to (one line) and any heads-up on what compile-step will do with it.
