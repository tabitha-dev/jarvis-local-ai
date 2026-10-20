"""
Jarvis - an offline voice assistant for Windows.

  Wake word  : "Hey Jarvis"   (openWakeWord, runs locally)
  Ears       : faster-whisper (speech-to-text, runs locally)
  Brain      : Ollama         (local AI model, no tokens, no internet)
  Voice      : Piper          (text-to-speech, runs locally)
               falls back to the built-in Windows voice if Piper isn't set up

Run:
  python jarvis.py            -> say "Hey Jarvis", then talk
  python jarvis.py --ptt      -> press Enter to talk (no wake word)
  python jarvis.py --text     -> type instead of talk (good for testing)
  python jarvis.py --no-ui    -> no HUD window, console only

The HUD window opens automatically. You can also type to Jarvis there,
or click TALK to speak without saying the wake word.

Say "goodbye" to quit, or "forget everything" to clear the conversation.
"""

import argparse
import datetime as dt
import http.server
import json
import queue
import re
import secrets
import subprocess
import sys
import threading
import urllib.parse
import time
import webbrowser
from pathlib import Path

import numpy as np
import requests
import sounddevice as sd

# --------------------------------------------------------------------------
# SETTINGS - change these to taste
# --------------------------------------------------------------------------
OLLAMA_MODEL = "gemma4:e2b"        # bigger/smarter: "gemma4:e4b" (needs a better PC)
OLLAMA_URL = "http://localhost:11434/api/chat"

WHISPER_MODEL = "base.en"          # "tiny.en" = faster, "small.en" = more accurate
WHISPER_DEVICE = "cpu"             # "cuda" if you have an NVIDIA GPU set up

PIPER_VOICE = "en_GB-alan-medium"  # Rights unclear; do not use commercially without permission. See docs/LICENSE_REVIEW.md.
# Cori has public-domain training data; verify model rights and change setup.bat to match.
VOICES_DIR = Path(__file__).parent / "voices"

WAKE_THRESHOLD = 0.5               # raise to 0.6-0.7 if it wakes up by accident
SILENCE_SECONDS = 1.0              # how long a pause ends your sentence
MAX_LISTEN_SECONDS = 20
MEMORY_TURNS = 10                  # how many back-and-forths it remembers
USER_NAME = "Friend"               # change this to your name
UI_PORT = 8765                     # local-only HUD port (tries the next few if busy)

SYSTEM_PROMPT = (
    "You are Jarvis, a witty, loyal British AI assistant, like the one from Iron Man. "
    f"The user is {USER_NAME}. Your replies are spoken out loud, so: "
    "keep answers short (1-3 sentences unless asked for more), never use markdown, "
    "bullet points, emojis, or code blocks, and spell things out the way you'd say them. "
    "If you don't know something, say so plainly. "
    "You can open apps and websites, search the web, and control volume and music - those "
    "commands are handled separately before questions reach you, so if the user asks you to "
    "do something on the computer that you can't, suggest they phrase it like 'open Chrome' "
    "or 'search YouTube for something'."
)

SAMPLE_RATE = 16000
FRAME = 1280  # 80 ms of audio, what the wake-word model expects


# --------------------------------------------------------------------------
# Microphone
# --------------------------------------------------------------------------
class Mic:
    def __init__(self):
        self.q = queue.Queue()
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE, channels=1, dtype="int16",
            blocksize=FRAME, callback=self._cb,
        )
        self.stream.start()
        self.noise_floor = 300.0

    def _cb(self, indata, frames, t, status):
        self.q.put(indata[:, 0].copy())

    def read(self):
        return self.q.get()

    def flush(self):
        """Throw away audio captured while Jarvis was talking."""
        while not self.q.empty():
            try:
                self.q.get_nowait()
            except queue.Empty:
                break

    def calibrate(self, seconds=1.0):
        self.flush()
        levels = [rms(self.read()) for _ in range(int(seconds * SAMPLE_RATE / FRAME))]
        self.noise_floor = max(float(np.median(levels)), 20.0)
        print(f"  mic background level: {self.noise_floor:.0f}")

    def record_utterance(self, ui=None):
        """Record until the speaker pauses. Returns float32 audio (never gives up early).

        Quiet mics are fine: even if the volume never crosses the "talking" level,
        we still hand the audio to Whisper, which has its own speech detector.
        """
        start_level = self.noise_floor * 1.8
        frames, started, silent_frames, peak = [], False, 0, 0.0
        silence_limit = int(SILENCE_SECONDS * SAMPLE_RATE / FRAME)
        max_frames = int(MAX_LISTEN_SECONDS * SAMPLE_RATE / FRAME)
        wait_frames = int(6 * SAMPLE_RATE / FRAME)  # stop waiting after 6 s of nothing

        for i in range(max_frames):
            chunk = self.read()
            if ui:
                ui.level(chunk, self.noise_floor)
            level = rms(chunk)
            peak = max(peak, level)
            loud = level > start_level
            frames.append(chunk)
            if not started:
                if loud:
                    started = True
                elif i > wait_frames:
                    break
                continue
            silent_frames = 0 if loud else silent_frames + 1
            if silent_frames >= silence_limit:
                break

        self.last_peak = peak
        return np.concatenate(frames).astype(np.float32) / 32768.0


def rms(chunk):
    return float(np.sqrt(np.mean(chunk.astype(np.float32) ** 2)))


def beep(freq=880, ms=120):
    try:
        import winsound
        winsound.Beep(freq, ms)
    except Exception:
        pass


# --------------------------------------------------------------------------
# Wake word
# --------------------------------------------------------------------------
class WakeWord:
    def __init__(self):
        import openwakeword
        from openwakeword.model import Model
        openwakeword.utils.download_models(["hey_jarvis"])  # one-time download
        self.model = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")

    def wait(self, mic, ui=None):
        """Block until "Hey Jarvis" is heard or the UI sends something."""
        self.model.reset()
        mic.flush()
        n = 0
        while True:
            chunk = mic.read()
            if ui:
                msg = ui.poll()
                if msg:
                    return msg
                n += 1
                if n % 2 == 0:
                    ui.level(chunk, mic.noise_floor)
            scores = self.model.predict(chunk)
            if max(scores.values()) >= WAKE_THRESHOLD:
                self.model.reset()
                return ("wake", None)


# --------------------------------------------------------------------------
# Speech to text
# --------------------------------------------------------------------------
class Ears:
    def __init__(self):
        from faster_whisper import WhisperModel
        compute = "int8" if WHISPER_DEVICE == "cpu" else "float16"
        self.model = WhisperModel(WHISPER_MODEL, device=WHISPER_DEVICE, compute_type=compute)

    def transcribe(self, audio):
        segments, _ = self.model.transcribe(audio, language="en", beam_size=1, vad_filter=True)
        return " ".join(s.text.strip() for s in segments).strip()


# --------------------------------------------------------------------------
# Text to speech
# --------------------------------------------------------------------------
class Voice:
    def __init__(self):
        self.piper = None
        self.fallback = None
        model_path = VOICES_DIR / f"{PIPER_VOICE}.onnx"
        try:
            from piper import PiperVoice
            if model_path.exists():
                self.piper = PiperVoice.load(str(model_path))
            else:
                print(f"  (Piper voice not found at {model_path}; using the Windows voice)")
        except Exception as e:
            print(f"  (Piper unavailable: {e}; using the Windows voice)")
        if self.piper is None:
            import pyttsx3
            self.fallback = pyttsx3.init()
            self.fallback.setProperty("rate", 185)

    def say(self, text):
        text = clean_for_speech(text)
        if not text:
            return
        if self.piper:
            for chunk in self.piper.synthesize(text):
                sd.play(chunk.audio_int16_array, chunk.sample_rate)
                sd.wait()
        else:
            self.fallback.say(text)
            self.fallback.runAndWait()


def clean_for_speech(text):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    text = re.sub(r"```.*?```", " (I've left out the code) ", text, flags=re.S)
    text = re.sub(r"(^|\n)\s*([-*]|\d+\.)\s+", r"\1", text)  # list bullets
    text = re.sub(r"[*_#`>|]", "", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)  # markdown links -> text
    return re.sub(r"\s+", " ", text).strip()


# --------------------------------------------------------------------------
# Brain (Ollama)
# --------------------------------------------------------------------------
class Brain:
    def __init__(self):
        self.history = []
        try:
            requests.get("http://localhost:11434", timeout=3)
        except requests.RequestException:
            sys.exit("Ollama isn't running. Open the Ollama app (or run `ollama serve`) and try again.")

    def reset(self):
        self.history = []

    def ask(self, text, on_sentence):
        """Stream the reply and hand each finished sentence to on_sentence()."""
        now = dt.datetime.now().strftime("%A %B %d %Y, %I:%M %p")
        messages = [{"role": "system", "content": f"{SYSTEM_PROMPT} Current date and time: {now}."}]
        messages += self.history[-MEMORY_TURNS * 2:]
        messages.append({"role": "user", "content": text})

        payload = {"model": OLLAMA_MODEL, "messages": messages, "stream": True, "keep_alive": "30m"}
        full, buf, in_think = "", "", False
        with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=300) as r:
            if r.status_code == 404:
                raise RuntimeError(f"Model '{OLLAMA_MODEL}' isn't downloaded. Run: ollama pull {OLLAMA_MODEL}")
            r.raise_for_status()
            for line in r.iter_lines():
                if not line:
                    continue
                data = json.loads(line)
                if data.get("error"):
                    raise RuntimeError(f"Ollama error: {data['error']}")
                piece = data.get("message", {}).get("content", "")
                full += piece
                # skip any "thinking" text some models produce
                if "<think>" in piece:
                    in_think = True
                if in_think:
                    if "</think>" in piece:
                        in_think = False
                        buf += piece.split("</think>", 1)[1]
                    continue
                buf += piece
                # speak each sentence as soon as it's finished
                while True:
                    m = re.search(r"^(.*?[.!?])\s+", buf, flags=re.S)
                    if not m:
                        break
                    on_sentence(m.group(1))
                    buf = buf[m.end():]
        if buf.strip():
            on_sentence(buf)

        self.history += [
            {"role": "user", "content": text},
            {"role": "assistant", "content": clean_for_speech(full)},
        ]


# --------------------------------------------------------------------------
# Interface (local web page in its own window - nothing leaves your PC)
# --------------------------------------------------------------------------
class UI:
    """Serves ui.html on localhost and pushes live events to it."""

    MAX_BODY = 4096      # bytes; commands are short
    MAX_TEXT = 500       # characters

    def __init__(self, port=UI_PORT, enabled=True):
        self.enabled = enabled
        # A fresh secret each run. Only the page Jarvis serves knows it, so other
        # websites open in your browser can't send commands to Jarvis (CSRF).
        self.token = secrets.token_urlsafe(24)
        self.inbox = queue.Queue()   # ("text", "...") or ("talk", None) from the page
        self.clients = []
        self.lock = threading.Lock()
        self.last = {"state": "idle"}
        self.history = []            # replayed when the window (re)connects
        if not enabled:
            return
        ui = self
        html_path = Path(__file__).parent / "ui.html"

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _allowed_host(self):
                # Blocks "DNS rebinding": a web page pretending to be 127.0.0.1
                return self.headers.get("Host", "") in ui.allowed_hosts

            def _reject(self, code):
                self.send_response(code)
                self.send_header("Content-Length", "0")
                self.end_headers()

            def do_GET(self):
                if not self._allowed_host():
                    return self._reject(403)
                parsed = urllib.parse.urlsplit(self.path)
                if parsed.path not in ("/", "/events"):
                    return self._reject(404)
                if parsed.path == "/events":
                    # EventSource cannot send a custom authorization header.
                    # Require the per-run token in the query string and reject
                    # requests from foreign browser origins before opening SSE.
                    origin = self.headers.get("Origin")
                    ticket = urllib.parse.parse_qs(parsed.query).get("token", [""])
                    if (origin and origin not in ui.allowed_origins) or not (
                        len(ticket) == 1 and secrets.compare_digest(ticket[0], ui.token)
                    ):
                        return self._reject(403)
                    self.send_response(200)
                    self.send_header("Content-Type", "text/event-stream")
                    self.send_header("Cache-Control", "no-store")
                    self.send_header("Referrer-Policy", "no-referrer")
                    self.send_header("X-Content-Type-Options", "nosniff")
                    self.end_headers()
                    q = queue.Queue()
                    with ui.lock:
                        ui.clients.append(q)
                    try:
                        self._send({"type": "info", "model": OLLAMA_MODEL, "user": USER_NAME})
                        for past in list(ui.history):
                            self._send(past)
                        self._send({"type": "state", "value": ui.last["state"]})
                        while True:
                            try:
                                self._send(q.get(timeout=15))
                            except queue.Empty:
                                self.wfile.write(b": ping\n\n")
                                self.wfile.flush()
                    except (BrokenPipeError, ConnectionError, OSError):
                        pass
                    finally:
                        with ui.lock:
                            if q in ui.clients:
                                ui.clients.remove(q)
                    return
                if parsed.query:
                    return self._reject(404)
                data = html_path.read_bytes().replace(b"__JARVIS_TOKEN__", ui.token.encode())
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("X-Frame-Options", "DENY")
                self.send_header("Referrer-Policy", "no-referrer")
                self.send_header("Content-Security-Policy",
                                 "default-src 'self'; script-src 'self' 'unsafe-inline'; "
                                 "style-src 'self' 'unsafe-inline'; frame-ancestors 'none'")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_POST(self):
                origin = self.headers.get("Origin")
                if (not self._allowed_host()
                        or (origin and origin not in ui.allowed_origins)
                        or not secrets.compare_digest(self.headers.get("X-Jarvis-Token", ""), ui.token)
                        or not self.headers.get("Content-Type", "").startswith("application/json")):
                    return self._reject(403)
                try:
                    n = int(self.headers.get("Content-Length") or 0)
                except ValueError:
                    return self._reject(400)
                if n > UI.MAX_BODY:
                    return self._reject(413)
                try:
                    body = json.loads(self.rfile.read(n) or b"{}")
                except ValueError:
                    return self._reject(400)
                if not isinstance(body, dict):
                    return self._reject(400)
                text = str(body.get("text", "")).strip()[:UI.MAX_TEXT]
                if self.path == "/say" and text:
                    ui.inbox.put(("text", text))
                elif self.path == "/talk":
                    ui.inbox.put(("talk", None))
                else:
                    return self._reject(404)
                self._reject(204)

            def _send(self, event):
                self.wfile.write(f"data: {json.dumps(event)}\n\n".encode())
                self.wfile.flush()

        for p in range(port, port + 10):  # another copy running? use the next free port
            try:
                self.server = http.server.ThreadingHTTPServer(("127.0.0.1", p), Handler)
                port = p
                break
            except OSError:
                continue
        else:
            raise RuntimeError(f"No free port between {UI_PORT} and {UI_PORT + 9} for the HUD")
        self.allowed_hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
        self.allowed_origins = {f"http://127.0.0.1:{port}", f"http://localhost:{port}"}
        self.server.daemon_threads = True
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{port}/"

    def open_window(self):
        if not self.enabled:
            return
        # Edge "app mode" = a clean window with no tabs or address bar
        for exe in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"):
            if Path(exe).exists():
                subprocess.Popen([exe, f"--app={self.url}", "--window-size=1280,800"])
                return
        webbrowser.open(self.url)

    def emit(self, type_, **kw):
        if not self.enabled:
            return
        event = {"type": type_, **kw}
        if type_ == "state":
            self.last["state"] = kw.get("value", "idle")
        elif type_ != "level":
            self.history = (self.history + [event])[-300:]
        with self.lock:
            for q in list(self.clients):
                q.put(event)

    def state(self, value):
        self.emit("state", value=value)

    def level(self, chunk, floor):
        self.emit("level", value=min(1.0, max(0.0, (rms(chunk) - floor) / (floor * 10 + 200))))

    def poll(self):
        try:
            return self.inbox.get_nowait()
        except queue.Empty:
            return None


# --------------------------------------------------------------------------
# Main loop
# --------------------------------------------------------------------------
QUIT_WORDS = {"goodbye", "good bye", "bye jarvis", "goodbye jarvis", "shut down", "exit jarvis",
              "go to sleep", "jarvis go to sleep", "jarvis shut down"}
RESET_WORDS = {"forget everything", "new conversation", "start over"}


def phrase(text):
    """'Hey Jarvis, goodbye!' -> 'goodbye' (so 'how do I say goodbye in French' does NOT quit)."""
    t = re.sub(r"[^\w\s']", " ", text.lower())
    t = re.sub(r"^\s*(hey|ok|okay)?\s*(jarvis)?\s*", "", t)
    return re.sub(r"\s+", " ", t).strip()


def handle(text, brain, voice, ui):
    """Returns False when it's time to quit."""
    ui.emit("you", text=text)
    lower = phrase(text)

    def reply(line):
        ui.emit("jarvis", text=line)
        ui.state("speaking")
        voice.say(line)

    if lower in QUIT_WORDS:
        reply(f"Goodbye, {USER_NAME}.")
        ui.emit("jarvis_end")
        ui.state("offline")
        return False
    if lower in RESET_WORDS:
        brain.reset()
        reply("Done. Fresh start.")
        ui.emit("jarvis_end")
        ui.state("idle")
        return True

    # 1) Is it a command? (open Chrome, search YouTube, volume up...) - instant, no AI
    try:
        import commands
        action = commands.try_run(text)
    except Exception as e:
        action = None
        print(f"[command error] {e}")
    if action:
        print(f"Jarvis: {action}")
        ui.emit("jarvis_start")
        reply(action)
        ui.emit("jarvis_end")
        ui.state("idle")
        return True

    # 2) Otherwise ask the AI brain
    print("Jarvis: ", end="", flush=True)
    ui.state("thinking")
    ui.emit("jarvis_start")

    def speak(sentence):
        line = clean_for_speech(sentence)
        if not line:
            return
        print(line, end=" ", flush=True)
        reply(line)

    try:
        brain.ask(text, speak)
    except Exception as e:
        print(f"\n[error] {e}")
        ui.emit("sys", text=f"Error: {e}")
        reply("Sorry, something went wrong with my brain. Check the window for details.")
    ui.emit("jarvis_end")
    ui.state("idle")
    print()
    return True


def main():
    parser = argparse.ArgumentParser(description="Offline Jarvis voice assistant")
    parser.add_argument("--ptt", action="store_true", help="press Enter to talk instead of the wake word")
    parser.add_argument("--text", action="store_true", help="type instead of talk")
    parser.add_argument("--no-ui", action="store_true", help="don't open the HUD window")
    args = parser.parse_args()

    print("Starting Jarvis...")
    ui = UI(enabled=not args.no_ui)
    brain = Brain()
    print("  brain ready (Ollama)")
    voice = Voice()
    print("  voice ready")

    if args.text:
        ui.open_window()
        voice.say("Jarvis online.")
        while True:
            try:
                text = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if text and not handle(text, brain, voice, ui):
                break
        return

    ears = Ears()
    print("  ears ready (Whisper)")
    mic = Mic()
    mic.calibrate()
    wake = None if args.ptt else WakeWord()

    ui.open_window()
    ui.emit("sys", text="All systems online. AI running locally on this PC.")
    voice.say("Jarvis online.")
    prompt = "Press Enter, then speak." if args.ptt else 'Say "Hey Jarvis" (or use the window)...'

    while True:
        try:
            ui.state("idle")
            print(f"\n{prompt}")
            if args.ptt:
                input()
                mic.flush()
                kind, payload = "wake", None
            else:
                kind, payload = wake.wait(mic, ui)

            if kind == "text":  # typed in the window
                print(f"You (typed): {payload}")
                if not handle(payload, brain, voice, ui):
                    break
                continue

            if kind == "talk":
                mic.flush()
            ui.state("listening")
            beep()
            print("Listening...")
            audio = mic.record_utterance(ui)
            beep(660, 80)
            ui.state("hearing")  # Listening ended; transcribing audio, not yet asking the AI.
            text = ears.transcribe(audio)
            if not text:
                msg = (f"Didn't catch that. Loudest sound {mic.last_peak:.0f}, "
                       f"background {mic.noise_floor:.0f}.")
                print(f"({msg} If those are close, check your mic in Windows Sound settings)")
                ui.emit("sys", text=msg)
                continue
            print(f"You: {text}")
            if not handle(text, brain, voice, ui):
                break
            time.sleep(0.2)
            mic.flush()  # don't let Jarvis hear its own voice
        except KeyboardInterrupt:
            break
    ui.state("offline")
    print("Jarvis offline.")


if __name__ == "__main__":
    main()
