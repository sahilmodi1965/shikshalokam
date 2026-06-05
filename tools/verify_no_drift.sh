#!/usr/bin/env bash
# tools/verify_no_drift.sh — the SINGLE definition of "the published site is not drifted."
#
# Rebuilds every generated file under docs/ from its sources (tools/build_site.py), then fails
# LOUDLY if docs/ changed. Exit 0 = in sync. Exit 1 = drift (docs/ was out of sync; the working
# tree is now rebuilt to the correct, source-derived state — commit it to publish the truth).
# Exit 2 = the builder itself errored.
#
# Used at every entry point: session_start.sh (after auto-pull), session_end.sh (before push),
# and the GitHub Action backstop. Because the check lives here — in a script, not in model
# memory — a resumed or compacted session that has forgotten every rule still cannot ship drift.
#
# Self-heal, runnable by hand any time:  bash tools/verify_no_drift.sh
set -u

cd "${CLAUDE_PROJECT_DIR:-}" 2>/dev/null || cd "$(dirname "$0")/.." || exit 2

ERR="$(mktemp)"
if ! python3 tools/build_site.py >/dev/null 2>"$ERR"; then
  echo "✗ verify_no_drift: tools/build_site.py FAILED — cannot determine drift:"
  sed 's/^/    /' "$ERR"
  rm -f "$ERR"
  exit 2
fi
rm -f "$ERR"

if git diff --quiet -- docs/ LEDGER.md; then
  echo "✓ verify_no_drift: docs/ + LEDGER.md match sources — no drift."
  exit 0
fi

echo "════════════════════════════════════════════════════════════════════"
echo "✗ verify_no_drift: DRIFT DETECTED — generated files differ from what the sources generate."
echo "  These published/generated files were out of sync with the brain's real content:"
git diff --name-only -- docs/ LEDGER.md | sed 's/^/    /'
echo "  The working tree has now been rebuilt to the correct (source-derived) state."
echo "  Commit the rebuilt docs/ to publish the truth.  (self-heal: python3 tools/build_site.py)"
echo "════════════════════════════════════════════════════════════════════"
exit 1
