---
date: 2026-05-27
slug: 2026-05-27-story-over-report
source_session: Sonal Bhasin — email feedback on the Masthanaiah portrait + Nagaland NLNF story (forwarded by Sahil)
classification: structural
promoted: landed  # corrected 2026-06-08: wiki/voice/** carries NO Write/Edit deny rule (only docs/** does — verified against .claude/settings.json); the "deny-listed" note above was wrong and the paste sat un-actioned for 12 days
promoted_at: 2026-06-08
promoted_by: Claude (same-session paste, prompted by Sonal's second feedback round — see [[2026-06-08-narrative-throughline-and-fact-grounding]] § Correction to a prior learning)
landed_so_far:
  - "projects/portraits/page.md § Masthanaiah portrait — full body rewrite (narrative arc) + gaps-to-fill section"
  - "projects/nagaland-coffee-book/page.md § GMS Jalukie story — full body rewrite (empathy + flow) + gaps-to-fill section"
  - "docs/projects/portraits.html + docs/projects/nagaland-coffee-book.html — HTML mirrors regenerated"
  - "projects/portraits/chatlog.md + projects/nagaland-coffee-book/chatlog.md — feedback session appended"
  - "wiki/voice/styleguide.md § Story over report — pasted in 2026-06-08, twelve days late, alongside the four-move extension from [[2026-06-08-narrative-throughline-and-fact-grounding]]"
related:
  - "[[2026-05-26-movement-frame-people-actors]] (companion voice rule)"
  - "[[2026-05-26-content-from-brain-directed-run]] (the session whose drafts this feedback corrects)"
  - "[[2026-05-26-five-decisions-binding]] (workflow that enables this loop)"
---

# Learning — 2026-05-27 — Story over report

## What Sonal said (verbatim, from email)

On the Masthanaiah portrait:

> *"This line doesn't make sense — 'Forty years in Andhra Pradesh's school education system followed.'"*
>
> *"'On the basis of strength enrollment of the students, the other facilities will come.' Doesn't sound right. Rephrase."*
>
> *"'he reformed the morning-afternoon shift system' doesn't sound right. Didn't understand what is meant by this."*
>
> *"Simplify — 'of pull-driven postings'."*
>
> *"Overall — The story is not impactful; his achievements are clubbed and listed altogether. It doesn't read like a story but reporting. The story needs to have a flow from his being a dropout to a Director, CSE Andhra Pradesh. The story should celebrate his commitment, challenges and how things changed for him. What did he do to improve the learning experiences of students and support teachers? He should emerge as a champion / an inspiring leader."*
>
> *"In case there are gaps in the story or missing information, we can get it from him. Let's ask the AI to highlight gaps that would help create this portrait."*

On the Nagaland NLNF story:

> *"'This is the school that, in 2026, won its way into the fifteen.' This needs more context."*
>
> *"The fest asked them — sounds more demanding, make it the fest encouraged instead."*
>
> *"The challenges paragraph need more empathy & context to hook readers."*
>
> *"Overall, the story currently has too many breaks with en dashes and commas and does not read like a story but like reporting. It has to sound human, evoke emotions, enhance relatability, etc."*

## The rule

**Story over report. When drafting any narrative piece — a portrait, a coffee-book story, a long
blog — write so the reader feels before they conclude.**

Five moves, in this order:

1. **Build an arc, don't list achievements.** Beginning → tension → turn → cost → outcome → close.
   The reader should be able to feel which paragraph is the *middle* and which is the *turn*. If
   every paragraph reads the same, it's reporting.
2. **Slow at the human moments.** The borrowed television. The lamp made from a tonic-syrup bottle.
   The teacher who walked two kilometres to school every day. Give them their own paragraph. Don't
   bury them inside a sentence about something else.
3. **Fewer em-dashes; shorter sentences alongside longer ones.** Em-dashes are the punctuation of
   reporting. One per paragraph in narrative, max. Rhythm beats density.
4. **Show the cost.** What did this leader give up? What was the hardest moment? When did they
   doubt themselves? A portrait without cost is a CV.
5. **Let the reader feel the leader as a person, not a list.** First-generation learner. Daily-wage
   parents. Forty years in service. Wife. Children. What they read in retirement. The human texture
   the institutional vocabulary skips.

**What to avoid:**

- *"X happened. He did Y. He delivered Z. He also did W."* — flat reporting cadence.
- Stacking achievements in one paragraph because they all happened in the same chapter — they each
  deserve their own beat.
- Institutional vocabulary inside human moments (*"originated · delivered · cascaded"* in the
  origin-story section flattens it).
- Em-dash overdose (>2 per paragraph = reporting).
- *"The Fest asked them"* / *"The school was tasked with"* — demanding voice. Prefer
  *"The Fest encouraged them"* / *"The school chose to."*
- Numbers without a human consequence — *"935 schools"* alone is reporting; *"935 schools — second
  only to UP — across his five and a half years"* is still reporting; *"935 schools, one principal
  at a time"* starts to land.

## Companion rule — surface gaps by default

**For any narrative piece, name what's missing.** Don't silently smooth over thin source material.
If the portrait would be stronger with three more concrete details, list them as *gaps to fill*
inside the page — so the team can decide whether to chase them before publishing. Sonal asked
for this explicitly: *"Let's ask the AI to highlight gaps that would help create this portrait."*

The pattern: a *Gaps that would lift this story* section at the bottom of every narrative piece,
phrased as questions the source-person or interviewer could answer. Specific, askable, scoped to
this piece.

## Paste-ready snippet — for `wiki/voice/styleguide.md` (Sahil's hand-edit)

Insert as a new section after `## Shikshagraha mentions — movement as frame, people as actors`,
before `## Gaps for user validation`:

```markdown
## Story over report — narrative voice for portraits, coffee-book stories, long blogs

Added 2026-05-27 from learning `learnings/2026-05-27-story-over-report.md` (Sonal's feedback
on the first Masthanaiah portrait + Nagaland NLNF story). **Binding for any narrative piece
— portraits, coffee-book stories, long blogs, donor letters.**

**The rule.** Write so the reader feels before they conclude. Five moves:

1. **Build an arc.** Beginning → tension → turn → cost → outcome → close. If every paragraph
   feels the same, it's reporting. The middle should feel different from the turn.
2. **Slow at human moments.** The borrowed television. The tonic-syrup-bottle lamp. The
   teacher who walked two kilometres every day. Give the moment its own paragraph. Don't
   bury it inside a sentence about something else.
3. **Fewer em-dashes. Vary sentence length.** Em-dashes are the punctuation of reporting.
   One per paragraph in narrative, max. Short sentences make rhythm; long sentences make
   thought. Mix them.
4. **Show the cost.** What did this leader give up? When did they doubt themselves? What
   was the hardest moment? A portrait without cost is a CV.
5. **Let the leader feel like a person.** Family. Roots. What they read now. The texture
   institutional vocabulary skips.

**Never** in a narrative piece:

- *"X happened. He did Y. He delivered Z."* — flat reporting cadence; collapse into an arc.
- Stacking three achievements in one paragraph because they fall in the same chapter — each
  beat deserves its own paragraph.
- Institutional verbs (*"originated · delivered · cascaded"*) inside human moments.
- "The X asked them" / "The school was tasked" — demanding voice. Prefer "encouraged" /
  "chose to" / "stepped up to."
- Numbers without a human consequence behind them.

**Always for narrative pieces:**

- A **Gaps that would lift this story** section at the bottom, phrased as questions the
  source-person could answer. Surface what's missing — don't silently smooth over thin
  material. (Sonal: *"Let's ask the AI to highlight gaps that would help create this portrait."*)
```

### Suggested commit message

```
voice: story over report — promote 2026-05-27 learning to styleguide

Sonal's feedback on the first Masthanaiah portrait + Nagaland NLNF story
surfaced the same structural issue in both: reads like reporting, not story.
Added § Story over report as the binding rule for narrative voice — five
moves (arc, slow at human moments, fewer em-dashes, show the cost, let
the leader feel like a person) plus a default to surface gaps inline.

Cites: learnings/2026-05-27-story-over-report.md
```

## Where this lands in practice

- **Today's recompile** — both pieces rewritten in the new voice, pushed live, Sonal reviews
  the same URLs.
- **Future drafts** — every portrait / coffee-book story / long blog drafts to this rule from
  the next session forward.
- **Gap-surfacing as default** — every narrative piece carries a *Gaps that would lift this
  story* section. The brain names what's missing without being asked.
