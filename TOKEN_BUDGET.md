# TOKEN_BUDGET — ShikshaLokam brain

Hard caps that protect `$20`-plan economics for the daily user. `brain-lint` reads this file and fails commits / skill invocations when any budget is exceeded.

All numbers in tokens, counted with the `cl100k_base` tokenizer.

---

## Session-level

| Surface | Budget | Source |
|---|---:|---|
| **SessionStart auto-injection** | **≤ 3,000** | `wiki/index.md` + `wiki/_index/topic-summaries.md` |
| `wiki/index.md` | ≤ 1,500 | — |
| `wiki/_index/topic-summaries.md` | ≤ 1,500 | — |

Nothing else loads at session start. No `CLAUDE.md` expansions, no voice layer, no individual articles. `INTENT.md` and `ARCHITECTURE.md` are read once per session by Claude (not auto-injected as system context).

---

## Skill metadata

| Surface | Budget | Notes |
|---|---:|---|
| **Skill metadata (all 6 skills combined)** | **≤ 1,000** | Frontmatter `description` only — what Claude's skill matcher sees on every turn. |
| **SKILL.md body on trigger** | **≤ 3,000 each** | Full body loads when a skill fires. Per-skill cap. |

The 6 skills are: `shikshalokam-ingest`, `-query`, `-write`, `-feedback`, `-lint`, `-weekly-review`.

---

## Voice-layer

Loaded **only** by `shikshalokam-write`. No other skill touches it.

| Surface | Budget |
|---|---:|
| **Voice layer total (on write only)** | **≤ 2,000** |
| `wiki/voice/styleguide.md` | ≤ 1,000 |
| 2 best-matched exemplars from `wiki/voice/exemplars/` | ≤ 1,000 combined |

Exemplar selection is LLM-picked via a cheap prior call against exemplar headers only (~500 tokens), not via embeddings.

---

## Prompt assembly ceilings

| Skill | Max assembled prompt |
|---|---:|
| **`shikshalokam-write`** | **≤ 12,000 tokens** |
| `shikshalokam-query` | ≤ 6,000 tokens |
| `shikshalokam-ingest` | ≤ 8,000 tokens (excluding raw payload) |
| `shikshalokam-feedback` | ≤ 4,000 tokens |
| `shikshalokam-lint` | ≤ 3,000 tokens |
| `shikshalokam-weekly-review` | ≤ 16,000 tokens (maintainer-driven, runs on $200) |

`write`'s 12K cap = `CLAUDE.md` rules + SessionStart injection + SKILL.md body + voice layer + up to 6 wiki articles drilled via wikilink + the prompt brief.

---

## Hard rules the lint skill enforces

1. **No skill may `Glob wiki/**/*.md` at prompt time.** Retrieval is strictly index-first, drill-down on wikilink match.
2. **No skill may read `wiki/voice/**`** unless it is `shikshalokam-write`.
3. **No skill may read the full `raw/` directory.** Only the specific daily-log file being processed.
4. **Per-file ceilings for index files are load-bearing.** If the compile-step would push `wiki/index.md` above 1,500 tokens, it must collapse older entries into `topic-summaries.md` instead.
5. **Skill metadata total across all 6 skills ≤ 1,000 tokens.** Every word in a skill's `description` frontmatter is paid for on every user turn.
6. **LEDGER.md is never read on SessionStart.** It is appended at session end. Reading it costs tokens; growing it is the point.

---

## Why these numbers

- `3,000` for SessionStart is the inflection point below which conversation latency stays imperceptible on Sonnet-class models.
- `1,000` for skill metadata is Anthropic's recommended ceiling.
- `12,000` for full `write` assembly is well below the effective-context sweet spot, leaving headroom for long raw briefs without replanning.
- Heavier `weekly-review` budget reflects that it runs on the $200 maintainer plan, not the daily user's $20 plan.

---

## Updating this file

Only maintainer commits edit `TOKEN_BUDGET.md`. Every edit references a `learnings/` slug or a stakeholder ask in the commit message. The lint skill reads this file on every commit and every skill invocation.
