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
Tabs: `Overview` · `Questions` (original 12) · `Questions_Revised_10` (current) ·
`Dashboard_Metrics` · `Report_Metrics/Templates`

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

**7 main questions + 3 probes = 10 turns.** Probes live in the follow-up column against their
parent question — they are not separately numbered questions, but each one still spends a turn.

| Q | Block | Probes | Turns | Why it earns the space |
|---|---|---|---|---|
| 1 | Profile — role, org, location | — | 1 | Ecosystem diversity. First candidate for pre-fill. |
| 2 | Editions attended | — | 1 | Repeat participation. Also pre-fillable. |
| 3 | Perception shift | 1 | 2 | Magnitude *and* substance, in two turns instead of four |
| **4** | **Action & outcome** | **2** | **3** | **The core metric and the stories. Never trade these away.** |
| 5 | Org influence | — | 1 | Institutional change — scale + substance in one turn |
| 6 | Continuity | — | 1 | Retention intent + design input for the year-round offer |
| 7 | Stories & recognition | — | 1 | Consent, Awards pipeline, follow-up contact |
| | | | **10** | |

Full text, branch logic, cut-and-recovery map and the probing rules live in the
`Questions_Revised_10` tab, generated from `questions-10turn.json` in this folder.

## The rules matter as much as the questions

A 10-question list without enforcement drifts straight back to 30:
- Hard cap 10 turns. Only Q3 (one probe) and Q4 (two probes) may probe; the other five never do.
- Never re-ask what was volunteered — if Q4's main answer already names the partner, skip probe 1
  (the conversation ends in 9).
- Every branch, including every "No", must return something usable.

## Open decision

**Can registration data pre-fill role / org / country / editions?** If yes, Q1+Q2 collapse into one
confirm-tap and 2 turns come free. Spend them on *"was that collaboration with someone you met at
InvokED, or someone you already knew?"* — that separates InvokED-**caused** from InvokED-adjacent,
a materially stronger claim for the report. This is the highest-leverage change available.

## Still to check

`Dashboard_Metrics` and `Report_Metrics/Templates` were built against the original 12 questions.
Cutting the perception baseline and the standalone network question may leave metrics with no
source. Worth an alignment pass before build.
