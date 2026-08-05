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
from email.header import Header
from pathlib import Path

# Windows terminals default to a legacy code page (cp1252); our output uses
# UTF-8 characters (→, 📅, em-dashes, curly quotes). Without this, every
# non-ASCII print aborts the whole command with UnicodeEncodeError. Force UTF-8
# on stdout/stderr so the engine is robust everywhere. No-op on Linux/macOS.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):  # non-reconfigurable stream (e.g. piped)
        pass

# ---- paths -----------------------------------------------------------------
REPO = Path(__file__).resolve().parents[2]
CLIENT_PATH = REPO / "tools" / "gsuite" / "oauth_client.json"   # committed (desktop app)
DRIVE_MAP = REPO / "tools" / "gsuite" / "drive_map.json"        # committed (shared folder IDs)
BRAIN_YML = REPO / "brain.yml"

HOME = Path.home() / ".shikshalokam"                            # OUTSIDE the repo
TOKEN_PATH = HOME / "token.json"                                # personal, never committed

# Gmail's API does NOT auto-append the account signature to API-created drafts
# (that only happens in the web compose UI), so we attach it ourselves. The
# signature's images are referenced by public https URL (the same hosted URLs
# Gmail uses for the native signature), NOT cid: inline parts — Gmail's web
# composer collapses cid: inline images into one attachment when a draft is
# edited and sent from there, which silently breaks the signature.
SIG_HTML = REPO / ".claude" / "gmail-signature.html"

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
    "https://www.googleapis.com/auth/presentations",     # Google Slides
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


_LOGGED_IN_EMAIL = None


def logged_in_email():
    """The signed-in account's email (cached per run). Empty string on failure."""
    global _LOGGED_IN_EMAIL
    if _LOGGED_IN_EMAIL is None:
        try:
            info = svc("oauth2", "v2").userinfo().get().execute()
            _LOGGED_IN_EMAIL = (info.get("email") or "").strip().lower()
        except Exception:
            _LOGGED_IN_EMAIL = ""
    return _LOGGED_IN_EMAIL


def resolve_sig_path():
    """Per-user signature so each teammate signs as themselves:
    .claude/signatures/<logged-in-email>.html if it exists, else the shared
    default SIG_HTML. (A multi-person brain must never sign one person as another.)"""
    email = logged_in_email()
    if email:
        per_user = REPO / ".claude" / "signatures" / f"{email}.html"
        if per_user.exists():
            return per_user
    return SIG_HTML


def team_emails():
    """Teammate emails from brain.yml (best-effort; used to auto-share Drive)."""
    emails = []
    try:
        for line in BRAIN_YML.read_text(encoding="utf-8").splitlines():
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
        return json.loads(DRIVE_MAP.read_text(encoding="utf-8"))
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


def _gcal_url(title, start, end, all_day=True, location="", details="", tz="Asia/Kolkata"):
    """Build a Google Calendar "add event" template URL (one click pre-fills the
    event in the recipient's Google Calendar). Dates are YYYY-MM-DD (all-day) or
    ISO datetimes YYYY-MM-DDTHH:MM:SS. For an all-day multi-day event Google
    treats the end date as EXCLUSIVE, so we bump it by one day so 26–27 reads as
    both days, not just the 26th. For timed events we pass `ctz` so the hour is
    anchored to the event's timezone — else a guest in another timezone sees the
    wrong time."""
    from urllib.parse import urlencode

    def _compact(s):
        return s.replace("-", "").replace(":", "")

    params = {"action": "TEMPLATE", "text": title, "details": details, "location": location}
    if all_day:
        from datetime import datetime, timedelta
        s = _compact(start)
        end_dt = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
        params["dates"] = f"{s}/{end_dt.strftime('%Y%m%d')}"
    else:
        params["dates"] = f"{_compact(start)}/{_compact(end)}"
        params["ctz"] = tz  # anchor timed events to the event's timezone
    return "https://calendar.google.com/calendar/render?" + urlencode(
        {k: v for k, v in params.items() if v}
    )


def _gcal_button(url, label="\U0001F4C5 Add to Google Calendar"):
    """An email-safe styled 'Add to Google Calendar' button (inline styles, no
    external CSS — survives Gmail/most clients). Gmail auto-links a bare URL but
    it looks raw; this gives the invite a real button."""
    return (
        '<div style="margin:20px 0;">'
        f'<a href="{url}" target="_blank" '
        'style="display:inline-block;background:#1a73e8;color:#ffffff;'
        'text-decoration:none;padding:11px 20px;border-radius:6px;'
        'font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:bold;">'
        f'{label}</a></div>'
    )


def _ics(title, start, end, all_day=True, location="", details="",
         organizer_email="", organizer_name="ShikshaLokam",
         attendee_email="", uid=None, method="PUBLISH"):
    """Build an iCalendar (RFC 5545) invitation. Embedded as a text/calendar
    part, this is what makes Gmail render its OWN native event card inside the
    email (the 'part of Google' look) — and, saved as an .ics, what lets Apple
    Calendar / Outlook add the event in one tap.

    METHOD:PUBLISH → a clean 'Add to Calendar' card, no RSVP (right for a broad
    guest send). METHOD:REQUEST → a Yes/Maybe/No invitation (RSVPs flow back to
    the organizer)."""
    from datetime import datetime, timedelta, timezone

    def esc(s):
        return (str(s).replace("\\", "\\\\").replace(";", "\\;")
                .replace(",", "\\,").replace("\r\n", "\\n").replace("\n", "\\n"))

    def fold(line):
        # RFC 5545 caps a content line at 75 octets; continue with a leading
        # space. Fold on characters (~72) — safe for our mostly-ASCII values.
        if len(line) <= 72:
            return line
        out, i = [line[:72]], 72
        while i < len(line):
            out.append(" " + line[i:i + 71])
            i += 71
        return "\r\n".join(out)

    if all_day:
        dt_start = f"DTSTART;VALUE=DATE:{start.replace('-', '')}"
        end_excl = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
        dt_end = f"DTEND;VALUE=DATE:{end_excl.strftime('%Y%m%d')}"
    else:
        c = lambda s: s.replace("-", "").replace(":", "")
        dt_start = f"DTSTART;TZID=Asia/Kolkata:{c(start)}"
        dt_end = f"DTEND;TZID=Asia/Kolkata:{c(end)}"

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if not uid:
        slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in title).strip("-")
        uid = f"{slug}-{start.replace('-', '')}@shikshalokam.org"

    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0",
        "PRODID:-//ShikshaLokam//gs.py//EN", "CALSCALE:GREGORIAN",
        f"METHOD:{method}", "BEGIN:VEVENT",
        f"UID:{uid}", f"DTSTAMP:{stamp}", dt_start, dt_end,
        f"SUMMARY:{esc(title)}",
    ]
    if location:
        lines.append(f"LOCATION:{esc(location)}")
    if details:
        lines.append(f"DESCRIPTION:{esc(details)}")
    if organizer_email:
        lines.append(f"ORGANIZER;CN={esc(organizer_name)}:mailto:{organizer_email}")
    if method == "REQUEST" and attendee_email:
        lines.append("ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;"
                     f"RSVP=TRUE:mailto:{attendee_email}")
    lines += ["STATUS:CONFIRMED", "SEQUENCE:0", "END:VEVENT", "END:VCALENDAR"]
    return "\r\n".join(fold(l) for l in lines) + "\r\n"


def _build_message(to, subject, body, cc=None, with_signature=True,
                   gcal_url=None, ics=None, ics_method="PUBLISH"):
    """Build a MIME message. With the signature on (default), produce a
    multipart/alternative (text + html). The signature references its images by
    public https URL (not cid: inline parts) — see SIG_HTML — so it survives
    being edited and re-sent through Gmail's web composer, which silently
    collapses cid: inline images into a single attachment on edit+send.

    When `ics` is given, a text/calendar part is added so Gmail renders its
    native event card, and a copy is attached as invite.ics for other clients."""
    from email.mime.multipart import MIMEMultipart
    sig_path = resolve_sig_path() if with_signature else None
    sig_html = sig_path.read_text(encoding="utf-8").strip() if (sig_path and sig_path.exists()) else ""
    # Add-to-Calendar button. Place it exactly where a {{ADD_TO_CALENDAR}} marker
    # sits in the body; otherwise append it after the body. Plain-text carries a
    # link fallback in the same spot for clients that don't render HTML.
    marker = "{{ADD_TO_CALENDAR}}"
    button_html = _gcal_button(gcal_url) if gcal_url else ""
    link_line = f"\U0001F4C5 Add to Google Calendar: {gcal_url}" if gcal_url else ""
    inline = bool(gcal_url) and marker in body
    if inline:
        text_body = body.replace(marker, link_line)
        body_html = _sig_text_to_html(body).replace(marker, button_html)
        trailing_button = ""
    else:
        text_body = body + (f"\n\n{link_line}" if gcal_url else "")
        body_html = _sig_text_to_html(body)
        trailing_button = button_html
    has_html = bool(sig_html or button_html)
    full_html = body_html + trailing_button + (("<br><br>" + sig_html) if sig_html else "")

    if ics:
        # Native-card path: text/plain + text/html + text/calendar as
        # alternatives, wrapped in multipart/mixed with the .ics attachment.
        alt = MIMEMultipart("alternative")
        alt.attach(MIMEText(text_body, "plain", "utf-8"))
        if has_html:
            alt.attach(MIMEText(full_html, "html", "utf-8"))
        cal = MIMEText(ics, "calendar", "utf-8")
        cal.set_param("method", ics_method)
        alt.attach(cal)
        msg = MIMEMultipart("mixed")
        msg.attach(alt)
        from email.mime.base import MIMEBase
        from email import encoders
        att = MIMEBase("application", "ics")
        att.set_payload(ics.encode("utf-8"))
        encoders.encode_base64(att)
        att.add_header("Content-Disposition", "attachment", filename="invite.ics")
        msg.attach(att)
    elif has_html:
        msg = MIMEMultipart("alternative")
        # Declare UTF-8 on every part, else em-dashes / curly quotes / arrows
        # render as mojibake (e.g. "—" -> "â€"") in the recipient's client.
        msg.attach(MIMEText(text_body, "plain", "utf-8"))
        msg.attach(MIMEText(full_html, "html", "utf-8"))
    else:
        msg = MIMEText(text_body, "plain", "utf-8")
    msg["to"] = to
    if cc:
        msg["cc"] = cc
    # Encode the subject too, so a non-ASCII subject isn't garbled in the header.
    msg["subject"] = Header(subject, "utf-8")
    return msg


def _ics_from_args(a, to):
    """Build an ICS invitation from --cal-* args (native Gmail card + .ics).
    Returns (ics_text, method), or (None, 'PUBLISH') if --cal-title is absent."""
    if not getattr(a, "cal_title", None):
        return None, "PUBLISH"
    method = (getattr(a, "cal_method", None) or "PUBLISH").upper()
    ics = _ics(
        a.cal_title, a.cal_start, a.cal_end,
        all_day=not getattr(a, "cal_timed", False),
        location=getattr(a, "cal_location", "") or "",
        details=getattr(a, "cal_details", "") or "",
        organizer_email=getattr(a, "cal_organizer", None) or logged_in_email(),
        attendee_email=to if method == "REQUEST" else "",
        uid=getattr(a, "cal_uid", None),
        method=method,
    )
    return ics, method


def cmd_email_draft(a):
    body = Path(a.body_file).read_text(encoding="utf-8") if a.body_file else a.body
    ics, method = _ics_from_args(a, a.to)
    msg = _build_message(a.to, a.subject, body, cc=a.cc,
                         with_signature=not getattr(a, "no_signature", False),
                         gcal_url=getattr(a, "gcal_url", None),
                         ics=ics, ics_method=method)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    draft = svc("gmail", "v1").users().drafts().create(
        userId="me", body={"message": {"raw": raw}}
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
    body = Path(a.body_file).read_text(encoding="utf-8") if a.body_file else a.body
    ics, method = _ics_from_args(a, to)
    msg = _build_message(to, subject, body, cc=cc,
                         with_signature=not getattr(a, "no_signature", False),
                         gcal_url=getattr(a, "gcal_url", None),
                         ics=ics, ics_method=method)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    g.users().drafts().update(
        userId="me", id=a.draft_id, body={"message": {"raw": raw}}
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
    # charset MUST be declared or Drive's HTML import guesses the encoding and
    # mangles multibyte UTF-8 (em dash, arrows, ×) into mojibake.
    return f'<html><head><meta charset="utf-8"></head><body>{html}</body></html>'


def cmd_doc_create(a):
    _, _, _, _, MediaInMemoryUpload = _google()
    # read_text() defaults to the platform encoding (cp1252 on Windows) and
    # silently corrupts UTF-8 files — force utf-8 on both read and upload.
    src = Path(a.body_file).read_text(encoding="utf-8") if a.body_file else a.body
    html = _md_to_html(src)
    meta = {"name": a.title, "mimeType": "application/vnd.google-apps.document"}
    folder = a.folder or load_map().get("Docs")
    if folder:
        meta["parents"] = [folder]
    media = MediaInMemoryUpload(html.encode("utf-8"),
                                mimetype="text/html; charset=utf-8", resumable=False)
    doc = svc("drive", "v3").files().create(
        body=meta, media_body=media, fields="id,webViewLink", supportsAllDrives=True
    ).execute()
    print(f"Doc created: {doc.get('webViewLink')}")


def cmd_slides_create(a):
    """Build a Google Slides deck from a spec: {title, slides:[{title, body}]}.
    Each slide uses the TITLE_AND_BODY layout; body lines become the body text.
    Returns the presentation link. Placeholders (e.g. [metric 1]) are kept as-is."""
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    slides = svc("slides", "v1")
    pres = slides.presentations().create(body={"title": spec.get("title", a.title or "Deck")}).execute()
    pid = pres["presentationId"]
    default_slide = pres["slides"][0]["objectId"]

    create_reqs = []
    for i, s in enumerate(spec.get("slides", [])):
        sid = f"slide{i:02d}"
        create_reqs.append({"createSlide": {
            "objectId": sid,
            "slideLayoutReference": {"predefinedLayout": "TITLE_AND_BODY"},
            "placeholderIdMappings": [
                {"layoutPlaceholder": {"type": "TITLE", "index": 0}, "objectId": f"{sid}_t"},
                {"layoutPlaceholder": {"type": "BODY", "index": 0}, "objectId": f"{sid}_b"},
            ],
        }})
    if create_reqs:
        slides.presentations().batchUpdate(presentationId=pid, body={"requests": create_reqs}).execute()

    text_reqs = []
    for i, s in enumerate(spec.get("slides", [])):
        sid = f"slide{i:02d}"
        if s.get("title"):
            text_reqs.append({"insertText": {"objectId": f"{sid}_t", "text": s["title"]}})
        if s.get("body"):
            text_reqs.append({"insertText": {"objectId": f"{sid}_b", "text": s["body"]}})
    text_reqs.append({"deleteObject": {"objectId": default_slide}})  # drop the blank starter slide
    slides.presentations().batchUpdate(presentationId=pid, body={"requests": text_reqs}).execute()

    folder = a.folder or load_map().get("Decks")
    if folder:
        try:
            svc("drive", "v3").files().update(
                fileId=pid, addParents=folder, fields="id", supportsAllDrives=True).execute()
        except Exception as e:  # noqa: BLE001 — best-effort placement
            print(f"  (could not move to Decks folder: {e})")
    print(f"Slides created: https://docs.google.com/presentation/d/{pid}/edit")


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


def cmd_cal_find(a):
    """Find events on a calendar (by keyword / time window) and print their
    eventId + iCalUID — the two handles you need to add guests to an existing
    invite and to tie an email's Accept card to it."""
    cal = svc("calendar", "v3")
    kwargs = {"calendarId": a.calendar, "singleEvents": True,
              "orderBy": "startTime", "maxResults": a.max}
    if a.query:
        kwargs["q"] = a.query
    kwargs["timeMin"] = a.after or _now_rfc3339()
    res = cal.events().list(**kwargs).execute()
    items = res.get("items", [])
    if not items:
        print("(no matching events)")
        return
    print("eventId\tiCalUID\tstart\tsummary")
    for ev in items:
        start = ev.get("start", {}).get("date") or ev.get("start", {}).get("dateTime", "")
        print(f'{ev["id"]}\t{ev.get("iCalUID", "")}\t{start}\t{ev.get("summary", "")}')


def cmd_cal_add_guests(a):
    """Add guests to an EXISTING event's guest list. --notify off by default so
    Google stays silent and we can send our own designed invite instead; the
    guest is still on the list, so tapping Accept in our email flips them to
    'Going' on your master event. Prints the iCalUID for the email's card."""
    cal = svc("calendar", "v3")
    ev = cal.events().get(calendarId=a.calendar, eventId=a.event).execute()
    attendees = ev.get("attendees", []) or []
    have = {x.get("email", "").lower() for x in attendees}
    added = []
    for e in [x.strip() for x in a.emails.split(",") if x.strip()]:
        if e.lower() not in have:
            attendees.append({"email": e})
            added.append(e)
    send = "all" if a.notify else "none"
    updated = cal.events().patch(
        calendarId=a.calendar, eventId=a.event,
        body={"attendees": attendees}, sendUpdates=send,
    ).execute()
    how = "Google emailed them the invite" if a.notify else "silent (send your own email)"
    print(f"Added {len(added)} new guest(s); {how}. "
          f"Guest list now: {len(updated.get('attendees', []))}.")
    print(f"iCalUID (use as --cal-uid): {updated.get('iCalUID', '')}")
    print(f"organizer (use as --cal-organizer): {updated.get('organizer', {}).get('email', '')}")


def cmd_cal_remove_guests(a):
    """Remove guests from an existing event's guest list (e.g. clean up test
    addresses). --notify off by default so removal is silent."""
    cal = svc("calendar", "v3")
    ev = cal.events().get(calendarId=a.calendar, eventId=a.event).execute()
    drop = {x.strip().lower() for x in a.emails.split(",") if x.strip()}
    attendees = ev.get("attendees", []) or []
    kept = [x for x in attendees if x.get("email", "").lower() not in drop]
    removed = len(attendees) - len(kept)
    send = "all" if a.notify else "none"
    updated = cal.events().patch(
        calendarId=a.calendar, eventId=a.event,
        body={"attendees": kept}, sendUpdates=send,
    ).execute()
    print(f"Removed {removed} guest(s). Guest list now: {len(updated.get('attendees', []))}.")


def _now_rfc3339():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cmd_gcal_link(a):
    """Print a Google Calendar 'add event' URL — paste into --gcal-url on
    email-draft/draft-update to embed an 'Add to Google Calendar' button."""
    url = _gcal_url(a.title, a.start, a.end, all_day=not a.timed,
                    location=a.location or "", details=a.details or "")
    print(url)


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
def _add_cal_args(parser):
    """Attach --cal-* flags: when --cal-title is given, the email carries an
    embedded calendar invitation so Gmail shows its native event card (and an
    .ics is attached for Apple/Outlook)."""
    parser.add_argument("--cal-title", help="event title → embeds a native calendar card")
    parser.add_argument("--cal-start", help="YYYY-MM-DD (all-day) or YYYY-MM-DDTHH:MM:SS")
    parser.add_argument("--cal-end", help="YYYY-MM-DD inclusive (all-day) or ISO datetime")
    parser.add_argument("--cal-location")
    parser.add_argument("--cal-details")
    parser.add_argument("--cal-timed", action="store_true",
                        help="treat start/end as datetimes (Asia/Kolkata), not all-day")
    parser.add_argument("--cal-method", choices=["PUBLISH", "REQUEST"], default="PUBLISH",
                        help="PUBLISH = Add-to-Calendar card (default, no RSVP); "
                             "REQUEST = Yes/Maybe/No invite (RSVPs go to organizer)")
    parser.add_argument("--cal-uid",
                        help="tie the card to an EXISTING event (its iCalUID, from cal-add-guests) "
                             "so Accept updates that master event, not a copy")
    parser.add_argument("--cal-organizer",
                        help="organizer email of the existing event (e.g. social@shikshalokam.org); "
                             "RSVPs flow here")


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
    d.add_argument("--no-signature", action="store_true",
                   help="skip the team signature (attached by default)")
    d.add_argument("--gcal-url",
                   help="embed an 'Add to Google Calendar' button linking to this URL "
                        "(build one with:  gs.py gcal-link ...)")
    _add_cal_args(d)
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
    du.add_argument("--no-signature", action="store_true",
                    help="skip the team signature (attached by default)")
    du.add_argument("--gcal-url",
                    help="embed an 'Add to Google Calendar' button linking to this URL")
    _add_cal_args(du)
    du.set_defaults(fn=cmd_draft_update)

    dr = sub.add_parser("draft-read",
                        help="read a draft's subject+body (or list drafts) to learn from edits")
    dr.add_argument("draft_id", nargs="?",
                    help="draft id to read; omit to list drafts (id<TAB>subject)")
    dr.add_argument("--max", type=int, default=30)
    dr.set_defaults(fn=cmd_draft_read)

    sc = sub.add_parser("slides-create", help="make a Google Slides deck from a JSON spec")
    sc.add_argument("--spec", required=True, help="path to {title, slides:[{title,body}]} JSON")
    sc.add_argument("--title")
    sc.add_argument("--folder", help="Drive folder id (defaults to the Decks folder)")
    sc.set_defaults(fn=cmd_slides_create)

    dc = sub.add_parser("doc-create", help="make a Google Doc from text/markdown")
    dc.add_argument("--title", required=True)
    dc.add_argument("--body")
    dc.add_argument("--body-file")
    dc.add_argument("--folder", help="folder id (default: Docs from drive_map.json)")
    dc.set_defaults(fn=cmd_doc_create)

    df = sub.add_parser("drive-folder", help="create a Drive folder")
    df.add_argument("--name", required=True)
    df.add_argument("--parent")
    df.set_defaults(fn=cmd_drive_folder)

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

    cf = sub.add_parser("cal-find", help="find events + their eventId/iCalUID on a calendar")
    cf.add_argument("--calendar", default="primary", help="calendar id (default: primary)")
    cf.add_argument("--query", help="keyword to match in the event")
    cf.add_argument("--after", help="RFC3339 lower bound (default: now)")
    cf.add_argument("--max", type=int, default=20)
    cf.set_defaults(fn=cmd_cal_find)

    ag = sub.add_parser("cal-add-guests", help="add guests to an existing event's guest list")
    ag.add_argument("--event", required=True, help="eventId (from cal-find)")
    ag.add_argument("--emails", required=True, help="comma-separated guest emails")
    ag.add_argument("--calendar", default="primary", help="calendar id (default: primary)")
    ag.add_argument("--notify", action="store_true",
                    help="let Google email them the official invite (default: silent)")
    ag.set_defaults(fn=cmd_cal_add_guests)

    rg = sub.add_parser("cal-remove-guests", help="remove guests from an existing event")
    rg.add_argument("--event", required=True, help="eventId (from cal-find)")
    rg.add_argument("--emails", required=True, help="comma-separated guest emails to remove")
    rg.add_argument("--calendar", default="primary", help="calendar id (default: primary)")
    rg.add_argument("--notify", action="store_true",
                    help="let Google email the removal (default: silent)")
    rg.set_defaults(fn=cmd_cal_remove_guests)

    gl = sub.add_parser("gcal-link",
                        help="build a Google Calendar 'add event' URL (for email --gcal-url)")
    gl.add_argument("--title", required=True)
    gl.add_argument("--start", required=True, help="YYYY-MM-DD (all-day) or YYYY-MM-DDTHH:MM:SS")
    gl.add_argument("--end", required=True, help="YYYY-MM-DD (inclusive) or ISO datetime")
    gl.add_argument("--timed", action="store_true", help="treat start/end as datetimes, not all-day")
    gl.add_argument("--location")
    gl.add_argument("--details")
    gl.set_defaults(fn=cmd_gcal_link)

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
