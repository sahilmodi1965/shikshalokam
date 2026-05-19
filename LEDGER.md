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
