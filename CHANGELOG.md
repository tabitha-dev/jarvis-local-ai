# Changelog

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
