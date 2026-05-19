# 2026-05-19 — project-page architecture (new artefact class)

## What the user said

Sahil, after Sonal-and-Sahil chatted about the post-ingest flow:

> Projects and content you will generate using claude code — Nagaland coffee book stories, Daily captions (LinkedIn, Twitter X), Blogs, Portrait stories. Automate Design of this a project 2 — now what we want to do is Sonal should be chatting with her claude code and ideally we don't want her to copy the content from the chat but it should be updated in the artifact itself as new pages. One will be Nagaland coffee book project page where its work in progress so as she adds information you must enrich that page. One page for captions where based on the chat and feedback and need it generate options for her to see. Create a blog page as well where latest blog ideas are getting updated and enriched based on Sonal's chat. As well as portrait page. The ideal session going forward after we are enriching this system is that Sonal will brainstorm with you and you will create content within the page budgets so she can after every push commit confirmation from her after content ingestion and run can just review it. And ideally she should be able to copy the title and paste it back and give feedback to you as well. Either way every thing counts and the brain should enrich and get better from there.

## Structural or one-off?

**Structural.** Per INTENT principle 6.

This is not a one-off feature request — it is a redesign of how the brain hands content back to the daily user. The previous flow (chat → output draft → manual copy → paste into target doc → drop into Drive) bled context: the brain held more than Sonal could carry between sessions, the working state lived in a chat transcript that's hard to scan, and the brain had no place to compound from the *brainstorm itself*.

The new flow makes the artefact persistent: chat is the means; the page is the artefact. The brain compounds on every session because (a) the page itself accrues, (b) a chatlog appended alongside captures the brainstorm thread, (c) the LEDGER continues to carry the daily entry, and (d) the existing learnings → weekly-review → wiki pipeline still applies for structural corrections.

## What changed (in this session)

### 1. New artefact class — `projects/<slug>/`

Five projects scaffolded as workspaces (this is in addition to the four artefact classes already in the brain: state / session / learning / route — plus the self-portrait `docs/index.html`):

```
projects/
  README.md                                 # the convention (binding)
  nagaland-coffee-book/  page.md  chatlog.md
  captions/              page.md  chatlog.md
  blogs/                 page.md  chatlog.md
  portraits/             page.md  chatlog.md
```

Each `page.md` carries: `_status:`, `page_budget_tokens:`, `voice:` (wikilink to styleguide register), `sources:` (wikilinks), `shareable_url:`. The body has structured sections that map to the project's content units (stories / caption variants / blog ideas / portrait cards).

### 2. Styled HTML mirrors at `docs/projects/`

Shared `style.css` (matches the visual language of `docs/index.html` — Fraunces + Inter, palette, spacing), plus an `index.html` landing page and one HTML per project. Each page is the **review surface** Sonal lands on after push. URLs:

- https://sahilmodi1965.github.io/shikshalokam/projects/index.html
- https://sahilmodi1965.github.io/shikshalokam/projects/nagaland-coffee-book.html
- https://sahilmodi1965.github.io/shikshalokam/projects/captions.html
- https://sahilmodi1965.github.io/shikshalokam/projects/blogs.html
- https://sahilmodi1965.github.io/shikshalokam/projects/portraits.html

### 3. Per-session contract (binding, applies to every future session)

Captured in `projects/README.md`:

> 1. Route to the project from intent or naming.
> 2. Read `page.md`; pull voice exemplar only if voice work is in play.
> 3. Edit `page.md` in place — add / refine / advance section status.
> 4. Mirror to `docs/projects/<slug>.html` (dual-write until a build script lands).
> 5. Append one entry to `chatlog.md`.
> 6. Report to user: title + one-line + "push?".
> 7. On confirm → SessionEnd hook commits + pushes → Pages rebuilds.
> 8. One `LEDGER.md` entry covers the whole session.

### 4. Feedback affordances

- **Sonal copies a section title back into chat** → implicit positive, advance status (e.g. `wip → review-ready`).
- **"use this" / "yes" / "perfect"** → confirmation language, same as above; voice rule applied logged to chatlog.
- **"not my voice" / "feels off" / "rewrite"** → routes to `learnings/`, no silent rewrite; 2–3 alternatives in next turn. Structural voice corrections promoted to `wiki/voice/**` by the weekly reviewer.

### 5. New sources / routes

- `raw/2026-05-19-project-pages-brief.md` — Sahil's brief captured verbatim.
- `routes/web-shikshalokam-org.md` — **new route** for the two public website surfaces Sonal flagged (live blogs archive, live portraits gallery). Both pending maintainer scrape.
- `routes/drive-sl-communications.md` § Blogs — appended **SLC Blogs 2026 WIP** doc (Sonal's current-cycle working doc, distinct from the 2025 doc already routed).

### 6. Self-portrait refresh

`docs/index.html` gained a new top-of-timeline entry (this session's work) and a new `<section id="projects">` block listing the four workspaces with live links. Previous "today" entry from this same date demoted per the page-refresh rule.

## Target: CLAUDE.md (deny-listed — Sahil applies)

CLAUDE.md is in the maintainer-only deny list. The proposed amendment lives below for Sahil to apply manually. Suggested insertion point: under **The four artefacts that ARE the brain** (turning it into "the five artefact classes"), and a new sub-section under **Per-session contract** for project-page routing.

### Suggested diff for `CLAUDE.md`

Replace the artefact table with:

```markdown
| Artefact | Lives at | Role | Who writes |
|---|---|---|---|
| **State** | `wiki/{sources,entities,concepts,synthesis,voice}/*.md` | What the brain knows. Typed, frontmatter-contracted, `_status:`-tracked. Read on every session. | Compile-step OR weekly-reviewer OR maintainer PR. Never the daily user mid-session. |
| **Session** | `LEDGER.md` (single file, append-only) | What happened. One entry per session. | Claude at session end, automatically. Lint enforces. |
| **Learning** | `learnings/<date>-<topic>.md` | How state changes. Audit trail of every correction the daily user surfaced. | Claude at session end when a correction occurred. Promoted to state by weekly-reviewer. |
| **Route** | `routes/*.md` | Where content lives outside the repo (Drive, Notion, archives). Pointers, not content. | Maintainers, on the daily user's request, in weekly review. |
| **Project** *(2026-05-19)* | `projects/<slug>/page.md` + `chatlog.md`, mirrored to `docs/projects/<slug>.html` | Persistent enrichable workspace for one content stream. Sonal brainstorms; the page accrues; HTML mirror is the review surface. | Claude in-session, on Sonal's brainstorm. The page IS the artefact. |
```

Add a new clause to **Per-session contract → During**:

```markdown
- If the user's ask names or implies one of the four projects (nagaland-coffee-book, captions, blogs, portraits), **route to that project's `page.md`** rather than producing a one-shot draft. Edit the page in place; mirror to `docs/projects/<slug>.html`; append one line to `chatlog.md`. See `projects/README.md` for the binding contract.
- Drafts in chat without a project home stay in chat (one-off). A persistent workspace exists only for the four named projects until a future session adds another.
```

Add a new clause to **Behavior rules (binding)**:

```markdown
11. **Project pages are persistent artefacts, not outputs.** Do not write content for the four named projects into `output/` — write into `projects/<slug>/page.md` and mirror to HTML. `output/` is reserved for one-shot drafts that don't fit a project.
```

## Cross-references

- See `raw/2026-05-19-project-pages-brief.md` for the user's brief verbatim.
- See `projects/README.md` for the binding per-session contract on project pages.
- See `routes/web-shikshalokam-org.md` for the new web-surface route.
- Pairs with [[2026-05-19-page-update-every-session]] — both are this-session structural promotions to the per-session contract; both surface CLAUDE.md edits Sahil applies manually.
- Voice rule applies: any voice corrections that emerge from project-page work go through this `learnings/` pipeline, not silent edits to `wiki/voice/**` (CLAUDE.md rule 8).
