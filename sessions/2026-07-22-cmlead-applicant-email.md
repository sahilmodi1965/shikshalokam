---
date: 2026-07-22
who: Sonal Bhasin
slug: cmlead-applicant-email
seq: 37
---
# Session — 2026-07-22

## What got made
- **Email to all 1,398 Meghalaya CMLEAD Fellowship applicants**, in the voice of the State Project
  Director, Samagra Shiksha. Thanks them for applying, owns the delay honestly (volume of
  applications, screening still running), states that only shortlisted candidates will be contacted,
  and gives the dates: interviews close last week of July 2026, 12 Fellows announced first week of
  August 2026. Doc: "CMLEAD Fellowship | Email to Applicants (SPD)", in `Meghalaya | CMLEAD Fellowship`.
- **A Meghalaya Drive tree** under the shared Brain Output root, with CMLEAD Fellowship, Reading
  Festival and State Programmes subfolders, registered in `tools/gsuite/drive_map.json`.
- **`gs.py drive-move`** — a new subcommand to file an existing Drive item into its proper folder.
  Filing was previously a manual step with no tool behind it.
- **`wiki/sources/meghalaya-cmlead-fellowship.md`** — the programme absorbed into the brain: design,
  eligibility, costs, the three launch voices, first-cohort numbers.

## What we learned
- **New standing rule from Sonal: manage Drive folders properly, always.** Everything the brain
  creates lands in its workstream folder, whoever created it, and Meghalaya content routes to the
  Meghalaya tree. Written into the `shikshalokam-gsuite` skill so it binds for the whole team, not
  just this session. The generic `Docs` folder is now a mistake to fix, never a default.
- **Government-voice content is its own register.** Candidate-facing mail from a department official
  is not SL caption voice: formal but human, plain sentences, no marketing lift. The existing CM / EM
  / SPD launch scripts are the reference, and the SPD's "Dear Youth" opener sets the warmth level.
- **Don't write promises the department hasn't approved.** Cut "the first cohort, not the last" from
  the email because Year 2 is a July/August 2027 decision. Flagged the choice rather than making it
  silently.

- **Migrated the Meghalaya back-catalogue into that tree** — 37 items gathered (20 CMLEAD, 5 Reading
  Festival, 12 State Programmes), with a reversible manifest at
  `routes/meghalaya-drive-migration-2026-07-22.json` recording every item's original parent.

## What we learned (part two)
- **A teammate cannot move another teammate's Drive files.** 35 of 37 items returned
  `ownedByMe: false, canEdit: false` — Drive reserves reparenting for the owner or an editor. The
  honest outcome is **shortcuts** in the destination folder pointing at originals that stay put.
  Only 2 were real moves. This is a permission fact, not a bug to retry; the real fixes are the
  owners moving their own files, ownership transfer, or a Shared Drive.
- **Some files must never be moved even when we can.** Media-coverage clippings, dated asset
  folders, and mixed-state folders (`Assam and Meghalaya Training`) belong to other maintained
  libraries. One media clipping got pulled in by a broad "Shillong" search term and was reverted to
  its `2022-2021` archive folder. Broad name-matching over-collects; check what a match actually is
  before filing it.

## Improve next
- The SPD's name is still missing; the email carries a `[Name]` placeholder until it arrives.
- The 35 shortcut'd Meghalaya files are still owned by kashmiri@, aquib@, vinaya@ and others. If the
  team wants genuinely consolidated storage, the owners need to move their own files into the tree,
  or hand over ownership, or the whole tree moves to a Shared Drive.
- The social post announcing the shortlist stage is still unwritten; the raw text exists in the brief.
