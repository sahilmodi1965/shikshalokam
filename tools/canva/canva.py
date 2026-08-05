#!/usr/bin/env python3
"""ShikshaLokam Canva engine — create designs in Canva from the brain.

Mirrors tools/gsuite/gs.py in spirit: OAuth once, then simple commands. Secrets
and tokens live OUTSIDE the repo in ~/.shikshalokam/. Standard library only —
no pip installs.

Commands
  login            one-time browser consent (OAuth 2.0 + PKCE)
  whoami           show the authed Canva user / team
  create-design    create a blank or custom-size design (optionally from an asset)
  upload-asset     upload an image file, return its asset id
  autofill         fill a Brand Template with data -> a design  (needs Canva Enterprise)
  export           export a design to png/pdf -> download url
  brand-templates  list brand templates you can autofill        (needs Canva Enterprise)

Setup: onboarding/canva-setup.md  (register a Connect app, then `login`).

NOTE (v1, 2026-07-03): built against the Canva Connect OpenAPI spec but NOT yet
run against a live app (needs client credentials first). Endpoint field shapes
(asset-upload job, export `format`) are validated on the first real call and
fixed there if Canva returns a shape hint.
"""
import argparse
import base64
import hashlib
import http.server
import json
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

HOME = Path.home() / ".shikshalokam"                 # OUTSIDE the repo (gitignored anyway)
CLIENT_PATH = HOME / "canva_client.json"             # {"client_id":..,"client_secret":..}
TOKEN_PATH = HOME / "canva_token.json"               # personal, never committed

API = "https://api.canva.com/rest"
AUTHORIZE_URL = "https://www.canva.com/api/oauth/authorize"
TOKEN_URL = f"{API}/v1/oauth/token"
REDIRECT_PORT = 8910
REDIRECT_URI = f"http://127.0.0.1:{REDIRECT_PORT}/callback"   # register this in the app

# Broad enough for the stated capabilities; keep in sync with onboarding/canva-setup.md.
SCOPES = [
    "profile:read",
    "asset:read", "asset:write",
    "design:meta:read", "design:content:read", "design:content:write",
    "brand_template:meta:read", "brand_template:content:read",
]


# ----------------------------- credentials / oauth -----------------------------

def _client():
    if not CLIENT_PATH.exists():
        sys.exit(
            "No Canva app credentials found.\n"
            "  1. Register a Canva Connect app (see onboarding/canva-setup.md).\n"
            f'  2. Save {{"client_id":"..","client_secret":".."}} to {CLIENT_PATH}\n'
            "  3. Run:  python tools/canva/canva.py login"
        )
    d = json.loads(CLIENT_PATH.read_text())
    return d["client_id"], d["client_secret"]


def _b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _basic_auth() -> str:
    cid, csec = _client()
    return "Basic " + base64.b64encode(f"{cid}:{csec}".encode()).decode()


def _post_form(url, form, auth=None):
    data = urllib.parse.urlencode(form).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    if auth:
        req.add_header("Authorization", auth)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"OAuth error {e.code}: {e.read().decode()[:500]}")


def _save_token(tok):
    HOME.mkdir(parents=True, exist_ok=True)
    tok["expires_at"] = time.time() + tok.get("expires_in", 0) - 60
    TOKEN_PATH.write_text(json.dumps(tok))
    try:
        TOKEN_PATH.chmod(0o600)
    except Exception:
        pass


def _refresh(tok):
    new = _post_form(TOKEN_URL,
                     {"grant_type": "refresh_token", "refresh_token": tok["refresh_token"]},
                     auth=_basic_auth())
    # Canva rotates the refresh token (single-use) — carry it forward if omitted.
    new.setdefault("refresh_token", tok.get("refresh_token"))
    _save_token(new)
    return json.loads(TOKEN_PATH.read_text())


def _access_token():
    if not TOKEN_PATH.exists():
        sys.exit("Not logged in to Canva. Run:  python tools/canva/canva.py login")
    tok = json.loads(TOKEN_PATH.read_text())
    if tok.get("expires_at", 0) <= time.time():
        tok = _refresh(tok)
    return tok["access_token"]


def cmd_login(_):
    cid, _csec = _client()
    verifier = _b64url(secrets.token_bytes(64))
    challenge = _b64url(hashlib.sha256(verifier.encode()).digest())
    state = _b64url(secrets.token_bytes(16))
    params = {
        "response_type": "code",
        "client_id": cid,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "code_challenge": challenge,
        "code_challenge_method": "s256",
        "state": state,
    }
    url = AUTHORIZE_URL + "?" + urllib.parse.urlencode(params)

    holder = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != "/callback":
                self.send_response(404); self.end_headers(); return
            qs = urllib.parse.parse_qs(parsed.query)
            holder["code"] = qs.get("code", [None])[0]
            holder["state"] = qs.get("state", [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h2>Canva connected. You can close this tab.</h2>")

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", REDIRECT_PORT), Handler)
    print("Opening browser for Canva consent...")
    webbrowser.open(url)
    print("If it didn't open, paste this into your browser:\n" + url)
    srv.handle_request()  # serve exactly one request (the redirect)

    if holder.get("state") != state:
        sys.exit("State mismatch — aborting for safety.")
    code = holder.get("code")
    if not code:
        sys.exit("No authorization code received.")
    tok = _post_form(TOKEN_URL, {
        "grant_type": "authorization_code",
        "code": code,
        "code_verifier": verifier,
        "redirect_uri": REDIRECT_URI,
    }, auth=_basic_auth())
    _save_token(tok)
    print("Logged in to Canva. Token saved to", TOKEN_PATH)


# ----------------------------- REST helper -----------------------------

def _api(method, path, body=None, headers=None, raw=None):
    h = {"Authorization": f"Bearer {_access_token()}"}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        h["Content-Type"] = "application/json"
    elif raw is not None:
        data = raw
    if headers:
        h.update(headers)
    req = urllib.request.Request(API + path, data=data, method=method)
    for k, v in h.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req) as r:
            text = r.read().decode()
            return json.loads(text) if text else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:800]
        sys.exit(f"Canva API {method} {path} -> {e.code}: {detail}")


def _poll(path, ok=("success",), fail=("failed",), tries=40, delay=2):
    """Poll an async job endpoint until its job.status resolves."""
    for _ in range(tries):
        res = _api("GET", path)
        job = res.get("job", res)
        status = job.get("status")
        if status in ok:
            return job
        if status in fail:
            sys.exit(f"Canva job failed: {json.dumps(job)[:500]}")
        time.sleep(delay)
    sys.exit(f"Canva job timed out: {path}")


# ----------------------------- commands -----------------------------

def cmd_whoami(_):
    print(json.dumps(_api("GET", "/v1/users/me"), indent=2))


def cmd_create_design(a):
    body = {}
    if a.preset:
        body["design_type"] = {"type": "preset", "name": a.preset}
    elif a.width and a.height:
        body["design_type"] = {"type": "custom", "width": a.width, "height": a.height}
    if a.title:
        body["title"] = a.title
    if a.asset_id:
        body["asset_id"] = a.asset_id
    res = _api("POST", "/v1/designs", body)
    d = res.get("design", res)
    print(f"Design created: id={d.get('id')}")
    urls = d.get("urls", {})
    if urls.get("edit_url"):
        print("  edit:", urls["edit_url"])
    if urls.get("view_url"):
        print("  view:", urls["view_url"])


def cmd_upload_asset(a):
    p = Path(a.file)
    raw = p.read_bytes()
    meta = json.dumps({"name_base64": base64.b64encode(p.name.encode()).decode()})
    job = _api("POST", "/v1/asset-uploads", raw=raw, headers={
        "Content-Type": "application/octet-stream",
        "Asset-Upload-Metadata": meta,
    })
    jid = job.get("job", job).get("id")
    done = _poll(f"/v1/asset-uploads/{jid}")
    asset = done.get("asset", {})
    print(f"Asset uploaded: id={asset.get('id')}  name={asset.get('name')}")


def cmd_autofill(a):
    data = json.loads(Path(a.data_file).read_text()) if a.data_file else json.loads(a.data or "{}")
    body = {"brand_template_id": a.template, "data": data}
    if a.title:
        body["title"] = a.title
    job = _api("POST", "/v1/autofills", body)
    jid = job.get("job", job).get("id")
    done = _poll(f"/v1/autofills/{jid}")
    design = done.get("result", {}).get("design", done.get("design", {}))
    print(f"Autofill done: design id={design.get('id')}")
    if design.get("urls", {}).get("edit_url"):
        print("  edit:", design["urls"]["edit_url"])


def cmd_export(a):
    body = {"design_id": a.design, "format": {"type": a.type}}
    job = _api("POST", "/v1/exports", body)
    jid = job.get("job", job).get("id")
    done = _poll(f"/v1/exports/{jid}")
    for u in done.get("urls", []):
        print("export url:", u)


def cmd_brand_templates(_):
    res = _api("GET", "/v1/brand-templates")
    for t in res.get("items", []):
        print(f"{t.get('id')}\t{t.get('title')}")


def main():
    ap = argparse.ArgumentParser(description="ShikshaLokam Canva engine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("login").set_defaults(fn=cmd_login)
    sub.add_parser("whoami").set_defaults(fn=cmd_whoami)

    cd = sub.add_parser("create-design"); cd.set_defaults(fn=cmd_create_design)
    cd.add_argument("--preset", help="Canva preset design type, e.g. 'square' / 'instagram_post'")
    cd.add_argument("--width", type=int)
    cd.add_argument("--height", type=int)
    cd.add_argument("--title")
    cd.add_argument("--asset-id", dest="asset_id", help="put an uploaded image into the design")

    ua = sub.add_parser("upload-asset"); ua.set_defaults(fn=cmd_upload_asset)
    ua.add_argument("file")

    af = sub.add_parser("autofill"); af.set_defaults(fn=cmd_autofill)
    af.add_argument("--template", required=True, help="brand_template_id")
    af.add_argument("--title")
    af.add_argument("--data", help="inline JSON of the data object")
    af.add_argument("--data-file", dest="data_file", help="path to JSON data object")

    ex = sub.add_parser("export"); ex.set_defaults(fn=cmd_export)
    ex.add_argument("--design", required=True, help="design_id")
    ex.add_argument("--type", default="png", choices=["png", "jpg", "pdf", "pptx", "gif", "mp4"])

    sub.add_parser("brand-templates").set_defaults(fn=cmd_brand_templates)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
