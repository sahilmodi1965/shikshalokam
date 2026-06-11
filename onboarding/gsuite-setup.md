# Switching on Google for the brain

This gives the brain hands in Gmail, Drive, Docs, and Calendar — so it can draft
emails, generate approved content as Google Docs into one shared folder, and make
calendar invites, all **as you**, with nothing sent until you approve it.

Two parts:
- **Part A** — a one-time setup, done **once for the whole team** (Sahil). ~15 min.
- **Part B** — what each teammate does. **60 seconds, one command, one click.**

---

## Part A — one-time, maintainer only (Sahil)

You're creating **one shared Google app** the whole team logs into. Do this once.

☐ **1. Make a project.** Go to <https://console.cloud.google.com> → top bar →
   *New Project* → name it `shikshalokam-brain` → Create.

☐ **2. Turn on the APIs.** *APIs & Services → Enable APIs* → enable each:
   **Gmail API**, **Google Drive API**, **Google Docs API**, **Google Calendar API**.

☐ **3. Consent screen.** *APIs & Services → OAuth consent screen*.
   - If the project sits under the **shikshalokam.org** Workspace → choose
     **Internal**. Then every `@shikshalokam.org` teammate can log in with zero
     extra steps. (Strongly preferred.)
   - If it's a personal Google account → choose **External**, and under
     *Test users* add: `sonal@shikshalokam.org`, `ayushtank@shikshalokam.org`,
     `aquib@shikshalokam.org`, and your own. (No Google verification needed for
     a small test-user list.)

☐ **4. Add the scopes** (paste these in the scopes step):
   ```
   openid
   https://www.googleapis.com/auth/userinfo.email
   https://www.googleapis.com/auth/gmail.compose
   https://www.googleapis.com/auth/drive
   https://www.googleapis.com/auth/documents
   https://www.googleapis.com/auth/calendar.events
   ```

☐ **5. Make the credential.** *APIs & Services → Credentials → Create Credentials
   → OAuth client ID → Application type: **Desktop app*** → Create → **Download JSON**.

☐ **6. Drop it in (do NOT commit).** Save that file as
   `tools/gsuite/oauth_client.json`. It is **gitignored on purpose** — never commit
   an app secret. Tell the brain *"the Google app is set up"* and it uploads the
   file once to the **private** Brain Output Drive folder, so teammates pull it
   from there during their 60-second login. (Repo stays secret-free.)

☐ **7. Build the shared folder (once).**
   ```
   pip3 install -r tools/gsuite/requirements.txt
   python3 tools/gsuite/gs.py login
   python3 tools/gsuite/gs.py drive-init
   ```
   This creates **"ShikshaLokam — Brain Output"** with clean subfolders, shares it
   with the team from `brain.yml`, and writes `tools/gsuite/drive_map.json`. Tell
   the brain *"save the drive map"* so everyone shares the same folders.

Done. The team can now do Part B.

---

## Part B — each teammate (60 seconds)

You don't need any of Part A. Just talk to the brain — *"set me up for Google"* —
and it walks you through this. By hand it's three lines:

☐ **1. Get the shared key file.** Open the **Brain Output** Drive folder (you were
   shared on it), download **`oauth_client.json`**, and save it into the brain at
   `tools/gsuite/oauth_client.json`. (Stuck? Tell the brain *"I downloaded the
   Google file"* and it moves it into place for you.)
☐ **2.** In Terminal, inside the brain:
   ```
   pip3 install -r tools/gsuite/requirements.txt
   python3 tools/gsuite/gs.py login
   ```
☐ **3.** A browser opens → pick your **@shikshalokam.org** account → **Allow**. Back
   in Terminal you'll see `Logged in as you@shikshalokam.org`. That's it.

Your login is saved on **your** computer only (`~/.shikshalokam/`, never shared).

Now just talk to the brain:
- *"Draft an email to <person> about <thing>."* → it writes the draft in **your**
  Gmail. You read it, you send it. The brain sends only if you say *"send it."*
- *"Make a Google Doc of this approved post."* → lands in the shared Docs folder.
- *"Set up a 30-min call with <person> Thursday 3pm."* → event on your calendar;
  it emails the invite only when you say so.

---

## The rules the brain keeps for you
- **Nothing leaves without you.** Emails are drafted; sending is a separate yes.
  Calendar invites notify people only on your explicit go.
- **Your login is yours.** It never enters the repo; teammates can't act as you.
- **One shared folder, kept tidy.** Approved content is generated into
  "ShikshaLokam — Brain Output" — not dumped as loose raw files.
