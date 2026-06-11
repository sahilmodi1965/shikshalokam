#!/usr/bin/env bash
# tools/session_end.sh — at Claude Code SessionEnd, publish honestly and invisibly.
#
# A content person types zero git/file commands all session; this is where their work goes live.
# All the real logic (rebuild from source -> verify no drift -> commit -> push -> honest report)
# lives in tools/publish.sh, so the same action is available on demand mid-session. Loud on failure;
# never claims "live" unless the push truly succeeded. Always exits 0 (a hook must not block close).
set +e

cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || {
  echo "⚠ SessionEnd: could not cd to \$CLAUDE_PROJECT_DIR — skipping publish."
  exit 0
}

DIRTY="$(git status --porcelain 2>/dev/null)"
TODAY="$(date -u +%Y-%m-%d)"
PY="$(command -v python3 || command -v python || command -v py || true)"

# Compounding guard (non-negotiable: every session makes the brain better). If the brain changed
# source but no sessions/<date>-*.md digest was written, write a minimal one so the session is
# recorded in the timeline/log/LEDGER. The brain should write a richer one; this is the floor.
if [ -n "$DIRTY" ] && ! ls sessions/${TODAY}-*.md >/dev/null 2>&1; then
  if [ -n "$PY" ]; then
    "$PY" "$CLAUDE_PROJECT_DIR/tools/ensure_digest.py" 2>/dev/null
  else
    echo "WARN: SessionEnd — the brain changed but no sessions/${TODAY}-*.md digest was written (no Python to auto-record)."
  fi
fi

# Publish: rebuild -> verify -> commit -> push -> honest, chat-ready report.
bash "$CLAUDE_PROJECT_DIR/tools/publish.sh"

exit 0
