#!/usr/bin/env python3
"""
Fix ONE site at a time: 01-alriyadh-academy
Clean approach: BeautifulSoup to add data-i18n to every translatable element.
Then clean script.js with EN/AR toggle that just swaps by data-i18n.
"""
import json, re
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(r"C:\Users\paule\OneDrive\Desktop\Arabix Theme\education")
SITE = "01-alriyadh-academy"
DIR = BASE / SITE

# Translation data
I18N = {
    "ar": {
        "site_name": "أكاديمية الرياض",
        "site_tagline": "التعليم في أبهى صوره",
        "nav_home": "الرئيسية",
        "nav_about": "عن الأكاديمية",
        "nav_programs": "البرامج",
        "nav_contact": "اتصل بنا",
        "lang_btn": "EN",
        "hero_tag": "منذ ١٩٩٥ — منذ ١٩٩٥",
        "hero_stat1": "عاماً من التميز",
        "hero_stat2": "خريج",
        "hero_stat3": "برنامج",
        "feat1_title": "تعليم معتمد",
        "feat1_desc": "جميع برامجنا معتمدة من وزارة التعليم السعودية ومنظمة الاعتماد الأكاديمي الدولية.",
        "feat2_title": "كفاءات متميزة",
        "feat2_desc": "أكثر من ٢٠٠ عضو هيئة تدريس من حملة الدكتوراه والماجستير من أفضل الجامعات العالمية.",
        "feat3_title": "بيئة محفزة",
        "feat3_desc": "حرم جامعي متكامل بمساحة ٥٠ ألف متر مربع يشمل مختبرات ومكتبات ومرافق رياضية.",
        "feat4_title": "شراكات عالمية",
        "feat4_desc": "اتفاقيات تبادل طلابي مع ١٥ جامعة في ٨ دول حول العالم.",
        "footer_links": "روابط",
        "footer_about": "عن الأكاديمية",
        "footer_progs": "البرامج",
        "footer_services": "الخدمات الطلابية",
        "footer_library": "المكتبة الرقمية",
        "footer_prog1": "علوم الحاسب",
        "footer_prog2": "الهندسة",
        "footer_prog3": "الطب",
        "footer_prog4": "إدارة الأعمال",
        "footer_contact": "تواصل",
        "footer_address": "الرياض — طريق الملك عبدالله",
        "footer_phone": "٩٢٠٠١١٢٢٣",
        "footer_email": "info@riyadh-academy.edu.sa",
        "footer_hours": "٧:٠٠ ص — ٩:٠٠ م",
        "footer_copy": "أكاديمية الرياض — جميع الحقوق محفوظة.",
        "cta_title": "ابدأ رحلتك معنا اليوم",
        "cta_desc": "سجل الآن وانطلق نحو مستقبل مشرق",
        "cta_btn": "تسجيل الآن",
        "programs_btn": "برامجنا",
        "learn_more": "اكتشف المزيد",
        "all_programs": "استعرض جميع البرامج",
        "director_say": "كلمة",
        "director_quote": "\"نؤمن في أكاديمية الرياض أن التعليم ليس مجرد نقل للمعرفة، بل بناء للإنسان والمجتمع. نسعى دائماً لتقديم تعليم متميز يجمع بين القيم الأصيلة وأحدث المناهج العالمية.\"",
        "director_name": "— د. عبدالعزيز السليم، مدير الأكاديمية",
        "sec_why_title": "لماذا أكاديمية الرياض؟",
        "sec_why_desc": "أكثر من ربع قرن من العطاء التعليمي يجمع بين الأصالة والابتكار",
        "sec_progs_title": "برامجنا الأكاديمية",
        "sec_progs_desc": "مسارات تعليمية متنوعة تناسب جميع الطموحات",
        "prog1_name": "علوم الحاسب",
        "prog1_badge": "بكالوريوس",
        "prog1_desc": "الذكاء الاصطناعي، الأمن السيبراني، وهندسة البرمجيات",
        "prog2_name": "إدارة الأعمال",
        "prog2_badge": "دبلوم",
        "prog2_desc": "قيادة، تسويق، وريادة أعمال",
        "prog3_name": "الهندسة",
        "prog3_badge": "ماجستير",
        "prog3_desc": "هندسة مدنية، كهربائية، وميكانيكية",
        "prog4_name": "الطب والجراحة",
        "prog4_badge": "بكالوريوس",
        "prog4_desc": "برنامج طبي متكامل مع تدريب سريري",
        "social_x": "تويتر",
        "social_insta": "انستغرام",
        "social_linkedin": "لينكد إن",
        "social_snap": "سناب شات",
        "social_yt": "يوتيوب",
        "page_title_about": "عن أكاديمية الرياض",
        "about_heading": "مسيرة عطاء",
        "about_p1": "تأسست أكاديمية الرياض عام ٢٠١٠ بموجب ترخيص من وزارة التعليم، بهدف تقديم تعليم متميز يجمع بين الأصالة والحداثة. منذ انطلاقتها، خرّجت الأكاديمية أكثر من ٥٠٠٠ طالب وطالبة التحقوا بأعرق الجامعات المحلية والعالمية.",
        "about_p2": "تمتد مساحة الحرم الجامعي على ٥٠ ألف متر مربع، ويضم ٣ مباني تعليمية مجهزة بأحدث التقنيات، ومكتبة مركزية تضم أكثر من ٣٠ ألف عنوان، وملاعب رياضية ومنشآت فنية.",
        "about_p3": "نفخر بشراكاتنا مع ١٥ جامعة دولية وبرامج تبادل طلابي مع مؤسسات تعليمية في أمريكا وبريطانيا وكندا.",
        "about_stat1": "خريج",
        "about_stat2": "متر مربع",
        "about_stat3": "جامعة شريكة",
    },
    "en": {
        "site_name": "Al-Riyadh Academy",
        "site_tagline": "Education at Its Finest",
        "nav_home": "Home",
        "nav_about": "About Us",
        "nav_programs": "Programs",
        "nav_contact": "Contact",
        "lang_btn": "عربي",
        "hero_tag": "Since 1995 — Since 1995",
        "hero_stat1": "Years of Excellence",
        "hero_stat2": "Graduates",
        "hero_stat3": "Programs",
        "feat1_title": "Accredited Education",
        "feat1_desc": "All our programs are accredited by the Saudi Ministry of Education and the International Academic Accreditation Organization.",
        "feat2_title": "Distinguished Staff",
        "feat2_desc": "Over 200 faculty members with PhDs and Masters from the world's best universities.",
        "feat3_title": "Inspiring Environment",
        "feat3_desc": "Integrated campus of 50,000 sqm with labs, libraries, and sports facilities.",
        "feat4_title": "Global Partnerships",
        "feat4_desc": "Student exchange agreements with 15 universities in 8 countries worldwide.",
        "footer_links": "Links",
        "footer_about": "About Us",
        "footer_progs": "Programs",
        "footer_services": "Student Services",
        "footer_library": "Digital Library",
        "footer_prog1": "Computer Science",
        "footer_prog2": "Engineering",
        "footer_prog3": "Medicine",
        "footer_prog4": "Business Admin",
        "footer_contact": "Contact",
        "footer_address": "Riyadh — King Abdullah Road",
        "footer_phone": "920011223",
        "footer_email": "info@riyadh-academy.edu.sa",
        "footer_hours": "7:00 AM — 9:00 PM",
        "footer_copy": "Al-Riyadh Academy — All Rights Reserved.",
        "cta_title": "Start Your Journey With Us Today",
        "cta_desc": "Register now and step toward a bright future",
        "cta_btn": "Register Now",
        "programs_btn": "Our Programs",
        "learn_more": "Discover More",
        "all_programs": "View All Programs",
        "director_say": "Message from",
        "director_quote": "\"At Al-Riyadh Academy, we believe education is not just transferring knowledge, but building individuals and society. We always strive to provide distinguished education blending authentic values with the latest global curricula.\"",
        "director_name": "— Dr. Abdulaziz Al-Saleem, Academy Director",
        "sec_why_title": "Why Al-Riyadh Academy?",
        "sec_why_desc": "Over a quarter century of educational excellence blending tradition with innovation",
        "sec_progs_title": "Our Academic Programs",
        "sec_progs_desc": "Diverse educational paths for all ambitions",
        "prog1_name": "Computer Science",
        "prog1_badge": "Bachelor's",
        "prog1_desc": "AI, Cybersecurity, and Software Engineering",
        "prog2_name": "Business Admin",
        "prog2_badge": "Diploma",
        "prog2_desc": "Leadership, Marketing, and Entrepreneurship",
        "prog3_name": "Engineering",
        "prog3_badge": "Master's",
        "prog3_desc": "Civil, Electrical, and Mechanical Engineering",
        "prog4_name": "Medicine & Surgery",
        "prog4_badge": "Bachelor's",
        "prog4_desc": "Integrated medical program with clinical training",
        "social_x": "Twitter",
        "social_insta": "Instagram",
        "social_linkedin": "LinkedIn",
        "social_snap": "Snapchat",
        "social_yt": "YouTube",
        "page_title_about": "About Al-Riyadh Academy",
        "about_heading": "A Journey of Excellence",
        "about_p1": "Founded in 2010 under the Ministry of Education license, Al-Riyadh Academy aims to provide distinguished education blending tradition with modernity. Since its inception, the academy has graduated over 5,000 students who joined prestigious universities locally and abroad.",
        "about_p2": "The campus spans 50,000 square meters, featuring 3 educational buildings equipped with latest technology, a central library with over 30,000 titles, sports facilities and arts centers.",
        "about_p3": "We pride ourselves on partnerships with 15 international universities and student exchange programs with institutions in the US, UK, and Canada.",
        "about_stat1": "Graduates",
        "about_stat2": "Square Meters",
        "about_stat3": "Partner Universities",
    }
}


# Build key->[text_matches] lookup
# For each key, we want all Arabic text forms it might match
def build_lookups():
    """Return dict: key -> set of possible Arabic text matches (stripped)"""
    lookup = {}
    for key, ar_val in I18N["ar"].items():
        if not ar_val:
            continue
        clean = ar_val.strip()
        # Also remove HTML tags for matching
        clean_nohtml = re.sub(r'<[^>]+>', '', clean).strip()
        if clean:
            lookup.setdefault(key, set()).add(clean)
        if clean_nohtml and clean_nohtml != clean:
            lookup.setdefault(key, set()).add(clean_nohtml)
        # Also store first few words for short matching
    return lookup


def extract_text(el):
    """Get clean text content of an element (ignoring nested tags)"""
    return re.sub(r'\s+', ' ', el.get_text()).strip()


def tag_element(soup, el, key, lang_data):
    """Add data-i18n to an element if not already present"""
    if el.has_attr('data-i18n'):
        return False
    el['data-i18n'] = key
    return True


def process_file(html_file):
    """Process a single HTML file - add data-i18n attributes"""
    print(f"\n--- {html_file.name} ---")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Remove any existing i18n scripts and data attributes
    html = re.sub(r'<script>window\.__i18n=.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'\s*data-i18n(?:-html)?="[^"]*"', '', html)
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Build lookup
    lookup = build_lookups()
    # Reverse lookup: text -> key
    text_to_key = {}
    for key, texts in lookup.items():
        for t in texts:
            text_to_key[t] = key
    
    # Also add English texts to reverse lookup (for when page is in en mode)
    for key, en_val in I18N["en"].items():
        if en_val:
            clean = en_val.strip()
            clean_nohtml = re.sub(r'<[^>]+>', '', clean).strip()
            if clean:
                text_to_key[clean] = key
            if clean_nohtml and clean_nohtml != clean:
                text_to_key[clean_nohtml] = key
    
    tagged = 0
    
    # Tag elements by matching their text content
    # Order: more specific selectors first
    for tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'a', 'button', 'li', 'label', 'cite', 'strong', 'em', 'div', 'small']:
        for el in soup.find_all(tag_name):
            if el.has_attr('data-i18n'):
                continue
            # Skip elements with block-level children
            has_block_child = any(
                c.name in ['div', 'section', 'nav', 'header', 'footer', 'main', 'aside', 'article', 'form', 'table', 'ul', 'ol']
                for c in el.find_all(recursive=False)
            )
            if has_block_child and tag_name != 'div':
                continue
            
            text = extract_text(el)
            if not text or len(text) < 2:
                continue
            
            # Check divs more carefully - only tag if they directly contain text
            if tag_name == 'div':
                direct_text = ''
                for child in el.children:
                    if child.name is None:  # NavigableString
                        direct_text += str(child).strip()
                if not direct_text or len(direct_text) < 2:
                    continue
                text = re.sub(r'\s+', ' ', direct_text).strip()
            
            if text in text_to_key:
                key = text_to_key[text]
                el['data-i18n'] = key
                tagged += 1
                continue
    
    print(f"  Tagged {tagged} elements with data-i18n")
    
    # Verify: check which keys are used vs available
    used_keys = set()
    for el in soup.find_all(attrs={'data-i18n': True}):
        used_keys.add(el['data-i18n'])
    
    ar_keys = set(k for k in I18N["ar"].keys() if I18N["ar"][k])
    unused = ar_keys - used_keys
    if unused:
        print(f"  UNUSED keys ({len(unused)}): {sorted(unused)[:10]}...")
    
    # Inject i18n data script before </body>
    i18n_script = soup.new_tag('script')
    i18n_script.string = f'window.__i18n={json.dumps(I18N, ensure_ascii=False)};'
    soup.body.append(i18n_script)
    
    # Write back
    html_out = str(soup)
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_out)
    print(f"  [OK] Written")
    return tagged


# Process index.html first (homepage)
for html_file in sorted(DIR.glob("*.html")):
    process_file(html_file)


print(f"\n{'='*60}")
print(f"HTML files tagged. Now writing script.js...")
print(f"{'='*60}")

# Write fresh script.js - clean and simple
SCRIPT = '''// Al-Riyadh Academy — i18n toggle + polish
(function() {
  'use strict';

  const LS_KEY = 'aracademy_lang';
  let currentLang = localStorage.getItem(LS_KEY) || document.documentElement.getAttribute('data-lang') || 'ar';

  // Set initial lang attr
  document.documentElement.lang = currentLang;
  document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';

  // ===== Apply translation =====
  function applyTranslation(lang) {
    if (!window.__i18n || !window.__i18n[lang]) return;
    const dict = window.__i18n[lang];
    const els = document.querySelectorAll('[data-i18n]');

    els.forEach(function(el) {
      const key = el.getAttribute('data-i18n');
      const val = dict[key];
      if (!val) return;

      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        // placeholder only
        return;
      }
      if (el.tagName === 'OPTION') {
        el.textContent = val.replace(/<[^>]+>/g, '');
        return;
      }
      // Normal elements — set HTML (supports inline tags like <span>)
      el.innerHTML = val;
    });

    // Update lang attribute and direction
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';

    // Toggle button text
    const toggleBtn = document.getElementById('langToggle');
    if (toggleBtn) toggleBtn.textContent = lang === 'ar' ? 'EN' : 'عربي';

    // Update title
    const titleKey = document.querySelector('title');
    if (titleKey) {
      const siteName = dict.site_name || '';
      const pageKey = document.querySelector('[data-i18n-page-title]');
      let pageTitle = '';
      if (pageKey) pageTitle = dict[pageKey.getAttribute('data-i18n-page-title')] || '';
      document.title = pageTitle ? pageTitle + ' | ' + siteName : siteName;
    }

    currentLang = lang;
    localStorage.setItem(LS_KEY, lang);
  }

  // ===== Load handler =====
  document.addEventListener('DOMContentLoaded', function() {
    // Loading screen
    var loading = document.getElementById('loading');
    if (loading) setTimeout(function() { loading.classList.add('hide'); }, 600);

    // Mobile menu
    var menuToggle = document.getElementById('menuToggle');
    var navLinks = document.getElementById('navLinks');
    if (menuToggle && navLinks) {
      menuToggle.addEventListener('click', function() { navLinks.classList.toggle('open'); });
      navLinks.querySelectorAll('a').forEach(function(a) {
        a.addEventListener('click', function() { navLinks.classList.remove('open'); });
      });
    }

    // Active nav link
    if (navLinks) {
      var currentFile = window.location.pathname.split('/').pop() || 'index.html';
      navLinks.querySelectorAll('a').forEach(function(a) {
        var href = a.getAttribute('href');
        if (href === currentFile || (currentFile === 'index.html' && href === 'index.html') || (currentFile === '' && href === 'index.html')) {
          a.classList.add('active');
        }
      });
    }

    // Lang toggle
    var langToggle = document.getElementById('langToggle');
    if (langToggle && window.__i18n) {
      applyTranslation(currentLang);
      langToggle.addEventListener('click', function() {
        applyTranslation(currentLang === 'ar' ? 'en' : 'ar');
      });
    }

    // Counter animation
    var counterObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var target = parseInt(el.getAttribute('data-target'));
        if (!target || el.getAttribute('data-animated') === 'true') return;
        el.setAttribute('data-animated', 'true');
        var current = 0;
        var step = Math.max(1, Math.ceil(target / 50));
        var timer = setInterval(function() {
          current = Math.min(current + step, target);
          el.textContent = current.toLocaleString() + '+';
          if (current >= target) clearInterval(timer);
        }, 20);
        counterObserver.unobserve(el);
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('[data-target]').forEach(function(el) { counterObserver.observe(el); });

    // Scroll animations (fade-in)
    var animObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('show');
          animObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.feat-card, .prog-card, .sec-head, .director-msg, .hero-content').forEach(function(el) {
      el.classList.add('fade-in');
      animObserver.observe(el);
    });

    // Back to top
    var backBtn = document.getElementById('backToTop');
    if (!backBtn) {
      backBtn = document.createElement('button');
      backBtn.id = 'backToTop';
      backBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
      backBtn.setAttribute('aria-label', 'Back to top');
      backBtn.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:999;width:44px;height:44px;border-radius:12px;background:#1a5c2a;color:#fff;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1.1rem;opacity:0;transform:translateY(20px);transition:0.4s;box-shadow:0 4px 16px rgba(0,0,0,.3);pointer-events:none;';
      document.body.appendChild(backBtn);
      window.addEventListener('scroll', function() {
        var show = window.scrollY > 400;
        backBtn.style.opacity = show ? '1' : '0';
        backBtn.style.transform = show ? 'translateY(0)' : 'translateY(20px)';
        backBtn.style.pointerEvents = show ? 'auto' : 'none';
      });
      backBtn.addEventListener('click', function() { window.scrollTo({ top: 0, behavior: 'smooth' }); });
    }

    // Form handling
    document.querySelectorAll('form').forEach(function(form) {
      form.addEventListener('submit', function(e) {
        e.preventDefault();
        var btn = form.querySelector('button[type="submit"], button:not([type])');
        if (btn) btn.disabled = true;
        var dict = window.__i18n && window.__i18n[currentLang];
        var msg = document.createElement('div');
        msg.style.cssText = 'padding:14px 18px;margin-top:16px;border-radius:10px;background:rgba(74,222,128,.15);color:#4ade80;text-align:center;font-weight:600;';
        msg.textContent = (dict && dict.form_success) || (currentLang === 'ar' ? '✓ تم إرسال الطلب بنجاح!' : '✓ Submitted successfully!');
        form.appendChild(msg);
        setTimeout(function() { form.reset(); if (btn) btn.disabled = false; }, 2000);
        setTimeout(function() { msg.remove(); }, 4500);
      });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function(a) {
      a.addEventListener('click', function(e) {
        var target = document.querySelector(a.getAttribute('href'));
        if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
      });
    });
  });
})();
'''

(DIR / 'script.js').write_text(SCRIPT, encoding='utf-8')
print("  [OK] script.js written")
print("\n✅ Done! All files processed. Deploy and test.")
