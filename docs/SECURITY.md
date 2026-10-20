# Security and threat model

This is an educational desktop assistant that can launch applications and act on a computer. It is **not a security-audited product**.

## Protections currently implemented

- Local dashboard listens on `127.0.0.1`, not a public interface.
- Browser-origin and host checks help mitigate attacks from unrelated websites.
- Per-session tokens are checked for local action routes and the Server-Sent Events `/events` endpoint.
- Command handlers launch applications without using a shell for user-controlled strings; web addresses are validated.
- Personal configuration, downloaded models, virtual environments and voice assets are ignored by Git.

## What these protections do **not** guarantee

- A program running with the same user privileges can potentially connect to and inspect the local service. The token is present in the locally served page; it is not a defense against local malware.
- Application launchers and user-defined shortcuts still perform actions on your computer. Read the source before adding commands.
- Automated tests use mocks and cannot prove Windows permission boundaries, microphone behavior or safe behavior in every environment.
- Model behavior may be wrong; do not use it to authorize sensitive or irreversible computer changes.

## Reporting security issues

Please do **not** publish exploit details or secrets in a public issue. Use GitHub's private vulnerability reporting feature if available on the repository, or contact the maintainer through GitHub. Don't include access tokens, transcripts or personal paths.

[← README](../README.md) · [Release readiness](../RELEASE_READINESS.md)
