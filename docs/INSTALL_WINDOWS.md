# Windows setup and first-run checks

> **Pre-release walkthrough, not a verified clean-install result.** Read the scripts and test in a controlled environment first.

## Prerequisites

- Windows 10/11 with `winget` (App Installer) available and working.
- Internet for Python, packages, Ollama, voice and model downloads.
- Microphone and speakers if you intend to test voice. You can try `--text` without them.
- At least 8 GB RAM; 16 GB recommended. Model downloads and disk usage vary.

## What `setup.bat` does

1. Locate or install **Python 3.12**.
2. Locate or install **Ollama**; attempt to start its local service and confirm the API responds.
3. Create `.venv`, install Python requirements and copy `commands.example.json` to `commands.json`.
4. Download the configured **Piper** voice files.
5. Download the **faster-whisper** speech model for transcription and default hands-free “Jarvis” name recognition only. The optional noncommercial `hey_jarvis` wake-word model is not downloaded during setup.
6. Ask Ollama to fetch the configured **Gemma 4** variant.

Each step now includes failure detection. The setup script returns a failure instead of reporting that an incomplete install succeeded. Windows/macOS/Linux behaviors are not interchangeable; this project currently targets Windows.

## Dependency versions

`requirements.txt` lists the packages needed for a development installation. The installer will prefer `requirements.lock.txt` when the maintainer has generated and committed one from a **verified working Windows installation**. No such lock file has been provided yet; an install without it can resolve different package versions over time. On the known-working PC, run `update_lock.bat` after confirming the app and tests work, review `requirements.lock.txt`, then test it on a separate clean Windows environment before a public release.

## Choose your voice

During Stage 4, the **numbered menu** offers:

- **1 — Windows built-in voice (default):** no separate voice model download. Press **Enter**, choose 1, or wait 25 seconds to choose this automatically.
- **2 — Cori:** optional British female Piper voice (`en_GB-cori-medium`), trained with public-domain source recordings. Review the model/output usage terms in [license review](LICENSE_REVIEW.md) before commercial use.

The selection is stored as `"voice": "windows"` or `"voice": "piper:en_GB-cori-medium"` in your *private* Git-ignored `commands.json`, not `jarvis.py`. Only those choices are accepted; there is no arbitrary voice-name input. If the Cori download fails, setup reports a failure and does not overwrite your prior choice. If the chosen model is missing or cannot load later, Jarvis falls back to Windows text-to-speech. To switch later, run `change_voice.bat` and restart Jarvis. **Alan is not part of the public menu.**

## Steps

1. Download source (when a release is available) or clone this repository for testing.
2. **Inspect** `setup.bat`, `requirements.txt`, and third-party notices before running a script. Do not blindly bypass Windows SmartScreen.
3. On a **test PC**, open a command prompt in the project directory and run `setup.bat`. A first download can take a while; time varies by internet speed and available CPU/disk.
4. Run `run_tests.bat`. This tests mocked actions and server authorization but **does not** open programs or validate microphone input.
5. If successful, run `run_jarvis.bat`. Check that the HUD opens, typed questions work and the Ollama model replies.
6. For voice testing, use a real microphone, confirm “Jarvis, what time is it?” and “Hi Jarvis, open Notepad,” verify HUD TALK, and check Windows SAPI voice output. Test the optional `--wake` mode only when you have reviewed its noncommercial license.
7. Repeat all steps on a **clean Windows 10 or 11 installation** before approving a first public release.

## Basic checks

```bat
py -3.12 --version
ollama --version
ollama list
.venv\Scripts\python.exe -m unittest discover tests -v
.venv\Scripts\python.exe jarvis.py --text
```

> Running the automated tests is not a substitute for actually launching the application and exercising voice, downloads, app commands and networking.

## Downloading models and licenses

Your computer downloads third-party assets during setup. They are not packaged in this repository. Pretrained wake-word models may be limited to non-commercial use, and each voice/model may have separate terms. Review [third-party notices](../THIRD_PARTY_NOTICES.md).

[← README](../README.md) · [Troubleshooting](TROUBLESHOOTING.md)
