#!/usr/bin/env bash
# tools/session_end.sh — commit + push at Claude Code SessionEnd, LOUD on failure.
#
# Replaces the old inline one-liner whose `git push ... || true` SILENTLY swallowed
# push failures — the exact reason Sonal's web-session work committed locally but
# never reached GitHub (the website never updated, with no error surfaced).
#
# Guards, in order: LEDGER entry present · self-portrait refreshed · HTML mirror
# regenerated for any changed project page · then commit · then push with a loud,
# unmissable failure block if the remote rejects (auth / offline / non-FF).
#
# Loud-by-design. Never silently swallows a failed push. Always exits 0 (a hook that
# aborts would block the session close).

set +e

cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || {
  echo "⚠ SessionEnd hook: could not cd to \$CLAUDE_PROJECT_DIR — skipping commit/push."
  exit 0
}

DIRTY="$(git status --porcelain 2>/dev/null)"
if [ -z "$DIRTY" ]; then
  exit 0  # nothing changed this session — nothing to publish
fi

TODAY=$(date -u +%Y-%m-%d)

# 1) LEDGER guard — every session must leave one entry (INTENT principle 2).
if ! grep -q "^## ${TODAY}" LEDGER.md 2>/dev/null; then
  echo "WARN: SessionEnd — no LEDGER.md entry dated ${TODAY}. INTENT principle 2 may be violated; brain-lint will flag."
fi

# 2) Self-portrait guard — brain changes must refresh docs/index.html.
if echo "$DIRTY" | grep -qE "(wiki/|routes/|LEDGER\.md)" && ! echo "$DIRTY" | grep -q "docs/index.html"; then
  echo "WARN: SessionEnd — brain content changed but docs/index.html (self-portrait) was not updated. It will go stale (per CLAUDE.md per-session contract)."
fi

# 3) Rebuild the whole generated site from source, so docs/ can never be committed out of
#    sync with the brain's real content. build_site.py is deterministic + idempotent and only
#    rewrites GENERATED surfaces (project pages in Phase 1 — it does NOT touch index.html or
#    log.html yet). page.md is the single source of truth; there is no hand-copied mirror to
#    forget (see learnings/2026-06-04-publish-confirmation-rca.md).
if ! python3 "$CLAUDE_PROJECT_DIR/tools/build_site.py" >/dev/null 2>&1; then
  echo "════════════════════════════════════════════════════════════════════"
  echo "✗ SessionEnd — tools/build_site.py errored; the published site may be STALE."
  echo "  Fix: python3 tools/build_site.py   (read the error, then re-end)"
  echo "════════════════════════════════════════════════════════════════════"
fi
# What actually changed on the live site this session — drives the honest publish claim below.
PUBLISHED_PAGES="$(git status --porcelain -- docs/projects 2>/dev/null | grep -oE 'docs/projects/[^ ]+\.html' | sed -E 's#docs/projects/(.+)\.html#\1#' | sort -u)"

# 4) Commit.
git add -A
if ! git commit -m "session: $(date -u +%Y-%m-%dT%H:%M:%SZ)" -q; then
  echo "⚠ SessionEnd — git commit produced nothing (already committed?). Continuing to push check."
fi

# 5) Push — LOUD on failure. No silent `|| true`.
PUSH_OUT="$(git push origin main 2>&1)"
PUSH_RC=$?
if [ "$PUSH_RC" -eq 0 ]; then
  echo "✓ SessionEnd — pushed to origin/main ($(git rev-parse --short HEAD)). Live site refreshes in ~60s."
  # Authoritative record of what actually reached the public site this session. The wrap's
  # "it's live" claim must match THIS — never promise a page updated unless it appears here.
  for slug in $PUBLISHED_PAGES; do
    echo "   → live: https://sahilmodi1965.github.io/shikshalokam/projects/${slug}.html"
  done
else
  echo "════════════════════════════════════════════════════════════════════"
  echo "✗ SessionEnd — PUSH FAILED (exit ${PUSH_RC})."
  echo "  Your work is committed LOCALLY but is NOT on GitHub."
  echo "  The website will NOT update until this is pushed."
  echo "  Most likely cause: this session lacks GitHub WRITE access (auth),"
  echo "  or the local branch diverged from origin/main."
  echo "  git said:"
  echo "$PUSH_OUT" | sed 's/^/    /'
  echo "  Fix: connect the repo with WRITE access, then run:  git push origin main"
  echo "════════════════════════════════════════════════════════════════════"
fi

# 6) Drift tripwire — the committed tree MUST equal what the sources generate. A fresh build
#    should change nothing; if it does, generation is non-deterministic and must be fixed.
if ! bash "$CLAUDE_PROJECT_DIR/tools/verify_no_drift.sh" >/dev/null 2>&1; then
  echo "WARN: SessionEnd — post-commit drift tripwire FAILED: committed docs/ do not match a fresh build."
  echo "  Generation may be non-deterministic. Inspect: bash tools/verify_no_drift.sh"
fi

exit 0
