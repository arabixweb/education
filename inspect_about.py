#!/usr/bin/env python3
"""Deep inspect what's untagged on about.html"""
import re
from pathlib import Path
from bs4 import BeautifulSoup

html = Path(r"C:\Users\paule\OneDrive\Desktop\Arabix Theme\education\01-alriyadh-academy\about.html").read_text(encoding='utf-8')
soup = BeautifulSoup(html, 'html.parser')

# Check all text-bearing elements that are NOT tagged
for tag_name in ['h1','h2','h3','h4','h5','h6','p','span','a','button','li','label','cite','strong','em','div','blockquote','small']:
    for el in soup.find_all(tag_name):
        if el.has_attr('data-i18n') and el['data-i18n']:
            continue
        # Skip block-containing
        has_block = any(c.name in ['div','section','nav','header','footer','main'] for c in el.find_all(recursive=False))
        if has_block:
            continue
        text = re.sub(r'\s+',' ',el.get_text()).strip()
        if len(text) < 3:
            continue
        # Skip pure numbers
        if re.sub(r'[\s,.]','',text).isdigit():
            continue
        print(f'[{el.name:8s}] [{text[:100]}]')
