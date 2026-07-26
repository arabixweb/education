#!/usr/bin/env python3
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
html = open(r'C:\Users\paule\OneDrive\Desktop\Arabix Theme\education\01-alriyadh-academy\index.html', encoding='utf-8').read()
m = re.search(r'window\.__i18n=({.*?});', html, re.DOTALL)
data = json.loads(m.group(1))
for key in ['أكاد', 'الري', 'riyadh']:
    if key in data['ar']:
        en_v = data['en'].get(key, 'MISSING')
        ar_v = data['ar'][key]
        print(f'{key}: AR="{ar_v}", EN="{en_v}"')
# Check hero stats
for k in sorted(data['ar'].keys()):
    if 'index_t0' in k or 'index_0' in k:
        print(f'{k}: AR="{data["ar"][k][:60]}", EN="{data["en"][k][:60]}"')
