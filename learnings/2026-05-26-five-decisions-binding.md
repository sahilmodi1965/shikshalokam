---
date: 2026-05-26
slug: 2026-05-26-five-decisions-binding
source_session: Sahil + Sonal joint call — five workflow decisions, all approved
classification: structural
promoted: partial  # rules A+B + log page built same-session; CLAUDE.md amendment paste-ready
promoted_at: 2026-05-26
promoted_by: Sahil (verbal "yesss" to all five decisions, screen-shared call with Sonal)
landed_so_far:
  - "tools/build_log.py — first stub generator for docs/log.html"
  - "docs/log.html — production log page, live"
  - "docs/index.html — nav link to /log/ added; today's timeline entry replaced"
  - "projects/README.md § Per-session contract — source-attached-briefs default added"
  - "LEDGER.md — fourth entry of the day for this build"
  - "tools/session_start.sh + .claude/settings.json — Rule B promoted from contract to harness: SessionStart hook now invokes a loud-by-design auto-pull-preflight script (fast-forward only, prints state to every session open, never silently swallows errors). Replaces the prior hook which used --rebase + 2>/dev/null + || true (the exact silent-fail mode that put local 2 commits behind Sonal's session this afternoon)."
pending_maintainer_paste:
  - "CLAUDE.md § 4 End — Rule A (always-push) + Rule B (auto-pull preflight) + production-log mention"
  - "wiki/voice/styleguide.md — § Shikshagraha mentions snippet from [[2026-05-26-movement-frame-people-actors]]"
related:
  - "[[2026-05-26-push-during-session-for-review]] (predecessor — push-mid-session rule)"
  - "[[2026-05-26-movement-frame-people-actors]] (predecessor — voice rule paste-ready)"
  - "[[2026-05-26-content-from-brain-directed-run]] (the directed-run pattern)"
---

# Learning — 2026-05-26 — Five decisions, all binding

## The decisions (in Sahil's words: *"yesss"*)

1. **Auto-push + auto-pull rules → binding from today.**
2. **Build the log page this session.**
3. **Default for emailed briefs with sources attached → Sahil routes.**
4. **Friday 29 May, 4pm IST as the standing weekly-review slot.**
5. **Sahil will paste the three hand-edit items after the call.**

Said yes to all five in the same breath. This learning records them so they bind from this commit.

---

## Decision 1 — Auto-push + auto-pull rules

### Rule A — Always-on auto-publish
**Every chat session that touches files on disk pushes that change before the wrap.** Push is the
default; non-push requires explicit opt-out (*"don't push, this is a draft"*). The reviewable URL is
the only valid form of "I'm done." Chat is the means; the live page is the artefact.

### Rule B — Auto-pull preflight
**Every session, before reading or writing anything, runs `git fetch && git pull --ff-only` first.**
If the local can't fast-forward, the brain stops and asks before resolving — never silently
overwrites.

### Why this matters
Today's call caught both failure modes live: (a) the morning's content-from-brain session handed
back URLs that weren't pushed, so Sonal saw stale HTML; (b) this afternoon's session opened with
local 2 commits behind Sonal's morning session — without auto-pull, edits would have silently
overwritten her voice rule.

### Rule B is now harness-enforced (2026-05-26, same call)

The existing SessionStart hook in `.claude/settings.json` was buggy in exactly the way that put
local 2 commits behind this afternoon — it used `git pull --rebase`, bailed silently on a dirty
tree, and `|| true`'d any error. Replaced with `tools/session_start.sh` which is loud-by-design:
prints state on every session open, uses `--ff-only` (never rewrites history), warns visibly when
the tree is dirty or diverged, returns 0 so Claude Code starts cleanly. Every Claude Code session
in this repo on any machine now auto-pulls before reading or writing anything. Contract → code.

### Paste-ready CLAUDE.md amendment (Sahil hand-edits CLAUDE.md after the call)

Insert into `CLAUDE.md` § 4 End, replacing the existing "After the wrap, the SessionEnd hook
auto-commits + pushes" line (or augmenting it):

```markdown
### 4a. Start — auto-pull preflight (binding)

Before reading or writing **anything**, every session runs:

```
git fetch && git pull --ff-only
```

If the local can't fast-forward (someone else pushed while this branch had uncommitted edits),
the brain stops and asks before resolving. Never silently overwrite the remote.

### 4b. During / End — always-on auto-publish (binding)

**Every session that touches files on disk pushes before the wrap.** Push is the default; the
only opt-out is the explicit user instruction *"don't push, this is a draft"* — and even then,
the brain warns once that the change will sit dirty until the next session.

The SessionEnd hook becomes the safety net (catches the rare ungraceful close), not the primary
publish path. Sessions that produce a reviewable artefact link MUST push *before* writing the
wrap — the wrap describes a live state, not a queued one.
```

---

## Decision 2 — The production log page

### What was built (in this session)

- **`docs/log.html`** — a chronological list of every session-bundle, newest first, generated from
  `LEDGER.md` + `git log`. Three columns per row: when (date + author), what (artefact title +
  direct link to the live page), why (one-line ask). Becomes the single source of truth for
  *"what has the brain produced and what needs review."*
- **`tools/build_log.py`** — stub script for regenerating `docs/log.html` from `LEDGER.md` on
  every session that touches the brain. First version is a simple Python script run on demand
  (`python tools/build_log.py`); future passes can wire it into the SessionEnd hook.
- **Nav link** added to `docs/index.html` bar: *Log →* points to `log.html`.

### Per-session contract addition (paste into CLAUDE.md § 4 End or § 5)

> Every session that appends a LEDGER entry must also append a row to `docs/log.html`. Either
> regenerate it via `python tools/build_log.py` (preferred), or hand-edit the top row in place
> until the build script is hardened. The log page is the public review surface; if a session
> isn't on it, the brain didn't compound for Sonal.

---

## Decision 3 — Default route for source-attached briefs

When Sonal emails Sahil a brief with **source material attached** (transcript, PDF, Drive share,
Google Sheet — anything that requires real ingest), the **default route is**:

**A — Sahil routes through his account.** Heavy ingest lives on the $200 plan; Sonal's $20 sessions
stay focused. Today's Masthanaiah portrait + Nagaland NLNF story ran this pattern end-to-end and
validated it.

Sonal's $20 session is reserved for:
- Reviewing the URLs Sahil's directed run produces
- Brainstorm-led sessions (no heavy ingest, just thinking out loud with the brain)
- Quick captions, single-paste briefs, asking the brain what it knows

### Where this lands

- `projects/README.md § Per-session contract` — adds the **"Two valid session shapes"** clause
  below `## Per-session contract`. Reflects both *brainstorm-led* (Sonal-driven) and *directed*
  (Sahil-routed-from-email) patterns. Today's commit lands it.

---

## Decision 4 — Friday 29 May, 4pm IST — weekly review slot

### The ritual (per `ARCHITECTURE.md` § Weekly)

Sahid + Sonal, 30 minutes. Runs the `shikshalokam-weekly-review` skill on a maintainer call.
Sifts this week's LEDGER + `learnings/`. Promotes structural learnings into `wiki/**` edits
(with `corrected_by:` references). Adds new routes. Flips `_status:` to `user-validated` where
evidence supports. Marks contradicted files stale.

### The first slot

**Friday 29 May 2026, 4pm IST.** Three structural learnings from this week are already queued
for promotion:

1. `learnings/2026-05-26-push-during-session-for-review.md` — push-mid-session rule (already
   covered by the auto-publish rule in Decision 1, but the learning stands as the audit trail).
2. `learnings/2026-05-26-movement-frame-people-actors.md` — voice rule (paste-ready snippet
   waiting for Sahil's hand).
3. `learnings/2026-05-26-five-decisions-binding.md` — this file. Covers the workflow tidy +
   the production log build.

Sahid runs the skill; the call ends with three commits to the brain that flip three learnings
to `promoted: true` and one `wiki/voice/styleguide.md` to `_status: user-validated`.

### Where this is recorded

- A new field in `brain.yml` would be the cleanest home (`weekly_review_slot: "fri-16-00-ist"`)
  but `brain.yml` is in the maintainer-only deny list per CLAUDE.md. **Sahil to add the field
  by hand** in the post-call paste batch. Until then, the slot lives in this learning + in
  Sahid's calendar.

---

## Decision 5 — Sahil's hand-paste queue (post-call)

Three items waiting for Sahil's hand after the call. Each requires explicit maintainer commit per
CLAUDE.md rules 8 (voice) + 10 (CLAUDE.md / brain.yml self-edit guard).

### Item 1 — Voice styleguide
**File:** `wiki/voice/styleguide.md`
**Snippet:** `learnings/2026-05-26-movement-frame-people-actors.md § Paste-ready snippets`
**Commit message:** *(see same learning § Suggested commit message)*

### Item 2 — CLAUDE.md § 4 — push-mid-session
**File:** `CLAUDE.md` § 4 End
**Snippet:** From `learnings/2026-05-26-push-during-session-for-review.md § The amendment`

### Item 3 — CLAUDE.md § 4 — Rules A + B
**File:** `CLAUDE.md` § 4 End (or new § 4a + 4b)
**Snippet:** This learning § Decision 1 § Paste-ready CLAUDE.md amendment (above)

### Item 4 (bonus) — `brain.yml` weekly slot
**File:** `brain.yml` § config
**Add:**
```yaml
  weekly_review_slot: "fri-16-00-ist"  # first slot: 2026-05-29 16:00 IST; Sahid + Sonal; runs shikshalokam-weekly-review
```

### Suggested combined commit message for the batch paste

```
binding: 5 workflow decisions land — push, pull, log, route, review slot

Lands the four pastes deferred by CLAUDE.md rules 8 + 10:
- CLAUDE.md § 4: Rule A (always-push), Rule B (auto-pull preflight), production-log mention
- CLAUDE.md § 4: push-mid-session rule (re-affirmation; covered by Rule A)
- wiki/voice/styleguide.md: § Shikshagraha mentions — movement as frame, people as actors
- brain.yml: weekly_review_slot for the standing Friday ritual

Cites: learnings/2026-05-26-five-decisions-binding.md
       learnings/2026-05-26-push-during-session-for-review.md
       learnings/2026-05-26-movement-frame-people-actors.md
```

---

## What "binding" means here

The brain treats these rules as binding **from this commit forward**, even though three of them
sit in files the brain can't edit itself. Sessions read `learnings/` at start; the learnings
*are* the contract until CLAUDE.md catches up. Sahil's paste makes the contract enforceable by
the lint skill; until then it's enforceable by the brain reading this file.

If a future session breaks any of the five rules above, that's a `learnings/` entry against the
brain — not a CLAUDE.md misread.
