---
project: invoked-impact-survey
title: "InvokED Impact Survey — the MItra questionnaire"
_status: user-validated
last_updated: 2026-08-03
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
- **Substantial action is not the only evidence.** Q5 sets a high bar (collaboration, pilot,
  funding, partnership, decision). Most respondents will answer No to it, and most of the
  ecosystem effect lives below that bar: an idea carried back to a team, an introduction
  brokered between two people, a practice changed, InvokED spoken or written about. **Q6 catches
  all of it, and is asked of everyone regardless of Q5.**
- **Time is the argument.** When the action began and whether it is still live is the most
  quotable figure the survey can produce. It is no longer a conversational turn — since
  2026-08-03 it sits on the **post-close screen** as two taps, which costs nothing against the
  cap. The argument survives; the coverage now depends on that screen shipping.

## What the 10 turns protect

**8 main questions + 2 probes = 10 turns**, exactly at the cap. Probes live in the follow-up
column against their parent question; they aren't separately numbered, but each spends a turn.

| Q | Block | Probes | Turns | Why it earns the space |
|---|---|---|---|---|
| 1 | Profile — role, org, location | — | 1 | Ecosystem diversity. Pre-fillable. |
| 2 | Editions attended | — | 1 | Repeat participation, and the edition cut for every other metric |
| 3 | Perception baseline — before their first InvokED | — | 1 | The "before" half of a matched pair |
| 4 | Perception today, same scale | 1 | 2 | The delta against Q3, plus the substance behind it |
| **5** | **Action & outcome** | **1** | **2** | **The flagship stories and the headline metric** |
| **6** | **Ripple beyond the project + influence on work** | — | **1** | **The breadth layer and the institutional layer, in one turn** |
| 7 | Continuity | — | 1 | Retention intent + design input for the year-round offer |
| 8 | **Future readiness** | — | 1 | The narrative asset — how leaders define it, and what they're doing |
| | | | **10** | |

### The 2026-08-03 revision (Sonal)

Sonal's read of the previous set: **Q4 and Q6 were almost the same question, and Q5 was not
needed.** Both hold up.

- **Q4 and Q6 overlapped in the wording, not just in feel.** Old Q4 asked about *"an idea you took
  back to your team"* and *"a way of working you changed"*; old Q6 asked whether it *"shaped how
  your organisation works — a decision, a programme, an approach."* The intended split was
  individual ripple vs institutional change, but a respondent answering honestly says the same
  thing twice and starts to feel tested.
- **They are now one turn.** The open answer carries the ripple; a tap in the same turn carries how
  far it reached institutionally (not at all / somewhat / significantly). Both metrics survive:
  ripple types from the prose, org-level influence from the tap.
- **Old Q5 (timing and continuity) left the conversation.** Its two taps moved to the post-close
  screen, which costs no turn. The timeline chart survives; what changes is coverage, which now
  depends on the post-close screen shipping and on respondents completing it. The report must
  state the base.

That freed two turns. Both were spent, per Sonal on 2026-08-03:

- **Editions attended came back as Q2.** It had been cut on 2026-07-27 to fund the future-readiness
  turn, leaving repeat participation orphaned and the aggregate report with no edition-level
  segmentation at all. It is a metric, not a nicety, and pre-fill was never guaranteed.
- **A perception baseline came in as Q3.** Q4 now asks for a rating on the *same* three-point scale,
  so shift is a movement between two matched points rather than a single self-rated magnitude.

**The honest limit on the baseline:** both ratings are collected in the same conversation, so this
is retrospective recall on a matched scale, not a measured before/after. It is a real improvement on
"how much did you shift", and it is still not a pre-post design. The methodology note says so.

**One cost worth naming.** The post-event block now holds 3 of the 10 turns rather than 4, while
perception holds 3. Given the stated objective — evidence what the two days set in motion — that is
the tightest part of the trade. If completion data later shows the interview running long, the
baseline is the first turn to give back.

### Q5 — one probe, not three

Q5 (the action question, numbered Q3 before this revision) was carrying 4 turns until 2026-07-27.
The three-probe ladder had two faults. On the **No** branch, probe 1 asked *what's holding it up*
and probe 2 asked *what would make it easier to act* — the same question twice, back to back. And
the two branches of any given probe were unrelated questions sharing a slot number: probe 2's Yes
side was attribution, its No side was barriers. Sonal's call: **if they say Yes or In progress, just
ask for the details all together.**

| | Yes / In progress | No |
|---|---|---|
| Probe | What it is · who it's with · **met at InvokED or already knew them** · what's come of it | What you'd still like to take forward · what's holding it up · anyone you're still in touch with |

**The cost, and the fix.** Partner origin — *met at InvokED vs already knew* — is the strongest
attribution claim the report has. Buried inside a four-part open answer, a share of respondents
will skip it. It is therefore **also a tap on the post-close screen**, which costs no turn. The
report states the base rather than implying full coverage.

Naming *funding unlocked* in the main question still matters: without the prompt, respondents
rarely volunteer it, and it's the outcome funders find most legible.

### Q6 — the ripple, asked of everyone

*"Beyond a formal project — has anything from InvokED travelled? An idea you took back to your
team, an introduction you made between two people, something you spoke or wrote about, a way of
working or a decision that changed?"* Plus, in the same turn, a tap: *did any of this reach how your
organisation works?*

Asked of every respondent, **including everyone who said No to Q5**. Without this question, a No
makes a respondent look like InvokED did nothing for them. Q6 is where the ecosystem story actually
lives, and it produces three metrics that nothing else can: **ripple types**, **reach beyond
attendees** (things that reached people who were never at InvokED), and **org-level influence**.

If the respondent answers in prose and never touches the tap, record it as unanswered. Never infer
"not at all" from silence.

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

## Moved out of the conversation (nothing lost)

- **Timing & continuity of action** — a conversational turn until 2026-08-03, now two taps on the
  post-close screen (when it began · still going / completed / stalled). Anchored to whatever the
  respondent described in Q5 or Q6; if both were empty, the taps are skipped. Stalled cases still
  go to the Forum lead list. **Report the base** — this is no longer collected from everyone.
- **Editions attended** — cut on 2026-07-27, **reinstated as Q2 on 2026-08-03** with a turn freed
  by the Q4/Q6 merge. Pre-fill from the registrant record where possible and ask only to confirm.
- **Story/video willingness · Awards nomination · follow-up contact** — cut as no longer aligned,
  but the report spec still expects all three. They move to the **post-close consent screen**
  alongside the optional photo upload. A post-close step isn't a turn, so this costs nothing.

Full text, branch logic, cut-and-recovery map and the probing rules live in the
`Questions_Revised_10` tab, generated from `questions-10turn.json` in this folder.

## The rules matter as much as the questions

A 10-question list without enforcement drifts straight back to 30:
- Hard cap 10 turns, and the design now uses all 10. Only Q4 and Q5 may probe, once each; the other
  six never do.
- Q3 and Q4 share one three-point scale and are read as a pair. Ask Q3 first, and never show its
  answer back while asking Q4.
- Q6 is asked of every respondent, whatever they answered in Q5.
- Q6's tap and open answer are collected in the same turn. Prose with no tap is recorded as
  unanswered, never inferred as "not at all".
- Never re-ask what was volunteered.
- Every branch, including every "No", must return something usable.

## Open decision

**Can registration data pre-fill role / org / country / editions?** Less load-bearing than it was —
editions-attended is a real turn again — but still worth having: pre-fill collapses Q1 and Q2 to
confirm-taps and frees up to two turns. Best use of freed turns under the current objective:
**bring timing and still-live back into the conversation**, since post-close coverage is weaker than
in-conversation coverage.

**Does the post-close screen actually ship?** Now carrying more than before: timing, durability,
partner-origin backstop, story/video willingness, awards, follow-up contact, photo. If it slips,
the timeline chart and the durability metric go with it. That is the single biggest build risk in
the instrument.

## Dashboard & report — what the re-source changed

Every metric is pointed at the new numbering. Beyond renumbering:

**One metric no longer exists. Don't build a tile for it.**
- **Network continuity as a single %** — no question is asked of every respondent about staying
  connected, so a percentage would misrepresent the data. Report **named connections as a count**.

**Two metrics changed shape on 2026-08-03.**
- **Perception shift** is now a **movement between two matched three-point scales** (Q3 → Q4), not a
  single self-rated magnitude. Report % who moved one step, % who moved two, % unchanged. Both
  ratings are still collected in the same conversation, so the methodology must say it is
  retrospective recall on a matched scale, not a measured pre-post.
- **Action timeline** and **still live** now come from **post-close taps**, not a turn. Chart them
  as before, and state the base.

**One metric is no longer orphaned.**
- **Repeat participation** — editions-attended is Q2 again, so this and edition-level segmentation
  are complete rather than dependent on pre-fill.

**The metrics that carry the objective.**
- **Any post-event effect** (Q5 + Q6) — the share of respondents reporting either substantial
  action or a ripple. **This is now the number the report opens with**, not the collaboration
  count, because it is the direct answer to "InvokED is not a two-day event."
- **Action timeline** and **still live** (post-close taps) — when it started, whether it's ongoing.
  The chart that makes the argument, now with a stated base.
- **Ripple types** and **reach beyond attendees** (Q6) — the different ways InvokED helped,
  including everything that never became a project.
- **Org-level influence** (Q6 tap) — how far the ripple reached institutionally, from the same turn.
- **Perception shift as a delta** (Q3 → Q4) — movement between two matched scales.
- **Ripple among non-collaborators** (Q5 = No × Q6) — the guard against misreading a No.
- **InvokED-caused vs InvokED-adjacent** (Q5 probe + post-close tap) — still the most defensible
  attribution claim, now reported with its base stated.
- **Latent collaborations & barriers** (Q5 No branch), plus stalled action from the post-close
  taps — the Forum lead list.

**New methodology notes**, all carried into the report tab: *a "No" on action is not an absence of
impact* (read Q5 and Q6 together, never publish the Q5 No rate alone) · *partner origin is
partially captured* (state the base) · *perception shift is a retrospective matched pair*, not a
measured pre-post · *timing is respondent-recalled and partially captured*, since it now sits on
the post-close screen · plus the existing self-selection note.
