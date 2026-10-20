"""Numbered local voice selector. Never accepts a free-typed model name.

Called by setup.bat and change_voice.bat. Press 1, 2 or Enter. A missing
console or 25-second timeout selects Windows, so unattended setup is safe.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from voice_settings import DEFAULT_VOICE, VOICE_MODELS, save_voice  # noqa: E402

NUMBERED = {"1": "windows", "2": "piper:en_GB-cori-medium"}


def choose_menu(timeout: float = 25.0) -> str:
    """Accept only keys 1, 2 and Enter; timeout/non-console => Windows."""
    if os.name != "nt" or not sys.stdin.isatty():
        print("No interactive Windows console; using Windows voice.")
        return DEFAULT_VOICE
    import msvcrt
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if msvcrt.kbhit():
            key = msvcrt.getwch()
            if key in ("\r", "\n"):
                return DEFAULT_VOICE
            if key in NUMBERED:
                return NUMBERED[key]
            if key in ("\x00", "\xe0") and msvcrt.kbhit():
                msvcrt.getwch()  # Ignore the second byte of a special key.
            print("Please press 1, 2, or Enter for the default.")
        time.sleep(0.05)
    print("No choice received; using Windows voice.")
    return DEFAULT_VOICE


def apply_voice(selection: str, config: Path | None = None, python_exe: str | None = None) -> None:
    """Fixed allowlist and list-form arguments prevent arbitrary model downloads."""
    if selection not in VOICE_MODELS:
        raise ValueError("Unknown voice selection")
    model = VOICE_MODELS[selection]
    if model is not None:
        (ROOT / "voices").mkdir(exist_ok=True)
        cmd = [python_exe or sys.executable, "-m", "piper.download_voices", model,
               "--data-dir", str(ROOT / "voices")]
        print("Downloading the chosen optional Piper voice...")
        subprocess.run(cmd, check=True, cwd=str(ROOT))
    save_voice(selection, path=config)
    print("Saved your private voice preference to commands.json:", selection)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Choose an allowed Jarvis voice on this PC")
    ap.add_argument("--timeout", type=float, default=25.0)
    args = ap.parse_args(argv)
    print("\nChoose a voice for this computer:")
    print("  1. Windows built-in voice (default; no voice download)")
    print("  2. Cori (British female; Piper; public-domain training recordings; optional download)")
    print("     Model and audio usage terms still require review; see docs/LICENSE_REVIEW.md")
    print("Press 1 or 2, or Enter for Windows. After 25 seconds, Windows is selected.")
    try:
        selection = choose_menu(max(0.0, min(args.timeout, 120.0)))
        apply_voice(selection)
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print("Voice selection was not saved. Existing preference remains: " + str(exc), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
