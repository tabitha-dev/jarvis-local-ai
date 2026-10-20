"""Tests for commands.py - run with:  python -m unittest discover tests

Nothing here actually opens apps: every launcher is replaced with a fake
that just records what WOULD have happened.
"""
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import commands  # noqa: E402


class FakeLaunchers(unittest.TestCase):
    def setUp(self):
        self.calls = []
        patches = [
            mock.patch.object(commands, "start", lambda t: self.calls.append(("app", t))),
            mock.patch.object(commands, "open_url", lambda u: self.calls.append(("url", u))),
            mock.patch.object(commands, "press_key", lambda vk, times=1: self.calls.append(("key", vk, times))),
            mock.patch.object(commands, "start_menu_lookup", lambda name: None),
            mock.patch.object(commands.os, "startfile", lambda p: self.calls.append(("file", p)), create=True),
            mock.patch.object(commands.subprocess, "Popen", lambda *a, **k: self.calls.append(("popen", a[0]))),
            mock.patch.object(commands.subprocess, "run",
                              lambda *a, **k: type("R", (), {"returncode": 0})()),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)

    def run_cmd(self, text):
        self.calls.clear()
        return commands.try_run(text)


class TestRouting(FakeLaunchers):
    def test_open_app_with_filler_words(self):
        self.assertEqual(self.run_cmd("Hey Jarvis, can you open Chrome please?"), "Opening chrome.")
        self.assertEqual(self.calls, [("app", "chrome")])

    def test_open_website_shortcut(self):
        self.run_cmd("Open YouTube.")
        self.assertEqual(self.calls, [("url", "https://www.youtube.com")])

    def test_open_two_things(self):
        self.run_cmd("open chrome and youtube")
        self.assertEqual([c[0] for c in self.calls], ["app", "url"])

    def test_search_youtube(self):
        self.run_cmd("search YouTube for lo-fi beats")
        self.assertEqual(self.calls, [("url", "https://www.youtube.com/results?search_query=lo-fi+beats")])

    def test_search_on_unknown_engine_does_not_crash(self):
        # used to raise KeyError('main')
        reply = self.run_cmd("search for restaurants on main")
        self.assertIn("Searching Google", reply)

    def test_volume(self):
        self.run_cmd("turn the volume up")
        self.assertEqual(self.calls, [("key", commands.VK_VOLUME_UP, 5)])

    def test_questions_go_to_the_ai(self):
        for q in ("How are you doing today?", "Tell me a joke", "explain flexbox like I'm five"):
            self.assertIsNone(self.run_cmd(q), q)
        self.assertEqual(self.calls, [])

    def test_time_questions_are_instant(self):
        for q in ("What time is it right now?", "Hey Jarvis, what time is it?", "what's the time now",
                  "tell me the time please", "do you know what time it is", "What day is it today?"):
            reply = self.run_cmd(q)
            self.assertIsNotNone(reply, q)
            self.assertTrue(reply.startswith(("It's", "Today is")), (q, reply))

    def test_other_time_zones_are_not_answered_from_the_pc_clock(self):
        self.assertIsNone(self.run_cmd("what time is it in Tokyo"))

    def test_long_unknown_open_goes_to_ai(self):
        self.assertIsNone(self.run_cmd("start a timer for ten minutes please"))


class TestSafety(FakeLaunchers):
    def test_search_text_is_url_encoded(self):
        self.run_cmd('search google for "a" & calc')
        url = self.calls[0][1]
        self.assertNotIn('"', url)
        self.assertNotIn(" ", url)

    def test_weird_website_text_is_not_opened(self):
        reply = self.run_cmd('open x.com/"&calc&"')
        self.assertFalse(any(c[0] == "url" for c in self.calls), self.calls)
        self.assertIsNotNone(reply)

    def test_refuses_to_close_windows_itself(self):
        reply = self.run_cmd("close explorer")
        self.assertIn("won't close", reply)

    def test_refuses_to_close_jarvis_console(self):
        self.assertIn("won't close", self.run_cmd("close python"))


class TestUrlGuard(unittest.TestCase):
    def test_open_url_rejects_quotes_and_spaces(self):
        for bad in ('https://x.com/"&calc', "https://x.com/a b", "file:///C:/Windows", "javascript:alert(1)"):
            with self.assertRaises(ValueError, msg=bad):
                commands.open_url(bad)

    def test_open_url_accepts_normal_links(self):
        with mock.patch.object(commands, "find_exe", lambda n: None), \
             mock.patch.object(commands.webbrowser, "open") as wb:
            commands.open_url("https://www.youtube.com/results?search_query=lo-fi+beats")
            wb.assert_called_once()


if __name__ == "__main__":
    unittest.main()
