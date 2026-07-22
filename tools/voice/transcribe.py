#!/usr/bin/env python3
"""
Transcribe a voice note (or any audio) into text the brain can read.

This is permanent infrastructure. The ingest path advertises "voice notes" as a
supported input; this is the thing that makes that true. Do not remove it.

Usage:
    python3 tools/voice/transcribe.py <audio-file> [<audio-file> ...]
    python3 tools/voice/transcribe.py --plain <audio-file>     # no timestamps
    python3 tools/voice/transcribe.py --save <audio-file>      # also write .txt beside a
                                                               #   copy in inbox/voice/

Handles WhatsApp .ogg/.opus, .m4a, .mp3, .wav, .aac, .flac, .mp4, .mov.
Runs fully locally (faster-whisper + PyAV). No API key, no upload, no cost —
which matters, because voice notes are often the most candid thing anyone sends.

Model is cached in ~/.cache/huggingface after first run, so it works offline
thereafter. Override with SL_WHISPER_MODEL (tiny|base|small|medium|large-v3).
"""

import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
INBOX = REPO / "inbox" / "voice"

# "small" (multilingual) is the floor for this team: the people sending voice
# notes speak Indian-accented English and code-switch into Hindi mid-sentence.
# base.en mangles both, and mangles every SL proper noun. Do not downgrade to
# save 20 seconds -- a wrong transcript is worse than a slow one.
DEFAULT_MODEL = os.environ.get("SL_WHISPER_MODEL", "small")

# Whisper conditions on this prompt, so the names we use daily come out spelled
# right instead of phonetically. Add to it whenever a new programme or partner
# name starts showing up garbled.
VOCAB = (
    "ShikshaLokam, Shikshagraha, SL 2.0, InvokED, Samaaj, Sarkaar, Bazaar, "
    "Sanchaar, Shikshagraha Commons, micro-improvement, MIP, Momentum Partner, "
    "Founding Partner, Anchor Partner, Strategic Partner, Co-Builder, Weaver, "
    "SFPI, Shibulal Family Philanthropic Initiatives, NILE, ELEVATE, DIKSHA, "
    "Vidya Amrit, NLNF, NIPUN, Nagaland, Meghalaya, CMLead, STEAM, Manch, "
    "Sonal, Ayush, Aquib, Sahil, Neeraj."
)

AUDIO_EXT = {
    ".ogg", ".opus", ".oga", ".m4a", ".mp3", ".wav",
    ".aac", ".flac", ".mp4", ".mov", ".webm", ".amr",
}


def load_model(name):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit(
            "faster-whisper is not installed.\n"
            "Run: bash tools/voice/setup.sh"
        )
    # int8 on CPU: this team is on Intel Macs with no GPU. Accurate enough at
    # "small", and keeps a 60-second note under a minute of compute.
    return WhisperModel(name, device="cpu", compute_type="int8")


def transcribe(model, path, plain=False):
    segments, info = model.transcribe(
        str(path),
        vad_filter=True,          # drops the silence WhatsApp pads onto notes
        beam_size=5,
        initial_prompt=VOCAB,
    )
    lines = []
    for s in segments:
        text = s.text.strip()
        if not text:
            continue
        lines.append(text if plain else f"[{int(s.start)//60:02d}:{int(s.start)%60:02d}] {text}")
    return info, lines


def main():
    args = [a for a in sys.argv[1:]]
    plain = "--plain" in args
    save = "--save" in args
    files = [a for a in args if not a.startswith("--")]

    if not files:
        sys.exit(__doc__)

    paths = []
    for f in files:
        p = Path(f).expanduser()
        if not p.exists():
            sys.exit(f"No such file: {p}")
        if p.suffix.lower() not in AUDIO_EXT:
            sys.exit(f"Not an audio file this handles: {p.suffix} ({p.name})")
        paths.append(p)

    model = load_model(DEFAULT_MODEL)

    for p in paths:
        info, lines = transcribe(model, p, plain=plain)
        header = (
            f"# Transcript — {p.name}\n"
            f"# language={info.language} duration={info.duration:.0f}s "
            f"model={DEFAULT_MODEL}\n"
        )
        body = "\n".join(lines)
        print(header)
        print(body)

        if save:
            INBOX.mkdir(parents=True, exist_ok=True)
            out = INBOX / (p.stem + ".txt")
            out.write_text(header + "\n" + body + "\n", encoding="utf-8")
            print(f"\n# saved -> {out.relative_to(REPO)}", file=sys.stderr)


if __name__ == "__main__":
    main()
