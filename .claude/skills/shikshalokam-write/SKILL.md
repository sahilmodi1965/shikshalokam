---
name: shikshalokam-write
description: Produce content (post, email, blurb, draft, blog, decklet) in ShikshaLokam's voice. Triggers on "draft me X", "write a Y about Z", "give me a LinkedIn / newsletter / fundraising / etc." Reads voice + relevant wiki content, assembles up to 12K tokens, produces review-ready output with sourced citations. Output lands in output/ if brain.yml output_channel != "none", else in chat reply.
---

# shikshalokam-write

## When this fires
- User requests a produced piece of content. Format hints in their wording ("post," "email," "tweet thread," "blurb," "blog," "deck," "fundraising letter").
- Does NOT fire on knowledge questions (→ `shikshalokam-query`) or ingestion (→ `shikshalokam-ingest`).

## What it reads (in order, budgeted per `TOKEN_BUDGET.md` ≤ 12K total)
1. **`CLAUDE.md`** rules (already in context).
2. **SessionStart injection** (`wiki/index.md` + `wiki/_index/topic-summaries.md`, already loaded).
3. **`wiki/voice/styleguide.md`** (≤1,000 tokens — the only skill allowed to read this).
4. **2 best-matched exemplars** from `wiki/voice/exemplars/` (≤1,000 tokens combined). LLM-picked from headers only; do not load all.
5. **Up to 6 `wiki/**.md` files** drilled via wikilink match against the user's brief — this includes any `wiki/sources/research-*.md` that match the brief's angle.
6. **`raw/<YYYY-MM-DD>.md` tail** (last ~500 tokens) for any context the user just dropped.

If the brief is **evidence-anchored** (a research-insight caption, a thought-leadership post, anything that makes a claim that should cite) and no filed `wiki/sources/research-*.md` covers the angle, run **`shikshalokam-research`** first (see that skill) — it verifies external studies, files them, and returns the wikilink to cite. Citing is the default; the user does not have to ask for it.

## What it does
1. **Validate brief.** If the request is ambiguous (length not specified, audience unclear, format genuinely unknown), ask one clarifying question. Cheap question, expensive wrong draft.
2. **Research, if evidence-anchored.** If the brief makes a claim that should cite and no filed `wiki/sources/research-*.md` covers it, run `shikshalokam-research` (verifies external studies against the trust tier, files them to `wiki/sources/research-*.md`, returns the wikilink). Default-on — do not wait to be asked for sources.
3. **Assemble context** per the read order above. If any read pushes over 12K, drop oldest exemplar first, then drop the lowest-relevance wiki article. Voice + styleguide is never dropped.
4. **Produce the draft.** Apply voice rules. Footnote each substantive claim with the `wiki/sources/<slug>` it draws from — every research claim cites a verified `research-*` source, with a verifiability flag only where the brain genuinely could not confirm exact wording.
4. **Write to `output/`** if `brain.yml: output_channel == "github-pages"` or `"drive"`. Filename: `output/<YYYY-MM-DD>-<slug>.md`. Frontmatter declares `_status: draft`, `sources: [[s1]], [[s2]]`, `voice_pulls: [styleguide §rule-name, exemplar/<slug>]`.
5. **Reply to user** with the draft (`chat_shield: true`) or the draft + a path (`chat_shield: false`).
6. **Surface uncited gaps.** If a section needed support and the brain had nothing, end with: *"I had nothing in the brain for [X] — pulled in best general framing. Want me to flag this as a gap to fill?"*

## What it must not do
- Do not write outside `output/`. Never edit `wiki/**.md` directly.
- Do not exceed 12K total prompt assembly.
- Do not silently hallucinate. If a fact isn't in `wiki/`, mark the gap in the draft and offer to flag.
- Do not pull from sibling brains (`cross_brain_wall: true`). Lint will block.
- Do not apply voice rules to content the user explicitly asked be left raw ("just give me the bullet points").

## Output format
- The draft (in the requested format).
- After the draft: `**Sources:** [[s1]] · [[s2]] · ...` + `**Voice notes:** applied <rule-a>, pulled exemplar <slug>` + `**Gaps:** <if any>`.
- LEDGER entry at session end records: prompt brief, draft path (if `output_channel != "none"`), sources touched, voice rules applied, any gaps.
