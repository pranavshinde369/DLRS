#!/usr/bin/env python3
import json, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / 'registry'

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def badges(manifest):
    b=[]
    review=manifest.get('review', {})
    rights=manifest.get('rights', {})
    if review.get('verified_consent_badge'): b.append('verified-consent')
    if review.get('public_data_only_badge'): b.append('public-data-only')
    if not manifest.get('rights', {}).get('allow_public_listing'): b.append('restricted-runtime')
    if rights.get('cross_border_transfer_status') == 'blocked' or rights.get('cross_border_transfer_basis') == 'none': b.append('cross-border-blocked')
    if manifest.get('subject', {}).get('status') == 'deceased': b.append('memorial-review-required')
    return b

def public_ok(m):
    if m.get('visibility') not in ('public_indexed','public_unlisted'): return False
    if not m.get('rights', {}).get('allow_public_listing'): return False
    if m.get('review', {}).get('status') != 'approved_public': return False
    if m.get('subject', {}).get('is_minor'): return False
    if not (m.get('review', {}).get('verified_consent_badge') or m.get('review', {}).get('public_data_only_badge')): return False
    return True

def main():
    entries=[]
    for manifest_path in sorted((ROOT/'humans').glob('*/*/*/manifest.json')):
        m=load_json(manifest_path)
        if not public_ok(m):
            continue
        rel=manifest_path.parent.relative_to(ROOT).as_posix()
        e={
            'record_id': m['record_id'],
            'path': rel,
            'display_name': m['subject']['display_name'],
            'visibility': m['visibility'],
            'badges': badges(m),
            'region': m['subject']['residency_region'],
            'locale': m['subject']['locale'],
            'risk_level': m['review']['risk_level'],
            'updated_at': m['audit']['last_modified_at']
        }
        entries.append(e)
    REGISTRY.mkdir(exist_ok=True)
    with open(REGISTRY/'humans.index.jsonl','w',encoding='utf-8') as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False)+'\n')
    with open(REGISTRY/'humans.index.csv','w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f, fieldnames=['record_id','path','display_name','visibility','badges','region','locale','risk_level','updated_at'])
        writer.writeheader()
        for e in entries:
            row=e.copy(); row['badges']='|'.join(row['badges']); writer.writerow(row)
    print(f'Built registry entries: {len(entries)}')

if __name__ == '__main__':
    main()
