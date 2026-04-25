#!/usr/bin/env python3
import argparse, shutil, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'humans' / '_TEMPLATE'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--record-id', required=True)
    ap.add_argument('--display-name', required=True)
    ap.add_argument('--region', required=True)
    ap.add_argument('--country', required=True)
    args = ap.parse_args()
    slug = args.display_name.lower().replace(' ', '-').replace('_','-')
    dest = ROOT / 'humans' / args.region / args.country / f'{args.record_id}_{slug}'
    if dest.exists():
        raise SystemExit(f'Already exists: {dest}')
    shutil.copytree(TEMPLATE, dest)
    manifest_path = dest / 'manifest.json'
    m = json.loads(manifest_path.read_text(encoding='utf-8'))
    m['record_id'] = args.record_id
    m['display_slug'] = slug
    m['subject']['display_name'] = args.display_name
    m['subject']['residency_region'] = args.country.upper()
    manifest_path.write_text(json.dumps(m, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    profile_path = dest / 'public_profile.json'
    p = json.loads(profile_path.read_text(encoding='utf-8'))
    p['record_id'] = args.record_id
    p['display_name'] = args.display_name
    profile_path.write_text(json.dumps(p, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(dest.relative_to(ROOT))

if __name__ == '__main__':
    main()
