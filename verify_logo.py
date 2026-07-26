#!/usr/bin/env python3
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
html = open(r'C:\Users\paule\OneDrive\Desktop\Arabix Theme\education\01-alriyadh-academy\index.html', encoding='utf-8').read()
m = re.search(r'window\.__i18n=({.*?});', html, re.DOTALL)
data = json.loads(m.group(1))
for k in sorted(data['ar'].keys()):
    ar = data['ar'][k]
    en = data['en'].get(k, '')
    if ar in ['أكاديمية', 'الرياض'] or 'Academy' in en or 'Riyadh' in en:
        print(f'{k}: AR="{ar}"  EN="{en}"')
