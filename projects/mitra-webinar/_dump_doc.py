#!/usr/bin/env python3
"""Dump tab structure + text of the campaign docs so we can see the current
arrangement and any hand edits."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools" / "gsuite"))
import gs

DOCS = {
    "Emails (1CKUR…)": "1CKURznd2GU2fDJ4s-qeh2wn_4bvIbtFnFljuubRoPXw",
    "Messages (1nkJb…)": "1nkJb1dkf_77T30cRHdlKQziGIxE_Alohr21HYkhQuVM",
}
docs = gs.svc("docs", "v1")

def elements_text(content):
    out = []
    for el in content:
        if "paragraph" in el:
            line = "".join(r.get("textRun", {}).get("content", "")
                           for r in el["paragraph"].get("elements", []))
            if line.strip():
                out.append(line.rstrip("\n"))
        elif "table" in el:
            for row in el["table"].get("tableRows", []):
                cells = [elements_text(c.get("content", [])).replace("\n", " ⏎ ")
                         for c in row.get("tableCells", [])]
                out.append("   ┃ " + " | ".join(cells))
    return "\n".join(out)

def text_of(body):
    return elements_text(body.get("content", []))

def walk(tabs, depth=0):
    for t in tabs or []:
        title = t.get("tabProperties", {}).get("title", "?")
        print(f"{'  '*depth}— TAB: {title}")
        body = t.get("documentTab", {}).get("body", {})
        txt = text_of(body)
        for ln in txt.splitlines():
            print(f"{'  '*depth}    {ln}")
        walk(t.get("childTabs"), depth + 1)

for label, did in DOCS.items():
    print("\n" + "=" * 70 + f"\n{label}\n" + "=" * 70)
    try:
        d = docs.documents().get(documentId=did, includeTabsContent=True).execute()
        if d.get("tabs"):
            walk(d["tabs"])
        else:
            print(text_of(d.get("body", {})))
    except Exception as e:
        print(f"  (couldn't read: {e})")
