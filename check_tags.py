#!/usr/bin/env python3
"""Check which elements got tagged in each page."""
from bs4 import BeautifulSoup
from pathlib import Path

DIR = Path(r"C:\Users\paule\OneDrive\Desktop\Arabix Theme\education\01-alriyadh-academy")

for f in sorted(DIR.glob("*.html")):
    print(f"\n=== {f.name} ===")
    soup = BeautifulSoup(open(f, encoding='utf-8'), 'html.parser')
    count = 0
    for el in soup.find_all(attrs={'data-i18n': True}):
        count += 1
        txt = ' '.join(el.get_text().split())[:80]
        key = el['data-i18n']
        k = key[:22]
        t = txt[:60]
        print(f"  [{k:22s}] {t}")
    print(f"Total: {count}")
