#!/usr/bin/env python3
"""
Final comprehensive fix for 01-alriyadh-academy.
Step 1: Tag HTML elements with data-i18n keys
Step 2: Inject __i18n with full AR/EN translations
Step 3: Write clean script.js
"""
import json, re, hashlib
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

BASE = Path(r"C:\Users\paule\OneDrive\Desktop\Arabix Theme\education")
SITE = "01-alriyadh-academy"
DIR = BASE / SITE

# Reset
import subprocess
subprocess.run(["git", "checkout", "35124f9", "--", f"{SITE}/"], cwd=BASE, capture_output=True)
print("[OK] Reset to original")

EN_TRANSLATIONS = {
    # Nav / Header
    "الرئيسية": "Home",
    "عن الأكاديمية": "About Us",
    "البرامج": "Programs",
    "اتصل بنا": "Contact",
    "اتصل": "Contact",
    "EN": "EN",
    "أ RIYADH أكاديمية الرياض": "أ RIYADH Al-Riyadh Academy",
    "أكاديمية الرياض": "Al-Riyadh Academy",
    "الرياض": "Riyadh",
    "شريكك في": "Your Partner in",
    "التميز التعليمي": "Educational Excellence",
    
    # Hero
    "منذ ١٩٩٥ — Since 1995": "Since 1995",
    "نحو جيل واعٍ ومبدع — أكثر من ١٠ آلاف خريج وأكثر من ٢٠ برنامجاً تعليمياً معتمداً.": "Towards a conscious, creative generation — over 10,000 graduates and 20+ accredited programs.",
    "عاماً من التميز": "Years of Excellence",
    "خريج": "Graduates",
    "برنامج": "Programs",
    "برامجنا": "Our Programs",
    "اكتشف المزيد": "Discover More",
    
    # Why section
    "لماذا ؟": "Why ?",
    "أكثر من ربع قرن من العطاء التعليمي يجمع بين الأصالة والابتكار": "Over a quarter century of educational excellence blending tradition with innovation",
    
    # Features
    "تعليم معتمد": "Accredited Education",
    "جميع برامجنا معتمدة من وزارة التعليم السعودية ومنظمة الاعتماد الأكاديمي الدولية.": "All programs accredited by the Saudi Ministry of Education and international bodies.",
    "كفاءات متميزة": "Distinguished Staff",
    "أكثر من ٢٠٠ عضو هيئة تدريس من حملة الدكتوراه والماجستير من أفضل الجامعات العالمية.": "Over 200 faculty members with PhDs and Masters from top global universities.",
    "بيئة محفزة": "Inspiring Environment",
    "حرم جامعي متكامل بمساحة ٥٠ ألف متر مربع يشمل مختبرات ومكتبات ومرافق رياضية.": "Integrated 50,000 sqm campus with labs, libraries, and sports facilities.",
    "شراكات عالمية": "Global Partnerships",
    "اتفاقيات تبادل طلابي مع ١٥ جامعة في ٨ دول حول العالم.": "Student exchange with 15 universities in 8 countries.",
    
    # Programs section  
    "برامجنا الأكاديمية": "Our Academic Programs",
    "مسارات تعليمية متنوعة تناسب جميع الطموحات": "Diverse educational paths for all ambitions",
    "بكالوريوس": "Bachelor's",
    "علوم الحاسب": "Computer Science",
    "الذكاء الاصطناعي، الأمن السيبراني، وهندسة البرمجيات": "AI, Cybersecurity, and Software Engineering",
    "دبلوم": "Diploma",
    "إدارة الأعمال": "Business Admin",
    "قيادة، تسويق، وريادة أعمال": "Leadership, Marketing, Entrepreneurship",
    "ماجستير": "Master's",
    "الهندسة": "Engineering",
    "هندسة مدنية، كهربائية، وميكانيكية": "Civil, Electrical, Mechanical Engineering",
    "الطب والجراحة": "Medicine & Surgery",
    "برنامج طبي متكامل مع تدريب سريري": "Integrated medical program with clinical training",
    "الأكاديمية": "the Academy",
    "استعرض جميع البرامج": "View All Programs",
    
    # Director / CTA
    "كلمة": "Message from",
    "المدير": "the Director",
    "\"نؤمن في أكاديمية الرياض أن التعليم ليس مجرد نقل للمعرفة، بل بناء للإنسان والمجتمع. نسعى دائماً لتقديم تعليم متميز يجمع بين القيم الأصيلة وأحدث المناهج العالمية.\"": "\"At Al-Riyadh Academy, we believe education is not just transferring knowledge, but building individuals and society. We blend authentic values with the latest global curricula.\"",
    "— د. عبدالعزيز السليم، مدير الأكاديمية": "— Dr. Abdulaziz Al-Saleem, Academy Director",
    "ابدأ رحلتك معنا اليوم": "Start Your Journey Today",
    "سجل الآن وانطلق نحو مستقبل مشرق": "Register now for a bright future",
    "تسجيل الآن": "Register Now",
    
    # Footer
    "مؤسسة تعليمية رائدة في المملكة العربية السعودية منذ 1995.": "A leading educational institution in Saudi Arabia since 1995.",
    "روابط": "Links",
    "الخدمات الطلابية": "Student Services",
    "المكتبة الرقمية": "Digital Library",
    "الطب": "Medicine",
    "تواصل": "Contact",
    "الرياض — طريق الملك عبدالله": "Riyadh — King Abdullah Road",
    "920011223": "920011223",
    "info@riyadh-academy.edu.sa": "info@riyadh-academy.edu.sa",
    "٧:٠٠ ص — ٩:٠٠ م": "7:00 AM — 9:00 PM",
    "© 2026 أكاديمية الرياض — جميع الحقوق محفوظة.": "© 2026 Al-Riyadh Academy — All Rights Reserved.",
    
    # About page specific
    "عن أكاديمية": "About Al-Riyadh",
    "شريكك الموثوق في التعليم منذ 1995": "Your trusted education partner since 1995",
    "حكاية": "The Story",
    "التميز": "Excellence",
    "تأسست أكاديمية الرياض عام 1995 بهدف تقديم تعليم متميز يواكب المعايير العالمية مع الحفاظ على القيم الإسلامية والعربية الأصيلة. على مدار أكثر من 25 عاماً، تخرج من الأكاديمية أكثر من 10 آلاف طالب وطالبة أصبحوا قادة في مجالاتهم.": "Founded in 1995, Al-Riyadh Academy aims to provide distinguished education meeting global standards while preserving authentic Islamic and Arab values. Over 25+ years, more than 10,000 graduates have become leaders in their fields.",
    "نؤمن بأن لكل طالب قدرات فريدة تستحق الرعاية والتنمية. لذلك نقدم بيئة تعليمية محفزة تشجع على الإبداع والابتكار مع توفير أحدث التقنيات التعليمية.": "We believe every student has unique abilities. We provide a stimulating environment encouraging creativity and innovation with cutting-edge technology.",
    "حصلت الأكاديمية على العديد من الجوائز المحلية والدولية، منها جائزة التميز التعليمي لعام 2023 من منظمة اليونسكو، وجائزة أفضل مؤسسة تعليمية في الشرق الأوسط 2024.": "The academy has won numerous local and international awards, including UNESCO's 2023 Educational Excellence Award and Best Educational Institution in the Middle East 2024.",
    "قيمنا": "Our Values",
    "الجوهرية": "Core",
    "الجامعي": "Campus",
    "الأصالة": "Authenticity",
    "الابتكار": "Innovation",
    "اعتماد أحدث أساليب التعليم والتقنية": "Adopting the latest educational methods and technology",
    "أعلى معايير الجودة الأكاديمية": "Highest academic quality standards",
    "المجتمع": "Community",
    "المساهمة الفاعلة في تنمية المجتمع": "Active contribution to community development",
    "الحرم": "Our",
    "بيئة تعليمية متكاملة على أحدث طراز": "A fully integrated, state-of-the-art learning environment",
    "المبادئ التي توجه مسيرتنا التعليمية": "Principles guiding our educational journey",
    "التمسك بالقيم الإسلامية والعربية": "Commitment to Islamic and Arab values",
    
    # Contact page specific
    "بنا": "Us",
    "نحن هنا لمساعدتك — تواصل معنا بأي وقت": "We are here to help — contact us anytime",
    "القبول": "Admissions",
    "مباشر": "Direct",
    "قدم الآن للفصل القادم — الأماكن محدودة": "Apply now for next semester — spaces limited",
    "تقديم طلب قبول": "Submit Application",
    "تحميل الدليل التعريفي": "Download Prospectus",
    "الاسم الكامل *": "Full Name *",
    "رقم الجوال *": "Phone Number *",
    "نوع الاستفسار": "Inquiry Type",
    "الرسالة *": "Message *",
    "إرسال": "Submit",
    "مواعيد العمل": "Working Hours",
    "المكان بالتفصيل هنا الموقع": "Detailed address here — Location",
    "السبت — الخميس: ٧:٠٠ ص — ٩:٠٠ م الجمعة: مغلق": "Sat — Thu: 7:00 AM — 9:00 PM Fri: Closed",
    "الهاتف": "Phone",
    "البريد الإلكتروني": "Email",
    "المكان بالتفصيل هنا": "Detailed location here",
    "الاستفسارات الأكاديمية": "Academic Inquiries",
    "القبول والتسجيل": "Admissions & Registration",
    "المنح الدراسية": "Scholarships",
    "الشؤون المالية": "Financial Affairs",
    "أخرى": "Other",
    
    # Programs page specific
    "برنامج شامل في الذكاء الاصطناعي، علم البيانات، الأمن السيبراني، وهندسة البرمجيات. مختبرات حديثة ومشاريع تخرج مع شركات تقنية كبرى.": "Comprehensive program in AI, Data Science, Cybersecurity, and Software Engineering. Modern labs with industry partners.",
    "تخصصات في التسويق الرقمي، ريادة الأعمال، الإدارة المالية، والقيادة. شراكات مع كبرى الشركات السعودية للتدريب.": "Specializations in Digital Marketing, Entrepreneurship, Financial Management. Partnerships with top Saudi companies.",
    "هندسة مدنية، كهربائية، ميكانيكية، وكيميائية — مناهج معتمدة دولياً ومختبرات مجهزة بأحدث المعدات.": "Civil, Electrical, Mechanical, Chemical Engineering — internationally accredited curricula with state-of-the-art labs.",
    "برنامج طبي متكامل من ٦ سنوات مع سنة امتياز في أرقى المستشفيات الجامعية. تدريب سريري منذ السنة الثالثة.": "Integrated 6-year medical program with internship year in top university hospitals. Clinical training from year 3.",
    "برنامج صيدلة سريرية يجمع بين العلوم الصيدلانية والممارسة السريرية في المستشفيات والصيدليات المجتمعية.": "Clinical pharmacy program combining pharmaceutical sciences with hospital and community practice.",
    "برنامج مكثف لتعليم اللغة العربية للناطقين بغيرها، يشمل القراءة والكتابة والمحادثة، مع أنشطة ثقافية.": "Intensive Arabic program for non-native speakers including reading, writing, and speaking with cultural activities.",
    "دبلوم متخصص في أمن المعلومات، اختبار الاختراق، وتحليل الثغرات — بالتعاون مع الهيئة الوطنية للأمن السيبراني.": "Specialized diploma in Information Security, Penetration Testing, and Vulnerability Analysis — in partnership with the National Cybersecurity Authority.",
    "برنامج ماجستير تنفيذي لإعداد القادة — محاضرات مسائية وعبر الإنترنت، بالتعاون مع جامعات بريطانية وأمريكية.": "Executive Master's program for leaders — evening and online lectures in partnership with British and American universities.",
    "اختر مسارك نحو المستقبل — أكثر من ٢٠ برنامجاً معتمداً": "Choose your path to the future — over 20 accredited programs",
    "مميزات": "Why Study",
    "الدراسة معنا": "With Us",
    "اعتماد أكاديمي": "Academic Accreditation",
    "منح دراسية": "Scholarships",
    "توظيف بعد التخرج": "Post-Graduation Employment",
    "برامج تبادل طلابي": "Student Exchange",
    "الأمن السيبراني": "Cybersecurity",
    "الصيدلة الإكلينيكية": "Clinical Pharmacy",
    "اللغة العربية لغير الناطقين بها": "Arabic for Non-Native Speakers",
    "إدارة الأعمال (MBA)": "Business Admin (MBA)",
    "٤ سنوات": "4 Years",
    "١٢٠ طالباً سنوياً": "120 students/year",
    "١٥٠ طالباً سنوياً": "150 students/year",
    "٥ سنوات": "5 Years",
    "٢٠٠ طالباً سنوياً": "200 students/year",
    "٦ سنوات": "6 Years",
    "٨٠ طالباً سنوياً": "80 students/year",
    "٦٠ طالباً سنوياً": "60 students/year",
    "سنة - سنتان": "1-2 Years",
    "مجموعات صغيرة": "Small groups",
    "سنتان": "2 Years",
    "٥٠ طالباً سنوياً": "50 students/year",
    "١.٥ سنة": "1.5 Years",
    "دفعة ٣٠ طالباً": "30 students/cohort",
}


def get_direct_text(el):
    """Get only direct text of an element (ignoring child elements)"""
    texts = []
    for child in el.children:
        if isinstance(child, NavigableString):
            t = child.strip()
            if t:
                texts.append(t)
    return ' '.join(texts)


def process_file(html_path):
    """Add data-i18n to all text-bearing elements, build translations"""
    print(f"\n--- {html_path.name} ---")
    
    html = html_path.read_text(encoding='utf-8')
    html = re.sub(r'<script>window\.__i18n=.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'\s*data-i18n(?:-html)?="[^"]*"', '', html)
    
    soup = BeautifulSoup(html, 'html.parser')
    translations = {}
    tagged = 0
    
    def make_key(text):
        """Create a readable key from Arabic text"""
        # First 4 Arabic chars or first 6 ascii
        ar_chars = re.findall(r'[\u0600-\u06FF]', text[:8])
        if ar_chars:
            return ''.join(ar_chars[:4])
        return re.sub(r'[^a-zA-Z0-9]', '', text[:6]).lower()
    
    # Process ALL elements with direct text content
    for el in soup.find_all(True):
        if el.name in ['html','head','body','meta','link','script','style','svg','path','circle','defs',
                        'linearGradient','stop','title']:
            continue
        if el.has_attr('data-i18n'):
            continue
        
        # Skip block containers
        block_tags = ['div','section','nav','header','footer','main','aside','article','form','table','ul','ol']
        
        # Get direct text
        direct = get_direct_text(el)
        if not direct or len(direct) < 2:
            continue
        
        # For block tags, only tag if they contain ONLY text (no element children)
        if el.name in block_tags:
            has_el_child = any(c.name for c in el.children if hasattr(c, 'name') and c.name)
            if has_el_child:
                continue
        
        # For inline tags, check they don't contain block children
        has_block = any(c.name in block_tags for c in el.find_all(recursive=False))
        if has_block:
            continue
        
        # Now tag this element
        full_text = direct.strip()
        
        # Create key
        key = make_key(full_text)
        # Ensure uniqueness
        if key in translations:
            # Find text-based suffix
            counter = 2
            while f"{key}_{counter}" in translations:
                counter += 1
            key = f"{key}_{counter}"
        
        el['data-i18n'] = key
        translations[key] = full_text
        tagged += 1
        
        # Also auto-fill EN if known
        # (will be merged later)
    
    print(f"  Tagged: {tagged} elements, {len(translations)} unique keys")
    return soup, translations


def inject_i18n(soup, all_translations):
    """Inject __i18n data before script.js"""
    # Build ar/en dicts
    en_dict = {}
    ar_dict = {}
    for key, ar_text in all_translations.items():
        ar_dict[key] = ar_text
        en_dict[key] = EN_TRANSLATIONS.get(ar_text, ar_text)  # fallback to Arabic
    
    i18n_data = {'ar': ar_dict, 'en': en_dict}
    i18n_json = json.dumps(i18n_data, ensure_ascii=False)
    
    script_tag = soup.new_tag('script')
    script_tag.string = f'window.__i18n={i18n_json};'
    
    scripts = soup.find_all('script', src=re.compile(r'script\.js'))
    if scripts:
        scripts[0].insert_before(script_tag)
    else:
        soup.body.append(script_tag)


# Process all HTML files
all_translations = {}

for html_file in sorted(DIR.glob("*.html")):
    soup, trans = process_file(html_file)
    all_translations.update(trans)
    inject_i18n(soup, trans)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"  [OK] Written: {html_file.name}")

# Check missing English translations
missing = [ar for ar in all_translations.values() if ar not in EN_TRANSLATIONS]
if missing:
    print(f"\n{'='*60}")
    print(f"WARNING: {len(missing)} texts missing English translations:")
    for t in sorted(set(missing)):
        print(f"  MISSING: {t[:80]}")
else:
    print(f"\n{'='*60}")
    print("All texts have English translations! ✓")
    
print(f"Total unique keys: {len(all_translations)}")

# Generate script.js
SCRIPT = '''(function() {
  'use strict';
  var LS = 'aracademy_lang';
  var current = localStorage.getItem(LS) || 'ar';
  document.documentElement.lang = current;
  document.documentElement.dir = current === 'ar' ? 'rtl' : 'ltr';

  function apply(lang) {
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
    if (btn) btn.textContent = lang === 'ar' ? 'EN' : '\\u0639\\u0631\\u0628\\u064A';
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
      apply(current);
      toggle.addEventListener('click', function() { apply(current === 'ar' ? 'en' : 'ar'); });
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
    new IntersectionObserver(function(es) {
      es.forEach(function(e) { if (e.isIntersecting) { e.target.classList.add('show'); } });
    }, { threshold: 0.1 }).observe(document.querySelectorAll('.feat-card, .prog-card, .sec-head, .director-msg, .hero-content'));
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
    document.querySelectorAll('form').forEach(function(f) {
      f.addEventListener('submit', function(e) { e.preventDefault();
        var btn = f.querySelector('button[type="submit"]');
        if (btn) btn.disabled = true;
        var dict = window.__i18n && window.__i18n[current];
        var m = document.createElement('div');
        m.style.cssText = 'padding:14px 18px;margin-top:16px;border-radius:10px;background:rgba(74,222,128,.15);color:#4ade80;text-align:center;font-weight:600;';
        m.textContent = (dict && dict.form_success) || (current === 'ar' ? '\\u2713 \\u062A\\u0645 \\u0627\\u0644\\u0625\\u0631\\u0633\\u0627\\u0644!' : '\\u2713 Submitted!');
        f.appendChild(m);
        setTimeout(function() { f.reset(); if (btn) btn.disabled = false; }, 2000);
        setTimeout(function() { m.remove(); }, 4500);
      });
    });
  });
})();
'''

(DIR / 'script.js').write_text(SCRIPT, encoding='utf-8')
print("[OK] script.js written")
print("\n✅ Site 01-alriyadh-academy complete!")
