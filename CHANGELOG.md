# Changelog

## Voice preference and beginner setup | October 2026
- Stage 4 of setup now shows a strict numbered voice menu: Windows built-in (default, no download) or optional Piper Cori, with unattended/Enter default to Windows.
- Voice choice is saved atomically in the user-only Git-ignored `commands.json` rather than requiring edits to `jarvis.py`. A missing/broken Cori voice falls back to Windows.
- `change_voice.bat` changes the saved setting later; Alan is excluded from the public menu.

## Pre-release fixes | October 2026
- Third-party license review ([docs/LICENSE_REVIEW.md](docs/LICENSE_REVIEW.md)): the default `alan` voice has no verified open grant; `cori` is documented as an alternative with public-domain source recordings, subject to model-rights verification.
- `tools\windows_test_report.bat` collects a minimal local-only version/status report without raw paths or audio-device names for the fresh Windows install test; the test guide explains how to get a clean environment.
- Windows batch files now use CRLF line endings, enforced by `.gitattributes` (LF-only `.bat` files can make `cmd.exe` miss `goto`/`call` labels).
- `run_jarvis.bat`, `run_tests.bat` and `make_release.bat` pause before exiting, so double-click users can read errors.
- `setup.bat` prefers `requirements.lock.txt` when present. `update_lock.bat` can generate it from a verified Windows environment; **no tested lock file has been supplied yet**.
- `.gitignore` excludes `*.zip` so release archives aren't committed by accident.
- README: real demo GIF and a 3-step Quick start; CONTRIBUTING now matches the MIT license.

## Private release candidate | October 2026

### Voice interaction and visual feedback
- Improved recognition of natural time/date questions so they use the fast command path.
- Added a cyan **HEARING** state for speech-to-text. Amber **PROCESSING** is reserved for local AI inference.
- Added regression tests for instant commands and the updated HUD state flow.

### Security and distribution preparation
- Preserved the authenticated local `/events` stream from the previous security review. The supplied V5 reference copy did not contain this fix and was not copied over the secure implementation.
- Added session authorization and origin regression tests for local HTTP actions and event streaming.
- Hardened Windows setup failure checks and introduced an allowlist-only release packager that refuses output without a chosen LICENSE.
- Added GitHub Actions code-level checks on Windows and Ubuntu; the initial Linux PortAudio dependency issue was fixed.
- Modernized README, authentic HUD screenshot, security, installation and troubleshooting guidance.

**Unverified:** fresh Windows setup, actual microphone/wake-word performance, speaker output and offline-with-Wi-Fi-disabled behavior. Project code now has an MIT LICENSE as requested in the handoff notes; third-party model and voice rights remain pending. No public release has been created.
