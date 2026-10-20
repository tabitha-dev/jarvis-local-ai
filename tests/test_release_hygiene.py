"""Guard against accidentally publishing private files in the tracked source tree.

These checks run without network, model downloads, microphone access, or billing.
They cover *tracked paths* only, not Git history or contents of opaque media.
"""
from __future__ import annotations

from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]

BANNED_DIRS = {".venv", "venv", "models", "voices", "__pycache__", ".pytest_cache"}
BANNED_SUFFIXES = {".mp3", ".wav", ".m4a", ".mp4", ".onnx", ".tflite",
                   ".pem", ".key", ".zip", ".log"}
BANNED_NAMES = {"commands.json", "windows-test-report.txt",
                "requirements.lock.tmp", ".env"}


def tracked_paths() -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z"],
        check=True, capture_output=True, timeout=10,
    )
    return [p.decode("utf-8") for p in result.stdout.split(b"\0") if p]


class PublicReleaseHygieneTests(unittest.TestCase):
    def test_no_private_paths_are_git_tracked(self):
        paths = tracked_paths()
        self.assertTrue(paths, "Expected Git tracked files for release audit")
        errors = []
        for name in paths:
            item = Path(name)
            parts_lower = {p.lower() for p in item.parts}
            filename = item.name.lower()
            if (parts_lower & BANNED_DIRS or filename in BANNED_NAMES
                    or (filename.startswith(".env.") and filename != ".env.example")
                    or item.suffix.lower() in BANNED_SUFFIXES):
                errors.append(name)
        self.assertEqual(errors, [], "Restricted paths are tracked: " + ", ".join(errors))

    def test_public_rights_notice_is_present(self):
        notice = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
        self.assertIn("CC BY-NC-SA", notice)
        self.assertIn("Cori", notice)
        self.assertIn("Alan", notice)

    def test_release_stays_on_hold_without_windows_evidence(self):
        readiness = (ROOT / "RELEASE_READINESS.md").read_text(encoding="utf-8")
        self.assertIn("PRIVATE, PRE-RELEASE", readiness)
        self.assertIn("fresh windows", readiness.lower())
        self.assertIn("requirements.lock.txt", readiness)


if __name__ == "__main__":
    unittest.main()
