---
date: 2026-07-27
person: Sonal Bhasin
project: invoked-impact-survey
---

# The survey stopped measuring only the flagship stories, and started measuring the ripple

Second session on the InvokED Impact Survey today. Sonal named the primary objective out loud for
the first time, and it changed the instrument:

> **InvokED is not a two-day thing. The survey exists to show the actions those two days trigger
> afterwards, and the different ways InvokED has helped the ecosystem.**

## What got made
- **`Questions_Revised_10` rebuilt** — now **8 mains + 2 probes = 10 turns** (was 6 mains + 4
  probes). Q3's three-probe ladder collapsed to one, which paid for two new questions.
- **`Dashboard_Metrics_Revised`** and **`Report_Metrics_Revised`** re-sourced and restructured
  around the objective. The report's opening block is no longer the collaboration count.
- All three regenerated from JSON in `projects/invoked-impact-survey/` via `gs.py sheet-add-tab
  --replace`. Project page rewritten to carry the reasoning.
  → https://docs.google.com/spreadsheets/d/1qMhSkrACZb4zmM2cBWDkyhEma_lDBa6_MkHnSsKU2B8/

## The Q3 fix
Sonal flagged probe 2 as not making sense. It didn't, and the diagnosis was worth having: the
**No branch** asked *"what's holding it up?"* in probe 1 and *"what would make it easier to act on
it?"* in probe 2 — the same question two turns running. Underneath that, each probe's two branches
were unrelated questions sharing a slot number (probe 2 Yes = attribution, probe 2 No = barriers),
which is why it read as a non-sequitur.

Her call: **if they say Yes or In progress, just ask for the details all together.** One probe per
branch now — Yes gets *what · who · met at InvokED or already knew · what's come of it*; No gets
*what you'd take forward · what's blocking · who you're still in touch with*. Two turns freed.

## The two questions those turns bought
The first suggestion I put up — *"what part of InvokED made the difference, a session, a person,
the format?"* — was **wrong, and the objective is what made it wrong**. That question is feedback
about the two days. The survey is about what happened after them. Withdrawn and replaced:

- **Q4, the ripple** — *"Beyond a formal project, has anything from InvokED travelled? An idea you
  took back to your team, an introduction you made between two people, something you spoke or wrote
  about, a way of working you changed?"* Asked of **everyone**, including everyone who said No to
  Q3. This is the "different ways" question.
- **Q5, timing** — when the action began (within weeks / a few months / later in the year / still
  unfolding) and whether it's still live. **This is the literal proof of the thesis**: action that
  began months after the edition is evidence, not assertion, that InvokED isn't two days.

Considered and passed over for Q5: *"did it reach people who were never at InvokED?"* — good
ecosystem-breadth claim, but "not a two-day thing" is a claim about **time**, so time won the turn.
Reach survives as a coded field inside Q4.

## What we learned
- **A high bar makes most of your impact invisible.** Q3 asks about *substantial* action —
  collaboration, pilot, funding, partnership, decision. Most respondents will say No to that, and
  before today a No made them look like InvokED did nothing for them. The ecosystem effect mostly
  lives *below* that bar. One extra question asked of everyone recovers all of it.
- **State the objective and half the design decisions make themselves.** Two sessions of careful
  trimming, and the sentence that reorganised the instrument arrived only when Sonal said it plainly.
  The brain should ask for it first next time, not third.
- **Collapsing a probe has a price — name it and pay it elsewhere.** Partner origin (met at InvokED
  vs already knew) is the strongest attribution claim in the survey. Inside a four-part open answer
  a share of people will skip it, so it's now also a post-close tap, and the methodology states the
  base rather than implying full coverage.

## Next
- **Bot system prompt** — persona, tone, probing rules as real LLM instructions. Still not started;
  the rules live only as sheet columns. This is now the biggest open item.
- **Registration pre-fill** (role / org / country / editions) — still undecided, still load-bearing
  for repeat participation. If a turn does come free, best use is now splitting Q5 rather than
  restoring the perception baseline.
- **Post-close screen** carries more weight than it did: editions tap, partner-origin backstop tap,
  story consent, Awards nomination, contact, photo. If it doesn't ship, three metrics degrade.
