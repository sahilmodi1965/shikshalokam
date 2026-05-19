---
type: route
purpose: "public website surfaces — shikshalokam.org/blogs and /education-leaders-portraits"
last_validated: 2026-05-19
maintainer: Sahil Modi
shared_by: Sonal Bhasin
shared_on: 2026-05-19
---

# shikshalokam.org — public web surfaces

The org's live public site carries two surfaces this brain must read against, since they are **canonical for already-published voice + existing portrait gallery**. Both pair with project workspaces in `projects/` and need a maintainer scrape pass before they become first-class wiki sources.

## Surfaces

### Published blogs
**https://shikshalokam.org/blogs/**

The canonical archive of published SLC blogs (long-form, third-person + first-person field reportage). Sonal flagged this 2026-05-19 as the enrichment target for the [[blogs]] project workspace. The brain currently holds **one** ingested blog exemplar (Vimal P. Thomas's Jharkhand piece, deferred from 2026-05-19 ingest) — this surface holds the full corpus.

Pairs with:
- [[blogs]] (project workspace) — the live page Sonal enriches
- [[drive-sl-communications]] § Blogs — Drive-side working docs (Blogs 2025, Blogs 2026 WIP)

### Education leaders portraits
**https://shikshalokam.org/education-leaders-portraits/**

The live portrait gallery — short-form leader profiles ShikshaLokam publishes as part of the Education Leaders Portraits series. Canonical for **portrait voice + format** (third-person, leader-foregrounded). Sonal flagged this 2026-05-19 as the enrichment target for the [[portraits]] project workspace.

Pairs with:
- [[portraits]] (project workspace) — the live page Sonal enriches

## Pending maintainer enrichment

Flagged for next monthly pass (Sahil $200 plan):

1. Scrape **https://shikshalokam.org/blogs/** — extract published blog list (titles, authors, dates, full text) into `wiki/sources/published-blogs-shikshalokam-org-<date>.md`. Pull 2-3 voice exemplars covering the **first-person field-reportage** register (Vimal Jharkhand pattern) and the **third-person institutional** register if present. Voice work requires a `learnings/` slug per CLAUDE.md voice rule.
2. Scrape **https://shikshalokam.org/education-leaders-portraits/** — extract the portrait gallery (each leader: name, role, location, hook, body, attribution) into `wiki/sources/portraits-shikshalokam-org-<date>.md`. Use the format to seed the portrait-section template inside [[portraits]] project page.
3. Cross-reference portrait names against the SL team roster and partner-state leader list to detect any leaders whose stories live in this brain elsewhere (e.g., Brazil presentation Nagaland/Punjab/Chhattisgarh leaders).

## How this brain uses these surfaces

Until the maintainer scrape runs, the brain treats these URLs as **read-only references** the daily user (Sonal) can point to in chat ("frame this like the blogs page"). Once scraped, the wiki sources become full first-class voice + format references the [[blogs]] and [[portraits]] project pages read on every session.
