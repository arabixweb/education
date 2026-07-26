#!/usr/bin/env python3
"""Check all unique keys and their Arabic texts for this site"""
import json, re
from pathlib import Path
from bs4 import BeautifulSoup

DIR = Path(r"C:\Users\paule\OneDrive\Desktop\Arabix Theme\education\01-alriyadh-academy")

all_keys = {}
for f in sorted(DIR.glob("*.html")):
    soup = BeautifulSoup(open(f, encoding='utf-8'), 'html.parser')
    # Extract __i18n data
    for script in soup.find_all('script'):
        if script.string and 'window.__i18n' in script.string:
            m = re.search(r'window\.__i18n=({.*?});', script.string, re.DOTALL)
            if m:
                data = json.loads(m.group(1))
                for key, ar_val in data.get('ar', {}).items():
                    if key not in all_keys:
                        all_keys[key] = []
                    all_keys[key].append({
                        'ar': ar_val,
                        'en': data['en'].get(key, ''),
                        'page': f.name
                    })

print(f"Total unique keys: {len(all_keys)}\n")
for i, (key, vals) in enumerate(sorted(all_keys.items())):
    ar = vals[0]['ar'][:100]
    en = vals[0]['en'][:100]
    pages = set(v['page'] for v in vals)
    print(f"{i:3d}. {key:12s} [{', '.join(sorted(pages)):40s}]")
    print(f"     AR: {ar}")
    print(f"     EN: {en}")
