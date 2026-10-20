# Third-party software and models

This repository contains **Jarvis-authored source code licensed under [MIT](LICENSE)** and its documentation. The MIT license does **not** supersede third-party restrictions. It does not bundle any models, voices or Python packages. `setup.bat` downloads them from their official sources on your machine, under their own licenses.

| Component | What it does | License | Notes |
| --- | --- | --- | --- |
| [Ollama](https://github.com/ollama/ollama) | Runs the local AI model | MIT | Installed separately |
| [Gemma 4](https://ollama.com/library/gemma4) (`gemma4:e2b`) | The AI brain | Apache 2.0 ([announcement](https://opensource.googleblog.com/2026/03/gemma-4-expanding-the-gemmaverse-with-apache-20.html)) | Downloaded by `ollama pull` |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Speech to text | MIT | Whisper `base.en` model downloaded on first run |
| [openWakeWord](https://github.com/dscripka/openWakeWord) | "Hey Jarvis" wake word | Code: Apache 2.0 | **Pretrained models (including `hey_jarvis`): CC BY-NC-SA 4.0, non-commercial.** Downloaded at runtime, not redistributed here. Check the license before any commercial use. |
| [Piper](https://github.com/OHF-Voice/piper1-gpl) (`piper-tts`) | Text to speech | GPL-3.0 | Installed with pip; Jarvis only imports it |
| Piper voice `en_GB-alan-medium` | Jarvis's British voice | See its [model card](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_GB/alan/medium/MODEL_CARD) | Card points to its source dataset for license terms; verify before commercial use |
| [sounddevice](https://github.com/spatialaudio/python-sounddevice), [NumPy](https://numpy.org), [requests](https://github.com/psf/requests), [pyttsx3](https://github.com/nateshmbhat/pyttsx3) | Audio, math, HTTP, fallback voice | MIT / BSD / Apache 2.0 / MPL-2.0 | Installed with pip |

"JARVIS" is used as a fan-inspired project name. This project is not affiliated with or endorsed by Marvel or Disney, and it uses no Marvel artwork, footage or voices.
