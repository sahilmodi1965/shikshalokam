---
name: publish-confirmation-rca
description: RCA — why the brain told Sonal her InvokED 6.0 invites were "live in ~60s" when the public page never updated; the hand-mirrored HTML drift, and the fix (generated pages + auto-regen hook)
metadata:
  type: feedback
---

# RCA — the brain told Sonal her work was published when it wasn't

**Reported by Sahil, 2026-06-04:** "Sonal's activity is not writing into the main webpage after her
message — a big failure of the system." And: "RCA on why the brain lied to Sonal in her session about
publishing to the page in 60 seconds, when checking shows that's not the real case at all."

**Why:** A brain that tells the daily user "it's live" when it isn't is worse than one that fails
loudly. Sonal approved invites, was told they were published, walked away — and the live page showed
neither her new approvals nor even the *revised* version of an older one. Trust in the whole system
turns on the wrap being true.

**How to apply:** The publish-confirmation the user sees must be a *consequence* of the artifact
actually reaching the live page — never a hard-coded line emitted regardless of what happened.

---

## Symptom

- Sonal's sessions on 2 Jun and 3 Jun approved/refined InvokED 6.0 invites (Camille Massey, the
  advisors-group invite; the Peggy Dulany draft was revised on 1 Jun).
- Each session ended with the standard wrap: *"👉 https://…/ (refreshes in ~60s)."*
- The live invite page `docs/projects/invoked-6.html` stayed frozen at **"1 June 2026 · two VIP
  invites approved,"** and still showed the **superseded** Peggy Dulany draft (the "One Billion
  Futures" version Sonal had already edited out). None of the later activity appeared.
- The 3 Jun LEDGER entry even asserted *"All pushed to live brain page."* That was false.

## Two distinct failure mechanisms (do not conflate them)

**Mechanism 1 — silent push failure (the Wendy Kopp incident, pre-2 Jun).**
Sonal's *web* session lacked GitHub write access. The old SessionEnd one-liner ended in
`git push … || true`, so the failed push was swallowed: work committed locally, never reached
GitHub, evaporated when the tab closed. **Already fixed on 2 Jun** — `tools/session_end.sh` now prints
an unmissable failure block instead of swallowing it.

**Mechanism 2 — the actual recurrence on 3 Jun (this RCA).** The push *succeeded*. The failure was
upstream of the push:

1. The approved invite copy was written **only** into the front-page timeline (`docs/index.html`)
   and `learnings/` — it was **never written into `projects/invoked-6/page.md`**, the project's
   source of record. The substance lived in the chat session and then was gone.
2. `docs/projects/invoked-6.html` was a **hand-authored mirror** of `page.md`. Keeping the two in
   sync was a manual copy-paste at session end. That step was skipped on 2 Jun (page.md edited, HTML
   not regenerated → drift) and never even reached on 3 Jun (page.md itself wasn't touched).
3. The wrap line *"refreshes in ~60s"* is **hard-coded**. The model emits it every session regardless
   of whether the page the user cares about actually changed. So the brain "promised" publication
   that, for the invite page, never happened.

## Root cause

Three compounding faults, all structural:

- **(A) The public page was hand-mirrored from its source** → guaranteed drift; the only safeguard
  was a non-blocking `WARN` that couldn't even fire when `page.md` wasn't touched.
- **(B) The publish claim was decoupled from reality** → the wrap says "live in 60s" without checking
  that the relevant artifact reached the live page, or that the push even succeeded.
- **(C) The artifact was never written to the source of record** → approvals went to the *derivative*
  surface (the timeline) instead of the *authoritative* one (`page.md`). The timeline should be
  derived from the work, not be the only place the work exists.

Note why "loud push failure" (the 2 Jun fix) did **not** catch this: on 3 Jun the push succeeded, so
a push-health check reports "✓ pushed." The content simply never entered the artifact that gets
published. Different fault, different fix.

## Fix shipped 2026-06-04 (this session)

- **`tools/build_project_page.py`** — `projects/<slug>/page.md` is now the **single source of truth**;
  `docs/projects/<slug>.html` is **generated** from it. There is no hand-authored HTML left to drift.
  Internal/external can no longer disagree. (Addresses A.)
- **`tools/session_end.sh`** — auto-regenerates the public page for any changed `page.md` *before*
  commit (no human copy-paste to forget), and prints the authoritative list of pages that actually
  went live: `→ live: https://…/projects/<slug>.html`. (Addresses A + B at the system layer.)
- **Re-rendered `docs/projects/invoked-6.html`** from `page.md`, so the live page now shows the
  *revised* Peggy Dulany and the approved Marc/Salesforce invites with correct status pills.

## Fix still required — maintainer actions (cannot be self-applied)

1. **CLAUDE.md §4 wrap contract.** Amend so the wrap may claim a specific project page is updated
   **only when** that project's `page.md` changed this session and regeneration succeeded. For
   project work, the contract is: the produced artifact is written into `projects/<slug>/page.md`
   — that, not a timeline blurb, is what makes it real. (CLAUDE.md is permission-denied to sessions;
   a maintainer applies this. Addresses B + C.)
2. **page.md is the system of record.** The front-page timeline and any summary are *derived*. An
   approval that exists only in the timeline is a bug, not a record.
3. **Web sessions without push access** need a signal Sonal can see — she never sees the terminal
   where the loud push-failure prints. Granting her web session write access (or surfacing the
   failure in-chat) is a human/permissions decision for Sahil. This was flagged on 2 Jun and is still
   open.
4. **Recover the 3 Jun approved copy.** The actual approved text for Camille Massey and the
   advisors-group invite was never saved to the repo. Per Sahil's call: it comes back from Sonal's
   next fresh session (approved on her local system, pushed from there) — not reconstructed here.
5. **Legacy project pages** (`blogs`, `captions`, `nagaland-coffee-book`, `portraits`) have backstage
   content in their `page.md` (raw draft paths, maintainer-TODO language). They are **not**
   regenerated yet — the SessionEnd hook only regenerates a page whose `page.md` changed this session,
   so they cannot leak until cleaned. Each needs a maintainer hygiene pass (or `· internal` section
   markers — supported by the generator) before it is regenerated.

See also [[2026-06-01-vip-invite-voice]] (the invite patterns that survived) and
[[2026-05-26-five-decisions-binding]] (the production-log / publish discipline this extends).
