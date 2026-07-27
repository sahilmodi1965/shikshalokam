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
| `Questions_Revised_10` | **current** — 8 mains + 2 probes |
| `Dashboard_Metrics_Revised` | **current** — re-sourced to the new numbering |
| `Report_Metrics_Revised` | **current** — per-conversation + aggregate |
| `Questions` · `Dashboard_Metrics` · `Report_Metrics/Templates` | v1, kept for comparison |
| `Overview` | programme brief — unchanged |

Each revised tab is generated from a JSON file in this folder, so it can be regenerated with
`gs.py sheet-add-tab --replace` rather than hand-edited.

**The sheet carries the spec only — no reasoning, no change history** (Sonal, 2026-07-27). People
open it without any of the conversation behind it, and rationale reads as noise to them. Everything
explaining *why* lives on this page instead. Keep it that way.

## The constraint that shapes everything

**10 questions total, probes included.** Stakeholder feedback, confirmed by Sonal on 2026-07-27 —
not 10 mains with free follow-ups. The original design was 12 mains + ~25 follow-ups ≈ 30 turns.

Why it bites: respondents are senior, time-poor education leaders — funders, government,
researchers, philanthropy. This is the **inverse of MItra's usual grassroots persona**. Length kills
completion in this audience, and a thin sample kills the report.

## The primary objective (Sonal, 2026-07-27)

**InvokED is not a two-day event. The survey exists to evidence what those two days set in
motion afterwards, and the different ways that helped the ecosystem.** Every design call below
serves that sentence. Anything that is feedback about the two days themselves does not belong
in this instrument.

Two consequences, both structural:
- **Substantial action is not the only evidence.** Q3 sets a high bar (collaboration, pilot,
  funding, partnership, decision). Most respondents will answer No to it, and most of the
  ecosystem effect lives below that bar: an idea carried back to a team, an introduction
  brokered between two people, a practice changed, InvokED spoken or written about. **Q4 catches
  all of it, and is asked of everyone regardless of Q3.**
- **Time is the argument.** **Q5** records when the action began and whether it is still live.
  If a meaningful share started months after the edition, the two-day framing collapses on the
  evidence rather than on assertion. That is the most quotable figure the survey can produce.

## What the 10 turns protect

**8 main questions + 2 probes = 10 turns**, exactly at the cap. Probes live in the follow-up
column against their parent question; they aren't separately numbered, but each spends a turn.
The post-event block (Q3, Q4, Q5) holds 4 of the 10.

| Q | Block | Probes | Turns | Why it earns the space |
|---|---|---|---|---|
| 1 | Profile — role, org, location | — | 1 | Ecosystem diversity. Pre-fillable. |
| 2 | Perception shift | 1 | 2 | Magnitude *and* substance, in two turns instead of four |
| **3** | **Action & outcome** | **1** | **2** | **The flagship stories and the headline metric** |
| **4** | **Ripple beyond the project** | — | **1** | **The breadth layer. The "different ways" question** |
| **5** | **Timing & continuity of action** | — | **1** | **The proof it isn't a two-day thing** |
| 6 | Org influence | — | 1 | Institutional change — scale + substance in one turn |
| 7 | Continuity | — | 1 | Retention intent + design input for the year-round offer |
| 8 | **Future readiness** | — | 1 | The narrative asset — how leaders define it, and what they're doing |
| | | | **10** | |

### Q3 — one probe, not three

Q3 was carrying 4 turns (main + three probes) until 2026-07-27. The three-probe ladder had two
faults. On the **No** branch, probe 1 asked *what's holding it up* and probe 2 asked *what would
make it easier to act* — the same question twice, back to back. And the two branches of any given
probe were unrelated questions sharing a slot number: probe 2's Yes side was attribution, its No
side was barriers. Sonal's call: **if they say Yes or In progress, just ask for the details all
together.**

| | Yes / In progress | No |
|---|---|---|
| Probe | What it is · who it's with · **met at InvokED or already knew them** · what's come of it | What you'd still like to take forward · what's holding it up · anyone you're still in touch with |

That returns 2 turns, which bought Q4 and Q5.

**The cost, and the fix.** Partner origin — *met at InvokED vs already knew* — is the strongest
attribution claim the report has. Buried inside a four-part open answer, a share of respondents
will skip it. It is therefore **also a tap on the post-close screen**, which costs no turn. The
report states the base rather than implying full coverage.

Naming *funding unlocked* in the main question still matters: without the prompt, respondents
rarely volunteer it, and it's the outcome funders find most legible.

### Q4 — the ripple, asked of everyone

*"Beyond a formal project — has anything from InvokED travelled? An idea you took back to your
team, an introduction you made between two people, something you spoke or wrote about, a way of
working you changed?"*

Asked of every respondent, **including everyone who said No to Q3**. Before this question existed,
a No made a respondent look like InvokED did nothing for them. Q4 is where the ecosystem story
actually lives, and it produces two metrics that nothing else can: **ripple types** and **reach
beyond attendees** (things that reached people who were never at InvokED).

### Q5 — when, and is it still going

Two taps in one turn: timing (within weeks / a few months later / later in the year / still
unfolding) and state (still going / completed / stalled). Anchored to whatever the respondent
described in Q3 or Q4. **If both were empty, Q5 is skipped and the conversation ends in 9.**
Stalled cases go to the Forum lead list.

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
- Hard cap 10 turns, and the design now uses all 10. Only Q2 and Q3 may probe, once each; the other
  six never do.
- Q4 is asked of every respondent, whatever they answered in Q3.
- Q5 is anchored to Q3 or Q4. If both were empty, skip it — the conversation ends in 9.
- Never re-ask what was volunteered.
- Every branch, including every "No", must return something usable.

## Open decision

**Can registration data pre-fill role / org / country / editions?** This is now load-bearing: it's
how editions-attended gets recovered at all. If yes, Q1 also collapses to a confirm-tap and a turn
comes free. Best use of that turn under the current objective: **split Q5**, so timing and
still-live are asked cleanly rather than as two taps in one breath. Second best: buy back the
perception baseline before Q2, which would make the shift measurable rather than self-reported.

## Dashboard & report — what the re-source changed

Every metric is pointed at the new numbering. Beyond renumbering:

**Two metrics no longer exist. Don't build tiles for them.**
- **Perception baseline / measured before-after** — the baseline question was cut, so shift is
  *self-reported magnitude*, not a measured delta. The published methodology must say so.
- **Network continuity as a single %** — no question is asked of every respondent about staying
  connected, so a percentage would misrepresent the data. Report **named connections as a count**.

**One metric is orphaned until a build decision lands.**
- **Repeat participation** — editions-attended has no turn. It exists only via pre-fill from the
  registrant record, or a post-close tap. No pre-fill, no metric, and no edition-level segmentation
  in the aggregate report either.

**The metrics that carry the objective.**
- **Any post-event effect** (Q3 + Q4) — the share of respondents reporting either substantial
  action or a ripple. **This is now the number the report opens with**, not the collaboration
  count, because it is the direct answer to "InvokED is not a two-day event."
- **Action timeline** and **still live** (Q5) — when it started, whether it's ongoing. The chart
  that makes the argument.
- **Ripple types** and **reach beyond attendees** (Q4) — the different ways InvokED helped,
  including everything that never became a project.
- **Ripple among non-collaborators** (Q3 = No × Q4) — the guard against misreading a No.
- **InvokED-caused vs InvokED-adjacent** (Q3 probe + post-close tap) — still the most defensible
  attribution claim, now reported with its base stated.
- **Latent collaborations & barriers** (Q3 No branch), plus stalled action from Q5 — the Forum
  lead list.

**New methodology notes**, all carried into the report tab: *a "No" on action is not an absence of
impact* (read Q3 and Q4 together, never publish the Q3 No rate alone) · *partner origin is
partially captured* (state the base) · *timing is respondent-recalled* (indicative of pattern, not
precise) · plus the existing self-selection note.
