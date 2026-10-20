# Release readiness

**Current status: PRIVATE, PRE-RELEASE, NO PUBLIC DOWNLOAD.**

## Code and quality gates

- [x] Remove personal `commands.json`, virtual environments, model binaries and recordings from tracked source.
- [x] Add loopback endpoint token, Host and Origin checks, including `/events`, and regression tests.
- [x] Provide clear setup and safety documentation with authentic interface imagery.
- [x] Provide an explicit source-only package checker (no automatic publishing).
- [x] **33 of 33 isolated source/unit tests PASS on Windows Server 2025 and Ubuntu 24.04**, Python 3.12, on the merged `main` commit. [Verified CI run](https://github.com/tabitha-dev/jarvis-local-ai/actions/runs/39359451513). Tests install import dependencies but **do not** download local AI models or verify microphone/speaker operation.
- [ ] On the working Windows PC run `update_lock.bat` after successful setup, validate the generated `requirements.lock.txt` with `pip check`, and commit the tested versions. **Lock file not yet supplied; unpinned installs can drift.**
- [ ] Complete and record the [fresh Windows verification checklist](docs/WINDOWS_RELEASE_TEST.md), including an **independent clean Windows 10/11 setup** with a working microphone, output speaker and actual model downloads.
- [ ] Review Windows command allowlists, local HTTP routes and setup scripts on a real PC.

## Licensing and publication gates

- [x] Owner-provided release notes requested **MIT** for original project code; MIT `LICENSE` added. Third-party models and voices are **not** included in this grant.
- [x] Third-party license review completed 2026-10-19: [docs/LICENSE_REVIEW.md](docs/LICENSE_REVIEW.md). Not legal advice.
- [ ] Owner decisions from that review: default voice (`alan` rights unclear; `cori` uses public-domain source recordings but model/output rights require review), wake-word use in monetized videos, source-only distribution.
- [ ] Create release notes and a verified source ZIP after clean-install testing.
- [ ] Explicitly approve changing repository visibility to Public and distributing code.
- [ ] Update the YouTube description only after the release URL actually works when signed out.

## Evidence boundary

A passing command/unit-test suite is **not proof** of a working Windows microphone, downloaded model, wake-word listener, complete offline operation or safe public deployment. The install sequence shown in the associated video is an explicitly **simulated walkthrough**; the real Jarvis interaction clip is separately identified.

[← README](README.md) · [Windows setup](docs/INSTALL_WINDOWS.md)
