#!/usr/bin/env python3
"""
Step 1: Extract all text elements with proper paths, tag them,
and generate a JSON with Arabic texts that I can add English to.
"""
import json, re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

BASE = Path(r"C:\Users\paule\OneDrive\Desktop\Arabix Theme\education")
SITE = "01-alriyadh-academy"
DIR = BASE / SITE

def elements_text(el):
    """Get just this element's direct text, not children's"""
    texts = []
    for child in el.children:
        if isinstance(child, NavigableString):
            t = child.strip()
            if t:
                texts.append(t)
    return ' '.join(texts)

# Process each HTML file
all_data = {}

for html_file in sorted(DIR.glob("*.html")):
    print(f"\n=== {html_file.name} ===")
    html = html_file.read_text(encoding='utf-8')
    # Remove existing i18n artifacts
    html = re.sub(r'<script>window\.__i18n=.*?</script>', '', html, flags=re.DOTALL)
    
    soup = BeautifulSoup(html, 'html.parser')
    file_data = []
    page = html_file.name.replace('.html', '')
    
    # Define elements to extract by tag pattern
    # We want: headings, paragraphs, spans, links, buttons, labels, blockquotes, citions,
    # but only those that directly contain text
    
    def tag_and_extract(el):
        """Tag element with data-i18n if it has direct text and return the text"""
        if el.has_attr('data-i18n'):
            return None
        # Only elements with direct text content (not from children)
        text = elements_text(el)
        if not text or len(text) < 1:
            return None
        
        # Skip elements that have block-level children
        block_tags = ['div','section','nav','header','footer','main','aside','article','form','table','ul','ol']
        if el.name in block_tags:
            # For divs, only tag if they have NO element children at all
            has_element_child = any(not isinstance(c, NavigableString) for c in el.children)
            if has_element_child:
                return None
        
        if text and len(text) >= 1:
            key = f"{page}_{short_id(text, el.name)}"
            el['data-i18n'] = key
            return {'key': key, 'tag': el.name, 'ar': text, 'selector': get_selector(el)}
        return None
    
    def short_id(text, tag):
        """Create a short readable ID from text"""
        # Take first 3 Arabic chars
        ar_chars = re.findall(r'[\u0600-\u06FF]', text)
        if ar_chars:
            return ''.join(ar_chars[:3])
        return text[:4].lower()
    
    def get_selector(el):
        """Get a CSS-like path for debugging"""
        parts = []
        for parent in el.parents:
            if parent.name == '[document]':
                break
            cls = ' '.join(parent.get('class', []))
            if cls:
                parts.append(f"{parent.name}.{cls.replace(' ', '.')}")
            else:
                parts.append(parent.name)
        parts.reverse()
        parts.append(el.name)
        return ' > '.join(parts)
    
    # Process elements in document order
    for el in soup.find_all(True):
        if el.name in ['html','head','body','meta','link','script','style','svg','path','circle','defs',
                        'linearGradient','stop','g','text', 'title']:
            continue
        if el.has_attr('data-i18n'):
            continue
        
        result = tag_and_extract(el)
        if result:
            file_data.append(result)
    
    # Check for any remaining untagged simple elements
    for el in soup.find_all(['h1','h2','h3','h4','h5','h6','p','span','a','button','label','cite','blockquote','strong','em','small','li']):
        result = tag_and_extract(el)
        if result:
            file_data.append(result)
    
    print(f"  Tagged {len(file_data)} elements")
    
    all_data[html_file.name] = file_data
    
    # Write back HTML with data-i18n
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

# Save extract texts to JSON
texts_json = {}
for fname, entries in all_data.items():
    for e in entries:
        texts_json[e['key']] = {
            'ar': e['ar'],
            'en': '',  # Fill manually later
            'tag': e['tag'],
            'page': e.get('selector', '')[:60]
        }

with open(DIR / '_translations.json', 'w', encoding='utf-8') as f:
    json.dump(texts_json, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"Total keys: {len(texts_json)}")
print(f"Saved to {SITE}/_translations.json")
print(f"{'='*60}")
print("\nNow edit the JSON to add English translations, then run step 2.")
