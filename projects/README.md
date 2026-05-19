---
type: convention
_status: research-seeded
last_updated: 2026-05-19
maintainer: Sahil Modi
daily_user: Sonal Bhasin
---

# Project pages — convention

Each `projects/<slug>/` is a **persistent enrichable workspace** for one ShikshaLokam content project. This is a third artefact class alongside the four already in the brain:

| Artefact class | Lives at | Role |
|---|---|---|
| State | `wiki/**` | What the brain knows. Typed, `_status:`-tracked. |
| Session | `LEDGER.md` | What happened, append-only. |
| Learning | `learnings/<date>-<topic>.md` | How state changes. |
| Route | `routes/*.md` | Where external content lives. |
| **Project** *(new — 2026-05-19)* | **`projects/<slug>/`** | **A live, enrichable workspace for one content stream.** |
| Self-portrait | `docs/index.html` | The public face. |

Project pages bridge the **chat-driven creative loop** (Sonal brainstorming) and the **state-driven knowledge layer** (`wiki/`). Drafts no longer get copy-pasted out of the chat — they accrue in `page.md` and are mirrored to a styled HTML at `docs/projects/<slug>.html` that Sonal can review on the live site.

---

## Layout

```
projects/<slug>/
  page.md           # canonical, brain-readable source. Frontmatter + structured sections.
  chatlog.md        # append-only transcript of brainstorm threads per session.
  archive/          # overflow once page budget is hit (created on demand)
  drafts/           # long-form drafts that overflowed page.md (blogs only, for now)
  posted/           # confirmed-posted content archive (captions only, for now)
```

Mirrored to:

```
docs/projects/
  style.css                       # shared styling (matches docs/index.html voice)
  index.html                      # projects landing page (links to the four below)
  nagaland-coffee-book.html
  captions.html
  blogs.html
  portraits.html
```

---

## The four current projects

| slug | What it holds | Status field values | Voice register |
|---|---|---|---|
| `nagaland-coffee-book` | Stories for the Nagaland coffee-table book | `wip` / `review-ready` / `locked` | Visual + story-led (CTB voice; see [[drive-sl-communications]] § Coffee Table Books, [[shikshalokam-brazil-stories-may2026]] § Nagaland PBL) |
| `captions` | Rolling option pool grouped by the weekday rhythm | `draft` / `approved` / `posted` | Caption voice (see [[styleguide]] § Caption form, [[captions]]) |
| `blogs` | Idea queue + WIP draft synopses | `seed` / `brief` / `outline` / `drafting` / `published` | Long-form first-person field reportage (Vimal Jharkhand pattern) |
| `portraits` | One section per education leader | `wip` / `review-ready` / `locked` | Third-person, leader-foregrounded (see [[web-shikshalokam-org]] live gallery) |

---

## Per-session contract

When Sonal opens Claude Code with a project in mind (named explicitly or implied), every session follows this shape:

1. **Route** — Claude identifies which project the chat is about. If ambiguous, asks one short question.
2. **Load** — Reads `projects/<slug>/page.md` (always cheap — under page-budget cap). If voice work is in play, reads the matching `wiki/voice/exemplars/` via the brain-write skill's voice-layer budget.
3. **Enrich** — Edits `page.md` in place: adds new sections, refines existing ones, advances `status:` fields. The page is the artefact; chat is the means.
4. **Mirror** — Regenerates `docs/projects/<slug>.html` to reflect the new `page.md`. Until a build script exists (deferred), Claude dual-writes.
5. **Append** — Adds one entry to `projects/<slug>/chatlog.md` summarising this session's thread (so the brain compounds from the brainstorm, not just the outputs).
6. **Report** — Surfaces a tight summary to Sonal: section title + one-line on what changed + "push?"
7. **Confirm** — Sonal: yes → SessionEnd hook commits + pushes → Pages rebuilds in ~60s. Sonal can review the URL `https://sahilmodi1965.github.io/shikshalokam/projects/<slug>.html`.
8. **LEDGER** — One `LEDGER.md` entry covers the whole session (per INTENT principle 2 — the brain compounds, not the chat).

---

## Feedback affordances

Sonal can give signal in three ways:

| Signal | Detection | Action |
|---|---|---|
| Copies a section title back into chat | Title-string match | Implicit positive — advance `status:` (e.g. `wip → review-ready`), log to chatlog |
| "Use this" / "yes" / "perfect" | Confirmation language | Same as above; if voice rule applied, log voice-confirm note to chatlog |
| "Not my voice" / "feels off" / "ugh" / "rewrite" | Correction tone | Route to `learnings/<date>-<slug>.md` via brain-feedback. Do **not** silently rewrite — offer 2–3 alternatives in the next turn. Voice corrections discovered this way that look **structural** get promoted to `wiki/voice/**` by the weekly reviewer. |

---

## Page budgets

Each `page.md` carries `page_budget_tokens` in frontmatter (default 8,000). When a page approaches the cap, items overflow per-project:

- `captions` → flush `status: posted` items to `projects/captions/posted/<YYYY-MM-DD>.md` (weekly)
- `blogs` → flush full drafts to `projects/blogs/drafts/<slug>.md`, keep one-line synopsis on page
- `nagaland-coffee-book` → flush `status: locked` stories to `projects/nagaland-coffee-book/archive/<YYYY-MM-DD>.md`
- `portraits` → flush `status: locked` portraits to `projects/portraits/archive/<YYYY-MM-DD>.md`

The maintainer's monthly pass runs `wc -w projects/*/page.md` and triggers overflow if any page is over budget.

---

## Cross-cutting rules (binding)

1. **`page.md` is the source of truth.** The HTML mirror at `docs/projects/<slug>.html` is rendered from it. If they drift, `page.md` wins.
2. **One LEDGER entry per session, always.** Even a quick caption tweak counts. INTENT principle 2 is non-negotiable.
3. **Voice corrections route to `learnings/`, not directly into `page.md`.** CLAUDE.md rule 8 (voice is hand-curated) still binds. The exemplar lives in `wiki/voice/**`; this project page only **applies** voice.
4. **No silent restructuring of `page.md` sections.** If the page shape needs to change (e.g. add a new rhythm slot), surface the proposal in chat first.
5. **The HTML mirror keeps Sonal's copy-back loop alive.** Section titles must be plain text she can highlight and paste. No markdown leakage. No HTML entities in titles.

---

## Why this layer exists

Captured in `learnings/2026-05-19-project-page-architecture.md`. Short version: the previous flow (chat → output draft → manual copy out of chat → paste into target doc → lose-the-thread → drop into Drive → forget which version is canonical) was bleeding context. The brain knew more than the user could carry. Project pages make the brain's contribution **persistent + reviewable + diffable** without putting Sonal through any extra ceremony.
