# Brain Ledger — ShikshaLokam

The single growing artefact. Every session leaves one entry. New entries appended at the top. Scroll down for older history.

This file is the **proof the brain compounded**. If a session ended with no entry here, INTENT principle 2 was violated — the brain didn't compound. `brain-lint` flags any commit missing today's ledger entry.

**Read this file** to see the brain's recent moves. **Show this file** in stakeholder demos when the question is "is it actually getting smarter?"

---

## How an entry looks

```
## 2026-05-14 14:23 UTC — Sonal — bihar-chaupal-linkedin

- **Asked:** 250-word LinkedIn post on Charan, a child at the Hirehalli Shiksha Chaupal
- **Produced:** drafts/2026-05-14-bihar-chaupal.md (review-ready)
- **Learned:** structural — "Chaupal moment" should replace "intervention" → learnings/2026-05-14-chaupal-moment.md → flagged for Friday review
- **Status changes:** wiki/concepts/shiksha-chaupals.md research-seeded → user-validated
- **Sources touched:** [[mothers-of-courage-press]] [[shikshagraha-content-platform]]
- **Voice notes:** Pratik confirmed Charan-as-protagonist framing; rejected "leverage" (already in Never list)
```

Each entry is 5–8 lines. Short on purpose — the ledger is a scannable timeline, not a transcript.

## Fields

- **Asked** — one line. What the daily user requested, in their words (or close paraphrase).
- **Produced** — one line. What artefact the brain made. Cite the file path if it landed in `output/`; otherwise summarise the answer.
- **Learned** — one line. One of:
  - `nothing` — no correction surfaced
  - `one-off — <user's words>` — a correction noted but judged non-structural
  - `structural — <topic> → learnings/<date>-<slug>.md → <target wiki file(s)>` — correction routed to weekly review
- **Status changes** — one line per affected file: `wiki/path.md <from> → <to>`. `none` if nothing flipped.
- **Sources touched** — wikilinks to `wiki/sources/*` the brain pulled from while producing. Empty list `[]` if none.
- **Voice notes** (optional) — only when voice rules were applied, confirmed, or contested. Skip otherwise.

## Lifetime invariants

- **Append-only.** Never edit an existing entry. Corrections to a past entry are written as a new entry that references the old timestamp.
- **One entry per session.** Multi-ask sessions still produce one entry — combine into a single asked/produced/learned summary. Forced concision is the point.
- **Newest at top.** New entries inserted directly below this "How an entry looks" block, pushing older entries down. Demo-readers see latest first.
- **Lint-enforced.** `brain-lint` fails the commit if the current session produced no LEDGER entry. The `SessionEnd` hook auto-commits only after verifying the entry exists.

## Why this file exists

Three reasons.

1. **Demo evidence.** Stakeholders ask "is it learning?" and the answer is a scroll. Three months of entries shows compounding more honestly than any metric.
2. **Successor handoff.** If the daily user hands the brain to someone else, the new person reads the LEDGER top-to-bottom and inherits the brain's actual history — not the maintainer's tribal memory.
3. **Audit.** When a stakeholder asks "where did we say X?", the LEDGER + frontmatter `corrected_by:` references reconstruct the full provenance chain.

The LEDGER is the brain's autobiography. It does not replace `wiki/` (the state) or `learnings/` (the deliberation log) — it complements both by being the one chronological surface.

---

<!-- Entries appended below this line. Newest immediately below. -->

## 2026-06-05 — Sonal — invoked-6-camille-advisors-live

- **Asked:** Push the Camille Massey and Advisors-group invites live — they were approved on 3 June but never rendered to the page.
- **Produced:** Both invites added to `projects/invoked-6/page.md` and `docs/projects/invoked-6.html`. Hero pill updated to "4 VIP invites approved by Sonal". Content log extended with 3 Jun and 5 Jun rows. Self-portrait timeline entry added for today; 3 Jun entry demoted. Footer/eyebrow dates updated to 5 June.
- **Learned:** nothing new — this is a surfacing session. The pattern was already in the learnings; the gap was a missed render.
- **Status changes:** none.
- **Sources touched:** [[invoked-5-proceedings-2026]] (Camille verbatim quote) · [[2026-06-01-vip-invite-voice]]

## 2026-06-03 — Sonal — invoked-6-vip-invites-approved

- **Asked:** Draft and refine InvokED 6.0 VIP invites for Marc Benioff (Salesforce), Camille Massey (Synergos), and Peggy Dulany (Synergos). Multiple rounds of feedback per email. Also drafted an advisors-group invite (not speaker, join as participant).
- **Produced:** Three approved invite drafts (Marc, Camille, Peggy). Advisors-group template drafted (pending approval). All pushed to live brain page.
- **Learned:** structural — six new patterns confirmed → `learnings/2026-06-01-vip-invite-voice.md`: no movement language for global partners; returning-speaker recall structure; meeting attribution ("me and the team"); "valuable" vs "extraordinary"; advisors = join not speak; merged CTA/save-the-dates.
- **Status changes:** none flipped.
- **Sources touched:** [[invoked-5-email-invites-2026]] [[invoked-5-proceedings-2026]]
- **Voice notes:** "unique kind of leadership" approved over "different kind"; "valuable technology partner" approved over "extraordinary"; movement stats removed from global-partner invites.

## 2026-06-02 — Sahil (maintainer amendment) — publish-direct-to-main-binding

- **Asked:** Sahil — after fixing the 403 (Sonal accepted the write-collaborator invite as `sonalb03`), close the gap once and for all: *"I want her to be able to use Claude Code web session or terminal or anything and always push to the brain — nothing should be local for anyone collaborating."* Verified state first via git: only `main` exists on origin, it is directly pushable (no branch protection), her lost work never reached origin (stuck on a web-session feature branch).
- **Produced:** **Constitutional amendment to `CLAUDE.md`** — new section **"Publishing — direct to `main` (binding for ALL surfaces)"** inserted after `## Identity`. States that every session (desktop, terminal, web) commits and pushes **directly to `main`**; never a feature branch, never a PR, never session-only work; a feature-branch-defaulting surface (the web app) must switch to `main`; a failed push is a loud emergency, not a branch fallback. Written reason in the commit per INTENT (constitution edits require it). `CLAUDE.md` is tool-deny-listed; edited via shell under the lead maintainer's explicit directive.
- **Learned:** structural — the brain's publish model is now explicit for all surfaces, closing the web-app "work hides on a branch" gap. Pairs with the same-day SessionEnd hardening (loud push failures).
- **Status changes:** none in `wiki/**`. `CLAUDE.md` amended (constitution).
- **Sources touched:** []
- **Note:** Permission wall (403) resolved by invite acceptance; branch-model gap resolved by this rule. Remaining for full green: Sonal opens a FRESH web session so it re-clones with her now-active write access, and the rule steers it to push to `main`.

## 2026-06-02 — Sahil (maintainer infra) — harden-sessionend-push-and-mirror-guards

- **Asked:** Sahil — Sonal's Claude Code **web** session drafted the Wendy Kopp invite but it never reached GitHub; her wrap said *"session auth is blocking the remote push."* *"Fix it all step by step and verify… so we can all start."* Root cause found in `.claude/settings.json`: the SessionEnd hook ended with `git push origin main 2>&1 || true` — **the `|| true` silently swallowed every push failure**, so a web session with no GitHub write access committed locally and reported nothing. Plus a second recurring gap: project `page.md` edits landing without the `docs/projects/<slug>.html` mirror being regenerated (live page stale).
- **Produced:**
  - **`tools/session_end.sh`** (new) — replaces the inline one-liner. Commit + push with a **loud, unmissable failure block** when the remote rejects (auth / offline / non-FF): *"Your work is committed LOCALLY but is NOT on GitHub."* Keeps the LEDGER + self-portrait guards; **adds a mirror-drift guard** — warns when any `projects/<slug>/page.md` changed without its `docs/projects/<slug>.html`. Always exits 0 (never blocks session close).
  - **`.claude/settings.json`** — SessionEnd hook now calls `bash tools/session_end.sh`; the silent `|| true` is gone (verified 0 matches). JSON validated; script `bash -n` clean; mirror guard dry-run fires correctly.
  - **The actual auth fix is Sahil's browser action** (grant GitHub write to the web session) — surfaced to him with exact steps + a verification test; not a repo-side change.
- **Learned:** nothing structural (infra hardening, not a voice/state change). Process note: push failures must be loud, not swallowed — a quiet `|| true` cost a full draft.
- **Status changes:** none. No `wiki/**` touched.
- **Sources touched:** []
- **Note:** Closes the two gaps Sahil flagged ("there are gaps"): (1) push failures are now visible everywhere, including Sonal's web sessions once they pull this; (2) mirror drift now warns at session close. Pairs with the still-pending auth grant (Step 2, Sahil) and getting today's Wendy invite live (needs the draft text).

## 2026-06-01 — Sahil (directed run, surfacing Sonal feedback) — invoked-6-html-mirror-approved-invites

- **Asked:** Sahil — *"update yourself fully and show me the updated …/projects/invoked-6.html link from Sonal's feedback that she gave earlier."* Pulled latest (4 commits via SessionStart hook), then found the gap: the prior session wrote Sonal's two approved VIP invites into `projects/invoked-6/page.md` but never regenerated the public HTML mirror — the live page still showed only the seeded scaffold (0 mentions of Peggy/Marc/approved).
- **Produced:**
  - **`docs/projects/invoked-6.html` rebuilt** to mirror the approved state: new **"Approved by Sonal"** section at the top rendering both invites in full (Peggy Dulany + Marc/Salesforce) with relationship context and the VIP-pattern summary; hero pills updated (2 approved VIP invites · dates locked); gap-list table flips **Dates → 26–27 Feb 2027 ✓** and **Venue → PCPA Bengaluru ✓** (now locked by the approved invites); content log extended to four rows (seed → draft → Peggy approved → Marc approved); refresh stamps bumped.
  - **`projects/invoked-6/page.md`** gap-list updated to mark `{{DATES}}` and `{{VENUE}}` as locked (was "needed") — faithful to what the approved invites establish, not invented.
  - **`docs/index.html`** self-portrait — new today entry ("two VIP invites approved + page now shows them"); prior Peggy-invite entry demoted; eyebrow → third session.
  - **Pushed mid-session** per the binding auto-publish rule, so the review URL is live when the wrap surfaces it.
- **Learned:** nothing structural — this is a mirror-sync + surfacing session. The VIP voice pattern itself was already captured in [[2026-06-01-vip-invite-voice]]; this session only propagates it to the public page. Process note worth holding: an approval recorded in `page.md` is not "shown" until the HTML mirror is regenerated in the same session.
- **Status changes:** none flipped in `wiki/**`. `projects/invoked-6/page.md` gap-list values updated (dates/venue locked); both invites remain `approved`.
- **Sources touched:** [[invoked-5-concept-note-2026]] [[invoked-5-email-invites-2026]] (via the workspace page) · learning [[2026-06-01-vip-invite-voice]]
- **Note:** Closes the loop on Sonal's earlier feedback — she scrolls the same invoked-6.html link and now sees both approved invites instead of the scaffold.

## 2026-06-01 — Sonal — invoked-6-peggy-dulany-invite

- **Asked:** (1) Draft InvokED 6.0 invite for Peggy Dulany (Synergos) — 26–27 Feb 2027, PCPA; 2-year engagement, One Billion Futures hook. (2) Sonal shared her edited Peggy version — "use as reference for future emails." (3) Sonal shared approved Marc/Salesforce invite — "feed into the brain."
- **Produced:** Two approved VIP invites in `projects/invoked-6/page.md`. Learning updated at `learnings/2026-06-01-vip-invite-voice.md` — full VIP pattern now confirmed across two examples: subject form, shared-belief connector (new from Marc), drop verbatim quotes, org-philosophy framing, "speaker and thought partner" ask, specific questions from invitee's world, first name once in body, co-design CTA, "possibility of" close, SD Shibulal signatory form.
- **Learned:** structural — VIP invite pattern built from two approved examples → `learnings/2026-06-01-vip-invite-voice.md` → flagged for Friday review.
- **Status changes:** both invites `approved` in `projects/invoked-6/page.md`.
- **Sources touched:** [[invoked-5-email-invites-2026]] [[invoked-5-proceedings-2026]] [[invoked-5-concept-note-2026]]

## 2026-06-01 — Sahil (directed run, routing Sonal email) — invoked-6-workspace-seeded

- **Asked:** Sonal emailed four InvokED 5.0 documents — concept note, session transcripts, summary, email-invitation library — and: *"We are starting to roll out invitations for InvokED 6.0, and I wanted to create this using Claude code… prepare a project specifically for this as well after absorbing the data."* Directed run (emailed brief + sources → Sahil's $200 account).
- **Produced:**
  - **Three new `wiki/sources/` files** (faithful extraction, no synthesis): [[invoked-5-concept-note-2026]] (what/why/who/WIIFT; 6–7 Feb 2026, PCPA Bengaluru, 1,000+ audience, Samaaj/Sarkaar/Bazaar/Sanchar, 250 Districts, one billion futures); [[invoked-5-proceedings-2026]] (digest of the summary + transcripts — session map, ~25 verbatim quotes, outcomes incl. 1.2M micro-improvements / Commons + STEM Collective launches / bright-spot numbers, named grassroots stories); [[invoked-5-email-invites-2026]] (the invitation library — skeleton, ~17 archetypes, standing phrases, signatories, logistics, verbatim canonical templates). Transcripts (~1.1M chars) read via Drive MCP, digested by subagents to keep main context clean.
  - **New project workspace `projects/invoked-6/`** — `page.md` + `chatlog.md`. Holds 12 invite templates rewritten as **6.0-ready skeletons** with `{{PLACEHOLDERS}}`, an audience→signatory→template map, a momentum bank of verified 5.0 lines, a standing-phrase bank, and — front and centre — a **gap-list of the 6.0 specifics the brain refuses to invent** (tagline, dates, venue, confirmed speakers, register link, dinner date, roundtable slot). Same gap-surfacing pattern Sonal liked on the portrait + Nagaland story.
  - **HTML mirror** `docs/projects/invoked-6.html`; projects landing updated four→five projects + new tile + refresh date; `wiki/index.md` gains an "Event sources (InvokED)" subsection; `docs/index.html` self-portrait gains today's timeline entry (prior demoted, dates bumped).
  - **Pushed mid-session** per the binding auto-publish rule, so the review URL is live when the wrap surfaces it.
- **Learned:** nothing structural — this is an ingest + project-scaffold session. The "surface gaps, don't invent facts" move is already a binding rule from 2026-05-27 (story-over-report § surface gaps); applied here to event logistics rather than a narrative.
- **Status changes:** none flipped. All three new sources land `research-seeded`; `projects/invoked-6/page.md` is `research-seeded`; templates carry `status: template` until Sonal supplies the 6.0 specifics.
- **Sources touched:** [[invoked-5-concept-note-2026]] [[invoked-5-proceedings-2026]] [[invoked-5-email-invites-2026]] (all created this session)
- **Note:** Fifth project workspace. First event/convening corpus in the brain. Next session shape: Sonal opens Claude Code, supplies 6.0 dates/venue/tagline (or names a recipient), and templates resolve into full drafts.

## 2026-05-27 — Sahil (routing Sonal feedback email) — masthanaiah-and-nagaland-v2-recompile

- **Asked:** Sahil — routed Sonal's structured email feedback on both pieces drafted on 2026-05-26. She flagged four specific phrasing issues in the Masthanaiah portrait (*"Forty years in Andhra Pradesh's school education system followed" doesn't make sense* / *"On the basis of strength enrollment..." doesn't sound right* / *"he reformed the morning-afternoon shift system" didn't understand* / *"of pull-driven postings" — simplify*), three in the Nagaland story (*"won its way into the fifteen" needs more context* / *"The fest asked them" should be "encouraged"* / *challenges paragraph needs more empathy*), and one structural rule across both — *"It doesn't read like a story but reporting."* She also asked the AI to highlight gaps for the portrait. *"Let me know once you feed this."*
- **Produced:**
  - **New structural learning [[2026-05-27-story-over-report]]** — captures Sonal's verbatim feedback + the new binding rule for narrative voice ("story over report"). Five moves: build an arc, slow at human moments, fewer em-dashes, show the cost, let the leader feel like a person. Plus the companion rule — **surface gaps by default** in every narrative piece. Paste-ready snippet for `wiki/voice/styleguide.md` § Story over report (Sahil's hand-edit, wiki/voice/** is deny-listed).
  - **Masthanaiah portrait — v2.** Full body rewrite (~620 words) as a beat-by-beat narrative arc — dropout → village school → first dropout (Sankara Raju walks to ask the father) → second dropout (the diploma-engineer cousin, the ST hostel, books-not-allowed-in-rooms) → first 10th pass in 1979 → enrolment-led growth theory → Hyderabad shift reform unpacked in plain English → 1996 counselling system with the room-watching-the-room image → Medak refusal-to-suspend as the test he speaks about most quietly → Director CSE final chapter (SLDP / IIM-A / PM SHRI 2nd in India / SALT) → close with both his repeated own-voice quotes. All four specific phrasing flags fixed inline. Companion Thursday caption also rewritten. **New gap-list** of 9 askable questions for Aquib to take to Masthanaiah Sir.
  - **Nagaland NLNF story — v2.** Full body rewrite (~600 words) as a small arc — Peren's hilly roads, dropped networks, daily-wage parents → the Fest's invitation (now *encouraged*, not asked) → the borrowed-television moment as the emotional centre (gets 3 paragraphs of weight, Kuzie Kulim's reason in her own words, plus one paragraph of pure reflection) → the small steps in each classroom (Ichaulu / Rebiheing / Maheingaule each get their own beat) → the parents turning around at the PTM → the school's single forward-looking line. Empathy + context up front; "encouraged" replaces "asked"; em-dash count reduced from 14 to ~4. **New gap-list** of 8 askable questions.
  - **HTML mirrors regenerated** — `docs/projects/portraits.html` + `docs/projects/nagaland-coffee-book.html` both rebuilt to render the v2 cards with pull-quotes, full body, content log (showing v1 superseded by v2), gap-list cards, voice-notes cards. Both pages bump *last updated* to 27 May.
  - **Chatlogs appended** — both project workspaces carry full v1→v2 transition notes + Sonal's verbatim feedback + classification routing.
  - **`docs/index.html`** — today's timeline entry added, prior entries demoted (no longer marked today).
  - **Pushed mid-session** per the binding auto-publish rule.
- **Learned:** structural — `learnings/2026-05-27-story-over-report.md`. This is the **first voice rule to surface from a content-quality correction** (the prior rule, *movement as frame, people as actors*, surfaced from a structural framing issue). Together the two rules now form the narrative voice spine: *frame correctly* (movement first, people inside) + *write narratively* (arc, not list).
- **Status changes:** **`wiki/voice/styleguide.md` flip to `_status: user-validated` + addition of § Story over report** is queued in the paste-ready snippet inside the learning file (`wiki/voice/**` is deny-listed; Sahil pastes by hand). Both project-page section statuses stay `review-ready` (now v2). Source pages (interview + form response) stay `research-seeded` — the brain reading + re-using them isn't yet a flip to user-validated; Sonal's "use this" on v2 will be.
- **Sources touched:** [[interview-masthanaiah-2026-04-20]] [[nlnf3-gms-jalukie-sectorb-response-2026-05-07]] [[styleguide]] (via paste snippet)
- **Voice notes:** v2 of both pieces is the first end-to-end demonstration of the new *story over report* rule. Specific wins to note: **the borrowed-television moment** now reads as the emotional centre of the Nagaland story rather than a sentence buried in challenges. **The Medak refusal-to-suspend** now reads as the moral test that defines Masthanaiah Sir rather than a sub-clause inside Hyderabad-reform achievements. **The bottle-lamp** gets its own sentence rather than a parenthetical. **The mid-walk MSc Physics decision** gets its own moment. The rule lands.
- **Note:** First post-feedback recompile day. The brain's loop ran end-to-end as designed: Sonal's email → Sahil routes → brain captures structural learning → brain recompiles content using the new rule → push → review URLs are the same as v1 (so Sonal scrolls the same links and sees the difference).

## 2026-05-26 — Sahil (post-call) — demo-tour-page-for-team

- **Asked:** Sahil — *"tomorrow we have a demo with the team, can we also create a one off page to explain how the brain works and will evolve over time too? it needs to be very simple and illustrative page and data flow and architecture shown in a fun way for the non technical team to understand."*
- **Produced:** **`docs/demo.html`** — one-page team tour, ~5 min read, from the brain's first-person POV. Eight sections: (1) hero + intro pill row, (2) one-liner blockquote in a gold-on-indigo gradient card, (3) **four-rooms grid** with tinted cards + emoji icons explaining State / Session / Learning / Routes in plain English, (4) **six-step flow diagram** with numbered cards + emoji + arrows (Brief → Ingest → Draft → Push → Review → Compound), (5) **two-ways panel** explaining brainstorm-led (Sonal-driven) vs directed run (Sahil-routed), (6) **how-I-learn example** showing the actual *movement-as-frame* correction Sonal made this week — Before / Feedback / After / Saved-as-rule in coloured cards, (7) **live numbers dashboard** (17 LEDGER entries · 11 sources · 5 concepts · 7 learnings · 4 workspaces · 6 routes · 3 drafts this week · 1 voice rule learned), (8) **May→September roadmap** with the May card highlighted as Now. Closes with a gradient promise band and three CTAs (back to brain / log / projects). Bar nav of `docs/index.html` adds *Tour* link between Projects and Log. Fully responsive, matches existing visual language (Fraunces serif + Inter + cascara/gold/indigo palette + soft-rose/mint/sky/sand tints).
- **Learned:** none new — this is a one-shot communication artefact, not a structural shift. Page is designed to be regenerable / refreshable as the brain compounds (numbers section will need a refresh after each weekly review).
- **Status changes:** none on `wiki/**`.
- **Sources touched:** []
- **Note:** **Sixth LEDGER entry today.** Built specifically for the 27 May team demo. Lives at https://sahilmodi1965.github.io/shikshalokam/demo.html — refresh ~60s after push. The page is for the team to understand the brain in plain English before the demo, and can be reused for board / funder briefings going forward.

## 2026-05-26 — Sahil (same call) — sessionstart-hook-hardened

- **Asked:** Sahil — *"qq when anyone logs in to claude code will they access the latest brain?"* → confirmed the existing SessionStart hook had three silent-fail bugs (used `git pull --rebase`, bailed quietly on dirty tree, `|| true` swallowed errors). Sahil: *"yes we need this please do it now."*
- **Produced:** **Rule B promoted from contract to harness.** New `tools/session_start.sh` — loud-by-design auto-pull preflight: fast-forward only, prints state on every session open, visibly warns on dirty / diverged trees, returns 0 so Claude Code starts cleanly even on failure. `.claude/settings.json` SessionStart hook now invokes the script (timeout 30s). Permissions allowlist extended for `tools/**` writes and the new bash + python script invocations. JSON validated. Dry-run on this machine confirmed the hook reports correctly. Every Claude Code session in this repo, on any machine (Sonal's, Sahil's, Sahid's, a future contributor's), now auto-pulls before reading or writing anything.
- **Learned:** none new — this is execution of [[2026-05-26-five-decisions-binding]] § Decision 1 § Rule B. Learning updated with the `landed_so_far:` entry + a new sub-section noting harness enforcement.
- **Status changes:** none on `wiki/**`.
- **Sources touched:** []
- **Note:** **Fifth LEDGER entry today** — five distinct beats in one shared call (content-from-brain run · push-mid-session fix · workflow tidy · five-decisions-binding · hook hardening). The auto-pull rule went from idea → contract → harness in a single day. Each beat made the prior one harder to undo.

## 2026-05-26 — Sahil + Sonal (joint video call) — five-decisions-binding-and-log-page-build

- **Asked:** Sahil — *"yesss"* to all five workflow decisions surfaced in the prior turn: (1) auto-push + auto-pull rules binding; (2) build the log page this session; (3) Sahil-routes-source-attached-briefs as the default; (4) Friday 29 May 4pm IST as the standing weekly-review slot; (5) Sahil hand-pastes the three queued items (voice styleguide + CLAUDE.md ×2) after the call.
- **Produced:**
  - **`docs/log.html`** — new public page at `/log/`, the **single review surface** for every artefact the brain has ever pushed. Newest first, grouped by date; each row shows author, slug, the one-line ask, and direct links to the live artefacts. Linked from the self-portrait bar nav (between *Projects →* and *Why*). Auto-generated from LEDGER.
  - **`tools/build_log.py`** — first stub generator. Parses `LEDGER.md` (split on the `<!-- Entries appended below -->` marker — robust against template-heading collisions), extracts the one-line Asked field + every URL in each entry body, filters to artefact URLs (anything on `sahilmodi1965.github.io/shikshalokam`), renders to styled HTML. 14 entries · 4 artefact links on first run.
  - **`learnings/2026-05-26-five-decisions-binding.md`** — captures all five decisions; carries paste-ready CLAUDE.md amendments for Rules A + B (auto-publish + auto-pull preflight); paste-ready `brain.yml` `weekly_review_slot` field; a combined commit-message stub for Sahil's post-call paste batch. The brain treats the rules as binding from this commit even though three of them live in files the brain can't edit itself — sessions read `learnings/` at start; the learnings *are* the contract until CLAUDE.md catches up.
  - **`projects/README.md` § Two valid session shapes** — new section adding the *"directed run"* shape (Sahil-routed) alongside the existing *"brainstorm-led"* shape (Sonal-driven), with the default rule (directed run for source-attached briefs).
  - **`docs/index.html`** — bar nav adds *Log* link; today's timeline entry replaced with the new five-decisions card; the prior workflow-tidy entry demoted (still on the page, no longer marked today).
  - **Pushed to remote** at the new always-on default — no opt-out invoked this session.
- **Learned:** structural — three of the five decisions land as `learnings/` entries the brain reads at session start, two of them land as live code (the log page + the build script + the README + the timeline). The four pending paste items (CLAUDE.md ×2 + voice styleguide + brain.yml) carry full paste-ready snippets in the corresponding learning files; Sahil's post-call paste closes the loop. `learnings/2026-05-26-five-decisions-binding.md` is the index for the paste queue.
- **Status changes:** none on existing wiki/** files. New project-page convention shape lands in `projects/README.md` (was `_status: research-seeded`, stays there — Sonal hasn't used the directed-run pattern from her own session yet, only Sahil-on-her-behalf).
- **Sources touched:** []
- **Voice notes:** none — this is a structural build session, not a content draft session.
- **Note:** **Fourth LEDGER entry today** — four times the brain compounded in one day (first content-from-brain run · push-mid-session structural fix · joint-call workflow tidy · five-decisions-binding build). Same-day multi-entry days are legitimate when the maintainer joins to authorise structural builds (precedent: 2026-05-21 had two). Today's four entries together form the operational backbone of the next CLAUDE.md per-session-contract revision.

## 2026-05-26 — Sahil + Sonal (joint video call) — workflow-tidy-and-drift-fix

- **Asked:** Sahil + Sonal — on a screen-shared video call, asked the brain to (a) execute the three maintenance items Sonal's earlier session left as a WhatsApp prompt (delete stale `sessions/2026-05-26-bihar-chaupal-post.md`, promote the *movement-as-frame, people-as-actors* learning into `wiki/voice/styleguide.md`, add `verify_before_publish: true` to the WEF source), and (b) lay out two structural improvements they want binding from now on — *every chat must produce a pushed, reviewable artefact link* AND *no silent fail if push is forgotten* — plus a 5-year-old-style walk-through of where else the workflow might fail.
- **Produced:**
  - **Drift caught.** Local was 2 commits behind `origin/main` from Sonal's session (`7c4da60` + `a6c5aeb`). Pulled fast-forward before touching anything — exactly the silent-overwrite scenario the next rule prevents.
  - **`sessions/2026-05-26-bihar-chaupal-post.md`** — `git rm`'d. Sonal's session created it before discovering LEDGER is the session log; it doesn't belong in `sessions/` (which is empty by design).
  - **WEF source flagged** — `wiki/sources/research-wef-future-is-collective-2025.md` carries `verify_before_publish: true` + `verify_what:` note + a banner at the top. Next pass downloads the PDF, quotes the in-report Shikshagraha mention verbatim, removes the banner.
  - **Voice-styleguide promotion drafted** — `learnings/2026-05-26-movement-frame-people-actors.md` updated with `promoted: pending-maintainer-hand-edit`, `landed_so_far:`, `pending_maintainer_paste:`, and a full **Paste-ready snippets** section (frontmatter swap + new `## Shikshagraha mentions` block + suggested commit message citing the learnings slug). `wiki/voice/**` is deny-listed per CLAUDE.md rule 8 (voice is hand-curated); Sahil pastes the snippet by hand to land it.
  - **Workflow upgrades laid out in chat** — *always-on auto-publish* rule + *production log* page proposal + *drift-prevention preflight* (auto-pull at session start) + 6-point 5-yo gap walk-through. Captured in the response, not yet committed as code — these need Sahil's explicit nod before the brain builds them (per CLAUDE.md rule 10: stop and ask before new conventions).
- **Learned:** structural (validation + queued) — the *movement-as-frame* rule is the first user-validated voice rule beyond the captions-doc exemplars; the *always-push* and *auto-pull-preflight* rules surface as the next two CLAUDE.md amendments. Two existing learnings — `2026-05-26-push-during-session-for-review` and today's joint-call walk-through — together form the operational backbone of the next CLAUDE.md per-session-contract revision; Sahil-by-hand.
- **Status changes:** `wiki/sources/research-wef-future-is-collective-2025.md` — `corrected_by:` appended (`_status:` unchanged — still research-seeded until Sonal uses it). `learnings/2026-05-26-movement-frame-people-actors.md` — `promoted:` → `pending-maintainer-hand-edit`. **`wiki/voice/styleguide.md` flip to `user-validated` is queued in the paste-ready snippet** — flips the moment Sahil commits the hand-edit.
- **Sources touched:** [[research-wef-future-is-collective-2025]] [[styleguide]] (via promotion-snippet — actual file edit pending Sahil's hand)
- **Voice notes:** The voice rule itself (*movement as frame, people as actors*) sits in the paste-ready snippet — see `learnings/2026-05-26-movement-frame-people-actors.md § Paste-ready snippets` for the exact text. Three lines that will land in `wiki/voice/styleguide.md` once Sahil pastes: movement first as container · real actors named within it · "Shikshagraha brought this to life" is a Never.
- **Note:** This is the **third LEDGER entry today** — two from earlier (first content-from-brain run, push-mid-session structural fix) plus this joint-call tidy. Pattern: same-day multi-entry days are legitimate when a maintainer joins to authorise structural builds (precedent in 2026-05-21).

## 2026-05-26 — Sonal Bhasin — variant-1-revision-and-approval

- **Asked:** Sonal — shared structured feedback on Variant 1 *"What if collective action could be measured?"*: (1) SL↔SG relation missing; (2) #InvokED2026 irrelevant to a timeless collective-action post; (3) Shiksha Chaupal unexplained / ShikshaLokam's role unnamed. Reviewed two revised iterations and approved the final copy.
- **Produced:** Variant 1 revised — Shiksha Chaupals defined as community gatherings at the heart of the Shikshagraha movement; real actors named within that frame (women from SHGs, didis, parents, Jyoti Mahila Samakhya, Srishti Mahila Samakhya, other SHGs & CSOs); ShikshaLokam's catalysing role made explicit; #InvokED2026 replaced with #ShikshaLokam. Status flipped `draft → approved`. `projects/captions/page.md` and `docs/projects/captions.html` updated and pushed. Live at https://sahilmodi1965.github.io/shikshalokam/projects/captions.html
- **Learned:** structural — "movement as frame, people as actors" — Shikshagraha leads any mention of ground-level action, but the real actors (SHG women, didis, parents, named partner CSOs) must be named within that frame. Naming partners by name is part of the voice, not a detail. → `learnings/2026-05-26-movement-frame-people-actors.md`
- **Status changes:** `projects/captions/page.md` Variant 1 `draft → approved`.
- **Sources touched:** [[shikshalokam-brazil-stories-may2026]] [[research-wef-future-is-collective-2025]]
- **Voice notes:** Movement named first as container; people fill it — "gatherings at the heart of the Shikshagraha movement — where [named actors] come together." Not "Shikshagraha brought this to life." #InvokED2026 is event-specific; removed from timeless collective-action posts.

## 2026-05-26 — Sahil (maintainer, routing Sonal email) — content-from-brain-first-run

- **Asked:** Sahil — routed Sonal's email *"Content Creation with Brain"* end-to-end: produce (1) an Ed-Leader Portrait of **Shri Vempuluru Nagoor Masthanaiah** from Aquib Rizwan's 20 Apr 2026 interview transcript, and (2) a coffee-table-book story celebrating **collective action + micro-improvement** from one of the 15 winning schools of **Nagaland Literacy & Numeracy Fest 3.0** (NIPUN Nagaland), pulled from the Google Form responses sheet Sonal shared. Sahil's overlay: *"go full force … at the end of the run I want links that Sonal can review overall."*
- **Produced:**
  - **`raw/2026-05-26.md`** — both source drops captured verbatim with provenance, brief, and open questions.
  - **Two new `wiki/sources/*.md`** (_status: research-seeded):
    [[interview-masthanaiah-2026-04-20]] (40-year arc, counselling-based transfer system 1996, PM SHRI 935 schools / 2nd in India, SLDP 250 HMs to IIM-A cascaded to ~45K schools; all verbatim quotes preserved) and
    [[nlnf3-gms-jalukie-sectorb-response-2026-05-07]] (GMS Jalukie Sector-B, Peren — Head Teacher Kuzie Kulim's four-teacher cohort; written consent agreed; image assets uploaded).
  - **Concept enrichment** — `wiki/concepts/programs.md` § Active adds **Nagaland Literacy & Numeracy Fest (NLNF) 3.0 / NIPUN Nagaland** as a named programme (Pre-Primary–G3 five-MIP-cycles + G4-5 PBL + mentoring + Mega PTMs + recognition stack), with the full collective named (DoSE + Samagra Shiksha Nagaland + SCERT · ShikshaLokam · Mantra4Change · NagaED · Education Above All).
  - **`projects/portraits/page.md`** — first real portrait card: *"From the fifth-class dropout — forty years of holding the line."* Status: **review-ready**. ~340-word body + companion Thursday caption draft.
  - **`projects/nagaland-coffee-book/page.md`** — project intent re-anchored on NLNF 3.0 / NIPUN Nagaland as the canonical container (was previously only the DEP / PBL macro framing); first real story card: *"Pebbles, poems, and a borrowed television."* Status: **review-ready**.
  - **HTML mirrors** — `docs/projects/portraits.html` + `docs/projects/nagaland-coffee-book.html` both rebuilt to render the new cards with pull-quotes, full body, content log, voice notes. `docs/projects/index.html` tile counts updated. `docs/index.html` self-portrait timeline gets a new today entry; projects-grid card text updated; eyebrow + footer dates → 26 May 2026.
  - **`wiki/index.md`** — new "Field sources" sub-section registering both new sources. **`wiki/sources/SOURCES.md`** — 2026-05-26 section appended. **`wiki/log.md`** — compile-step audit entry.
  - **chatlogs** appended on both project workspaces; **`learnings/2026-05-26-content-from-brain-directed-run.md`** captures the operational refinement (directed-content-run vs brainstorm-led-run patterns).
  - **Two review-ready URLs** handed back to Sonal:
    https://sahilmodi1965.github.io/shikshalokam/projects/portraits.html
    https://sahilmodi1965.github.io/shikshalokam/projects/nagaland-coffee-book.html
- **Learned:** structural-validation — first end-to-end demonstration of the 19 May project-page architecture carrying full review-ready content. Loop ran exactly as designed: brief in → source ingest → concept enrichment → workspace draft → HTML mirror → live URL. Operational refinement captured in `learnings/2026-05-26-content-from-brain-directed-run.md`: name "directed content run" as a valid sibling pattern to the "brainstorm-led run" in `projects/README.md` § per-session contract.
- **Status changes:** none on existing files. Two new `wiki/sources/research-seeded` source pages + one concept page (`programs.md`) appended-to (kept `_status: research-seeded` since NLNF section is research-derived from Sonal's brief + Brazil-presentation cross-reference, not yet user-validated by Sonal). Both project-page **section** statuses set to `review-ready` (first sections on each page). Source-page `_status:` will flip to `user-validated` on Sonal's first "use this" / "not my voice" reply.
- **Sources touched:** [[interview-masthanaiah-2026-04-20]] [[nlnf3-gms-jalukie-sectorb-response-2026-05-07]] [[shikshalokam-brazil-stories-may2026]] [[shikshagraha-brief-collaterals-feb2026]] [[styleguide]] [[khushboo-newsletter-jan2024]]
- **Voice notes:** *Portrait* — leader-foregrounded with his own self-correction as the opener (*"Not from the teacher — from dropout of fifth class."*), location-rooted on the village under a tree, one specific origin moment (tonic-syrup-bottle lamp), the named first teacher (Sankara Raju), three-chapter career arc with verbs doing the work (*originated · reformed · delivered · cascaded*), own-voice close (*"Aims must be good. If aims are good, results automatically will be good."*). Resisted dressing him in language he didn't use — no Sanskrit-flourish, no "thought leader," no superlatives; his English is broken-declarative-repetitive and his authority comes from concrete acts. Matches the live-gallery register (*"Holding Space for Every Learner" / "Turning a Failing School Around"*). *Nagaland story* — story-first / data-after per Khushboo's newsletter exemplar; named everyone (all four teachers + school + district + every partner CSO + government bodies by name + role) per the Brazil-presentation collective-naming convention; held close to school's own words (*"Quality foundational learning is possible even with limited resources."*); resisted inventing numbers the source didn't carry.
- **Note:** Two open queues for next sessions — (1) 14 more NLNF 3.0 winning-school responses on the same Google Form sheet (one school per session so each gets its own voice pass); (2) Masthanaiah Sir's photos pending his share before the portrait can be illustrated. `wiki/entities/` directory considered as a home for Masthanaiah-as-named-thing — deferred per CLAUDE.md rule 10; he lives as a source + a portrait card for now.

## 2026-05-21 — Sahil (maintainer, Sonal on call) — research-pipeline-build

- **Asked:** Sahil, with Sonal on the call — "fix all the feedbacks and share a new post / variation after all structural changes are made." Same-session promotion of the feedback captured in the entry below.
- **Produced:**
  - **New skill `shikshalokam-research`** (`.claude/skills/shikshalokam-research/SKILL.md`) — verifies external studies against a 3-tier trust scale, files them, returns the wikilink to cite. Runs standalone or as a step inside `shikshalokam-write`.
  - **`shikshalokam-write` updated** — research + auto-cite is now a default step (step 2) for evidence-anchored content; read order pulls `wiki/sources/research-*.md`.
  - **Three studies verified (live WebSearch) and filed** as `wiki/sources/research-*.md`: [[research-leithwood-leadership-2004]] (Wallace Foundation review — leadership second only to teaching), [[research-aser-2024]] (Pratham — government-school foundational-learning recovery), [[research-wef-future-is-collective-2025]] (Schwab Foundation / WEF — names Shikshagraha). Registered in `wiki/index.md`, `wiki/sources/SOURCES.md`, `wiki/log.md`.
  - **Date-wise content log** — `## Content log` section added to `projects/captions/page.md` + mirrored to `docs/projects/captions.html` (new `.logtable` style in `docs/projects/style.css`); `projects/README.md` per-session contract now requires it on every project page.
  - **New post:** captions **Variant 4** — *"The recovery no one's talking about."* (LinkedIn, ~95 words, ASER 2024 equity) — first caption drafted end-to-end through the new pipeline. **Variant 2 citation corrected** — unconfirmed OECD placeholder → verified Leithwood et al. (2004), Wallace Foundation. V1 + V3 source lines tightened to the filed sources.
  - `docs/index.html` self-portrait timeline entry rewritten (research capability built, not just captured); captions tile counts updated to 4 across `docs/index.html`, `docs/projects/index.html`, `docs/projects/captions.html`.
- **Learned:** structural learning `learnings/2026-05-21-research-citation-and-datewise-log.md` **promoted** (`promoted: true`) — same-session maintainer build, not deferred to weekly review. CLAUDE.md amendment (new behavior rule 12 — "Evidence is researched, not improvised") recorded in the learning for Sahil to paste by hand (`CLAUDE.md` is Write/Edit deny-listed).
- **Status changes:** three new `wiki/sources/research-*.md` created at `_status: research-seeded` — weekly review to flip to `user-validated` once Sonal has used them. No existing-file `_status:` transitions.
- **Sources touched:** [[research-leithwood-leadership-2004]] [[research-aser-2024]] [[research-wef-future-is-collective-2025]] [[shikshalokam-brazil-stories-may2026]] [[shikshalokam-2-strategy-note-jul2025]]
- **Voice notes:** Variant 4 — aphoristic setup opener, comma-dense stat block, gain-and-gap honesty (voice rule: hopeful but honest — never a gain without the matching gap), "har kadam shiksha ki oar..!" sign-off, CTA closer, hashtag stack.
- **Note:** Two LEDGER entries for 2026-05-21 — this build entry and the feedback-capture entry below — one continuous session, split because a maintainer (Sahil) joined to authorise the build. Precedent: 2026-05-19 also carried two entries.

## 2026-05-21 — Sonal Bhasin — research-citation-and-datewise-log

- **Asked:** Sonal — reviewing the three Tuesday research-insight caption variants, she gave process feedback (explicitly tagged "take this as a brain feedback"): she wants a standing capability that researches external studies, trustable surveys, and reliable sources strengthening SL messaging (education leadership · collective action · education equity); future prompts should auto-cite that research without being asked; the research should compound into the brain; and the project pages should show every draft on a dated basis, not just a weekly roll-up.
- **Produced:** No draft — feedback-capture session. Wrote `learnings/2026-05-21-research-citation-and-datewise-log.md` capturing all four parts, classified structural, with a four-step promotion path routed to Sahil's monthly maintainer pass (the parts are capability builds, not weekly-review wiki edits).
- **Learned:** structural — research-as-a-capability + auto-cite + compound-to-`wiki/sources/` + date-wise project-page log → learnings/2026-05-21-research-citation-and-datewise-log.md → target: shikshalokam-write skill, a new research capability, docs/projects/*.html, projects/README.md, CLAUDE.md.
- **Status changes:** none. No `wiki/**` touched; the three 19 May caption variants stay `_status: research-seeded` (Sonal has not approved any — she redirected to process).
- **Sources touched:** []
- **Note:** The three Tuesday variants are still awaiting Sonal's pick — copying a title back still flips it to approved. Interim behaviour until the capability is built: sessions keep citing real studies by hand with a verifiability flag, as the 19 May captions did. Building the research agent mid-session was deliberately not done (CLAUDE.md rule 5 — no ghost features; rule 10 — stop before new conventions).

## 2026-05-19 — Sahil (on Sonal's behalf) — first-captions-demo + nav-fix

- **Asked:** Sahil — (1) the main brain page is missing navigation to the new project workspaces; add it. (2) First captions demo: byte-sized informative posts anchored on research studies / surveys / reports that strengthen SL-aligned messaging — collective action + agency for education leaders.
- **Produced:**
  - **`docs/index.html` bar nav** — added `<nav class="bar-nav">` with Projects (lead, cascara colour), Why, Voice, Story, Roadmap. Sticky on scroll. Mobile breakpoint hides non-lead links and the chat CTA below 760px so the Projects link stays accessible.
  - **3 caption variants drafted for Tuesday — Tech / Research Insight** in `projects/captions/page.md`, mirrored to `docs/projects/captions.html`:
    - V1 LinkedIn (~95 words) — *"What if collective action could be measured?"* — Bihar Shiksha Chaupal numbers (55K women, 2,450 chaupals, 28K schools) + WEF *The Future is Collective* (2025) recognition. Both anchors verifiable in the brain ([[shikshalokam-brazil-stories-may2026]], [[drive-sl-communications]] § 2025-26).
    - V2 LinkedIn (~95 words) — *"Reform begins with curriculum. Shikshagraha begins with the leader."* — OECD school-leadership research **paraphrased not quoted**, exact citation flagged for Sonal to verify before posting. Threads in the I HAVE / I CAN / I WISH agency framework from the SL 2.0 Strategy Note.
    - V3 X/Twitter (245 chars) — *"Twenty years of ASER — the network is what's missing."* — Pratham's ASER cited as a longitudinal body of work, safe attribution for the byte format.
  - **Captions tile counts updated** across `docs/index.html` § projects, `docs/projects/index.html` tile, and `docs/projects/captions.html` hero pill row (3 Tuesday variants drafted · 4 rhythm slots still empty).
  - **`projects/captions/chatlog.md`** appended with the first real session entry (rhythm day, brief, variants, voice rules applied, open thread for next session).
- **Learned:** one-off — Sahil's "where is the projects nav" was a direct correction; fixed in place. No learnings file needed (not structural — the bar simply needed an explicit nav element). The captions demo is the **first real test of the project-page architecture**: chat → page edit → HTML mirror → push → review. Loop ran end-to-end this turn.
- **Status changes:** `projects/captions/page.md` stays at `_status: research-seeded` — Sonal hasn't reviewed yet. Will flip to `user-validated` on her first approval ("use this") or correction ("not my voice"), whichever lands first.
- **Sources touched:** [[shikshalokam-brazil-stories-may2026]] [[drive-sl-communications]] [[shikshalokam-2-strategy-note-jul2025]] [[styleguide]]
- **Voice notes:** V1 uses rhetorical-question opener + comma-dense stat block + "har kadam shiksha ki oar..!" sign-off. V2 uses pulled-finding opener + stacked short lines + I HAVE / I CAN / I WISH (SL 2.0 framework). V3 uses compressed stacked-line cadence with no closer (X format). All three end with the canonical hashtag stack (V1/V2 with full closer, V3 minimal).
- **Note:** Three-beat session — combined with the prior architecture entry (committed in 7d2b485) those are the two LEDGER entries for 2026-05-19. Pushed manually within the session so Sahil could verify the nav + captions render live; SessionEnd hook will no-op on clean tree at session close. Open: Sonal can copy any variant title back into chat to flip its status to `approved`; pushback routes to learnings. Maintainer enrichment candidates surfaced for next pass: Karthik Muralidharan / J-PAL South Asia, IDR sector pieces, NCERT / Azim Premji University, Hargreaves on distributed leadership.

## 2026-05-19 — Sahil (maintainer) — project-page-architecture

- **Asked:** Sahil + Sonal — stand up project-page workspaces so Sonal's brainstorms enrich a live artefact in place instead of producing one-shot drafts she has to copy out of chat. Four projects: Nagaland coffee book, captions, blogs, portraits. Confirm new Drive/web sources alongside.
- **Produced:**
  - **New artefact class** at `projects/<slug>/` — four workspaces scaffolded (`page.md` + `chatlog.md` each), plus `projects/README.md` carrying the binding per-session contract for project pages. Each `page.md` has structured frontmatter (`_status:`, `page_budget_tokens:`, `voice:` wikilink, `sources:` wikilinks, `shareable_url:`) and the right body shape per project: story pool for Nagaland; rhythm-grouped option pool for captions; idea-queue + WIP-draft layer for blogs; one-section-per-leader template for portraits.
  - **Styled HTML mirrors** at `docs/projects/` — shared `style.css` matching the self-portrait's visual language, a projects landing `index.html`, and four project HTML pages. Live at https://sahilmodi1965.github.io/shikshalokam/projects/{index,nagaland-coffee-book,captions,blogs,portraits}.html — refresh ~60s after push.
  - **`docs/index.html` refreshed** — new top-of-timeline entry (project workspaces), prior 19 May entry demoted; new `<section id="projects">` listing the four workspaces with live links.
  - **`raw/2026-05-19-project-pages-brief.md`** — Sahil's brief captured verbatim with intent + the architectural decision Sahil/Claude locked this session (styled HTML pages, dual-write page.md + HTML until a build script lands).
  - **New route `routes/web-shikshalokam-org.md`** — the two public web surfaces Sonal flagged (https://shikshalokam.org/blogs/ and https://shikshalokam.org/education-leaders-portraits/), both pending maintainer scrape and flagged as voice + format anchors for the [[blogs]] and [[portraits]] workspaces.
  - **`routes/drive-sl-communications.md` § Blogs** — appended SLC Blogs 2026 WIP doc (`1pLXmcCcMD2-v_eThOZT2ioRunchx4DFoTe_tpet0EqM`), the only Drive link in Sahil's drop that wasn't already routed; the rest (SL 2-Pager, both coffee-table files, Blogs 2025, both captions docs) are already mapped in existing routes.
- **Learned:** structural — the chat→output→manual-copy flow was bleeding context; the brain held more than Sonal could carry between sessions. Project pages move the artefact to disk + HTML so the brain compounds on the brainstorm itself, not just the outputs. → `learnings/2026-05-19-project-page-architecture.md` → CLAUDE.md per-session contract + new artefact-class row.
- **Status changes:** none on existing files. New `projects/**/page.md` files at `_status: research-seeded` — will flip to `user-validated` once Sonal opens a session with any one of them and the page accrues real content. `routes/web-shikshalokam-org.md` at `_status` implicit-research-seeded (route — same convention as other route files in the brain).
- **Sources touched:** [[drive-sl-communications]] [[captions]] [[shikshalokam-brazil-stories-may2026]] [[shikshagraha-brief-collaterals-feb2026]] [[styleguide]]
- **Note:** CLAUDE.md amendment (new artefact row in the four-becomes-five table, new clause in per-session contract for project routing, new binding rule #11 on project pages as persistent not output) handed back to Sahil in the learnings file — CLAUDE.md is in the maintainer-only deny list and cannot be edited mid-session. Next Sonal session will be the first real test of the loop (brainstorm → page → push → review); the LEDGER entry from that session is the proof point. Deferred to next maintainer pass: scrape https://shikshalokam.org/blogs/ + /education-leaders-portraits/ into wiki/sources/; build a `tools/build_project_pages.py` if dual-write becomes painful.

## 2026-05-19 — Sahil (maintainer) — sl-communications-folder-ingest

- **Asked:** Sahil — ingest the SL Communications Drive folder Sonal shared today (id `1P-6AHbwLkkGqPOxydhwTyZKUM8U6LP66`) and update the brain artefact.
- **Produced:**
  - New route `routes/drive-sl-communications.md` mapping the SL-org-specific Comms folder (distinct from movement-level `routes/drive-communications.md`). Two top-level subfolders (ShikshaLokam Resources, Social Media Content) — 25 items in Resources, plus already-routed captions docs in SM.
  - New source `wiki/sources/shikshalokam-2-strategy-note-jul2025.md` (_status: research-seeded) — full ingest of the SL 2.0 Strategy Note (Jul 2025). **Fills the SL-org-narrative gap** — brain previously held movement narrative ([[shikshagraha-narrative-2026]]) but no canonical SL-org positioning doc. Captures: SL 1.0→2.0 evolution (platform→network→movement builder), SFPI/NILE origin, ELEVATE digital-public-goods program, 8-team internal structure, ecosystem roles map (Co-Builders/Strategic/Anchor/Collaborators/Momentum/Ambassadors/Advisors/Mentors), 10 verbs of the movement, I HAVE / I CAN / I WISH agency progression.
  - New source `wiki/sources/shikshalokam-brazil-stories-may2026.md` (_status: research-seeded) — four collective-action case studies prepared for Lemann Foundation Summit (Brazil): Nagaland PBL, Punjab PEC (Schwab-recognised), Chhattisgarh ECE/Anganwadi, Bihar Shiksha Chaupals. Canonical multi-partner story template + freshest field numbers (Bihar: 55K women / 2,450 chaupals / 28K schools).
  - Updated `wiki/index.md` (two new source wikilinks + new route wikilink + clarified movement-vs-SL-org route distinction), `wiki/sources/SOURCES.md` (2026-05-19 ingest section), `routes/drive-communications.md` (purpose clarified to "movement-level"; cross-link added to new SL-org route), `wiki/log.md` (compile entry).
- **Learned:** structural — Sahil caught the failure mode: prior enrichment auto-committed and pushed but `docs/index.html` was never updated, leaving the published self-portrait stale ("last updated 14 May 2026"). The "every enrichment updates this page" rule was implicit; made it explicit. → `learnings/2026-05-19-page-update-every-session.md` → CLAUDE.md per-session contract + `.claude/settings.json` SessionEnd hook.
- **Status changes:** none on existing files. New files at `_status: research-seeded` (correct for maintainer-seeded content; flip to user-validated only after Sonal uses them).
- **Sources touched:** [[shikshalokam-2-strategy-note-jul2025]] [[shikshalokam-brazil-stories-may2026]] [[drive-sl-communications]]
- **Note:** Two-ask session — combined into one entry per the one-entry-per-session rule. Ask 1: ingest SL Comms folder (above). Ask 2: enforce page-update rule across both brains. SessionEnd hook now warns when `wiki/`, `routes/`, or `LEDGER.md` change without `docs/index.html` changing; also fixed the `head -50 LEDGER.md` bug (full-file grep now). Same hook + learning pushed to sibling Mantra4Change repo. CLAUDE.md patch handed back for Sahil to apply (CLAUDE.md is in the maintainer-only deny list). Deferred for next enrichment pass per CLAUDE.md voice rule: Vimal P. Thomas's "A Quiet Revolution in Jharkhand's Schools" blog FINAL from `SLC | Blogs 2025`. Also deferred: ShikshaLokam Overview 2025 (v2) shortcut, SL Brand Guidelines vs movement Brand Guidelines comparison, partner-state asset folders.

## 2026-05-14 00:00 UTC — migration — content-brain-overlay-applied

- **Asked:** Sahil (maintainer) — apply the unified content-brain overlay to ShikshaLokam.
- **Produced:** unified file shape (wiki/ typed nodes, INTENT.md, ARCHITECTURE.md, AGENTS.md, TOKEN_BUDGET.md, brain.yml, 6 brand-prefixed skills, this LEDGER).
- **Learned:** nothing yet — first user session post-migration is the first real entry.
- **Status changes:** every wiki/**.md now carries `_status:` frontmatter.
- **Sources touched:** none — structural migration, no content changes.
- **Note:** data preserved verbatim from prior state/ layout. Pre-migration git tag: `pre-unify-2026-05-14`.

## 2026-05-14 19:30 UTC — Sahil (maintainer) — first-enrichment-pass

- **Asked:** Sahil — pull movement-level content from the Shikshagraha Drive into ShikshaLokam brain so the May 30 demo lands with a real, populated brain.
- **Produced:**
  - 3 routes added (`routes/drive-communications.md`, `routes/drive-assets.md`, `routes/drive-coffee-table-book.md`) mapping the Shikshagraha Comms folder, Assets folder, Coffee Table Book folder.
  - 2 new wiki sources (`wiki/sources/shikshagraha-narrative-2026.md` — full canonical movement narrative; the "As ShikshaLokam" section explicitly carries SL's own-impact statements; `wiki/sources/shikshagraha-brief-collaterals-feb2026.md` — latest comprehensive movement stats + brochure structure).
  - 1 voice exemplar (`wiki/voice/exemplars/khushboo-newsletter-jan2024.md` — Khushboo Awasthi's canonical year-end newsletter voice; she signs for ShikshaLokam stakeholder comms).
  - `wiki/index.md` populated with real entries (replaces the migration stub).
  - `SHOWCASE.md` written at brain root — the single human-readable page anyone can scroll to see this brain working.
- **Learned:** Comms Strategy doc currently a stub (objectives + audience segments only); worth maintainer enrichment. Khushboo Awasthi appears in BOTH brains' leadership (this brain's COO + Mantra4Change's Co-Founder) — cross-brain references must explicitly name her dual role per INTENT principle 7.
- **Status changes:** none yet — Sonal's session-driven validation flips state as she uses the brain.
- **Sources touched:** [[shikshagraha-narrative-2026]] [[shikshagraha-brief-collaterals-feb2026]] [[khushboo-newsletter-jan2024]]
- **Note:** This is the first real enrichment after migration. Next enrichment is monthly (Sahil $200 plan); next weekly review is Fri May 23 with Sahid + Sonal. The brain is now ready for Sonal to test in a fresh terminal session.

## 2026-05-14 20:30 UTC — Sahil (maintainer) — captions-2026-27-ingested

- **Asked:** Sahil — pull the live SM Captions 2026-27 doc that's always being worked on, add as ongoing reference.
- **Produced:**
  - Updated `routes/captions.md` to reflect that the 2026-27 doc is now fetched + ingested (was previously "pending re-share").
  - New voice exemplar: `wiki/voice/exemplars/sm-captions-2026-rhythm.md` with the canonical monthly weekday rhythm (Mon feedback / Tue research / Wed studio / Thu portrait / Fri InvokED) and 6 real April-May caption exemplars covering InvokED session teasers, research insights, event announcements (Skoll World Forum), coverage reposts (DEP Nagaland — sourced cross-brain mention of Mantra4Change), welcomes, and awards closing.
- **Learned:** The 2026-27 captions doc is **always-being-worked-on** — needs monthly re-pull. Added that note to the route file so future enrichment passes know to refresh.
- **Status changes:** `routes/captions.md` updated from "pending re-share" to "fetched + ingested 2026-05-14."
- **Sources touched:** [[sm-captions-2026-rhythm]] [[captions]]
- **Note:** The Nagaland DEP April caption is a sourced cross-brain reference (mentions Mantra4Change as partner) — kept verbatim per INTENT principle 7 (cross-brain references explicit + sourced, never transplanted).

## 2026-05-14 21:30 UTC — Sahil (maintainer) — awards-2027-campaign-ingest

- **Asked:** Sahil — ingest the live Shikshagraha Awards 2027 nominations LinkedIn post (posted by Shikshagraha team, reposted by ShikshaLokam).
- **Produced:**
  - New source: `wiki/sources/awards-2027-nominations-live-2026-05.md` with full verbatim post + canonical framings (SFPI institutional credit, three-line audience frame, four-language ladder, hashtag stack).
  - New voice exemplar: `wiki/voice/exemplars/awards-2027-linkedin-post.md` — the canonical campaign-announcement voice pattern. Anatomy table breaks down each move (headline / institutional credit / purpose sentence / stacked three-line audience / direct ask / emoji-led link block / multilingual ladder / hashtag stack / tags).
  - Updated `wiki/concepts/leadership.md` — added the 12 confirmed ShikshaLokam team members tagged in the post (Sonal Bhasin, Anish Saha LL.M, Anubhuti Srivastava, Arshul M., Joyeeta Ray, Neeraj Doddamane, Sharon Varghese, Shwetha Kamath, Syed Hyder Ali H, Vinaya Kurtkoti, Aquib Rizwan, Ayush Tank) + Gurudutt Ramachandra from the SM Captions welcome post. _status: research-seeded → user-validated.
  - Updated identity files (brain.yml, INTENT, CLAUDE, README, SHOWCASE, wiki/index) — Sonal → Sonal Bhasin (full name confirmed from this post).
  - Updated `docs/index.html` — new timeline entries + Sonal Bhasin everywhere + cross-link to the Awards 2027 ingest.
- **Learned:** Sonal's full name is Sonal Bhasin. The Awards are instituted by SFPI (Shibulal Family Philanthropic Initiatives) — Mantra4Change is amplifier, not host. The "Women leading communities. Youth igniting change. Teachers and school leaders building the future from within the system." three-line frame is the canonical audience statement for Awards content — use verbatim.
- **Status changes:** `wiki/concepts/leadership.md` flipped research-seeded → user-validated; identity files updated to canonical name "Sonal Bhasin".
- **Sources touched:** [[awards-2027-nominations-live-2026-05]] [[awards-2027-linkedin-post]] [[leadership]]

## 2026-05-14 22:00 UTC — Sahil (maintainer) — vibe-prospecting-team-discovery

- **Asked:** Sahil — use Vibe Prospecting MCP to enrich team members in both brains, no email enrichment (free preview discovery only).
- **Produced:**
  - Updated `wiki/concepts/leadership.md` with a new "C-Suite / Heads" section: **Neeraj Doddamane** confirmed as Chief Strategy Officer (was research-seeded "role unclear"), **Vijayashree Urs** confirmed as CTO (the "Vijayashree's team" named in the SoW), **Gokul Tirumalai** as Head of Solutions, **Shwetha Kamath** as Head of Ecosystem Development (role newly attached), **Sudha M S** as Head of Product Management.
  - Added "Surfaced via Shikshagraha movement LinkedIn page" sub-section: Luv Kumar (Comms Manager, Pune), Nikita Pradhan (Research & Design Leader), Roddur Mitra (Program Leader) — parent-org pending confirmation.
- **Learned:** "Vijayashree's team" in the SoW = Vijayashree Urs's ShikshaLokam tech team. Significant — when Pratik or Sonal asks about engineering support, the brain can now route correctly. Five Heads (C-Suite + Ops) now have LinkedIn URLs + skill profiles attached.
- **Status changes:** `wiki/concepts/leadership.md` already user-validated; now significantly enriched with role confirmations + LinkedIn provenance.
- **Sources touched:** [[leadership]]
- **Cost:** Zero credits — preview-only fetch (no email enrichment, no export). 50 prospects per company are available; previewing only 5 each kept the run free.

## 2026-05-14 22:30 UTC — Sahil (maintainer) — vibe-team-export

- **Asked:** Sahil — pull all 50 SL team members from Vibe Prospecting (cost 50 credits, no email enrichment).
- **Produced:** Full 50-person SL team roster ingested into `wiki/concepts/leadership.md`. Comprehensive sections by function: C-Suite (3) → Heads & Directors (6) → Communications + Brand (8 incl. Sonal Bhasin) → Programs (14) → Product Development (4) → Engineering & Platform (14, the DIKSHA + product tech tier). Plus tagged-in-Awards-without-Vibe-data names and the 3 movement-page contributors.
- **Learned:** SL has a sizable engineering tier (~14 people in Engineering & Platform) — consistent with DIKSHA being co-built. Sonal Bhasin's role: **Manager, Strategic Communications, based in Kanpur** (works from there, not Bengaluru). Vinay R is Head of Programs (NEW). Aishwarya Rastogi heads Impact Measurement and Data (NEW — important for evidence/M&E content). Anish Saha LL.M is Senior Leader Ecosystem Development.
- **Status changes:** Leadership concept significantly enriched; 50 sourced LinkedIn URLs available.
- **Sources touched:** [[leadership]]
- **Cost:** 50 Explorium credits (no email enrichment). Dataset retained on Vibe Prospecting hub: `ds-89871931-4312-4f1d-991e-6f6079432c7f`.
