#!/usr/bin/env python3
"""Generate docs/log.html from LEDGER.md + git log.

The production log page is the single review surface for the ShikshaLokam brain — every
artefact pushed, newest first, with direct links to the live pages and the one-line ask that
produced it.

This is the **first stub**. It does enough to keep the log accurate; future maintainer passes
should harden it (better URL extraction, commit-bundle grouping, error handling, tests).

Usage:
    python tools/build_log.py

Reads:
    - LEDGER.md (parses ## YYYY-MM-DD entries)
    - git log (date + commit subjects)

Writes:
    - docs/log.html

Convention: every session that appends a LEDGER entry should regenerate docs/log.html (either
by running this script or by hand-editing the top row in place). Per
learnings/2026-05-26-five-decisions-binding.md § Decision 2.
"""

from __future__ import annotations

import re
import subprocess
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LEDGER = REPO / "LEDGER.md"
OUT = REPO / "docs" / "log.html"

# ---------------------------------------------------------------------------
# Parse LEDGER.md

# Headings look like: ## 2026-05-26 — Sahil + Sonal — joint-call-workflow-tidy
ENTRY_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})(?:\s+(\d{2}:\d{2}\s*\w+))?\s+—\s+([^—]+?)\s+—\s+(.+)$")
URL_RE = re.compile(r"https?://[^\s)\]<>\"']+")


ENTRIES_MARKER = "<!-- Entries appended below this line. Newest immediately below. -->"


def parse_ledger() -> list[dict]:
    """Parse LEDGER.md entries.

    The LEDGER carries a literal template block above the actual entries. Everything
    above the ENTRIES_MARKER is preamble (intro + template + invariants); only what's
    below is real session entries. Splitting on the marker is the cleanest skip.
    """
    text = LEDGER.read_text(encoding="utf-8")
    if ENTRIES_MARKER not in text:
        # Fallback: try to find the last template block end ("```" then real entries).
        body = text
    else:
        _, body = text.split(ENTRIES_MARKER, 1)

    entries: list[dict] = []
    current: dict | None = None
    for line in body.splitlines():
        m = ENTRY_RE.match(line)
        if m:
            if current:
                entries.append(current)
            date, time, author, slug = m.groups()
            current = {
                "date": date,
                "time": time or "",
                "author": author.strip(),
                "slug": slug.strip(),
                "body": [],
                "urls": [],
            }
            continue
        if current is None:
            continue
        current["body"].append(line)
        for u in URL_RE.findall(line):
            if u not in current["urls"]:
                current["urls"].append(u)

    if current:
        entries.append(current)
    return entries


def extract_field(body: list[str], field: str) -> str:
    """Pull the one-liner after '- **<field>:**' (or '- *<field>:*') from an entry body."""
    needle = field.lower()
    for line in body:
        ls = line.lstrip()
        if ls.startswith(f"- **{field}:**") or ls.startswith(f"- *{field}:*"):
            return ls.split(":", 1)[1].strip().rstrip("*").strip()
        # Fallback: bare "Asked:" without bold
        if ls.lower().startswith(f"- {needle}:"):
            return ls.split(":", 1)[1].strip()
    return ""


# ---------------------------------------------------------------------------
# Render HTML

CSS = """
:root {
  --gold:#D4A24C; --cascara:#C26A4A; --indigo:#2A2D5A; --ink:#1A1B2E;
  --paper:#FAF6EE; --mist:#EDEAF5; --rule:#D9D5E0; --muted:#6E6A78; --sl:#2A2D5A;
}
* { box-sizing: border-box; }
html, body { margin:0; padding:0; }
body { font-family: 'Inter', -apple-system, system-ui, sans-serif; background: var(--paper); color: var(--ink); line-height: 1.55; }
h1, h2, h3 { font-family: 'Fraunces', Georgia, serif; font-weight: 600; line-height: 1.18; margin: 0; }
h1 { font-size: clamp(2rem, 4vw, 2.8rem); font-weight: 700; letter-spacing: -0.02em; }
h2 { font-size: 1.3rem; margin: 0 0 8px; }
.wrap { max-width: 1080px; margin: 0 auto; padding: 0 24px; }
.bar { position: sticky; top:0; z-index:50; background: rgba(250,246,238,0.94); backdrop-filter: blur(8px); border-bottom: 1px solid var(--rule); }
.bar-inner { display:flex; align-items:center; justify-content:space-between; padding: 14px 0; }
.mark { font-family: 'Fraunces', serif; font-weight: 600; font-size: 1.05rem; }
.mark .brand { color: var(--sl); }
.mark .sep { color: var(--rule); margin: 0 4px; }
.mark .project { color: var(--cascara); font-style: italic; }
.bar-back { font-size: 0.85rem; color: var(--muted); text-decoration: none; }
.hero { padding: 56px 0 32px; }
.hero .eyebrow { font-size: 0.78rem; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; color: var(--cascara); margin-bottom: 0.9rem; }
.hero .lede { font-size: 1.05rem; color: var(--muted); max-width: 720px; margin-top: 1rem; }
section { padding: 36px 0; border-top: 1px solid var(--rule); }
.day { margin-bottom: 28px; }
.day-head { font-family: 'Fraunces', serif; font-weight: 600; color: var(--indigo); font-size: 1.4rem; margin: 0 0 14px; }
.entry { background:#fff; border:1px solid var(--rule); border-radius:14px; padding:18px 22px; margin-bottom: 12px; }
.entry .head { display:flex; align-items:baseline; gap:14px; flex-wrap:wrap; font-size:0.85rem; color:var(--muted); }
.entry .head .who { color: var(--indigo); font-weight:600; }
.entry .head .slug { background: var(--mist); color: var(--ink); padding: 2px 9px; border-radius: 999px; font-size:0.74rem; letter-spacing:0.04em; font-family:'Inter'; }
.entry h2 { margin-top: 8px; }
.entry .ask { font-style: italic; color: var(--ink); margin: 6px 0 10px; }
.entry .links { font-size:0.88rem; }
.entry .links a { display:inline-block; margin-right: 12px; color: var(--sl); text-decoration: none; border-bottom: 1px dashed var(--cascara); padding-bottom: 1px; }
.entry .links a:hover { color: var(--cascara); }
footer { padding: 36px 0; color: var(--muted); font-size: 0.84rem; border-top: 1px solid var(--rule); }
footer a { color: var(--muted); }
"""


def filter_artifact_urls(urls: list[str]) -> list[str]:
    """Keep URLs that point to live, reviewable artefacts. Drop sources, repo paths, etc."""
    keep = []
    for u in urls:
        if "sahilmodi1965.github.io/shikshalokam" in u:
            keep.append(u)
    return keep


def render(entries: list[dict]) -> str:
    # Group by date
    by_date: dict[str, list[dict]] = {}
    for e in entries:
        by_date.setdefault(e["date"], []).append(e)

    today = datetime.now().strftime("%Y-%m-%d")
    parts: list[str] = []
    parts.append(
        f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Production log — ShikshaLokam brain</title>
<meta name="description" content="Every artefact the ShikshaLokam brain has pushed, newest first. Source of truth for review." />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<header class="bar">
  <div class="wrap bar-inner">
    <div class="mark">
      <a href="index.html" style="text-decoration:none;color:inherit;"><span class="brand">ShikshaLokam</span></a>
      <span class="sep">/</span>
      <span class="project">log</span>
    </div>
    <a class="bar-back" href="index.html">← the brain</a>
  </div>
</header>

<main>

<section class="hero">
  <div class="wrap">
    <div class="eyebrow">Production log — regenerated {today}</div>
    <h1>Every artefact, by the day it landed.</h1>
    <p class="lede">
      The single source of truth for what the ShikshaLokam brain has produced. Each row is one
      session bundle — what was asked, what landed, where it lives on the site. Newest first.
      Generated from <code>LEDGER.md</code> by <code>tools/build_log.py</code>.
    </p>
  </div>
</section>

<section>
  <div class="wrap">
"""
    )

    for date in sorted(by_date.keys(), reverse=True):
        date_h = datetime.strptime(date, "%Y-%m-%d").strftime("%-d %B %Y")
        parts.append(f'    <div class="day"><div class="day-head">{date_h}</div>\n')

        for e in by_date[date]:
            asked = extract_field(e["body"], "Asked")
            artefact_urls = filter_artifact_urls(e["urls"])
            link_html = "".join(
                f'<a href="{u}" target="_blank" rel="noopener">{u.replace("https://sahilmodi1965.github.io/shikshalokam/","").replace(".html","") or "self-portrait"}</a>'
                for u in artefact_urls
            )
            slug_clean = e["slug"].replace("`", "").strip()
            parts.append(
                f"""      <div class="entry">
        <div class="head">
          <span class="who">{e['author']}</span>
          <span class="slug">{slug_clean}</span>
        </div>
        <p class="ask">{asked or '<em>(see LEDGER entry)</em>'}</p>
        {f'<div class="links">{link_html}</div>' if link_html else ''}
      </div>
"""
            )
        parts.append("    </div>\n")

    parts.append(
        """  </div>
</section>

</main>

<footer>
  <div class="wrap">
    <p>Generated from <a href="https://github.com/sahilmodi1965/shikshalokam/blob/main/LEDGER.md">LEDGER.md</a> by <code>tools/build_log.py</code>.
    Source of truth: the LEDGER. This page: the public mirror. <a href="index.html">↩ the brain self-portrait</a></p>
  </div>
</footer>

</body>
</html>
"""
    )
    return "".join(parts)


def main() -> None:
    entries = parse_ledger()
    html = render(entries)
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT} — {len(entries)} entries, {sum(len(filter_artifact_urls(e['urls'])) for e in entries)} artefact links.")


if __name__ == "__main__":
    main()
