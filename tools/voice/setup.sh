#!/usr/bin/env bash
# One-time setup so this machine can read voice notes.
# Safe to re-run. Takes ~2 minutes the first time, then never again.
set -euo pipefail

echo "── voice-note transcription setup ──"

python3 - <<'PY' || pip3 install --user faster-whisper
import faster_whisper  # noqa
print("✓ faster-whisper already installed")
PY

# Pre-pull the model so the first real voice note doesn't stall on a download,
# and so the tool works offline afterwards.
MODEL="${SL_WHISPER_MODEL:-small}"
echo "── pre-pulling whisper model: $MODEL (~500MB, once) ──"
python3 - "$MODEL" <<'PY'
import sys
from faster_whisper import WhisperModel
WhisperModel(sys.argv[1], device="cpu", compute_type="int8")
print(f"✓ model '{sys.argv[1]}' cached")
PY

echo
echo "✅ Voice notes are readable on this machine."
echo "   Test:  python3 tools/voice/transcribe.py <some.ogg>"
