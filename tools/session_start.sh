#!/usr/bin/env bash
# tools/session_start.sh — auto-pull preflight for Claude Code SessionStart
#
# Invoked by .claude/settings.json on every Claude Code SessionStart in this repo.
# Enforces Rule B from learnings/2026-05-26-five-decisions-binding.md:
#   "Every session, before reading or writing anything, runs git fetch && git pull --ff-only."
#
# Loud-by-design: prints to stdout so Claude (and the user) sees the state at session open.
# Never silently overwrites the remote; never silently swallows errors.

set +e  # do not abort the hook on a single failed command — we always exit 0

cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || {
  echo "⚠ SessionStart hook: could not cd to \$CLAUDE_PROJECT_DIR — skipping auto-pull."
  exit 0
}

echo "── SessionStart: auto-pull preflight ──"

# 1) Fetch — be loud if we can't reach the remote
if ! git fetch origin main --quiet 2>&1; then
  echo "⚠ git fetch failed (offline? auth?). Continuing with local state — verify before editing."
  exit 0
fi

LOCAL=$(git rev-parse HEAD 2>/dev/null)
REMOTE=$(git rev-parse origin/main 2>/dev/null)

if [ -z "$REMOTE" ]; then
  echo "⚠ Could not resolve origin/main — skipping auto-pull."
  exit 0
fi

if [ "$LOCAL" = "$REMOTE" ]; then
  echo "✓ Brain up to date with origin/main ($(git rev-parse --short HEAD))"
  exit 0
fi

BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "?")
AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "?")
DIRTY="$(git status --porcelain)"

if [ "$AHEAD" != "0" ] && [ "$BEHIND" != "0" ]; then
  echo "⚠ DIVERGED — local is $AHEAD ahead, $BEHIND behind origin/main."
  echo "  Auto-pull skipped (not fast-forward). Resolve before editing:"
  echo "    git log --oneline HEAD..origin/main   # see what's on remote"
  echo "    git log --oneline origin/main..HEAD   # see what's local"
  exit 0
fi

if [ -n "$DIRTY" ]; then
  echo "⚠ Local is $BEHIND commit(s) behind origin/main AND has uncommitted changes."
  echo "  Auto-pull skipped — uncommitted files would conflict on pull:"
  echo "$DIRTY" | sed 's/^/    /'
  echo "  Action: commit or stash, then run: git pull --ff-only origin main"
  exit 0
fi

# Fast-forward only — never merge, never rebase, never silently rewrite history.
if git pull --ff-only --quiet origin main 2>&1; then
  NEW=$(git rev-parse --short HEAD)
  echo "✓ Auto-pulled $BEHIND commit(s) from origin/main — now at $NEW"
  echo "  Recent:"
  git log --oneline -"${BEHIND}" 2>/dev/null | sed 's/^/    /'
else
  echo "⚠ git pull --ff-only failed unexpectedly (was clean + FF-able). Investigate manually:"
  echo "    cd \$CLAUDE_PROJECT_DIR && git pull --ff-only origin main"
fi

exit 0
