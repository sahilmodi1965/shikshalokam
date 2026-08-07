#!/usr/bin/env bash
# tools/verify_no_drift.sh — sanity check that the site BUILDS cleanly from source.
#
# History: docs/ + LEDGER.md used to be committed, and this script checked them for "drift" from
# their sources. They are now CI build artifacts (gitignored), built + deployed by
# .github/workflows/deploy-pages.yml on every push — so there is no committed output to drift.
# This script now just proves the build works (a malformed page/template would fail it).
#
# Exit 0 = builds clean (or no Python here). Exit 2 = the builder errored.
# Run by hand any time:  bash tools/verify_no_drift.sh
set -u

cd "${CLAUDE_PROJECT_DIR:-}" 2>/dev/null || cd "$(dirname "$0")/.." || exit 2

# Portable Python — Windows usually exposes `python` or the `py` launcher, not `python3`, AND it
# ships a `python3` Microsoft Store alias stub that IS on PATH but errors out. So test each
# candidate actually runs; `command -v` alone picks the stub and every build "fails".
PY=""
for cand in python3 python py; do
  if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import sys" >/dev/null 2>&1; then
    PY="$(command -v "$cand")"; break
  fi
done
if [ -z "$PY" ]; then
  echo "ℹ verify_no_drift: no Python here — skipping local build check (CI builds with Python on push)."
  exit 0
fi

ERR="$(mktemp)"
if ! "$PY" tools/build_site.py >/dev/null 2>"$ERR"; then
  echo "✗ verify_no_drift: the site does NOT build from source:"
  sed 's/^/    /' "$ERR"
  rm -f "$ERR"
  exit 2
fi
rm -f "$ERR"
echo "✓ verify_no_drift: site builds cleanly from source."
exit 0
