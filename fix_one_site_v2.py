#!/usr/bin/env python3
"""
Fix ONE site: 01-alriyadh-academy
Approach: reset from git (original clean), then use BeautifulSoup to statically
add data-i18n to EVERYTHING. Use fuzzy matching so nothing is missed.
"""
import json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(r"C:\Users\paule\OneDrive\Desktop\Arabix Theme\education")
SITE_DIR = BASE / "01-alriyadh-academy"

# Translation data - MUST match actual HTML text exactly
I18N = {
    "ar": {
        "site_name": "أكاديمية الرياض",
        "nav_home": "الرئيسية",
        "nav_about": "عن الأكاديمية",
        "nav_programs": "البرامج",
        "nav_contact": "اتصل بنا",
        "lang_btn": "EN",
        "lang_btn_ar": "عربي",
        "hero_badge": "منذ ١٩٩٥ — Since 1995",
        "hero_title": "شريكك في <span class='gold'>التميز التعليمي</span>",
        "hero_gold": "التميز التعليمي",
        "hero_desc": "نحو جيل واعٍ ومبدع — أكثر من ١٠ آلاف خريج وأكثر من ٢٠ برنامجاً تعليمياً معتمداً.",
        "hero_stat1_lbl": "عاماً من التميز",
        "hero_stat2_lbl": "خريج",
        "hero_stat3_lbl": "برنامج",
        "sec_why_title": "لماذا <span class='gold'>أكاديمية الرياض</span>؟",
        "sec_why_gold": "أكاديمية الرياض",
        "sec_why_desc": "أكثر من ربع قرن من العطاء التعليمي يجمع بين الأصالة والابتكار",
        "feat1_title": "تعليم معتمد",
        "feat1_desc": "جميع برامجنا معتمدة من وزارة التعليم السعودية ومنظمة الاعتماد الأكاديمي الدولية.",
        "feat2_title": "كفاءات متميزة",
        "feat2_desc": "أكثر من ٢٠٠ عضو هيئة تدريس من حملة الدكتوراه والماجستير من أفضل الجامعات العالمية.",
        "feat3_title": "بيئة محفزة",
        "feat3_desc": "حرم جامعي متكامل بمساحة ٥٠ ألف متر مربع يشمل مختبرات ومكتبات ومرافق رياضية.",
        "feat4_title": "شراكات عالمية",
        "feat4_desc": "اتفاقيات تبادل طلابي مع ١٥ جامعة في ٨ دول حول العالم.",
        "sec_progs_title": "برامجنا <span class='gold'>الأكاديمية</span>",
        "sec_progs_gold": "الأكاديمية",
        "sec_progs_desc": "مسارات تعليمية متنوعة تناسب جميع الطموحات",
        "prog1_badge": "بكالوريوس",
        "prog1_name": "علوم الحاسب",
        "prog1_desc": "الذكاء الاصطناعي، الأمن السيبراني، وهندسة البرمجيات",
        "prog2_badge": "دبلوم",
        "prog2_name": "إدارة الأعمال",
        "prog2_desc": "قيادة، تسويق، وريادة أعمال",
        "prog3_badge": "ماجستير",
        "prog3_name": "الهندسة",
        "prog3_desc": "هندسة مدنية، كهربائية، وميكانيكية",
        "prog4_badge": "بكالوريوس",
        "prog4_name": "الطب والجراحة",
        "prog4_desc": "برنامج طبي متكامل مع تدريب سريري",
        "all_programs": "استعرض جميع البرامج",
        "director_title": "كلمة <span class='gold'>المدير</span>",
        "director_gold": "المدير",
        "director_quote": "\"نؤمن في أكاديمية الرياض أن التعليم ليس مجرد نقل للمعرفة، بل بناء للإنسان والمجتمع. نسعى دائماً لتقديم تعليم متميز يجمع بين القيم الأصيلة وأحدث المناهج العالمية.\"",
        "director_name": "— د. عبدالعزيز السليم، مدير الأكاديمية",
        "cta_title": "ابدأ رحلتك معنا اليوم",
        "cta_desc": "سجل الآن وانطلق نحو مستقبل مشرق",
        "cta_btn": "تسجيل الآن",
        "footer_desc": "مؤسسة تعليمية رائدة في المملكة العربية السعودية منذ 1995.",
        "footer_links": "روابط",
        "footer_progs": "برامج",
        "footer_contact": "تواصل",
        "footer_contact_h4": "تواصل",
        "footer_about": "عن الأكاديمية",
        "footer_services": "الخدمات الطلابية",
        "footer_library": "المكتبة الرقمية",
        "footer_prog1": "علوم الحاسب",
        "footer_prog2": "الهندسة",
        "footer_prog3": "الطب",
        "footer_prog4": "إدارة الأعمال",
        "footer_address": "الرياض — طريق الملك عبدالله",
        "footer_phone": "920011223",
        "footer_email": "info@riyadh-academy.edu.sa",
        "footer_hours": "٧:٠٠ ص — ٩:٠٠ م",
        "footer_copy": "أكاديمية الرياض — جميع الحقوق محفوظة.",
        "programs_btn": "برامجنا",
        "learn_more": "اكتشف المزيد",
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
        "about_stat1_lbl": "خريج",
        "about_stat2_lbl": "متر مربع",
        "about_stat3_lbl": "جامعة شريكة",
        "about_stat1_num": "5000",
        "about_stat2_num": "50000",
        "about_stat3_num": "15",
        "page_title_contact": "اتصل بنا",
        "contact_heading": "تواصل معنا",
        "contact_legend": "نحن هنا لمساعدتك",
        "form_name": "الاسم",
        "form_email": "البريد الإلكتروني",
        "form_phone": "الجوال",
        "form_program_opt": "اختر البرنامج",
        "form_prog1": "علوم الحاسب",
        "form_prog2": "إدارة الأعمال",
        "form_prog3": "الهندسة",
        "form_prog4": "الطب",
        "form_message": "الرسالة",
        "form_submit": "إرسال",
        "form_success": "تم الإرسال بنجاح! سنتواصل معك قريباً.",
        "page_title_programs": "برامجنا",
        "programs_heading": "برامجنا الأكاديمية",
        "programs_intro": "مسارات تعليمية متنوعة تناسب جميع الطموحات",
        "breadcrumb_home": "الرئيسية",
        "breadcrumb_about": "عن الأكاديمية",
        "breadcrumb_programs": "البرامج",
        "breadcrumb_contact": "اتصل بنا",
    },
    "en": {
        "site_name": "Al-Riyadh Academy",
        "nav_home": "Home",
        "nav_about": "About Us",
        "nav_programs": "Programs",
        "nav_contact": "Contact",
        "lang_btn": "عربي",
        "lang_btn_ar": "EN",
        "hero_badge": "Since 1995",
        "hero_title": "Your Partner in <span class='gold'>Educational Excellence</span>",
        "hero_gold": "Educational Excellence",
        "hero_desc": "Towards a conscious and creative generation — over 10,000 graduates and 20 accredited programs.",
        "hero_stat1_lbl": "Years of Excellence",
        "hero_stat2_lbl": "Graduates",
        "hero_stat3_lbl": "Programs",
        "sec_why_title": "Why <span class='gold'>Al-Riyadh Academy</span>?",
        "sec_why_gold": "Al-Riyadh Academy",
        "sec_why_desc": "Over a quarter century of educational excellence blending tradition with innovation",
        "feat1_title": "Accredited Education",
        "feat1_desc": "All our programs are accredited by the Saudi Ministry of Education and the International Academic Accreditation Organization.",
        "feat2_title": "Distinguished Staff",
        "feat2_desc": "Over 200 faculty members with PhDs and Masters from the world's best universities.",
        "feat3_title": "Inspiring Environment",
        "feat3_desc": "Integrated campus of 50,000 sqm with labs, libraries, and sports facilities.",
        "feat4_title": "Global Partnerships",
        "feat4_desc": "Student exchange agreements with 15 universities in 8 countries worldwide.",
        "sec_progs_title": "Our <span class='gold'>Programs</span>",
        "sec_progs_gold": "Programs",
        "sec_progs_desc": "Diverse educational paths for all ambitions",
        "prog1_badge": "Bachelor's",
        "prog1_name": "Computer Science",
        "prog1_desc": "AI, Cybersecurity, and Software Engineering",
        "prog2_badge": "Diploma",
        "prog2_name": "Business Administration",
        "prog2_desc": "Leadership, Marketing, and Entrepreneurship",
        "prog3_badge": "Master's",
        "prog3_name": "Engineering",
        "prog3_desc": "Civil, Electrical, and Mechanical Engineering",
        "prog4_badge": "Bachelor's",
        "prog4_name": "Medicine & Surgery",
        "prog4_desc": "Integrated medical program with clinical training",
        "all_programs": "View All Programs",
        "director_title": "Message from <span class='gold'>the Director</span>",
        "director_gold": "the Director",
        "director_quote": "\"At Al-Riyadh Academy, we believe education is not just transferring knowledge, but building individuals and society. We always strive to provide distinguished education blending authentic values with the latest global curricula.\"",
        "director_name": "— Dr. Abdulaziz Al-Saleem, Academy Director",
        "cta_title": "Start Your Journey With Us Today",
        "cta_desc": "Register now and step toward a bright future",
        "cta_btn": "Register Now",
        "footer_desc": "A leading educational institution in Saudi Arabia since 1995.",
        "footer_links": "Links",
        "footer_progs": "Programs",
        "footer_contact": "Contact",
        "footer_contact_h4": "Contact",
        "footer_about": "About Us",
        "footer_services": "Student Services",
        "footer_library": "Digital Library",
        "footer_prog1": "Computer Science",
        "footer_prog2": "Engineering",
        "footer_prog3": "Medicine",
        "footer_prog4": "Business Admin",
        "footer_address": "Riyadh — King Abdullah Road",
        "footer_phone": "920011223",
        "footer_email": "info@riyadh-academy.edu.sa",
        "footer_hours": "7:00 AM — 9:00 PM",
        "footer_copy": "Al-Riyadh Academy — All Rights Reserved.",
        "programs_btn": "Our Programs",
        "learn_more": "Discover More",
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
        "about_stat1_lbl": "Graduates",
        "about_stat2_lbl": "Sq. Meters",
        "about_stat3_lbl": "Partner Universities",
        "about_stat1_num": "5,000+",
        "about_stat2_num": "50,000+",
        "about_stat3_num": "15+",
        "page_title_contact": "Contact Us",
        "contact_heading": "Get in Touch",
        "contact_legend": "We are here to help you",
        "form_name": "Name",
        "form_email": "Email",
        "form_phone": "Phone",
        "form_program_opt": "Select a program",
        "form_prog1": "Computer Science",
        "form_prog2": "Business Admin",
        "form_prog3": "Engineering",
        "form_prog4": "Medicine",
        "form_message": "Message",
        "form_submit": "Submit",
        "form_success": "Submitted successfully! We will contact you soon.",
        "page_title_programs": "Our Programs",
        "programs_heading": "Our Academic Programs",
        "programs_intro": "Diverse educational paths for all ambitions",
        "breadcrumb_home": "Home",
        "breadcrumb_about": "About Us",
        "breadcrumb_programs": "Programs",
        "breadcrumb_contact": "Contact",
    }
}


def clean_text(t):
    """Normalize whitespace in text"""
    return re.sub(r'\s+', ' ', t).strip()


def reset_from_git():
    """Reset site files from original git commit"""
    import subprocess
    subprocess.run(
        ["git", "checkout", "35124f9", "--", "01-alriyadh-academy/"],
        cwd=BASE, capture_output=True
    )
    print("[OK] Reset from git commit 35124f9")


def process_file(html_path):
    """Tag all elements with data-i18n using text matching"""
    print(f"\n--- {html_path.name} ---")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Remove existing __i18n scripts
    html = re.sub(r'<script>window\.__i18n=.*?</script>\s*', '', html, flags=re.DOTALL)
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Build lookup: normalized Arabic text -> key
    # Include ALL forms (with/without HTML tags)
    ar_lookup = {}  # clean_text -> key
    for key, val in I18N["ar"].items():
        if not val:
            continue
        # Version without HTML tags
        nohtml = clean_text(re.sub(r'<[^>]+>', '', val))
        if nohtml and len(nohtml) >= 2:
            ar_lookup[nohtml] = key
        # Also keep HTML version as separate entry if different
        html_clean = clean_text(val)
        if html_clean != nohtml and html_clean and len(html_clean) >= 2:
            ar_lookup[html_clean] = key
    
    tagged = 0
    
    def try_tag(el, text=None):
        nonlocal tagged
        if el.has_attr('data-i18n') and el['data-i18n']:
            return True  # already tagged
        if text is None:
            text = clean_text(el.get_text())
        if not text or len(text) < 2:
            return False
        
        # Direct match
        if text in ar_lookup:
            el['data-i18n'] = ar_lookup[text]
            tagged += 1
            return True
        return False
    
    # Strategy 1: Tag specific elements first by traversing the DOM tree
    # and matching text
    
    # Tag <title>
    for el in soup.find_all('title'):
        t = clean_text(el.get_text())
        if 'أكاديمية' in t:
            el['data-i18n'] = 'site_name'
            tagged += 1
    
    # Tag nav links - by href attribute
    nav = soup.find('div', id='navLinks')
    if nav:
        for a in nav.find_all('a'):
            href = a.get('href', '')
            if 'index' in href:
                a['data-i18n'] = 'nav_home'; tagged += 1
            elif 'about' in href:
                a['data-i18n'] = 'nav_about'; tagged += 1
            elif 'programs' in href or 'courses' in href:
                a['data-i18n'] = 'nav_programs'; tagged += 1
            elif 'contact' in href:
                a['data-i18n'] = 'nav_contact'; tagged += 1
    
    # Tag footer section
    footer = soup.find('footer')
    if footer:
        # Find the h4 headings in footer
        for h4 in footer.find_all('h4'):
            t = clean_text(h4.get_text())
            if t == 'روابط':
                h4['data-i18n'] = 'footer_links'; tagged += 1
            elif t == 'برامج':
                h4['data-i18n'] = 'footer_progs'; tagged += 1
            elif t == 'تواصل':
                h4['data-i18n'] = 'footer_contact_h4'; tagged += 1
        
        # Tag footer links by href
        for a in footer.find_all('a'):
            href = a.get('href', '')
            t = clean_text(a.get_text())
            if 'about' in href:
                a['data-i18n'] = 'footer_about'; tagged += 1
            elif 'contact' in href and 'services' not in t:
                a['data-i18n'] = 'footer_services'; tagged += 1
            elif 'library' in t or 'الرقمية' in t:
                a['data-i18n'] = 'footer_library'; tagged += 1
            elif '#' in href and not any(x in t for x in ['تويتر','انستغرام','لينكد','سناب','يوتيوب']):
                continue  # skip social links for now
        
        # Tag footer contact info by text
        for p in footer.find_all('p'):
            t = clean_text(p.get_text())
            if 'المملكة' in t and '1995' in t:
                p['data-i18n'] = 'footer_desc'; tagged += 1
                break
        # The footer-bottom p
        fb = footer.find('div', class_='footer-bottom')
        if fb:
            for p in fb.find_all('p'):
                p['data-i18n'] = 'footer_copy'; tagged += 1
    
    # Strategy 3: Tag ALL remaining elements by scanning text content
    for tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'a', 'button', 'li', 'label', 'cite', 'strong', 'em', 'div', 'small', 'blockquote']:
        for el in soup.find_all(tag_name):
            if el.has_attr('data-i18n') and el['data-i18n']:
                continue
            # Skip if has block-level children
            has_block = any(c.name in ['div','section','nav','header','footer','main','aside','article','form','table','ul','ol','blockquote'] for c in el.find_all(recursive=False))
            if has_block:
                continue
            
            text = clean_text(el.get_text())
            if not text or len(text) < 3:
                continue
            
            # Check direct text content (ignoring child elements)
            direct_text = ''.join(s for s in el.strings).strip()
            direct_text = clean_text(direct_text)
            
            # Try to match
            if try_tag(el, text):
                continue
            if direct_text and direct_text != text and try_tag(el, direct_text):
                continue
            
            # Substring matching: check if any key is a substring of text or vice versa
            matched = False
            # Sort by length descending for best match
            for lookup_text, key in sorted(ar_lookup.items(), key=lambda x: -len(x[0])):
                if len(lookup_text) < 5:
                    continue
                if lookup_text in text or text in lookup_text:
                    # Check if they share a significant portion
                    short, long = (lookup_text, text) if len(lookup_text) < len(text) else (text, lookup_text)
                    if short in long and len(short) >= max(5, len(long) * 0.4):
                        el['data-i18n'] = key
                        tagged += 1
                        matched = True
                        break
            if matched:
                continue
    
    # Report
    used = set()
    for el in soup.find_all(attrs={'data-i18n': True}):
        used.add(el['data-i18n'])
    unused = set(I18N["ar"].keys()) - used
    print(f"  Tagged: {tagged} | Used keys: {len(used)}/{len(I18N['ar'])}")
    if unused:
        print(f"  Unused: {sorted(unused)[:15]}")
    
    # Inject i18n DATA RIGHT BEFORE script.js
    i18n_json = json.dumps(I18N, ensure_ascii=False)
    script_tag = soup.new_tag('script')
    script_tag.string = f'window.__i18n={i18n_json};'
    
    # Find the script.js reference and add before it
    scripts = soup.find_all('script', src=re.compile(r'script\.js'))
    if scripts:
        scripts[0].insert_before(script_tag)
    else:
        soup.body.append(script_tag)
    
    # Write back
    html_out = str(soup)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_out)
    print(f"  [OK] Written")


def write_script_js():
    """Write clean script.js with simple working toggle"""
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
    if (btn) btn.textContent = lang === 'ar' ? 'EN' : 'عربي';
    var title = document.querySelector('title');
    if (title) { var n = dict.site_name || ''; title.textContent = n; }
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
      b.id = 'backToTop';
      b.innerHTML = '<i class="fas fa-arrow-up"></i>';
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
      f.addEventListener('submit', function(e) {
        e.preventDefault();
        var btn = f.querySelector('button[type="submit"]');
        if (btn) btn.disabled = true;
        var dict = window.__i18n && window.__i18n[current];
        var m = document.createElement('div');
        m.style.cssText = 'padding:14px 18px;margin-top:16px;border-radius:10px;background:rgba(74,222,128,.15);color:#4ade80;text-align:center;font-weight:600;';
        m.textContent = (dict && dict.form_success) || (current === 'ar' ? '✓ تم الإرسال بنجاح!' : '✓ Submitted!');
        f.appendChild(m);
        setTimeout(function() { f.reset(); if (btn) btn.disabled = false; }, 2000);
        setTimeout(function() { m.remove(); }, 4500);
      });
    });
  });
})();
'''
    (SITE_DIR / 'script.js').write_text(script, encoding='utf-8')
    print("[OK] script.js written")


def verify():
    """Check how many data-i18n were added per page"""
    print(f"\n{'='*60}")
    print("VERIFICATION")
    print(f"{'='*60}")
    for f in sorted(SITE_DIR.glob("*.html")):
        soup = BeautifulSoup(open(f, encoding='utf-8'), 'html.parser')
        count = len(soup.find_all(attrs={'data-i18n': True}))
        print(f"  {f.name}: {count} elements tagged")


if __name__ == '__main__':
    reset_from_git()
    for h in sorted(SITE_DIR.glob("*.html")):
        process_file(h)
    write_script_js()
    verify()
