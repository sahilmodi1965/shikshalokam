---
name: shikshalokam-gsuite
description: The brain's hands in Google Workspace — draft Gmail, send only after explicit approval, generate approved content into one shared Drive folder as Google Docs, make calendar invites. Triggers on "draft an email to X", "send it", "make a doc of this", "put this in Drive", "set up a call with X", "send the invite". Runs as the logged-in teammate via tools/gsuite/gs.py. Never sends, shares, or notifies without a human yes.
---

# shikshalokam-gsuite

The brain's hands for Gmail, Drive, Docs, and Calendar. The teammate just talks; this
skill turns that into the right `tools/gsuite/gs.py` call, **as them**, with the two
gates always intact. If someone isn't logged in yet, point them to
`onboarding/gsuite-setup.md` Part B (one command, one click) — don't make them think
about auth.

## When this fires
- "Draft an email to <person> about <thing>" → write it in voice, then create the draft.
- "Send it" / "send the email" → send that specific draft (a separate, approved step).
- "Make a Google Doc of this" / "put the approved post in Drive" → generate a Doc.
- "Set up a call / meeting with <person> <time>" → create a calendar event.
- "Send the invite" → notify attendees.

## The flow

**Email (draft → approve → send):**
1. Compose the email at full quality in the team's voice (lean on shikshalokam-write
   for the body — never a thin draft).
2. Show the teammate the email in chat. Then create the draft:
   `gs.py email-draft --to … --subject … --body-file <tmp.md>`
3. Surface the draft id and that it's in their Gmail → Drafts. **Stop.**
4. Only when they explicitly say send: `gs.py email-send <draft_id>`. Confirm the
   messageId back. Never infer approval from "looks good" — get an actual yes.

**Doc / Drive (publish ONLY on Sonal's explicit approval):**
- The brain repo is the source of truth. Anyone can draft; content lives in the
  brain (versioned, visible) until **Sonal approves it explicitly**. Writing to
  Drive *is* the publish event — so `doc-create` runs **only after Sonal's clear
  yes**, not on any teammate's request. If someone else asks to "put it in Drive,"
  hold it in the brain and note it's pending Sonal's approval.
- On Sonal's approval: `gs.py doc-create --title … --body-file <approved.md>` →
  lands in the shared **Docs** folder (from `drive_map.json`) and returns a link.
  Surface the link.
- New project folder? `gs.py drive-folder --name … --parent <id>`. Keep the shared
  tree tidy — generated/approved content only, never raw dumps. The taxonomy lives
  in `brain.yml → gsuite.output_taxonomy`.
- If `drive_map.json` is missing, the shared folder hasn't been built yet — the
  maintainer runs `gs.py drive-init` once (Part A step 7).

**Calendar (create → notify):**
- `gs.py cal-invite --summary … --start … --end … --attendees …` adds it to their
  calendar **silently**. It emails attendees **only** with `--notify` — treat that
  flag as a send and get an explicit yes first.

## Non-negotiables
- **Three gates, always.** (1) Email send and (2) calendar `--notify` need a clear
  yes from the person at the keyboard. (3) Drive publish (`doc-create` / writing
  approved content) needs **Sonal's explicit approval** — she is the approver; the
  repo is the source of truth until then.
- **Act as the logged-in person.** Run `gs.py whoami` if unsure who's driving;
  attribution must stay honest. Don't act as someone who isn't at the keyboard.
- **One tidy shared folder.** Approved content is generated into "ShikshaLokam —
  Brain Output"; never scatter loose files or dump raw material there.
- **Speak the house style** — see CLAUDE.md "How the brain speaks." Short, indented,
  managed-upwards. Confirm what happened in a line, not a paragraph.

## After acting
A clean session digest line (what was drafted / sent / generated, with the link), so
the brain compounds. Never paste raw email bodies or private content into sessions/.
