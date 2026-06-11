#!/usr/bin/env bash
# tools/publish.sh — the one true publish action, honest by construction.
#
# The site is built + deployed by CI (.github/workflows/deploy-pages.yml), not committed. So
# publishing = save the SOURCE and push; GitHub Actions then rebuilds + deploys the site (~1–2 min).
# A content person types zero git commands; this is where their work goes live. Loud on failure;
# never claims success unless the push actually reached GitHub. Run by session_end.sh and on demand.
set +e
cd "${CLAUDE_PROJECT_DIR:-}" 2>/dev/null || cd "$(dirname "$0")/.." || { echo "NOT PUBLISHED — repo not found."; exit 1; }

BASE="https://sahilmodi1965.github.io/shikshalokam"
PY="$(command -v python3 || command -v python || command -v py || true)"

# 1) Local build sanity check (if Python is here). docs/ + LEDGER.md are gitignored CI artifacts —
#    we do NOT commit them; we only confirm the site still builds before pushing, to catch a broken
#    page/template before it reaches CI. No Python on this machine? Skip — CI is the source of truth.
if [ -n "$PY" ]; then
  if ! "$PY" tools/build_site.py >/dev/null 2>build_err.log; then
    echo "❌ NOT PUBLISHED — the site doesn't build from source, so nothing was pushed."
    sed 's/^/    /' build_err.log; rm -f build_err.log
    exit 1
  fi
  rm -f build_err.log
fi

# 2) Stage + commit SOURCE changes only (docs/ + LEDGER.md are gitignored, so never staged).
git add -A
if git diff --cached --quiet; then
  echo "ℹ️ Nothing new to publish — no source changes since the last push."
  exit 0
fi
CHANGED="$(git diff --cached --name-only)"
git commit -q -m "session: $(date -u +%Y-%m-%dT%H:%M:%SZ)" 2>/dev/null

# 3) Push — the moment of truth.
PUSH_OUT="$(git push origin main 2>&1)"; PUSH_RC=$?

if [ "$PUSH_RC" -ne 0 ]; then
  echo "════════════════════════════════════════════════════════════════════"
  echo "❌ NOT PUBLISHED — your work is committed locally but did NOT reach GitHub."
  echo "   It is NOT live. Most likely this session lacks write access to the repo."
  echo "$PUSH_OUT" | sed 's/^/    /'
  echo "   To publish: connect with write access, then run  bash tools/publish.sh"
  echo "════════════════════════════════════════════════════════════════════"
  exit 2
fi

echo "✅ PUSHED to origin/main ($(git rev-parse --short HEAD)). GitHub Actions is now rebuilding +"
echo "   deploying the site — live in ~1–2 minutes at:"
echo "   → $BASE/"
echo "$CHANGED" | grep -oE 'projects/[^/]+/page\.md' | sed -E "s#projects/(.+)/page\.md#   → $BASE/projects/\1.html#" | sort -u
echo "   (deploy status: $BASE/  ·  Actions tab on GitHub shows the run)"
exit 0
