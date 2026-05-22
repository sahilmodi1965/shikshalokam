---
user_words: |
  this was a result of prompt Research studies, surveys and repports that
  strenghten the need for any of the SL aligned messaging- collective action,
  importance of agency for education leaders. Use those studies to create byte
  sized informative posts. share by Sonal, what we wanted out of this was also
  amn agent that would do research of external studies adn trustable surveyr
  sand reliable sources which strentghed the messaging of of Sl and need for
  focusing oneduation leadership and power of collective action in solving ,
  challneg of education equity. (take this as a brain feedack) so the later
  promts automatically cites research as welkl and recompile, ideally in the
  project pages, we want to see every draft an not just weekly but a date wise
  update of how we are adding tihsi content
classification: structural
target_files:
  - .claude/skills/shikshalokam-write/   # auto-research + auto-cite step
  - .claude/agents/  OR  new skill       # the research capability itself — Sahil designs
  - docs/projects/*.html                 # date-wise activity log section
  - projects/README.md                   # per-session contract: log every draft, dated
  - CLAUDE.md                            # per-session contract clause (maintainer applies)
suggested_change: |
  Four linked asks, all about how research-anchored content gets made and shown:

  1. RESEARCH CAPABILITY. Sonal wants a standing capability that goes and
     researches external studies, trustable surveys, and reliable sources that
     strengthen SL-aligned messaging — specifically education leadership, the
     power of collective action, and the challenge of education equity. Today
     this happens by hand (the 19 May captions cited WEF / OECD / ASER because
     Claude reached for them; nothing made it do so).

  2. AUTO-CITE BY DEFAULT. Future content prompts should run that research and
     attach citations automatically — Sonal should not have to ask for sources.
     "the later prompts automatically cite research."

  3. RECOMPILE / BAKE IN. The research found should compound into the brain as
     reusable evidence (wiki/sources/ research files), not be re-searched fresh
     each session — so every later draft pulls from a growing, sourced library.

  4. DATE-WISE DRAFT LOG. The project pages should show every draft as it is
     added, on a dated basis — "not just weekly but a date wise update of how
     we are adding this content." Today captions.html says variants "archive
     weekly"; Sonal wants a running, dated activity record visible on the page.
promoted: true
promoted_at: 2026-05-21
promoted_commit: "same-session maintainer build (Sahil, 2026-05-21) — see LEDGER § 2026-05-21 research-pipeline-build"
created: 2026-05-21
---

## Context

Sonal was shown the three Tuesday research-insight caption variants drafted on
19 May (the first real test of the project-page architecture). Instead of
copying a title back to approve one, she replied with process feedback and
explicitly tagged it: *"(take this as a brain feedback)."*

The three variants already cite real research — WEF *The Future is Collective*
(2025), OECD school-leadership research, Pratham's ASER. So the brain can do
this. Sonal's point is that it happened **because Claude chose to**, not because
the brain is *built* to. She wants the research-and-cite step to be a standing
part of how content is made, and she wants the cadence of new drafts to be
**visible and dated** on the project pages, not summarised weekly.

This is not a correction of a draft — no draft needs regenerating. It is a
correction of how the brain is shaped. Hence structural, per INTENT principle 6.

## Structural or one-off?

**Structural**, and the user said so outright. It changes:
- how the `shikshalokam-write` skill behaves (a research + auto-cite step),
- whether the brain has a research capability at all (new agent or skill),
- how `wiki/sources/` grows (a research-evidence library that compounds),
- how the project pages present work (a dated activity log).

None of that is fixable in one draft. All of it needs maintainer-built changes.

## Promotion path

This is **bigger than a weekly-review wiki edit** — the weekly reviewer (Sahid)
promotes learnings into `wiki/**` content, but three of the four parts here are
*capability builds*, which live on Sahil's monthly maintainer pass (CLAUDE.md
"Heavy ops live on maintainer accounts"). The weekly review's job is to confirm
priority and hand off; Sahil's job is to build. Concrete steps:

**1 — Research capability (Sahil, monthly).**
Decide the form: a `research` sub-agent the write skill invokes, or a new
`shikshalokam-research` skill. It should take a messaging angle (education
leadership / collective action / education equity) and return sourced findings
from a defined trust tier. Candidate reliable sources, some already surfaced in
the 19 May captions "Notes for next iteration" and LEDGER entry: OECD, World
Bank, UNESCO, WEF, Pratham/ASER, NCERT, Azim Premji University, J-PAL South Asia
(Karthik Muralidharan), NITI Aayog, NAS, IDR. The trust bar is Sonal's phrase —
*"trustable surveys and reliable sources"* — name it explicitly in the skill so
the brain never cites a weak source.

**2 — Auto-cite in `shikshalokam-write`.**
Add a step: when the ask is research-anchored content, run the research
capability first and attach a `Sources:` block with full citation + a
verifiability flag where the citation is paraphrased (the 19 May OECD variant
already did this manually — "Sonal to confirm exact citation before posting").
Make it default-on so Sonal need not ask.

**3 — Compound into `wiki/sources/`.**
Each verified study becomes a `wiki/sources/research-<slug>.md` file,
`_status: research-seeded`, with the canonical claim, the citation, and the
SL-messaging angle it supports. Later drafts cite the wiki file, not a fresh web
search. This is the "recompile" Sonal asked for — research baked in, not
re-fetched.

**4 — Date-wise draft log on project pages.**
Add a dated activity-log section to each `docs/projects/<slug>.html` (and/or a
roll-up on `docs/projects/index.html`): every session that adds or revises a
draft appends a dated row — *date · what was added · status*. Update
`projects/README.md` per-session contract to require the log append. This
supersedes the current "variants archive weekly" copy on `captions.html` — keep
the dated record even after a variant archives.

**CLAUDE.md clause (Sahil applies — file is maintainer deny-listed).**
Add to the per-session contract: research-anchored content runs the research
step and cites by default; every project-page draft change appends a dated log
entry.

## Interim behaviour (until built)

Sessions should keep doing by hand what the 19 May captions did — reach for a
real study and cite it with a verifiability flag. The gap Sonal named is that
it is not yet *guaranteed*. Do not treat this learning as a licence to build the
agent mid-session (CLAUDE.md rule 5, no ghost features; rule 10, stop and ask
before new conventions) — it waits for Sahil's maintainer pass.

## Cross-references

- Pairs with [[2026-05-19-project-page-architecture]] — the date-wise log is a
  new section on the project pages that learning stood up.
- The captions page already lists research anchors to pull in its "Notes for
  next iteration" block, and the 19 May LEDGER entry flagged the same names for
  a maintainer enrichment pass — this learning makes that pass a defined build.
- Voice rule unaffected — `wiki/voice/**` is not a target here.

## Promoted — what was built (2026-05-21, same-session maintainer build)

Sahil, on the call with Sonal, directed the build in the same session this
learning was captured ("fix all the feedbacks and share a new post after all
structural changes are made"). Not a weekly-review promotion — a maintainer
build, which the plan allows. All four parts landed:

1. **Research capability** — new skill `.claude/skills/shikshalokam-research/`.
   Defines the trust tier (Tier 1 cite directly · Tier 2 cite with attribution ·
   Tier 3 never cite as evidence), the verify-then-file flow, and how it runs
   both standalone and as a step inside `shikshalokam-write`.
2. **Auto-cite by default** — `.claude/skills/shikshalokam-write/SKILL.md` gained
   a research step (step 2) and a strengthened citation requirement; the read
   order now pulls `wiki/sources/research-*.md`.
3. **Compounded into the brain** — first research pass filed three verified
   studies as `wiki/sources/research-*.md`: [[research-leithwood-leadership-2004]],
   [[research-aser-2024]], [[research-wef-future-is-collective-2025]]. Registered
   in `wiki/index.md`, `wiki/sources/SOURCES.md`, `wiki/log.md`.
4. **Date-wise draft log** — `## Content log` section added to
   `projects/captions/page.md` and mirrored to `docs/projects/captions.html`
   (new `.logtable` style); `projects/README.md` per-session contract now
   requires the dated log on every project page (step 3b, cross-cutting rules
   6–7).

Demonstrated end-to-end: captions Variant 2's unconfirmed OECD citation was
corrected to the verified Wallace Foundation source, and a new Variant 4 ("The
recovery no one's talking about.", ASER 2024) was drafted fully through the new
pipeline and logged dated.

## CLAUDE.md amendment (Sahil applies by hand — file is maintainer deny-listed)

`CLAUDE.md` is `deny`-listed for Write/Edit in `.claude/settings.json`, so this
clause is a patch for Sahil to paste in. Add to **Behavior rules (binding)** as
the next number (note: rule 11 is also pending from
[[2026-05-19-project-page-architecture]]):

```markdown
12. **Evidence is researched, not improvised.** Research-anchored content
    (research-insight captions, thought-leadership, any claim that should cite)
    runs through `shikshalokam-research` and carries a verified citation by
    default — the daily user never has to ask for sources. Verified studies
    compound into `wiki/sources/research-*.md` so later drafts cite from the
    brain. Project-page drafts append a dated row to the page's `## Content log`.
```

No other CLAUDE.md change is required — the per-session project-page contract
already lives in `projects/README.md`, which was updated this session.
