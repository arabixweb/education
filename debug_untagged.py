#!/usr/bin/env python3
"""Debug: find untagged elements in homepage."""
import re, sys
from pathlib import Path
from bs4 import BeautifulSoup

DIR = Path(r"C:\Users\paule\OneDrive\Desktop\Arabix Theme\education\01-alriyadh-academy")

# Untagged elements on index
soup = BeautifulSoup(open(DIR / "index.html", encoding='utf-8'), 'html.parser')
found = 0
for e in soup.find_all(['h1','h2','h3','h4','p','span','a','button','li','label','cite','strong','div']):
    if e.has_attr('data-i18n'):
        continue
    t = re.sub(r'\s+', ' ', e.get_text()).strip()
    if len(t) < 3:
        continue
    # Skip elements with block-level children
    block_children = [c.name for c in e.find_all(recursive=False) if c.name in ['div','section','nav','header','footer','main']]
    if block_children:
        continue
    sys.stdout.reconfigure(encoding='utf-8')
    print(f'[{e.name:8s}] [{t[:90]}]')
    found += 1

print(f"\nUntagged: {found}")
