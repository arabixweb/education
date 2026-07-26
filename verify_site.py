#!/usr/bin/env python3
"""Verify site is properly configured"""
import json, re
from pathlib import Path
from bs4 import BeautifulSoup

DIR = Path(r"C:\Users\paule\OneDrive\Desktop\Arabix Theme\education\01-alriyadh-academy")

print("="*60)
print("VERIFICATION: 01-alriyadh-academy")
print("="*60)

total_el = 0
total_keys = 0
missing_en = []

for f in sorted(DIR.glob("*.html")):
    soup = BeautifulSoup(open(f, encoding='utf-8'), 'html.parser')
    els = soup.find_all(attrs={'data-i18n': True})
    total_el += len(els)
    
    # Check __i18n data
    i18n_data = None
    for script in soup.find_all('script'):
        if script.string and 'window.__i18n' in script.string:
            m = re.search(r'window\.__i18n=({.*?});', script.string, re.DOTALL)
            if m:
                i18n_data = json.loads(m.group(1))
    
    if i18n_data:
        total_keys += len(i18n_data['ar'])
        for key in i18n_data['ar']:
            ar_val = i18n_data['ar'][key]
            en_val = i18n_data['en'].get(key, '')
            if en_val == ar_val:
                missing_en.append(f"{f.name}:{key} = {ar_val[:60]}")
    
    # Check tagged elements all have translations
    for el in els:
        key = el['data-i18n']
        if i18n_data and key not in i18n_data['ar']:
            print(f"  WARNING: {f.name} has key '{key}' not in translations!")
    
    print(f"  {f.name}: {len(els)} tagged, {len(i18n_data['ar']) if i18n_data else 0} keys")

print(f"\nTotal: {total_el} tagged elements, {total_keys} translation keys")
if missing_en:
    print(f"\n⚠️ {len(missing_en)} texts still missing English translations:")
    for m in missing_en:
        print(f"  {m}")
else:
    print("\n✅ ALL texts have English translations!")

# Check script.js
script_js = DIR / 'script.js'
if script_js.exists():
    print(f"\n✅ script.js exists ({script_js.stat().st_size} bytes)")
else:
    print(f"\n❌ script.js MISSING!")
