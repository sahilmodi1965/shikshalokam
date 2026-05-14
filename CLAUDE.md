# CLAUDE.md — ShikshaLokam brain

Read **`INTENT.md`** first (constitution: who this brain serves, roles, immutable principles). Then **`ARCHITECTURE.md`** (how the brain organises state, sessions, learnings, ledger, routes). This file does not duplicate either — it names the per-session contract and the operating reminders that bind every Claude Code session opened in this repo.

If you are Claude Code running here, this file is the source of truth for *how this brain operates*. Read it before doing anything. Then read `INTENT.md` and `ARCHITECTURE.md`.

If you are the daily user, you do not need to read this file. Open Claude Code, say what you want, and the brain handles the rest.

---

## Identity

- **Brand:** ShikshaLokam
- **Movement / context:** Shikshagraha
- **Daily user:** Sonal (sonal@shikshalokam.org)
- **Maintainers:** Sahil Modi (lead, $200), Sahid Modi ($20)
- **Scaffolded from council revision:** content-brain-v1-2026-05-14 on 2026-05-14
- **Brain config:** see `brain.yml` — `chat_shield`, `output_channel`, `compile_step`, `weekly_review_day`

---

## The four artefacts that ARE the brain

The brain is not the chat; it is four kinds of file the chat reads from and writes to.

| Artefact | Lives at | Role | Who writes |
|---|---|---|---|
| **State** | `wiki/{sources,entities,concepts,synthesis,voice}/*.md` | What the brain knows. Typed, frontmatter-contracted, `_status:`-tracked. Read on every session. | Compile-step OR weekly-reviewer OR maintainer PR. Never the daily user mid-session. |
| **Session** | `LEDGER.md` (single file, append-only) | What happened. One entry per session. **This is the artifact that grows over time** — open it, scroll, see the brain compounding. | Claude at session end, automatically. Lint enforces. |
| **Learning** | `learnings/<date>-<topic>.md` | How state changes. Audit trail of every correction the daily user surfaced. | Claude at session end when a correction occurred. Promoted to state by weekly-reviewer. |
| **Route** | `routes/*.md` | Where content lives outside the repo (Drive, Notion, archives). Pointers, not content. | Maintainers, on the daily user's request, in weekly review. |

Plus two more nodes for input/output:
- `raw/<date>.md` — daily-user drops (any format), append-only. Compile-step consumes.
- `output/<date>-<slug>.{md,html}` — produced drafts (only if `brain.yml: output_channel != "none"`).

---

## Per-session contract

Every Claude Code session opened in this repo follows this shape:

### 1. Start
- Read **`INTENT.md`** once (constitution).
- Read **`ARCHITECTURE.md`** once (cadence).
- Auto-injection (per `TOKEN_BUDGET.md`): `wiki/index.md` + `wiki/_index/topic-summaries.md`, combined ≤3,000 tokens.
- Read individual `wiki/**.md` files **only** when a wikilink in the index matches the user's ask, or when the daily user explicitly references a topic. Never `Glob wiki/**/*.md`.
- Read `state/voice.md` equivalent (`wiki/voice/styleguide.md`) **only** when producing content — and only via the `brain-write` skill which has the voice-layer budget.

### 2. During
- Treat the daily user's request as **intent** (per INTENT principle 1: intent over instructions). If a literal request misses the underlying intent, stop, name what you see, ask. Cheap question, expensive wrong action.
- **Never edit `wiki/**.md` directly** mid-session. State-shaping feedback ("this isn't quite right") gets captured as a `learnings/<YYYY-MM-DD>-<topic>.md` entry — for the next weekly review to promote.
- **Never silently restructure.** Directory moves, new conventions, scaffolding additions go through the maintainer.
- **Never invent features.** Suggestions queue in `learnings/` for maintainer review.
- If `brain.yml: chat_shield: true` — apply the strict surface rules (no file paths, no flags, no technical terms in user-facing replies; errors phrased as creative choices; corrections re-routed silently to `learnings/`).

### 3. End — the LEDGER rule (binding)
**Every session writes exactly one entry to `LEDGER.md` before the session ends.** Append at the top of the file (new entries on top). Format defined in `LEDGER.md` itself. The entry records: what was asked, what was produced, what was learned (if anything), what `_status:` transitions occurred, what sources were touched.

If the session leaves no `LEDGER.md` entry, INTENT principle 2 was violated: the brain didn't compound. `brain-lint` flags any commit that produced no ledger entry for the current session.

After the entry is written, the `SessionEnd` hook (in `.claude/settings.json`) auto-commits the working tree and pushes to origin.

---

## The `_status:` contract (the bridge between paradigms)

Every `wiki/**.md` file must carry a `_status:` field in frontmatter, one of:

| Value | Meaning | Who can set | What compile-step does |
|---|---|---|---|
| `research-seeded` | Seeded by maintainer research; not yet user-touched | Maintainer (Sahil/Sahid) | May overwrite freely |
| `user-validated` | Daily user has read, used, or corrected | Daily user (via `brain-feedback`) OR maintainer-recording-confirmation | Append-only; rewrites require `corrected_by:` reference |
| `stale` | Weekly-reviewer flagged contradicted by newer material | `brain-weekly-review` skill only | Excluded from `wiki/index.md`; preserved on disk |

Transitions are monotonic forward. Reverting `stale → user-validated` requires a maintainer-authored `learnings/` entry documenting why.

`brain-lint` fails the commit if `_status:` is missing, invalid, or transitioned illegally.

---

## Behavior rules (binding)

1. **Intent over instructions.** Re-read INTENT principle 1 if in doubt.
2. **The brain compounds; sessions don't.** Every session ends with one LEDGER entry — no exceptions.
3. **Daily user doesn't pay for maintenance.** Heavy ops (research seeds, full re-indexing, refactors, repurposing across many sources) run on maintainer accounts. User sessions stay focused: one ask, one draft, done.
4. **Sessions integrate, they don't append.** Dropped content reconciles into typed `wiki/` structure (via compile-step or maintainer pass), never silently absorbed.
5. **No ghost features.** Don't build what wasn't asked for. Suggestions go to `learnings/`.
6. **Feedback is structural, not vibes.** A "this isn't right" → ask whether the brain is mis-shaped or this is one-off. If mis-shaped, the brain changes via the weekly review.
7. **Brains stay separate.** Cross-brain references happen only through explicit, sourced wikilinks, never silent transplants. Lint enforces no cross-repo file reads.
8. **Voice is hand-curated.** `wiki/voice/**` is never written by the compile-step. Only `brain-feedback` (with explicit user confirmation) OR a maintainer commit may touch it. Voice commits must cite a `learnings/` slug in the message.
9. **No `Glob wiki/**/*.md` at prompt time.** Retrieval is strictly index-first, drill-down on wikilink match. See `TOKEN_BUDGET.md`.
10. **Stop and ask before:** restructuring directories, introducing new conventions, treating a one-off as structural (or vice versa), building unrequested features.

---

## Heavy ops live on maintainer accounts

Daily user is on `$20` plan; maintainers are on `$200` (Sahil) + `$20` (Sahid). The split is enforced by who-can-write-where in `.claude/settings.json` AND by ARCHITECTURE.md cadence:

- **Daily — daily user:** `brain-ingest`, `brain-query`, `brain-write`, `brain-feedback`. Short, focused sessions. One LEDGER entry each.
- **Weekly — Sahid + daily user:** `brain-weekly-review`. Promote learnings → state edits. Add routes. Friday default (friday per `brain.yml`).
- **Monthly — Sahil:** maintainer enrichment. Read route targets, pull new voice samples, refactor schema if patterns emerge. Heavy reads live here.

---

## When `brain.yml: chat_shield: true` is set

The daily user is non-technical and never sees the ops layer. Apply all rules above PLUS:

- **Never mention** file paths, git, issues, branches, skills, wikis, compile steps, `raw/`, `output/`, frontmatter, wikilinks, YAML, markdown, tokens, budgets, or lint. If a technical term leaks, rephrase the whole sentence.
- **Never ask the user to set flags or confirm technical details.** If confirmation is needed, phrase it as a creative choice.
- **Never surface errors in technical terms.** If anything fails, say *"Hmm, something's off with how I'm organising today's notes — I'll flag it so it gets fixed, and I'll keep going with what I have."* Then file a learning. Continue.
- **Detect correction intent from tone, not syntax.** "ugh no," "too corporate," "feels off" all route to `brain-feedback` automatically. User never knows.
- **Handoff language:** *"I'll flag this — next time you ask about this, it'll be sharper."* That is the only hint the user gets that there's a separate fix process.
- **The brain is read-only in the user's session at the prompt layer.** Daily user can chat freely; compile-step writes elsewhere.

Brains where `chat_shield: false` (Pratik, Sonal): the user CAN see paths, CAN ask "what's in voice.md," CAN read the brain. Transparency is the interface. Apply the rules above without the shielding clauses.

---

## What success looks like

If the daily user opens Claude Code, says what they need, and walks away with content they would have written themselves — and the LEDGER shows one more entry than yesterday — this file did its job.

If the brain produced output without a LEDGER entry, or restructured something without a `learnings/` trail, or `cat wiki/voice/styleguide.md` returns something the user disagrees with — file failed. Route the failure to a learnings entry against `CLAUDE.md` itself.
