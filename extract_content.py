#!/usr/bin/env python3
"""
Step 1: Extract ALL text content from original HTML files
Step 2: Create translation keys based on ACTUAL content
Step 3: Tag every element with data-i18n
Step 4: Write English translations
"""
import json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(r"C:\Users\paule\OneDrive\Desktop\Arabix Theme\education")
SITE = "01-alriyadh-academy"
DIR = BASE / SITE

# Reset from git first
import subprocess
subprocess.run(["git", "checkout", "35124f9", "--", f"{SITE}/"], cwd=BASE, capture_output=True)
print("[OK] Reset to original")

def clean(t):
    return re.sub(r'\s+', ' ', t).strip()

def extract_texts(soup):
    """Extract all text-bearing elements and their text"""
    result = []
    seen_texts = set()
    
    for tag_name in ['h1','h2','h3','h4','h5','h6','p','span','a','button','li','label','cite','strong','em','small','blockquote']:
        for el in soup.find_all(tag_name):
            # Skip if has block-level children
            has_block = any(c.name in ['div','section','nav','header','footer','main','aside','article','form','table','ul','ol','blockquote'] for c in el.find_all(recursive=False))
            if has_block:
                continue
            # Skip social/media icons-only elements
            if tag_name == 'a' and el.find('i') and not clean(el.get_text()):
                continue
            
            text = clean(el.get_text())
            if len(text) < 2:
                continue
            if text in seen_texts:
                continue
            seen_texts.add(text)
            
            # Check for direct text (not just children)
            has_element_children = len(el.find_all(recursive=False)) > 0
            
            result.append({
                'el': el,
                'tag': tag_name,
                'text': text,
                'has_children': has_element_children,
                'inner_html': str(el.encode_contents(), 'utf-8').strip() if hasattr(el, 'encode_contents') else '',
            })
    return result

# Process all HTML files
all_texts = {}
for html_file in sorted(DIR.glob("*.html")):
    print(f"\n=== {html_file.name} ===")
    html = html_file.read_text(encoding='utf-8')
    # Remove any i18n artifacts
    html = re.sub(r'<script>window\.__i18n=.*?</script>', '', html, flags=re.DOTALL)
    
    soup = BeautifulSoup(html, 'html.parser')
    texts = extract_texts(soup)
    all_texts[html_file.name] = texts
    
    for t in texts:
        txt = t['text'][:90]
        tag = t['tag']
        print(f"  [{tag:8s}] [{txt}]")

print(f"\n\n{'='*60}")
print("Total texts extracted:")
total = sum(len(v) for v in all_texts.values())
print(f"Total elements: {total}")
