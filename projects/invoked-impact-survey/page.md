---
project: invoked-impact-survey
title: "InvokED Impact Survey — the MItra questionnaire"
_status: user-validated
last_updated: 2026-07-27
maintainer: Sahil Modi
daily_user: Sonal Bhasin
page_budget_tokens: 8000
sources:
  - "[[invoked-5-proceedings-2026]] — outcomes and quotes the survey is trying to evidence at scale"
  - "[[mitra-listening-at-scale-part1-2026]] — how MItra's conversational probing works"
voice: "[[styleguide]] — interview register: warm but professional, peer-to-peer, crisp; never simplistic or hand-holding"
shareable_url: "https://sahilmodi1965.github.io/shikshalokam/projects/invoked-impact-survey.html"
---

# InvokED Impact Survey — the MItra questionnaire

The InvokED Impact & Perception Survey runs on MItra as a short conversational interview across the
InvokED 1.0–5.0 community (~800–1,000 registrants, realistic target 150–250 completions). It is
InvokED's move **from visibility to credibility** — proving what happened *after* the events.

**Working template (Sonal's, editable):**
https://docs.google.com/spreadsheets/d/1qMhSkrACZb4zmM2cBWDkyhEma_lDBa6_MkHnSsKU2B8/

| Tab | Status |
|---|---|
| `Questions_Revised_10` | **current** — 6 mains + 4 probes |
| `Dashboard_Metrics_Revised` | **current** — re-sourced to the new numbering |
| `Report_Metrics_Revised` | **current** — per-conversation + aggregate |
| `Questions` · `Dashboard_Metrics` · `Report_Metrics/Templates` | v1, kept for comparison |
| `Overview` | programme brief — unchanged |

Each revised tab is generated from a JSON file in this folder, so it can be regenerated with
`gs.py sheet-add-tab --replace` rather than hand-edited.

## The constraint that shapes everything

**10 questions total, probes included.** Stakeholder feedback, confirmed by Sonal on 2026-07-27 —
not 10 mains with free follow-ups. The original design was 12 mains + ~25 follow-ups ≈ 30 turns.

Why it bites: respondents are senior, time-poor education leaders — funders, government,
researchers, philanthropy. This is the **inverse of MItra's usual grassroots persona**. Length kills
completion in this audience, and a thin sample kills the report.

## What the 10 turns protect

The requirement doc names **post-event action & collaboration** the most critical of the four
capture areas, so it gets 3 of the 10 turns (Q5–Q7). That block is the only one that produces
**Action Stories** — who / what / outcome — which are what the Impact Report, the narrative assets
and Shikshagraha Awards outreach are actually built from.

**6 main questions + 4 probes = 10 turns**, exactly at the cap. Probes live in the follow-up column
against their parent question; they aren't separately numbered, but each spends a turn.

| Q | Block | Probes | Turns | Why it earns the space |
|---|---|---|---|---|
| 1 | Profile — role, org, location | — | 1 | Ecosystem diversity. Pre-fillable. |
| 2 | Perception shift | 1 | 2 | Magnitude *and* substance, in two turns instead of four |
| **3** | **Action & outcome** | **3** | **4** | **The core metric and the stories. Never trade these away.** |
| 4 | Org influence | — | 1 | Institutional change — scale + substance in one turn |
| 5 | Continuity | — | 1 | Retention intent + design input for the year-round offer |
| 6 | **Future readiness** | — | 1 | The narrative asset — how leaders define it, and what they're doing |
| | | | **10** | |

**Q3 carries 4 of the 10 turns** — main + three probes, branching on Yes/In-progress vs No:

| | Yes / In progress | No |
|---|---|---|
| Probe 1 | Who is it with, what are you doing together? | What would you still like to take forward, and what's blocking it? |
| Probe 2 | **Met at InvokED, or already knew them?** | What would make it easier to act on it? |
| Probe 3 | What's come out of it — or what do you expect? | Anyone from InvokED you're still in touch with? |

Probe 2 on the Yes branch is the **attribution question** — it separates an InvokED-*caused*
collaboration from one that merely happened afterwards. That distinction is the strongest claim the
Impact Report can make. On the No branch, probe 3 recovers network data from non-collaborators, so
neither branch wastes its four turns.

## Future readiness — one turn here, a separate survey elsewhere

Q6 asks how the respondent *defines* future readiness and what they're doing about it. It sits last
on purpose: reflective and expansive, so it never competes with the impact data upstream.

What justifies one turn *here* is that this audience is different in kind: these are the people
whose definition shapes how the sector uses the term. Treat the answers as **narrative source
material, not a representative measure.**

**A separate million-voices instrument is not being built for now** (Sonal, 2026-07-27). So Q6 is
the *only* future-readiness data being collected — which makes the framing constraint sharper, not
looser: the report must not imply coverage beyond 150–250 senior leaders. If the listening exercise
is ever picked up, it needs its own audience (teachers, youth, parents, system actors), its own
scale, and grassroots language — MItra's usual persona, not this one.

## Moved out of the conversation (nothing lost)

- **Editions attended** — cut on 2026-07-27 to fund the future-readiness turn. Weakest turn, most
  pre-fillable field. Recover via the registrant record (preferred) or a post-close tap. **If
  neither is possible, reinstate it and drop Q5 instead** — repeat participation is a credibility
  metric and must not vanish.
- **Story/video willingness · Awards nomination · follow-up contact** — cut as no longer aligned,
  but the report spec still expects all three. They move to the **post-close consent screen**
  alongside the optional photo upload. A post-close step isn't a turn, so this costs nothing.

Full text, branch logic, cut-and-recovery map and the probing rules live in the
`Questions_Revised_10` tab, generated from `questions-10turn.json` in this folder.

## The rules matter as much as the questions

A 10-question list without enforcement drifts straight back to 30:
- Hard cap 10 turns, and the design now uses all 10. Only Q2 (one probe) and Q3 (three probes) may
  probe; the other four never do.
- Never re-ask what was volunteered — if Q3's main answer already names the partner, skip probe 1
  (the conversation ends in 9).
- Every branch, including every "No", must return something usable.

## Open decision

**Can registration data pre-fill role / org / country / editions?** This is now load-bearing: it's
how editions-attended gets recovered at all. If yes, Q1 also collapses to a confirm-tap and a turn
comes free. Best use of it: buy back the **perception baseline** before Q2 — *"before your first
InvokED, how did you view collaboration?"* — which would make the before/after shift measurable
rather than self-reported. It was the first thing cut, and the right thing to restore.

## Dashboard & report — what the re-source changed

Every metric was re-pointed at the new numbering. Three things are not just renumbering:

**Two metrics no longer exist. Don't build tiles for them.**
- **Perception baseline / measured before-after** — the baseline question was cut, so shift is
  *self-reported magnitude*, not a measured delta. The published methodology must say so.
- **Network continuity as a single %** — no question is now asked of every respondent about staying
  connected, so a percentage would misrepresent the data. Report **named connections as a count**.

**One metric is orphaned until a build decision lands.**
- **Repeat participation** — editions-attended has no turn. It exists only via pre-fill from the
  registrant record, or a post-close tap. No pre-fill, no metric, and no edition-level segmentation
  in the aggregate report either.

**Four new metrics, one of which should lead the report.**
- **InvokED-caused vs InvokED-adjacent** (Q3 probe 2) — the split between partners *met at InvokED*
  and partners already known. This is the difference between "things happened afterwards" and
  "InvokED caused things." It is the most defensible number in the whole survey.
- **Latent collaborations & barriers** (Q3 No branch) — the Forum lead list; previously the No
  branch yielded almost nothing.
- **Future readiness — definitions** and **— contributions** (Q6) — the narrative layer.

Also carried into the report tab: a **methodology block** on self-selection (respondents who
collaborated are likelier to reply, so collaboration rates skew high — publish the honest number).
