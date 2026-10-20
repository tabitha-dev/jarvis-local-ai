# Third-party license review

> **Status: preliminary source-license review completed; rights and owner decisions still open.** Checked on 2026-10-19 against each project's own license page or model card. This is a practical checklist, **not legal advice**.

Jarvis's repository contains only project-authored code (MIT). It **does not redistribute** any model, voice or package: `setup.bat` downloads them to the user's own PC. Keeping third-party assets out of the repository reduces redistribution concerns; however, it does not guarantee every downstream use is licensed. The remaining question is **"what can the creator and viewers do with the downloaded parts?"**, especially in **monetized videos** or anything commercial.

## Summary

| Component | License (verified) | Public repo OK? | Personal use | Monetized video / commercial |
| --- | --- | --- | --- | --- |
| Jarvis source code | MIT ([LICENSE](../LICENSE)) | ✅ | ✅ | ✅ |
| Ollama | MIT | ✅ (not bundled) | ✅ | ✅ |
| Gemma 4 (`gemma4:e2b`) | Apache 2.0 ([Google](https://opensource.googleblog.com/2026/03/gemma-4-expanding-the-gemmaverse-with-apache-20.html)) | ✅ | ✅ | ✅ |
| faster-whisper + `base.en` model | MIT ([model](https://huggingface.co/Systran/faster-whisper-base.en)) | ✅ | ✅ | ✅ |
| openWakeWord code | Apache 2.0 | ✅ | ✅ | ✅ |
| openWakeWord **`hey_jarvis` model** | **CC BY-NC-SA 4.0** ([README](https://github.com/dscripka/openWakeWord#license)) | ✅ (not bundled) | ✅ | ⚠️ **Non-commercial only** |
| Piper (`piper-tts`) | GPL-3.0 | ✅ (imported, not bundled) | ✅ | ✅ |
| **Piper voice `en_GB-alan-medium`** | **No satisfactory open license established** (see below) | ✅ (voice not bundled) | ⚠️ Permission uncertain | ⚠️ **Do not use commercially without written permission** |
| pyttsx3 (fallback voice) | MPL-2.0 | ✅ | ✅ | ✅ |
| sounddevice / NumPy / requests | MIT / BSD / Apache 2.0 | ✅ | ✅ | ✅ |
| Name "JARVIS" | Marvel trademark | ✅ with the existing disclaimer | ✅ | ⚠️ Don't use it as a product or brand name |

## Finding 1: the "alan" voice has no open license

- Its [model card](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_GB/alan/medium/MODEL_CARD) points to Mycroft's `apope_low` voice for the dataset license.
- That folder's `LICENSE` file in [MycroftAI/mimic3-voices](https://github.com/MycroftAI/mimic3-voices/tree/master/voices/en_UK/apope_low) reads **"Copyright 2022 Mycroft AI. All Rights Reserved."**
- The card also says it was **fine-tuned from the `lessac` voice**. The Lessac/Blizzard 2013 data is licensed for **research only** and excludes commercial use ([license](https://www.cstr.ed.ac.uk/projects/blizzard/2013/lessac_blizzard2013/license.html)). Most Piper "medium" voices are fine-tuned from lessac, so this affects other voices too, not just alan.

**Promising alternative:** `en_GB-cori-medium` (or `-high`). Its model card describes a UK English **female** voice, **trained from scratch** on **public-domain** LibriVox recordings ([model card](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_GB/cori/medium/MODEL_CARD)). Using a built-in Windows voice on the licensed Windows device may avoid the Piper voice-model provenance issue, but check the relevant Windows usage terms before commercial redistribution of recordings.

## Finding 2: the "Hey Jarvis" wake word is non-commercial (now opt-in)

**Resolved for default setup (2026-10-20):** `setup.bat` no longer downloads the pretrained wake-word model, and normal Jarvis startup uses the HUD TALK button. The user must explicitly pass `--wake` to download and use `hey_jarvis`; its noncommercial license remains applicable in that mode.

openWakeWord's pretrained models are CC BY-NC-SA 4.0. Personal use and a non-monetized demo fit this license. Whether a **monetized** video demonstrating the pretrained model constitutes licensed use requires rights-holder clarification; do not assume it is allowed. Options, safest first:

1. Demo with push-to-talk or typing in monetized videos (no wake-word model involved).
2. Train your own wake word with openWakeWord's training notebook on your own recordings, then license it however you like.
3. Keep `hey_jarvis` and say "non-commercial model" in the description (already in THIRD_PARTY_NOTICES).

## Finding 3: GPL Piper and MIT Jarvis can coexist

Jarvis only **imports** Piper and never ships it, so the MIT license on Jarvis's own code is fine. If a future release bundles Piper (for example a one-click `.exe` built with PyInstaller), that bundle has to follow **GPL-3.0** (source available, GPL terms for the combined program). Keep shipping source only, or revisit then.

## Owner decisions (tick before going public)

- [x] **Public-release code voice menu:** Windows built-in voice is the default; optional Cori is selectable via a strict numbered menu, with the preference saved in private `commands.json`. Alan is excluded from the public menu. The owner may keep Alan only in her separate private development copy; commercial rights for that voice remain unconfirmed.
- [ ] **Commercial-use rights:** confirm Cori model/output rights and the relevant Windows built-in voice recording terms before any monetized voice demonstration.
- [ ] **Videos:** is the channel/video monetized? If yes, use the Windows voice or cori for Jarvis's voice on camera, and push-to-talk instead of the wake word, and verify the rights governing the resulting audio.
- [x] **Wake word:** opt-in only with `--wake`; not downloaded in default setup. Use it only where the noncommercial license permits, or train and appropriately license a custom model.
- [ ] **Distribution:** source only (current plan). No bundled models, voices or `.exe`.
- [ ] Re-check these licenses on release day; model cards can change.

[← Third-party notices](../THIRD_PARTY_NOTICES.md) · [Release checklist](../RELEASE_READINESS.md)

> **Scope:** Sources describe model provenance and repository/dataset terms. Neither MIT for the repository nor public-domain training recordings automatically licenses every voice-model weight, synthesized-audio use, trademark, or downstream commercial activity. Seek qualified legal advice for commercial release.
