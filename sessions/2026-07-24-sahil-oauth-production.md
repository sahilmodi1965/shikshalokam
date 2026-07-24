---
date: 2026-07-24
person: Sahil Modi
project: gsuite-engine
title: "OAuth app published to production; ownership handed to Ayush, Aquib, Sonal"
_status: complete
---

# What got made

Issue #5 (OAuth app stuck in Testing) resolved end to end.

- **App published: Testing → In production** in the Google Auth Platform console
  (project `shikshalokam-brain`). Two pains fixed at once: social@shikshalokam.org
  can now log in (the 403 for non-test-users is gone), and refresh tokens stop
  force-expiring every 7 days — no more weekly browser re-consent for the team.
- **Ownership handed over.** Owner invites sent via IAM to ayushtank@, aquib@ and
  sonal@shikshalokam.org; each becomes a project owner on accepting Google's email.
  Ayush is the issue owner going forward.
- **Docs:** `onboarding/gsuite-setup.md` gained step 3b — Testing vs Production
  publishing status, why Testing 403s non-test-users and expires tokens weekly,
  and the one-time "unverified app" screen after publishing (Advanced → Continue).
- **Hygiene fix:** `tools/gsuite/oauth_client.json` was tracked in git despite the
  "no secret ever touches git" rule (the gitignore landed after the file). Untracked
  now; the file stays local + in the private Drive folder. Old secret remains in git
  history — rotating the OAuth client is noted on issue #5 as optional follow-up.

# What we learned

- **Testing-mode OAuth apps are a hidden tax.** Google force-expires their refresh
  tokens every 7 days and blocks anyone off the test-user list. The weekly re-login
  everyone treated as normal was one console click away from gone.
- **The new console moved the button.** "Publish app" now lives under Google Auth
  Platform → Audience, not the old OAuth-consent-screen page — the docs now point
  at the right place.
- **A gitignore rule doesn't untrack an already-committed file.** Worth a lint-style
  check: files matched by .gitignore that are nonetheless tracked.

# What's next

- Ayush/Aquib/Sonal accept the owner invites; social@ logs in; InvokED invites go out.
- Everyone re-runs `gs.py login` once past the one-time unverified screen.
- Optional: rotate the OAuth client and re-upload the JSON to the private Drive folder.
