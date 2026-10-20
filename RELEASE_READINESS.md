# Release readiness

**Current status: PRIVATE, PRE-RELEASE, NO PUBLIC DOWNLOAD.**

## Code and quality gates

- [x] Remove personal `commands.json`, virtual environments, model binaries and recordings from tracked source.
- [x] Add loopback endpoint token, Host and Origin checks, including `/events`, and regression tests.
- [x] Provide clear setup and safety documentation with authentic interface imagery.
- [x] Provide an explicit source-only package checker (no automatic publishing).
- [x] Previous Windows **and** Ubuntu GitHub Actions code-level checks passed (27 tests). Current V5-combined candidate requires fresh 33-test CI confirmation; neither suite downloads models or checks microphone hardware.
- [ ] Complete and record the [fresh Windows verification checklist](docs/WINDOWS_RELEASE_TEST.md), including an **independent clean Windows 10/11 setup** with a working microphone, output speaker and actual model downloads; record results using [Windows validation checklist](docs/WINDOWS_RELEASE_TEST.md).
- [ ] Review Windows command allowlists, local HTTP routes and setup scripts on a real PC.

## Licensing and publication gates

- [x] Owner-provided release notes requested **MIT** for original project code; MIT `LICENSE` added. Third-party models and voices are **not** included in this grant.
- [ ] Validate pretrained wake-word models and Piper voice license implications, particularly noncommercial model restrictions.
- [ ] Create release notes and a verified source ZIP after clean-install testing.
- [ ] Explicitly approve changing repository visibility to Public and distributing code.
- [ ] Update the YouTube description only after the release URL actually works when signed out.

## Evidence boundary

A passing command/unit-test suite is **not proof** of a working Windows microphone, downloaded model, wake-word listener, complete offline operation or safe public deployment. The install sequence shown in the associated video is an explicitly **simulated walkthrough**; the real Jarvis interaction clip is separately identified.

[← README](README.md) · [Windows setup](docs/INSTALL_WINDOWS.md)
