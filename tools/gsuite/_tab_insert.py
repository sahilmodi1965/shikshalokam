#!/usr/bin/env python3
"""One-off: insert Nagaland Variant B into an existing tab of a Google Doc."""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gs  # reuse auth + service builders

DOC_ID = "1NDr1e1JbSpQnFYQ4qoiuJ4BR1BuwgwE2VyZysyjQF0U"
TAB_TITLE = "tab 3"

# ---- pull Variant B body out of page.md ------------------------------------
page = (gs.REPO / "projects" / "invoked-nagaland-nlf" / "page.md").read_text(encoding="utf-8")
chunk = page.split("## Draft B — The Land of Festivals", 1)[1]
# start at the title line, drop the meta italic descriptor
start = chunk.index("**Continuous Acts of Miracles in the Hills**")
body_md = chunk[start:].strip()

# ---- parse markdown into blocks + inline runs ------------------------------
def parse_inline(text):
    """Return (clean_text, runs) where runs = [(start,end,'bold'|'italic')]."""
    out, runs = [], []
    for tok in re.split(r'(\*\*.+?\*\*|\*[^*]+?\*)', text):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            s = len("".join(out)); inner = tok[2:-2]
            out.append(inner); runs.append((s, s+len(inner), "bold"))
        elif tok.startswith("*") and tok.endswith("*"):
            s = len("".join(out)); inner = tok[1:-1]
            out.append(inner); runs.append((s, s+len(inner), "italic"))
        else:
            out.append(tok)
    return "".join(out), runs

blocks = []  # (style, clean_text, runs)
first_title = False
for raw in body_md.splitlines():
    line = raw.strip()
    if not line:
        continue
    if line.startswith("### "):
        blocks.append(("HEADING_2", line[4:].strip(), []))
    elif not first_title and line.startswith("**") and line.endswith("**"):
        blocks.append(("TITLE", line[2:-2].strip(), []))
        first_title = True
    else:
        clean, runs = parse_inline(line)
        blocks.append(("NORMAL_TEXT", clean, runs))

# ---- locate the tab --------------------------------------------------------
docs = gs.svc("docs", "v1")
doc = docs.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()

def walk(tabs):
    for t in tabs or []:
        yield t
        yield from walk(t.get("childTabs"))

target = None
titles = []
for t in walk(doc.get("tabs")):
    title = t.get("tabProperties", {}).get("title", "")
    titles.append(title)
    if title.strip().lower() == TAB_TITLE.lower():
        target = t
if not target:
    sys.exit(f"Tab '{TAB_TITLE}' not found. Tabs present: {titles}")

tab_id = target["tabProperties"]["tabId"]
content = target["documentTab"]["body"]["content"]
end_index = max(c["endIndex"] for c in content if "endIndex" in c)
insert_at = end_index - 1  # before the body's final newline
print(f"Tab '{TAB_TITLE}' id={tab_id}; body end={end_index}; inserting at {insert_at}")

# ---- build text + style requests -------------------------------------------
full = []
style_reqs = []
cursor = insert_at
for style, text, runs in blocks:
    block_start = cursor
    full.append(text + "\n")
    if style in ("TITLE", "HEADING_2"):
        style_reqs.append({"updateParagraphStyle": {
            "range": {"tabId": tab_id, "startIndex": block_start,
                      "endIndex": block_start + len(text) + 1},
            "paragraphStyle": {"namedStyleType": style},
            "fields": "namedStyleType"}})
    for (rs, re_, kind) in runs:
        style_reqs.append({"updateTextStyle": {
            "range": {"tabId": tab_id, "startIndex": block_start + rs,
                      "endIndex": block_start + re_},
            "textStyle": {"bold": True} if kind == "bold" else {"italic": True},
            "fields": kind}})
    cursor += len(text) + 1

text_blob = "".join(full)
requests = [{"insertText": {
    "location": {"tabId": tab_id, "index": insert_at},
    "text": text_blob}}] + style_reqs

docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()
print(f"Inserted {len(blocks)} blocks ({len(text_blob)} chars), {len(style_reqs)} style ops.")
print(f"Open: https://docs.google.com/document/d/{DOC_ID}/edit?tab={tab_id}")
