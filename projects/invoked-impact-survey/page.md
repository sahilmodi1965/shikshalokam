---
project: invoked-impact-survey
title: "InvokED Impact Survey — the MItra questionnaire"
_status: user-validated
last_updated: 2026-08-06
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

**The sheet carries the spec only — no reasoning, no rules, no change history** (Sonal, 2026-07-27,
restated 2026-08-06). People open it without any of the conversation behind it, and rationale reads
as noise. That includes build rules: they govern how the instrument is assembled, so they live here,
not in the tab. The tab is questions, columns and metric rows — nothing else. Everything explaining
*why* lives on this page.

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
- **Substantial action is not the only evidence.** Q4 sets a high bar (collaboration, pilot,
  funding, partnership, decision). Most respondents will answer No to it, and most of the
  ecosystem effect lives below that bar: an idea carried back to a team, an introduction
  brokered between two people, a practice changed, InvokED spoken or written about. **Q5 catches
  all of it, and is asked of everyone regardless of Q4.**
- **Time is the argument.** **Q6** records when the action began and whether it is still live.
  If a meaningful share started months after the edition, the two-day framing collapses on the
  evidence rather than on assertion. That is the most quotable figure the survey can produce, and
  it is a real turn — it is not parked on any surface the instrument does not control.

## The rule that governs the instrument

**Every dashboard and report metric must trace to a question in the questionnaire. If no question
produces it, it is not a metric.** Sonal, 2026-08-06, on finding *Story pipeline* and *Awards
pipeline* on the dashboard with nothing in the conversation behind them.

This is the rule that keeps the sheet honest. A metric sourced from something the instrument does
not ask is a wish with a tile.

## What the 10 turns protect

**8 main questions + 2 probes = 10 turns**, exactly at the cap. Probes live in the follow-up
column against their parent question; they aren't separately numbered, but each spends a turn.
The post-event block (Q4, Q5, Q6) holds 4 of the 10.

| Q | Block | Probes | Turns | Why it earns the space |
|---|---|---|---|---|
| 1 | Profile — role, org, location | — | 1 | Ecosystem diversity. Pre-fillable. |
| 2 | Editions attended | — | 1 | Repeat participation, and the edition cut for every other metric |
| 3 | Perception shift | 1 | 2 | Magnitude *and* substance, in two turns instead of four |
| **4** | **Action & outcome** | **1** | **2** | **The flagship stories and the headline metric** |
| **5** | **Ripple beyond the project + influence on work** | — | **1** | **The breadth layer and the institutional layer, in one turn** |
| **6** | **Timing & continuity of action** | — | **1** | **The proof it isn't a two-day thing** |
| 7 | Continuity | — | 1 | Retention intent + design input for the year-round offer |
| 8 | **Future readiness** | — | 1 | The narrative asset — how leaders define it, and what they're doing |
| | | | **10** | |

### How this set was arrived at (3 and 6 August 2026)

**3 August — Sonal: Q4 and Q6 are almost the same, and Q5 is not needed.** Both held up.

- Old Q4 asked about *"an idea you took back to your team"* and *"a way of working you changed"*;
  old Q6 asked whether it *"shaped how your organisation works — a decision, a programme, an
  approach."* The intended individual-vs-institutional split lived in the design notes, not in the
  wording, so a respondent answering honestly says the same thing twice and starts to feel tested.
- **They became one turn** — now Q5. The open answer carries the ripple; a tap in the same turn
  carries how far it reached institutionally. Both metrics survive: ripple types from the prose,
  org-level influence from the tap.
- That freed two turns, which went to **editions attended** and a **perception baseline**.

**6 August — the baseline came back out.** Applying the rule above to the whole dashboard, four
metrics turned out to have no question behind them: *action timeline*, *still live*, *story
pipeline* and *awards pipeline*. All four were sourced from a "post-close screen" that existed only
as a line in this repo. Timing is the chart that carries the survey's primary objective, so it could
not stay on an imaginary surface. It needed a real turn, and the perception baseline paid for it.

The baseline was the right turn to give back: both ratings were collected inside the same
conversation, so the "delta" was retrospective recall on a matched scale, only marginally stronger
than asking how much someone shifted. Perception is a single self-rated magnitude question again,
and the methodology says so plainly.

**The post-close screen is gone.** Nothing in the instrument depends on it now.

### Q4 — one probe, not three

Q4 (the action question) was carrying 4 turns until 2026-07-27. The three-probe ladder had two
faults. On the **No** branch, probe 1 asked *what's holding it up* and probe 2 asked *what would
make it easier to act* — the same question twice, back to back. And the two branches of any given
probe were unrelated questions sharing a slot number: probe 2's Yes side was attribution, its No
side was barriers. Sonal's call: **if they say Yes or In progress, just ask for the details all
together.**

| | Yes / In progress | No |
|---|---|---|
| Probe | What it is · who it's with · **met at InvokED or already knew them** · what's come of it | What you'd still like to take forward · what's holding it up · anyone you're still in touch with |

**The known cost.** Partner origin — *met at InvokED vs already knew* — is the strongest attribution
claim the report has, and it sits inside a four-part open answer, so a share of respondents will
skip it. There is no backstop tap any more. Report it as a split of the answers that carry it and
**state the base**.

Naming *funding unlocked* in the main question still matters: without the prompt, respondents
rarely volunteer it, and it's the outcome funders find most legible.

### Q5 — the ripple, asked of everyone

*"Beyond a formal project — has anything from InvokED travelled? An idea you took back to your
team, an introduction you made between two people, something you spoke or wrote about, a way of
working or a decision that changed?"* Plus, in the same turn, a tap: *did any of this reach how your
organisation works?*

Asked of every respondent, **including everyone who said No to Q4**. Without this question, a No
makes a respondent look like InvokED did nothing for them. Q5 is where the ecosystem story actually
lives, and it produces three metrics nothing else can: **ripple types**, **reach beyond attendees**,
and **org-level influence**.

If the respondent answers in prose and never touches the tap, record it as unanswered. Never infer
"not at all" from silence.

### Q6 — when, and is it still going

Two taps in one turn: timing (within weeks / a few months later / later in the year / still
unfolding) and state (still going / completed / stalled). Anchored to whatever the respondent
described in Q4 or Q5. **If both were empty, Q6 is skipped and the conversation ends in 9.**
Stalled cases go to the Forum lead list.

## Future readiness — one turn here, a separate survey elsewhere

Q8 asks how the respondent *defines* future readiness and what they're doing about it. It sits last
on purpose: reflective and expansive, so it never competes with the impact data upstream.

What justifies one turn *here* is that this audience is different in kind: these are the people
whose definition shapes how the sector uses the term. Treat the answers as **narrative source
material, not a representative measure.**

**A separate million-voices instrument is not being built for now** (Sonal, 2026-07-27). So Q8 is
the *only* future-readiness data being collected — which makes the framing constraint sharper, not
looser: the report must not imply coverage beyond 150–250 senior leaders. If the listening exercise
is ever picked up, it needs its own audience (teachers, youth, parents, system actors), its own
scale, and grassroots language — MItra's usual persona, not this one.

## Moved out of the instrument entirely

**Story/video willingness · Shikshagraha Awards nomination · best follow-up contact · photo.**
These are operational asks, not measures of what InvokED set in motion. They were cut from the
conversation on 2026-07-27 and parked on a "post-close consent screen"; on 2026-08-06 that screen
was removed, because it was a line in this repo rather than anything MItra does, and because two
dashboard tiles were being built on it.

They are now collected by **the thank-you email that follows the survey** — a normal outward ask,
gated like any other email. **No dashboard tile is built from them.** *Story pipeline* and *Awards
pipeline* have been deleted from `Dashboard_Metrics_Revised`.

**Editions attended** — cut on 2026-07-27, **reinstated as Q2 on 2026-08-03**. Pre-fill from the
registrant record where possible and ask only to confirm.

**Perception baseline** — added as a turn on 2026-08-03, **removed on 2026-08-06** to fund Q6.
Perception shift is a single self-rated magnitude question again.

Full text, branch logic, cut-and-recovery map and the probing rules live in the
`Questions_Revised_10` tab, generated from `questions-10turn.json` in this folder.

## The rules matter as much as the questions

A 10-question list without enforcement drifts straight back to 30:
- **Every metric traces to a question.** If nothing in the questionnaire produces it, no tile.
  (This rule lives here, not in the sheet.)
- Hard cap 10 turns, and the design now uses all 10. Only Q3 and Q4 may probe, once each; the other
  six never do.
- Q5 is asked of every respondent, whatever they answered in Q4.
- Q5's tap and open answer are collected in the same turn. Prose with no tap is recorded as
  unanswered, never inferred as "not at all".
- Q6 is anchored to Q4 or Q5. If both were empty, skip it — the conversation ends in 9.
- Never re-ask what was volunteered.
- Every branch, including every "No", must return something usable.

## Open decision

**Can registration data pre-fill role / org / country / editions?** If yes, Q1 and Q2 collapse to
confirm-taps and up to two turns come free. Best use of them under the current objective, in order:
**buy back the perception baseline** (making shift a matched-scale movement rather than a
self-rating), then **split Q6**, so timing and still-live are asked cleanly rather than as two taps
in one breath.

## Dashboard & report — what the re-source changed

Every metric is pointed at the new numbering. Beyond renumbering:

**Three metrics no longer exist. Don't build tiles for them.**
- **Story pipeline** and **Awards pipeline** — deleted on 2026-08-06. No question produces them;
  they are collected by the thank-you email instead.
- **Perception baseline / measured before-after** — the baseline turn was removed to fund Q6, so
  shift is *self-reported magnitude*, not a measured delta. The published methodology must say so.
- **Network continuity as a single %** — no question is asked of every respondent about staying
  connected, so a percentage would misrepresent the data. Report **named connections as a count**.

**Nothing is orphaned.** Every remaining row on `Dashboard_Metrics_Revised` names the question it
comes from. **Partner origin** is the one to watch: it is real (Q4 probe, Yes branch) but sits
inside a four-part open answer with no backstop, so report it against a stated base.

**The metrics that carry the objective.**
- **Any post-event effect** (Q4 + Q5) — the share of respondents reporting either substantial
  action or a ripple. **This is now the number the report opens with**, not the collaboration
  count, because it is the direct answer to "InvokED is not a two-day event."
- **Action timeline** and **still live** (Q6) — when it started, whether it's ongoing. The chart
  that makes the argument.
- **Ripple types** and **reach beyond attendees** (Q5) — the different ways InvokED helped,
  including everything that never became a project.
- **Org-level influence** (Q5 tap) — how far the ripple reached institutionally, from the same turn.
- **Ripple among non-collaborators** (Q4 = No × Q5) — the guard against misreading a No.
- **InvokED-caused vs InvokED-adjacent** (Q4 probe) — still the most defensible attribution claim,
  reported with its base stated.
- **Latent collaborations & barriers** (Q4 No branch), plus action recorded as stalled in Q6 — the
  Forum lead list.

**New methodology notes**, all carried into the report tab: *a "No" on action is not an absence of
impact* (read Q4 and Q5 together, never publish the Q4 No rate alone) · *partner origin is
partially captured* (state the base) · *perception shift is self-reported*, not a measured
before/after · *timing is respondent-recalled* (indicative of pattern, not precise) · plus the
existing self-selection note.
