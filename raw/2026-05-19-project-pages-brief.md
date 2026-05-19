---
type: raw
source: chat
captured_by: Sahil Modi
captured_on: 2026-05-19
intent: "stand up project-page workspaces so Sonal's chats enrich live artefacts in place"
---

# Brief — project-page architecture (from Sahil, 2026-05-19)

## Sources confirmed / re-shared

Verbatim links from chat (most already routed; listed here for traceability):

- **SL 2-Pager** — https://drive.google.com/file/d/1AfM9xxrCwg3ngkKFib2PurR5czXjXvEC/view  (already in [[drive-sl-communications]] § 2-Pagers, distinct file id)
- **Coffee Table — Micro Miracles 2.0** — https://drive.google.com/file/d/1lcm00kDhu9tUteiPCtjni-y3gspf3pRV/view  (already in [[drive-sl-communications]] § Coffee Table Books)
- **Coffee Table — Small Steps Volume II** — https://drive.google.com/file/d/1RXozBdzoQ-kW2gt7dWmd54MOWQfPyR9B/view  (already in [[drive-sl-communications]] § Coffee Table Books)
- **Blogs 2025** — https://docs.google.com/document/d/1ucPbxDxAPEjodc0LLkgkYx5MNtfmcWzX-CrMd3H7phQ/edit  (already in [[drive-sl-communications]] § Blogs — carries Vimal Jharkhand FINAL)
- **2026 Blogs WIP** — https://docs.google.com/document/d/1pLXmcCcMD2-v_eThOZT2ioRunchx4DFoTe_tpet0EqM/edit  **(new — added to [[drive-sl-communications]] § Blogs this session)**
- **Captions latest (2026-27 working)** — https://docs.google.com/document/d/1dc38xR0t8sPMgBb1FJiOjjqeSol5dDL2Tyk5ikz6n5w/edit  (already in [[captions]])
- **Captions last-year reference (2025-26)** — https://docs.google.com/document/d/1CBg6cYWPg-_r-HjU6ZCkjoRVYld6gpo_SKqN68wwEeQ/edit  (already in [[captions]])
- **Website blogs page** — https://shikshalokam.org/blogs/  **(new — routed at [[web-shikshalokam-org]] this session, pending maintainer scrape)**
- **Website portraits page** — https://shikshalokam.org/education-leaders-portraits/  **(new — routed at [[web-shikshalokam-org]] this session, pending maintainer scrape)**

## The architectural ask (Sahil's words, lightly normalised)

Four content projects Sonal will run through this brain going forward:

1. Nagaland coffee book stories
2. Daily captions (LinkedIn, Twitter / X)
3. Blogs
4. Portraits

The current flow — chat produces draft, Sonal copies out of chat — is being replaced. The new flow:

> "Sonal should be chatting with her Claude code and ideally we don't want her to copy the content from the chat but it should be updated in the artifact itself as new pages. One will be Nagaland coffee book project page where it's work-in-progress so as she adds information you must enrich that page. One page for captions where based on the chat and feedback and need it generate options for her to see. Create a blog page as well where latest blog ideas are getting updated and enriched based on Sonal's chat. As well as a portrait page. The ideal session going forward after we are enriching this system is that Sonal will brainstorm with you and you will create content within the page budgets so she can after every push commit confirmation from her, after content ingestion and run, just review it. And ideally she should be able to copy the title and paste it back and give feedback to you as well. Either way every thing counts and the brain should enrich and get better from there."

## Architecture decision (Sahil + Claude, this session)

- Page format: **styled HTML pages** at `docs/projects/<slug>.html`, mirroring `projects/<slug>/page.md` (the canonical source). Shareable URL: `https://sahilmodi1965.github.io/shikshalokam/projects/<slug>.html`.
- Per-session loop: chat → edit `page.md` in place → mirror to HTML → Claude reports + asks "push?" → Sonal confirms → SessionEnd hook commits + pushes → Pages rebuilds ~60s.
- Feedback affordance: each section in the HTML carries a copy-friendly title Sonal can paste back into chat as her "use this / fix this / not my voice" signal.

## What this raw entry triggered

Reified in this session into:
- `projects/` directory with four workspaces (`page.md` + `chatlog.md` each).
- `projects/README.md` documenting the per-session contract for these pages.
- `docs/projects/` with shared `style.css` + four project HTML pages.
- Learnings entry `2026-05-19-project-page-architecture.md` capturing the design decision for the next weekly review (so the project-page contract can be promoted into CLAUDE.md by the maintainer — CLAUDE.md is in the deny list and cannot be edited mid-session).
