---
name: shikshalokam-ingest
description: Absorb content someone drops into the brain — pasted text, PDFs, URLs, voice notes — so it makes the brain smarter right away. Triggers when someone attaches a file, pastes substantial prose, shares a URL, or says "here's stuff I found" / "remember this" / "add to brain". Captures it raw AND files it into typed, sourced wiki/ memory in the same session (no approval queue).
---

# shikshalokam-ingest

Good content should make the brain smarter immediately — not sit in a queue waiting for a weekly
pass. When someone drops something worth keeping, capture it faithfully and integrate it into the
brain's structured memory in the same session.

## When this fires
- Someone pastes ≥200 chars of prose, attaches a file, shares a URL, or says "here's stuff," "remember
  this," "add this," "found this for the brain."
- Not for draft-feedback ("this isn't my voice" → `shikshalokam-feedback`) or content requests
  ("draft me…" → `shikshalokam-write`).

## What it does
1. **Capture faithfully.** Append the raw drop to `raw/<YYYY-MM-DD>.md` under a
   `## <timestamp> — <label>` block (append-only; never edit prior entries). This is the unaltered
   record of what came in.
2. **Absorb into typed memory, this session** (when `brain.yml: absorb_content: in-session`, the
   default). Reconcile the drop into the right `wiki/` layer — `sources/` (a faithful extract of an
   external thing), `entities/` (a person/program/partner), `concepts/` (an idea), `synthesis/`
   (a cross-cutting angle). Each new/updated file:
   - carries the full frontmatter contract (`type`, `title|name`, `sources`, `created`, `updated`,
     and a valid `_status`),
   - cites where it came from (the raw drop and/or the URL) — never an unsourced claim,
   - **integrates, doesn't overwrite**: add to what's there; if it contradicts an existing
     user-validated fact, note both and flag the conflict rather than silently replacing it.
   Set `_status: user-validated` when a teammate is vouching for the content; `research-seeded` when
   it's reference material pulled in for later confirmation.
3. **Reply like a colleague.** Plain language: "Got it — I've added Khushboo's note on X to what we
   know about leadership, and kept the original. Ask me to use it anytime." Mention the file only if
   they'd find it useful; never make them think about paths.
4. The session digest (`sessions/<date>-<person>.md`) records what was absorbed.

## What it must not do
- Don't silently overwrite or corrupt existing knowledge. Integrate; flag contradictions.
- Don't file an unsourced or untyped entry — structure is always enforced (lint checks frontmatter +
  `_status` + wikilinks), so "absorb freely" never becomes "corrupt freely."
- Don't pull from sibling brains (`cross_brain_wall: true`).
- Don't ration or truncate to save tokens — capture and absorb fully.
