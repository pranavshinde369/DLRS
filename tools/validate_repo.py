#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISALLOWED_EXT = {'.mp4','.mov','.mkv','.wav','.flac','.mp3','.aac','.png','.jpg','.jpeg','.webp','.zip','.7z','.tar','.gz','.safetensors','.onnx','.pt','.pth','.gguf'}

# Some docs/assets exceptions can be added here.
ALLOW_PREFIXES = {'docs/', 'assets/public/'}

def is_allowed(path: Path):
    rel = path.relative_to(ROOT).as_posix()
    return any(rel.startswith(prefix) for prefix in ALLOW_PREFIXES)

def check_sensitive_files():
    errors=[]
    for p in ROOT.rglob('*'):
        if p.is_file() and '.git' not in p.parts:
            if p.suffix.lower() in DISALLOWED_EXT and not is_allowed(p):
                errors.append(f'Raw or large sensitive file should not be committed: {p.relative_to(ROOT)}')
    return errors

def main():
    errors = check_sensitive_files()
    manifests = sorted((ROOT/'humans').glob('*/*/*/manifest.json')) if (ROOT/'humans').exists() else []
    for m in manifests:
        r = subprocess.run([sys.executable, str(ROOT/'tools'/'validate_manifest.py'), str(m)], text=True, capture_output=True)
        if r.returncode != 0:
            errors.append(r.stdout + r.stderr)
        else:
            print(r.stdout.strip())
    if errors:
        print('\nVALIDATION FAILED')
        for e in errors:
            print('-', e)
        sys.exit(1)
    print(f'Validation passed. Manifests checked: {len(manifests)}')

if __name__ == '__main__':
    main()
