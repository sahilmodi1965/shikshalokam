---
project: linkedin-analytics
title: "LinkedIn archive + analytics + inference (Path A — export-based)"
_status: spec
last_updated: 2026-07-15
maintainer: Ayush Tank
daily_user: Ayush Tank
sources:
  - "Path A/B feasibility (in-session 2026-07-13) — LinkedIn Community Management API vs admin XLS export"
  - "[[../../wiki/voice/exemplars/sm-captions-2026-rhythm]] — captions already in the brain"
voice: "n/a — internal capability spec"
---

# LinkedIn archive + analytics + inference — Path A (no API approval)

**Goal.** Learn what actually works on our LinkedIn — turn our own post history into a
"what-performs" readout that sharpens future drafts and comms strategy. Not a scheduler; not
posting. **Pull our track record in.**

**Why Path A first.** The live Community Management API can read posts + analytics but is gated
(app review, business/use-case approval, wait). The admin **XLS export** delivers ~80% of the value
**today, zero approval.** Upgrade to the API later for full automation (Path B) if worth it.

## Inputs (both already available)
1. **Post metrics** — Page admin → **Analytics → Export → Updates** stream. One row per organic
   post: Impressions · Clicks · CTR · Reactions · Comments · Reposts. Pulls **up to 1 year at a
   time**, exports as **XLS**. Run once per year to backfill history.
2. **Captions** — already in the brain: the SM Captions Google Docs (2025-26 + 2026-27). The archive
   half is largely done; the export supplies the *numbers* to join against it.

## The build
1. **Land the export as data we can read.** Upload the exported file to Drive as a **Google Sheet**,
   then read it with the tool we already have — `gs.py sheet-read --id <sheet> --range 'Updates!A1:...'`.
   No new dependency, no XLS parser needed.
2. **Ingest + join.** Parse each row (post URL · date · the six metrics). Match rows to caption text
   by **post URL** (best) or **date/order** (fallback). Store as typed, sourced brain memory →
   `wiki/sources/linkedin-post-performance-<window>.md` (one dataset, `_status`-tracked).
3. **Tag each post** with features the write layer cares about: hook type (question / aphorism /
   pulled-quote), length, program/topic, CTA present?, emoji count, hashtag count, post type
   (portrait / teaser / event / welcome / milestone).
4. **Infer.** Correlate those features with engagement → a **"what works" readout**: which hooks,
   lengths, topics, CTAs, and post types land hardest.
5. **Feed back.** Distill findings into (a) a note the `shikshalokam-write` voice layer reads, so
   drafts lean toward what performs, and (b) a short **strategy summary** (what to make more of).

## Cadence
- **Monthly:** admin drops the latest Updates export → brain refreshes the dataset + readout.
- That manual step is the only cost of skipping the API. Path B removes it later.

## Honest caveats
- **Caption↔metric matching** is imperfect when multiple posts share a day — post URL in the export
  fixes most of it; the rest is light manual matching.
- **Directional, not statistical.** With ~150–180 posts/year the readout shows tendencies, not proof.
  Frame findings as "leans," never laws.
- **Export text is thin** — the native export is metrics-first; full caption text comes from our own
  captions docs, which is why the join matters.

## Definition of done (v1)
- One `wiki/sources/linkedin-post-performance-*.md` dataset in the brain, joined + tagged.
- A one-page "what works on our LinkedIn" readout.
- A voice-layer note so the next draft already reflects it.

## Later — Path B (automation, optional)
Register a developer app → apply for the **Community Management API** product (needs business legal
name, address, website, privacy policy, approved use case) → 2-legged OAuth reads posts + page
statistics automatically, retiring the monthly manual export.
