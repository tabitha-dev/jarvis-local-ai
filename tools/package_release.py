"""Allowlist-only source packaging. No publishing and no personal assets."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    '.gitignore', 'README.md', 'RELEASE_READINESS.md',
    'THIRD_PARTY_NOTICES.md', 'CONTRIBUTING.md',
    'commands.example.json', 'commands.py', 'jarvis.py',
    'setup.bat', 'run_jarvis.bat', 'run_tests.bat',
    'make_release.bat', 'requirements.txt', 'ui.html',
    'tests/test_commands.py', 'tests/test_ui_security.py',
    'docs/ARCHITECTURE.md', 'docs/INSTALL_WINDOWS.md',
    'docs/TROUBLESHOOTING.md', 'docs/SECURITY.md',
    'tools/package_release.py',
    'assets/jarvis-real-hud.jpg',
)


def inspect():
    missing = [name for name in FILES if not (ROOT / name).is_file()]
    if missing:
        raise ValueError('Required files missing: ' + ', '.join(missing))
    cfg = json.loads((ROOT/'commands.example.json').read_text(encoding='utf-8'))
    assert isinstance(cfg, dict) and 'apps' in cfg
    for name in FILES:
        target = ROOT / name
        if target.is_symlink() or not target.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError(f'Unsafe source file: {name}')
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Inspect sources without producing any ZIP')
    parser.add_argument('--output', type=Path, help='Write a source-only ZIP after a project LICENSE is chosen')
    args = parser.parse_args()
    inspect()
    if args.check or args.output is None:
        print(f'PASS: reviewed allowlist of {len(FILES)} source/docs assets; no distribution package created.')
        return 0
    if not (ROOT/'LICENSE').is_file():
        print('STOP: choose and add project LICENSE with the owner before making a shareable ZIP.', file=sys.stderr)
        return 2
    if args.output.exists():
        print('STOP: target already exists; refusing to overwrite it.', file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    paths = (*FILES, 'LICENSE')
    with zipfile.ZipFile(args.output, 'x', compression=zipfile.ZIP_DEFLATED) as z:
        for name in paths:
            z.write(ROOT / name, arcname=f'jarvis-local-ai/{name}')
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(f'Source archive created: {args.output} (SHA256 {digest})')
    print('Not proof of Windows validation. Obtain owner permission before public distribution.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
