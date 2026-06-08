#!/usr/bin/env python3
"""tools/build_site.py — the ONE entrypoint that regenerates all generated outputs from source.

Drift-proof contract: docs/ is 100% generated, and so is LEDGER.md. Nothing here is hand-edited.
Run this (or `bash tools/verify_no_drift.sh`) any time to rebuild from source.

DETERMINISTIC + IDEMPOTENT: same sources -> byte-identical output. No wall-clock, no randomness;
every date is derived from the sources (session files / page frontmatter). Proof:
    python3 tools/build_site.py && python3 tools/build_site.py && git diff --exit-code docs/ LEDGER.md

Sources -> outputs:
  sessions/<date>-<slug>.md        ->  docs/index.html (timeline) + docs/log.html + LEDGER.md
  projects/<slug>/page.md          ->  docs/projects/<slug>.html   (every project with a page.md)
  tools/templates/index.shell.html ->  the static frame around the generated timeline

Self-heal (any session, fresh or resumed): python3 tools/build_site.py
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import build_project_page as bpp  # noqa: E402  (path set above)

SESSIONS = REPO / "sessions"
DOCS = REPO / "docs"
SHELL = REPO / "tools" / "templates" / "index.shell.html"
LEDGER = REPO / "LEDGER.md"

# Every project that has a page.md is generated — page.md is the single source of truth and the
# public HTML is a pure function of it (see tools/build_project_page.py). Deriving this list from
# the filesystem (rather than hard-coding one slug) is what keeps the no-drift guarantee honest:
# any project whose page.md changes is regenerated and drift-checked, with nothing frozen behind.
def _generated_projects() -> list[str]:
    return bpp.slugs_with_page()


# ---------------------------------------------------------------------------
# Session files — the single source for timeline, log, and the LEDGER rollup

def parse_session(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    meta: dict = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        fm, body = text[3:end].strip("\n"), text[end + 4:].lstrip("\n")
        cur = None
        for line in fm.splitlines():
            if re.match(r"^\s+-\s+", line):
                if cur:
                    meta.setdefault(cur, [])
                    if isinstance(meta[cur], list):
                        meta[cur].append(line.strip()[1:].strip())
                continue
            m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
            if m:
                k, v = m.group(1), m.group(2).strip()
                cur = k
                meta[k] = v if v else []
    lines = body.split("\n")
    title, subtitle, i = "", "", 0
    for j, ln in enumerate(lines):
        if ln.startswith("# "):
            title = ln[2:].strip()
            i = j + 1
            break
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines):
        ms = re.match(r"^\*\*(.+)\*\*$", lines[i].strip())
        if ms:
            subtitle = ms.group(1).strip()
            i += 1
    narrative = "\n".join(lines[i:]).strip()
    try:
        seq = int(meta.get("seq", 0))
    except (TypeError, ValueError):
        seq = 0
    live = meta.get("live_urls") or []
    if isinstance(live, str):
        live = [live] if live else []
    return {
        "date": str(meta.get("date", "")).strip(),
        "who": str(meta.get("who", "")).strip() or "the brain",
        "slug": str(meta.get("slug", path.stem)).strip(),
        "seq": seq,
        "live_urls": live,
        "title": title,
        "subtitle": subtitle,
        "narrative": narrative,
    }


def load_sessions() -> list[dict]:
    if not SESSIONS.exists():
        return []
    items = [parse_session(p) for p in SESSIONS.glob("*.md")]
    # newest first: by seq desc, then date desc, then slug for a stable total order
    items.sort(key=lambda s: (s["seq"], s["date"], s["slug"]), reverse=True)
    return items


def paragraphs(md: str) -> str:
    out = []
    for para in re.split(r"\n\s*\n", md.strip()):
        para = para.strip()
        if para:
            out.append(f"<p>{bpp.inline(para)}</p>")
    return "\n          ".join(out)


# ---------------------------------------------------------------------------
# docs/index.html — shell + generated timeline

def render_timeline(sessions: list[dict]) -> str:
    blocks = []
    for n, s in enumerate(sessions):
        today = " today" if n == 0 else ""
        sub = (("Today · " if n == 0 else "") + s["subtitle"]).strip(" ·")
        blocks.append(
            f'      <article class="tl-entry{today}">\n'
            f'        <div class="tl-date">{bpp.pretty_date(s["date"])}<small>{html.escape(sub)}</small></div>\n'
            f'        <div class="tl-body">\n'
            f'          <h3>{bpp.inline(s["title"])}</h3>\n'
            f'          {paragraphs(s["narrative"])}\n'
            f'        </div>\n'
            f'      </article>'
        )
    return "\n\n".join(blocks)


def build_index(sessions: list[dict]) -> str:
    shell = SHELL.read_text(encoding="utf-8")
    last_updated = bpp.pretty_date(sessions[0]["date"]) if sessions else ""
    out = shell.replace("{{TIMELINE}}", render_timeline(sessions))
    out = out.replace("{{LAST_UPDATED}}", last_updated)
    (DOCS / "index.html").write_text(out, encoding="utf-8")
    return "docs/index.html"


# ---------------------------------------------------------------------------
# docs/log.html — the production log, generated from session files

LOG_CSS = """
:root{--gold:#D4A24C;--cascara:#C26A4A;--indigo:#2A2D5A;--ink:#1A1B2E;--paper:#FAF6EE;--mist:#EDEAF5;--rule:#D9D5E0;--muted:#6E6A78;--sl:#2A2D5A;}
*{box-sizing:border-box;}html,body{margin:0;padding:0;}
body{font-family:'Inter',-apple-system,system-ui,sans-serif;background:var(--paper);color:var(--ink);line-height:1.55;}
h1,h2,h3{font-family:'Fraunces',Georgia,serif;font-weight:600;line-height:1.18;margin:0;}
h1{font-size:clamp(2rem,4vw,2.8rem);font-weight:700;letter-spacing:-0.02em;}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px;}
.bar{position:sticky;top:0;z-index:50;background:rgba(250,246,238,0.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--rule);}
.bar-inner{display:flex;align-items:center;justify-content:space-between;padding:14px 0;}
.mark{font-family:'Fraunces',serif;font-weight:600;font-size:1.05rem;}
.mark .brand{color:var(--sl);}.mark .sep{color:var(--rule);margin:0 4px;}.mark .project{color:var(--cascara);font-style:italic;}
.bar-back{font-size:0.85rem;color:var(--muted);text-decoration:none;}
.hero{padding:56px 0 28px;}
.hero .eyebrow{font-size:0.78rem;font-weight:600;letter-spacing:0.16em;text-transform:uppercase;color:var(--cascara);margin-bottom:0.9rem;}
.hero .lede{font-size:1.05rem;color:var(--muted);max-width:720px;margin-top:1rem;}
section{padding:30px 0;border-top:1px solid var(--rule);}
.day{margin-bottom:26px;}.day-head{font-family:'Fraunces',serif;font-weight:600;color:var(--indigo);font-size:1.4rem;margin:0 0 14px;}
.entry{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:18px 22px;margin-bottom:12px;}
.entry .head{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;font-size:0.85rem;color:var(--muted);}
.entry .head .who{color:var(--indigo);font-weight:600;}
.entry .head .slug{background:var(--mist);color:var(--ink);padding:2px 9px;border-radius:999px;font-size:0.74rem;letter-spacing:0.04em;}
.entry h3{margin:8px 0 6px;font-size:1.15rem;}
.entry p{margin:6px 0 10px;color:var(--ink);font-size:0.96rem;}
.entry .links a{display:inline-block;margin-right:12px;color:var(--sl);text-decoration:none;border-bottom:1px dashed var(--cascara);font-size:0.88rem;}
footer{padding:36px 0;color:var(--muted);font-size:0.84rem;border-top:1px solid var(--rule);}
footer a{color:var(--muted);}
"""


def build_log(sessions: list[dict]) -> str:
    by_date: dict[str, list[dict]] = {}
    for s in sessions:
        by_date.setdefault(s["date"], []).append(s)
    days = []
    for date in sorted(by_date.keys(), reverse=True):
        rows = []
        for s in by_date[date]:
            links = "".join(
                f'<a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(u.split("//")[-1])}</a>'
                for u in s["live_urls"]
            )
            links_div = f'<div class="links">{links}</div>' if links else ""
            rows.append(
                f'      <div class="entry">\n'
                f'        <div class="head"><span class="who">{html.escape(s["who"])}</span>'
                f'<span class="slug">{html.escape(s["slug"])}</span></div>\n'
                f'        <h3>{bpp.inline(s["title"])}</h3>\n'
                f'        <p>{bpp.inline(s["narrative"])}</p>\n'
                f'        {links_div}\n'
                f'      </div>'
            )
        days.append(
            f'    <div class="day"><div class="day-head">{bpp.pretty_date(date)}</div>\n'
            + "\n".join(rows) + "\n    </div>"
        )
    body = "\n".join(days)
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Production log — ShikshaLokam brain</title>
<meta name="description" content="Every session the ShikshaLokam brain has run, newest first. Generated from the session files." />
<meta name="generator" content="tools/build_site.py — generated from sessions/; do not hand-edit" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{LOG_CSS}</style>
</head>
<body>
<header class="bar"><div class="wrap bar-inner">
  <div class="mark"><a href="index.html" style="text-decoration:none;color:inherit;"><span class="brand">ShikshaLokam</span></a><span class="sep">/</span><span class="project">log</span></div>
  <a class="bar-back" href="index.html">← the brain</a>
</div></header>
<main>
<section class="hero"><div class="wrap">
  <div class="eyebrow">Production log</div>
  <h1>Every session, by the day it landed.</h1>
  <p class="lede">What the brain has produced and learned, newest first — one entry per session.
  Generated from the session files; this page can't drift from what really happened.</p>
</div></section>
<section><div class="wrap">
{body}
</div></section>
</main>
<footer><div class="wrap"><p>Generated from <code>sessions/</code> by <code>tools/build_site.py</code>.
<a href="index.html">↩ the brain self-portrait</a></p></div></footer>
</body>
</html>
"""
    (DOCS / "log.html").write_text(page, encoding="utf-8")
    return "docs/log.html"


# ---------------------------------------------------------------------------
# LEDGER.md — generated rollup (scannable, proof it compounded)

LEDGER_PREAMBLE = """# LEDGER — what the ShikshaLokam brain has done

**Generated** from the session files in `sessions/` by `tools/build_site.py` — do not hand-edit.
One entry per session, newest first. Each session leaves a `sessions/<date>-<who>.md` file; this is
the running, scannable proof that the brain compounds. The hand-written ledger that preceded this
generated one is preserved at `archive/LEDGER-handwritten-through-2026-06-05.md`.

---
"""


def build_ledger(sessions: list[dict]) -> str:
    parts = [LEDGER_PREAMBLE]
    for s in sessions:
        head = f"## {s['date']} — {s['who']} — {s['slug']}"
        line = f"\n{head}\n\n**{s['subtitle']}**\n\n{s['narrative']}\n"
        if s["live_urls"]:
            line += "\nLive: " + " · ".join(s["live_urls"]) + "\n"
        parts.append(line)
    LEDGER.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    return "LEDGER.md"


# ---------------------------------------------------------------------------
# Driver

def build_project_pages() -> list[str]:
    out_dir = DOCS / "projects"
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for slug in _generated_projects():
        (out_dir / f"{slug}.html").write_text(bpp.build(slug), encoding="utf-8")
        written.append(f"docs/projects/{slug}.html")
    return written


def build_all() -> list[str]:
    written = build_project_pages()
    sessions = load_sessions()
    if sessions and SHELL.exists():
        written.append(build_index(sessions))
        written.append(build_log(sessions))
        written.append(build_ledger(sessions))
    return written


def main() -> int:
    for w in build_all():
        print(f"built: {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
