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
5. Download the **faster-whisper** and **openWakeWord** assets.
6. Ask Ollama to fetch the configured **Gemma 4** variant.

Each step now includes failure detection. The setup script returns a failure instead of reporting that an incomplete install succeeded. Windows/macOS/Linux behaviors are not interchangeable; this project currently targets Windows.

## Steps

1. Download source (when a release is available) or clone this repository for testing.
2. **Inspect** `setup.bat`, `requirements.txt`, and third-party notices before running a script. Do not blindly bypass Windows SmartScreen.
3. On a **test PC**, open a command prompt in the project directory and run `setup.bat`. A first download can take a while; time varies by internet speed and available CPU/disk.
4. Run `run_tests.bat`. This tests mocked actions and server authorization but **does not** open programs or validate microphone input.
5. If successful, run `run_jarvis.bat`. Check that the HUD opens, typed questions work and the Ollama model replies.
6. For voice testing, use a real microphone, check push-to-talk, the wake word and Piper audio output.
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
