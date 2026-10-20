"""Checks which HUD colors each kind of request shows.

Run with:  python -m unittest discover tests
Amber "thinking" must mean ONLY "the AI model is working".
"""
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import commands  # noqa: E402
import jarvis  # noqa: E402


class FakeUI:
    def __init__(self):
        self.states = []

    def state(self, value):
        self.states.append(value)

    def emit(self, *a, **k):
        pass


class FakeVoice:
    def say(self, text):
        pass


class FakeBrain:
    def ask(self, text, on_sentence):
        on_sentence("Imagine a toy shelf.")


class TestHudStates(unittest.TestCase):
    def setUp(self):
        p = mock.patch.object(commands.subprocess, "Popen", lambda *a, **k: None)
        p.start()
        self.addCleanup(p.stop)

    def test_instant_command_never_shows_thinking(self):
        ui = FakeUI()
        jarvis.handle("What time is it right now?", FakeBrain(), FakeVoice(), ui)
        self.assertNotIn("thinking", ui.states)
        self.assertIn("speaking", ui.states)

    def test_ai_question_shows_thinking_then_speaking(self):
        ui = FakeUI()
        jarvis.handle("Explain flexbox like I'm five", FakeBrain(), FakeVoice(), ui)
        self.assertIn("thinking", ui.states)
        self.assertLess(ui.states.index("thinking"), ui.states.index("speaking"))

    def test_hud_has_a_hearing_label(self):
        html = (Path(jarvis.__file__).parent / "ui.html").read_text(encoding="utf-8")
        self.assertIn('hearing:   ["HEARING"', html)

    def test_speech_to_text_uses_hearing_not_thinking(self):
        src = Path(jarvis.__file__).read_text(encoding="utf-8")
        before_transcribe = src.split("text = ears.transcribe(audio)")[0].rsplit("ui.state(", 1)[1]
        self.assertTrue(before_transcribe.startswith('"hearing"'), before_transcribe[:20])


if __name__ == "__main__":
    unittest.main()
