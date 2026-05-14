# ARCHITECTURE — ShikshaLokam brain

This brain organises four things: **state**, **session**, **learning**, **route** — plus the **LEDGER** as the single growing chronological surface.

## `wiki/` — state

What the brain knows about ShikshaLokam. Typed, frontmatter-contracted, `_status:`-tracked. Read by every session as context, via the index (never globbed).

### Five layers

| Layer | Path | What it holds | Body shape (fixed by `AGENTS.md`) |
|---|---|---|---|
| **sources** | `wiki/sources/<slug>.md` | One file per ingested source (PDF, URL, transcript, paste). Faithful extraction, no interpretation. | Faithful body, no synthesis. |
| **entities** | `wiki/entities/<kebab>.md` | One file per named thing (person, partner, program, audience segment). | One-line definition / Key facts (cited) / Relationships / Open questions. |
| **concepts** | `wiki/concepts/<kebab>.md` | One file per idea, framework, claim, or recurring theme. | TL;DR (≤80w) / Why it matters for ShikshaLokam / Supporting sources / Related concepts / Contradictions. |
| **synthesis** | `wiki/synthesis/<kebab>.md` | Cross-cutting angles that connect multiple concepts and entities into a reusable POV. | The angle / Evidence trail / Counter-angle / Post hooks. |
| **voice** | `wiki/voice/styleguide.md` + `wiki/voice/exemplars/` | Always/Never rules, words-we-use / words-we-avoid, supporting samples. Hand-curated. | Free-form, but each rule cites at least one exemplar. |

### Frontmatter contract (every file)

```yaml
---
type: source | entity | concept | synthesis | voice
title|name: "<canonical>"
sources: [[s1]], [[s2]]   # empty list for type: source
corrected_by: [issue-42, learnings/2026-05-12-pratik-pdf-stitched]
created: YYYY-MM-DD
updated: YYYY-MM-DD
_status: research-seeded | user-validated | stale
---
```

`brain-lint` enforces the contract at commit time. Missing fields, missing `_status:`, invalid `_status:` values, or illegal transitions fail the commit.

### Index files (auto-injected at SessionStart)

- `wiki/index.md` — master index, ≤1,500 tokens. One line per entity / concept / synthesis. Updated by compile-step (or maintainer when compile-step is `deferred`).
- `wiki/_index/topic-summaries.md` — graphrag-style community summaries, ≤1,500 tokens. Regenerated when topic clusters shift.
- `wiki/log.md` — append-only compile-step audit log. **Not the LEDGER.** This logs what the compile-step did to `wiki/`; the LEDGER logs what the daily user did with the brain.

## `LEDGER.md` — session

**The single artefact that grows over time.** See `LEDGER.md` itself for format. One entry per session. Newest at top. Append-only. Lint-enforced.

This is the **demo surface**. Stakeholders read it. Successors read it. The maintainer reads it at weekly review.

## `learnings/` — learning

Bridge between session feedback and state. Each entry: `learnings/<YYYY-MM-DD>-<topic>.md`. Created by `brain-feedback` skill OR Claude at session end when correction surfaced. Contents:

1. What the user said (verbatim or close).
2. Whether this is one-off or structural (per INTENT principle 6).
3. If structural: which `wiki/` file changed, what the change was, link to commit (filled at promotion time).
4. If one-off: noted, no state change.

Promoted to state by `brain-weekly-review` skill. A learning that never lands in a `corrected_by:` frontmatter list is by definition one-off.

## `routes/` — pointer

Pointers from the brain to where content lives outside the repo (Drive folders, Notion pages, public URLs). One file per use-case: `routes/<purpose>.md`. Each:

- Names the use-case ("voice references — long-form donor pitches").
- Points to folder URL(s) and/or specific file URL(s).
- Notes what each pointer is canonical for, with last-validated date.

**Why routes exist:** the brain can't scale by re-pasting content every session. Routes let the brain answer "for that, see your X folder" without ingesting the world. Routes are maintained by maintainers; the daily user requests additions in weekly review.

## `raw/` — input

Daily-user drops, any format. Append-only daily file: `raw/<YYYY-MM-DD>.md`. Compile-step consumes; once compiled, raw is preserved for audit but not re-read.

## `output/` — produced drafts (opt-in)

Only present if `brain.yml: output_channel != "none"`. Holds produced drafts. The LEDGER references files here.

---

## How the brain learns

Multi-loop, each on the right plan and the right cadence.

### Daily — daily user, $20 plan
Opens Claude Code, reads `wiki/index.md` + `wiki/_index/topic-summaries.md` (auto-injected, ≤3K tokens), drops or refers to content, asks for output, gives feedback. Writes one LEDGER entry at end. Never edits `wiki/**.md` directly. Token budget protected by lazy reads, routing to Drive instead of embedding, and short scannable state files.

### Weekly — Sahid + daily user, $20 plan
**`friday` 30 minutes.** Runs `brain-weekly-review` skill. Sifts `LEDGER.md` (this week's entries) and `learnings/`. Promotes session feedback into learning entries; promotes structural learnings into `wiki/**.md` edits (with `corrected_by:` references). Adds new routes as the working set evolves. Flips `_status:` for files contradicted by newer material to `stale`.

### Monthly — Sahil, $200 plan
Reads route targets (Drive folders, fresh org material, partner press, public reports). Pulls voice samples and ecosystem updates into `wiki/` with citations. Updates `wiki/sources/SOURCES.md`. Refactors `wiki/` taxonomy if patterns emerge. Heavy reading lives here — not in user sessions.

### Month-end stakeholder demo
Per the signed SoW. Daily user drives. LEDGER is part of the demo material.

### Cross-org events (multi-brain engagements)
InvokED, awards, new partnerships trigger ad-hoc enrichment passes — maintainer responsibility.

---

## Handoffs

- **Daily user → Sahid (weekly):** "this isn't quite right" surfaces in LEDGER, captured in `learnings/`, promoted to state edit if structural.
- **Sahid → Sahil (when needed):** "we should pull voice samples from the donor folder" → enrichment pass.
- **Maintainers → daily user:** structural shifts arrive as a short brief before the next session (sometimes pinned in the LEDGER as a maintainer-authored entry).

## Takeovers

- Sahid can run enrichment on his $20 account for urgent / small items, with explicit awareness of token cost.
- Future tech-head contributors join as maintainers via explicit handover; roles expand, never collapse (per INTENT principle 3).

Research-seeded state becomes `user-validated` only when explicitly confirmed by the brain user (or a maintainer recording the confirmation in a learning).

## Why this shape

The brain has four temporal modes plus one spatial pointer:

- **State** (`wiki/`) — what's always true (until corrected). Read first, via index.
- **Session** (`LEDGER.md`) — what happened, chronological. The single growing artefact. Append-only.
- **Learning** (`learnings/`) — how state changes. Audit trail of how the brain got smarter.
- **Route** (`routes/`) — where content lives outside the repo.
- **Input/output** (`raw/`, `output/`) — boundary surfaces.

Without this separation, sessions silently mutate "the brain" (violating INTENT principle 4), feedback gets lost (violating principle 6), or the brain loses provenance (violating principle 1). The `_status:` field on every `wiki/**.md` is the bridge that lets the compile-step engine run aggressively without corrupting brand fidelity — engine compiles freely from `research-seeded`, append-only over `user-validated`, never touches `stale`.
