#!/usr/bin/env python3
"""
Generate full i18n for all 5 education sites using a more robust approach.
Uses BeautifulSoup-like parsing (via html.parser) and direct text matching.
"""

import json, re, os
from html.parser import HTMLParser
from pathlib import Path

BASE = Path(r"C:\Users\paule\OneDrive\Desktop\Arabix Theme\education")

# ===================== INCLUDES TRANSLATION DATA =====================
# Import translations from the existing file
import sys
sys.path.insert(0, str(BASE))
# We can't import an .html/.py file directly, so we'll parse it
# Actually let's just embed what we need from the existing generate_i18n.py

# Read the existing file to extract SITES dict
import importlib.util

# Instead, let's just exec the SITES definition from the existing file
with open(BASE / 'generate_i18n.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract SITES dict definition
# Find start of SITES assignment
start = content.find("SITES = {}")
if start == -1:
    start = content.find("SITES = [")
if start == -1:
    start = content.find("SITES ={")
    
# Find the function definitions that come after SITES
end = content.find("def get_main_script")
if end == -1:
    end = content.find("def process_html")

# Get just the SITES dict part
sites_code = content[start:end].strip()

# Clean up any trailing commas or syntax issues
if sites_code.endswith(',\n'):
    sites_code = sites_code[:-2]

# Execute the SITES definition
exec(sites_code)

# The SITES variable should now be available
# Verify
if 'SITES' not in dir():
    print("ERROR: Could not extract SITES dict")
    sys.exit(1)

print(f"Loaded translations for: {list(SITES.keys())}")


def add_data_i18n(html, key, ar_text, en_text):
    """
    Robustly add data-i18n attribute by finding element containing ar_text.
    Handles extra whitespace, newlines, nested HTML tags.
    """
    if not ar_text or len(ar_text) < 3:
        return html
    
    # Strip and normalize whitespace in the search text
    ar_norm = ' '.join(ar_text.split())
    
    # Check if ar_text contains HTML
    has_html = bool(re.search(r'<[^>]+>', ar_norm))
    
    if has_html:
        # For HTML text, we need to match ignoring the inner HTML tags
        # Create a pattern that matches ar_text but allows any inner tags
        # E.g., "لماذا <span class='gold'>أكاديمية الرياض</span>؟"
        # becomes:  لماذا <inner tags>أكاديمية الرياض<inner tags>؟
        
        # Split by HTML tags
        parts = re.split(r'(<[^>]+>)', ar_norm)
        pattern_parts = []
        for part in parts:
            if part.startswith('<'):
                # This is a tag - match any HTML tag
                pattern_parts.append(r'<[^>]*>')
            else:
                # This is text - escape it for regex
                pattern_parts.append(re.escape(part))
        ar_pattern = r'\s*'.join(pattern_parts)
    else:
        ar_pattern = re.escape(ar_norm)
    
    # Build regex with optional whitespace/newlines between characters
    # and allow for extra whitespace around the text in the HTML
    regex = rf'(<[^>]+?)>\s*{ar_pattern}\s*</'
    
    def replacer(m):
        open_tag = m.group(1)
        if 'data-i18n' not in open_tag:
            attrs = ' data-i18n="' + key + '"'
            if has_html:
                attrs += ' data-i18n-html="true"'
            # Insert before the closing >
            if open_tag.endswith('/'):
                # Self-closing tag - shouldn't happen but handle
                return open_tag[:-1] + attrs + '/>' + m.group(0)[len(open_tag)+1:]
            return open_tag + attrs + '>' + m.group(0)[len(open_tag)+1:]
        return m.group(0)
    
    new_html = re.sub(regex, replacer, html, count=1, flags=re.DOTALL)
    
    if new_html == html:
        # Try without the mandatory whitespace check - very flexible
        regex2 = rf'(<[^>]+?)>.*?{ar_pattern}.*?</'
        m2 = re.search(regex2, new_html, re.DOTALL)
        if m2:
            # Use the match but we need to be smarter
            pass
    
    return new_html


def add_data_i18n_flexible(html, key, ar_text):
    """
    Even more flexible: find the text anywhere and add data-i18n to containing element.
    Works by finding the text position and walking up to find the enclosing tag.
    """
    if not ar_text or len(ar_text) < 3:
        return html
    
    ar_norm = ' '.join(ar_text.split())
    has_html = bool(re.search(r'<[^>]+>', ar_norm))
    
    if has_html:
        # Build a flexible pattern
        parts = re.split(r'(<[^>]+>)', ar_norm)
        pattern = ''
        for part in parts:
            if part.startswith('<'):
                pattern += r'\s*<[^>]*>\s*'
            else:
                pattern += re.escape(part)
    else:
        pattern = re.escape(ar_norm)
    
    # Allow whitespace between any characters
    # pattern = r'\s*'.join(pattern)
    # Actually the above is wrong for non-has_html. Let me just use original pattern
    # with \s* between parts
    
    # Find an open tag followed by any content containing the pattern
    regex = rf'(<[a-zA-Z][^>]*?)>((?:[^<]*<[^>]*>)*[^<]*?){pattern}((?:[^<]*<[^>]*>)*[^<]*?)</\s*[a-zA-Z]'
    
    def replacer(m):
        open_tag = m.group(1)
        if 'data-i18n' in open_tag:
            return m.group(0)
        # Find last word of tag and insert attribute
        return open_tag + ' data-i18n="' + key + '" ' + ('data-i18n-html="true" ' if has_html else '') + '>' + m.group(2) + m.group(3) + m.group(4) + '</'
    
    new_html = re.sub(regex, replacer, html, count=1, flags=re.DOTALL)
    return new_html


def simple_text_mark(html, key, ar_text):
    """
    Super simple approach: find the Arabic text as a plain string in the HTML
    and wrap it with data-i18n on its parent tag.
    Uses a character-by-character search approach.
    """
    if not ar_text or len(ar_text) < 5:
        return html
    
    # Normalize
    ar_clean = ar_text.strip()
    
    # Remove HTML tags for matching
    ar_no_html = re.sub(r'<[^>]+>', '', ar_clean).strip()
    if not ar_no_html or len(ar_no_html) < 3:
        return html
    
    has_html = ar_clean != ar_no_html
    
    # Find position of ar_no_html in the HTML
    idx = html.find(ar_no_html)
    if idx == -1:
        # Try with extra spaces collapsed
        html_normalized = re.sub(r'\s+', ' ', html)
        ar_normalized = re.sub(r'\s+', ' ', ar_no_html)
        # This doesn't help with position finding
        return html
    
    # Found the text - now find the enclosing tag
    # Look backwards from idx to find '<' that isn't closed
    before = html[:idx]
    
    # Find the last opening tag before idx
    # We need to find the innermost tag that contains this text
    
    # Count tags between the last outer block-level tag
    last_open = before.rfind('>')
    before_open = before[:last_open+1] if last_open != -1 else before
    tag_start = before_open.rfind('<')
    
    if tag_start == -1:
        return html
    
    # Get the open tag
    open_tag_end = before_open.find('>', tag_start)
    if open_tag_end == -1:
        return html
    
    open_tag = before_open[tag_start:open_tag_end]
    
    # Get tag name
    tag_name_match = re.match(r'<(\w+)', open_tag)
    if not tag_name_match:
        return html
    
    tag_name = tag_name_match.group(1)
    
    # Check this isn't a self-closing or void tag
    if open_tag.endswith('/') or tag_name in ('br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr'):
        return html
    
    # Don't add if already has data-i18n
    if 'data-i18n' in open_tag:
        return html
    
    # Find the closing tag
    rest = html[idx:]
    # Find the next </tag_name>
    close_pattern = rf'</{tag_name}\s*>'
    close_match = re.search(close_pattern, rest, re.IGNORECASE)
    if not close_match:
        return html
    
    close_start = idx + close_match.start()
    close_end = idx + close_match.end()
    
    # Check that the matching is correct by verifying the inner content
    # Construct new open tag with data-i18n
    new_open_tag = open_tag + ' data-i18n="' + key + '"' + (' data-i18n-html="true"' if has_html else '')
    
    # Reconstruct
    new_html = before_open[:tag_start] + new_open_tag + '>' + before_open[open_tag_end+1:] + html[idx:]
    
    return new_html


def process_site(site_key):
    """Process all HTML files in a site folder."""
    site_dir = BASE / site_key
    if not site_dir.exists():
        print(f"  [SKIP] {site_dir} not found")
        return
    
    print(f"\n{'='*60}")
    print(f"Processing: {site_key}")
    print(f"{'='*60}")
    
    lang_data = SITES[site_key]
    
    # Keys for each page type
    page_keys_map = {}
    
    # Build base keys
    base_keys = [
        'site_name', 'site_tagline',
        'nav_home', 'nav_about', 'nav_programs', 'nav_contact',
        'lang_btn',
        'footer_desc', 'footer_links', 'footer_progs', 'footer_contact',
        'footer_prog1', 'footer_prog2', 'footer_prog3', 'footer_copy',
        'back_to_top'
    ]
    
    for suffix in ['', '2', '3']:
        k = f'form_prog{suffix}'
        if k in lang_data['ar']:
            base_keys.append(k)
    
    page_keys_map['index'] = list(set(base_keys + [
        'hero_tag', 'hero_title', 'hero_desc', 'hero_cta_primary', 'hero_cta_secondary',
        'hero_stat1', 'hero_stat2', 'hero_stat3',
        'sec_why_title', 'sec_why_desc',
        'feat1_title', 'feat1_desc', 'feat2_title', 'feat2_desc',
        'feat3_title', 'feat3_desc', 'feat4_title', 'feat4_desc',
        'why1_title', 'why1_desc', 'why2_title', 'why2_desc',
        'why3_title', 'why3_desc', 'why4_title', 'why4_desc',
        'cta_title', 'cta_desc', 'cta_btn',
        'founder_quote', 'founder_name',
        'hero_accent1', 'hero_accent2', 'hero_accent3',
        'quran_ayat', 'quran_surah',
    ]))
    
    page_keys_map['about'] = list(set(base_keys + [
        'page_title_about', 'about_heading', 'about_p1', 'about_p2', 'about_p3',
        'about_stat1_label', 'about_stat2_label', 'about_stat3_label', 'about_stat4_label',
        'breadcrumb_about',
    ]))
    
    page_keys_map['programs'] = list(set(base_keys + [
        'page_title_programs', 'programs_intro',
        'prog1_title', 'prog1_desc', 'prog1_meta',
        'prog2_title', 'prog2_desc', 'prog2_meta',
        'prog3_title', 'prog3_desc', 'prog3_meta',
        'prog4_title', 'prog4_desc', 'prog4_meta',
        'prog5_title', 'prog5_desc', 'prog5_meta',
        'prog6_title', 'prog6_desc', 'prog6_meta',
        'breadcrumb_programs',
        'course_badge',
    ]))
    
    contact_keys = list(set(base_keys + [
        'page_title_contact', 'contact_heading', 'form_heading',
        'form_name', 'form_name_ph', 'form_email', 'form_email_ph',
        'form_phone', 'form_phone_ph', 'form_program', 'form_program_ph',
        'form_message', 'form_message_ph', 'form_submit', 'form_success',
        'breadcrumb_contact',
        'contact_address', 'contact_phone', 'contact_email',
        'contact_hours', 'contact_hours_label',
        'address_label', 'phone_label', 'email_label',
        'form_nationality', 'form_nationality_ph',
        'form_qualification', 'form_qualification_ph',
        'form_qual_high', 'form_qual_diploma', 'form_qual_bachelor', 'form_qual_master',
        'benefit1', 'benefit1_desc', 'benefit2', 'benefit2_desc',
        'benefit3', 'benefit3_desc', 'benefit4', 'benefit4_desc',
    ]))
    page_keys_map['contact'] = contact_keys
    page_keys_map['courses.html'] = page_keys_map['programs']
    # Also map for filenames
    page_keys_map['courses'] = page_keys_map['programs']
    
    for html_file in sorted(site_dir.glob("*.html")):
        fname = html_file.name
        print(f"  Reading: {fname}")
        
        content = html_file.read_text(encoding='utf-8')
        
        # Determine keys for this page
        base = fname.replace('.html', '')
        keys = page_keys_map.get(base, page_keys_map.get('index', []))
        keys = list(set(keys))
        
        # Filter to only keys that exist in translations
        existing_keys = [k for k in keys if k in lang_data['ar'] and lang_data['ar'][k]]
        
        # Process each key - add data-i18n to the HTML
        for key in existing_keys:
            ar_text = lang_data['ar'][key]
            en_text = lang_data['en'].get(key, '')
            
            if not ar_text or len(ar_text) < 2:
                continue
            
            content = simple_text_mark(content, key, ar_text)
        
        # Count how many data-i18n attributes we added
        count = content.count('data-i18n="')
        print(f"  -> Added {count} data-i18n attributes")
        
        # Add i18n data and enhanced script tag
        i18n_script = f'\n<script>window.__i18n={json.dumps(lang_data, ensure_ascii=False, indent=2)};</script>\n'
        
        # Remove existing __i18n script if any
        content = re.sub(r'<script>window\.__i18n=.*?</script>', '', content, flags=re.DOTALL)
        
        # Update script.js to enhanced version or add the __i18n before it
        content = content.replace('</body>', f'{i18n_script}</body>')
        
        html_file.write_text(content, encoding='utf-8')
        print(f"  [OK] Updated: {fname}")
    
    # Generate enhanced script.js
    script_content = generate_enhanced_script(site_key)
    (site_dir / 'script.js').write_text(script_content, encoding='utf-8')
    print(f"  [OK] Written: script.js")


def generate_enhanced_script(site_key):
    """Generate enhanced script.js with working i18n toggle and all polish features."""
    site_name = site_key.replace('-', ' ').title()
    return f'''// {site_name} — Enhanced Script with i18n + Polish Features
document.addEventListener('DOMContentLoaded', () => {{
  // ===== Loading Screen =====
  const loadingEl = document.getElementById('loading');
  if (loadingEl) setTimeout(() => loadingEl.classList.add('hide'), 600);

  // ===== Mobile Menu =====
  const menuToggle = document.getElementById('menuToggle');
  const navLinks = document.getElementById('navLinks');
  if (menuToggle && navLinks) {{
    menuToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
    navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));
  }}

  // ===== ACTIVE NAV LINK =====
  const navEls = navLinks?.querySelectorAll('a');
  if (navEls) {{
    const currentFile = window.location.pathname.split('/').pop() || 'index.html';
    navEls.forEach(a => {{
      const href = a.getAttribute('href');
      if (href === currentFile || (currentFile === 'index.html' && href === 'index.html') || (currentFile === '' && href === 'index.html')) {{
        a.classList.add('active');
      }}
    }});
  }}

  // ===== LANGUAGE TOGGLE WITH FULL i18n =====
  const langToggle = document.getElementById('langToggle');
  let currentLang = document.documentElement.lang || 'ar';

  function applyTranslation(lang) {{
    if (!window.__i18n || !window.__i18n[lang]) return;
    const dict = window.__i18n[lang];
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    if (langToggle) langToggle.textContent = dict.lang_btn || (lang === 'ar' ? 'EN' : 'عربي');

    // Method 1: Walk all elements and match by data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {{
      const key = el.getAttribute('data-i18n');
      const isHtml = el.hasAttribute('data-i18n-html');
      const trans = dict[key];
      if (trans) {{
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{
          // For placeholder translations
          const phKey = el.getAttribute('data-i18n-ph');
          if (phKey && dict[phKey]) el.placeholder = dict[phKey];
        }} else if (el.tagName === 'OPTION') {{
          el.textContent = trans;
        }} else if (el.tagName === 'META') {{
          el.content = trans.replace(/<[^>]+>/g, '');
        }} else if (el.tagName === 'TITLE') {{
          el.textContent = trans.replace(/<[^>]+>/g, '');
        }} else if (isHtml) {{
          el.innerHTML = trans;
        }} else {{
          el.innerHTML = trans;
        }}
      }}
    }});

    // Method 2: Match elements by their text content against the dictionary
    // For elements that we somehow missed
    document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, a, button, li, td, th, label, cite, strong, em, small').forEach(el => {{
      if (el.hasAttribute('data-i18n')) return; // Already handled
      if (el.children.length > 0 && !el.querySelector('[data-i18n]')) return; // Has complex children
      if (!el.textContent || el.textContent.trim().length < 3) return;
      // Only match if el contains direct text (not nested)
      const directText = Array.from(el.childNodes)
        .filter(n => n.nodeType === 3)
        .map(n => n.textContent.trim())
        .join('');
      if (directText.length < 3) return;
      
      const text = (el.textContent || '').trim();
      // Look up in current lang dict value
      for (const [key, value] of Object.entries(dict)) {{
        if (!value) continue;
        const cleanValue = value.replace(/<[^>]+>/g, '').trim();
        if (cleanValue === text || cleanValue === directText) {{
          const isHtmlValue = value !== cleanValue;
          el.setAttribute('data-i18n', key);
          if (isHtmlValue) el.setAttribute('data-i18n-html', 'true');
          el.innerHTML = dict[key];
          break;
        }}
      }}
    }});
  }}

  if (langToggle) {{
    // Apply saved preference
    const saved = localStorage.getItem('{site_key}_lang');
    if (saved && saved !== currentLang) {{
      currentLang = saved;
    }}
    applyTranslation(currentLang);

    langToggle.addEventListener('click', () => {{
      currentLang = currentLang === 'ar' ? 'en' : 'ar';
      localStorage.setItem('{site_key}_lang', currentLang);
      applyTranslation(currentLang);
    }});
  }}

  // ===== SCROLL ANIMATIONS =====
  const observer = new IntersectionObserver(entries => {{
    entries.forEach(entry => {{
      if (entry.isIntersecting) {{
        entry.target.classList.add('show');
        observer.unobserve(entry.target);
      }}
    }});
  }}, {{ threshold: 0.1, rootMargin: '0px 0px -40px 0px' }});

  document.querySelectorAll('.fade-in, [class*="feat-"], [class*="prog-"], [class*="waha-"], .why-card, .program-full-card').forEach(el => {{
    if (!el.classList.contains('fade-in')) el.classList.add('fade-in');
    observer.observe(el);
  }});

  // ===== BACK TO TOP BUTTON =====
  let backToTop = document.getElementById('backToTop');
  if (!backToTop) {{
    backToTop = document.createElement('button');
    backToTop.id = 'backToTop';
    backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTop.setAttribute('data-i18n', 'back_to_top');
    backToTop.setAttribute('aria-label', 'Back to top');
    Object.assign(backToTop.style, {{
      position: 'fixed', bottom: '24px', right: '24px', zIndex: '999',
      width: '44px', height: '44px', borderRadius: '12px',
      background: 'var(--primary-uni, var(--coral, #7c3aed))',
      color: '#fff', border: 'none', cursor: 'pointer',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontSize: '1.1rem', opacity: '0', transform: 'translateY(20px)',
      transition: '0.4s', boxShadow: '0 4px 16px rgba(0,0,0,.3)'
    }});
    document.body.appendChild(backToTop);

    window.addEventListener('scroll', () => {{
      const show = window.scrollY > 400;
      backToTop.style.opacity = show ? '1' : '0';
      backToTop.style.transform = show ? 'translateY(0)' : 'translateY(20px)';
      backToTop.style.pointerEvents = show ? 'auto' : 'none';
    }});
    backToTop.addEventListener('click', () => window.scrollTo({{ top: 0, behavior: 'smooth' }}));
  }}

  // ===== COUNTER ANIMATION =====
  const counterObserver = new IntersectionObserver(entries => {{
    entries.forEach(entry => {{
      if (entry.isIntersecting) {{
        const el = entry.target;
        const target = parseInt(el.dataset.target);
        if (!target || el.dataset.animated === 'true') return;
        el.dataset.animated = 'true';
        let current = 0;
        const step = Math.max(1, Math.ceil(target / 50));
        const timer = setInterval(() => {{
          current = Math.min(current + step, target);
          if (el.dataset.suffix) {{
            el.textContent = current.toLocaleString() + el.dataset.suffix;
          }} else {{
            el.textContent = current.toLocaleString() + '+';
          }}
          if (current >= target) clearInterval(timer);
        }}, 20);
        counterObserver.unobserve(el);
      }}
    }});
  }}, {{ threshold: 0.5 }});
  document.querySelectorAll('[data-target]').forEach(el => counterObserver.observe(el));

  // ===== FORM HANDLING =====
  document.querySelectorAll('form').forEach(form => {{
    form.addEventListener('submit', e => {{
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      if (btn) btn.disabled = true;

      const msgBox = document.createElement('div');
      msgBox.style.cssText = 'padding:14px 18px;margin-top:16px;border-radius:10px;background:rgba(74,222,128,.15);color:#4ade80;text-align:center;font-weight:600;';

      const lang = currentLang;
      const dict = window.__i18n?.[lang];
      msgBox.textContent = dict?.form_success || (lang === 'ar' ? '✓ تم إرسال الطلب بنجاح!' : '✓ Form submitted successfully!');
      form.appendChild(msgBox);

      setTimeout(() => {{ form.reset(); if (btn) btn.disabled = false; }}, 2000);
      setTimeout(() => msgBox.remove(), 4000);
    }});
  }});

  // ===== SMOOTH SCROLL FOR ANCHOR LINKS =====
  document.querySelectorAll('a[href^="#"]').forEach(a => {{
    a.addEventListener('click', e => {{
      e.preventDefault();
      const target = document.querySelector(a.getAttribute('href'));
      if (target) target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }});
  }});

  // ===== FILTER TABS (for program pages) =====
  const filterBtns = document.querySelectorAll('.filter-btn');
  if (filterBtns.length > 0) {{
    filterBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        filterBtns.forEach(b => {{
          b.style.background = 'var(--bg-card)';
          b.style.color = '';
        }});
        btn.style.background = 'var(--coral, var(--primary-uni))';
        btn.style.color = '#fff';
      }});
    }});
  }}

  console.log('%c{site_name}','color:#7c3aed;font-size:1.2rem;font-weight:bold');
  console.log('Lang:', currentLang, '| Keys:', Object.keys(window.__i18n?.ar || {{}}).length);
}});
'''


def main():
    for site_key in SITES.keys():
        process_site(site_key)
    
    print(f"\n{'='*60}")
    print("ALL SITES PROCESSED!")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
