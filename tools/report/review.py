#!/usr/bin/env python3
"""Serve the report's review page and auto-save comments to a file.

    python tools/report/review.py tools/report/asc-3-0.json

Opens http://localhost:8765 . Hover anything in the report, click the ●, type.
Every comment is written straight to

    tools/report/out/<slug>-comments.json

so there is no export step and nothing to hand over — the brain reads that file
and applies the changes. Ctrl-C to stop; comments stay in the file.
"""
import json
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import build_report as br

PORT = 8765


def load_doc(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class Handler(BaseHTTPRequestHandler):
    doc_path = None
    slug = None

    @property
    def comments_file(self):
        return br.OUT / f"{self.slug}-comments.json"

    def _send(self, code, body, ctype):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/") or "/"
        if path == "/":
            # rebuilt per request, so editing the content JSON only needs a refresh
            doc = load_doc(self.doc_path)
            self._send(200, br.build_review_html(doc), "text/html; charset=utf-8")
        elif path == "/comments":
            f = self.comments_file
            body = f.read_text(encoding="utf-8") if f.exists() else "{}"
            self._send(200, body, "application/json")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        if self.path.split("?")[0].rstrip("/") != "/comments":
            self._send(404, "not found", "text/plain")
            return
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n).decode("utf-8") or "{}"
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            self._send(400, '{"error":"bad json"}', "application/json")
            return
        self.comments_file.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
        total = sum(len(v) for v in data.values())
        print(f"  saved {total} comment(s) -> {self.comments_file}")
        self._send(200, '{"ok":true}', "application/json")

    def log_message(self, *a):  # keep the console to just the save lines
        pass


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: review.py <content.json>")
    doc_path = str(Path(sys.argv[1]).resolve())
    Handler.doc_path = doc_path
    Handler.slug = load_doc(doc_path)["meta"]["slug"]

    srv = HTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://localhost:{PORT}/"
    print(f"Review page:  {url}")
    print(f"Comments  ->  {br.OUT / (Handler.slug + '-comments.json')}")
    print("Hover any element, click the round + button, type. Saves as you go. Ctrl-C to stop.")
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped - comments kept in the file above.")


if __name__ == "__main__":
    main()
