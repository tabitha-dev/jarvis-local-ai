# Real Windows release verification

> **Owner/manual checklist. This has NOT been completed.** GitHub-hosted unit-test jobs do not perform this full installation and hardware test.

## Environment (record after testing)

- Windows edition/version: ___________________
- Clean installation / new Windows profile: ___________________
- CPU and RAM: ___________________
- Python 3.12 / Ollama versions: ___________________
- Microphone and speaker types: ___________________
- Test date and tester: ___________________

## How to get a clean Windows environment

Your own Windows profile already has Python, Ollama, the models and the `.venv` from development, so testing there proves nothing new. Use one of these, best first:

1. **A second PC or laptop** (a friend's or family member's, with permission). This is the truest "viewer" test.
2. **A new local Windows user account** on your PC (Settings → Accounts → Other users → Add account → "I don't have this person's sign-in information" → "Add a user without a Microsoft account"). It works on Windows Home. Some components are installed per-user, but machine-wide Python/Ollama services, PATH entries, caches or models may remain available across accounts. Check what is actually preinstalled before calling the account clean. It still shares your hardware and drivers, so record it as "new profile, same PC".
3. **Windows Sandbox** (Pro/Enterprise only) is **not** recommended: the availability of `winget`, audio, network access and GPU functionality varies, so the current installer may not work in it, and it throws away the multi-GB downloads when it closes.

In the clean environment:

- Download the repo as a ZIP from GitHub (don't copy your working folder: it contains `.venv`, voices and `commands.json`).
- **Screen-record the whole install** (Snipping Tool → Record, or Win + Alt + R with Xbox Game Bar). This is real footage that can replace the simulated install in the video.
- When done, double-click `tools\windows_test_report.bat`. It writes a minimal local `windows-test-report.txt` containing OS/Python/Ollama version information, presence of the expected AI model, voice-file availability, audio-device count, and package/test pass/fail results. It deliberately excludes raw diagnostic logs, Windows account names, computer names and audio device names. Read it before sharing; if anything still looks private, do not upload it. For failures, run the relevant command locally and redact its output separately.
- Afterwards you can delete the test account to free the disk space (Settings → Accounts → Other users → Remove).

## Steps to record as PASS / FAIL

- [ ] Start with a new Windows 10 or 11 environment with no preinstalled Python/Ollama/Jarvis state; confirm `winget` works.
- [ ] Download or clone the **private** candidate source and inspect `setup.bat` yourself. Never bypass SmartScreen blindly.
- [ ] Run `setup.bat`. Confirm each of the six numbered stages completes, and simulate/observe a failure so the script exits non-zero without a false success message.
- [ ] From a verified Windows environment, run `update_lock.bat`, review `requirements.lock.txt` for reproducible versions and sensitive local paths, commit the lock file, and repeat a clean install using it.
- [ ] Verify `ollama list` includes the configured Gemma model, and the Piper, Whisper and wake-word assets exist.
- [ ] Run `run_tests.bat` with real Python dependencies; record the final reported test count and result.
- [ ] Run `python jarvis.py --text` and ask a simple question; confirm the local model replies.
- [ ] Run `run_jarvis.bat`; confirm the HUD opens without exposing a LAN port.
- [ ] Type “what time is it?” in the HUD and confirm the response.
- [ ] Test microphone selection, push-to-talk, wake-word activation and playback on the real device.
- [ ] Use a **safe example** such as “open Notepad”; check that the expected application actually opens, and test URL and volume commands.
- [ ] Test controlled loss of network **after** downloads: local inference vs browser actions are documented correctly. Do not claim an offline test if not performed.
- [ ] Confirm regular user permissions are sufficient or document any prompts and limitations.
- [ ] Verify no private config, model weights, voice assets, recordings, API keys or virtual environments enter the source ZIP.
- [ ] Re-read [model and voice rights](../THIRD_PARTY_NOTICES.md) and the [license review](LICENSE_REVIEW.md); confirm the voice and wake-word decisions.
- [ ] Owner explicitly approves code license, public visibility and release artifact.

## Report

For each failed step, record: command, expected result, actual result, and a *redacted* log. Avoid uploading usernames, home paths, secrets, audio recordings, local addresses beyond loopback, and Jarvis conversation contents.

**Release decision:** ☐ Hold ☐ Ready after creator approval

[← README](../README.md) · [Release checklist](../RELEASE_READINESS.md)
