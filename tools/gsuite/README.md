# The G-Suite engine (`tools/gsuite/`)

The brain's hands for Google Workspace. **Teammates never read this** — the brain
drives it for them. This file is for whoever maintains the engine.

## Why an engine, not MCP
A scaffolded engine gives us: one shared login, honest per-person attribution,
a fixed shared output folder, and gated sending — none of which the MCP route
gave us cleanly. The brain calls `gs.py`; humans only ever click "Allow" once.

## How auth works
- **One shared Desktop OAuth app** (Sahil sets it up once — see
  `../../onboarding/gsuite-setup.md` Part A). Its `oauth_client.json` is **gitignored and
  distributed via the private Brain Output Drive folder** — NO secret ever enters git.
  `gs.py login` auto-places it from the teammate's Downloads, so onboarding stays a single
  move. (Personal tokens also stay out of git, in `~/.shikshalokam/`.)
- **Each person logs in once** (`gs.py login`) → browser consent → their token is
  written to `~/.shikshalokam/token.json`, **outside the repo, never committed**.
- One machine = one person = honest attribution. Matches "one page, one person."

## Commands
```
python3 tools/gsuite/gs.py login            # one-time consent
python3 tools/gsuite/gs.py whoami           # who am I
python3 tools/gsuite/gs.py email-draft --to a@b.org --subject "..." --body-file f.md
python3 tools/gsuite/gs.py email-send <draft_id>     # ONLY after explicit approval
python3 tools/gsuite/gs.py doc-create --title "..." --body-file f.md
python3 tools/gsuite/gs.py drive-folder --name "..." [--parent <id>]
python3 tools/gsuite/gs.py drive-init       # build + share the Brain Output tree (once)
python3 tools/gsuite/gs.py cal-invite --summary "..." --start ... --end ... [--notify]
python3 tools/gsuite/gs.py sheet-read --id <sheet id> --range "'Tab'!A1:J40"
python3 tools/gsuite/gs.py sheet-update --id <sheet id> --range "'Tab'!A1" --values "a|b;;c|d"
python3 tools/gsuite/gs.py sheet-add-tab --id <sheet id> --title "New_Tab" --json rows.json \
        [--replace] [--header-row 2] [--freeze 2] [--col-width 250]
python3 tools/gsuite/gs.py doc-highlight --id <doc id> --tab "Draft 2" \
        [--pattern '\[\[.*?\]\]'] [--color '#FFFF00']
python3 tools/gsuite/gs.py doc-format-tab --id <doc id> --tab "Draft 1"
```

Tab bodies are inserted as **plain text** — `doc-add-tab` / `doc-set-tab` do not run the
markdown pass that `doc-create` does — so a tab draft arrives with no formatting and no
way to mark its own gaps. Two commands close that:
- `doc-format-tab` turns `**bold**` and `*italic*` markers already in the tab into real
  formatting and deletes the markers.
- `doc-highlight` colours every regex match, defaulting to `[[…]]` in yellow. Convention:
  write a missing fact inline as `[[FILL: what we still need]]` so the reader sees exactly
  what is outstanding.

Run `doc-set-tab` → `doc-format-tab` → `doc-highlight`, in that order: formatting deletes
marker characters and shifts every index after them, so highlight last.

`sheet-update`'s `--values` splits on `|` and `;;`, so it can only carry short plain
values. `sheet-add-tab` takes a JSON file (list of rows, each a list of cells) and can
therefore carry any character — use it for real content. It refuses to overwrite an
existing tab unless `--replace` is passed, and never touches other tabs.

## The two gates (never bypass)
- **Email** — `email-draft` writes a draft; nothing leaves. `email-send` is a
  separate command run **only after the person approves that specific email**.
- **Calendar** — `cal-invite` adds the event to your calendar silently; it emails
  attendees **only** with `--notify`. Treat `--notify` like a send.

## Files
- `gs.py` — the engine.
- `requirements.txt` — `pip3 install -r` once per machine.
- `oauth_client.json` — shared Desktop app config; **gitignored**, distributed via the
  private Drive folder, auto-placed by `gs.py login` from Downloads. Never committed.
- `drive_map.json` — committed folder-ID map written by `drive-init`; lets the
  whole team write into the same shared folders.
- `~/.shikshalokam/token.json` — personal, local, gitignored. Never commit.

## Extending
Add a subcommand in `gs.py` and a line here. Keep the gated pattern for anything
outward-facing (sends, shares, invites). Keep the output taxonomy in `brain.yml`.
