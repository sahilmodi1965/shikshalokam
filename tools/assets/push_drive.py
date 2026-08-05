#!/usr/bin/env python3
"""push_drive.py — upload generated assets (PNG/PDF/…) to a Drive folder,
as the logged-in teammate, reusing the gs.py auth. No Google-Doc conversion —
files land as real binaries.

Usage:
    python tools/assets/push_drive.py <file-or-dir> [more...] --folder <PARENT_ID> [--subfolder NAME]
"""
import argparse, mimetypes, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "gsuite"))
import gs
from googleapiclient.http import MediaFileUpload

def gather(paths):
    files = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            files += [f for f in sorted(p.iterdir())
                      if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".pdf", ".gif")]
        elif p.exists():
            files.append(p)
    return files

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--folder", required=True, help="Drive parent folder id")
    ap.add_argument("--subfolder", help="create/use this subfolder under parent")
    a = ap.parse_args()
    drive = gs.svc("drive", "v3")
    parent = a.folder
    if a.subfolder:
        q = (f"mimeType='application/vnd.google-apps.folder' and trashed=false "
             f"and name='{a.subfolder}' and '{parent}' in parents")
        hit = drive.files().list(q=q, fields="files(id)", supportsAllDrives=True,
                                 includeItemsFromAllDrives=True).execute().get("files", [])
        if hit:
            parent = hit[0]["id"]
        else:
            f = drive.files().create(
                body={"name": a.subfolder, "mimeType": "application/vnd.google-apps.folder",
                      "parents": [parent]}, fields="id,webViewLink", supportsAllDrives=True).execute()
            parent = f["id"]
            print(f"subfolder '{a.subfolder}': {f.get('webViewLink')}")
    for f in gather(a.paths):
        mime = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
        media = MediaFileUpload(str(f), mimetype=mime, resumable=False)
        q = f"name='{f.name}' and '{parent}' in parents and trashed=false"
        hit = drive.files().list(q=q, fields="files(id)", supportsAllDrives=True,
                                 includeItemsFromAllDrives=True).execute().get("files", [])
        if hit:
            doc = drive.files().update(fileId=hit[0]["id"], media_body=media,
                                       fields="id,webViewLink", supportsAllDrives=True).execute()
            verb = "updated"
        else:
            doc = drive.files().create(body={"name": f.name, "parents": [parent]},
                                       media_body=media, fields="id,webViewLink",
                                       supportsAllDrives=True).execute()
            verb = "added  "
        print(f"  {verb} {f.name}  ->  {doc.get('webViewLink')}")

if __name__ == "__main__":
    main()
