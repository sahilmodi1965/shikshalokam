---
name: shikshalokam-ops
description: The architecture lane — the brain files and fixes its OWN bugs, frictions, ideas, and CI failures as GitHub Issues, then resolves them with auto-merging PRs. No one flags anything on WhatsApp. Triggers when something breaks or feels clunky, when a teammate suggests an improvement, on "triage the backlog" / "what's broken" / "file that", and at session start to sweep open issues. CONTENT never comes through here — content publishes every session via the content lane.
---

# shikshalokam-ops

How the brain evolves itself. Two lanes, never confused:
- **Content lane** — what teammates make. Publishes **every session, seamlessly** (handled by
  `tools/publish.sh`; same-page edits auto-merge, nothing lost). Never goes through Issues.
- **Architecture lane** (this skill) — how the brain itself improves: bugs, frictions, ideas, CI
  failures. These become **GitHub Issues the system files and fixes autonomously**.

Tooling: `tools/ops.sh` (needs the GitHub CLI `gh`, authed once). If `gh` isn't here, it says so
with the one-time setup — surface that, don't silently skip.

## File, don't flag (no WhatsApp)
The moment you or a teammate hits a bug, a friction ("this step is clunky"), an idea, or you see a
red CI run — **file a GitHub Issue**, don't ask anyone to remember it:
```
tools/ops.sh issue "<short title>" "<what + why + where>" bug|friction|feature|ci
```
A red build already files its own issue automatically (`.github/workflows/ci-failure-to-issue.yml`).

## Triage + fix (every session, and on "triage the backlog")
1. `tools/ops.sh backlog` — list open issues.
2. Pick the highest-value, clearly-scoped one. (Big/ambiguous ones: leave a comment with a plan.)
3. Fix it on a branch:
   - `git checkout -b issue-<n>-<slug>`
   - make the change · build-check (`python3 tools/build_site.py`) · keep it tight.
4. Ship it as an auto-merging PR:
   - `tools/ops.sh fixed "issue-<n>-<slug>" "<title>" "<what changed>" <n>`
   - It opens the PR, links the issue (auto-closes on merge), and sets **auto-merge**.
5. Note what you did in the session digest.

## Rules
- **Architecture changes go through Issues** — so there's a visible, trustable trail. Content does not.
- **Small, safe, reversible** PRs. Don't bundle unrelated fixes.
- **Never touch the gates or the honesty machinery** without flagging it explicitly to the team first.
- **Auto-merge is on** for now — keep things moving; a bad change surfaces as a new CI issue and
  self-corrects. (Repo settings: "Allow auto-merge" must be enabled.)
- If `gh` is missing on this machine, the lane is read-only — tell the user the one-time `gh` setup
  rather than dropping the item.

## The point
Nobody chases the backlog in chat. The brain notices, files, fixes, and records — and gets better
every session. Humans spend their attention on content and judgement, not coordination.
