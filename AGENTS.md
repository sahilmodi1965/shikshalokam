# AGENTS.md — ShikshaLokam brain — compile-step schema

This file is the contract between the **compile-step subprocess** (when active) and the brain's `wiki/`. It is read by `brain-ingest` when ingesting, by the compile-step subprocess when compiling, and by `brain-lint` when validating.

`brain.yml: compile_step` controls activation:
- `deferred` — schema enforced, but compile-step is a no-op. `wiki/` is hand-curated by maintainer enrichment.
- `active` — compile-step subprocess runs on every `raw/` change. Writes per the schema below.

In both modes, this file is the **frontmatter and body contract** that `brain-lint` enforces for every `wiki/**.md` file, regardless of who wrote it.

---

## 1. When the compile step runs (active mode only)

- **Trigger:** immediately after any `brain-ingest` invocation that writes to `raw/<YYYY-MM-DD>.md`.
- **Gate:** the SHA-256 hash of the daily log must have changed since the last run. Unchanged logs are no-ops.
- **Runtime:** Python subprocess using the Claude Agent SDK.
- **Permissions:**
  - `permission_mode: "acceptEdits"`
  - `max_turns: 30`
  - `tools: [Read, Write, Edit, Glob, Grep]` — **no Bash**. Prompt-injection blast radius stays off the shell.
- **Inputs:**
  - `raw/<YYYY-MM-DD>.md` (today's dump)
  - `wiki/index.md` (current master index)
  - `wiki/_index/topic-summaries.md`
  - `wiki/log.md` (tail 200 lines)
  - Any existing `wiki/**.md` reachable by wikilink from the above
- **Outputs allowed:**
  - New or updated files under `wiki/{sources,entities,concepts,synthesis}/`
  - `wiki/index.md` (refreshed)
  - `wiki/_index/topic-summaries.md` (refreshed only when topic clusters shift)
  - `wiki/log.md` (append-only)
- **Outputs forbidden:**
  - `wiki/voice/**` — voice is hand-curated; only `brain-feedback` (with explicit user confirmation) or maintainer commits touch it
  - `learnings/**`, `routes/**`, `LEDGER.md`
  - `*.md` files at brain root (`INTENT.md`, `CLAUDE.md`, `ARCHITECTURE.md`, `AGENTS.md`, `TOKEN_BUDGET.md`, `brain.yml`)
  - `.claude/**`

---

## 2. The four article types

Every `wiki/{sources,entities,concepts,synthesis}/*.md` belongs to exactly one type. No new types may be introduced without a maintainer-approved overlay revision.

### 2.1 `sources/<slug>.md`

One file per ingested source. Faithful record, no interpretation.

```yaml
---
type: source
title: "<human title>"
kind: pdf | url | image | voice | note | spreadsheet
origin: <path in raw/ or URL>
ingested: YYYY-MM-DD
tags: [tag1, tag2]
sources: []                # sources always have an empty sources list
corrected_by: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
_status: research-seeded | user-validated | stale
---
```

**Body:** faithful extraction. No synthesis. No editorialising.

### 2.2 `entities/<kebab>.md`

One file per named thing.

```yaml
---
type: entity
name: "<canonical name>"
kind: person | partner | program | audience | channel | brand
aliases: ["<other names>"]
tags: []
sources: [[source-slug-1]], [[source-slug-2]]
corrected_by: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
_status: research-seeded | user-validated | stale
---
```

**Body sections (fixed order):**
1. **One-line definition** — who/what this is in ≤140 chars.
2. **Key facts** — bulleted, every bullet cites `[[source-slug]]`.
3. **Relationships** — wikilinks to other entities, each with a one-line relation description.
4. **Open questions** — bullets of what's unknown or contradictory.

### 2.3 `concepts/<kebab>.md`

One file per idea, framework, claim, or recurring theme. This is where the brain *thinks*.

```yaml
---
type: concept
title: "<canonical name>"
tags: []
sources: [[source-slug-1]]
corrected_by: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
_status: research-seeded | user-validated | stale
---
```

**Body sections (fixed order):**
1. **TL;DR** — one paragraph, ≤80 words.
2. **Why it matters for ShikshaLokam** — one paragraph tying to brand goals.
3. **Supporting sources** — bulleted wikilinks to `[[sources/...]]`.
4. **Related concepts** — wikilinks to `[[concepts/...]]`.
5. **Contradictions / open threads** — explicit list. Do not resolve silently.

### 2.4 `synthesis/<kebab>.md`

Cross-cutting POVs the `brain-write` skill preferentially reads.

```yaml
---
type: synthesis
title: "<canonical name>"
tags: []
draws_on: [[concept-a]], [[entity-b]]
sources: [[source-slug-1]]
corrected_by: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
_status: research-seeded | user-validated | stale
---
```

**Body sections:**
1. **The angle** — one paragraph.
2. **Evidence trail** — bulleted wikilinks.
3. **Counter-angle** — one paragraph.
4. **Post hooks** — 3–5 bullets of concrete openers.

---

## 3. Wikilink discipline

- Every cross-reference uses Obsidian `[[wikilinks]]`. No raw paths, no markdown links.
- Every claim in `entities/`, `concepts/`, `synthesis/` cites at least one `[[sources/...]]`. Uncited claims fail lint.
- No article links to itself.
- Orphans (files not reachable from `wiki/index.md`) fail lint.
- Broken wikilinks fail lint.

---

## 4. The `_status:` contract (the bridge)

This is the field that lets the compile-step engine and the discipline-curation paradigm coexist.

| `_status:` | Set by | Compile-step behaviour | Lint behaviour |
|---|---|---|---|
| `research-seeded` | Maintainer (during enrichment) | May rewrite freely | Required during file creation |
| `user-validated` | Daily user (via `brain-feedback`) OR maintainer recording user confirmation in `learnings/` | Append-only; rewrites require `corrected_by:` reference | Promotion from `research-seeded` requires evidence of user touch |
| `stale` | `brain-weekly-review` only | Excluded from `wiki/index.md`; preserved on disk | Reversion to `user-validated` requires maintainer `learnings/` entry citing reason |

Transitions are monotonic forward. `brain-lint` fails commits that:
- Omit `_status:`
- Set `_status:` to an undefined value
- Transition illegally (e.g. `stale → research-seeded`, `user-validated → research-seeded`)
- Set `_status: user-validated` without an accompanying `learnings/` or `LEDGER.md` reference in the commit

---

## 5. Provenance and correction traceability

Every wiki file carries:

- `sources: [[s1]], [[s2]]` — where the claims came from
- `corrected_by: [issue-42, learnings/2026-05-12-pratik-correction]` — what reshaped this file

When a feedback skill files an issue or creates a learning that touches a wiki page, and the weekly-reviewer or maintainer merges the structural fix, the commit must append the issue number or learnings slug to `corrected_by:` on every file it touches. This is how the brain stays auditable across corrections.

`wiki/index.md` carries a "Compiled From" table listing every compiled article with its source provenance, so the daily user (via `brain-query`) can always answer "where did we learn this?" without a maintainer in the loop.

The `corrected_by:` regex: `^(issue-\d+|learnings/\d{4}-\d{2}-\d{2}-[a-z0-9-]+)$`. Lint validates.

---

## 6. Compile-step log discipline (when active)

`wiki/log.md` is append-only. Every compile run appends:

```
## YYYY-MM-DDTHH:MM:SSZ
- ingest: raw/YYYY-MM-DD.md (3 new sources)
- created: entities/new-partner.md
- updated: concepts/voice-thread.md
- refreshed: index.md
- corrected_by: [learnings/2026-05-12-pratik-correction]
```

Lint fails if any edit to `wiki/log.md` is not a pure append. `wiki/log.md` is **distinct from `LEDGER.md`** — `log.md` records what the compile-step did to `wiki/`, `LEDGER.md` records what the daily user did with the brain.

---

## 7. Non-goals

- No embedding generation. No vector index. No similarity search.
- No Bash access in the compile-step.
- No writes outside `wiki/` from compile-step. The `output/` channel is owned by `brain-write`, not compile-step.
- No touching of `wiki/voice/**` from compile-step.

---

## 8. Implementation status

`brain.yml: compile_step: deferred`

- If `deferred`: the Python subprocess does not exist yet. `wiki/` is built and maintained by maintainer enrichment passes. This file is the spec that future implementation must satisfy.
- If `active`: the subprocess lives at `tools/compile.py` (created by the maintainer at activation time). The schema above is the contract it must satisfy.
