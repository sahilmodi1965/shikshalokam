---
date: 2026-07-29
person: Sonal Bhasin
project: mitra
---

# The four MItra use cases are now in the brain

Sonal asked the brain to read and understand all the MItra use cases. It couldn't — they were
nowhere in `wiki/`. Fixed.

## What got made
- **[[mitra-concept-note-use-cases]]** — the canonical record: what MItra is, who it's for, the
  **four current use cases** (Discussion Capture · Story Capture · Evaluation Studies · Perception
  or Feedback Capture), the superseded 2025 set, the benefits framing, and every live deployment
  visible in Drive.
- **`projects/mitra-webinar/page.md:32`** — agenda item 6 said "the four use cases" and never named
  them. It names them now, and links to the source.

## The gap that made this necessary
The brain held MItra's *positioning* (the blog, "not a survey, not a form, a companion") and one
deep *deployment* (the InvokED survey), but nothing about what the capability is actually for. A
teammate asking "what does MItra do" would have got an anchor line and a single example.

## Worth flagging
- **The concept note has two versions and they disagree.** V2 (24 Jun 2026, "MItra by ELEVATE") is
  current. V1 (2025) lists a completely different four. Anyone quoting an old deck will name the
  wrong set.
- **"Repository of Improvements" quietly disappeared.** It was a V1 use case — a best-practice base
  where AI matches your current challenge to an exemplar project you can adapt and run. In V2 it
  survives only as a *benefit*, not a use case. Flagged on the source file; worth confirming whether
  that was deliberate.
- **Multilingual is real, not aspirational.** Every live requirement template carries actual
  translations — Hindi, Tamil, Kannada — against each question.

## What we learned
- **The brain knew how to talk about MItra before it knew what MItra does.** Comms material got
  absorbed as it was produced; the product definition never did, because nobody was drafting from
  it. Positioning arrives on its own; substance has to be fetched deliberately.
- **Auth fragility is now a recurring tax.** Second token failure in a week. The Cloud project sits
  under a personal Gmail (`modi.sahil.im@`), outside the shikshalokam.org Workspace — which is why
  "Internal" isn't available, why every login hits an unverified-app warning, and why team auth
  keeps breaking. Publishing to Production (24 Jul) fixed the 7-day expiry but not the root cause.
- **`oauth_client.json` is deliberately not in git.** Correct, but it means a fresh machine can't
  log in without a manual Drive download — and the failure message doesn't say where to look.

## Next
- Confirm whether **Repository of Improvements** was intentionally dropped from the use-case set.
- **Move the Cloud project into the shikshalokam.org Workspace org** — the real fix for team auth.
  Needs Sahil (project owner) + a Workspace admin.
- MItra Blog Part 2 exists in Drive ("MItra Blog 2026") but isn't published or absorbed.
