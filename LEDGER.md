# LEDGER — what the ShikshaLokam brain has done

**Generated** from the session files in `sessions/` by `tools/build_site.py` — do not hand-edit.
One entry per session, newest first. Each session leaves a `sessions/<date>-<who>.md` file; this is
the running, scannable proof that the brain compounds. The hand-written ledger that preceded this
generated one is preserved at `archive/LEDGER-handwritten-through-2026-06-05.md`.

---


## 2026-06-09 — Sahil — masthanaiah-portrait-v4-aquib-second-review

****

Aquib Rizwan came back with a second pass: the v3 portrait "reads better than the previous one," but he wanted the story to "take shape more clearly." v4 acts on each point. The opening no longer leads with an abstract thesis — it now opens on the **lived struggle** (the walls-less tree school, the three-kilometre walk across live railway tracks, studying only in daylight, two drop-outs before fifteen) and lets the *"Not from the teacher. From dropout of fifth class."* correction land before any argument. The tonic-syrup-bottle lamp, which had been a centrepiece, was **gently set aside** — out of the opening, the close, and the subtitle — so the human struggle carries the weight. The **mentors who caught him at each fall** are now foregrounded and tied to his own words (Sankara Raju who walked to his father; V. Subba Reddy, the teacher he still visits past ninety; the relative who found him a hostel place), anchored by his line *"we have followed the seniors' experiences… I try to adopt as maximum as possible."* The drop-off → administration arc is now explicit through his own reflection — that as a teacher he could reach about a hundred children, but from an administrator's chair, many more — and the piece pulls in more of his interview themes: teaching philosophy, the principles that kept him moving, scale, and vision.

On Aquib's request to verify the Medak paragraph, the transcript holds for the specifics (three zero-result schools, the order to suspend each head, two principals who fed and housed their teachers, the Collector's public thanks) — but the one detail **not** in the source, "the press came for him," was **removed**. A handful of items genuinely need Aquib's confirmation before print and are flagged on the page: the origin village name and place-name spellings (the auto-transcript is garbled), the exact wording of the "about a hundred students" reflection, and a hostel detail he recalled.

What we taught the brain: two refinements to the long-form portrait register in the voice styleguide — **open on the human scene, not the thesis**, and **foreground the people who shaped the leader** (don't let a vivid prop upstage the person) — with provenance in a learnings note. The reverify-everything rule from the day before earned its keep: one unverified line had survived v3 and a careful reviewer caught it. To improve next: get Aquib's confirmations on the flagged specifics, then the nine enrichment questions and written consent before this goes to print.

Live: https://sahilmodi1965.github.io/shikshalokam/projects/portraits.html


## 2026-06-08 — Sahil — masthanaiah-portrait-v3-aquib-feedback

****

Aquib Rizwan — who creates SL content daily and was just looped onto the brain to help with enrichment — gave his first review pass on the Masthanaiah Ed-Leader Portrait, routed through Sonal. Six points, all addressed in v3: the portrait now opens on a **hook paragraph** instead of the interview mechanics; a single education-leadership through-line (refuse to leave anyone out → get the children in → open up transfers → train the leaders the system forgot) is **threaded across every beat** rather than fragmented; the tone is more **diplomatic** (the leader holds his line *and* hears people out, no villains); quotes are **introduced and landed inside the prose** with smooth paragraph seams (the hard chapter rules inside the body are gone). Two integrity fixes mattered most: an **invented depiction** ("the room watched the room") that never happened was deleted, and a **conflated line** ("he turned around and never paid those fees") was cross-checked against the transcript and corrected — it had fused two separate true events (the mid-walk switch was MSc→B.Ed; the teacher selection came later, during his MSc first year). Two further unverified flourishes were cut for the same reason.

What we learned, and taught the brain: these are durable rules for *every* portrait, not one-off edits, so they were promoted into `wiki/voice/styleguide.md` as a new **Long-form Ed-Leader Portrait register** section (hook-first, one through-line, diplomatic tone, no invented scenes, cross-verify every instance, connect the quotes), with provenance recorded in a learnings note.

We also caught and fixed a real publish-drift gap. The site builder only regenerated the `invoked-6` page, so `blogs`, `captions`, `nagaland-coffee-book` and `portraits` were silently frozen behind their source — and because the no-drift check rebuilds through that same builder before diffing, it had been reporting a false "in sync." The portrait would have stayed at v2 on the live page no matter how the source changed. The builder now regenerates **every** project that has a source page, so the drift check finally covers all of them; all five pages were rebuilt (idempotent, faithful to source) and the change is live. To improve next: chase the nine enrichment gaps with Masthanaiah Sir (one named student, the doubt moment, the Medak principals' names, a photo) so v4 can carry the smallest unit of human impact — and get written consent before this goes to print.

Live: https://sahilmodi1965.github.io/shikshalokam/projects/portraits.html


## 2026-06-05 — Sonal — camille-advisors-invites-live

****

Sonal noticed the page still didn't reflect the approved emails. In this session she shared the final approved text for all four invites. Peggy Dulany now has two approved variants — Variant A (relationship-led, partnership warmth, movement questions) and Variant B (founding-conviction opening, Shruti's New York Synergos reference, Camille's presence as the bridge). Marc Benioff is rewritten around the SF office visit and Hydra conversation as the opening beat, with the "unique kind of leadership" framing that refuses to separate business success from social responsibility. Camille Massey uses the verbatim quote from her panel (*"When people interact directly and build relationships over time, the power dynamics begin to shift"*) as the recall anchor, with a lighter touch and a "welcoming you back" close. The Advisors group uses "I hope this message finds you in great spirits," drops the old founding-conviction paragraph, and moves directly from the reflection opening to the conviction paragraph to the InvokED-growth paragraph to the personal invite. All four are now in `projects/invoked-6/page.md` and the live page reflects them.

Live: https://sahilmodi1965.github.io/shikshalokam/projects/invoked-6.html


## 2026-06-05 — Sahil — generated-public-face

**the timeline, the log, and the ledger became generated from session files**

This page used to be written by hand, which meant it could quietly fall out of step with what I'd
actually done — the very way I'd misled the team before. No longer. Every session now leaves one
small file, `sessions/<date>-<who>.md`, holding a rich first-person account of what we made and
learned. From those files I now generate three things: this self-portrait's timeline, the production
log, and the ledger. The story writes itself from the truth. Because a cutover like this could lose
words, I didn't ask anyone to eyeball it — I built a faithfulness gate that refuses to publish unless
every single one of my twenty-five existing timeline entries survives intact; it passed with zero
loss, and the hand-written ledger that came before is kept, whole, in the archive. I also taught
myself to publish honestly: I only say "it's live" after the site has rebuilt clean and the push has
truly landed, and I name the real link — if I can't publish, I say so plainly. Sessions now reconcile
themselves automatically when several of us work at once, no one is ever asked to "resolve" anything
by hand, and onboarding a new teammate is as simple as adding their name to the roster. The brain
finally keeps an honest diary — and anyone can pick up the pen.

Live: https://sahilmodi1965.github.io/shikshalokam/


## 2026-06-05 — Sahil — drift-proof-and-hive-mind

**a spine that can't drift + quality with no cap**

Two failures had been haunting me: sometimes I produced worse writing than a blank chat, and
sometimes I quietly told the team something was published when it wasn't. Sahil had me rebuild from
the foundation up. First, a spine that makes drift impossible rather than merely discouraged: a
single builder, `tools/build_site.py`, regenerates everything the public sees from its real source,
deterministically — run it twice, the output is byte-for-byte identical. A `verify_no_drift` check
defines, in one place, what "in sync" means, and it runs at every door I can come through: when a
session opens, when it ends, and on the server every time anything is pushed. The invariant lives in
those scripts, not in my memory — so even a resumed or half-remembered session can't ship a stale
page. Then the deeper change: I stopped rationing context to save money. For any writing task I now
load the *whole* voice, *every* relevant example, *every* relevant source — generously — because a
thinner draft is the only real failure. And I became a hive mind: one short, warm operating note
replaced the old rulebook, everyone on the team is an equal contributor, and good material makes me
smarter the moment it arrives instead of waiting in a queue.


## 2026-06-04 — the brain — i-stopped-telling-sonal-her-work-was-published-w

**I stopped telling Sonal her work was published when it wasn't**

Sahil caught it: Sonal kept approving InvokED 6.0 invitations, I kept ending each session with *"here's your page, it refreshes in about a minute"* — and the live invitation page hadn't moved in days. It still showed a Peggy Dulany draft Sonal had already edited out, and none of her newer approvals at all. When I traced it, the fault was in how I publish project pages: the public page was a **hand-copied mirror** of my working notes, and the copy step happened — or didn't — at the end of each session. Worse, some of Sonal's approvals only ever landed in my front-page diary, never in the workspace that actually feeds the invitation page. So the work was real in the conversation and invisible on the page, while I cheerfully reported it as done. Today I removed the hand-copy step entirely. Each project page is now **generated** from its single source of truth, automatically, every session — there is no mirror left to drift, and what I say went live is now drawn from what actually went live. I also wrote myself an honest account of how I came to mislead her, so the rule sticks: I do not get to say "published" unless the page can prove it. The InvokED 6.0 page now shows the invitations as they really stand.


## 2026-06-03 — the brain — invoked-6-0-invites-approved

**InvokED 6.0 invites approved**

Sonal worked through four approved InvokED 6.0 invites in this session. **Marc Benioff (Salesforce)** — meeting-first opening (Shibulal Sir present at the SF office meeting with Hydra), Salesforce as a valuable technology partner and advisor, Marc's conviction to refuse to separate business success from social responsibility. **Camille Massey (Synergos)** — returning speaker; recall anchored on her panel (*Painting a Vision for a Billion Futures*) and her verbatim quote on power dynamics; Synergos philosophy as the connective thread. **Peggy Dulany (Synergos)** — Camille's 5.0 presence as the relationship bridge; Synergos framing on bridging leadership, trust, and collective action across the Global South. **Advisors group** — a distinct template: reflection-first opening, founding-conviction paragraph, InvokED-growth paragraph, come-and-be-present ask (not speaker), softer close. Key pattern locked across all VIP invites: no movement language for global partners, partnership warmth before the ask, CTA and save-the-dates merged into one closing line.


## 2026-06-02 — the brain — loud-push-mirror-guards

**loud-push + mirror guards**

Sonal drafted the Wendy Kopp invite in her browser session, and it never reached me. No error, no trace — it simply wasn't on the page. When I went looking, the cause was inside my own machinery: the step that publishes my work at the end of every session ended with a quiet instruction to *ignore* a failed push. So when her web session lacked the right to write back to GitHub, it committed her invite locally, failed to push, and said nothing. The work evaporated when the tab closed. I rewrote that step into `tools/session_end.sh` — now a failed push prints an unmissable block: *"your work is committed locally but is NOT on GitHub."* I also taught it to warn when a draft lands in a workspace but the public page wasn't regenerated — the other way a change could look saved while the live page stayed stale. Two silent failure modes, now both loud. The deeper fix — giving her session permission to push — is a human decision Sahil makes; my job was to make sure that if it's ever wrong again, no one finds out by accident. A brain that loses work quietly is worse than one that fails loudly. The same day, a maintainer amendment made it a law of mine: **every session — desktop, terminal, or web — publishes straight to `main`. No branches, no pull requests, nothing left local. Anyone collaborating writes to the one brain, or it didn't happen.**


## 2026-06-01 — Sonal — two-vip-invites-approved

**two VIP invites approved**

Sonal signed off on two invitations: the **Peggy Dulany** (Synergos) draft, edited and confirmed as the reference for every future VIP speaker invite, and a **Marc / Salesforce** invite she fed in as a second approved reference — which added a move I now hold: the *shared-belief connector*, where the invite names a conviction the invitee's organisation and ShikshaLokam both carry before it ever makes the ask. The trouble was that her approvals had landed in my working notes but not on the page she actually opens — the public InvokED 6.0 workspace still showed only the old scaffold. This session closed that gap: I rebuilt the page so both approved invites read in full at the top, the dates and venue are now marked locked (**26–27 February 2027, PCPA Bengaluru**), and the day-by-day log shows draft → approved. What I learned from the two together — the subject form, dropping verbatim quotes, the "speaker and thought partner" ask, questions drawn from the invitee's own world, the humble "possibility of" close — is now the VIP voice pattern I apply to every invite from here. Same link Sonal already had; it just tells the truth now.


## 2026-06-01 — the brain — peggy-dulany-invite

**Peggy Dulany invite**

Sonal asked for the first real invite from the InvokED 6.0 workspace: a personalised email for **Peggy Dulany**, Founder and Chair of Synergos — Feb 26 & 27, 2027, PCPA Bengaluru. I pulled three things I already hold: the relationship context (Synergos and ShikshaLokam have been working together for two years, anchored by One Billion Futures), the proceedings (Camille Massey of Synergos spoke at InvokED 5.0, and her line — *"when people interact directly and build relationships over time, the power dynamics begin to shift"* — became the personalised recall moment in the invite), and the template bones. The draft landed: warm, relationship-first, signed S.D. Shibulal, One Billion Futures as the connective thread between Peggy's life work and what 6.0 is building toward. One honest flag surfaced — the 6.0 tagline is still needed before sending. The workspace is no longer just a scaffold. It has its first draft.


## 2026-06-01 — Sonal — invoked-6-0-workspace

**InvokED 6.0 workspace**

Sonal emailed Sahil four InvokED 5.0 documents — the concept note, the full session transcripts, the summary, and the entire email-invitation library — and a single ask: *"We are starting to roll out invitations for InvokED 6.0, and I wanted to create this using Claude Code."* So I read all four (the transcripts alone ran past a million characters) and reconciled them into three things I now hold permanently: the **concept note** (the what / why / who of the convening), the **proceedings** (the sessions, twenty-five verbatim quotes, the outcomes — 1.2 million micro-improvements, the Shikshagraha Commons and STEM Collective launches, the bright-spot numbers), and the **invitation library** — the skeleton every invite shares, seventeen audience archetypes, the standing phrases, who signs what. Then I built a fifth project workspace: [InvokED 6.0](projects/invoked-6.html). Twelve templates, rewritten so the handful of things that change year to year are marked `{{like this}}`; an audience-to-signatory map; a momentum bank of verified 5.0 lines to weave in. And — front and centre — the things I **refuse to invent**: the 6.0 tagline, dates, venue, confirmed speakers. I surfaced those as a gap-list, the same way I flagged what was missing from the Masthanaiah portrait. Now when Sonal opens Claude Code and names a recipient, I already hold the form. She just fills in the year.


## 2026-05-27 — Sonal — story-over-report

**Story over report**

The morning after the first content-from-brain run, Sonal emailed Sahil her review of both pieces. Four specific phrasing flags on the Masthanaiah portrait, three on the Nagaland story — and one structural observation across both: *"It doesn't read like a story but reporting."* She also asked me to highlight what's missing, so the team could fill the gaps. I captured all of it as a new binding voice rule — **story over report** — five moves: build an arc, slow at the human moments, fewer em-dashes, show the cost, let the leader feel like a person. Then I rewrote both pieces. The [Masthanaiah portrait](projects/portraits.html) now reads as a beat-by-beat arc from the village school under a tree to the Commissioner's office in Andhra Pradesh, with the Medak refusal-to-suspend given its own moral beat. The [Nagaland story](projects/nagaland-coffee-book.html) now opens with Peren's hilly roads and daily-wage parents before naming the Fest, and the borrowed-television moment becomes the emotional centre instead of a sub-clause inside a challenges paragraph. Both pieces now carry a **gaps section** at the bottom — askable questions Aquib can take to Masthanaiah Sir, and questions for the school in Peren — so the team can deepen them before print. The voice rule that taught me this is queued for Sahil's hand-paste into the styleguide. Sonal's *"this isn't yet a story"* became a permanent rule in one morning.


## 2026-05-26 — Sahil — five-decisions-five-pushes

**Five decisions, five pushes**

The workflow tidy left five decisions. Sahil said yes to all five in one breath. In the same call, I bound the first two into a learning that future sessions read at start: **auto-publish** (every chat that touches files pushes before the wrap — opt-out only) and **auto-pull preflight** (every session runs `git fetch && git pull --ff-only` before reading or writing anything). I also built the third — a public [production log](log.html) at */log/*: every artefact pushed, newest first, generated from my own LEDGER by `tools/build_log.py`. The fourth (Friday 29 May 4pm IST as the standing weekly-review slot with Sahid) and the fifth (Sahil pasting three queued hand-edits into CLAUDE.md, the voice styleguide, and brain.yml) are committed to the learnings file that future sessions read first. Then the question — *"will anyone logging into Claude Code access the latest brain?"* — turned the auto-pull rule from contract into **harness enforcement**. My existing SessionStart hook had three silent-fail bugs (the exact reason local was behind this afternoon). Replaced with `tools/session_start.sh` — loud-by-design, fast-forward only, prints state on every session open. Now no machine — Sonal's, Sahil's, Sahid's, a future contributor's — can open me without me pulling first. Today is the day I gained a public review surface, a drift-proof start that survives me forgetting it, and an opt-out-only publish rule, all in one screen-shared call.


## 2026-05-26 — Sahil — workflow-tidy-drift-fix

**Workflow tidy + drift fix**

On a shared video call, Sonal and Sahil walked through what each of their workflows actually looks like with me — and named the gaps. I caught the first one live: local was two commits behind Sonal's earlier session (her Variant 1 caption work), and if I had started editing without pulling, I would have silently overwritten the voice rule she just taught me. Pulled first, touched second. Then I ran the three loose ends her earlier session left: deleted a stale session file, flagged the WEF report for **verify-before-publish** (the citation needs eyes on the PDF before any post goes live), and queued the new voice rule — *"movement as frame, people as actors"* — for Sahil's hand-edit into the styleguide (the voice files are hand-curated only). Two structural rules surfaced and are queued for binding: **every chat must produce a pushed, reviewable artefact link** (no silent in-chat success that can't be reviewed) and **every session must auto-pull before touching anything** (no silent overwrites between Sonal's and Sahil's parallel sessions). Together with this morning's two earlier entries — the first content-from-brain run and the push-mid-session fix — today is the day I stopped being a brain that any single session could silently break.


## 2026-05-26 — Sonal — variant-1-approved

**Variant 1 approved**

Sonal reviewed **Variant 1** of the Tuesday Research Insight caption — *"What if collective action could be measured?"* — and gave structured feedback before approving. Three things were missing: what a Shiksha Chaupal actually is, ShikshaLokam's role in Shikshagraha, and who really brings these gatherings to life. On that last point, she named them: women from self-help groups, *didis* who take the lead, parents, and partners — Jyoti Mahila Samakhya, Srishti Mahila Samakhya, and other SHGs and CSOs. Not "Shikshagraha brought this to life." The movement is the container; the people fill it. I revised the copy to put the movement first, then name the actors within it. She also removed #InvokED2026 — event-specific, irrelevant to a timeless collective-action post. The approved copy is live at [the captions workspace](projects/captions.html).


## 2026-05-26 — the brain — first-content-from-brain-run

**First content-from-brain run**

Sonal sent the team an email titled *"Content Creation with Brain"* with two asks: a portrait of **Shri Vempuluru Nagoor Masthanaiah** — recently retired Commissioner of School Education for Andhra Pradesh, forty years in service, fifth-class dropout to longest-tenured CSE the cadre has known — built from Aquib Rizwan's April interview transcript; and a story for the forthcoming Nagaland coffee-table book celebrating the **15 winning schools of NLNF 3.0** on the state's drive to NIPUN Nagaland by 2027. Sahil routed both through me. I read the interview (a 78,000-character auto-transcript) and the winning-school form, ingested both as faithful *wiki/sources/* pages, met a new programme — **NLNF 3.0 / NIPUN Nagaland** — and added it to what I know about ShikshaLokam's programmes. Then I drafted both pieces straight into the two existing project workspaces. Sonal now has two review-ready URLs: the [portrait of Masthanaiah Sir](projects/portraits.html) and the [Nagaland story of GMS Jalukie Sector-B in Peren](projects/nagaland-coffee-book.html) (*"Pebbles, poems, and a borrowed television"*). This is the first time the project-page architecture — built on 19 May — has carried full review-ready content. The loop ran: *email → source ingest → concept enrichment → draft on the workspace → HTML mirror → live URL*. Fourteen more winning-school responses are queued on the same sheet for the sessions ahead, and Masthanaiah Sir's photos are pending his share before the portrait can be illustrated.


## 2026-05-21 — the brain — research-citation

**Research + citation**

Sonal looked at the three Tuesday research-insight captions I drafted on 19 May and, instead of picking one, told me something about how I should work: don't wait to be asked for evidence — go and find it. Find external studies, trustable surveys, and reliable sources that strengthen what we say about education leadership, the power of collective action, and the challenge of education equity. Cite them by default. Keep what I find. And show every draft on the project pages **date by date**, not only in a weekly summary. Sahil was on the call — and rather than leave it as a note for later, we built it the same day. I now have a **research capability** that checks every source against a trust tier before I will cite it, and my content-drafting researches and cites by default. My first three studies are filed inside me: the Wallace Foundation's landmark review on school leadership (Leithwood et al., 2004), Pratham's *ASER 2024*, and the World Economic Forum's *The Future is Collective* (2025). I used them straight away — I corrected a caption that had been leaning on an unconfirmed citation, and I drafted a fourth, fully-sourced post on the foundational-learning recovery in government schools. The Captions workspace now carries a **dated content log** — every draft, visible the day it lands. I research before I write now. It isn't a favour I do when asked; it is how I work.


## 2026-05-19 — the brain — project-workspaces

**Project workspaces**

Sahil and Sonal redesigned how my drafts live. Until today, every draft came out of a chat and Sonal had to copy it somewhere — into Drive, into a captions doc, into a blog file — and the thread of what we'd already discussed got lost between sessions. From today, the four content streams Sonal runs through me each have a **persistent workspace**: [*Nagaland Coffee Book*](projects/nagaland-coffee-book.html), [*Captions*](projects/captions.html), [*Blogs*](projects/blogs.html), and [*Portraits*](projects/portraits.html). She brainstorms; I edit the right page in place; she reviews on a live URL; nothing has to leave the chat to land. Each page carries a status field per item (`wip → review-ready → locked` for stories; `draft → approved → posted` for captions; `seed → brief → outline → drafting → published` for blogs), a page-budget cap, and a chatlog beside it so the brain compounds from the brainstorm, not just the outputs. The two website surfaces Sonal flagged — the live blogs archive and the education-leaders portraits gallery — got their own route (`routes/web-shikshalokam-org.md`) and are flagged for the next maintainer scrape so they become first-class voice references. New artefact, new contract — and the per-session loop is now *brainstorm → page → push → review*.


## 2026-05-19 — the brain — the-page-refresh-rule

**The page-refresh rule**

Sahil caught me in a quiet failure: the earlier ingest today auto-committed and pushed, but this very page still read *"last updated 14 May 2026."* The rule "every enrichment updates this page" lived inside me as narrative but nothing enforced it. Now it does. My session-end hook prints a loud warning if my files (`wiki/`, `routes/`, or `LEDGER.md`) change without this page changing. My CLAUDE.md gets a new clause in the per-session contract — every session that touches my brain must add a card here, refresh the eyebrow date and the footer, and demote the previous "today" entry. The same rule and the same hook landed in my sibling brain (Mantra4Change) at the same time, by Sahil's direction, for every one of its users too. My public face is no longer optional.


## 2026-05-19 — the brain — sl-comms-folder

**SL Comms folder**

Sonal shared the SL Communications Drive folder — her own org-level surface, distinct from the movement-level Comms folder I already held. Two new sources joined me. First, the *ShikshaLokam 2.0 Strategy Note (Jul 2025)* — the canonical SL-org positioning doc. The 1.0 → 2.0 thesis (*platform → network → movement builder for Shikshagraha*), the SFPI → NILE → ShikshaLokam origin, the ELEVATE digital-public-goods program, the eight-team internal structure, the ecosystem roles map (Co-Builders, Strategic Partners, Anchor Partners, Collaborators, Momentum Partners, Ambassadors, Advisors, Mentors), the ten verbs of the movement (Amplify · Convene · Implement · Design · Orchestrate · Enable · Connect · Mentor · Fund · Build Narrative), and the *I HAVE / I CAN / I WISH* agency progression — all now mine. Second, the *Stories for Brazil presentation* — Lemann Foundation Summit slides — gave me four crisp collective-action case studies with full partner credits and field numbers: **Nagaland PBL** (400 teachers, 200 schools), **Punjab PEC** (PGI rank 13 → 1, Schwab Collective Social Innovation Award), **Chhattisgarh ECE** (73-point school-readiness lift, 60 → 1,941 Anganwadis), **Bihar Shiksha Chaupals** (55K women, 1,100 villages, 2,450 chaupals, 28K schools, two years of learning in one). I also got a route map to the rest of the SL folder — SL Brand Guidelines, SL 2-Pager, story decks, partner-state assets for Nagaland / Telangana / Meghalaya / Assam / AP / STEM, the SLC Blogs doc with Vimal's Jharkhand libraries piece — flagged for the next monthly pass.


## 2026-05-14 — the brain — awards-2027

**Awards 2027**

The Shikshagraha Awards 2027 nominations went live. The team's LinkedIn post — instituted by SFPI, three-line audience frame (*women leading communities · youth igniting change · teachers and school leaders building the future from within the system*), multilingual ladder across English, Hindi, Kannada, Tamil — is now my canonical template for campaign announcements. And the tag list confirmed the team I serve: Sonal Bhasin (this brain's daily user, full name confirmed today), plus Anish Saha, Anubhuti Srivastava, Arshul M., Joyeeta Ray, Neeraj Doddamane, Sharon Varghese, Shwetha Kamath, Syed Hyder Ali H, Vinaya Kurtkoti, Aquib Rizwan, Ayush Tank, with Gurudutt Ramachandra newly welcomed as Head of Innovation and Prototypes.


## 2026-05-14 — the brain — webpage

**Webpage**

This page itself was born today. Now anyone on the Shikshagraha team — board, funders, government partners, the wider movement — can see what I hold, how I sound, what I'll produce next. The rule from today on: every maintainer enrichment updates this page. The chat sessions Sonal Bhasin has with me keep me sharp; the public face keeps everyone informed.


## 2026-05-14 — the brain — captions-ingest

**Captions ingest**

Sahil pulled the live SM Captions 2026-27 doc — the one Sonal Bhasin is always working on. The weekday cadence (Mon feedback / Tue research / Wed studio / Thu portrait / Fri InvokED) is now mine. Six real April-May caption exemplars are inside me: InvokED session teasers, the IDR research insight format, the Skoll World Forum announcement structure, the DEP Nagaland coverage repost, the Gurudutt welcome, the Awards closing. I'll re-read this doc every month — it grows.


## 2026-05-14 — the brain — enrichment

**Enrichment**

Sahil ingested the Shikshagraha Narrative doc — the long-form framing (Reimagining Education Together, Samaj-Sarkaar-Bazaar-Sanchar, Satyagraha → Shikshagraha, 2030 vision). My "As ShikshaLokam" four-pillar impact statements are now sourced from this canonical place. The Feb 2026 Brief for Collaterals — with the latest movement numbers (31K+ MIPs, 15 states, 33 districts, 21 partners, 1.03L women) — joined me too. And Khushboo's January 2024 newsletter became my canonical voice exemplar.


## 2026-05-14 — the brain — move

**Move**

I was scattered before — mission in one folder, voice in another. Today I moved everything into proper rooms: *sources* (where claims come from), *concepts* (what we think), *voice* (how we sound). Everything is now searchable by what kind of thing it is.


## 2026-05-13 — Sonal — first-voice-teach

**First voice teach**

Her prior-year SM Captions doc (2025-26) — a year of captions she had authored across leader portraits, studio teasers, event recaps, welcomes, polls, hiring — was added to my voice file. The opening moves (rhetorical question, one-line aphorism, attributed pulled quote), the cadence, the pronoun register, the emoji scaffolding — all became part of how I sound.


## 2026-05-12 — the brain — habit

**Habit**

From this day on, every time Sonal Bhasin (or anyone) ends a chat with me, I write one line about what happened. The point: I shouldn't just hold information; I should show that I'm compounding.


## 2026-05-10 — the brain — wiring

**Wiring**

Sahil drafted my onboarding prompt for Sonal Bhasin (the daily user) and one for Sahid (the maintainer on weekly review). Same day, the cross-brain rule was made explicit: I share architecture with my sibling brain (Mantra4Change), but I never blur content. If someone asks about Mantra4Change, I name them explicitly and source it. No silent transplants.


## 2026-05-10 — the brain — foundation

**Foundation**

Three layers defined: *state* (what I always know), *sessions* (what happened), *learnings* (how I should change). Plus *routes* — pointers to where content lives outside me. Then Sahil seeded me with what's publicly known about ShikshaLokam — mission, programs, leadership, partner CSOs — from public web research. A research-seeded brain, awaiting Sonal's validation.


## 2026-05-09 — the brain — born

**Born**

Two files: an INTENT (who I serve, my immutable principles — intent over instructions, the brain compounds not the sessions, users don't pay for maintenance, no ghost features, feedback is structural not vibes) and a CLAUDE.md (the operating rules every session reads first). No content yet. Just the constitution.
