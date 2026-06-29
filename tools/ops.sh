#!/usr/bin/env bash
# tools/ops.sh — the brain's hands for the ARCHITECTURE lane (GitHub Issues + PRs).
#
# The system files and fixes its OWN bugs, frictions and ideas — nobody flags anything on
# WhatsApp. CONTENT never comes through here; content publishes every session via publish.sh.
# This lane is for how the brain itself evolves: bug/friction/feature/ci issues → fixes → PRs.
#
#   tools/ops.sh issue "<title>" "<body>" [bug|friction|feature|ci]   # file one
#   tools/ops.sh backlog                                              # list open issues
#   tools/ops.sh fixed "<branch>" "<title>" "<body>" [issue#]         # open + auto-merge a fix PR
set -u
cd "${CLAUDE_PROJECT_DIR:-}" 2>/dev/null || cd "$(dirname "$0")/.." || exit 1

need_gh() {
  if ! command -v gh >/dev/null 2>&1; then
    echo "ℹ The issues lane needs the GitHub CLI once (it's not installed/authed here)."
    echo "  Install: https://cli.github.com  ·  then: gh auth login   (then I can file + fix autonomously)"
    exit 3
  fi
}
ensure_label() { gh label create "$1" --color "C2A24C" --force >/dev/null 2>&1 || true; }

cmd="${1:-}"; shift || true
case "$cmd" in
  issue)
    need_gh
    title="${1:?need a title}"; body="${2:-}"; label="${3:-friction}"
    ensure_label "$label"
    gh issue create --title "$title" --body "$body" --label "$label"
    ;;
  backlog)
    need_gh
    gh issue list --state open --limit 40 --json number,title,labels \
      --jq '.[] | "#\(.number) [\(.labels|map(.name)|join(","))] \(.title)"'
    ;;
  fixed)
    need_gh
    branch="${1:?need a branch}"; title="${2:?need a title}"; body="${3:-}"; issue="${4:-}"
    [ -n "$issue" ] && body="${body}

Closes #${issue}."
    git push origin "$branch" >/dev/null 2>&1 || { echo "couldn't push $branch"; exit 1; }
    url="$(gh pr create --base main --head "$branch" --title "$title" --body "$body")"
    gh pr merge "$branch" --auto --merge >/dev/null 2>&1
    echo "PR opened + set to auto-merge: $url"
    ;;
  *)
    echo "usage: tools/ops.sh issue \"<title>\" \"<body>\" [bug|friction|feature|ci] | backlog | fixed \"<branch>\" \"<title>\" \"<body>\" [issue#]"
    exit 1
    ;;
esac
