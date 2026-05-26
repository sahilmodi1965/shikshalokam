# Wiki compile log

Append-only record of compile-step runs. **Distinct from LEDGER.md** — `log.md` records what the compile-step did to `wiki/`; `LEDGER.md` records what the daily user did with the brain.

## 2026-05-14T00:00:00Z — migration
- Created wiki/ structure via content-brain overlay migration.
- No compile-step run yet (`brain.yml: compile_step: deferred`).

## 2026-05-19T00:00:00Z — Sahil enrichment pass — SL Communications folder
- Sonal shared the SL-org-specific Drive folder (id `1P-6AHbwLkkGqPOxydhwTyZKUM8U6LP66`).
- Added `routes/drive-sl-communications.md` mapping the SL-org folder (distinct from the movement-level Comms folder at `routes/drive-communications.md`).
- Added `wiki/sources/shikshalokam-2-strategy-note-jul2025.md` (_status: research-seeded) — SL 1.0 → 2.0 positioning. Fills SL-org-narrative gap.
- Added `wiki/sources/shikshalokam-brazil-stories-may2026.md` (_status: research-seeded) — four Lemann-summit collective-action case studies.
- Updated `wiki/index.md`, `wiki/sources/SOURCES.md`, `routes/drive-communications.md` cross-link.
- No `_status:` transitions on existing files. No `wiki/voice/**` edits (Vimal Jharkhand blog deferred — requires `learnings/` slug).

## 2026-05-21T00:00:00Z — Sahil maintainer build — research-evidence library
- Promoted `learnings/2026-05-21-research-citation-and-datewise-log.md` (Sonal's brain feedback) in a same-session maintainer build.
- New skill `.claude/skills/shikshalokam-research/` — verifies external studies against a trust tier, files them, returns the wikilink to cite.
- `.claude/skills/shikshalokam-write/SKILL.md` updated — research + auto-cite is now a default step for evidence-anchored content.
- Added three `wiki/sources/research-*.md` (all _status: research-seeded), first run of the research skill: `research-leithwood-leadership-2004`, `research-aser-2024`, `research-wef-future-is-collective-2025`.
- Updated `wiki/index.md` (new Research-evidence library sub-section), `wiki/sources/SOURCES.md`.
- No `_status:` transitions on existing files. No `wiki/voice/**` edits.

## 2026-05-26T00:00:00Z — Sahil maintainer pass — first content-from-brain run for Sonal
- Routed Sonal's email ("Content Creation with Brain") end-to-end: source ingest → concept enrichment → project-page draft → HTML mirror → review URL.
- Added `raw/2026-05-26.md` capturing the brief verbatim + provenance for both source drops.
- Added two `wiki/sources/*.md` (_status: research-seeded): `interview-masthanaiah-2026-04-20`, `nlnf3-gms-jalukie-sectorb-response-2026-05-07`.
- Updated `wiki/concepts/programs.md` § Active — added **Nagaland Literacy & Numeracy Fest (NLNF) 3.0 / NIPUN Nagaland** as a named program (was previously only present as the DEP / PBL macro story in Brazil-stories).
- Updated `wiki/index.md` (new sources registered) and `wiki/sources/SOURCES.md` (2026-05-26 section).
- Enriched two project workspaces in place:
  - `projects/portraits/page.md` — first real portrait card (Vempuluru Nagoor Masthanaiah), `status: review-ready`.
  - `projects/nagaland-coffee-book/page.md` — first real story card (GMS Jalukie Sector-B, Peren), `status: review-ready`; project intent re-anchored on NLNF 3.0 / NIPUN Nagaland as the canonical container.
- HTML mirrors at `docs/projects/{portraits,nagaland-coffee-book,index}.html` updated. `docs/index.html` self-portrait timeline updated.
- No `_status:` transitions on existing files. No `wiki/voice/**` edits.
