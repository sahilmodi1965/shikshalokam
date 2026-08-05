#!/usr/bin/env python3
"""Hand a generation prompt to the Gemini web app — free, no API, no billing.

The brain writes a good image/video prompt; this copies it to the clipboard and
opens Gemini in the default browser. You paste (Ctrl/Cmd+V) and hit enter, then
generate right there in your Gemini window. Nothing is sent to any paid API.

Usage:
  python tools/gemini/handoff.py "your prompt here"
  echo "your prompt" | python tools/gemini/handoff.py
  python tools/gemini/handoff.py --video "your prompt here"   # (label only)
"""
import sys, subprocess, webbrowser, platform

GEMINI_URL = "https://gemini.google.com/app"


def copy_to_clipboard(text: str) -> bool:
    """Cross-platform clipboard copy. Returns True on success."""
    system = platform.system()
    if system == "Windows":
        # Try PowerShell Set-Clipboard first (more reliable than clip.exe, which
        # fails in some shells with "Access is denied"), then fall back to clip.
        for cmd in (["powershell", "-NoProfile", "-Command",
                     "$input | Set-Clipboard"], ["clip"]):
            try:
                subprocess.run(cmd, input=text, text=True, check=True)
                return True
            except Exception:  # noqa: BLE001 — try the next method
                continue
        print("(couldn't reach clipboard on Windows)", file=sys.stderr)
        return False
    try:
        if system == "Darwin":
            subprocess.run(["pbcopy"], input=text, text=True, check=True)
        else:  # Linux
            subprocess.run(["xclip", "-selection", "clipboard"],
                           input=text, text=True, check=True)
        return True
    except Exception as e:  # noqa: BLE001 — clipboard is best-effort
        print(f"(couldn't reach clipboard: {e})", file=sys.stderr)
        return False


def main(argv):
    args = [a for a in argv if a not in ("--video", "--image")]
    prompt = " ".join(args).strip() or sys.stdin.read().strip()
    if not prompt:
        sys.exit("No prompt given.")

    ok = copy_to_clipboard(prompt)
    webbrowser.open(GEMINI_URL)

    print("Gemini opened in your browser.")
    if ok:
        print("Prompt is on your clipboard — click the box, paste (Ctrl+V), Enter.")
    else:
        print("Paste this prompt yourself:\n\n" + prompt)


if __name__ == "__main__":
    main(sys.argv[1:])
