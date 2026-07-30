---
date: 2026-07-30
person: Sonal Bhasin
project: invoked-6
---

# InvokED 6.0 speaker pictures standardised, and three LinkedIn URLs found

Side task off the IEFG work. Five people for InvokED 6.0: Peggy Dulany (Synergos), Sanjay Purohit
(C4EC), Dr Santhosh Mathew (Gates Foundation), SD Shibulal, Shruti Shibulal.

## What got made
- **`6.0 Speaker Pictures` folder populated** — five images, all **1:1 at 1200x1200, each under
  200KB**, all normalised to `.jpg`.
- **Three LinkedIn URLs confirmed:** Peggy Dulany `/in/peggy-dulany-aab40334`, Sanjay Purohit
  `/in/purohitmsanjay`, Dr Santhosh Mathew `/in/santhoshmathewresearchpolicy`.

## Where the pictures came from
Four already existed in the master **Speaker Pictures** folder, which is the team's canonical set —
Sonal pointed there rather than letting the brain pick. Peggy Dulany was the only one missing; her
official headshot came from the Synergos site. Sonal had separately added a higher-resolution
portrait of her, and trashed the Synergos one, so the folder now holds one image per person.

## What we learned
- **Blind centre-cropping would have ruined half of these.** Four of six sources were landscape with
  the subject off-centre — Santhosh Mathew sits right of frame, Shruti left. Each crop point was set
  per image from the face position and checked visually before upload. **Never square-crop a
  portrait without looking at it.**
- **Filename is not a reliable guide to content.** The 2400x2400 files named "Sanjay Purohit" and
  "Shruti Shibulal" in *Speaker posters* are full promotional posters, not headshots; a 1748x1240
  "Ms. Shruti Shibulal.png" in *Speakers* is a thank-you card. Anything going into a picture folder
  has to be opened first.
- **LinkedIn cannot be scraped.** Direct fetches return HTTP 999, so only what search engines have
  indexed is visible. For Shruti Shibulal and SD Shibulal only company pages and posts *about* them
  surfaced, never their profiles. **That is a tool limit, not evidence a profile doesn't exist** —
  Sonal confirmed Shruti's does. Ask the person for the URL rather than guessing; a wrong LinkedIn
  link on an outbound invite reaches a stranger.
- **Two different people share the name Sanjay Purohit on LinkedIn.** `/in/sanjaypurohit` is the
  Group CEO of Sapphire Foods. The C4EC one is `/in/purohitmsanjay`. Same trap with Santhosh Mathew,
  where a second profile surfaces under "Antlegs".
- **Pillow was not installed** on this machine; installed via pip to do face-aware cropping. `sips`
  can only centre-crop, which was not good enough here.

## Next
- **Shruti Shibulal and SD Shibulal LinkedIn URLs** — Sonal to paste them in; then all five get
  recorded together.
- **Source quality:** Sanjay Purohit's original is 682x682 and Shruti's 1400x933, so both are
  upscaled at 1200x1200. Fine on screen, weak for print. Better source files worth requesting.
