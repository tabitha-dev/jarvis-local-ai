# Jarvis: a local AI voice assistant for Windows

> **PRIVATE DEVELOPMENT PREVIEW — NOT A VERIFIED PUBLIC RELEASE.** The source has not been tested on a fresh Windows installation. Please do not treat the setup instructions below as installation proof. The repository will remain private until security, licenses, and fresh-install checks are complete.

Say **"Hey Jarvis"**, ask a question, and a local AI model answers out loud. It can also open apps and websites, search, and control volume and music. It is designed for Windows with local AI. The current code has **not** passed independent end-to-end Windows installation tests. It does not require a cloud AI key for local model responses.

> Built by [Tabitha Dev](https://www.youtube.com/@tabitha-dev). Software Engineering, Made Simple.

## How it works

```
"Hey Jarvis" ─► openWakeWord ─► faster-whisper ─► commands.py ──► runs the command (open Chrome, volume up…)
  (your mic)      wake word      speech → text        │
                                                       └─ not a command ─► Ollama + Gemma 4 ─► Piper speaks the answer
                                         HUD (ui.html) shows every step live
```

- **Commands are instant.** `commands.py` checks for things like "open Chrome" before the AI is involved.
- **Everything else goes to the AI**, which runs on your PC through Ollama, and is spoken back sentence by sentence.
- **The HUD** is one HTML file (SVG + CSS, no frameworks). Python serves it on `127.0.0.1` only and streams state changes with Server-Sent Events.

## What you need

- Windows 10 or 11 with [winget](https://learn.microsoft.com/windows/package-manager/winget/) (built into current Windows)
- 8 GB RAM minimum, 16 GB recommended
- About 10 GB free disk space (the AI model is about 4.5 GB)
- A microphone
- Internet for the one-time setup. After that, the AI conversation runs locally. Opening websites still needs internet.
- A graphics card is **not** required. Everything runs on the CPU by default.

## Install

1. Download this repo (**Code → Download ZIP**) and unzip it, for example to `Documents\jarvis`.
2. **Read `setup.bat` first.** It's short. Only run scripts you've checked.
3. **After reviewing the batch file**, run `setup.bat` on your own test Windows PC. It attempts to install Python 3.12 and Ollama with winget, create a virtual environment, install packages and download models. Some setup commands do not yet halt on every download failure, so verify the final outputs individually.
   - If Ollama opens and asks you to sign up, choose **"No thanks, I'll use Ollama locally."**
   - If Hugging Face prints a yellow "symlinks" warning, read it. It may affect caching and disk usage, and you should not ignore unrelated warnings.
4. If all setup stages succeed, try `run_jarvis.bat`. The HUD should open when Jarvis starts. This has not yet been verified on a fresh Windows install.

The **first** answer after starting can take a minute or more while the model loads into memory. Later answers are faster.

## Using it

Say "Hey Jarvis", wait for the beep, then talk. Or type in the HUD, or click **TALK** to skip the wake word.

| You say | Jarvis does |
| --- | --- |
| "Open Chrome" · "Open VS Code" · "Open Figma" | Opens the app (any installed app, found through your Start Menu) |
| "Open YouTube" · "Open reddit.com" | Opens the site |
| "Open downloads" | Opens the folder |
| "Open Chrome and YouTube" | Does both |
| "Search YouTube for lo-fi beats" · "Google best React libraries" | Searches |
| "Play lo-fi beats" | Searches YouTube for it |
| "Volume up" · "Mute" · "Pause" · "Next song" | Media keys |
| "Take a screenshot" · "Lock my computer" · "What time is it" | System actions |
| "Close Chrome" | Asks the app to close (it won't close Windows itself or Jarvis) |
| "Forget everything" · "Goodbye" | Clears memory · quits |
| Anything else | Asked to the local AI |

Other ways to start it (from a terminal in this folder, after `.venv\Scripts\activate`):

```
python jarvis.py --text     # type instead of talk
python jarvis.py --ptt      # press Enter, then talk (no wake word)
python jarvis.py --no-ui    # console only
```

## Make it yours

- **Shortcuts:** edit `commands.json` (created from `commands.example.json` by setup). Add a name under `apps`, `websites` or `folders`, then restart.
- **Settings:** the top of `jarvis.py` has `USER_NAME`, `OLLAMA_MODEL` (try `gemma4:e4b` on a stronger PC), `WHISPER_MODEL`, `PIPER_VOICE` and `WAKE_THRESHOLD`.
- **Look:** change the colors in the `:root` variables at the top of `ui.html`.

## Troubleshooting

- **"Didn't catch that":** Jarvis prints your loudest sound vs. the background level. If they're close, pick the right mic and raise its level in Windows **Settings → System → Sound → Input**.
- **Wakes up by accident:** raise `WAKE_THRESHOLD` to 0.6–0.7.
- **"Ollama isn't running":** open the Ollama app from the Start Menu, then start Jarvis again.
- **Slow answers:** normal on CPU-only laptops. Try a smaller Whisper model (`tiny.en`) or an NVIDIA GPU.

## Security notes

- The HUD server listens on `127.0.0.1` only. Command requests carry a per-run token plus Host/Origin checks; the event stream also requires its own per-run token and checks Host/Origin. These are defenses against other browser origins, not a guarantee against malicious programs already running on the same PC.
- Apps are launched **without a shell**, and web addresses are validated, so spoken or typed text can't be turned into extra Windows commands.
- Jarvis can open programs on your PC. Don't expose its port to a network, and review `commands.py` before adding new actions.

Run the tests (nothing is actually launched): double-click `run_tests.bat`, or run `python -m unittest discover tests`.

## Licenses

Jarvis's own code: **LICENSE NOT YET SELECTED.** No permission to reuse or redistribute the original source is granted by this private staging repository. Select a license deliberately before any public release.
Third-party models and packages have their own licenses. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). In particular, the openWakeWord pretrained models are **non-commercial** (CC BY-NC-SA 4.0).
