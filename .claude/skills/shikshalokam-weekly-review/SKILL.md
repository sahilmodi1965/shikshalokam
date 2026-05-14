---
name: shikshalokam-weekly-review
description: Run the Friday weekly review ritual with the maintainer + daily user. Sift LEDGER entries from the past week, promote structural learnings to wiki/ edits (with corrected_by appends), flip _status: from research-seeded to user-validated where evidence supports, mark contradicted files stale. Heavy ops — runs on $200 maintainer plan. Output: a one-page review summary + the commits made.
---

# shikshalokam-weekly-review

## When this fires
- Manually invoked by the maintainer on `brain.yml: weekly_review_day` (default Friday).
- Auto-flagged if `learnings/` has unpromoted entries older than 7 days.
- Does NOT fire in daily-user sessions. Heavy ops only.

## What it reads
- `LEDGER.md` — entries since last review (default: last 7 days).
- `learnings/*.md` — all entries with `promoted: false`.
- `wiki/index.md` and `wiki/_index/topic-summaries.md`.
- Specific `wiki/**.md` files referenced in `learnings/` `target_files`.
- `wiki/voice/styleguide.md` (one of the few skills that may read this — only for review of structural voice learnings).

## What it does
1. **Summarise the week.** Read LEDGER entries since last review. Group by theme. Surface:
   - Total sessions this week.
   - Asks that recurred (signal that brain may need new synthesis page).
   - One-offs that recurred (signal that one-off may actually be structural).
   - `_status: research-seeded` files that the daily user touched (candidates for promotion).
   - Gaps the brain admitted (`not-in-brain` flags, missing-source notes).
2. **Promote structural learnings.**
   - For each `learnings/<slug>.md` with `classification: structural` and `promoted: false`:
     - Open the listed `target_files`.
     - Apply the `suggested_change`. Preserve intent; edit precisely.
     - Append the learnings slug to the file's `corrected_by:` frontmatter.
     - Flip `_status:` to `user-validated` (or keep, never demote).
     - Set the learnings entry's `promoted: true`, `promoted_at: <today>`, `promoted_commit: <sha>` (after commit).
   - Commit each promotion in its own commit. Message format: `wiki(<file>): promote learnings/<slug> — <one-line change>`. The learnings slug is required (lint enforces).
3. **Voice updates.** If a learnings entry targets `wiki/voice/**`, the maintainer reviews with the daily user before promotion. Voice is hand-curated.
4. **Stale flags.** For any `wiki/**.md` file contradicted by the week's LEDGER or by a new source: flip `_status: user-validated → stale`. Commit message: `wiki(<file>): _status stale — contradicted by <evidence>`.
5. **Route additions.** Daily user's route requests from the week (surfaced in LEDGER) get added to `routes/<purpose>.md` by the maintainer. Each route names last-validated date.
6. **Pinned LEDGER entry.** Append a maintainer-authored entry to `LEDGER.md` summarising the review:
   ```
   ## 2026-05-15 14:00 UTC — Sahid (maintainer) — weekly-review
   - Sifted: 9 LEDGER entries, 3 learnings.
   - Promoted: 2 structural learnings → wiki/concepts/shiksha-chaupals.md, wiki/voice/styleguide.md.
   - Stale: 0.
   - Routes added: 1 (donor-pitches Drive folder).
   - Themes recurring: storytelling around individual children; next maintainer pass should pull more child-story samples.
   ```

## What it must not do
- Do not run as the daily user. This is a maintainer skill on the $200 plan.
- Do not promote learnings the daily user hasn't seen. If a learning has not been reviewed live with the user, ask before promoting (especially voice changes).
- Do not exceed 16,000 tokens total prompt assembly. (Heavier than other skills, but bounded; maintainer plan absorbs.)
- Do not silently discard `learnings/` entries. Unpromoted entries stay on disk with `promoted: false` — they're a backlog signal.

## Output format
- One-page maintainer-readable review summary (in chat).
- N commits made (one per promotion, plus the pinned LEDGER entry).
- Pinned LEDGER entry is the user-facing artefact of the review.
