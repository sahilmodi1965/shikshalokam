#!/usr/bin/env python3
"""Read a Google Doc that has TABS — list them, or dump one tab's text with indices.

gs.py can create Docs but can't read them, and a tabbed Doc (SM Captions 2026-27,
CTB Story Drafts) is invisible to a plain documents().get(). This fills that gap.

    python tools/gsuite/doc_tabs.py <docId>                  # list every tab + its tabId
    python tools/gsuite/doc_tabs.py <docId> <tabId>          # dump that tab's paragraphs

The dump prints `[startIndex-endIndex]` per paragraph — those are exactly the numbers a
batchUpdate deleteContentRange/insertText needs, so a caption can be rewritten in place.
Pattern for the edit (see also _tab_insert.py):

    reqs = [
        {"deleteContentRange": {"range": {"startIndex": s, "endIndex": e, "tabId": TAB}}},
        {"insertText": {"location": {"index": s, "tabId": TAB}, "text": NEW}},
    ]
    gs.svc("docs", "v1").documents().batchUpdate(documentId=DOC, body={"requests": reqs}).execute()

Locate the block by SEARCHING its text (not by hardcoded indices — the doc moves under you),
and set endIndex to the last paragraph's endIndex - 1 so its trailing newline survives.
A tabId always belongs in the range/location dict, or the edit lands on the wrong tab.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gs  # reuse auth + service builders


def walk(tabs):
    """Yield every tab, including nested childTabs."""
    for t in tabs or []:
        yield t
        yield from walk(t.get("childTabs"))


def fetch(doc_id):
    return gs.svc("docs", "v1").documents().get(
        documentId=doc_id, includeTabsContent=True
    ).execute()


def list_tabs(doc):
    print("TITLE:", doc.get("title"))

    def show(tabs, depth=0):
        for t in tabs or []:
            p = t.get("tabProperties", {})
            print(" " * depth, "TAB", p.get("tabId"), "|", p.get("title"))
            show(t.get("childTabs"), depth + 2)

    show(doc.get("tabs"))


def dump_tab(doc, tab_id):
    tab = next((t for t in walk(doc.get("tabs"))
                if t["tabProperties"]["tabId"] == tab_id), None)
    if not tab:
        sys.exit(f"tab {tab_id} not found — run without a tabId to list them")

    def render(content, indent=""):
        for el in content:
            if "paragraph" in el:
                p = el["paragraph"]
                style = p.get("paragraphStyle", {}).get("namedStyleType", "")
                txt = "".join(e.get("textRun", {}).get("content", "")
                              for e in p.get("elements", []))
                print(f"[{el.get('startIndex')}-{el.get('endIndex')}] "
                      f"{style[:12]:<12}| {indent}{txt.rstrip()}")
            elif "table" in el:
                print(f"[{el.get('startIndex')}-{el.get('endIndex')}] TABLE")
                for r, row in enumerate(el["table"]["tableRows"]):
                    for c, cell in enumerate(row["tableCells"]):
                        print(f"  --- row{r} col{c} ---")
                        render(cell["content"], indent + "    ")

    render(tab["documentTab"]["body"]["content"])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    document = fetch(sys.argv[1])
    if len(sys.argv) == 2:
        list_tabs(document)
    else:
        dump_tab(document, sys.argv[2])
