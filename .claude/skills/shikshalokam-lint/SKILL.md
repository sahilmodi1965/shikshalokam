---
name: shikshalokam-lint
description: Enforce the brain's invariants — frontmatter contracts, _status field + transitions, LEDGER append-only, wikilink integrity, no orphans, no glob, TOKEN_BUDGET caps, voice-untouched-by-compile. Triggers pre-commit AND on every brain-write/brain-feedback invocation. Fails commits that violate. The parser-checkable backbone — without this skill, discipline degrades to vibes.
---

# shikshalokam-lint

## When this fires
- Pre-commit (every commit must pass).
- On every `shikshalokam-write` and `shikshalokam-feedback` invocation (catches issues before they hit a commit).
- Manually: user can ask "lint the brain" or "check the brain" and this fires.

## What it checks

### Frontmatter contract (per `AGENTS.md §2`)
- Every `wiki/**.md` carries: `type`, `title|name`, `sources`, `corrected_by`, `created`, `updated`, `_status:`.
- `type` matches the directory (`sources/` → `type: source`, etc.).
- `wiki/sources/*.md` has `sources: []` (sources cite nothing further).
- Other files have at least one `[[source-slug]]` in `sources:`.

### `_status:` rules (per `AGENTS.md §4`)
- `_status:` present and one of `research-seeded | user-validated | stale`.
- Monotonic transitions only. Lint checks `git log -p` on the file for the previous `_status:` and rejects illegal moves:
  - `user-validated → research-seeded` FAIL
  - `stale → research-seeded` FAIL
  - `stale → user-validated` requires a `learnings/` slug in the commit message
  - `research-seeded → user-validated` requires either a `learnings/` slug OR a `LEDGER.md` reference in the same commit

### `LEDGER.md` append-only + presence
- Diff against `LEDGER.md`: only additions allowed, no edits to existing entries, no deletions, no re-ordering of older entries.
- New session commits MUST include a new top-section entry dated today (UTC). If missing, fail.
- Format: `## YYYY-MM-DD HH:MM UTC — <user> — <slug>` + the 5–8 line body per `LEDGER.md` itself.

### Wikilink integrity
- Every `[[slug]]` resolves to an existing `wiki/**.md` file.
- No file links to itself.
- Every non-`sources/` file is reachable from `wiki/index.md` via at least one wikilink chain (no orphans).

### TOKEN_BUDGET caps (per `TOKEN_BUDGET.md`)
- `wiki/index.md` ≤ 1,500 tokens.
- `wiki/_index/topic-summaries.md` ≤ 1,500 tokens.
- Combined skill metadata across all 7 SKILL.md ≤ 1,000 tokens. (7th skill `shikshalokam-research` added 2026-05-21; combined metadata measured ~700 tokens — within cap.)

### Voice + structural file protection
- Compile-step commits (`tools/compile.py` author, or commits authored by the compile agent) must not touch `wiki/voice/**`, `INTENT.md`, `CLAUDE.md`, `ARCHITECTURE.md`, `AGENTS.md`, `TOKEN_BUDGET.md`, `brain.yml`, `LEDGER.md` (except via the append protocol).
- `wiki/voice/**` commits must cite a `learnings/<slug>` in the commit message.

### Cross-brain wall (`brain.yml: cross_brain_wall: true`)
- No Read targets outside `$CLAUDE_PROJECT_DIR`. (Caught at permission layer too, but lint flags any attempt logged in session traces.)

### No-glob rule
- Static check: no SKILL.md may contain `Glob(wiki/**/*.md)` patterns.

## What it does on failure
- Pre-commit: exits non-zero with a numbered list of violations + the file:line for each. Commit blocked.
- Mid-session (during write/feedback): surfaces violations inline so Claude can fix before continuing.
- For `chat_shield: true` brains: lint failures surface to the user as *"Hmm, something's off with how I'm organising today's notes — I'll flag it so it gets fixed."* The detailed report still lands in the commit-block.

## What it must not do
- Do not write outside `learnings/<>.md` (and only when surfacing its own gaps for review).
- Do not exceed 3,000 tokens total prompt assembly.
- Do not modify the files it lints.

## Output format
```
LINT — ShikshaLokam brain — YYYY-MM-DD HH:MM UTC
  ✓ frontmatter contract — 47 files checked, 47 pass
  ✓ _status transitions — 3 transitions in commit, all legal
  ✗ LEDGER.md — no entry dated 2026-05-14 (today) found in head
  ✓ wikilink integrity — 152 links checked
  ✓ token budgets — all within caps
  ✗ orphans — wiki/concepts/example.md unreachable from index

2 violations. Commit blocked.
```
