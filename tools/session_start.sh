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

# Portable Python — Windows usually exposes `python` or the `py` launcher, not `python3`.
PY="$(command -v python3 || command -v python || command -v py || true)"

build_check() {
  # docs/ + LEDGER.md are CI build artifacts now (gitignored) — GitHub Actions rebuilds + deploys
  # the site on every push, so there is no committed output to drift or self-heal. We just do a
  # quick local build so a malformed page/template is caught early. Never blocks; never pushes.
  [ -z "$PY" ] && return
  if ! "$PY" "$CLAUDE_PROJECT_DIR/tools/build_site.py" >/dev/null 2>&1; then
    echo "⚠ Heads-up: the site doesn't build cleanly from source — a page or template may be malformed."
    echo "  See the error: $PY tools/build_site.py"
  fi
}

auto_rebase() {
  # Diverged + clean tree: replay local commits onto origin/main automatically — a content person
  # never resolves anything by hand. Generated files (docs/, LEDGER.md) can't truly conflict — they
  # are rebuilt from source — so any conflict there is resolved by picking a side then rebuilding.
  # Only a GENUINE source-file conflict stops the rebase; we abort cleanly (main untouched), log it,
  # and let the session continue. We never force-push and never rewrite pushed history.
  echo "⚠ DIVERGED — local $AHEAD ahead, $BEHIND behind. Auto-rebasing local commits onto origin/main…"
  if git rebase origin/main >/dev/null 2>&1; then
    echo "✓ Rebased cleanly onto origin/main."
    return 0
  fi
  local gitdir guard unmerged nongen f
  gitdir="$(git rev-parse --git-dir 2>/dev/null)"
  guard=0
  while [ -d "$gitdir/rebase-merge" ] || [ -d "$gitdir/rebase-apply" ]; do
    guard=$((guard + 1))
    if [ "$guard" -gt 50 ]; then
      git rebase --abort 2>/dev/null
      echo "⚠ Rebase did not converge — aborted, main untouched. Session continues; sync later."
      return 1
    fi
    unmerged="$(git diff --name-only --diff-filter=U 2>/dev/null)"
    if [ -z "$unmerged" ]; then
      git rebase --continue >/dev/null 2>&1 || break
      continue
    fi
    nongen="$(echo "$unmerged" | grep -vE '^(docs/|LEDGER\.md$)')"
    if [ -n "$nongen" ]; then
      git rebase --abort 2>/dev/null
      echo "⚠ Genuine source-file conflict (needs a human) — left main as-is, did NOT rebase:"
      echo "$nongen" | sed 's/^/    /'
      echo "  Your session continues normally; reconcile these files when convenient."
      return 1
    fi
    # generated-only conflict: unblock by taking either side; build_site rebuilds the truth after.
    for f in $unmerged; do
      git checkout --theirs -- "$f" 2>/dev/null || git checkout --ours -- "$f" 2>/dev/null
      git add -- "$f" 2>/dev/null
    done
    git rebase --continue >/dev/null 2>&1 || true
  done
  echo "✓ Rebased; generated-file conflicts resolved by rebuilding from source."
  return 0
}

echo "── SessionStart: auto-pull preflight ──"

# 0) Recover from an interrupted rebase/merge left by a crashed prior session. Without this the
#    brain stays WEDGED across sessions and a non-technical teammate is fully stuck — and the
#    self-heal below can't run because the conflicted files (incl. tools/build_site.py) won't parse.
#    Aborting restores every file to its last clean committed state, so everything works again.
GITDIR="$(git rev-parse --git-dir 2>/dev/null)"
if [ -n "$GITDIR" ] && { [ -d "$GITDIR/rebase-merge" ] || [ -d "$GITDIR/rebase-apply" ]; }; then
  echo "⚠ A previous session was interrupted mid-rebase — auto-recovering (files restored to last saved state)…"
  git rebase --abort 2>/dev/null && echo "✓ Recovered: rebase aborted, working tree is clean again."
fi
if [ -n "$GITDIR" ] && [ -f "$GITDIR/MERGE_HEAD" ]; then
  echo "⚠ A previous session was interrupted mid-merge — auto-recovering…"
  git merge --abort 2>/dev/null && echo "✓ Recovered: merge aborted, working tree is clean again."
fi

# Identity — every save must attribute to a teammate in brain.yml. Equal access, correct credit.
GIT_EMAIL="$(git config user.email 2>/dev/null)"
GIT_NAME="$(git config user.name 2>/dev/null)"
if [ -n "$GIT_EMAIL" ] && grep -qF "${GIT_EMAIL}" brain.yml 2>/dev/null; then
  echo "✓ Signed in as ${GIT_NAME} <${GIT_EMAIL}> — in the team roster."
else
  echo "⚠ git identity '${GIT_NAME} <${GIT_EMAIL}>' is NOT in the brain.yml team roster — commits will be mis-attributed."
  echo "  Add this person under 'team:' in brain.yml, or set the identity on this machine:"
  echo "    git config user.name \"Your Name\" && git config user.email \"you@your-org\""
fi

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
  build_check
  exit 0
fi

BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "?")
AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "?")
DIRTY="$(git status --porcelain)"

if [ -n "$DIRTY" ]; then
  # Uncommitted work present — don't pull/rebase under it. Source edits are untouched; just
  # self-heal generated files. (Rare at session start, since session end commits everything.)
  echo "⚠ Uncommitted changes present — skipping sync so nothing of yours is disturbed:"
  echo "$DIRTY" | sed 's/^/    /'
  build_check
  exit 0
fi

if [ "$AHEAD" != "0" ] && [ "$BEHIND" != "0" ]; then
  auto_rebase
  build_check
  exit 0
fi

# Fast-forward only — never merge, never rebase, never silently rewrite history.
if git pull --ff-only --quiet origin main 2>&1; then
  NEW=$(git rev-parse --short HEAD)
  echo "✓ Auto-pulled $BEHIND commit(s) from origin/main — now at $NEW"
  echo "  Recent:"
  git log --oneline -"${BEHIND}" 2>/dev/null | sed 's/^/    /'
  build_check
else
  echo "⚠ git pull --ff-only failed unexpectedly (was clean + FF-able). Investigate manually:"
  echo "    cd \$CLAUDE_PROJECT_DIR && git pull --ff-only origin main"
fi

exit 0
