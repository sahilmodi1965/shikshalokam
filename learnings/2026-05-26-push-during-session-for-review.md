---
date: 2026-05-26
slug: 2026-05-26-push-during-session-for-review
source_session: Sahil — after the first content-from-brain run handed back unpushed URLs
classification: structural
promoted: false  # CLAUDE.md per-session contract amendment — Sahil to land by hand (CLAUDE.md is in maintainer-only deny list)
target_files:
  - CLAUDE.md § 4 End — LEDGER + wrap (change "After the wrap, the SessionEnd hook auto-commits + pushes" to make push mid-session the default when the wrap hands back a live review URL)
  - projects/README.md § per-session contract (note the same)
related:
  - "[[2026-05-26-content-from-brain-directed-run]] (the session that surfaced the gap)"
  - "[[2026-05-19-project-page-architecture]] (the architecture this binds to)"
---

# Learning — 2026-05-26 — push during session for review (not at SessionEnd)

## What happened (verbatim)

Sahil, after I handed back two review URLs at the end of the `content-from-brain-first-run` session:

> *"which link takes me to the udpated content I couldnt see anything? whay is event going on?"*

> *"okay just push dynamically going forward, we will need to review the content created from here
> so they can review it if not pushed how will they even review it"*

## What was wrong

The session produced both pieces on disk, then surfaced two review URLs in the wrap —
**without pushing first.** GitHub Pages was still serving the prior commit. The reviewer
(Sonal in the loop, Sahil checking first) saw yesterday's HTML.

The CLAUDE.md per-session contract reads:

> *"After the wrap, the SessionEnd hook auto-commits + pushes; Pages rebuilds."*

The hook is real and the auto-commit works — but it only fires **at session close**, which can be
minutes or hours after the wrap. Any URL surfaced in the wrap is therefore stale to the reviewer
until the session ends. That's a contract bug for reviewer-facing sessions.

## Classification

**Structural.** This isn't a one-off mistake — it'd repeat on every reviewer-facing session
unless the rule changes. There is precedent already: the 19 May LEDGER entry noted
*"Pushed manually within the session so Sahil could verify the nav + captions render live;
SessionEnd hook will no-op on clean tree at session close."* Today's correction makes that
precedent the default.

## The amendment (for the maintainer to land into CLAUDE.md)

Replace the current "After the wrap, the SessionEnd hook auto-commits + pushes" line with:

> **Sessions that hand back a live review URL (project-page edits, `docs/**.html` changes, any
> artefact a reviewer outside the session needs to see) push mid-session, before writing the
> wrap.** The wrap describes a live state, not a queued one — say "pushed, refreshing in ~60s"
> alongside the URL. The SessionEnd hook then no-ops on a clean tree at session close.
>
> Sessions with no reviewer-facing surface (LEDGER-only housekeeping, learnings file with no
> live mirror, internal `wiki/**` edits not yet wired into a project page) continue to rely on
> the SessionEnd hook.

## Pinning the rule in three places

1. **`CLAUDE.md` § 4 End — LEDGER + wrap** — maintainer-edit only; amendment above.
2. **`projects/README.md` § per-session contract** — note the rule for project-page workspaces
   specifically (these are by definition reviewer-facing).
3. **Memory — Sahil's auto-memory `feedback_push_during_session.md`** — written this turn so
   future Claude Code sessions in this repo carry the rule.

## What this session did differently after the correction

- Staged all 13 modified + 4 new files explicitly (no `git add -A`).
- Committed with a content-named message (`5a55c7e`).
- Pushed.
- Told Sahil one line: "pushed, GitHub Pages rebuilds in ~60s, hard-refresh."

That's the pattern every reviewer-facing session inherits from today onwards.
