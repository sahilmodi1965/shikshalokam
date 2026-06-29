#!/usr/bin/env python3
"""Trash the 4 single-asset Day-1 Docs and replace with 2 grouped Google Docs:
   - 'MItra Webinar — Emails'   (all emails)
   - 'MItra Webinar — Messages' (WhatsApp + LinkedIn + poster + clip script)
Rebuilt from page.md each run."""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools" / "gsuite"))
import gs
from googleapiclient.http import MediaInMemoryUpload

FOLDER = "1rjYIErAuZdpCoML5WAz4LFKD9hWY-05h"
OLD_DOCS = [
    "19p3Eut-RiO3CEA72x6MYcv9Wzy0NE_eiuUAeFF1YIXw",  # Email 1
    "1BCOyraeBtu7vMCxpvSzJuxvT8gZ16AbTV0XQO06lD3s",  # Poster
    "141OHdiMZoVAJegHhF7-pFndx5nDk8k7Of3_OLyw04Nw",  # WhatsApp 1:1
    "1dUeQ7Jbcp99VjwcBCpoIIQtvXoW1n4sW8HnybXXVpDg",  # WhatsApp broadcast
]

drive = gs.svc("drive", "v3")

# 1) trash old docs
for fid in OLD_DOCS:
    try:
        drive.files().update(fileId=fid, body={"trashed": True}, supportsAllDrives=True).execute()
        print(f"trashed {fid}")
    except Exception as e:
        print(f"  (couldn't trash {fid}: {e})")

# 2) parse asset blocks
page = (gs.REPO / "projects" / "mitra-webinar" / "page.md").read_text(encoding="utf-8")
lib = page.split("## Asset library", 1)[1]
blocks = [b for b in ("\n" + lib).split("\n### ") if b.strip() and b.lstrip().startswith("Day ")]

def title_of(b):
    return b.splitlines()[0].split(" · status")[0].strip().replace("`", "")

emails = [b for b in blocks if "Email" in title_of(b)]
whatsapp = [b for b in blocks if "WhatsApp" in title_of(b)]
linkedin = [b for b in blocks if "LinkedIn" in title_of(b)]
poster = [b for b in blocks if "Poster" in title_of(b)]
clip = [b for b in blocks if "Demo teaser clip" in title_of(b)]
messages = whatsapp + linkedin + poster + clip

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
        lines = b.splitlines()
        parts.append(f"<h1>{inline(title_of(b))}</h1>")
        parts.append(md_html("\n".join(lines[1:])))
    return "<html><body>" + "\n".join(parts) + "</body></html>"

def make(title, group):
    html = build(group)
    media = MediaInMemoryUpload(html.encode("utf-8"), mimetype="text/html", resumable=False)
    doc = drive.files().create(
        body={"name": title, "mimeType": "application/vnd.google-apps.document", "parents": [FOLDER]},
        media_body=media, fields="id,webViewLink", supportsAllDrives=True).execute()
    print(f"{title}: {doc.get('webViewLink')}")

make("MItra Webinar — Emails", emails)
make("MItra Webinar — Messages", messages)
