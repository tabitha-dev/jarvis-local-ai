"""Checks that only the Jarvis window can send commands to Jarvis.

Run with:  python -m unittest discover tests
Starts the real HUD server on a spare local port; no microphone or AI needed.
"""
import http.client
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import jarvis  # noqa: E402


class TestHudSecurity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ui = jarvis.UI(port=18765)
        cls.port = cls.ui.server.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.ui.server.shutdown()

    def post(self, path="/say", body=None, headers=None):
        h = {"Host": f"127.0.0.1:{self.port}", "Content-Type": "application/json",
             "X-Jarvis-Token": self.ui.token}
        h.update(headers or {})
        h = {k: v for k, v in h.items() if v is not None}
        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        data = body if isinstance(body, bytes) else json.dumps(body or {"text": "open chrome"}).encode()
        c.request("POST", path, body=data, headers=h)
        r = c.getresponse()
        r.read()
        return r.status

    def drain(self):
        out = []
        while (m := self.ui.poll()):
            out.append(m)
        return out

    def test_page_contains_token(self):
        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        c.request("GET", "/", headers={"Host": f"127.0.0.1:{self.port}"})
        html = c.getresponse().read().decode()
        self.assertIn(self.ui.token, html)
        self.assertNotIn("__JARVIS_TOKEN__", html)

    def get(self, path, headers=None):
        h = {"Host": f"127.0.0.1:{self.port}"}
        h.update(headers or {})
        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3)
        c.request("GET", path, headers=h)
        response = c.getresponse()
        status = response.status
        # For successful SSE, immediately close so the test never waits for
        # the long-lived event stream to finish.
        if status != 200:
            response.read()
        c.close()
        return status

    def test_events_requires_token(self):
        self.assertEqual(self.get("/events"), 403)
        self.assertEqual(self.get("/events?token=wrong"), 403)

    def test_events_rejects_foreign_origin_even_with_token(self):
        self.assertEqual(self.get("/events?token=" + self.ui.token,
                                  {"Origin": "https://untrusted.example"}), 403)

    def test_events_accepts_matching_token(self):
        self.assertEqual(self.get("/events?token=" + self.ui.token), 200)

    def test_good_request_is_accepted(self):
        self.drain()
        self.assertEqual(self.post(), 204)
        self.assertEqual(self.drain(), [("text", "open chrome")])

    def test_missing_token_is_rejected(self):
        self.assertEqual(self.post(headers={"X-Jarvis-Token": None}), 403)
        self.assertEqual(self.drain(), [])

    def test_other_website_is_rejected(self):
        self.assertEqual(self.post(headers={"Origin": "https://evil.example"}), 403)

    def test_dns_rebinding_host_is_rejected(self):
        self.assertEqual(self.post(headers={"Host": "evil.example:8765"}), 403)

    def test_plain_text_form_post_is_rejected(self):
        # what a hidden form on another site would send
        self.assertEqual(self.post(headers={"Content-Type": "text/plain"}), 403)

    def test_huge_body_is_rejected(self):
        self.assertEqual(self.post(body=b'{"text":"' + b"a" * 10000 + b'"}'), 413)

    def test_unknown_path_is_404(self):
        self.assertEqual(self.post(path="/run"), 404)


class TestQuitPhrases(unittest.TestCase):
    def test_exact_goodbye_quits(self):
        for t in ("Goodbye.", "Hey Jarvis, goodbye!", "go to sleep"):
            self.assertIn(jarvis.phrase(t), jarvis.QUIT_WORDS, t)

    def test_questions_mentioning_goodbye_do_not_quit(self):
        for t in ("How do I say goodbye in French?", "How do I shut down a docker container?"):
            self.assertNotIn(jarvis.phrase(t), jarvis.QUIT_WORDS, t)


if __name__ == "__main__":
    unittest.main()
