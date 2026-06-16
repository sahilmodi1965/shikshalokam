#!/usr/bin/env python3
"""PreToolUse hook for mcp__claude_ai_Gmail__create_draft.

Gmail's API does NOT auto-append the account signature to API-created drafts
(that only happens in the web compose UI). So drafts created by the brain ship
bare. This hook intercepts every create_draft call and guarantees Sonal's rich
HTML signature is attached:

  * If the call has no htmlBody, it builds one from the plain-text `body`
    (so the draft renders as rich HTML) and appends the signature.
  * If it already has an htmlBody, it just appends the signature.
  * If the signature is already present, it leaves the call untouched
    (idempotent — safe on retries / manually-built htmlBody).

It returns the modified input via hookSpecificOutput.updatedInput so the draft
is corrected automatically, no model action required.
"""
import base64
import json
import os
import sys
from html import escape

SIG_MARKER = "gmail_signature"

# Inline images referenced by the signature via cid:<filename>. They are
# embedded as inline attachments so the signature renders even when a mail
# client blocks remote images (Gmail does, in drafts/previews).
SIG_IMAGES = ["logo.png", "ln.png", "tt.png", "sp.png", "yt.png"]


def project_dir() -> str:
    return os.environ.get(
        "CLAUDE_PROJECT_DIR",
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    )


def load_signature() -> str:
    path = os.path.join(project_dir(), ".claude", "gmail-signature.html")
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return ""


def load_inline_attachments() -> list:
    """Read each signature image and return an inline-attachment object whose
    Content-ID is derived from the filename (matching the cid: refs in the
    signature HTML)."""
    base = os.path.join(project_dir(), ".claude", "signature-assets")
    out = []
    for name in SIG_IMAGES:
        path = os.path.join(base, name)
        try:
            with open(path, "rb") as fh:
                content = base64.b64encode(fh.read()).decode("ascii")
        except OSError:
            continue
        out.append({
            "filename": name,
            "mimeType": "image/png",
            "inline": True,
            "content": content,
        })
    return out


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

    # Attach the signature images inline, without dropping any the caller set.
    existing = list(tool_input.get("attachments") or [])
    have = {a.get("filename") for a in existing if isinstance(a, dict)}
    for att in load_inline_attachments():
        if att["filename"] not in have:
            existing.append(att)
    if existing:
        new_input["attachments"] = existing

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
