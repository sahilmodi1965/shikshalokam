---
date: 2026-08-03
person: Sonal Bhasin
project: invoked-impact-survey
---

# MItra survey — Q4/Q6 merged, Q5 off the conversation, two turns respent

## What got made
Revised the InvokED Impact Survey questionnaire (v3) and re-sourced both metrics tabs.
Regenerated `Questions_Revised_10`, `Dashboard_Metrics_Revised` and `Report_Metrics_Revised`
in Sonal's working template from the JSON in this folder.

## What we learned
- **Sonal's read was right on both counts.** Old Q4 asked about "an idea you took back to your
  team" and "a way of working you changed"; old Q6 asked whether it "shaped how your organisation
  works". The intended individual-vs-institutional split existed in the design notes but not in the
  wording, so a respondent answers the same thing twice.
- **The merge keeps both metrics.** One turn now carries an open answer (ripple types, reach beyond
  attendees) plus a tap in the same turn (org-level influence). Prose with no tap is recorded as
  unanswered, never inferred as "not at all".
- **Old Q5 (timing, still-live) moved to the post-close screen** as two taps. The timeline chart
  survives at zero turn cost, but coverage now depends on that screen shipping and on respondents
  completing it. That is now the biggest single build risk in the instrument, and the report has to
  state the base.
- **Both freed turns were spent** (Sonal's call): editions attended came back as Q2, un-orphaning
  repeat participation and edition-level segmentation; a perception baseline came in as Q3, so shift
  is a movement between two matched three-point scales rather than a self-rated magnitude.
- **Honest limit recorded:** both perception ratings are collected in the same conversation, so the
  delta is retrospective recall on a matched scale, not a measured pre-post. New methodology note
  says exactly that.

## What to improve next
- The post-event block now holds 3 of 10 turns while perception holds 3. Against the stated
  objective (evidence what the two days set in motion), that is the tightest part of the trade.
  If completion data shows the interview running long, the baseline is the first turn to give back.
- Open: does the post-close screen actually ship? It now carries timing, durability, partner-origin
  backstop, story/video willingness, awards, follow-up contact and photo.
