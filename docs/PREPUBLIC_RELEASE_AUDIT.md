# Pre-public release audit | 2026-10-20

**Status: HOLD — private repository. This is a pre-release readiness report, not permission to publish.**

## Verified remotely

- **Latest CI:** 61 of 61 isolated checks PASS on Windows Server 2025 and Ubuntu 24.04, Python 3.12 (47 prior functional/unit checks, 11 listening/voice checks and three release-hygiene checks), [run 39502432199](https://github.com/tabitha-dev/jarvis-local-ai/actions/runs/39518410655).
- **Source repository:** `main` currently has a project-authored MIT license, README, third-party notices, security guidance, voice chooser (Windows default / optional Cori), pre-release installer and source-only packaging allowlist.
- **Local HTTP protections:** token, origin and host checks are implemented and tested at source level. No formal penetration test has been performed.
- **Source hygiene:** private `commands.json`, virtual environments, models and media are absent from the reviewed tracked file tree. GitHub Actions additionally checks for accidentally tracked private/config/media files; this is not a full secret-history or binary forensics scan.
- **Video:** separately approved creator video has been produced, but does not prove Windows clean-install readiness and does not grant permission to publish the source.

## Mandatory gates before switching repository visibility to Public

- [ ] **Future independent clean-PC verification (not a prerequisite for a transparently labeled source release):** test `setup.bat` on Windows 10/11 without preinstalled Python/Ollama/models. Follow [Windows test checklist](WINDOWS_RELEASE_TEST.md). Real hardware and actual downloads **cannot** be validated by mocked CI tests.
- [ ] **Hardware and runtime:** test Windows default TTS, actual microphone and speakers, optional Cori selection and fallback, browser commands, HUD, typed prompt and local Ollama response. Record truthful PASS/FAIL results.
- [x] **Windows lock supplied:** the working Windows 11 machine generated `requirements.lock.txt` with `update_lock.bat`; reported `pip check` success. Dependency versions are committed, with Windows-only markers. Future independent Windows clean install is still recommended.
- [x] **Wake-word default behavior:** regular startup recognizes “Jarvis, …” locally using faster-whisper; TALK and typing remain available. Installer no longer downloads `hey_jarvis` automatically. The pretrained wake word is only fetched and used when a user explicitly starts with `--wake`; its **CC BY-NC-SA 4.0 noncommercial license still applies** and requires separate authorization for commercial usage. Guarded by `tests/test_listen_mode.py`.
- [ ] **Voice rights:** Windows built-in TTS is the default and Alan has been excluded. Optional Cori's public-domain **training recordings alone do not establish** all voice-model/output/commercial rights. Verify those terms before promoting a monetized voice demo or distributing outputs.
- [ ] **Real Windows safety review:** confirm command allowlists, install scripts and loopback HUD behavior on Windows, without enabling unsafe external access or bypassing security warnings. Scrub personal paths and any private settings from shareable artifacts.
- [ ] **Release package:** inspect source-only ZIP from `make_release.bat` / `tools/package_release.py`; no pretrained model, voice binary, local config, `.venv`, chat transcript, personal logs, API keys, nor unauthorized recordings.
- [ ] **Owner approval:** review and approve the public MIT code release, model/voice licensing decisions, exact release files, and GitHub visibility change. Do **not** publish this repository, create a public release or update YouTube download links before this step.

## Test handoff for a real Windows PC

1. Follow [the independent Windows test guide](WINDOWS_RELEASE_TEST.md), preferably on a second computer with permission. Record the OS, Python/Ollama versions, whether the machine had Python/Ollama already, and a PASS/FAIL per checklist item.
2. Run `tools\\windows_test_report.bat` **locally** after installation. Open the resulting `windows-test-report.txt` and remove anything you do not want shared. The report intentionally avoids computer/user names but is still reviewed before upload.
3. Run `update_lock.bat` **only after** the environment passes; review `requirements.lock.txt` before committing.
4. Provide the redacted report and PASS/FAIL notes for review. Do not send raw personal logs or access tokens. The maintainer can then address failures in the existing private repository.
5. Only after the last gate is complete and owner explicitly approves public release, change repository visibility and verify the download while signed out.

**Until those checks are completed, the correct external description is “private pre-release prototype with 56 passing isolated checks”, not “publicly installation-tested” or “commercially cleared.”**
