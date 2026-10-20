# Contributing

Thanks for your interest in Jarvis. Project-authored code carries the [MIT License](LICENSE), but the repository is still a **private pre-release** and has not been distributed publicly. Third-party models, voices and packages keep their own licenses (see [Third-party notices](THIRD_PARTY_NOTICES.md)); please don't redistribute model weights or voice files.

## Before contributing

- Open an issue with a reproducible description, or discuss the change with the maintainer.
- Use a branch and submit a PR with a concise explanation and any test results.
- Do not include API keys, `commands.json`, personal folders, model weights, recording transcripts or `.venv` files.
- Prefer focused tests for command routing and local HTTP endpoints.
- Keep claims about simulations, Windows installation and offline functionality accurate.

### Local checks

```sh
python -m compileall -q commands.py jarvis.py tests
python -m unittest discover tests -v
python tools/package_release.py --check
```

The unit tests mock commands and, on non-Windows computers without audio packages, may need additional developer dependencies. GitHub Actions provides code-level smoke tests, **not** hardware validation.

[← README](README.md)
