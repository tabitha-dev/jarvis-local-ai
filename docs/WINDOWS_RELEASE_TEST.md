# Real Windows release verification

> **Owner/manual checklist. This has NOT been completed.** GitHub-hosted unit-test jobs do not perform this full installation and hardware test.

## Environment (record after testing)

- Windows edition/version: ___________________
- Clean installation / new Windows profile: ___________________
- CPU and RAM: ___________________
- Python 3.12 / Ollama versions: ___________________
- Microphone and speaker types: ___________________
- Test date and tester: ___________________

## Steps to record as PASS / FAIL

- [ ] Start with a new Windows 10 or 11 environment with no preinstalled Python/Ollama/Jarvis state; confirm `winget` works.
- [ ] Download or clone the **private** candidate source and inspect `setup.bat` yourself. Never bypass SmartScreen blindly.
- [ ] Run `setup.bat`. Confirm each of the six numbered stages completes, and simulate/observe a failure so the script exits non-zero without a false success message.
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
- [ ] Re-read [model and voice rights](../THIRD_PARTY_NOTICES.md); confirm intended commercial/redistribution use.
- [ ] Owner explicitly approves code license, public visibility and release artifact.

## Report

For each failed step, record: command, expected result, actual result, and a *redacted* log. Avoid uploading usernames, home paths, secrets, audio recordings, local addresses beyond loopback, and Jarvis conversation contents.

**Release decision:** ☐ Hold ☐ Ready after creator approval

[← README](../README.md) · [Release checklist](../RELEASE_READINESS.md)
