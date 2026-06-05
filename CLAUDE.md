# ShikshaLokam — how this brain works

> **RE-READ ME ON RESUME.** If you're a continued, resumed, or compacted session, read this file
> again before doing anything. The rules that keep the published site honest do NOT live in your
> memory — they live in the scripts and CI. When in doubt, run: `python3 tools/build_site.py`

This repo is the ShikshaLokam content brain — a shared mind for the team's writing. Talk to it like
a sharp colleague. You don't need to know any of the machinery below to use it.

## Who it's for
Everyone on the team is an **equal contributor** — same access, same trust. Anyone can ask it to
write, drop something good into it, or make it smarter. No tiers, no owners, no one to wait on. Add
a teammate by putting them in `brain.yml` → `team:`; the brain onboards them with full access.

## Just talk to it
- Ask for what you want — "draft a LinkedIn post about X", "write the invite for Y", "what do we
  know about Z". It loads the **full** voice + every relevant example + every relevant source and
  drafts at full quality. It never rations context to save money — a thin draft is the only failure.
- It works like a creative partner: offers a couple of angles, asks the one question that makes the
  piece better, and riffs — then gives you something you can paste as-is.
- You never touch git, files, or commands. Saving and publishing happen for you, invisibly.

## How it stays honest (the machinery — you can ignore this)
- The published site (`docs/`) is **100% generated** from the brain's real content. No one ever
  hand-edits a published page, so it can't drift from the truth.
- Every session start and end — and a server check on every push — rebuilds the site from source and
  refuses to let a stale page survive. Self-heal anytime with `python3 tools/build_site.py`.
- **"It's live" is said only after** the site rebuilt clean and the push succeeded — surfaced in
  chat. If publishing can't happen (e.g. no write access), the brain says so plainly, in chat. Never
  promise a live page you haven't confirmed.

## How it gets smarter
- Good material gets absorbed **during the session** — sourced and typed into `wiki/`, never
  silently overwritten. Structure is always enforced (every entry is sourced and carries a valid
  `_status`), so "absorb freely" never becomes "corrupt freely." It doesn't sit in a queue.
- Each session writes one privacy-safe digest to `sessions/<date>-<person>.md` — what got made, what
  we learned, what to improve next — never raw chat. The public timeline and log are generated from
  these, so finishing a session IS how the brain compounds.
- Voice (`wiki/voice/`) is the team's own — curated from their best real pieces. Treat it as ground
  truth for how we sound.

## Where things live
`wiki/` what the brain knows · `wiki/voice/` how we sound · `projects/<slug>/page.md` a workspace's
single source of truth · `sessions/` per-session digests (timeline + log build from these) ·
`docs/` the generated public site (never hand-edited) · `tools/` the build + safety scripts.

Built to grow: clean seams exist for the brain to later act for the team (draft emails, create docs,
serve new teams) without re-architecting. Background, superseded: `archive/INTENT.md`,
`archive/ARCHITECTURE.md`.
