#!/usr/bin/env python3
"""Regenerate the 2 grouped Google Docs IN PLACE from page.md (links stay stable):
   - 'MItra Webinar — Emails'   (all emails)
   - 'MItra Webinar — Messages' (WhatsApp + LinkedIn + poster + clip script)
Updates content of the existing fileIds; does not create new docs."""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools" / "gsuite"))
import gs
from googleapiclient.http import MediaInMemoryUpload

EMAILS_ID = "1CKURznd2GU2fDJ4s-qeh2wn_4bvIbtFnFljuubRoPXw"
MESSAGES_ID = "1nkJb1dkf_77T30cRHdlKQziGIxE_Alohr21HYkhQuVM"

drive = gs.svc("drive", "v3")

page = (gs.REPO / "projects" / "mitra-webinar" / "page.md").read_text(encoding="utf-8")
lib = page.split("## Asset library", 1)[1]
blocks = [b for b in ("\n" + lib).split("\n### ") if b.strip() and b.lstrip().startswith("Day ")]

def title_of(b):
    return b.splitlines()[0].split(" · status")[0].strip().replace("`", "")

emails = [b for b in blocks if "Email" in title_of(b)]
non_email = [b for b in blocks if "Email" not in title_of(b)]

def grp(b):
    t = title_of(b)
    if "WhatsApp" in t: return 0
    if "LinkedIn" in t: return 1
    if "Blog Part 2" in t: return 2
    if "Poster" in t: return 3
    if "Demo teaser clip" in t: return 4
    return 5  # anything else (e.g. Q&A) lands at the end — nothing dropped
messages = sorted(non_email, key=grp)  # each asset classified once; stable order

def inline(s):
    s = s.replace("`", "")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"<i>\1</i>", s)
    return s

def md_html(md):
    lines = md.splitlines(); html = []; i = 0
    while i < len(lines):
        s = lines[i].rstrip()
        if s.startswith("|") and i + 1 < len(lines) and set(lines[i+1].strip()) <= set("|-: "):
            hdr = [c.strip() for c in s.strip().strip("|").split("|")]; i += 2; rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            t = "<table border='1' cellpadding='4'><tr>" + "".join(f"<th>{inline(h)}</th>" for h in hdr) + "</tr>"
            for r in rows:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
            html.append(t + "</table>"); continue
        if not s.strip(): i += 1; continue
        if s.startswith("### "): html.append(f"<h2>{inline(s[4:])}</h2>")
        elif s.startswith("> "): html.append(f"<p>{inline(s[2:])}</p>")
        elif s.strip() == ">": pass
        elif s.startswith("- "): html.append(f"<ul><li>{inline(s[2:])}</li></ul>")
        else: html.append(f"<p>{inline(s)}</p>")
        i += 1
    return "\n".join(html)

def build(group):
    parts = []
    for b in group:
        parts.append(f"<h1>{inline(title_of(b))}</h1>")
        parts.append(md_html("\n".join(b.splitlines()[1:])))
    return "<html><body>" + "\n".join(parts) + "</body></html>"

def update(fid, group, label):
    html = build(group).encode("utf-8")
    media = MediaInMemoryUpload(html, mimetype="text/html", resumable=False)
    doc = drive.files().update(fileId=fid, media_body=media,
                               fields="id,webViewLink", supportsAllDrives=True).execute()
    print(f"{label} ({len(group)} assets): {doc.get('webViewLink')}")

update(EMAILS_ID, emails, "Emails")
update(MESSAGES_ID, messages, "Messages")
