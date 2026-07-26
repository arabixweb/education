#!/usr/bin/env python3
"""
Final i18n fix:
1. Remove ALL data-i18n attributes (broken ones included) from HTML files
2. Keep the injected window.__i18n data (dedupe if needed)
3. Write final script.js with runtime bidirectional text matching
"""
import json, re, sys
from pathlib import Path

BASE = Path(r"C:\Users\paule\OneDrive\Desktop\Arabix Theme\education")

# Load SITES dict from generate_i18n.py
with open(BASE / 'generate_i18n.py', 'r', encoding='utf-8') as f:
    content = f.read()
start = content.find("SITES = {}")
end = content.find("def get_main_script")
exec(content[start:end].strip())

print(f"Loaded: {list(SITES.keys())}")


def clean_html(html):
    """Remove all data-i18n / data-i18n-html attributes."""
    # Broken variants first: data-i18n="key data-i18n-html"
    html = re.sub(r'\s+data-i18n="[^"]*"', '', html)
    html = re.sub(r"\s+data-i18n='[^']*'", '', html)
    html = re.sub(r'\s+data-i18n-html="[^"]*"', '', html)
    html = re.sub(r'\s+data-i18n-html\b(?!=)', '', html)
    return html


SCRIPT_TEMPLATE = '''// __SITE_NAME__ — Final Script: i18n toggle + polish
document.addEventListener('DOMContentLoaded', () => {
  // ===== Loading Screen =====
  const loadingEl = document.getElementById('loading');
  if (loadingEl) setTimeout(() => loadingEl.classList.add('hide'), 600);

  // ===== Mobile Menu =====
  const menuToggle = document.getElementById('menuToggle');
  const navLinks = document.getElementById('navLinks');
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
    navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));
  }

  // ===== Active Nav Link =====
  if (navLinks) {
    const currentFile = window.location.pathname.split('/').pop() || 'index.html';
    navLinks.querySelectorAll('a').forEach(a => {
      const href = a.getAttribute('href');
      a.classList.toggle('active', href === currentFile || (currentFile === '' && href === 'index.html'));
    });
  }

  // ===== i18n: bidirectional runtime matching =====
  const langToggle = document.getElementById('langToggle');
  let currentLang = 'ar';

  function cleanText(s) { return (s || '').replace(/<[^>]+>/g, '').replace(/\\s+/g, ' ').trim(); }

  // Build lookup: cleanedText -> key (from both languages)
  const lookup = {};
  if (window.__i18n) {
    for (const lang of ['ar', 'en']) {
      const dict = window.__i18n[lang] || {};
      for (const [key, value] of Object.entries(dict)) {
        const c = cleanText(value);
        if (c.length >= 2) lookup[c] = key;
      }
    }
  }

  function tagElements() {
    // Tag translatable elements by matching their text against the lookup
    document.querySelectorAll('h1,h2,h3,h4,h5,h6,p,span,a,button,li,label,cite,option,strong,em,small,div').forEach(el => {
      if (el.hasAttribute('data-i18n')) return;
      // Skip elements with element children EXCEPT allowed inline tags (span, strong, em, i, b)
      const badChild = Array.from(el.children).some(c => !['SPAN','STRONG','EM','I','B','BR'].includes(c.tagName));
      if (badChild) return;
      const text = cleanText(el.textContent);
      if (text.length < 2) return;
      const key = lookup[text];
      if (key) el.setAttribute('data-i18n', key);
    });
  }

  function applyTranslation(lang) {
    if (!window.__i18n || !window.__i18n[lang]) return;
    const dict = window.__i18n[lang];
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      const trans = dict[key];
      if (!trans) return;
      if (el.tagName === 'OPTION') { el.textContent = cleanText(trans); }
      else if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') { /* placeholders below */ }
      else el.innerHTML = trans;
    });
    // Placeholders
    document.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(el => {
      const ph = el.getAttribute('data-i18n-ph');
      if (ph && dict[ph]) el.placeholder = dict[ph];
    });
    if (langToggle) langToggle.textContent = lang === 'ar' ? 'EN' : 'عربي';
    // Page title
    const titleKey = document.title && lookup[cleanText(document.title)];
    if (titleKey && dict[titleKey]) document.title = cleanText(dict[titleKey]);
  }

  if (langToggle && window.__i18n) {
    tagElements();
    const saved = localStorage.getItem('edu_lang');
    if (saved === 'en') { currentLang = 'en'; applyTranslation('en'); }
    langToggle.addEventListener('click', () => {
      currentLang = currentLang === 'ar' ? 'en' : 'ar';
      localStorage.setItem('edu_lang', currentLang);
      applyTranslation(currentLang);
    });
  }

  // ===== Scroll Animations =====
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('show'); observer.unobserve(e.target); } });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.fade-in, [class*="feat-"], [class*="prog-"], [class*="waha-"], .why-card, .program-full-card').forEach(el => {
    if (!el.classList.contains('fade-in')) el.classList.add('fade-in');
    observer.observe(el);
  });

  // ===== Counter Animation =====
  const counterObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseInt(el.dataset.target);
      if (!target || el.dataset.animated === 'true') return;
      el.dataset.animated = 'true';
      let current = 0;
      const step = Math.max(1, Math.ceil(target / 50));
      const timer = setInterval(() => {
        current = Math.min(current + step, target);
        el.textContent = current.toLocaleString() + '+';
        if (current >= target) clearInterval(timer);
      }, 20);
      counterObserver.unobserve(el);
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('[data-target]').forEach(el => counterObserver.observe(el));

  // ===== Back to Top =====
  let backToTop = document.getElementById('backToTop');
  if (!backToTop) {
    backToTop = document.createElement('button');
    backToTop.id = 'backToTop';
    backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTop.setAttribute('aria-label', 'Back to top');
    backToTop.style.cssText = 'position:fixed;bottom:24px;left:24px;z-index:999;width:44px;height:44px;border-radius:12px;background:__ACCENT__;color:#fff;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1.1rem;opacity:0;transform:translateY(20px);transition:0.4s;box-shadow:0 4px 16px rgba(0,0,0,.3);pointer-events:none;';
    document.body.appendChild(backToTop);
    window.addEventListener('scroll', () => {
      const show = window.scrollY > 400;
      backToTop.style.opacity = show ? '1' : '0';
      backToTop.style.transform = show ? 'translateY(0)' : 'translateY(20px)';
      backToTop.style.pointerEvents = show ? 'auto' : 'none';
    });
    backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  // ===== Form Handling =====
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"], button:not([type])');
      if (btn) btn.disabled = true;
      const dict = window.__i18n && window.__i18n[currentLang];
      const msgBox = document.createElement('div');
      msgBox.style.cssText = 'padding:14px 18px;margin-top:16px;border-radius:10px;background:rgba(74,222,128,.15);color:#4ade80;text-align:center;font-weight:600;';
      msgBox.textContent = (dict && dict.form_success) || (currentLang === 'ar' ? '✓ تم إرسال الطلب بنجاح!' : '✓ Submitted successfully!');
      form.appendChild(msgBox);
      setTimeout(() => { form.reset(); if (btn) btn.disabled = false; }, 2000);
      setTimeout(() => msgBox.remove(), 4500);
    });
  });

  // ===== Smooth scroll =====
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
    });
  });
});
'''

ACCENTS = {
    "01-alriyadh-academy": "#0d5c3f",
    "02-qudra-institute": "#2563eb",
    "03-noor-alhuda": "#c8a24a",
    "04-saudi-future-university": "#6d28d9",
    "05-alwaha-center": "#e87a5d",
}

for site_key, lang_data in SITES.items():
    site_dir = BASE / site_key
    if not site_dir.exists():
        continue
    print(f"\n=== {site_key} ===")
    
    for html_file in sorted(site_dir.glob("*.html")):
        html = html_file.read_text(encoding='utf-8')
        html = clean_html(html)
        # Remove existing injected i18n scripts (dedupe)
        html = re.sub(r'\s*<script>window\.__i18n=.*?</script>\s*', '\n', html, flags=re.DOTALL)
        # Inject fresh i18n data BEFORE script.js tag so it's available
        data_tag = f'<script>window.__i18n={json.dumps(lang_data, ensure_ascii=False)};</script>'
        if '<script src="script.js"></script>' in html:
            html = html.replace('<script src="script.js"></script>', f'{data_tag}\n<script src="script.js"></script>')
        else:
            html = html.replace('</body>', f'{data_tag}\n</body>')
        html_file.write_text(html, encoding='utf-8')
        print(f"  [OK] {html_file.name}")
    
    # Write final script.js
    script = SCRIPT_TEMPLATE.replace('__SITE_NAME__', site_key.replace('-', ' ').title())
    script = script.replace('__ACCENT__', ACCENTS.get(site_key, '#7c3aed'))
    (site_dir / 'script.js').write_text(script, encoding='utf-8')
    print(f"  [OK] script.js")

print("\nDONE - all sites cleaned and finalized")
