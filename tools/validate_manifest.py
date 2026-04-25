#!/usr/bin/env python3
import json, sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except Exception:
    Draft202012Validator = None

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_manifest(path: Path, schema_path: Path):
    manifest = load_json(path)
    errors = []
    if Draft202012Validator:
        schema = load_json(schema_path)
        validator = Draft202012Validator(schema)
        for e in sorted(validator.iter_errors(manifest), key=lambda e: e.path):
            errors.append(f"schema: {'/'.join(map(str, e.path))}: {e.message}")
    # MCS checks
    subject = manifest.get('subject', {})
    rights = manifest.get('rights', {})
    consent = manifest.get('consent', {})
    review = manifest.get('review', {})
    visibility = manifest.get('visibility')
    if subject.get('is_minor') and visibility in ('public_indexed', 'public_unlisted'):
        errors.append('MCS: minors cannot be publicly indexed or unlisted without special legal review')
    if visibility in ('public_indexed', 'public_unlisted'):
        if not rights.get('allow_public_listing'):
            errors.append('MCS: public visibility requires rights.allow_public_listing=true')
        if review.get('status') != 'approved_public':
            errors.append('MCS: public visibility requires review.status=approved_public')
        if not (review.get('verified_consent_badge') or review.get('public_data_only_badge')):
            errors.append('MCS: public visibility requires verified-consent or public-data-only badge')
    if (rights.get('allow_voice_clone') or rights.get('allow_avatar_clone')) and not consent.get('separate_biometric_consent'):
        errors.append('MCS: voice/avatar cloning requires separate biometric consent')
    if not consent.get('withdrawal_endpoint'):
        errors.append('MCS: consent.withdrawal_endpoint is required')
    return errors

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: validate_manifest.py path/to/manifest.json')
        sys.exit(2)
    root = Path(__file__).resolve().parents[1]
    schema_path = root / 'schemas' / 'manifest.schema.json'
    errors = validate_manifest(Path(sys.argv[1]), schema_path)
    if errors:
        print(f'FAILED: {sys.argv[1]}')
        for e in errors:
            print(' -', e)
        sys.exit(1)
    print(f'OK: {sys.argv[1]}')
