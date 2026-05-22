---
name: shikshalokam-research
description: Research external studies, surveys, and reports that strengthen SL-aligned messaging — education leadership, the power of collective action, education equity. Verifies each source against a trust tier, then compounds it into wiki/sources/research-*.md so later drafts cite from the brain, not a fresh search. Runs standalone ("research studies on X") OR as the first step of shikshalokam-write for any evidence-anchored content. Heavy ops — runs on the maintainer plan.
---

# shikshalokam-research

The brain's evidence-finder. ShikshaLokam's messaging is strongest when it stands
on real, citable research. This skill goes and finds that research, verifies it,
and files it so the brain accumulates a sourced evidence library instead of
re-searching every time.

Created 2026-05-21 from `learnings/2026-05-21-research-citation-and-datewise-log.md`
(Sonal's brain feedback: *"an agent that would do research of external studies
and trustable surveys and reliable sources."*)

## When this fires

- **Standalone** — "research studies on X", "find surveys that back Y", "what's
  the evidence for Z". Does a pass, files what it verifies, reports back.
- **As a step inside `shikshalokam-write`** — automatically, before drafting any
  evidence-anchored content (research-insight captions, thought-leadership posts,
  anything that should cite). The write skill does not ask permission; citing is
  the default. See that skill's read order.
- Does NOT fire for content that is purely narrative/voice (a welcome post, an
  event teaser with no claim to support).

## The trust tier (binding — never cite below it)

| Tier | What | How to cite |
|---|---|---|
| **Tier 1 — cite directly** | Peer-reviewed studies · multilateral bodies (OECD, World Bank, UNESCO, UNICEF) · government statistics (NAS, NCERT, NITI Aayog, MoE) · large established surveys (Pratham ASER) · WEF / Schwab Foundation reports · foundation-commissioned research reviews (e.g. Wallace Foundation) | Full citation: author(s)/institution, year, title, publisher. |
| **Tier 2 — cite with named attribution + date, verify currency** | Reputable think-tanks / sector media with named authorship — IDR, Brookings, Azim Premji University working papers, J-PAL / 3ie evaluations, Central Square Foundation | Name the author and the year in-text; flag if older than ~7 years. |
| **Tier 3 — never cite as evidence** | News aggregators, blogs, advocacy pages, undated or anonymous web content, AI summaries, anything paywalled-and-unread | Do not cite. May be used only to *find* a Tier 1/2 primary source, then cite that. |

## What it does

1. **Take the messaging angle.** One of: education leadership / agency · the power
   of collective action · the challenge of education equity — or whatever the
   brief implies. Note the specific claim the content needs to support.
2. **Search the trust tiers.** Use WebSearch / WebFetch. Prefer the primary
   source over anyone reporting on it — chase a news mention back to the study.
3. **Verify each candidate.** Confirm: it is real and correctly attributed; the
   finding actually says what the draft needs; it is current enough; the numbers
   are quoted exactly. An unverifiable source is dropped, not softened.
4. **Compound into the brain.** For each verified study, write or update
   `wiki/sources/research-<slug>.md` — full citation, the canonical claim(s)
   verbatim, the SL-messaging angle it supports, the URL, a `verified:` date,
   `_status: research-seeded`. Append a line to `wiki/sources/SOURCES.md` and
   register it in `wiki/index.md` § Sources.
5. **Return findings.** Exact citation(s) + the `[[research-<slug>]]` wikilink
   the draft should cite. If invoked by `shikshalokam-write`, hand these to the
   draft step. If standalone, report them and stop.

## Recompile — cite from the brain, not the web

Once a study is in `wiki/sources/research-*.md`, later drafts cite the wiki file.
A draft re-searches the web only when (a) no filed source covers the angle, or
(b) a filed source is stale. This is the "recompile" the feedback asked for —
research accumulates; it is not re-fetched every session.

## What it must not do

- Never cite a Tier 3 source as evidence.
- Never invent, paraphrase-into-error, or overstate a finding. One study is "a
  study found" — not "research shows". Quote numbers exactly.
- Never cite a source it could not verify. Drop it; flag the gap.
- Never write to `wiki/voice/**`, `wiki/concepts/**`, or `wiki/synthesis/**` —
  this skill owns `wiki/sources/research-*.md` only.
- Never pull from a sibling brain (`cross_brain_wall: true`).

## Output format

- **Standalone:** the verified findings, each with full citation + `[[wikilink]]`,
  plus any gap it could not fill. Then a LEDGER entry.
- **Inside `shikshalokam-write`:** the findings pass silently to the draft step;
  the draft's `Sources:` block carries them. One LEDGER entry covers the session.
