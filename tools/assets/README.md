# tools/assets — the asset factory

Turns brain content into **finished, on-brand assets** and pushes them where they live.
One engine: branded HTML → **headless Chrome** (auto-detected; Chrome or Edge) → PNG / PDF.
No extra Python deps. Brand styling = ShikshaLokam 2.0 palette, baked into the templates.

## The three tools

**Carousel generator** — slide spec → branded PNG slides + a combined PDF (LinkedIn/Insta).
```
python tools/assets/carousel.py tools/assets/carousels/<spec>.json
```
- Specs live in `carousels/*.json`: `{ "name", "size":[w,h], "slides":[ {type, kicker, headline, big, label, sub, cta} ] }`
- Slide `type`: `cover` · `stat` · `close`.
- Output → `tools/assets/out/<name>/` (slide_N.png at 1080×1350 + `<name>.pdf`).
- **Auto-pull from a page (no JSON):** `python tools/assets/carousel.py <page>.md --name <deck>` reads
  the `Carousel slides:` list straight from a brain page and builds the deck.

**PDF creator** — markdown → branded A4 PDF.
```
python tools/assets/pdf.py <input.md> [--out FILE.pdf] [--title "..."]
```

**Poster generator** — poster spec → branded 1:1 PNG (square; LinkedIn/Insta/print).
```
python tools/assets/poster.py tools/assets/posters/<spec>.json
```
- Spec: `{ name, size, eyebrow, hero:[lines], subhead, details, cta, register_link, footer }`
- QR: renders a real QR when `register_link` is a live URL, else a labelled placeholder.

**Drive push** — upload generated files to a Drive folder, as the logged-in teammate (idempotent: re-runs update, not duplicate). Needs `gs.py login` (Drive scope).
```
python tools/assets/push_drive.py <file-or-dir>... --folder <PARENT_ID> [--subfolder NAME]
```

## Example — the MItra impact carousel
```
python tools/assets/carousel.py tools/assets/carousels/mitra-impact.json
python tools/assets/push_drive.py tools/assets/out/mitra-impact \
  --folder 1rjYIErAuZdpCoML5WAz4LFKD9hWY-05h --subfolder "Generated assets"
```

## Decisions / still open
- **Canva — decided (2026-06-30): this renderer is the Canva replacement** for posters, carousels,
  and PDFs. No Connect-API setup; we own the pipeline end-to-end.
- **Website** — still open: publish assets to shikshalokam.org (WordPress REST API + application
  password) vs embed in the brain's own site. Needs scoping.
- **Polish (buildable anytime):** real QR generation + brand logos/fonts baked into templates;
  auto-pull carousel slides from `page.md` (skip the JSON step).
