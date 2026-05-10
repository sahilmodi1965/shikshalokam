# ARCHITECTURE — ShikshaLokam brain

This brain organises four things: **state**, **session**, and **learning**, plus **routes** to where content lives outside the repo.

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

## `routes/`

Pointers from the brain to where content actually lives — Google Drive folders, Notion pages, public URLs. Routes are the bridge between the in-repo brain (curated, scannable) and the live workspace (dynamic, large).

Each route file:

- Names the use-case (e.g., "voice references — long-form donor pitches")
- Points to a folder URL and/or specific file URLs
- Notes what each pointer is canonical for, with last-validated date

Why routes exist: the brain can't scale by re-pasting content every session. Routes give it a curated directory of where content lives. With routes, the brain can:

- Tell the user where to look ("for that register, see your donor-pitches folder")
- Be enriched periodically — maintainer sessions read route targets and pull voice samples / program details into `state/` with citations
- Survive content churn — when files move in Drive, the route updates; `state/` files stay stable

Routes are **created during onboarding** (the brain user shares their working folders) and **maintained by maintainers** thereafter. The brain user does not edit routes directly; they request additions in weekly review.

This folder is created when the first route is added — not pre-stubbed.

## How the brain learns

The brain has multiple feedback loops, each on the right plan and at the right timing:

**Daily — brain user, $20 Pro.** Komal opens Claude Code, reads `state/` and `routes/` lazily (only what's relevant, not upfront), drops or refers to content, asks for output, gives feedback in plain English, writes a `sessions/` entry at end. Never edits `state/` directly. Token budget is protected by lazy reads, routing to Drive instead of embedding, and short scannable state files.

**Weekly review — Sahid + brain user.** Sift `sessions/` and `learnings/`. Promote session feedback into learning entries; promote learnings into state-file edits. Add new routes as the working set evolves.

**Monthly enrichment — Sahil, $200 Max.** Reads route targets (Drive folders, fresh InvokED material, partner press, public reports). Pulls voice samples and ecosystem updates into `state/` with citation. Updates `SOURCES.md`. Refactors state taxonomy if patterns emerge. Heavy reading lives here — not in user sessions.

**Month-end stakeholder demo** — per the signed SoW (May–September 2026).

**Cross-org events** (InvokED, awards, new partnerships) trigger ad-hoc enrichment passes — maintainer responsibility.

### Handoffs

- Brain user → Sahid (weekly review): "this isn't quite right" → `learnings/` entry → state edit
- Sahid → Sahil (when needed): "we should pull voice samples from the donor folder" → enrichment pass
- Maintainers → brain user: structural shifts arrive as a short brief before the next session

### Takeovers

- Sahid can run enrichment on his $20 account for urgent / small items, with explicit awareness of token cost
- Future tech-head contributors join as maintainers via explicit handover; roles expand, never collapse (per INTENT principle 3)

Research-seeded state becomes `user-validated` only when explicitly confirmed by the brain user (or a maintainer recording the confirmation in a learning).

## Why this shape

The brain has three temporal modes plus one spatial pointer:

- **State** — what's always true (until corrected). Read first.
- **Sessions** — what happened. Append-only, never rewritten.
- **Learnings** — how state changes. Audit trail of how the brain got smarter.
- **Routes** — where content lives outside the repo. Where to look, not what is.

Without this separation, sessions silently mutate "the brain" (violating INTENT principle 4), feedback gets lost (violating principle 6), or the brain loses provenance (violating principle 1). Routes prevent the brain from ballooning under content load — content stays in Drive; the brain stays curated.
