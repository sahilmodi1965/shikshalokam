#!/usr/bin/env bash
# tools/publish.sh — the one true publish action, honest by construction.
#
# Rebuild generated outputs from source -> verify no drift -> commit -> push -> report, in
# chat-ready language. It says "LIVE" ONLY after the push actually succeeds AND the site verifies
# clean. If the push fails (e.g. this session has no write access), it says so plainly and does NOT
# claim the work is live. Run by session_end.sh and on demand mid-session.
#
# The final line printed here is the truth to relay in chat. Never claim "live" without it.
set +e
cd "${CLAUDE_PROJECT_DIR:-}" 2>/dev/null || cd "$(dirname "$0")/.." || { echo "NOT PUBLISHED — repo not found."; exit 1; }

BASE="https://sahilmodi1965.github.io/shikshalokam"

# Portable Python — Windows usually exposes `python` or the `py` launcher, not `python3`.
PY="$(command -v python3 || command -v python || command -v py || true)"
if [ -z "$PY" ]; then
  echo "❌ NOT PUBLISHED — Python isn't installed on this computer, so the site can't be rebuilt."
  echo "   Install Python (see onboarding/first-session.md), then: bash tools/publish.sh"
  exit 1
fi

# 1) Rebuild everything generated, from source.
if ! "$PY" tools/build_site.py >/dev/null 2>build_err.log; then
  echo "❌ NOT PUBLISHED — the site failed to build from source, so nothing was pushed. It is NOT live."
  sed 's/^/    /' build_err.log; rm -f build_err.log
  exit 1
fi
rm -f build_err.log

# 2) Stage + commit (only if something changed).
git add -A
if git diff --cached --quiet; then
  echo "ℹ️ Nothing new to publish — the live site already matches the brain."
  exit 0
fi
CHANGED="$(git diff --cached --name-only)"
git commit -q -m "session: $(date -u +%Y-%m-%dT%H:%M:%SZ)" 2>/dev/null

# 3) Push — the moment of truth.
PUSH_OUT="$(git push origin main 2>&1)"; PUSH_RC=$?

# 4) Drift tripwire — committed tree must equal a fresh build.
DRIFT_OK=1
bash tools/verify_no_drift.sh >/dev/null 2>&1 || DRIFT_OK=0

if [ "$PUSH_RC" -ne 0 ]; then
  echo "════════════════════════════════════════════════════════════════════"
  echo "❌ NOT PUBLISHED — your work is committed locally but did NOT reach GitHub."
  echo "   It is NOT live. Most likely this session lacks write access to the repo."
  echo "$PUSH_OUT" | sed 's/^/    /'
  echo "   To publish: connect with write access, then run  bash tools/publish.sh"
  echo "════════════════════════════════════════════════════════════════════"
  exit 2
fi

if [ "$DRIFT_OK" -ne 0 ]; then
  echo "⚠ Pushed, but the post-publish drift check did not come back clean — generation may be"
  echo "  non-deterministic. Inspect: bash tools/verify_no_drift.sh"
fi

echo "✅ LIVE — pushed to origin/main ($(git rev-parse --short HEAD)). The site rebuilds in ~1 minute:"
echo "   → $BASE/"
echo "$CHANGED" | grep -oE 'docs/projects/[^ ]+\.html' | sed -E "s#docs/projects/(.+)\.html#   → $BASE/projects/\1.html#" | sort -u
if echo "$CHANGED" | grep -q '^docs/log.html'; then echo "   → $BASE/log.html"; fi
exit 0
