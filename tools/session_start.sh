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

verify_and_heal() {
  # Self-heal drift on EVERY clean session open — including resumed / web / compacted sessions.
  # Rebuild all generated docs/ from source; if anything changed, the published site had drifted
  # and is now corrected in the working tree (committed at session end). Start NEVER pushes — it
  # only heals locally. The invariant lives here, in the harness, not in model memory.
  if ! python3 "$CLAUDE_PROJECT_DIR/tools/build_site.py" >/dev/null 2>&1; then
    echo "⚠ SessionStart — tools/build_site.py errored; cannot confirm the site is in sync."
    echo "  Self-heal by hand: python3 tools/build_site.py"
    return
  fi
  if git diff --quiet -- docs/ LEDGER.md 2>/dev/null; then
    echo "✓ Published site in sync with sources (no drift)."
  else
    echo "⚠ SessionStart — drift self-healed: generated files were out of sync and rebuilt from source:"
    git diff --name-only -- docs/ LEDGER.md 2>/dev/null | sed 's/^/    /'
    echo "  (these rebuilt files commit automatically at session end.)"
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
  verify_and_heal
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
  verify_and_heal
  exit 0
fi

if [ "$AHEAD" != "0" ] && [ "$BEHIND" != "0" ]; then
  auto_rebase
  verify_and_heal
  exit 0
fi

# Fast-forward only — never merge, never rebase, never silently rewrite history.
if git pull --ff-only --quiet origin main 2>&1; then
  NEW=$(git rev-parse --short HEAD)
  echo "✓ Auto-pulled $BEHIND commit(s) from origin/main — now at $NEW"
  echo "  Recent:"
  git log --oneline -"${BEHIND}" 2>/dev/null | sed 's/^/    /'
  verify_and_heal
else
  echo "⚠ git pull --ff-only failed unexpectedly (was clean + FF-able). Investigate manually:"
  echo "    cd \$CLAUDE_PROJECT_DIR && git pull --ff-only origin main"
fi

exit 0
