# ShikshaLokam brain

The ShikshaLokam content brain. Holds the voice, mission, audience, programs, ecosystem, leadership, and sources of ShikshaLokam in a typed, provenance-tracked wiki. Produces review-ready content from a one-line prompt. Learns from corrections through a weekly review ritual.

## Who this is for

- **Sonal Bhasin** — daily user. Drops content, asks for drafts, gives feedback. Does not restructure.
- **Maintainers (Sahil Modi (lead, $200), Sahid Modi ($20))** — shape the brain, run heavy ops on their accounts, hold the Friday review ritual.

## Open Claude Code here and just talk

```bash
cd ~/shikshalokam && claude
```

Then say what you need:
- *"Draft a 250-word post on [topic]."*
- *"What do we know about [partner / program / topic]?"*
- *"Here's a PDF I want to remember — [paste / attach]."*
- *"This doesn't sound like me — [say what's wrong]."*

The brain handles the rest.

## What's inside (for the curious)

- **`LEDGER.md`** — the single growing artefact. Every chat leaves one entry. Scroll to see the brain compounding.
- **`wiki/`** — what the brain knows. Voice, mission, audience, programs, sources, etc.
- **`INTENT.md`** — the brain's constitution. Read this if you want to understand how it operates.
- **`learnings/`** — every "this isn't quite right" the user surfaced. Reviewed Fridays.
- **`routes/`** — pointers to content that lives in Drive / Notion / elsewhere.

You don't need to read any of these to use the brain. They exist so the brain (and a successor) can audit what was learned and why.

## Weekly rhythm

- **Daily** — short Claude Code sessions, focused output.
- **Fridays** — 30-min review with a maintainer. Sift learnings, promote to state, add routes.
- **Month-end** — stakeholder demo per the engagement's SoW.

## Status

Scaffolded from `council/templates/domains/content-brain/` revision content-brain-v1-2026-05-14 on 2026-05-14.

For operational rules see `CLAUDE.md` (Claude Code's source of truth). For architecture see `ARCHITECTURE.md`. For the constitution see `INTENT.md`.
