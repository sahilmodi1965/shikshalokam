# ShikshaLokam Brain — Architecture & Operating Model (v2)

_Last set: 2026-06-11. This is the current design. The earlier model is in `archive/ARCHITECTURE.md`._

## The mission
Turn a 3-person content team into **content architects** — humans own judgement (voice, strategy,
approval); the brain does the mechanical work (drafting, formatting, Docs/Sheets/email/calendar ops,
publishing). Goal: ~100x the team's output and transparency **without paid infrastructure** — only
what we already have: the **Claude Code plan**, **GitHub** (repo, Actions, Issues, PRs, Pages), and
**Google Workspace**.

## Non-negotiables
1. **Every session compounds.** No session ends without making the brain better — a draft produced,
   a lesson learned, feedback absorbed, a digest written. This is enforced, not hoped for.
2. **Nothing gets lost.** Two people on the same page doing different things must both land — work
   is queued, never overwritten.
3. **The brain speaks short, structured, managed-upwards** (see CLAUDE.md).
4. **Cheap + effective.** No paid servers/DBs. We may change the workflow many times, but it stays
   on free infra.
5. **Self-driving.** The system flags its own bugs/ideas as GitHub Issues and fixes them — no one
   chases anything on WhatsApp.

## The stack (only what we already pay for)
| Layer | We use | Cost |
|---|---|---|
| Authoring + reasoning | Claude Code (each person's plan) | already have |
| Source of truth + queue + CI + backlog | GitHub repo · Actions · PRs · Issues · Pages | free tier |
| Productivity actions | Google Workspace — Gmail, Docs, Sheets, Calendar, Drive | already have |

## 1. Source of truth + the queue (nothing lost)
- The **GitHub repo is the single source of truth** — only *source* lives here (wiki, projects,
  sessions, voice). Generated pages are never committed (CI builds them).
- Each session works on its **own branch → opens a PR → auto-merges** when checks pass.
- **GitHub merge queue** serializes merges: if two people touched the same page, the second PR is
  rebased on the first and re-checked before it lands. Different sections merge automatically; the
  brain reconciles the rare same-line overlap (it authored both). **Result: a real queue — both
  contributions land, in order, nothing overwritten.**

## 2. Every session compounds (the learning loop)
- A session that changes the brain **must** write `sessions/<date>-<who>.md` (what was made, learned,
  what to improve). The timeline, log, and LEDGER build from these.
- Good material is **absorbed into `wiki/` in-session** — sourced + typed, so the next draft is better.
- Corrections update **`wiki/voice/`** in the same session. The brain literally sounds more like us
  every time it's corrected.

## 3. Autonomous operations (no WhatsApp)
- **The system files its own work as GitHub Issues** — a bug hit, a friction noticed, an idea, a CI
  failure → an Issue with a label (`bug` / `feature` / `friction`), opened by the brain via `gh`.
- A scheduled Action + each session **triages the backlog**; the brain picks issues up, fixes them,
  and opens **auto-merging PRs**. Field-test "what's clunky" notes become issues automatically.
- **Self-healing:** auto-pull, auto-rebase, mid-rebase auto-recovery, CI build+deploy, build sanity
  check. A red CI run files an issue the brain resolves next session.

## 4. Productivity engine — Google Workspace (gated)
The brain acts **as the logged-in person** (token on their laptop, never in git):
- **Gmail** — draft → *you say send* → sent. (Batch: personalised drafts to many stakeholders.)
- **Docs** — generate approved content as a Google Doc.
- **Sheets** — read + update cells (trackers, caption sheets, status).
- **Calendar** — make events → *you say notify* → invites go out.
- **Drive** — **only after Sonal approves** → the approved Doc is written to the shared folder.

## 5. Publishing
On every merge to main, **GitHub Actions builds the site from source and deploys to GitHub Pages**.
The public site is the read-only **content board** — what exists, what version, what's approved.

## The gates (safety, always on)
- **Email send** and **calendar notify** need an explicit human yes.
- **Drive publish** needs **Sonal's explicit approval** (she is the approver; the repo is truth until then).
- **Branches + PRs** mean main is never edited live; the queue protects it.

## Cost
$0 beyond existing plans. Private-repo Actions minutes (≈2,000/mo free) cover build/deploy + triage
for a 3-person cadence. No Vercel, no database, no server.

## Workflow diagram
```
        ┌─────────────────────── THE COMPOUNDING LOOP ───────────────────────┐
        │   better drafts every session                                       │
        ▼                                                                      │
   ┌──────────────┐     absorb feedback + learnings      ┌──────────────────┐  │
   │ wiki + voice │◀─────────────────────────────────────│  SESSION          │ │
   │ what we know │                                       │  draft · learn ·  │ │
   └──────────────┘                                       │  digest (required)│ │
        ▲                                                 └─────────┬─────────┘ │
   PEOPLE (3 architects + Sahil) ── chat ──▶ CLAUDE CODE ───────────┘           │
                                              work on a branch │                │
                                                               ▼                │
                                        ┌────────────────────────────────┐      │
                                        │  QUEUE: PR + merge queue +      │ same │
                                        │  auto-merge — nothing lost,     │ page │
                                        │  same-page work serialised      │ ───▶ │
                                        └───────────────┬────────────────┘      │
                                                        ▼ merge to main          │
                              ┌──────────────────────────────────────┐           │
                              │   GITHUB REPO = SOURCE OF TRUTH       │           │
                              └───┬───────────────┬──────────────┬───┘           │
                  push triggers ↓  │               │              │ files issues   │
            ┌──────────────────────┐│               │              ▼  autonomously  │
            │ GH ACTIONS:          ││               │     ┌──────────────────────┐ │
            │ build + deploy       ││               │     │ GITHUB ISSUES = backlog│─┘
            │      ▼               ││               │     │ system flags + fixes   │
            │ GITHUB PAGES (board) ││               │     └──────────────────────┘
            └──────────────────────┘│               ▼ acts AS you, gated
                                     │   ── GSUITE ── Gmail▶send · Docs · Sheets · Calendar ·
                                     │                Drive (only on Sonal's approval)
                                     ▼
                              (humans approve · the brain does the rest)
```

## Roadmap to freeze
**Build now (this upgrade):** branch+PR+merge-queue+auto-merge · mandatory-digest enforcement ·
autonomous Issue filing + triage · Sheets in the GSuite engine · CI-failure→Issue.
**Then freeze.** All further change flows through **GitHub Issues the system files and fixes itself**,
with auto-merging PRs. Progress is documented here and in `sessions/` — automatically.
