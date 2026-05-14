# Brain Ledger — ShikshaLokam

The single growing artefact. Every session leaves one entry. New entries appended at the top. Scroll down for older history.

This file is the **proof the brain compounded**. If a session ended with no entry here, INTENT principle 2 was violated — the brain didn't compound. `brain-lint` flags any commit missing today's ledger entry.

**Read this file** to see the brain's recent moves. **Show this file** in stakeholder demos when the question is "is it actually getting smarter?"

---

## How an entry looks

```
## 2026-05-14 14:23 UTC — Sonal — bihar-chaupal-linkedin

- **Asked:** 250-word LinkedIn post on Charan, a child at the Hirehalli Shiksha Chaupal
- **Produced:** drafts/2026-05-14-bihar-chaupal.md (review-ready)
- **Learned:** structural — "Chaupal moment" should replace "intervention" → learnings/2026-05-14-chaupal-moment.md → flagged for Friday review
- **Status changes:** wiki/concepts/shiksha-chaupals.md research-seeded → user-validated
- **Sources touched:** [[mothers-of-courage-press]] [[shikshagraha-content-platform]]
- **Voice notes:** Pratik confirmed Charan-as-protagonist framing; rejected "leverage" (already in Never list)
```

Each entry is 5–8 lines. Short on purpose — the ledger is a scannable timeline, not a transcript.

## Fields

- **Asked** — one line. What the daily user requested, in their words (or close paraphrase).
- **Produced** — one line. What artefact the brain made. Cite the file path if it landed in `output/`; otherwise summarise the answer.
- **Learned** — one line. One of:
  - `nothing` — no correction surfaced
  - `one-off — <user's words>` — a correction noted but judged non-structural
  - `structural — <topic> → learnings/<date>-<slug>.md → <target wiki file(s)>` — correction routed to weekly review
- **Status changes** — one line per affected file: `wiki/path.md <from> → <to>`. `none` if nothing flipped.
- **Sources touched** — wikilinks to `wiki/sources/*` the brain pulled from while producing. Empty list `[]` if none.
- **Voice notes** (optional) — only when voice rules were applied, confirmed, or contested. Skip otherwise.

## Lifetime invariants

- **Append-only.** Never edit an existing entry. Corrections to a past entry are written as a new entry that references the old timestamp.
- **One entry per session.** Multi-ask sessions still produce one entry — combine into a single asked/produced/learned summary. Forced concision is the point.
- **Newest at top.** New entries inserted directly below this "How an entry looks" block, pushing older entries down. Demo-readers see latest first.
- **Lint-enforced.** `brain-lint` fails the commit if the current session produced no LEDGER entry. The `SessionEnd` hook auto-commits only after verifying the entry exists.

## Why this file exists

Three reasons.

1. **Demo evidence.** Stakeholders ask "is it learning?" and the answer is a scroll. Three months of entries shows compounding more honestly than any metric.
2. **Successor handoff.** If the daily user hands the brain to someone else, the new person reads the LEDGER top-to-bottom and inherits the brain's actual history — not the maintainer's tribal memory.
3. **Audit.** When a stakeholder asks "where did we say X?", the LEDGER + frontmatter `corrected_by:` references reconstruct the full provenance chain.

The LEDGER is the brain's autobiography. It does not replace `wiki/` (the state) or `learnings/` (the deliberation log) — it complements both by being the one chronological surface.

---

<!-- Entries appended below this line. Newest immediately below. -->

## 2026-05-14 00:00 UTC — migration — content-brain-overlay-applied

- **Asked:** Sahil (maintainer) — apply the unified content-brain overlay to ShikshaLokam.
- **Produced:** unified file shape (wiki/ typed nodes, INTENT.md, ARCHITECTURE.md, AGENTS.md, TOKEN_BUDGET.md, brain.yml, 6 brand-prefixed skills, this LEDGER).
- **Learned:** nothing yet — first user session post-migration is the first real entry.
- **Status changes:** every wiki/**.md now carries `_status:` frontmatter.
- **Sources touched:** none — structural migration, no content changes.
- **Note:** data preserved verbatim from prior state/ layout. Pre-migration git tag: `pre-unify-2026-05-14`.

## 2026-05-14 19:30 UTC — Sahil (maintainer) — first-enrichment-pass

- **Asked:** Sahil — pull movement-level content from the Shikshagraha Drive into ShikshaLokam brain so the May 30 demo lands with a real, populated brain.
- **Produced:**
  - 3 routes added (`routes/drive-communications.md`, `routes/drive-assets.md`, `routes/drive-coffee-table-book.md`) mapping the Shikshagraha Comms folder, Assets folder, Coffee Table Book folder.
  - 2 new wiki sources (`wiki/sources/shikshagraha-narrative-2026.md` — full canonical movement narrative; the "As ShikshaLokam" section explicitly carries SL's own-impact statements; `wiki/sources/shikshagraha-brief-collaterals-feb2026.md` — latest comprehensive movement stats + brochure structure).
  - 1 voice exemplar (`wiki/voice/exemplars/khushboo-newsletter-jan2024.md` — Khushboo Awasthi's canonical year-end newsletter voice; she signs for ShikshaLokam stakeholder comms).
  - `wiki/index.md` populated with real entries (replaces the migration stub).
  - `SHOWCASE.md` written at brain root — the single human-readable page anyone can scroll to see this brain working.
- **Learned:** Comms Strategy doc currently a stub (objectives + audience segments only); worth maintainer enrichment. Khushboo Awasthi appears in BOTH brains' leadership (this brain's COO + Mantra4Change's Co-Founder) — cross-brain references must explicitly name her dual role per INTENT principle 7.
- **Status changes:** none yet — Sonal's session-driven validation flips state as she uses the brain.
- **Sources touched:** [[shikshagraha-narrative-2026]] [[shikshagraha-brief-collaterals-feb2026]] [[khushboo-newsletter-jan2024]]
- **Note:** This is the first real enrichment after migration. Next enrichment is monthly (Sahil $200 plan); next weekly review is Fri May 23 with Sahid + Sonal. The brain is now ready for Sonal to test in a fresh terminal session.

## 2026-05-14 20:30 UTC — Sahil (maintainer) — captions-2026-27-ingested

- **Asked:** Sahil — pull the live SM Captions 2026-27 doc that's always being worked on, add as ongoing reference.
- **Produced:**
  - Updated `routes/captions.md` to reflect that the 2026-27 doc is now fetched + ingested (was previously "pending re-share").
  - New voice exemplar: `wiki/voice/exemplars/sm-captions-2026-rhythm.md` with the canonical monthly weekday rhythm (Mon feedback / Tue research / Wed studio / Thu portrait / Fri InvokED) and 6 real April-May caption exemplars covering InvokED session teasers, research insights, event announcements (Skoll World Forum), coverage reposts (DEP Nagaland — sourced cross-brain mention of Mantra4Change), welcomes, and awards closing.
- **Learned:** The 2026-27 captions doc is **always-being-worked-on** — needs monthly re-pull. Added that note to the route file so future enrichment passes know to refresh.
- **Status changes:** `routes/captions.md` updated from "pending re-share" to "fetched + ingested 2026-05-14."
- **Sources touched:** [[sm-captions-2026-rhythm]] [[captions]]
- **Note:** The Nagaland DEP April caption is a sourced cross-brain reference (mentions Mantra4Change as partner) — kept verbatim per INTENT principle 7 (cross-brain references explicit + sourced, never transplanted).
