# InvokED 6.0 — chatlog

Append-only. One block per session thread.

---

## 2026-06-01 — Sahil (directed run, routing Sonal's email) — workspace seeded from InvokED 5.0 corpus

**Thread.** Sonal emailed Sahil four InvokED 5.0 documents — concept note, session transcripts,
summary, and the email-invitation library — and asked: *"We are starting to roll out invitations for
InvokED 6.0, and I wanted to create this using Claude Code. Please let me know once I can proceed…
prepare a project specifically for this as well after absorbing the data."*

**Directed run** (per the project convention: emailed brief + source material → Sahil ingests on the
$200 account, Sonal reviews the URL).

**What the brain absorbed.** The four Google Docs were read via Drive (transcripts ~1.1M chars,
processed by subagents to keep context clean) and reconciled into three faithful `wiki/sources/`
files:
- `invoked-5-concept-note-2026` — the canonical what / why / who / "what you gain" (Mission to
  Movement; 6–7 Feb 2026; PCPA Bengaluru; 1,000+ audience; segment value props).
- `invoked-5-proceedings-2026` — sessions, ~25 verbatim quotes, outcomes/announcements, bright-spot
  numbers, named grassroots stories (digest of the summary + transcripts docs).
- `invoked-5-email-invites-2026` — the full invitation library: skeleton, ~17 archetypes, standing
  phrases, signatories, logistics, verbatim canonical templates. **The direct model for 6.0.**

**What the workspace holds.** Twelve invite templates rewritten as **6.0-ready skeletons** with
`{{PLACEHOLDERS}}` for the handful of things that change year to year (edition, tagline, dates,
venue, register link). An audience→signatory→template map. A momentum bank of verified 5.0 outcomes
to weave in. A standing-phrase bank. And — front and centre — a **gap-list of the 6.0 specifics the
brain refuses to invent**: tagline, dates, venue, confirmed speakers, register link, dinner date,
roundtable slot. Fill those in chat and every template resolves.

**Decision — no invented facts.** 5.0 was the "fifth edition." 6.0 is assumed sixth, but dates,
venue, and theme are org decisions, not the brain's. Surfaced as placeholders + a flagged table,
the same gap-surfacing pattern Sonal liked on the Masthanaiah portrait and the Nagaland story.

**Open question for Sonal (in the wrap):** the 6.0 tagline + dates + venue, and whether 6.0 keeps the
four-pillar frame / 250 Districts anchor and re-runs Learning Journey + Dinner + Roundtable + Tech
Track.

**Next session shape.** Sonal opens Claude Code: *"InvokED 6.0 — draft the government-official invite
for [Name]"* (or any segment) → Claude resolves the template and writes the draft as a
`### Invite —` section, `status: draft`.
