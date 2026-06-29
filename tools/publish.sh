#!/usr/bin/env bash
# tools/publish.sh — save the session's SOURCE and get it live, SEAMLESSLY.
#
# Content publishes every session. Same-page work never blocks and is never lost:
#  • We rebase onto the latest before pushing — git auto-merges edits to different lines/sections
#    of the same page, so two people on one page both land.
#  • The rare genuine same-line clash is PARKED on a branch (+ a PR if `gh` is available) so it's
#    preserved for a one-click merge — never dropped.
# The site itself is built + deployed by GitHub Actions (docs/ is not committed).
set +e
cd "${CLAUDE_PROJECT_DIR:-}" 2>/dev/null || cd "$(dirname "$0")/.." || { echo "NOT PUBLISHED — repo not found."; exit 1; }

BASE="https://sahilmodi1965.github.io/shikshalokam"
PY="$(command -v python3 || command -v python || command -v py || true)"

# 1) Local build sanity check (catch a broken page/template before it reaches CI).
if [ -n "$PY" ]; then
  if ! "$PY" tools/build_site.py >/dev/null 2>build_err.log; then
    echo "❌ NOT PUBLISHED — the site doesn't build from source, so nothing was pushed."
    sed 's/^/    /' build_err.log; rm -f build_err.log
    exit 1
  fi
  rm -f build_err.log
fi

# 2) Commit SOURCE changes (docs/ + LEDGER.md are gitignored CI artifacts; never staged).
git add -A
if git diff --cached --quiet; then
  echo "ℹ️ Nothing new to publish — no source changes since the last push."
  exit 0
fi
CHANGED="$(git diff --cached --name-only)"
git commit -q -m "session: $(date -u +%Y-%m-%dT%H:%M:%SZ)" 2>/dev/null

report_live() {
  echo "✅ PUSHED to origin/main ($(git rev-parse --short HEAD)). GitHub Actions is rebuilding +"
  echo "   deploying now — live in ~1–2 min at: $BASE/"
  echo "$CHANGED" | grep -oE 'projects/[^/]+/page\.md' | sed -E "s#projects/(.+)/page\.md#   → $BASE/projects/\1.html#" | sort -u
}

# 3) Seamless push: rebase onto latest (auto-merges non-overlapping) and retry.
WHO="$(git config user.name 2>/dev/null | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"; [ -z "$WHO" ] && WHO="teammate"
for attempt in 1 2 3 4 5; do
  git fetch origin main -q 2>/dev/null
  if git rebase origin/main >/dev/null 2>&1; then
    if git push origin main >/dev/null 2>&1; then
      report_live
      exit 0
    fi
    continue   # someone landed in between — re-fetch + rebase and try again
  fi
  # Genuine same-line clash — PRESERVE the work, never drop it.
  git rebase --abort 2>/dev/null
  BRANCH="content/${WHO}-$(date -u +%Y%m%d-%H%M%S)"
  git branch -f "$BRANCH" HEAD
  if git push origin "$BRANCH" >/dev/null 2>&1; then
    if command -v gh >/dev/null 2>&1; then
      PRURL="$(gh pr create --base main --head "$BRANCH" \
        --title "content: ${WHO} session (same-page merge needed)" \
        --body "Auto-parked: another session touched the same lines this session. **Nothing is lost** — merging this lands the work." 2>/dev/null)"
      gh pr merge "$BRANCH" --auto --merge >/dev/null 2>&1
      echo "⚠ SAVED — a rare same-line clash means your work is on a PR (nothing lost):"
      echo "   ${PRURL:-branch $BRANCH}  (auto-merges once the overlap is cleared)"
    else
      echo "⚠ SAVED — a rare same-line clash; your work is on branch '$BRANCH' (nothing lost)."
      echo "   A maintainer merges it. (Install gh to auto-open PRs.)"
    fi
    exit 0
  fi
  echo "❌ Could not reach GitHub — your work is committed locally (NOT lost). Check access, then: bash tools/publish.sh"
  exit 2
done

echo "❌ Busy remote — couldn't land after 5 tries. Your work is committed locally (NOT lost). Re-run: bash tools/publish.sh"
exit 2
