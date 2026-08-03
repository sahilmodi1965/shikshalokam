---
date: 2026-08-03
person: Sonal Bhasin
project: iefg-membership
---

# IEFG application: three review rounds closed, and the numbers pulled from the live dashboard

## What got made
- **All review comments actioned** across three rounds. Green-highlighted checkboxes ticked, 1b cut
  by about half with every bullet and proof point kept, all bullets given a consistent "we" opener,
  and the Future Readiness Skill Index dated so it doesn't imply we already have it.
- **2h rebuilt from https://dashboard.shikshagraha.org**, including the dashboard URL itself so a
  reviewer can verify the claims rather than take them on trust.
- **Brain updated** so the application state survives this session: the working record and the
  denominator rule are both written down.

## The find
The dashboard is a JavaScript app, so fetching the page returns an empty shell. The data actually
comes from public JSON in a Google Cloud Storage bucket, reachable by reading the app bundle for its
storage config. Pulling that gave the live figures directly.

**The form's partner numbers were badly stale: 21 → 44 Momentum Partners, 9 → 15 Strategic
Partners.** Nobody would have caught that from the brain, which still held the February 2026 set.

## What we learned
- **A number without its denominator looks like an error.** The form carried "20L+ improvements" in
  one section and 1.57 million in another. Sonal's clarification: **over 2 million is everything SL
  has triggered since 2017; 1.57 million is what has happened since the Shikshagraha movement
  began** — a subset on a later clock. Both are now scope-labelled in the form, and the rule is
  recorded against the strategy note so it isn't rediscovered.
- **A dashboard's headline panel may be a target, not an achievement.** The dashboard shows "12
  states / 250 districts / 521,415 schools" directly beside live metrics, but that panel sits under
  "To impact at least 30% of India's states and districts by 2030." Reading it as current
  performance would have understated states and wildly overstated districts.
- **Check whether a string actually renders before calling it a problem.** A test label,
  "Voices of Change testing GCP update", sits in the dashboard's landing-page JSON. It was reported
  as public-facing; it is not — the carousel component takes `title` as an input and never binds it
  into its template. Worth tidying, not worth escalating. **Reading the data is not the same as
  reading the page.**

## Next
- Shwetha's response for 3b, and the 3a attachment. Neither has reached the brain.
- The Shiksha Samvaad impact line, and the yellow-highlighted checks.
- **The DNP / CWS comment on Digital Literacy stays open** — Sonal is holding it for leadership.
