# JARVIS Local AI — Public source release notes

**Status:** Prepared public source code candidate. No public GitHub visibility change or YouTube upload has been made by this release-preparation branch.

## What is included
- MIT-licensed project-authored Python code, HTML/CSS/JavaScript HUD, Windows batch setup, tests and documentation.
- Default hands-free “Jarvis, …” recognition through locally running faster-whisper, with TALK/typing alternatives.
- Windows SAPI spoken output with pyttsx3 fallback; quick app, website and clock commands.
- Working-Windows `requirements.lock.txt` supplied by the maintainer on October 20, 2026, with platform markers.
- GitHub source download includes only reviewed source/docs/images; **no** speech/audio recordings, personalized `commands.json`, API keys, pretrained voice or wake model binaries.
- Optional `--wake` downloads a pretrained model subject to **CC BY-NC-SA 4.0 (noncommercial)**. It is not the default.

## Testing and limitations
- **61 isolated tests passed** on GitHub Actions Windows Server 2025 and Ubuntu 24.04, Python 3.12. These tests mock audio and actual launches.
- Creator reports an end-to-end Windows 11 **fresh-folder** test with working microphone, speech replies, local AI, and app launch; **Python and Ollama were already installed**.
- **Not yet tested:** an independent completely clean Windows PC without Python and Ollama preinstalled. This remains on the follow-up checklist and is **not claimed as completed**.
- No claim of a formal security audit or commercial clearance for optional Cori voice model/outputs. Review [third-party notices](THIRD_PARTY_NOTICES.md) and [license review](docs/LICENSE_REVIEW.md).

## Download and installation
1. After the repository is made public, use **Code → Download ZIP** at https://github.com/tabitha-dev/jarvis-local-ai or clone the repository.
2. Read [Windows installation guide](docs/INSTALL_WINDOWS.md), [security guidance](docs/SECURITY.md), and the batch files.
3. Run `setup.bat` on a Windows 10/11 computer that you are authorized to configure; setup downloads Python/Ollama/model assets as required.
4. Run `run_tests.bat`, then `run_jarvis.bat`; listen for "Jarvis online", then say "Jarvis, what time is it?"
5. The default Windows voice needs no separate Piper download. Cori is an optional model with rights requiring review.

## Publishing sequence
Only after repository visibility is intentionally changed and the link works while signed out, add the public GitHub link and verified read-only student guide link to the approved YouTube V8 description. Upload the video Unlisted for review before making it Public.

**Maintainer:** Tabitha Dev
