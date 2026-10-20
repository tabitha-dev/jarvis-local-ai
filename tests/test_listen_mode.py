"""Wake word is opt-in: the default install never downloads the non-commercial model."""
import argparse
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import jarvis  # noqa: E402


def args(**kw):
    base = dict(ptt=False, text=False, no_ui=False, wake=False)
    base.update(kw)
    return argparse.Namespace(**base)


class ListenModeTests(unittest.TestCase):
    def test_default_is_talk_button(self):
        self.assertEqual(jarvis.listen_mode(args()), "button")

    def test_wake_word_only_when_asked(self):
        self.assertEqual(jarvis.listen_mode(args(wake=True)), "wake")

    def test_ptt_and_no_ui_use_enter(self):
        self.assertEqual(jarvis.listen_mode(args(ptt=True)), "enter")
        self.assertEqual(jarvis.listen_mode(args(no_ui=True)), "enter")

    def test_talk_button_returns_ui_events_without_a_model(self):
        class Mic:
            noise_floor = 1.0
            def flush(self): pass
            def read(self): return b"\0" * 10
        class UI:
            def __init__(self): self.calls = 0
            def level(self, *a): pass
            def poll(self):
                self.calls += 1
                return ("talk", None) if self.calls > 2 else None
        self.assertEqual(jarvis.TalkButton().wait(Mic(), UI()), ("talk", None))

    def test_setup_does_not_download_wake_word_model(self):
        setup = (ROOT / "setup.bat").read_text(encoding="utf-8")
        self.assertNotIn("download_models", setup)
        self.assertNotIn("hey_jarvis", setup)

    def test_no_movie_reference_in_persona(self):
        self.assertNotIn("Iron Man", (ROOT / "jarvis.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
