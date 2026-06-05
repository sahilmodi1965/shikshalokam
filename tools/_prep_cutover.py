#!/usr/bin/env python3
"""ONE-TIME migration (2026-06-05 public-face cutover). Idempotent-ish: safe to re-run.

Splits the hand-authored docs/index.html into two SOURCE artifacts so the page can become
generated without losing a word:

  1. sessions/<date>-<slug>.md  — one file per existing timeline entry, carrying the entry's
     rich first-person narrative faithfully (the exact words, as markdown). This is the schema
     that henceforth feeds the timeline, the log, and the LEDGER rollup.
  2. tools/templates/index.shell.html — everything in index.html EXCEPT the timeline entries
     (hero, why, what-i-know, voice, outputs, projects, roadmap, chat, movement, footer), with
     {{TIMELINE}} where the entries go and {{LAST_UPDATED}} where the dates go.

After this runs, tools/build_site.py composes shell + generated-timeline -> docs/index.html.
Run from repo root: python3 tools/_prep_cutover.py
"""
from __future__ import annotations
import html
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INDEX = REPO / "docs" / "index.html"
SESS = REPO / "sessions"
TPL = REPO / "tools" / "templates"

MONTHS = {m: i for i, m in enumerate(
    ["January","February","March","April","May","June","July","August",
     "September","October","November","December"], 1)}


def date_iso(raw: str) -> str:
    # "4 June 2026" -> "2026-06-04"
    m = re.match(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", raw.strip())
    if not m:
        return raw.strip()
    d, mon, y = int(m.group(1)), MONTHS[m.group(2)], int(m.group(3))
    return f"{y:04d}-{mon:02d}-{d:02d}"


def html_to_md(s: str) -> str:
    s = re.sub(r'<a href="([^"]+)">(.*?)</a>', r"[\2](\1)", s, flags=re.S)
    s = re.sub(r"<strong>(.*?)</strong>", r"**\1**", s, flags=re.S)
    s = re.sub(r"<em>(.*?)</em>", r"*\1*", s, flags=re.S)
    s = re.sub(r"<code>(.*?)</code>", r"`\1`", s, flags=re.S)
    s = re.sub(r"\s+", " ", s).strip()
    return html.unescape(s)


def slugify(text: str, seen: set) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:48].strip("-") or "entry"
    slug, n = base, 2
    while slug in seen:
        slug = f"{base}-{n}"; n += 1
    seen.add(slug)
    return slug


def who_of(title: str) -> str:
    if title.startswith("Sonal"):
        return "Sonal"
    if title.startswith("Sahil"):
        return "Sahil"
    return "the brain"


def main() -> int:
    text = INDEX.read_text(encoding="utf-8")
    OPEN = '<div class="timeline">'
    start = text.index(OPEN) + len(OPEN)
    sec_end = text.index("</section>", start)
    inner = text[start:sec_end]

    arts = re.findall(r'<article class="tl-entry( today)?">(.*?)</article>', inner, flags=re.S)
    print(f"found {len(arts)} timeline entries")

    SESS.mkdir(exist_ok=True)
    TPL.mkdir(parents=True, exist_ok=True)
    seen: set = set()
    total = len(arts)
    for idx, (today_flag, block) in enumerate(arts):
        date_raw, small = re.search(r'<div class="tl-date">(.*?)<small>(.*?)</small>', block, re.S).groups()
        subtitle = re.sub(r"^\s*Today\s*·\s*", "", html.unescape(small.strip()))
        title = html_to_md(re.search(r"<h3>(.*?)</h3>", block, re.S).group(1))
        body = html_to_md(re.search(r"<p>(.*?)</p>", block, re.S).group(1))
        diso = date_iso(date_raw)
        slug = slugify(subtitle or title, seen)
        seq = total - idx  # top entry (idx 0) gets the highest seq -> sorts newest-first
        who = who_of(title)
        fm = (
            "---\n"
            f"date: {diso}\n"
            f"who: {who}\n"
            f"slug: {slug}\n"
            f"seq: {seq}\n"
            "live_urls:\n"
            "backfilled_from: docs/index.html timeline (2026-06-05 cutover)\n"
            "---\n\n"
            f"# {title}\n\n"
            f"**{subtitle}**\n\n"
            f"{body}\n"
        )
        (SESS / f"{diso}-{slug}.md").write_text(fm, encoding="utf-8")

    # --- carve the template shell ---
    before = text[:start]
    tail = inner[inner.rindex("</article>") + len("</article>"):]  # closing </div></div>
    after = text[sec_end:]
    shell = before + "\n{{TIMELINE}}\n" + tail + after
    shell = re.sub(r"(A self-portrait — last updated )([^<]+)(</div>)",
                   r"\1{{LAST_UPDATED}}\3", shell)
    shell = re.sub(r"(Last refresh: <strong>)([^<]+)(</strong>)",
                   r"\1{{LAST_UPDATED}}\3", shell)
    (TPL / "index.shell.html").write_text(shell, encoding="utf-8")
    print(f"wrote tools/templates/index.shell.html  ({len(shell)} bytes)")
    print(f"wrote {total} session files to sessions/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
