#!/usr/bin/env python3
"""Generate docs/projects/<slug>.html from projects/<slug>/page.md.

WHY THIS EXISTS (the once-and-for-all fix)
------------------------------------------
The project pages used to be HAND-AUTHORED HTML kept in sync with their page.md
by a human copy-paste at the end of each session. That sync was the failure point:

  - 2026-06-02: page.md was edited, the HTML was NOT regenerated -> drift.
  - 2026-06-03: Sonal approved Camille Massey + the advisors-group invite; those
    landed only in the front-page timeline and in learnings/, never in page.md or
    on the live invite page. The LEDGER claimed "All pushed to live brain page."
    That was false. The live page still showed a SUPERSEDED Peggy Dulany draft.

To Sonal, that reads as: "I approved invites, the brain told me it's live in 60s,
and the page doesn't show them." Internal (page.md) and external (the .html) drifted.

The cure: the HTML is now a pure function of page.md. There is no hand-authored HTML
to drift. `page.md` is the single source of truth; this script renders it; the
SessionEnd hook runs it automatically before every push. Anyone — Sonal, her team,
a maintainer — edits page.md, and the public page follows. No drift, internal or
external, ever again.

USAGE
-----
    python3 tools/build_project_page.py            # rebuild every project page
    python3 tools/build_project_page.py invoked-6  # rebuild one slug
    python3 tools/build_project_page.py --check     # build to memory, diff, exit 1 if any page is stale

Reads:  projects/<slug>/page.md   (markdown + YAML-ish frontmatter)
Writes: docs/projects/<slug>.html (generated; DO NOT hand-edit)

The generator leans entirely on docs/projects/style.css — the same visual system
the hand-authored pages used — so generated pages match the house style.
"""

from __future__ import annotations

import html
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROJECTS = REPO / "projects"
OUT_DIR = REPO / "docs" / "projects"

# Map a page.md `status` value to a style.css pill class + display label.
STATUS_PILL = {
    "template":  ("status-brief",    "template"),
    "seed":      ("status-seed",     "seed"),
    "draft":     ("status-draft",    "draft"),
    "drafting":  ("status-drafting", "drafting"),
    "revised":   ("status-outline",  "revised"),
    "approved":  ("status-approved", "approved"),
    "ready":     ("status-ready",    "ready"),
    "sent":      ("status-posted",   "sent"),
    "posted":    ("status-posted",   "posted"),
    "published": ("status-published","published"),
    "locked":    ("status-locked",   "locked"),
}

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


# ---------------------------------------------------------------------------
# Inline markdown -> HTML (operates on already-escaped text)

def inline(text: str) -> str:
    """Render inline markdown on a single (HTML-escaped) string."""
    s = html.escape(text, quote=False)
    # links [label](url) — do before bold/italic so the url isn't mangled
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
               lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>', s)
    # wikilinks [[target]] — internal pointers, not public URLs. Render as muted italic,
    # showing only the basename (strip any ../../path so the public page never shows a file path).
    s = re.sub(r"\[\[([^\]]+)\]\]",
               lambda m: f'<em class="wikilink">{m.group(1).split("|")[0].strip().rsplit("/", 1)[-1]}</em>', s)
    # bold **x**
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    # italic *x* (avoid touching ** already consumed)
    s = re.sub(r"(?<!\*)\*(?!\s)([^*]+?)\*(?!\*)", r"<em>\1</em>", s)
    # inline code `x`
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def pretty_date(value: str) -> str:
    """2026-06-01 -> '1 June 2026'. Pass through anything that doesn't match."""
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", str(value).strip())
    if not m:
        return str(value).strip()
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    return f"{d} {MONTHS[mo - 1]} {y}"


# ---------------------------------------------------------------------------
# Frontmatter

def parse_frontmatter(text: str):
    """Return (meta dict, body str). Supports `key: value` and simple `key:` lists."""
    meta: dict = {}
    if not text.startswith("---"):
        return meta, text
    end = text.find("\n---", 3)
    if end == -1:
        return meta, text
    block = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")
    cur_key = None
    for line in block.splitlines():
        if not line.strip():
            continue
        if re.match(r"^\s+-\s+", line):  # list item under the previous key
            if cur_key:
                meta.setdefault(cur_key, [])
                if isinstance(meta[cur_key], list):
                    meta[cur_key].append(line.strip()[1:].strip().strip('"'))
            continue
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip().strip('"')
            cur_key = key
            meta[key] = val if val else []
    return meta, body


# ---------------------------------------------------------------------------
# Block tokenizer

def split_blocks(body: str):
    """Yield ('type', payload) blocks from markdown body."""
    lines = body.split("\n")
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Horizontal rule / section divider
        if re.match(r"^-{3,}$", stripped) or re.match(r"^\*{3,}$", stripped):
            yield ("hr", None)
            i += 1
            continue

        # Headings
        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            yield (f"h{len(m.group(1))}", m.group(2).strip())
            i += 1
            continue

        # Table (block of lines starting with |)
        if stripped.startswith("|"):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            yield ("table", rows)
            continue

        # Blockquote (consecutive > lines)
        if stripped.startswith(">"):
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                q = lines[i].strip()[1:]
                if q.startswith(" "):
                    q = q[1:]
                quote.append(q)
                i += 1
            yield ("quote", quote)
            continue

        # List (consecutive -, *, • items, with 2-space / tab continuation lines)
        if re.match(r"^([-*]|•)\s+", stripped):
            items = []
            while i < n:
                cur = lines[i]
                s = cur.strip()
                if re.match(r"^([-*]|•)\s+", s):
                    items.append(re.sub(r"^([-*]|•)\s+", "", s))
                    i += 1
                elif s and items and (cur.startswith("  ") or cur.startswith("\t")):
                    items[-1] += " " + s  # wrapped continuation of the current item
                    i += 1
                else:
                    break
            yield ("list", items)
            continue

        # Paragraph (until blank line or next block starter)
        para = []
        while i < n and lines[i].strip() and not re.match(
                r"^(#{1,4}\s|>|\||[-*]\s|•\s|-{3,}$|\*{3,}$)", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        # A run of lines each shaped like "**Label:** value" is invite/card metadata,
        # not prose — keep them on separate lines instead of collapsing into one blob.
        if len(para) > 1 and all(re.match(r"^\*\*[^*]+:\*\*", ln) for ln in para):
            yield ("meta", para)
        else:
            yield ("para", " ".join(para))
    return


# ---------------------------------------------------------------------------
# Rendering helpers

def render_table(rows, *, status_pills=False) -> str:
    """GFM pipe table -> .logtable. status_pills: wrap a final 'Status' column in pills."""
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    # drop the |---|---| separator row
    cells = [c for c in cells if not all(re.match(r"^:?-{1,}:?$", x) or x == "" for x in c)]
    if not cells:
        return ""
    header, *data = cells
    status_col = None
    if status_pills:
        for idx, h in enumerate(header):
            if h.lower() == "status":
                status_col = idx
                break
    out = ['<table class="logtable">', "<thead><tr>"]
    out += [f"<th>{inline(h)}</th>" for h in header]
    out.append("</tr></thead><tbody>")
    for row in data:
        out.append("<tr>")
        for idx, cell in enumerate(row):
            if status_col is not None and idx == status_col:
                out.append(f"<td>{render_status_cell(cell)}</td>")
            elif idx == 0:
                out.append(f'<td class="log-date">{inline(cell)}</td>')
            else:
                out.append(f"<td>{inline(cell)}</td>")
        out.append("</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def render_status_cell(cell: str) -> str:
    """Turn a status cell like '`approved`' or 'draft →' into a pill (best effort)."""
    raw = cell.replace("`", "").strip()
    key = re.sub(r"[^a-z].*$", "", raw.lower())
    if key in STATUS_PILL:
        cls, label = STATUS_PILL[key]
        trailer = raw[len(key):].strip()
        suffix = f" {inline(trailer)}" if trailer else ""
        return f'<span class="pill {cls}">{label}</span>{suffix}'
    return inline(cell)


def render_quote(quote_lines) -> str:
    """Email/standing-phrase blockquote -> the bordered, pre-line invite box."""
    body = "\n".join(inline(l) for l in quote_lines)
    return (
        '<div class="quote-box" '
        'style="white-space:pre-line;font-size:0.94rem;'
        'border-left:3px solid var(--gold);padding-left:16px;margin:4px 0;">\n'
        f"{body}\n</div>"
    )


def parse_invite_heading(text: str):
    """'Invite — Peggy (Synergos) · status `approved`' -> ('Invite — Peggy (Synergos)', 'approved')."""
    m = re.search(r"·\s*status\s*`?([A-Za-z]+)`?\s*$", text)
    if m:
        return text[:m.start()].strip().rstrip("·").strip(), m.group(1).lower()
    return text.strip(), None


# ---------------------------------------------------------------------------
# Whole-page renderer

def render_page(slug: str, md_text: str, build_dt: datetime) -> str:
    meta, body = parse_frontmatter(md_text)
    title = meta.get("title", slug)
    last_updated = meta.get("last_updated", "")
    shareable_url = meta.get("shareable_url", "")

    blocks = list(split_blocks(body))

    # --- derive hero summary + pills from invite statuses and template count ---
    status_counts: dict[str, int] = {}
    template_count = 0
    for kind, payload in blocks:
        if kind == "h3":
            label, status = parse_invite_heading(payload)
            if status and label.lower().startswith("invite"):
                status_counts[status] = status_counts.get(status, 0) + 1
            if payload.lower().startswith("template"):
                template_count += 1

    order = ["approved", "sent", "posted", "revised", "draft", "template"]
    summary_bits = []
    for s in order:
        if status_counts.get(s):
            summary_bits.append(f"{status_counts[s]} {s}")
    for s, c in status_counts.items():
        if s not in order and c:
            summary_bits.append(f"{c} {s}")
    summary = " · ".join(summary_bits)

    pills = []
    for s in order:
        if status_counts.get(s):
            cls = STATUS_PILL.get(s, ("", s))[0]
            pills.append(f'<span class="pill {cls}">{status_counts[s]} {s}</span>')
    if template_count:
        pills.append(f'<span class="pill">{template_count} templates</span>')
    if last_updated:
        pills.append(f'<span class="pill">updated {pretty_date(last_updated)}</span>')

    # --- hero: H1 + the intro paragraph(s) before the first H2 ---
    hero_title = title
    hero_lede_parts = []
    section_blocks = []
    seen_h1 = False
    in_hero = True
    for kind, payload in blocks:
        if kind == "h1" and not seen_h1:
            hero_title = payload
            seen_h1 = True
            continue
        if kind == "h2":
            in_hero = False
        if in_hero and kind == "para":
            hero_lede_parts.append(inline(payload))
        elif not in_hero:
            section_blocks.append((kind, payload))
    hero_lede = "<br/><br/>".join(hero_lede_parts)

    # Drop sections explicitly marked internal: a heading ending in "· internal" (or
    # "(internal)") and everything under it until the next heading of same-or-higher level.
    # Lets page.md hold backstage notes (maintainer TODOs, raw paths) without leaking them
    # onto the public page. Default is public — you opt OUT, so nothing silently hides.
    def _is_internal(text):
        return bool(re.search(r"·\s*internal\b", text, re.I)) or \
            text.strip().lower().endswith("(internal)")
    _level = {"h2": 2, "h3": 3, "h4": 4}
    kept = []
    skip_level = None
    for kind, payload in section_blocks:
        lvl = _level.get(kind)
        if skip_level is not None:
            if lvl is not None and lvl <= skip_level:
                skip_level = None  # this heading closes the skipped region; re-evaluate it
            else:
                continue
        if lvl is not None and _is_internal(payload):
            skip_level = lvl
            continue
        kept.append((kind, payload))
    section_blocks = kept

    # H1 like "InvokED 6.0 — invitation workspace" -> two display lines
    if " — " in hero_title:
        a, b = hero_title.split(" — ", 1)
        h1_html = f"{inline(a)} —<br/>{inline(b)}."
    else:
        h1_html = inline(hero_title)

    eyebrow = "Project workspace"
    if last_updated:
        eyebrow += f" — last updated {pretty_date(last_updated)}"
    if summary:
        eyebrow += f" · {summary}"

    # --- render the sections ---
    out = []
    open_section = False
    open_card = False

    def close_card():
        nonlocal open_card
        if open_card:
            out.append("</div></div>")  # card-body, card
            open_card = False

    def close_section():
        nonlocal open_section
        close_card()
        if open_section:
            out.append("</div></section>")
            open_section = False

    for idx, (kind, payload) in enumerate(section_blocks):
        if kind == "h2":
            close_section()
            out.append('<section><div class="wrap">')
            open_section = True
            out.append(f"<h2>{inline(payload)}</h2>")
            continue

        if not open_section:  # safety: open a section if content precedes any H2
            out.append('<section><div class="wrap">')
            open_section = True

        if kind == "h3":
            close_card()
            label, status = parse_invite_heading(payload)
            pill = ""
            if status and status in STATUS_PILL:
                cls, lbl = STATUS_PILL[status]
                pill = f' <span class="pill {cls}">{lbl}</span>'
            out.append('<div class="card">')
            out.append(f'<div class="label">{inline(label)}{pill}</div>')
            out.append('<div class="card-body">')
            open_card = True
            continue

        if kind == "h4":
            out.append(f"<h4>{inline(payload)}</h4>")
            continue

        if kind == "para":
            out.append(f"<p>{inline(payload)}</p>")
            continue

        if kind == "meta":
            lines_html = "<br/>".join(inline(ln) for ln in payload)
            out.append(
                '<p class="card-meta-lines" '
                'style="color:var(--muted);font-size:0.9rem;margin:0 0 12px;">'
                f"{lines_html}</p>"
            )
            continue

        if kind == "list":
            items = "".join(f"<li>{inline(it)}</li>" for it in payload)
            out.append(f"<ul>{items}</ul>")
            continue

        if kind == "quote":
            out.append(render_quote(payload))
            continue

        if kind == "table":
            # Heuristic: a table with a 'Status' column renders status pills.
            head = payload[0].lower() if payload else ""
            out.append(render_table(payload, status_pills=("status" in head)))
            continue

        if kind == "hr":
            continue  # section/visual dividers are implicit in the card/section layout

    close_section()
    sections_html = "\n".join(out)

    built = build_dt.strftime("%-d %B %Y, %H:%M UTC")
    pills_html = "\n      ".join(pills)
    lede_block = f'<p class="lede">{hero_lede}</p>' if hero_lede else ""

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(title)} — ShikshaLokam</title>
<meta name="description" content="{html.escape(re.sub(r'<[^>]+>', '', hero_lede)[:180])}" />
<meta name="generator" content="tools/build_project_page.py — generated from projects/{slug}/page.md; do not hand-edit" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,500;9..144,600;9..144,700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>

<header class="bar">
  <div class="wrap bar-inner">
    <div class="mark">
      <a href="../index.html" style="text-decoration:none;color:inherit;"><span class="brand">ShikshaLokam</span></a>
      <span class="sep">/</span>
      <a href="index.html" style="text-decoration:none;color:inherit;"><span>projects</span></a>
      <span class="sep">/</span>
      <span class="project">{html.escape(slug)}</span>
    </div>
    <a class="bar-back" href="index.html">← all projects</a>
  </div>
</header>

<main>

<section class="hero">
  <div class="wrap">
    <div class="eyebrow">{html.escape(eyebrow)}</div>
    <h1>{h1_html}</h1>
    {lede_block}
    <div class="pill-row">
      {pills_html}
    </div>
  </div>
</section>

{sections_html}

</main>

<footer>
  <div class="wrap">
    <div>
      <p style="color:var(--paper);font-weight:500;">{html.escape(title)}</p>
      <p class="footer-meta">Generated from <code>projects/{slug}/page.md</code> — the single source of truth.
      This page is built automatically; do not hand-edit. Last build: <strong>{built}</strong>.</p>
    </div>
    <div>
      <p class="footer-meta">
        <a href="index.html">↩ all projects</a><br/>
        <a href="../index.html">↩ the brain self-portrait</a>
      </p>
    </div>
  </div>
</footer>

</body>
</html>
"""


# ---------------------------------------------------------------------------
# Driver

def slugs_with_page():
    return sorted(p.parent.name for p in PROJECTS.glob("*/page.md"))


def build(slug: str, build_dt: datetime) -> str:
    src = PROJECTS / slug / "page.md"
    if not src.exists():
        raise FileNotFoundError(f"no page.md for project '{slug}' ({src})")
    return render_page(slug, src.read_text(encoding="utf-8"), build_dt)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = {a for a in argv[1:] if a.startswith("--")}
    build_dt = datetime.now(timezone.utc)

    targets = args if args else slugs_with_page()
    if not targets:
        print("build_project_page: no projects with page.md found", file=sys.stderr)
        return 1

    stale = []
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for slug in targets:
        out_path = OUT_DIR / f"{slug}.html"
        new_html = build(slug, build_dt)
        if "--check" in flags:
            old = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
            # ignore the build-timestamp line when diffing
            norm = lambda s: re.sub(r"Last build: <strong>.*?</strong>", "", s)
            if norm(old) != norm(new_html):
                stale.append(slug)
                print(f"STALE: docs/projects/{slug}.html differs from page.md")
            else:
                print(f"ok:    docs/projects/{slug}.html matches page.md")
        else:
            out_path.write_text(new_html, encoding="utf-8")
            print(f"built: docs/projects/{slug}.html  <-  projects/{slug}/page.md")

    if "--check" in flags and stale:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
