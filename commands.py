"""
Jarvis commands - things Jarvis can actually DO on your PC.

These are matched instantly (no AI needed), so they're fast and reliable.
Anything that isn't a command goes to the AI brain as a normal question.

Add your own apps, websites and folders in commands.json - no coding needed.
"""

import ctypes
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import urllib.parse
import webbrowser
from pathlib import Path

HERE = Path(__file__).parent
CONFIG_FILE = HERE / "commands.json"
if not CONFIG_FILE.exists():
    CONFIG_FILE = HERE / "commands.example.json"
HOME = Path.home()

# --------------------------------------------------------------------------
# Built-in shortcuts (you can override/add more in commands.json)
# --------------------------------------------------------------------------
DEFAULT_CONFIG = {
    "browser": "chrome",
    "apps": {
        "chrome": "chrome",
        "google chrome": "chrome",
        "edge": "msedge",
        "vs code": "code",
        "vscode": "code",
        "visual studio code": "code",
        "code": "code",
        "file explorer": "explorer",
        "explorer": "explorer",
        "files": "explorer",
        "notepad": "notepad",
        "calculator": "calc",
        "terminal": "wt",
        "command prompt": "cmd",
        "settings": "ms-settings:",
        "task manager": "taskmgr",
        "snipping tool": "ms-screenclip:",
        "paint": "mspaint",
        "spotify": "spotify:",
        "ollama": "ollama app",
    },
    "websites": {
        "youtube": "https://www.youtube.com",
        "youtube studio": "https://studio.youtube.com",
        "gmail": "https://mail.google.com",
        "email": "https://mail.google.com",
        "google": "https://www.google.com",
        "google drive": "https://drive.google.com",
        "drive": "https://drive.google.com",
        "calendar": "https://calendar.google.com",
        "github": "https://github.com",
        "linkedin": "https://www.linkedin.com",
        "linkedin jobs": "https://www.linkedin.com/jobs",
        "claude": "https://claude.ai",
        "chatgpt": "https://chatgpt.com",
        "netflix": "https://www.netflix.com",
        "amazon": "https://www.amazon.com",
        "figma": "https://www.figma.com",
    },
    "folders": {
        "documents": str(HOME / "Documents"),
        "downloads": str(HOME / "Downloads"),
        "desktop": str(HOME / "Desktop"),
        "pictures": str(HOME / "Pictures"),
        "videos": str(HOME / "Videos"),
        "music": str(HOME / "Music"),
        "jarvis": str(HERE),
        "jarvis folder": str(HERE),
    },
    "search_engines": {
        "google": "https://www.google.com/search?q={}",
        "youtube": "https://www.youtube.com/results?search_query={}",
        "github": "https://github.com/search?q={}",
        "amazon": "https://www.amazon.com/s?k={}",
        "maps": "https://www.google.com/maps/search/{}",
    },
}


def load_config():
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    if CONFIG_FILE.exists():
        try:
            user = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            for key, val in user.items():
                if isinstance(val, dict) and isinstance(cfg.get(key), dict):
                    cfg[key].update({k.lower(): v for k, v in val.items()})
                elif not key.startswith("_"):
                    cfg[key] = val
        except Exception as e:
            print(f"  (couldn't read commands.json: {e})")
    return cfg


CONFIG = load_config()


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def normalize(text):
    t = text.lower().strip()
    t = re.sub(r"[.!?,]+$", "", t).strip()
    t = re.sub(r"^((?:hey|hi|hello|ok|okay|yo)[,\s]+)?jarvis[,\s]*", "", t)
    t = re.sub(r"^(can you |could you |would you |will you |please |i want you to |go ahead and )+", "", t)
    t = re.sub(r"\s+please$", "", t)
    t = re.sub(r"^(the |my )(?=(chrome|edge|calculator|notepad|terminal|settings|task manager)\b)", "", t)
    return t.strip()


SAFE_URL = re.compile(r"^https?://[A-Za-z0-9.-]+(?::\d+)?(?:/[A-Za-z0-9\-._~%!$'()*+,;=:@/?#]*)?$")


def find_exe(name):
    """Resolve a program name ("chrome", "code") to a full path, or None."""
    found = shutil.which(name)
    if found:
        return found
    try:  # Windows "App Paths" registry (where Chrome, Edge, etc. register)
        import winreg
        for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
            try:
                key = rf"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{name}.exe"
                with winreg.OpenKey(hive, key) as k:
                    path = winreg.QueryValue(k, None)
                    if path and Path(path.strip('"')).exists():
                        return path.strip('"')
            except OSError:
                pass
    except ImportError:
        pass
    return None


def start(target):
    """Launch an app name, URI (ms-settings:), folder or file - WITHOUT a shell.

    No shell means nothing in the text can be run as an extra command
    (e.g. "notepad & del ..." is just a weird app name that won't be found).
    """
    if re.match(r"^[a-z][a-z0-9+.-]*:", target) and not re.match(r"^[a-z]:\\", target, re.I):
        os.startfile(target)            # protocol URIs like ms-settings: or spotify:
        return
    exe = find_exe(target)
    if exe:
        subprocess.Popen([exe], close_fds=True)
    else:
        os.startfile(target)            # lets Windows resolve it, still no shell


def open_url(url):
    """Open a web address in the configured browser. Rejects anything that isn't a plain URL."""
    if not SAFE_URL.match(url):
        raise ValueError("that doesn't look like a normal web address")
    exe = find_exe(CONFIG.get("browser", "chrome"))
    if exe:
        subprocess.Popen([exe, url], close_fds=True)
    else:
        webbrowser.open(url)            # fall back to the default browser


def start_menu_lookup(name):
    """Find an installed app by its Start Menu shortcut name."""
    roots = [
        Path(os.environ.get("APPDATA", "")) / "Microsoft/Windows/Start Menu/Programs",
        Path(os.environ.get("PROGRAMDATA", "C:/ProgramData")) / "Microsoft/Windows/Start Menu/Programs",
    ]
    want = name.lower().replace(" ", "")
    best = None
    for root in roots:
        if not root.exists():
            continue
        for lnk in root.rglob("*.lnk"):
            stem = lnk.stem.lower()
            flat = stem.replace(" ", "")
            if "uninstall" in flat:
                continue
            if flat == want:
                return lnk
            if want in flat and (best is None or len(stem) < len(best.stem)):
                best = lnk
    return best


def press_key(vk, times=1):
    for _ in range(times):
        ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
        ctypes.windll.user32.keybd_event(vk, 0, 2, 0)


PROTECTED_PROCESSES = {
    "explorer.exe", "svchost.exe", "winlogon.exe", "csrss.exe", "lsass.exe", "services.exe",
    "system.exe", "smss.exe", "wininit.exe", "dwm.exe", "python.exe", "pythonw.exe",
    "cmd.exe", "conhost.exe", "windowsterminal.exe", "ollama.exe", "ollama app.exe",
}

VK_VOLUME_MUTE, VK_VOLUME_DOWN, VK_VOLUME_UP = 0xAD, 0xAE, 0xAF
VK_MEDIA_NEXT, VK_MEDIA_PREV, VK_MEDIA_PLAY_PAUSE = 0xB0, 0xB1, 0xB3

PROCESS_NAMES = {
    "chrome": "chrome.exe", "google chrome": "chrome.exe", "edge": "msedge.exe",
    "vs code": "Code.exe", "vscode": "Code.exe", "code": "Code.exe",
    "notepad": "notepad.exe", "spotify": "Spotify.exe", "calculator": "CalculatorApp.exe",
    "paint": "mspaint.exe",
}


# --------------------------------------------------------------------------
# The command handlers. Each returns what Jarvis should say, or None.
# --------------------------------------------------------------------------
def cmd_search(t):
    m = re.match(r"^(?:search|look up|google)\s+(?:(\w+)\s+)?(?:for\s+)?(.+)$", t)
    m2 = re.match(r"^search (?:for )?(.+?) on (\w+)$", t)
    if m2 and m2.group(2) in CONFIG["search_engines"]:
        query, engine = m2.group(1), m2.group(2)
    elif m:
        engine, query = (m.group(1) or "google"), m.group(2)
        if t.startswith("google "):
            engine, query = "google", t[len("google "):]
        if engine not in CONFIG["search_engines"]:
            query, engine = f"{engine} {query}".strip(), "google"
    else:
        return None
    query = re.sub(r"^for\s+", "", query).strip()
    if not query:
        return None
    url = CONFIG["search_engines"][engine].format(urllib.parse.quote_plus(query))
    open_url(url)
    return f"Searching {engine.title()} for {query}."


def cmd_play(t):
    m = re.match(r"^play\s+(.+?)(?:\s+on youtube)?$", t)
    if not m or m.group(1) in ("music", "", "it"):
        return None
    q = m.group(1)
    open_url(CONFIG["search_engines"]["youtube"].format(urllib.parse.quote_plus(q)))
    return f"Pulling up {q} on YouTube."


def cmd_open(t):
    m = re.match(r"^(?:open|launch|start|run|go to|pull up|bring up|show me|take me to)\s+(?:up\s+)?(.+)$", t)
    if not m:
        return None
    target = m.group(1).strip()
    target = re.sub(r"\s+(app|application|program|for me|website|site|page)$", "", target)
    target = re.sub(r"^(the|a)\s+", "", target)

    # folders ("open downloads", "open my documents folder")
    folder_key = re.sub(r"^my\s+", "", target)
    folder_key = re.sub(r"\s+folder$", "", folder_key)
    if folder_key in CONFIG["folders"]:
        os.startfile(CONFIG["folders"][folder_key])
        return f"Opening your {folder_key} folder."

    # websites
    for key in (target, re.sub(r"^my\s+", "", target)):
        if key in CONFIG["websites"]:
            open_url(CONFIG["websites"][key])
            return f"Opening {key}."

    # apps
    key = re.sub(r"^my\s+", "", target)
    if key in CONFIG["apps"]:
        app = CONFIG["apps"][key]
        if app == "ollama app":
            lnk = start_menu_lookup("ollama")
            if lnk:
                os.startfile(str(lnk))
                return "Opening Ollama."
        start(app)
        return f"Opening {key}."

    # a raw website like "open reddit.com"
    site = target.replace(" dot ", ".").replace(" ", "")
    if re.match(r"^[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}(/[\w\-./?=&%#]*)?$", site):
        open_url("https://" + site)
        return f"Opening {site}."

    # anything installed on the PC (searches your Start Menu)
    lnk = start_menu_lookup(key)
    if lnk:
        os.startfile(str(lnk))
        return f"Opening {lnk.stem}."

    if len(target.split()) > 3:
        return None  # probably a sentence ("start a timer for ten minutes") - let the AI answer
    return f"I couldn't find an app called {target}. You can add it to commands dot json."


def cmd_close(t):
    m = re.match(r"^(?:close|quit|exit|kill)\s+(?:the\s+|my\s+)?(.+?)(?:\s+app)?$", t)
    if not m or m.group(1) in ("jarvis",):
        return None
    name = m.group(1)
    exe = PROCESS_NAMES.get(name) or (name.replace(" ", "") + ".exe")
    if not re.match(r"^[\w.-]+\.exe$", exe) or exe.lower() in PROTECTED_PROCESSES:
        return f"I won't close {name}. It's part of Windows or Jarvis itself."
    r = subprocess.run(["taskkill", "/im", exe], capture_output=True, text=True)
    if r.returncode == 0:
        return f"Closing {name}."
    return f"{name.title()} doesn't seem to be open."


def cmd_volume(t):
    if re.search(r"\b(unmute|mute)\b", t) and ("volume" in t or "sound" in t or t in ("mute", "unmute")):
        press_key(VK_VOLUME_MUTE)
        return "Done."
    if re.search(r"(volume|sound|turn it)\s*(up|louder)|louder|turn up the (volume|sound)|increase (the )?volume", t):
        press_key(VK_VOLUME_UP, 5)
        return "Turning it up."
    if re.search(r"(volume|sound|turn it)\s*(down|quieter)|quieter|turn down the (volume|sound)|decrease (the )?volume|lower (the )?volume", t):
        press_key(VK_VOLUME_DOWN, 5)
        return "Turning it down."
    return None


def cmd_media(t):
    if t in ("pause", "play", "resume", "pause music", "play music", "resume music", "pause the music", "stop the music"):
        press_key(VK_MEDIA_PLAY_PAUSE)
        return "Done."
    if t in ("next", "next song", "skip", "skip song", "next track", "skip this song"):
        press_key(VK_MEDIA_NEXT)
        return "Skipping."
    if t in ("previous", "previous song", "last song", "go back a song"):
        press_key(VK_MEDIA_PREV)
        return "Going back."
    return None


def cmd_system(t):
    if re.search(r"\block (the |my )?(computer|pc|screen)\b|^lock$", t):
        subprocess.Popen("rundll32.exe user32.dll,LockWorkStation")
        return "Locking your computer."
    if re.search(r"(take a |take |grab a )?screenshot|screen ?shot", t):
        start("ms-screenclip:")
        return "Select the area you want to capture."
    # Catch natural time/date variations immediately without involving the language model.
    # Questions such as "what time is it in Tokyo" still go to conversational AI.
    if re.search(r"^(?:tell me |do you know )?(what time is it|what time it is|what's the time|what is the time|"
                 r"the time|time)(?: (?:right now|now|currently|please|jarvis))*$", t):
        return "It's " + dt.datetime.now().strftime("%I:%M %p").lstrip("0") + "."
    if re.search(r"^(?:tell me )?(what's the date|what is the date|what day is it|what's today|today's date|"
                 r"the date)(?: (?:today|right now|now|please|jarvis))*$", t):
        return "Today is " + dt.datetime.now().strftime("%A, %B %d").replace(" 0", " ") + "."
    return None


def cmd_help(t):
    if re.search(r"^(help|what can you do|what are your commands|commands|list commands)$", t):
        return ("I can open apps, websites and folders, search Google or YouTube, play videos, "
                "close apps, control the volume and music, take screenshots, lock your computer, "
                "and answer questions. Try saying: open Chrome, or search YouTube for lo-fi beats.")
    return None


HANDLERS = [cmd_help, cmd_system, cmd_volume, cmd_media, cmd_search, cmd_play, cmd_close, cmd_open]


def try_run(text):
    """Return what Jarvis should say if `text` is a command, else None."""
    t = normalize(text)
    # allow chaining: "open chrome and youtube" -> two commands
    parts = [t]
    m = re.match(r"^(open|launch|start)\s+(.+?)\s+and\s+(?:open\s+)?(.+)$", t)
    if m:
        parts = [f"{m.group(1)} {m.group(2)}", f"{m.group(1)} {m.group(3)}"]
    replies = []
    for p in parts:
        for h in HANDLERS:
            try:
                out = h(p)
            except Exception as e:
                out = f"That command hit an error: {e}"
            if out:
                replies.append(out)
                break
    return " ".join(replies) if replies else None
