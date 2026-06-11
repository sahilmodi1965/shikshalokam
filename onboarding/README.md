# Joining the ShikshaLokam brain

The brain is a **hive mind for content** — a shared AI partner for the team's writing. Everyone who
joins is an **equal contributor**: same access, same trust, no tiers, no one to wait on. Anyone can
ask it to write, drop something good into it, or correct it — and it gets smarter for everyone.

Two things make it safe and easy:
- **You never touch git, files, or commands.** You just talk to it. Saving and publishing happen for
  you, invisibly, every session.
- **The published site can't drift.** It's generated from the brain's real content and checked at
  every turn, so what the team sees is always the truth.

## Adding a teammate (roster-driven — any contributor can do this)

1. Open `brain.yml` and add them under `team:`:
   ```yaml
   team:
     - name: "Their Name"
       email: "their-git-email@org"   # the email their commits are signed with
   ```
2. That's it. The brain now recognizes them as a full, equal contributor, and the session checks
   attribute their work correctly. Send them **`onboarding/first-session.md`** to get set up.

No maintainer needs to approve it; there is no dependency on any one person.

## The docs here
- **`first-session.md`** — a friendly, one-time setup so a new teammate can open the brain and just
  start working. After that, every session is zero-ops.
- **`gsuite-setup.md`** — switch on Google for the brain (Gmail/Drive/Docs/Calendar). Part A is a
  one-time team setup (Sahil); Part B is each teammate's 60-second login. Optional — do it when you
  want the brain to draft emails and generate approved Docs into the shared folder.
- **`README.md`** (this file) — the model + how to add someone.

Historical onboarding (the earlier tiered, `state/`-based model) is preserved under `archive/` —
superseded, kept for provenance.
