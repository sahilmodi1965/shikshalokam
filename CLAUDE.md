# CLAUDE.md — ShikshaLokam brain

Read [`INTENT.md`](./INTENT.md) first (who this brain serves, roles, immutable principles). Then [`ARCHITECTURE.md`](./ARCHITECTURE.md) (how the brain organises state, sessions, and learnings). This file does not duplicate either — it names cadence and operating reminders.

## Cadence

- **Daily** — Komal drops content and runs Claude Code sessions for output. $20 plan economics: keep sessions focused; defer heavy ops to maintainer accounts.
- **Weekly internal review** — maintainers + user. What got built, what felt rough, what changed in the brain.
- **Month-end demo** — to stakeholders per the signed Scope of Work (May–September 2026).

## Per-session workflow

Every session follows the same shape:

1. **Start** — read `INTENT.md` and `ARCHITECTURE.md` once. Read `state/` files lazily — only the ones touching what Komal asked.
2. **During** — never edit `state/` directly. State-shaping feedback ("this isn't quite right") gets captured in `learnings/<YYYY-MM-DD>-<topic>.md` for the next weekly review to promote.
3. **End** — write `sessions/<YYYY-MM-DD>-<short-handle>.md`: what was asked, what was produced, what felt rough, what the user pushed back on. Even short — the entry is the proof the session happened. The `SessionEnd` hook in `.claude/settings.json` auto-commits the working tree.

If the session leaves no `sessions/` entry, INTENT principle 2 was violated: the brain didn't compound.

## Operating reminders

When in doubt, apply INTENT.md principle 1: stop, name what you see, ask. Especially before:

- Restructuring directories or moving files
- Introducing new conventions, templates, or scaffolding
- Building features that weren't asked for
- Treating a one-off correction as a structural change (or vice versa)

Heavy ops — research seeds, indexing, refactors, repurposing — run on maintainer accounts (Sahil $200, Sahid $20). User sessions stay light so the $20 plan stretches.
