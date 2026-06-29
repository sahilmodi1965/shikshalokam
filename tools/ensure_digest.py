#!/usr/bin/env python3
"""Guarantee every changing session leaves a record — the brain MUST compound.

If the brain changed source this session but no `sessions/<date>-*.md` digest was written,
this writes a minimal, valid auto-digest so the timeline / log / LEDGER still include the
session. The brain should always write a real, richer digest; this is the floor, not the
ceiling. Called by tools/session_end.sh before publishing.
"""
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SESS = REPO / "sessions"


def sh(*args):
    return subprocess.run(args, cwd=REPO, capture_output=True, text=True).stdout


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if list(SESS.glob(f"{today}-*.md")):
        return  # a digest already exists for today — nothing to do

    # Did the brain actually change SOURCE? (ignore gitignored build artifacts)
    changed = []
    for line in sh("git", "status", "--porcelain").splitlines():
        name = line[3:].strip()
        if name and not name.startswith("docs/") and name != "LEDGER.md":
            changed.append(name)
    if not changed:
        return  # nothing of substance changed — no record needed

    who = sh("git", "config", "user.name").strip() or "the brain"
    whoslug = re.sub(r"[^a-z0-9]+", "-", who.lower()).strip("-") or "teammate"

    seq = 0
    for p in SESS.glob("*.md"):
        m = re.search(r"^seq:\s*(\d+)", p.read_text(encoding="utf-8"), re.M)
        if m:
            seq = max(seq, int(m.group(1)))
    seq += 1

    files = "\n".join(f"- `{c}`" for c in changed[:30])
    body = (
        f"---\n"
        f"date: {today}\n"
        f"who: {who}\n"
        f"slug: auto-{whoslug}\n"
        f"seq: {seq}\n"
        f"---\n"
        f"# Session — {today}\n\n"
        f"**Auto-recorded so the brain compounds — a fuller digest wasn't written this session.**\n\n"
        f"Source touched this session:\n{files}\n"
    )
    (SESS / f"{today}-auto-{whoslug}.md").write_text(body, encoding="utf-8")
    print(f"ℹ Wrote a minimal session digest (sessions/{today}-auto-{whoslug}.md) so this session is recorded.")


if __name__ == "__main__":
    main()
