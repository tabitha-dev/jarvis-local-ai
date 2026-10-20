# Release readiness

**Current status: PRIVATE, PRE-RELEASE, NO PUBLIC DOWNLOAD.**

## Code and quality gates

- [x] Remove personal `commands.json`, virtual environments, model binaries and recordings from tracked source.
- [x] Add loopback endpoint token, Host and Origin checks, including `/events`, and regression tests.
- [x] Provide clear setup and safety documentation with authentic interface imagery.
- [x] Provide an explicit source-only package checker (no automatic publishing).
- [ ] Observe a green Windows GitHub Actions test run using installed test dependencies.
- [ ] Perform an **independent clean Windows 10/11 setup** with a working microphone, output speaker and actual model downloads.
- [ ] Review Windows command allowlists, local HTTP routes and setup scripts on a real PC.

## Licensing and publication gates

- [ ] Creator selects project source license and confirms rights (e.g., MIT or Apache-2.0, if appropriate). Do not assume one.
- [ ] Validate pretrained wake-word models and Piper voice license implications, particularly noncommercial model restrictions.
- [ ] Create release notes and a verified source ZIP after clean-install testing.
- [ ] Explicitly approve changing repository visibility to Public and distributing code.
- [ ] Update the YouTube description only after the release URL actually works when signed out.

## Evidence boundary

A passing command/unit-test suite is **not proof** of a working Windows microphone, downloaded model, wake-word listener, complete offline operation or safe public deployment. The install sequence shown in the associated video is an explicitly **simulated walkthrough**; the real Jarvis interaction clip is separately identified.

[← README](README.md) · [Windows setup](docs/INSTALL_WINDOWS.md)
