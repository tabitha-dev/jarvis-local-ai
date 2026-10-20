# Release readiness — private staging (NOT PUBLIC)

Before making this repository public or putting a download link in YouTube:

- [ ] Choose, verify rights to use, and add a project license. No license has been selected.
- [ ] Verify redistribution/commercial use terms for all pretrained models and Piper voice assets; do not bundle third-party model weights.
- [ ] Perform an independent clean Windows 10/11 setup test, including reboots, winget downloads, checks on failures, voice input/output and local model installation.
- [ ] Review Windows command allow-lists and app-launch behavior, and review local HTTP API threat model, including `/events`, `/say`, `/talk`, DNS rebinding, and local processes.
- [ ] Run unit tests in a real Windows environment with installed dependencies (mocked audio tests alone aren't an integration test).
- [ ] Confirm config contains no personal paths, API credentials, cookies or private files. Do not commit `commands.json`, `.venv`, voice files or model weights.
- [ ] Review YouTube visuals: real footage vs permanently labeled simulated install; never claim Wi-Fi-off demo or fresh Windows validation not actually recorded.
- [ ] Obtain creator approval to change repository visibility, publish download links and create a GitHub release.

Current automatic tests do not demonstrate real microphone, audio output, or fresh-install functionality. This repo remains private and no GitHub release exists.
