# Troubleshooting

| Problem | What to try |
|---|---|
| `winget` is not recognized | Install or repair Microsoft App Installer, restart the terminal, check `winget --version`. |
| Python 3.12 not found | Run `py -3.12 --version` and verify the user installation location. |
| Ollama cannot start | Open the Ollama app, run `ollama --version`, and check `http://127.0.0.1:11434/api/tags` locally. |
| Local model is missing | Run `ollama list`; install the model named in `jarvis.py` with `ollama pull gemma4:e2b`. |
| Model response is slow | First load may take longer. CPU-only inference varies substantially; check available memory. |
| Piper download fails | Ensure the virtual environment is active, internet works, and the correct model/voice is selected. |
| Microphone isn't detected | Check Windows Settings → System → Sound → Input and microphone permission. |
| Optional wake word (`--wake`) falsely triggers | Raise `WAKE_THRESHOLD` gradually. The default TALK mode does not need the noncommercial model. |
| Browser or app command doesn't work | Verify the application is installed and customize `commands.json` with its actual executable or shortcut. |
| Dashboard doesn't open | Check whether the loopback port is occupied; consult the console log. Do not expose the HUD on a public network. |

When filing a bug, omit personal paths, tokens, transcripts, user info and microphone recordings unless you explicitly choose to disclose them. Include Windows version, Python version, the steps you tried and the **redacted** terminal error.

[← README](../README.md) · [Security](SECURITY.md)
