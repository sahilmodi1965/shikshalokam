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

# Session-record guard — the timeline, log, and LEDGER all generate from sessions/<date>-<who>.md.
# If the brain changed but no session digest was written, warn (don't block): the session would
# otherwise be invisible in the brain's own story.
if [ -n "$DIRTY" ] && ! ls sessions/${TODAY}-*.md >/dev/null 2>&1; then
  echo "WARN: SessionEnd — the brain changed but no sessions/${TODAY}-*.md digest was written."
  echo "  The public timeline/log/LEDGER build from session files — add one so this session is recorded."
fi

# Publish: rebuild -> verify -> commit -> push -> honest, chat-ready report.
bash "$CLAUDE_PROJECT_DIR/tools/publish.sh"

exit 0
