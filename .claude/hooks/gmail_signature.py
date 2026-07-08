#!/usr/bin/env python3
"""PreToolUse hook for mcp__claude_ai_Gmail__create_draft.

Gmail's API does NOT auto-append the account signature to API-created drafts
(that only happens in the web compose UI). So drafts created by the brain ship
bare. This hook intercepts every create_draft call and attaches the rich HTML
signature OF THE PERSON RUNNING THIS SESSION — resolved from `git config
user.email` (the same identity the SessionStart roster check uses) to
`.claude/signatures/<email>.html`. No file for that person = no signature
(never someone else's):

  * If the call has no htmlBody, it builds one from the plain-text `body`
    (so the draft renders as rich HTML) and appends the signature.
  * If it already has an htmlBody, it just appends the signature.
  * If the signature is already present, it leaves the call untouched
    (idempotent — safe on retries / manually-built htmlBody).

It returns the modified input via hookSpecificOutput.updatedInput so the draft
is corrected automatically, no model action required.
"""
import json
import os
import subprocess
import sys
from html import escape

SIG_MARKER = "gmail_signature"

# The signature references its images by public https URL (the same hosted URLs
# Gmail uses for the native signature), NOT cid: inline attachments. Gmail's web
# composer collapses cid: inline images into a single attachment when a draft is
# edited and sent from there, silently breaking the signature — hosted URLs do
# not have that failure mode.


def project_dir() -> str:
    return os.environ.get(
        "CLAUDE_PROJECT_DIR",
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    )


def session_email() -> str:
    """Who is drafting = the signed-in teammate, per git config user.email
    (the identity the SessionStart roster check validates)."""
    try:
        out = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True, text=True, cwd=project_dir(), timeout=5,
        )
        return out.stdout.strip()
    except Exception:
        return ""


def load_signature() -> str:
    email = session_email()
    if not email:
        return ""
    path = os.path.join(project_dir(), ".claude", "signatures", f"{email}.html")
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return ""  # no signature on file for this person — ship bare, never someone else's


def text_to_html(body: str) -> str:
    """Plain-text body -> simple HTML: blank lines split paragraphs, single
    newlines become <br>."""
    paras = [p for p in body.replace("\r\n", "\n").split("\n\n")]
    out = []
    for p in paras:
        if p.strip() == "":
            continue
        out.append("<div>" + escape(p).replace("\n", "<br>") + "</div>")
    return "<br>".join(out) if out else ""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # don't block on malformed input

    tool_input = payload.get("tool_input", {}) or {}
    sig = load_signature()
    if not sig:
        return 0  # nothing to add; let the call through unchanged

    existing_html = tool_input.get("htmlBody") or ""
    if SIG_MARKER in existing_html:
        return 0  # already signed — idempotent no-op

    if existing_html:
        new_html = existing_html + "<br><br>" + sig
    else:
        body_html = text_to_html(tool_input.get("body", ""))
        new_html = (body_html + "<br><br>" + sig) if body_html else sig

    new_input = dict(tool_input)
    new_input["htmlBody"] = new_html

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "updatedInput": new_input,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
