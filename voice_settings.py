"""Validated, user-local voice preference. Public choices exclude unlicensed voices."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parent
CONFIG_FILE = ROOT / "commands.json"
DEFAULT_VOICE = "windows"
# Only these exact public options may be selected or loaded by Jarvis.
VOICE_MODELS = {
    "windows": None,
    "piper:en_GB-cori-medium": "en_GB-cori-medium",
}


def get_voice(path: Path | None = None) -> str:
    """Missing/corrupted/unknown private configuration safely chooses Windows."""
    path = Path(path) if path is not None else CONFIG_FILE
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return DEFAULT_VOICE
    if not isinstance(data, dict):
        return DEFAULT_VOICE
    candidate = data.get("voice", DEFAULT_VOICE)
    return candidate if isinstance(candidate, str) and candidate in VOICE_MODELS else DEFAULT_VOICE


def save_voice(selection: str, path: Path | None = None) -> None:
    """Update only voice, preserving the person's other shortcuts and config."""
    if selection not in VOICE_MODELS:
        raise ValueError("Voice not in the public allowlist")
    path = Path(path) if path is not None else CONFIG_FILE
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Invalid commands.json: expected a JSON object")
    else:
        data = {}
    data["voice"] = selection
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=".voice-setting-", suffix=".tmp", delete=False) as f:
            tmp = Path(f.name)
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    finally:
        if tmp is not None and tmp.exists():
            tmp.unlink()
