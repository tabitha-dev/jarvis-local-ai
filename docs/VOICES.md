# Choosing Jarvis's voice

Jarvis can speak with the **built-in Windows voice** (the default) or the optional **Cori** voice from Piper. You pick one during `setup.bat`, and you can change it any time with `change_voice.bat`. Your choice is saved only on your PC, in `commands.json`, which Git ignores.

## The voices

| Voice | Sounds like | Download | License |
| --- | --- | --- | --- |
| **1. Windows built-in** (default) | Whatever voice Windows is set to, for example Microsoft David or Zira | None | Part of Windows; applicable Windows usage terms still apply |
| **2. Cori** (`en_GB-cori-medium`) | British English, female, more natural | Approximately 60 MB if selected (size varies) | Trained from scratch on public-domain LibriVox recordings ([model card](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_GB/cori/medium/MODEL_CARD)); confirm model/output rights for intended use |

Not sure? Keep the Windows voice. It needs no extra model download, and you can switch later.

## Pick a voice during setup

In step **4/6** of `setup.bat`, press **1** for Windows, **2** for Cori, or **Enter** (or wait 25 seconds) for the Windows default.

## Change your voice later

1. Close Jarvis.
2. Double-click `change_voice.bat` in the Jarvis folder.
3. Press **1** or **2**, the same as in setup.
4. Start Jarvis again with `run_jarvis.bat`. It says "Jarvis online." in the selected voice.

## Change which Windows voice it uses

The Windows option uses your PC's default text-to-speech voice.

1. Press **Windows + R**, type `control`, and press **Enter** to open Control Panel.
2. Search for **text to speech** and open **Change text to speech settings**.
3. Pick a voice under **Voice selection**, click **Preview Voice**, then **OK**.
4. Restart Jarvis.

Only voices listed there work with Jarvis. For additional voices, try **Settings → Time & language → Speech → Add voices**, but not every voice installed there appears in the classic control-panel list.

## If the voice isn't working

| What happens | What to do |
| --- | --- |
| You chose Cori but hear the Windows voice | The Cori file is missing or did not load. Run `change_voice.bat`, choose **2**, and watch for download errors. Jarvis falls back to Windows when Cori cannot load. |
| Cori download fails | Check your internet connection and run `change_voice.bat` again. Your previous preference stays saved until a new one succeeds. |
| No sound at all | Check which output speaker Windows uses, then try typing a question in the HUD. |
| The voice talks too fast or too slow | For Windows TTS, open `jarvis.py`, find `setProperty("rate", 185)`, and try a value between 150 and 220. |

## Advanced: add another Piper voice

Piper has [many voices](https://huggingface.co/rhasspy/piper-voices), but **each has its own license**. Some may be trained using research-only data; check the weights, dataset and output-use terms, especially for public or monetized videos.

1. **Check the license first.** Read the model's `MODEL_CARD` and data source details before using it.
2. Add it to `voice_settings.py` under `VOICE_MODELS`, for example `"piper:en_US-example-medium": "en_US-example-medium"`.
3. Add a menu number for it in `tools/select_voice.py` and step 4 of `setup.bat`.
4. Update the tests in `tests/test_voice.py`, which intentionally verify the exact allowlist. Run `run_tests.bat`.
5. Run `change_voice.bat` and choose the new option.

Never commit voice model weights. The `voices/` folder is Git-ignored.

[← README](../README.md) · [Third-party notices](../THIRD_PARTY_NOTICES.md) · [Troubleshooting](TROUBLESHOOTING.md)
