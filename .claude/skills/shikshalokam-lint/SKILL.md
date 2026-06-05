---
name: shikshalokam-lint
description: Enforce the brain's STRUCTURE so "absorb freely" never becomes "corrupt freely" — frontmatter contract, valid _status, wikilink integrity, no orphans, no glob. Runs on demand ("lint the brain") and as a quick self-check during write/ingest/feedback. Structure only; it never rations content and has no token caps.
---

# shikshalokam-lint

The backbone that lets the brain absorb content freely without corrupting itself. It checks that
every piece of knowledge is **well-formed and sourced** — never that there's "too much" of it. There
are no token budgets here; quality and fullness are the point.

## When this fires
- On demand: "lint the brain" / "check the brain."
- As a fast self-check while writing, ingesting, or applying feedback — so a malformed entry is
  caught before it's committed.

## What it checks (structure, not scarcity)

### Frontmatter contract
- Every `wiki/**.md` carries: `type`, `title|name`, `sources`, `corrected_by`, `created`, `updated`,
  `_status`.
- `type` matches the directory (`sources/` → `source`, `entities/` → `entity`, etc.).
- `wiki/sources/*.md` has `sources: []` (a source cites nothing further); every other file cites at
  least one `[[slug]]` — nothing enters the brain unsourced.

### `_status` validity
- Present and one of `research-seeded | user-validated | stale`.
- Forward moves are free (the brain absorbs in-session): `research-seeded → user-validated` whenever a
  teammate vouches for it. The only guarded move is a **downgrade** — `user-validated → research-seeded`
  or silently dropping `stale` — which must carry a `learnings/<slug>` in `corrected_by` explaining why.

### Wikilink integrity
- Every `[[slug]]` resolves to an existing `wiki/**.md` file. No file links to itself.
- Every non-`sources/` file is reachable from `wiki/index.md` (no orphans).

### Cross-brain wall (`brain.yml: cross_brain_wall: true`)
- No reads outside `$CLAUDE_PROJECT_DIR`. (Also enforced at the permission layer.)

### No-glob
- No SKILL.md globs `wiki/**/*.md` at prompt time — retrieval is index-first, drill-down on match.

### Session record present
- A session that changed the brain leaves a `sessions/<date>-<person>.md` digest (the public
  timeline + log generate from these). A change with no digest is flagged.

## On failure
- Surface a numbered list with `file:line` for each violation so it can be fixed before commit.
- Plain-language summary for the person; the detail is for whoever's fixing it.

## What it must not do
- Don't enforce token caps, plan tiers, or chat-shield behaviour — all retired.
- Don't modify the files it lints (it may write a `learnings/` note flagging its own gaps).
- Don't block on "too much content." Fullness is good; only malformed/unsourced/orphaned is a fault.

## Output format
```
LINT — ShikshaLokam brain
  ✓ frontmatter contract — 25 files checked, 25 pass
  ✓ _status — all valid; 2 forward promotions, 0 unexplained downgrades
  ✓ wikilink integrity — 60 links, 0 broken, 0 orphans
  ✗ session record — brain changed but no sessions/2026-06-05-*.md digest found
  1 issue. Fix before publishing.
```
