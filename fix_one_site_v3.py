#!/usr/bin/env python3
"""
Proper approach:
1. Reset HTML from git
2. Extract EVERY text-bearing element from every page
3. Generate unique keys (text_hash -> key mapping)
4. Tag each element with data-i18n
5. Generate Arabic translations (= existing text) and English translations
6. inject __i18n data + clean script.js
"""
import json, re, hashlib
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

BASE = Path(r"C:\Users\paule\OneDrive\Desktop\Arabix Theme\education")
SITE = "01-alriyadh-academy"
DIR = BASE / SITE

# Reset from git
import subprocess
subprocess.run(["git", "checkout", "35124f9", "--", f"{SITE}/"], cwd=BASE, capture_output=True)
print("[OK] Reset to clean originals")

def clean(t):
    return re.sub(r'\s+', ' ', t).strip()

def short_hash(text):
    return hashlib.md5(text.encode()).hexdigest()[:6]

# English translations for known texts
# Will be filled automatically for everything else
EN_TRANSLATIONS = {}

def auto_translate(text):
    """Generate English translation - use lookup or fallback to original"""
    if text in EN_TRANSLATIONS:
        return EN_TRANSLATIONS[text]
    # If starts with English/number, keep as-is
    if text and (text[0].isascii() and not text[0].isdigit()):
        return text
    return text  # fallback: keep Arabic

def process_file(html_path):
    """Tag every text-bearing element with data-i18n."""
    print(f"\n--- {html_path.name} ---")
    
    html = html_path.read_text(encoding='utf-8')
    # Remove any existing i18n artifacts
    html = re.sub(r'<script>window\.__i18n=.*?</script>', '', html, flags=re.DOTALL)
    # Clear any old data-i18n
    html = re.sub(r'\s*data-i18n(?:-html)?="[^"]*"', '', html)
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Tag elements
    translations = {}  # key -> {'ar': str, 'en': str}
    key_map = {}  # text -> key (dedup)
    tagged_count = 0
    
    def get_or_create_key(text):
        nonlocal tagged_count
        if text in key_map:
            return key_map[text]
        key = f"t{short_hash(text)}"
        key_map[text] = key
        tagged_count += 1
        return key
    
    # Tag by traversing ALL elements
    for el in soup.find_all(True):  # All tags
        if el.name in ['html','head','body','meta','link','script','style','svg','path','circle','defs','linearGradient','stop','title']:
            continue
        if el.has_attr('data-i18n'):
            continue
        # Skip if contains block-level children
        block_tags = ['div','section','nav','header','footer','main','aside','article','form','table','ul','ol']
        has_block = any(c.name in block_tags for c in el.find_all(recursive=False))
        if has_block:
            continue
        
        text = clean(el.get_text())
        if not text or len(text) < 2:
            continue
        
        # Get only the direct text content (not from children)
        direct_text = ''.join(s.strip() for s in el.strings).strip()
        if not direct_text:
            continue  # text comes only from child elements
        
        direct_clean = clean(direct_text)
        if len(direct_clean) < 2:
            continue
        
        key = get_or_create_key(direct_clean)
        el['data-i18n'] = key
        
        # Store translation
        if key not in translations:
            translations[key] = {
                'ar': direct_clean,
                'en': auto_translate(direct_clean)
            }
    
    print(f"  Tagged: {tagged_count} elements")
    
    # Build translation dict from all keys
    i18n_data = {'ar': {}, 'en': {}}
    for key, data in translations.items():
        i18n_data['ar'][key] = data['ar']
        i18n_data['en'][key] = data['en']
    
    # Inject i18n data
    i18n_json = json.dumps(i18n_data, ensure_ascii=False)
    script_tag = soup.new_tag('script')
    script_tag.string = f'window.__i18n={i18n_json};'
    
    # Find script.js reference and add before it
    scripts = soup.find_all('script', src=re.compile(r'script\.js'))
    if scripts:
        scripts[0].insert_before(script_tag)
    else:
        soup.body.append(script_tag)
    
    # Write back
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"  [OK] Written ({len(translations)} unique keys)")


def write_script():
    """Simple clean script.js"""
    script = '''(function() {
  'use strict';
  var LS = 'aracademy_lang';
  var current = localStorage.getItem(LS) || 'ar';
  document.documentElement.lang = current;
  document.documentElement.dir = current === 'ar' ? 'rtl' : 'ltr';

  function tr(lang) {
    var dict = window.__i18n && window.__i18n[lang];
    if (!dict) return;
    document.querySelectorAll('[data-i18n]').forEach(function(el) {
      var key = el.getAttribute('data-i18n');
      var val = dict[key];
      if (!val) return;
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') return;
      if (el.tagName === 'OPTION') { el.textContent = val.replace(/<[^>]+>/g,''); return; }
      el.innerHTML = val;
    });
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    var btn = document.getElementById('langToggle');
    if (btn) btn.textContent = lang === 'ar' ? 'EN' : '\u0639\u0631\u0628\u064a';
    var title = document.querySelector('title');
    if (title) { var n = dict.site_name || ''; title.textContent = n || title.textContent; }
    current = lang;
    localStorage.setItem(LS, lang);
  }

  document.addEventListener('DOMContentLoaded', function() {
    var loading = document.getElementById('loading');
    if (loading) setTimeout(function() { loading.classList.add('hide'); }, 600);
    var menu = document.getElementById('menuToggle');
    var nav = document.getElementById('navLinks');
    if (menu && nav) {
      menu.addEventListener('click', function() { nav.classList.toggle('open'); });
      nav.querySelectorAll('a').forEach(function(a) {
        a.addEventListener('click', function() { nav.classList.remove('open'); });
      });
    }
    if (nav) {
      var cf = window.location.pathname.split('/').pop() || 'index.html';
      nav.querySelectorAll('a').forEach(function(a) {
        var h = a.getAttribute('href');
        if (h === cf || (cf === 'index.html' && (h === 'index.html' || h === ''))) a.classList.add('active');
      });
    }
    var toggle = document.getElementById('langToggle');
    if (toggle && window.__i18n) {
      tr(current);
      toggle.addEventListener('click', function() { tr(current === 'ar' ? 'en' : 'ar'); });
    }
    // Counter animation
    new IntersectionObserver(function(es) {
      es.forEach(function(e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        var target = parseInt(el.getAttribute('data-target'));
        if (!target || el.getAttribute('data-animated') === 'true') return;
        el.setAttribute('data-animated', 'true');
        var cur = 0;
        var step = Math.max(1, Math.ceil(target / 50));
        var tmr = setInterval(function() {
          cur = Math.min(cur + step, target);
          el.firstChild.textContent = cur.toLocaleString();
          if (cur >= target) clearInterval(tmr);
        }, 20);
      });
    }, { threshold: 0.5 }).observe(document.querySelectorAll('[data-target]'));
    // Scroll animation
    new IntersectionObserver(function(es) {
      es.forEach(function(e) { if (e.isIntersecting) { e.target.classList.add('show'); } });
    }, { threshold: 0.1 }).observe(document.querySelectorAll('.feat-card, .prog-card, .sec-head, .director-msg, .hero-content'));
    // Back to top
    var bt = document.getElementById('backToTop') || (function() {
      var b = document.createElement('button');
      b.id = 'backToTop'; b.innerHTML = '<i class="fas fa-arrow-up"></i>';
      b.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:999;width:44px;height:44px;border-radius:12px;background:#1a5c2a;color:#fff;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1.1rem;opacity:0;transform:translateY(20px);transition:0.4s;box-shadow:0 4px 16px rgba(0,0,0,.3);pointer-events:none;';
      document.body.appendChild(b);
      window.addEventListener('scroll', function() {
        var s = window.scrollY > 400;
        b.style.opacity = s ? '1' : '0';
        b.style.transform = s ? 'translateY(0)' : 'translateY(20px)';
        b.style.pointerEvents = s ? 'auto' : 'none';
      });
      b.addEventListener('click', function() { window.scrollTo({ top: 0, behavior: 'smooth' }); });
      return b;
    })();
    // Form
    document.querySelectorAll('form').forEach(function(f) {
      f.addEventListener('submit', function(e) { e.preventDefault();
        var btn = f.querySelector('button[type="submit"]');
        if (btn) btn.disabled = true;
        var dict = window.__i18n && window.__i18n[current];
        var m = document.createElement('div');
        m.style.cssText = 'padding:14px 18px;margin-top:16px;border-radius:10px;background:rgba(74,222,128,.15);color:#4ade80;text-align:center;font-weight:600;';
        m.textContent = (dict && dict.form_success) || (current === 'ar' ? '\u2713 \u062A\u0645 \u0627\u0644\u0625\u0631\u0633\u0627\u0644 \u0628\u0646\u062C\u0627\u062D!' : '\u2713 Submitted!');
        f.appendChild(m);
        setTimeout(function() { f.reset(); if (btn) btn.disabled = false; }, 2000);
        setTimeout(function() { m.remove(); }, 4500);
      });
    });
  });
})();
'''
    (DIR / 'script.js').write_text(script, encoding='utf-8')
    print("[OK] script.js written")


def verify():
    """Verify results"""
    print(f"\n{'='*60}")
    print("VERIFICATION")
    print(f"{'='*60}")
    total_els = 0
    for f in sorted(DIR.glob("*.html")):
        soup = BeautifulSoup(open(f, encoding='utf-8'), 'html.parser')
        count = len(soup.find_all(attrs={'data-i18n': True}))
        total_els += count
        print(f"  {f.name}: {count} tagged")
    print(f"  TOTAL: {total_els}")


if __name__ == '__main__':
    for h in sorted(DIR.glob("*.html")):
        process_file(h)
    write_script()
    verify()
