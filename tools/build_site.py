#!/usr/bin/env python3
"""tools/build_site.py — the ONE entrypoint that regenerates all generated docs/** from source.

Drift-proof contract: docs/ is 100% generated. Nothing in docs/ is hand-edited. Run this
(or `bash tools/verify_no_drift.sh`) any time to rebuild the published site from its sources.

DETERMINISTIC + IDEMPOTENT: the same sources produce byte-identical output. No wall-clock
stamps, no randomness — every date is derived from the sources themselves. Proof:
    python3 tools/build_site.py && python3 tools/build_site.py && git diff --exit-code docs/

PHASE 1 scope (current): project pages only — the surface that is already generated.
  docs/index.html (timeline) and docs/log.html move into this builder in Phase 3, generated
  from sessions/<date>-<person>.md. Until that lands on main, this builder deliberately does
  NOT touch index.html or log.html, so the hooks never regenerate/push them.

Sources -> outputs:
  projects/<slug>/page.md  ->  docs/projects/<slug>.html   (slugs in GENERATED_PROJECTS)

Self-heal (any session, fresh or resumed): python3 tools/build_site.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import build_project_page as bpp  # noqa: E402  (path set above)

# Project pages GENERATED from page.md. A slug joins this list once its page.md is the clean
# single source of truth for it. The legacy hand-authored pages (blogs, captions,
# nagaland-coffee-book, portraits) are NOT here yet — their page.md still carries backstage
# content, so they remain hand-authored until a migration pass cleans them. build_site only
# touches what's listed here, which is why Phase 1 is a no-op against the live site.
GENERATED_PROJECTS = [
    "invoked-6",
]


def build_project_pages() -> list[str]:
    written: list[str] = []
    out_dir = REPO / "docs" / "projects"
    out_dir.mkdir(parents=True, exist_ok=True)
    for slug in GENERATED_PROJECTS:
        (out_dir / f"{slug}.html").write_text(bpp.build(slug), encoding="utf-8")
        written.append(f"docs/projects/{slug}.html")
    return written


def build_all() -> list[str]:
    written: list[str] = []
    written += build_project_pages()
    # --- PHASE 3 seams (generated from sessions/, land on a branch first) ---
    # written += build_index()   # docs/index.html — timeline from sessions/<date>-<person>.md
    # written += build_log()     # docs/log.html   — running log from the same session files
    return written


def main() -> int:
    written = build_all()
    for w in written:
        print(f"built: {w}")
    print(f"build_site: {len(written)} file(s) regenerated from source.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
