#!/usr/bin/env python3
"""Consolidate the MItra webinar copy into ONE Google Doc with two tabs:
   📧 Emails  and  💬 WhatsApp — rebuilt from page.md each run.
The Emails doc is retired to a one-line pointer so there's a single source.
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools" / "gsuite"))
import gs
from googleapiclient.http import MediaInMemoryUpload

DOC_ID = "1nkJb1dkf_77T30cRHdlKQziGIxE_Alohr21HYkhQuVM"      # the single consolidated doc
OLD_EMAILS_ID = "1CKURznd2GU2fDJ4s-qeh2wn_4bvIbtFnFljuubRoPXw"  # retired -> pointer

docs = gs.svc("docs", "v1")
drive = gs.svc("drive", "v3")

import time
from googleapiclient.errors import HttpError

def bu(requests):
    """batchUpdate with a small retry on transient 5xx."""
    for attempt in range(4):
        try:
            return docs.documents().batchUpdate(
                documentId=DOC_ID, body={"requests": requests}).execute()
        except HttpError as e:
            if e.resp.status >= 500 and attempt < 3:
                time.sleep(1.5 * (attempt + 1)); continue
            raise

# --- read page.md asset blocks -------------------------------------------------
page = (gs.REPO / "projects" / "mitra-webinar" / "page.md").read_text(encoding="utf-8")
lib = page.split("## Asset library", 1)[1].split("## Superseded", 1)[0]
blocks = [b for b in ("\n" + lib).split("\n### ") if b.strip() and b.lstrip().startswith("Day ")]

def title_of(b):
    return b.splitlines()[0].split(" · status")[0].strip().replace("`", "")

def to_text(b):
    lines = b.splitlines()
    out = [title_of(b), ""]
    for ln in lines[1:]:
        s = ln.rstrip()
        if not s.strip():
            out.append("")
            continue
        s = s.lstrip()
        if s.startswith("> "):
            s = s[2:]
        elif s == ">":
            s = ""
        s = s.replace("**", "").replace("`", "")
        s = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"\1", s)   # *italic* -> italic
        out.append(s)
    txt = "\n".join(out)
    txt = re.sub(r"\n{3,}", "\n\n", txt).strip()
    return txt

SEP = "\n\n————————————————————————\n\n"
emails = SEP.join(to_text(b) for b in blocks if "Email" in title_of(b))
whats  = SEP.join(to_text(b) for b in blocks if "WhatsApp" in title_of(b))

# Inject the live Meet link into the (private) Drive doc only — it is kept OUT of
# page.md (which renders to the public site) via the {{MEET_LINK}} placeholder.
_meet = Path.home() / ".shikshalokam" / "mitra_meet_link.txt"
if _meet.exists():
    link = _meet.read_text(encoding="utf-8").strip()
    emails = emails.replace("{{MEET_LINK}}", link)
    whats = whats.replace("{{MEET_LINK}}", link)

# --- rebuild to exactly two tabs, WITHOUT renaming (rename 500s server-side) ---
# Reuse a tab of the wanted title if it exists (clear + refill); create it if not;
# then delete any leftover tabs. addDocumentTab + deleteTab + insert/delete content
# all work; only updateDocumentTabProperties (rename) is broken, so we avoid it.
WANT = [("Emails", "📧", emails), ("WhatsApp", "💬", whats)]

def snapshot():
    d = docs.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()
    out = {}
    for t in d.get("tabs", []):
        tid = t["tabProperties"]["tabId"]
        title = t["tabProperties"].get("title", "")
        end = t["documentTab"]["body"]["content"][-1]["endIndex"]
        out[tid] = {"title": title, "end": end}
    return out

def ensure(title, icon, text):
    tabs = snapshot()
    tid = next((k for k, v in tabs.items() if v["title"] == title), None)
    if tid is None:
        res = bu([{"addDocumentTab": {"tabProperties": {"title": title, "iconEmoji": icon}}}])
        tid = res["replies"][0]["addDocumentTab"]["tabProperties"]["tabId"]
        tabs = snapshot()
    end = tabs.get(tid, {}).get("end", 2)
    if end > 2:  # clear existing body (keep the final newline the API won't delete)
        bu([{"deleteContentRange": {"range": {"tabId": tid, "startIndex": 1, "endIndex": end - 1}}}])
    bu([{"insertText": {"location": {"tabId": tid, "index": 1}, "text": text}}])
    print(f"  tab '{title}' -> {tid}")
    return tid

keep = {ensure(*w) for w in WANT}
for tid in list(snapshot()):        # drop anything that isn't one of our two tabs
    if tid not in keep:
        bu([{"deleteTab": {"tabId": tid}}])
        print(f"  deleted stray tab {tid}")
print("rebuilt: Emails + WhatsApp tabs")

# 4) name the consolidated doc clearly
drive.files().update(fileId=DOC_ID, body={"name": "MItra Webinar — Copy (Emails + WhatsApp)"},
                     supportsAllDrives=True).execute()

# 5) retire the old Emails doc to a single pointer line
pointer = ("<html><body><p>Moved. All MItra webinar copy now lives in one doc — "
           "<b>MItra Webinar — Copy (Emails + WhatsApp)</b> — in the 📧 Emails and 💬 WhatsApp tabs:</p>"
           f"<p>https://docs.google.com/document/d/{DOC_ID}/edit</p></body></html>").encode("utf-8")
drive.files().update(fileId=OLD_EMAILS_ID,
                     media_body=MediaInMemoryUpload(pointer, mimetype="text/html"),
                     supportsAllDrives=True).execute()

print("done: https://docs.google.com/document/d/%s/edit" % DOC_ID)
