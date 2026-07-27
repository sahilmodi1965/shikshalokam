#!/usr/bin/env python3
"""
gs.py — ShikshaLokam G-Suite engine.

One shared OAuth *desktop* app (Sahil sets it up once). Each teammate logs in a
single time in the browser; their personal token lives OUTSIDE the repo, in
~/.shikshalokam/, and is never committed. Every action runs *as the logged-in
person*, so attribution stays honest.

The brain never asks a teammate to think about any of this — it calls these
subcommands for them. Humans only ever click "Allow" once, then just talk.

Capabilities (all gated the way brain.yml says):
  login / whoami            — one-time consent, who am I
  email-draft               — write a Gmail draft (nothing sent)
  email-send <draft_id>     — send a draft  (ONLY after explicit approval)
  draft-update <draft_id>   — overwrite an existing draft in place (no duplicate)
  draft-read [draft_id]     — read a draft back (list drafts if id omitted) to learn from edits
  doc-create                — turn text/markdown into a real Google Doc
  drive-folder              — make a folder
  drive-move                — file a doc/folder into its proper folder (folder hygiene)
  drive-init                — build the shared "Brain Output" tree + share it
  cal-invite                — create a calendar event (notify only with --notify)
  search                    — find threads by Gmail query (threadId + subject)
  label-list/create         — list user labels / make a new one
  label-apply/remove        — add or remove a label on thread(s)
  filter-create             — auto-label future mail matching a query

Setup + onboarding: onboarding/gsuite-setup.md
"""

import argparse
import base64
import json
import sys
from email.mime.text import MIMEText
from pathlib import Path

# ---- paths -----------------------------------------------------------------
REPO = Path(__file__).resolve().parents[2]
CLIENT_PATH = REPO / "tools" / "gsuite" / "oauth_client.json"   # committed (desktop app)
DRIVE_MAP = REPO / "tools" / "gsuite" / "drive_map.json"        # committed (shared folder IDs)
BRAIN_YML = REPO / "brain.yml"

HOME = Path.home() / ".shikshalokam"                            # OUTSIDE the repo
TOKEN_PATH = HOME / "token.json"                                # personal, never committed

# Gmail's API does NOT auto-append the account signature to API-created drafts
# (that only happens in the web compose UI), so we attach it ourselves — the
# signature OF THE LOGGED-IN ACCOUNT, from .claude/signatures/<email>.html.
# No file for that account = no signature (never someone else's). Signature
# images are referenced by public https URL (the same hosted URLs Gmail uses
# for the native signature), NOT cid: inline parts — Gmail's web composer
# collapses cid: inline images into one attachment when a draft is edited and
# sent from there, which silently breaks the signature.
SIG_DIR = REPO / ".claude" / "signatures"

# Least surprise, broad enough for the stated capabilities. Keep in sync with
# the consent screen in onboarding/gsuite-setup.md.
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/gmail.compose",     # create drafts AND send them
    "https://www.googleapis.com/auth/gmail.modify",      # search + labels (CRUD + apply/remove)
    "https://www.googleapis.com/auth/gmail.settings.basic",  # auto-label filters
    "https://www.googleapis.com/auth/drive",             # folders, uploads, organize
    "https://www.googleapis.com/auth/documents",         # Google Docs
    "https://www.googleapis.com/auth/spreadsheets",      # Google Sheets (read + update cells)
    "https://www.googleapis.com/auth/calendar.events",   # invites
]

# Simple, shared output structure. Edit gsuite.output_taxonomy in brain.yml to
# extend it — drive-init reads from there if present, else uses this default.
DEFAULT_ROOT = "ShikshaLokam — Brain Output"
DEFAULT_TAXONOMY = ["Emails", "Docs", "Decks", "Social", "Newsletters"]


# ---- google plumbing (lazy import so a missing dep gives a kind message) ----
def _google():
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaInMemoryUpload
        return Request, Credentials, InstalledAppFlow, build, MediaInMemoryUpload
    except ImportError:
        sys.exit(
            "Google libraries aren't installed yet. Run:\n"
            "    pip3 install -r tools/gsuite/requirements.txt"
        )


def get_creds():
    Request, Credentials, _, _, _ = _google()
    if not TOKEN_PATH.exists():
        sys.exit("Not logged in yet. Run:  python3 tools/gsuite/gs.py login")
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            TOKEN_PATH.write_text(creds.to_json())
        else:
            sys.exit("Login expired. Run:  python3 tools/gsuite/gs.py login")
    return creds


def svc(api, version):
    _, _, _, build, _ = _google()
    return build(api, version, credentials=get_creds(), cache_discovery=False)


def team_emails():
    """Teammate emails from brain.yml (best-effort; used to auto-share Drive)."""
    emails = []
    try:
        for line in BRAIN_YML.read_text().splitlines():
            line = line.strip()
            if line.startswith("email:"):
                val = line.split("email:", 1)[1].split("#", 1)[0]  # drop inline comment
                val = val.strip().strip('"').strip("'")
                if "@" in val:
                    emails.append(val)
    except OSError:
        pass
    return emails


def load_map():
    if DRIVE_MAP.exists():
        return json.loads(DRIVE_MAP.read_text())
    return {}


# ---- commands --------------------------------------------------------------
def _find_downloaded_client():
    """Newest Google client JSON sitting in Downloads/Desktop (or cwd)."""
    import glob
    hits = []
    for d in (Path.home() / "Downloads", Path.home() / "Desktop", Path.cwd()):
        hits += glob.glob(str(d / "client_secret_*.json"))
        hits += glob.glob(str(d / "oauth_client*.json"))
    hits = [h for h in hits if Path(h).resolve() != CLIENT_PATH.resolve()]
    hits.sort(key=lambda p: Path(p).stat().st_mtime, reverse=True)
    return hits[0] if hits else None


def _ensure_client():
    """The shared Desktop key is distributed via the private Brain Output Drive
    folder, NEVER via git. If it's not in place yet, adopt it from Downloads so the
    teammate never has to wrangle file paths."""
    if CLIENT_PATH.exists():
        return
    import shutil
    found = _find_downloaded_client()
    if found:
        try:
            if "installed" not in json.load(open(found)):
                found = None
        except (ValueError, OSError):
            found = None
    if found:
        shutil.copy(found, CLIENT_PATH)
        print(f"Found the Google key in {Path(found).parent.name}/ — placed it. ✓")
        return
    sys.exit(
        "I need the shared Google key once (it's never stored in git):\n"
        "  1. Open the 'ShikshaLokam — Brain Output' Drive folder (you're shared on it).\n"
        "  2. Download 'oauth_client.json' (one click).\n"
        "  3. Run this again — I'll find it in your Downloads and place it automatically.\n"
        "(Maintainer hasn't set it up? see onboarding/gsuite-setup.md Part A.)"
    )


def cmd_login(_):
    _, _, InstalledAppFlow, _, _ = _google()
    _ensure_client()
    HOME.mkdir(parents=True, exist_ok=True)
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_PATH), SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent")
    TOKEN_PATH.write_text(creds.to_json())
    TOKEN_PATH.chmod(0o600)
    cmd_whoami(None)


def cmd_whoami(_):
    info = svc("oauth2", "v2").userinfo().get().execute()
    print(f"Logged in as {info.get('email')}")


def _sig_text_to_html(body):
    """Plain-text body -> simple HTML: blank lines split paragraphs, single
    newlines become <br> (mirrors the old MCP signature hook)."""
    from html import escape
    out = []
    for p in body.replace("\r\n", "\n").split("\n\n"):
        if p.strip() == "":
            continue
        out.append("<div>" + escape(p).replace("\n", "<br>") + "</div>")
    return "<br>".join(out)


def _account_sig_html():
    """The logged-in account's signature from SIG_DIR, or '' if none on file."""
    try:
        email = svc("oauth2", "v2").userinfo().get().execute().get("email", "")
    except Exception:
        return ""
    p = SIG_DIR / f"{email}.html"
    if p.exists():
        return p.read_text().strip()
    if email:
        print(f"(no signature on file for {email} — add .claude/signatures/{email}.html; drafting without one)")
    return ""


def _build_message(to, subject, body, cc=None, with_signature=True, attach=None):
    """Build a MIME message. With the signature on (default), produce a
    multipart/alternative (text + html) carrying the LOGGED-IN person's
    signature — see SIG_DIR. Signature images use public https URLs (not cid:
    inline parts) so they survive being edited and re-sent through Gmail's web
    composer, which silently collapses cid: inline images into a single
    attachment on edit+send. `attach` = list of file paths to attach."""
    sig_html = _account_sig_html() if with_signature else ""
    if not sig_html:
        core = MIMEText(body)
    else:
        from email.mime.multipart import MIMEMultipart
        body_html = _sig_text_to_html(body)
        full_html = (body_html + "<br><br>" + sig_html) if body_html else sig_html
        core = MIMEMultipart("alternative")
        core.attach(MIMEText(body, "plain"))
        core.attach(MIMEText(full_html, "html"))
    files = [Path(p).expanduser() for p in (attach or [])]
    if files:
        import mimetypes
        from email import encoders
        from email.mime.base import MIMEBase
        from email.mime.multipart import MIMEMultipart
        msg = MIMEMultipart("mixed")
        msg.attach(core)
        for f in files:
            if not f.exists():
                sys.exit(f"attachment not found: {f}")
            ctype, _ = mimetypes.guess_type(str(f))
            maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
            part = MIMEBase(maintype, subtype)
            part.set_payload(f.read_bytes())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment", filename=f.name)
            msg.attach(part)
    else:
        msg = core
    msg["to"] = to
    if cc:
        msg["cc"] = cc
    msg["subject"] = subject
    return msg


def cmd_email_draft(a):
    body = Path(a.body_file).read_text() if a.body_file else a.body
    msg = _build_message(a.to, a.subject, body, cc=a.cc,
                         with_signature=not getattr(a, "no_signature", False),
                         attach=getattr(a, "attach", None))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    message = {"raw": raw}
    if getattr(a, "thread", None):
        message["threadId"] = a.thread  # reply inside an existing thread
    draft = svc("gmail", "v1").users().drafts().create(
        userId="me", body={"message": message}
    ).execute()
    print(f"Draft created. id={draft['id']}  (review in Gmail → Drafts)")
    print("To send after approval:  python3 tools/gsuite/gs.py email-send " + draft["id"])


def cmd_email_send(a):
    sent = svc("gmail", "v1").users().drafts().send(
        userId="me", body={"id": a.draft_id}
    ).execute()
    print(f"Sent. messageId={sent.get('id')}")


def cmd_draft_update(a):
    """Overwrite an existing draft in place (same draft id, so edits the team
    sees in Gmail → Drafts update rather than spawning a duplicate). Subject and
    recipients carry over from the existing draft when not given."""
    g = svc("gmail", "v1")
    existing = g.users().drafts().get(
        userId="me", id=a.draft_id, format="metadata"
    ).execute()
    payload = existing.get("message", {}).get("payload", {})
    to = a.to or _header(payload, "To")
    subject = a.subject or _header(payload, "Subject")
    cc = a.cc or _header(payload, "Cc") or None
    body = Path(a.body_file).read_text() if a.body_file else a.body
    msg = _build_message(to, subject, body, cc=cc,
                         with_signature=not getattr(a, "no_signature", False),
                         attach=getattr(a, "attach", None))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    message = {"raw": raw}
    thread_id = existing.get("message", {}).get("threadId")
    if thread_id:
        message["threadId"] = thread_id  # keep the draft in its thread
    g.users().drafts().update(
        userId="me", id=a.draft_id, body={"message": message}
    ).execute()
    print(f"Draft {a.draft_id} updated in place. (review in Gmail → Drafts)")
    print("To send after approval:  python3 tools/gsuite/gs.py email-send " + a.draft_id)


def _header(payload, name):
    for h in payload.get("headers", []):
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def _extract_plain(payload):
    """Best-effort plain-text body from a Gmail message payload. Prefers
    text/plain; recurses through multipart; falls back to a tag-stripped
    text/html so an edited HTML draft still reads back."""
    mime = payload.get("mimeType", "")
    body = payload.get("body", {})
    data = body.get("data")
    if mime == "text/plain" and data:
        return base64.urlsafe_b64decode(data).decode("utf-8", "replace")
    for part in payload.get("parts", []) or []:
        text = _extract_plain(part)
        if text:
            return text
    if mime == "text/html" and data:
        import re
        html = base64.urlsafe_b64decode(data).decode("utf-8", "replace")
        html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
        html = re.sub(r"</(div|p|li|h[1-6])>", "\n", html, flags=re.I)
        return re.sub(r"<[^>]+>", "", html)
    return ""


def cmd_draft_read(a):
    """List drafts (id + subject), or print one draft's subject + body so the
    brain can read a teammate's edits back and learn from them."""
    g = svc("gmail", "v1")
    if not a.draft_id:
        res = g.users().drafts().list(userId="me", maxResults=a.max).execute()
        drafts = res.get("drafts", [])
        if not drafts:
            print("(no drafts)")
            return
        for d in drafts:
            mid = d.get("message", {}).get("id")
            subj = "(no subject)"
            if mid:
                meta = g.users().messages().get(
                    userId="me", id=mid, format="metadata",
                    metadataHeaders=["Subject"],
                ).execute()
                subj = _header(meta.get("payload", {}), "Subject") or subj
            print(f'{d["id"]}\t{subj}')
        return
    draft = g.users().drafts().get(
        userId="me", id=a.draft_id, format="full"
    ).execute()
    payload = draft.get("message", {}).get("payload", {})
    print(f'Subject: {_header(payload, "Subject")}')
    print(f'To: {_header(payload, "To")}')
    print("---")
    print(_extract_plain(payload).strip())


def _md_to_html(text):
    """Minimal markdown -> HTML so Docs conversion keeps headings/bold/lists."""
    out, in_list = [], False
    for line in text.splitlines():
        s = line.rstrip()
        if s.startswith("# "):
            out.append(f"<h1>{s[2:]}</h1>"); continue
        if s.startswith("## "):
            out.append(f"<h2>{s[3:]}</h2>"); continue
        if s.startswith("### "):
            out.append(f"<h3>{s[4:]}</h3>"); continue
        if s.startswith(("- ", "* ")):
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{s[2:]}</li>"); continue
        if in_list:
            out.append("</ul>"); in_list = False
        out.append(f"<p>{s}</p>" if s else "<br/>")
    if in_list:
        out.append("</ul>")
    html = "\n".join(out)
    # bold / italic
    import re
    html = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html)
    html = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"<i>\1</i>", html)
    return f"<html><body>{html}</body></html>"


def cmd_doc_create(a):
    _, _, _, _, MediaInMemoryUpload = _google()
    src = Path(a.body_file).read_text() if a.body_file else a.body
    html = _md_to_html(src)
    meta = {"name": a.title, "mimeType": "application/vnd.google-apps.document"}
    folder = a.folder or load_map().get("Docs")
    if folder:
        meta["parents"] = [folder]
    media = MediaInMemoryUpload(html.encode(), mimetype="text/html", resumable=False)
    doc = svc("drive", "v3").files().create(
        body=meta, media_body=media, fields="id,webViewLink", supportsAllDrives=True
    ).execute()
    print(f"Doc created: {doc.get('webViewLink')}")


def cmd_drive_find(a):
    """Find Drive files by name substring (newest first) so the brain can
    locate a doc the team mentions by title."""
    drive = svc("drive", "v3")
    q = f"name contains '{a.query}' and trashed = false"
    res = drive.files().list(
        q=q, pageSize=a.max,
        fields="files(id,name,mimeType,webViewLink,modifiedTime)",
        orderBy="modifiedTime desc",
        includeItemsFromAllDrives=True, supportsAllDrives=True,
    ).execute()
    files = res.get("files", [])
    if not files:
        print("(no matches)")
        return
    for f in files:
        kind = f["mimeType"].rsplit(".", 1)[-1]
        print(f'{f["id"]}\t{kind}\t{f["name"]}\t{f.get("webViewLink", "")}')


def cmd_drive_move(a):
    """File a Drive item into its proper folder. Folder hygiene is a standing
    rule: nothing the brain creates is left loose in the generic Docs folder."""
    drive = svc("drive", "v3")
    cur = drive.files().get(
        fileId=a.id, fields="id,name,parents,webViewLink", supportsAllDrives=True,
    ).execute()
    old = ",".join(cur.get("parents", []))
    f = drive.files().update(
        fileId=a.id, addParents=a.folder, removeParents=old,
        fields="id,name,parents,webViewLink", supportsAllDrives=True,
    ).execute()
    print(f'Moved "{f["name"]}" → folder {a.folder}\n{f.get("webViewLink", "")}')


def _read_elements(content):
    """Flatten a list of structural elements (paragraphs + tables) to text."""
    out = []
    for el in content or []:
        para = el.get("paragraph")
        if para:
            for run in para.get("elements", []):
                tr = run.get("textRun")
                if tr:
                    out.append(tr.get("content", ""))
        table = el.get("table")
        if table:
            for row in table.get("tableRows", []):
                for cell in row.get("tableCells", []):
                    out.append(_read_elements(cell.get("content", [])))
    return "".join(out)


def _tab_text(tab):
    title = tab.get("tabProperties", {}).get("title", "")
    body = tab.get("documentTab", {}).get("body", {})
    parts = [f"\n===== TAB: {title} =====\n", _read_elements(body.get("content", []))]
    for child in tab.get("childTabs", []) or []:
        parts.append(_tab_text(child))
    return "".join(parts)


def _doc_text(doc):
    """Flatten a Docs API document to plain text, across all tabs if present."""
    tabs = doc.get("tabs")
    if tabs:
        return "".join(_tab_text(t) for t in tabs)
    return _read_elements(doc.get("body", {}).get("content", []))


def cmd_doc_read(a):
    """Print a Google Doc's plain text (all tabs) so the brain can work from it."""
    doc = svc("docs", "v1").documents().get(
        documentId=a.id, includeTabsContent=True
    ).execute()
    print(_doc_text(doc).strip())


def cmd_doc_replace(a):
    """Find-and-replace exact text in a Google Doc in place (applies across all
    tabs). Use to action review comments without recreating the doc."""
    body = {"requests": [{
        "replaceAllText": {
            "containsText": {"text": a.find, "matchCase": True},
            "replaceText": a.replace,
        }
    }]}
    res = svc("docs", "v1").documents().batchUpdate(
        documentId=a.id, body=body
    ).execute()
    n = (res.get("replies") or [{}])[0].get("replaceAllText", {}).get("occurrencesChanged", 0)
    print(f"Replaced {n} occurrence(s).")


def _find_tab(tabs, title):
    for t in tabs or []:
        if t.get("tabProperties", {}).get("title") == title:
            return t
        hit = _find_tab(t.get("childTabs", []), title)
        if hit:
            return hit
    return None


def cmd_doc_fill_tab(a):
    """Insert text into an existing tab (by title). Tabs can't be created via
    the API, so the tab must already exist; this fills it in one shot."""
    docs = svc("docs", "v1")
    doc = docs.documents().get(documentId=a.id, includeTabsContent=True).execute()
    tab = _find_tab(doc.get("tabs", []), a.tab)
    if not tab:
        sys.exit(f"No tab titled {a.tab!r}. Create the (blank) tab in the doc first.")
    tab_id = tab["tabProperties"]["tabId"]
    text = Path(a.body_file).read_text() if a.body_file else a.body
    docs.documents().batchUpdate(
        documentId=a.id,
        body={"requests": [{"insertText": {
            "location": {"tabId": tab_id, "index": 1}, "text": text,
        }}]},
    ).execute()
    print(f"Filled tab {a.tab!r}.")


def cmd_doc_set_tab(a):
    """REPLACE an existing tab's whole body with new text — the in-place edit.

    This is the default when a Doc is the working surface: the team reads and
    comments in the Doc, so revisions must land in the tab they already have
    open, not in a new one. `doc-fill-tab` only prepends; `doc-add-tab` makes a
    fresh tab and leaves the stale draft behind. Use those two only when you
    genuinely want to add.
    """
    docs = svc("docs", "v1")
    doc = docs.documents().get(documentId=a.id, includeTabsContent=True).execute()
    tab = _find_tab(doc.get("tabs", []), a.tab)
    if not tab:
        sys.exit(f"No tab titled {a.tab!r}.")
    tab_id = tab["tabProperties"]["tabId"]
    content = tab["documentTab"]["body"]["content"]
    end = content[-1]["endIndex"] - 1  # final newline can't be deleted
    text = Path(a.body_file).read_text() if a.body_file else a.body
    reqs = []
    if end > 1:
        reqs.append({"deleteContentRange": {"range": {
            "tabId": tab_id, "startIndex": 1, "endIndex": end}}})
    reqs.append({"insertText": {"location": {"tabId": tab_id, "index": 1}, "text": text}})
    docs.documents().batchUpdate(documentId=a.id, body={"requests": reqs}).execute()
    print(f"Replaced contents of tab {a.tab!r}.")


def cmd_doc_delete_tab(a):
    """Blank a superseded tab and leave a pointer in it.

    The Docs API can CREATE tabs (`addDocumentTab`) but has no delete request —
    `deleteDocumentTab` does not exist and returns 400. Verified 2026-07-23.
    So a tab can only be emptied here; the person removes it with a right-click
    in the tab sidebar. This is the reason to prefer `doc-set-tab` (edit the tab
    the team already has open) over `doc-add-tab` for revisions.
    """
    note = a.note or "SUPERSEDED - do not use. This tab can be deleted (right-click it in the sidebar).\n"
    docs = svc("docs", "v1")
    doc = docs.documents().get(documentId=a.id, includeTabsContent=True).execute()
    tab = _find_tab(doc.get("tabs", []), a.tab)
    if not tab:
        sys.exit(f"No tab titled {a.tab!r}.")
    tab_id = tab["tabProperties"]["tabId"]
    end = tab["documentTab"]["body"]["content"][-1]["endIndex"] - 1
    reqs = []
    if end > 1:
        reqs.append({"deleteContentRange": {"range": {
            "tabId": tab_id, "startIndex": 1, "endIndex": end}}})
    reqs.append({"insertText": {"location": {"tabId": tab_id, "index": 1}, "text": note}})
    docs.documents().batchUpdate(documentId=a.id, body={"requests": reqs}).execute()
    print(f"Blanked tab {a.tab!r}. The API cannot delete tabs — remove it by hand if you want it gone.")


def cmd_doc_add_tab(a):
    """Create a NEW tab in a doc and fill it — the correct way to add a new draft
    (e.g. an InvokED invitee) to the shared register. Tabs ARE creatable via the
    Docs API request `addDocumentTab` (NOT `createTab`/`insertTab`). Never fall
    back to a separate doc just because a tab doesn't exist yet."""
    docs = svc("docs", "v1")
    doc = docs.documents().get(documentId=a.id, fields="tabs(tabProperties(index))").execute()
    idx = len(doc.get("tabs", []))  # append at the end
    r = docs.documents().batchUpdate(documentId=a.id, body={"requests": [
        {"addDocumentTab": {"tabProperties": {"title": a.title, "index": idx}}}
    ]}).execute()
    tab_id = r["replies"][0]["addDocumentTab"]["tabProperties"]["tabId"]
    text = Path(a.body_file).read_text() if a.body_file else (a.body or "")
    if text:
        docs.documents().batchUpdate(documentId=a.id, body={"requests": [
            {"insertText": {"location": {"tabId": tab_id, "index": 1}, "text": text}}
        ]}).execute()
    print(f"Created tab {a.title!r} (tabId {tab_id}) and filled it.")


def cmd_doc_comments(a):
    """List a Doc's comments (author, the text they anchor to, the comment, and
    replies) so the brain can act on review feedback. Skips resolved unless --all."""
    drive = svc("drive", "v3")
    res = drive.comments().list(
        fileId=a.id, pageSize=100,
        fields="comments(id,author/displayName,content,resolved,"
               "quotedFileContent/value,replies(author/displayName,content))",
    ).execute()
    comments = res.get("comments", [])
    if not a.all:
        comments = [c for c in comments if not c.get("resolved")]
    if not comments:
        print("(no comments)")
        return
    for i, c in enumerate(comments, 1):
        who = c.get("author", {}).get("displayName", "?")
        anchor = (c.get("quotedFileContent") or {}).get("value", "")
        print(f"[{i}] {who}{' (resolved)' if c.get('resolved') else ''}  id={c.get('id')}")
        if anchor:
            print(f'    on: "{anchor}"')
        print(f"    {c.get('content', '')}")
        for r in c.get("replies", []) or []:
            print(f"    ↳ {r.get('author', {}).get('displayName', '?')}: {r.get('content', '')}")


def cmd_comment_resolve(a):
    """Resolve a Doc comment after its feedback has been incorporated. Optionally
    leave a closing reply first (e.g. what changed). Get comment ids from
    `doc-comments`."""
    drive = svc("drive", "v3")
    drive.replies().create(
        fileId=a.id, commentId=a.comment,
        body={"content": a.reply or "Done.", "action": "resolve"}, fields="id,action",
    ).execute()
    print(f"Resolved comment {a.comment}.")


def cmd_drive_folder(a):
    meta = {"name": a.name, "mimeType": "application/vnd.google-apps.folder"}
    if a.parent:
        meta["parents"] = [a.parent]
    f = svc("drive", "v3").files().create(
        body=meta, fields="id,webViewLink", supportsAllDrives=True
    ).execute()
    print(f"Folder '{a.name}': {f.get('webViewLink')}  id={f['id']}")
    return f["id"]


def _share(drive, file_id, email):
    try:
        drive.permissions().create(
            fileId=file_id,
            body={"type": "user", "role": "writer", "emailAddress": email},
            sendNotificationEmail=False, supportsAllDrives=True,
        ).execute()
    except Exception as e:  # noqa: BLE001 — best-effort, report and continue
        print(f"  (could not share with {email}: {e})")


def cmd_drive_init(_):
    drive = svc("drive", "v3")
    root_name = DEFAULT_ROOT
    taxonomy = DEFAULT_TAXONOMY
    root = drive.files().create(
        body={"name": root_name, "mimeType": "application/vnd.google-apps.folder"},
        fields="id,webViewLink",
    ).execute()
    mapping = {"_root": root["id"], "_root_link": root.get("webViewLink")}
    print(f"Created root: {root.get('webViewLink')}")
    for name in taxonomy:
        sub = drive.files().create(
            body={"name": name, "mimeType": "application/vnd.google-apps.folder",
                  "parents": [root["id"]]},
            fields="id",
        ).execute()
        mapping[name] = sub["id"]
        print(f"  + {name}")
    for email in team_emails():
        _share(drive, root["id"], email)
        print(f"  shared with {email}")
    DRIVE_MAP.write_text(json.dumps(mapping, indent=2) + "\n")
    print(f"\nWrote {DRIVE_MAP.relative_to(REPO)} — commit it so the team shares the same folders.")


def cmd_cal_invite(a):
    event = {
        "summary": a.summary,
        "description": a.description or "",
        "start": {"dateTime": a.start, "timeZone": a.tz},
        "end": {"dateTime": a.end, "timeZone": a.tz},
    }
    if a.attendees:
        event["attendees"] = [{"email": e.strip()} for e in a.attendees.split(",")]
    send = "all" if a.notify else "none"
    ev = svc("calendar", "v3").events().insert(
        calendarId="primary", body=event, sendUpdates=send
    ).execute()
    note = "invites emailed" if a.notify else "added to your calendar only (no emails)"
    print(f"Event created ({note}): {ev.get('htmlLink')}")


def cmd_sheet_read(a):
    res = svc("sheets", "v4").spreadsheets().values().get(
        spreadsheetId=a.id, range=a.range
    ).execute()
    rows = res.get("values", [])
    if not rows:
        print("(empty range)")
        return
    for r in rows:
        print("\t".join(str(c) for c in r))


def cmd_sheet_update(a):
    # --values is row(s): cells separated by "|", rows separated by ";;"
    rows = [[c for c in row.split("|")] for row in a.values.split(";;")]
    res = svc("sheets", "v4").spreadsheets().values().update(
        spreadsheetId=a.id, range=a.range, valueInputOption="USER_ENTERED",
        body={"values": rows},
    ).execute()
    print(f"Updated {res.get('updatedCells', 0)} cell(s) in {a.range}.")


def cmd_sheet_add_tab(a):
    """Create a NEW tab in a Sheet and fill it. Existing tabs are never touched
    unless --replace names one explicitly. Rows come from a JSON file (list of
    lists) so cell text can contain any character — the --values pipe syntax of
    sheet-update can't carry '|' or ';;'."""
    s = svc("sheets", "v4")

    meta = s.spreadsheets().get(spreadsheetId=a.id).execute()
    existing = {sh["properties"]["title"]: sh["properties"]["sheetId"]
                for sh in meta.get("sheets", [])}
    if a.title in existing:
        if not a.replace:
            print(f"Tab '{a.title}' already exists — pass --replace to overwrite it.")
            return
        s.spreadsheets().batchUpdate(spreadsheetId=a.id, body={
            "requests": [{"deleteSheet": {"sheetId": existing[a.title]}}]
        }).execute()

    added = s.spreadsheets().batchUpdate(spreadsheetId=a.id, body={
        "requests": [{"addSheet": {"properties": {"title": a.title}}}]
    }).execute()
    sheet_id = added["replies"][0]["addSheet"]["properties"]["sheetId"]

    rows = json.loads(Path(a.json).read_text()) if a.json else []
    if rows:
        ncols = max(len(r) for r in rows)
        s.spreadsheets().values().update(
            spreadsheetId=a.id, range=f"'{a.title}'!A1",
            valueInputOption="USER_ENTERED", body={"values": rows},
        ).execute()

        reqs = [
            {"repeatCell": {
                "range": {"sheetId": sheet_id},
                "cell": {"userEnteredFormat": {"wrapStrategy": "WRAP",
                                               "verticalAlignment": "TOP"}},
                "fields": "userEnteredFormat(wrapStrategy,verticalAlignment)"}},
            {"updateDimensionProperties": {
                "range": {"sheetId": sheet_id, "dimension": "COLUMNS",
                          "startIndex": 0, "endIndex": ncols},
                "properties": {"pixelSize": a.col_width},
                "fields": "pixelSize"}},
        ]
        if a.header_row:
            hr = a.header_row - 1
            reqs.append({"repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": hr, "endRowIndex": hr + 1},
                "cell": {"userEnteredFormat": {"textFormat": {"bold": True},
                                               "backgroundColor": {"red": 0.85, "green": 0.87, "blue": 0.94}}},
                "fields": "userEnteredFormat(textFormat,backgroundColor)"}})
        if a.freeze:
            reqs.append({"updateSheetProperties": {
                "properties": {"sheetId": sheet_id,
                               "gridProperties": {"frozenRowCount": a.freeze}},
                "fields": "gridProperties.frozenRowCount"}})
        s.spreadsheets().batchUpdate(spreadsheetId=a.id, body={"requests": reqs}).execute()

    print(f"Tab '{a.title}' created — {len(rows)} row(s) — "
          f"https://docs.google.com/spreadsheets/d/{a.id}/edit#gid={sheet_id}")


# ---- gmail: search + labels + filters --------------------------------------
def _resolve_label(g, name_or_id):
    """Return a label id for a display name or id (system or user). None if
    no user/system label matches."""
    labels = g.users().labels().list(userId="me").execute().get("labels", [])
    for l in labels:
        if name_or_id in (l["id"], l["name"]):
            return l["id"]
    return None


def _subject(g, thread_id):
    meta = g.users().threads().get(
        userId="me", id=thread_id, format="metadata", metadataHeaders=["Subject"]
    ).execute()
    msgs = meta.get("messages", [])
    if msgs:
        for h in msgs[0].get("payload", {}).get("headers", []):
            if h["name"] == "Subject":
                return h["value"]
    return "(no subject)"


def cmd_search(a):
    g = svc("gmail", "v1")
    res = g.users().threads().list(userId="me", q=a.query, maxResults=a.max).execute()
    threads = res.get("threads", [])
    if not threads:
        print("(no matches)")
        return
    for t in threads:
        print(f'{t["id"]}\t{_subject(g, t["id"])}')


def cmd_label_list(a):
    g = svc("gmail", "v1")
    labels = g.users().labels().list(userId="me").execute().get("labels", [])
    user = [l for l in labels if l.get("type") == "user"]
    for l in sorted(user, key=lambda x: x["name"].lower()):
        print(f'{l["id"]}\t{l["name"]}')


def cmd_label_create(a):
    g = svc("gmail", "v1")
    if _resolve_label(g, a.name):
        print(f'Label already exists: {a.name}')
        return
    body = {"name": a.name,
            "labelListVisibility": "labelShow",
            "messageListVisibility": "show"}
    if a.bg or a.text:
        body["color"] = {"backgroundColor": a.bg or "#cccccc",
                         "textColor": a.text or "#000000"}
    l = g.users().labels().create(userId="me", body=body).execute()
    print(f'Created label {l["name"]}  id={l["id"]}')


def _modify_threads(a, add):
    g = svc("gmail", "v1")
    lid = _resolve_label(g, a.label)
    if not lid:
        sys.exit(f'Label not found: {a.label}  '
                 f'(create it:  gs.py label-create --name "{a.label}")')
    key = "addLabelIds" if add else "removeLabelIds"
    ids = [t.strip() for t in a.thread.split(",") if t.strip()]
    for tid in ids:
        g.users().threads().modify(userId="me", id=tid, body={key: [lid]}).execute()
    print(f'{"Labelled" if add else "Unlabelled"} {len(ids)} thread(s) with {a.label}.')


def cmd_label_apply(a):
    _modify_threads(a, add=True)


def cmd_label_remove(a):
    _modify_threads(a, add=False)


def cmd_filter_create(a):
    g = svc("gmail", "v1")
    lid = _resolve_label(g, a.label)
    if not lid:
        sys.exit(f'Label not found: {a.label}  '
                 f'(create it:  gs.py label-create --name "{a.label}")')
    action = {"addLabelIds": [lid]}
    if a.archive:                      # skip the inbox, file straight under the label
        action["removeLabelIds"] = ["INBOX"]
    body = {"criteria": {"query": a.query}, "action": action}
    f = g.users().settings().filters().create(userId="me", body=body).execute()
    print(f'Filter created id={f.get("id")} — applies "{a.label}" to: {a.query}')


# ---- cli -------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(prog="gs.py", description="ShikshaLokam G-Suite engine")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("login", help="one-time browser consent").set_defaults(fn=cmd_login)
    sub.add_parser("whoami", help="show logged-in account").set_defaults(fn=cmd_whoami)

    d = sub.add_parser("email-draft", help="create a Gmail draft (nothing sent)")
    d.add_argument("--to", required=True)
    d.add_argument("--subject", required=True)
    d.add_argument("--cc")
    d.add_argument("--body")
    d.add_argument("--body-file")
    d.add_argument("--attach", action="append",
                   help="file to attach (repeatable)")
    d.add_argument("--thread", help="Gmail threadId to draft the reply inside")
    d.add_argument("--no-signature", action="store_true",
                   help="skip your signature (your .claude/signatures/<email>.html is attached by default)")
    d.set_defaults(fn=cmd_email_draft)

    s = sub.add_parser("email-send", help="send a draft (ONLY after approval)")
    s.add_argument("draft_id")
    s.set_defaults(fn=cmd_email_send)

    du = sub.add_parser("draft-update",
                        help="overwrite an existing draft in place (to/subject carry over if omitted)")
    du.add_argument("draft_id")
    du.add_argument("--to")
    du.add_argument("--subject")
    du.add_argument("--cc")
    du.add_argument("--body")
    du.add_argument("--body-file")
    du.add_argument("--attach", action="append",
                    help="file to attach (repeatable)")
    du.add_argument("--no-signature", action="store_true",
                    help="skip your signature (your .claude/signatures/<email>.html is attached by default)")
    du.set_defaults(fn=cmd_draft_update)

    dr = sub.add_parser("draft-read",
                        help="read a draft's subject+body (or list drafts) to learn from edits")
    dr.add_argument("draft_id", nargs="?",
                    help="draft id to read; omit to list drafts (id<TAB>subject)")
    dr.add_argument("--max", type=int, default=30)
    dr.set_defaults(fn=cmd_draft_read)

    dc = sub.add_parser("doc-create", help="make a Google Doc from text/markdown")
    dc.add_argument("--title", required=True)
    dc.add_argument("--body")
    dc.add_argument("--body-file")
    dc.add_argument("--folder", help="folder id (default: Docs from drive_map.json)")
    dc.set_defaults(fn=cmd_doc_create)

    dfind = sub.add_parser("drive-find", help="find Drive files by name (id<TAB>kind<TAB>name<TAB>link)")
    dfind.add_argument("--query", required=True, help="name substring to match")
    dfind.add_argument("--max", type=int, default=20)
    dfind.set_defaults(fn=cmd_drive_find)

    drd = sub.add_parser("doc-read", help="print a Google Doc's plain text")
    drd.add_argument("--id", required=True, help="document id")
    drd.set_defaults(fn=cmd_doc_read)

    drp = sub.add_parser("doc-replace", help="find/replace exact text in a Doc in place")
    drp.add_argument("--id", required=True, help="document id")
    drp.add_argument("--find", required=True, help="exact text to find (case-sensitive)")
    drp.add_argument("--replace", required=True, help="replacement text")
    drp.set_defaults(fn=cmd_doc_replace)

    dft = sub.add_parser("doc-fill-tab", help="insert text into an existing tab (by title)")
    dft.add_argument("--id", required=True, help="document id")
    dft.add_argument("--tab", required=True, help="exact tab title (must already exist)")
    dft.add_argument("--body")
    dft.add_argument("--body-file")
    dft.set_defaults(fn=cmd_doc_fill_tab)

    dst = sub.add_parser("doc-set-tab",
                         help="REPLACE an existing tab's contents in place — the default edit")
    dst.add_argument("--id", required=True, help="document id")
    dst.add_argument("--tab", required=True, help="exact tab title (must already exist)")
    dst.add_argument("--body")
    dst.add_argument("--body-file")
    dst.set_defaults(fn=cmd_doc_set_tab)

    ddt = sub.add_parser("doc-delete-tab",
                         help="blank a superseded tab (the API cannot delete tabs)")
    ddt.add_argument("--id", required=True, help="document id")
    ddt.add_argument("--tab", required=True, help="exact tab title")
    ddt.add_argument("--note", help="text to leave in the emptied tab")
    ddt.set_defaults(fn=cmd_doc_delete_tab)

    dad = sub.add_parser("doc-add-tab",
                         help="create a NEW tab (addDocumentTab) and fill it — for a new draft")
    dad.add_argument("--id", required=True, help="document id")
    dad.add_argument("--title", required=True, help="tab title, e.g. the invitee's name")
    dad.add_argument("--body")
    dad.add_argument("--body-file")
    dad.set_defaults(fn=cmd_doc_add_tab)

    dco = sub.add_parser("doc-comments", help="list a Doc's comments + replies")
    dco.add_argument("--id", required=True, help="document id")
    dco.add_argument("--all", action="store_true", help="include resolved comments")
    dco.set_defaults(fn=cmd_doc_comments)

    cr = sub.add_parser("comment-resolve",
                        help="resolve a Doc comment (get its id from doc-comments)")
    cr.add_argument("--id", required=True, help="document id")
    cr.add_argument("--comment", required=True, help="comment id from doc-comments")
    cr.add_argument("--reply", help="closing reply to leave (default 'Done.')")
    cr.set_defaults(fn=cmd_comment_resolve)

    df = sub.add_parser("drive-folder", help="create a Drive folder")
    df.add_argument("--name", required=True)
    df.add_argument("--parent")
    df.set_defaults(fn=cmd_drive_folder)

    dm = sub.add_parser("drive-move", help="move a file/folder into its proper folder")
    dm.add_argument("--id", required=True, help="file or folder id to move")
    dm.add_argument("--folder", required=True, help="destination folder id")
    dm.set_defaults(fn=cmd_drive_move)

    sub.add_parser("drive-init", help="build + share the Brain Output tree").set_defaults(fn=cmd_drive_init)

    ci = sub.add_parser("cal-invite", help="create a calendar event")
    ci.add_argument("--summary", required=True)
    ci.add_argument("--start", required=True, help="ISO, e.g. 2026-06-12T15:00:00")
    ci.add_argument("--end", required=True)
    ci.add_argument("--tz", default="Asia/Kolkata")
    ci.add_argument("--attendees", help="comma-separated emails")
    ci.add_argument("--description")
    ci.add_argument("--notify", action="store_true", help="email attendees (the 'send')")
    ci.set_defaults(fn=cmd_cal_invite)

    sr = sub.add_parser("sheet-read", help="read a range from a Google Sheet")
    sr.add_argument("--id", required=True, help="spreadsheet id")
    sr.add_argument("--range", required=True, help="e.g. 'Sheet1!A1:C10'")
    sr.set_defaults(fn=cmd_sheet_read)

    su = sub.add_parser("sheet-update", help="update cells in a Google Sheet")
    su.add_argument("--id", required=True, help="spreadsheet id")
    su.add_argument("--range", required=True, help="e.g. 'Sheet1!A1'")
    su.add_argument("--values", required=True,
                    help="cells split by '|', rows split by ';;'  (e.g. \"a|b||c;;d|e|f\")")
    su.set_defaults(fn=cmd_sheet_update)

    sat = sub.add_parser("sheet-add-tab",
                         help="create a NEW tab in a Sheet and fill it from a JSON file")
    sat.add_argument("--id", required=True, help="spreadsheet id")
    sat.add_argument("--title", required=True, help="new tab name")
    sat.add_argument("--json", help="path to a JSON file: list of rows, each a list of cells")
    sat.add_argument("--replace", action="store_true",
                     help="overwrite the tab if it already exists (otherwise refuses)")
    sat.add_argument("--header-row", type=int, default=0,
                     help="1-indexed row to bold+shade as the header (0 = none)")
    sat.add_argument("--freeze", type=int, default=0, help="freeze this many top rows")
    sat.add_argument("--col-width", type=int, default=260, help="column width in pixels")
    sat.set_defaults(fn=cmd_sheet_add_tab)

    se = sub.add_parser("search", help="search threads (prints 'threadId<TAB>subject')")
    se.add_argument("--query", required=True, help="Gmail search syntax")
    se.add_argument("--max", type=int, default=30)
    se.set_defaults(fn=cmd_search)

    ll = sub.add_parser("label-list", help="list user labels (id<TAB>name)")
    ll.set_defaults(fn=cmd_label_list)

    lc = sub.add_parser("label-create", help="create a label")
    lc.add_argument("--name", required=True)
    lc.add_argument("--bg", help="background hex, e.g. #16a766")
    lc.add_argument("--text", help="text hex, e.g. #ffffff")
    lc.set_defaults(fn=cmd_label_create)

    la = sub.add_parser("label-apply", help="add a label to thread(s)")
    la.add_argument("--thread", required=True, help="comma-separated thread ids")
    la.add_argument("--label", required=True, help="label name or id")
    la.set_defaults(fn=cmd_label_apply)

    lr = sub.add_parser("label-remove", help="remove a label from thread(s)")
    lr.add_argument("--thread", required=True, help="comma-separated thread ids")
    lr.add_argument("--label", required=True, help="label name or id")
    lr.set_defaults(fn=cmd_label_remove)

    fc = sub.add_parser("filter-create", help="auto-label future mail matching a query")
    fc.add_argument("--label", required=True, help="label name or id to apply")
    fc.add_argument("--query", required=True, help="Gmail search syntax to match on")
    fc.add_argument("--archive", action="store_true", help="also skip the inbox")
    fc.set_defaults(fn=cmd_filter_create)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
