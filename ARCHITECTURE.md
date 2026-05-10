# ARCHITECTURE — ShikshaLokam brain

This brain organises three things: **state**, **session**, and **learning**.

## `state/`

What the brain knows about ShikshaLokam. Long-running. Updated by user-validated corrections, never silently overwritten. Read by every session as context.

Initial files (may grow):

- `mission.md` — what the org exists for, scope, theory of change
- `voice.md` — how this org sounds (tone, register, recurring phrases, what it avoids), with quoted samples + source URLs
- `audience.md` — who the content speaks to (segments, intent, sensitivities)
- `programs.md` — current initiatives, status, framing
- `ecosystem.md` — partners, funders, peers, where this org sits in the wider field
- `leadership.md` — who runs the org, public roles, public posture
- `SOURCES.md` — running index of every source consulted, with last-fetched date

Each state file declares its current `_status:_` at the top:

- `research-seeded — awaiting user validation` — initial; treat as provisional
- `user-validated` — user has confirmed or corrected; treat as authoritative
- `stale — needs revisit` — flagged downstream; queued for next maintainer pass

## `sessions/`

Per-session log. Written at session end by Claude Code. Format: `YYYY-MM-DD-<short-handle>.md`. Each entry: what was dropped or asked, what was produced, what felt rough, anything the user pushed back on.

Sessions are append-only history. State-changing feedback within a session creates a corresponding `learnings/` entry rather than mutating state silently.

This folder is created on first session — not pre-stubbed.

## `learnings/`

Bridge between session feedback and state.

Each learning entry: `YYYY-MM-DD-<topic>.md`. Contents:

1. What the user said (verbatim or close)
2. Whether this is one-off or structural (per INTENT principle 6)
3. If structural: which state file changed, what the change was, link to commit
4. If one-off: noted, but no state change

This folder is created on first learning — not pre-stubbed.

## Lifecycles

- **Daily user session** — reads `state/` for context, writes a `sessions/` entry at end. Never edits state directly.
- **Maintainer / weekly review** — promotes session feedback into a `learnings/` entry, which then triggers a state file edit. Commit message references the learning entry.
- Research-seeded state becomes `user-validated` only when explicitly confirmed by Komal (or a maintainer recording her confirmation).

## Why this shape

The brain has three temporal modes:

- **State** — what's always true (until corrected). Read first.
- **Sessions** — what happened. Append-only, never rewritten.
- **Learnings** — how state changes. Audit trail of how the brain got smarter.

Without this separation, sessions silently mutate "the brain" (violating INTENT principle 4), feedback gets lost (violating principle 6), or the brain loses provenance (violating principle 1).
