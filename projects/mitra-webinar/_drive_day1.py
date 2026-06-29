#!/usr/bin/env python3
"""Create 'MItra Webinar' under the 'pictures & resources' Drive folder and
upload the Day-1 assets as Google Docs. Search-first: won't create if the
parent folder is ambiguous. Searches My Drive + shared drives + shared-with-me."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools" / "gsuite"))
import gs
from googleapiclient.http import MediaInMemoryUpload

drive = gs.svc("drive", "v3")

def q_run(q):
    out = {}
    for params in (dict(corpora="user"),
                   dict(corpora="allDrives", includeItemsFromAllDrives=True)):
        try:
            res = drive.files().list(
                q=q, fields="files(id,name,owners(emailAddress))",
                pageSize=100, supportsAllDrives=True, **params).execute()
            for f in res.get("files", []):
                out[f["id"]] = f
        except Exception as e:
            print(f"  (query {params} failed: {e})")
    return list(out.values())

def folders(term):
    return q_run(f"mimeType='application/vnd.google-apps.folder' and trashed=false "
                 f"and name contains '{term}'")

# union of likely matches
cands = {f["id"]: f for f in folders("esource") + folders("icture") + folders("Pictures")}
cands = list(cands.values())
print("Candidate folders:")
for f in cands:
    own = (f.get("owners") or [{}])[0].get("emailAddress", "?")
    print(f"  - {f['name']}  (owner={own}, id={f['id']})")

def score(f):
    n = f["name"].lower()
    return ("resource" in n) + ("picture" in n or "pic" in n)

ranked = sorted(cands, key=score, reverse=True)
chosen = None
if ranked and score(ranked[0]) >= 1 and (len(ranked) == 1 or score(ranked[0]) > score(ranked[1])):
    chosen = ranked[0]

if not chosen:
    print("\nNo single clear match. Listing folders shared with you (to identify it):")
    for f in q_run("mimeType='application/vnd.google-apps.folder' and trashed=false and sharedWithMe=true"):
        print(f"  - {f['name']}  (id={f['id']})")
    print("\nNothing created. Send me the folder name or its link/ID and I'll use it directly.")
    sys.exit(0)

print(f"\nParent = '{chosen['name']}' (id={chosen['id']})")

sub = drive.files().create(
    body={"name": "MItra Webinar", "mimeType": "application/vnd.google-apps.folder",
          "parents": [chosen["id"]]},
    fields="id,webViewLink", supportsAllDrives=True).execute()
print(f"Created subfolder 'MItra Webinar': {sub.get('webViewLink')}  id={sub['id']}")

page = (gs.REPO / "projects" / "mitra-webinar" / "page.md").read_text(encoding="utf-8")
lib = page.split("## Asset library", 1)[1]
day1 = [b for b in ("\n" + lib).split("\n### ") if b.startswith("Day 1")]

def to_body(lines):
    out = []
    for ln in lines:
        if ln.strip() == ">": out.append("")
        elif ln.startswith("> "): out.append(ln[2:])
        else: out.append(ln)
    return "\n".join(out).replace("`", "")

for b in day1:
    lines = b.splitlines()
    title = "MItra — " + lines[0].split(" · status")[0].strip()
    html = gs._md_to_html(to_body(lines[1:]))
    media = MediaInMemoryUpload(html.encode(), mimetype="text/html", resumable=False)
    doc = drive.files().create(
        body={"name": title, "mimeType": "application/vnd.google-apps.document",
              "parents": [sub["id"]]},
        media_body=media, fields="id,webViewLink", supportsAllDrives=True).execute()
    print(f"  + {title}\n    {doc.get('webViewLink')}")
