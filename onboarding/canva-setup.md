# Canva setup — let the brain create designs in Canva

One-time, ~5 minutes. After this, the brain can create designs, upload photos,
autofill brand templates, and export — all via `tools/canva/canva.py`, as you.

Only **you** can do Part A (registering the app); the brain can't click inside
Canva's developer portal. After that, everything is a command.

## Part A — register a Canva Connect app (once)
1. Go to **https://www.canva.com/developers/** → *Your integrations* → **Create an integration**
   (type: **Public** or **Team**; a Team integration is fine for internal use).
2. Under **Scopes**, enable:
   `profile:read`, `asset:read`, `asset:write`, `design:meta:read`,
   `design:content:read`, `design:content:write`,
   `brand_template:meta:read`, `brand_template:content:read`.
3. Under **Redirect URLs**, add exactly:
   ```
   http://127.0.0.1:8910/callback
   ```
4. Copy the **Client ID** and generate + copy the **Client secret**.
5. Save them outside the repo (never commit) at `~/.shikshalokam/canva_client.json`:
   ```json
   { "client_id": "YOUR_ID", "client_secret": "YOUR_SECRET" }
   ```
   (On Windows that's `C:\Users\<you>\.shikshalokam\canva_client.json`.)

## Part B — log in (once)
```
python tools/canva/canva.py login
```
A browser opens → approve → "Canva connected." The token lands in
`~/.shikshalokam/canva_token.json` (auto-refreshes; never committed).

Check it worked:
```
python tools/canva/canva.py whoami
```

## What the brain can then do
- `upload-asset <photo.jpg>` → returns an asset id (real photos, per our design rule).
- `create-design --width 1080 --height 1080 --title "…" [--asset-id <id>]` → a design + edit link.
- `autofill --template <brand_template_id> --data-file data.json` → a finished, on-brand design.
- `export --design <id> --type png` → a download URL.

## Honest limits (read before promising a magic poster)
- **No "Magic Design via API."** The Connect API does **not** run Canva's Magic Design
  text-to-design. It creates blank/custom designs, uploads assets, autofills **brand
  templates**, and exports.
- **Autofill needs Canva Enterprise.** `autofill` and `brand-templates` only work if the
  logged-in account is in a **Canva Enterprise** org. This is the path to a *designed,
  on-brand* poster from the brain: build a Brand Template once (with named text fields +
  an image field), then the brain fills it.
- **Without Enterprise:** the brain can still `create-design` (blank/custom) and drop an
  uploaded photo in via `--asset-id`, then hand you an edit link to finish in Canva —
  but it can't lay the whole poster out for you.

## Where things live
`tools/canva/canva.py` the engine · `~/.shikshalokam/canva_client.json` app creds (outside
repo) · `~/.shikshalokam/canva_token.json` your token (outside repo). Secrets never touch git.
