# Release readiness

**Current status: PUBLIC SOURCE RELEASE (SOURCE ONLY; INDEPENDENT CLEAN WINDOWS INSTALL UNVERIFIED).**

## Code and quality gates

- [x] Remove personal `commands.json`, virtual environments, model binaries and recordings from tracked source.
- [x] Add loopback endpoint token, Host and Origin checks, including `/events`, and regression tests.
- [x] Provide clear setup and safety documentation with authentic interface imagery.
- [x] Provide an explicit source-only package checker (no automatic publishing).
- [x] **61 of 61 isolated checks PASS on Windows Server 2025 and Ubuntu 24.04**, Python 3.12, on the validated source branch (47 prior tests + 11 listening/voice tests + 3 release-hygiene checks). [Verified CI run](https://github.com/tabitha-dev/jarvis-local-ai/actions/runs/39523115430). The core tests include voice selection and fallback; tests install only development/test dependencies and **do not** download local AI models or verify microphone/speaker operation.
- [x] **Windows dependency lock supplied:** the October 20 Windows 11 `requirements.lock.txt` generated with `update_lock.bat` is committed. The maintainer reports `pip check` passed on that working setup. A second clean-PC installation remains untested.
- [x] User-reported Windows 11 *fresh-folder* end-to-end test on the creator's existing computer (2026-10-20): speech recognition for “Jarvis,” audible voice reply, and app launch. Python/Ollama were already installed; this is **not** an independent clean-PC test.
- [ ] **Recommended follow-up (not a condition for a disclosed source release):** complete an independent clean Windows 10/11 installation where Python and Ollama were not previously installed. The current Windows 11 fresh-folder test was on a PC that already had both; do not claim a clean-PC installation was verified.
- [ ] Review Windows command allowlists, local HTTP routes and setup scripts on a real PC.
- [ ] Review the [pre-public audit and handoff](docs/PREPUBLIC_RELEASE_AUDIT.md), then complete privacy-safe test evidence before a source-only public release.

## Licensing and publication gates

- [x] Owner-provided release notes requested **MIT** for original project code; MIT `LICENSE` added. Third-party models and voices are **not** included in this grant.
- [x] Third-party license review completed 2026-10-19: [docs/LICENSE_REVIEW.md](docs/LICENSE_REVIEW.md). Not legal advice.
- [x] Remove Alan from public setup, use Windows as default and offer optional Cori, with user-local voice selection stored in Git-ignored commands.json.
- [ ] Owner decisions from that review: Cori model/output rights (optional voice), commercial rights for any explicitly enabled wake-word use, and source-only distribution.
- [x] Make pretrained `hey_jarvis` **opt-in**. The ordinary hands-free “Jarvis, …” startup uses faster-whisper without loading or downloading that CC BY-NC-SA noncommercial model; TALK and typing remain available. The explicit `--wake` option still requires users to follow its license.
- [x] Prepare public source release notes and a GitHub source ZIP path. The independent clean-PC installation remains unverified and disclosed.
- [ ] Owner approval and actual GitHub visibility switch to Public. This release-preparation branch alone does not publish the repository.
- [ ] Update the YouTube description only after the release URL actually works when signed out.

## Evidence boundary

A passing command/unit-test suite is **not proof** of a working Windows microphone, downloaded model, wake-word listener, complete offline operation or safe public deployment. The install sequence shown in the associated video is an explicitly **simulated walkthrough**; the real Jarvis interaction clip is separately identified.

[← README](README.md) · [Windows setup](docs/INSTALL_WINDOWS.md)
