#!/usr/bin/env python3
"""
Generate full i18n support for all 5 education sites.
- Adds data-i18n attributes to HTML files
- Generates enhanced script.js with translation dicts + polish features
"""

import os, re, json, shutil
from pathlib import Path

BASE = Path(r"C:\Users\paule\OneDrive\Desktop\Arabix Theme\education")

# ===================== TRANSLATIONS =====================

SITES = {}

# ---- Site 01: Al-Riyadh Academy ----
SITES["01-alriyadh-academy"] = {
    "ar": {
        "site_name": "أكاديمية الرياض",
        "site_tagline": "التعليم في أبهى صوره",
        "nav_home": "الرئيسية",
        "nav_about": "عن الأكاديمية",
        "nav_programs": "البرامج",
        "nav_contact": "اتصل بنا",
        "lang_btn": "EN",
        "lang_btn_alt": "عربي",
        "hero_tag": "منارة علم وتربية",
        "hero_title": "أكاديمية <strong>الرياض</strong><br>حيث <span class='gold'>التميز</span> يبدأ",
        "hero_desc": "أكاديمية رائدة في تعليم العلوم والآداب بمناهج عصرية وكوادر تعليمية متميزة. نعد طلابنا لمستقبل مشرق منذ ٢٠١٠.",
        "hero_cta_primary": "تعرف على برامجنا",
        "hero_cta_secondary": "اكتشف الأكاديمية",
        "hero_stat1": "خريج",
        "hero_stat2": "برنامج",
        "hero_stat3": "معلم",
        "sec_why_title": "لماذا <span class='gold'>أكاديمية الرياض</span>؟",
        "sec_why_desc": "٢٥ عاماً من التميز في التعليم — رؤية واضحة، منهج متطور، بيئة محفزة",
        "feat1_title": "مناهج حديثة",
        "feat1_desc": "نعتمد أحدث المناهج العالمية المطورة وفق رؤية المملكة ٢٠٣٠ مع التركيز على المهارات الرقمية.",
        "feat2_title": "كوادر متميزة",
        "feat2_desc": "معلمون مؤهلون من أفضل الجامعات المحلية والعالمية، يمتلكون خبرات تربوية واسعة.",
        "feat3_title": "بيئة تفاعلية",
        "feat3_desc": "مختبرات علمية، مكتبة رقمية، أنشطة لا منهجية — كل ذلك في حرم جامعي متكامل.",
        "feat4_title": "متابعة فردية",
        "feat4_desc": "نظام متابعة شخصية لكل طالب مع تقارير دورية للأهالي وخطط دعم مخصصة.",
        "page_title_about": "عن <span class='gold'>أكاديمية الرياض</span>",
        "about_heading": "مسيرة <span class='gold'>عطاء</span>",
        "about_p1": "تأسست أكاديمية الرياض عام ٢٠١٠ بموجب ترخيص من وزارة التعليم، بهدف تقديم تعليم متميز يجمع بين الأصالة والحداثة. منذ انطلاقتها، خرّجت الأكاديمية أكثر من ٥٠٠٠ طالب وطالبة التحقوا بأعرق الجامعات المحلية والعالمية.",
        "about_p2": "تمتد مساحة الحرم الجامعي على ٥٠ ألف متر مربع، ويضم ٣ مباني تعليمية مجهزة بأحدث التقنيات، ومكتبة مركزية تضم أكثر من ٣٠ ألف عنوان، وملاعب رياضية ومنشآت فنية.",
        "about_p3": "نفخر بشراكاتنا مع ١٥ جامعة دولية وبرامج تبادل طلابي مع مؤسسات تعليمية في أمريكا وبريطانيا وكندا.",
        "about_stat1_label": "خريج",
        "about_stat2_label": "متر مربع",
        "about_stat3_label": "جامعة شريكة",
        "page_title_programs": "برامجنا <span class='gold'>الأكاديمية</span>",
        "programs_intro": "برامج متنوعة تناسب جميع الاهتمامات والمراحل الدراسية",
        "prog1_title": "مسار العلوم",
        "prog1_desc": "فيزياء، كيمياء، أحياء — مع مختبرات متطورة ومشاريع بحثية",
        "prog1_meta": "٣ سنوات",
        "prog2_title": "مسار التقنية",
        "prog2_desc": "برمجة، ذكاء اصطناعي، روبوتكس — إعداد لمستقبل رقمي واعد",
        "prog2_meta": "٤ سنوات",
        "prog3_title": "مسار اللغات",
        "prog3_desc": "إنجليزية، فرنسية، صينية — مع مختبر لغات وبرامج تبادل دولي",
        "prog3_meta": "٣ سنوات",
        "prog4_title": "مسار الفنون",
        "prog4_desc": "فنون بصرية، مسرح، موسيقى — إطلاق العنان للإبداع",
        "prog4_meta": "٣ سنوات",
        "prog5_title": "التحضير الجامعي",
        "prog5_desc": "برنامج مكثف لتأهيل الطلاب للقبول في الجامعات السعودية والعالمية",
        "prog5_meta": "سنة واحدة",
        "prog6_title": "التعليم عن بُعد",
        "prog6_desc": "منصة تعليمية متكاملة — دروس مباشرة ومسجلة تناسب الجميع",
        "prog6_meta": "حسب البرنامج",
        "page_title_contact": "اتصل بنا — القبول والتسجيل",
        "contact_heading": "تواصل مع <span class='gold'>الأكاديمية</span>",
        "form_heading": "طلب التسجيل",
        "form_name": "الاسم الكامل",
        "form_name_ph": "أدخل اسمك",
        "form_email": "البريد الإلكتروني",
        "form_email_ph": "example@email.com",
        "form_phone": "رقم الجوال",
        "form_phone_ph": "05xxxxxxxx",
        "form_program": "البرنامج المطلوب",
        "form_program_ph": "اختر البرنامج",
        "form_message": "رسالتك",
        "form_message_ph": "اكتب رسالتك هنا",
        "form_submit": "إرسال الطلب",
        "form_success": "تم إرسال طلبك بنجاح! سنتواصل معك قريباً.",
        "form_prog1": "مسار العلوم",
        "form_prog2": "مسار التقنية",
        "form_prog3": "مسار اللغات",
        "form_prog4": "مسار الفنون",
        "form_prog5": "التحضير الجامعي",
        "form_prog6": "التعليم عن بُعد",
        "footer_desc": "أكاديمية رياضية رائدة — تعليم يجمع بين الأصالة والحداثة.",
        "footer_links": "روابط",
        "footer_progs": "البرامج",
        "footer_contact": "تواصل",
        "footer_prog1": "مسار العلوم",
        "footer_prog2": "مسار التقنية",
        "footer_prog3": "مسار اللغات",
        "footer_copy": "أكاديمية الرياض — جميع الحقوق محفوظة.",
        "breadcrumb_home": "الرئيسية",
        "breadcrumb_about": "عن الأكاديمية",
        "breadcrumb_programs": "البرامج",
        "breadcrumb_contact": "اتصل بنا",
        "cta_title": "ابدأ رحلة التميز اليوم",
        "cta_desc": "سجل الآن وكن جزءاً من قصتنا",
        "cta_btn": "تسجيل الآن",
        "founder_quote": "التعليم هو أقوى سلاح يمكنك استخدامه لتغيير العالم. في أكاديمية الرياض، نزرع بذور المعرفة ونرعى عقول المستقبل.",
        "founder_name": "— د. عبدالرحمن آل الشيخ، المؤسس",
        "why1_title": "بيئة محفزة",
        "why1_desc": "حرم جامعي متكامل يلهم الإبداع",
        "why2_title": "اعتماد دولي",
        "why2_desc": "شهادات معترف بها عالمياً",
        "why3_title": "نشاطات متنوعة",
        "why3_desc": "رياضة، فنون، تطوع ورحلات",
        "why4_title": "دعم مستمر",
        "why4_desc": "مرشد أكاديمي لكل طالب",
        "back_to_top": "العودة للأعلى",
        "contact_address": "الرياض — حي النرجس",
        "contact_phone": "٩٢٠٠٠١٢٣٤",
        "contact_email": "info@riyadh-academy.edu.sa",
        "contact_hours": "٧:٣٠ صباحاً — ٣:٠٠ مساءً (الأحد — الخميس)",
        "contact_hours_label": "ساعات العمل",
        "address_label": "العنوان",
        "phone_label": "الهاتف",
        "email_label": "البريد الإلكتروني",
    },
    "en": {
        "site_name": "Al-Riyadh Academy",
        "site_tagline": "Education at Its Finest",
        "nav_home": "Home",
        "nav_about": "About Us",
        "nav_programs": "Programs",
        "nav_contact": "Contact",
        "lang_btn": "عربي",
        "lang_btn_alt": "EN",
        "hero_tag": "A Beacon of Knowledge",
        "hero_title": "Al-Riyadh <strong>Academy</strong><br>Where <span class='gold'>Excellence</span> Begins",
        "hero_desc": "A leading academy teaching sciences and arts with modern curricula and distinguished faculty. Preparing our students for a bright future since 2010.",
        "hero_cta_primary": "Explore Programs",
        "hero_cta_secondary": "Discover Academy",
        "hero_stat1": "Graduates",
        "hero_stat2": "Programs",
        "hero_stat3": "Teachers",
        "sec_why_title": "Why <span class='gold'>Al-Riyadh Academy</span>?",
        "sec_why_desc": "25 years of excellence in education — clear vision, advanced curriculum, inspiring environment",
        "feat1_title": "Modern Curriculum",
        "feat1_desc": "We adopt the latest global curricula aligned with Saudi Vision 2030, with focus on digital skills.",
        "feat2_title": "Distinguished Staff",
        "feat2_desc": "Qualified teachers from top local and international universities with extensive educational expertise.",
        "feat3_title": "Interactive Environment",
        "feat3_desc": "Science labs, digital library, extracurricular activities — all in an integrated campus.",
        "feat4_title": "Individual Mentoring",
        "feat4_desc": "Personal tracking system for each student with periodic reports and customized support plans.",
        "page_title_about": "About <span class='gold'>Al-Riyadh Academy</span>",
        "about_heading": "A Journey <span class='gold'>of Excellence</span>",
        "about_p1": "Founded in 2010 under the Ministry of Education license, Al-Riyadh Academy aims to provide distinguished education blending tradition with modernity. Since its inception, the academy has graduated over 5,000 students who joined prestigious universities locally and abroad.",
        "about_p2": "The campus spans 50,000 square meters, featuring 3 educational buildings equipped with latest technology, a central library with over 30,000 titles, sports facilities and arts centers.",
        "about_p3": "We pride ourselves on partnerships with 15 international universities and student exchange programs with institutions in the US, UK, and Canada.",
        "about_stat1_label": "Graduates",
        "about_stat2_label": "Square Meters",
        "about_stat3_label": "Partner Universities",
        "page_title_programs": "Our <span class='gold'>Programs</span>",
        "programs_intro": "Diverse programs for all interests and academic levels",
        "prog1_title": "Science Track",
        "prog1_desc": "Physics, Chemistry, Biology — with advanced labs and research projects",
        "prog1_meta": "3 Years",
        "prog2_title": "Technology Track",
        "prog2_desc": "Programming, AI, Robotics — preparing for a promising digital future",
        "prog2_meta": "4 Years",
        "prog3_title": "Languages Track",
        "prog3_desc": "English, French, Chinese — with language lab and international exchange programs",
        "prog3_meta": "3 Years",
        "prog4_title": "Arts Track",
        "prog4_desc": "Visual arts, theater, music — unleashing creativity",
        "prog4_meta": "3 Years",
        "prog5_title": "University Prep",
        "prog5_desc": "Intensive program preparing students for admission to Saudi and international universities",
        "prog5_meta": "1 Year",
        "prog6_title": "Distance Learning",
        "prog6_desc": "Integrated online platform — live and recorded classes for everyone",
        "prog6_meta": "Varies",
        "page_title_contact": "Contact — Admissions & Registration",
        "contact_heading": "Get in <span class='gold'>Touch</span>",
        "form_heading": "Registration Form",
        "form_name": "Full Name",
        "form_name_ph": "Enter your name",
        "form_email": "Email",
        "form_email_ph": "example@email.com",
        "form_phone": "Phone Number",
        "form_phone_ph": "05xxxxxxxx",
        "form_program": "Desired Program",
        "form_program_ph": "Select a program",
        "form_message": "Your Message",
        "form_message_ph": "Type your message here",
        "form_submit": "Submit Application",
        "form_success": "Your application has been submitted! We will contact you soon.",
        "form_prog1": "Science Track",
        "form_prog2": "Technology Track",
        "form_prog3": "Languages Track",
        "form_prog4": "Arts Track",
        "form_prog5": "University Prep",
        "form_prog6": "Distance Learning",
        "footer_desc": "A leading Riyadh academy — education blending tradition with modernity.",
        "footer_links": "Links",
        "footer_progs": "Programs",
        "footer_contact": "Contact",
        "footer_prog1": "Science Track",
        "footer_prog2": "Technology Track",
        "footer_prog3": "Languages Track",
        "footer_copy": "Al-Riyadh Academy — All Rights Reserved.",
        "breadcrumb_home": "Home",
        "breadcrumb_about": "About Us",
        "breadcrumb_programs": "Programs",
        "breadcrumb_contact": "Contact",
        "cta_title": "Start Your Excellence Journey",
        "cta_desc": "Register now and be part of our story",
        "cta_btn": "Register Now",
        "founder_quote": "Education is the most powerful weapon to change the world. At Al-Riyadh Academy, we plant the seeds of knowledge and nurture the minds of tomorrow.",
        "founder_name": "— Dr. Abdulrahman Al-Sheikh, Founder",
        "why1_title": "Inspiring Environment",
        "why1_desc": "Integrated campus inspiring creativity",
        "why2_title": "Accreditation",
        "why2_desc": "Globally recognized certificates",
        "why3_title": "Activities",
        "why3_desc": "Sports, arts, volunteering, trips",
        "why4_title": "Ongoing Support",
        "why4_desc": "Academic advisor for every student",
        "back_to_top": "Back to Top",
        "contact_address": "Riyadh — Al Narjis District",
        "contact_phone": "920001234",
        "contact_email": "info@riyadh-academy.edu.sa",
        "contact_hours": "7:30 AM — 3:00 PM (Sun — Thu)",
        "contact_hours_label": "Hours",
        "address_label": "Address",
        "phone_label": "Phone",
        "email_label": "Email",
    }
}

SITES["02-qudra-institute"] = {
    "ar": {
        "site_name": "معهد قدرة",
        "site_tagline": "قدراتك .. مستقبلك",
        "nav_home": "الرئيسية",
        "nav_about": "عن المعهد",
        "nav_courses": "الدورات",
        "nav_contact": "اتصل بنا",
        "lang_btn": "EN",
        "lang_btn_alt": "عربي",
        "hero_tag": "تدريب احترافي — نتائج ملموسة",
        "hero_title": "طوّر <strong>قدراتك</strong><br>وابنِ <span class='blue-accent'>مستقبلك</span>",
        "hero_desc": "معهد قدرة — وجهتك للتدريب الاحترافي في التقنية والإدارة. أكثر من ١٠٠ دورة تدريبية معتمدة، مدربون خبراء، وشهادات معترف بها في سوق العمل.",
        "hero_cta_primary": "تصفح الدورات",
        "hero_cta_secondary": "عن المعهد",
        "hero_stat1": "دورة تدريبية",
        "hero_stat2": "متدرب",
        "hero_stat3": "شهادة معتمدة",
        "sec_why_title": "وش <span class='blue-accent'>يميزنا</span>؟",
        "sec_why_desc": "أكثر من ١٠ سنوات في التدريب الاحترافي",
        "feat1_title": "مدربون خبراء",
        "feat1_desc": "ممارسون في المجال — ليسوا مجرد أكاديميين — يشاركونكم تجاربهم الواقعية.",
        "feat2_title": "شهادات احترافية",
        "feat2_desc": "شهادات معتمدة من الجهات الرسمية — أضفها لسيرتك الذاتية وارفع فرصك الوظيفية.",
        "feat3_title": "تدريب عملي",
        "feat3_desc": "مشاريع تطبيقية، ورش عمل، محاكاة واقعية — تتعلم بالممارسة لا بالتنظير.",
        "feat4_title": "مواعيد مرنة",
        "feat4_desc": "مسائي وصباحي — حضور فعلي أو عن بُعد — اختر ما يناسب جدولك.",
        "hero_accent1": "دورة",
        "hero_accent2": "متدرب",
        "hero_accent3": "شهادة",
        "page_title_about": "عن <span class='blue-accent'>معهد قدرة</span>",
        "about_heading": "قصتنا <span class='blue-accent'>في التدريب</span>",
        "about_p1": "انطلق معهد قدرة عام ٢٠١٤ كمنصة تدريب احترافي تهدف إلى سد الفجوة بين المهارات الأكاديمية ومتطلبات سوق العمل. اليوم، نحن واحد من أبرز معاهد التدريب في المملكة.",
        "about_p2": "نقدم أكثر من ١٠٠ دورة تدريبية في مجالات التقنية والإدارة واللغات، مع شراكات استراتيجية مع كبرى شركات التقنية مثل Microsoft وAWS وGoogle.",
        "about_p3": "معدل توظيف خريجينا يتجاوز ٨٥٪ خلال ٣ أشهر من إكمال البرنامج — وهذا هو مقياس نجاحنا الحقيقي.",
        "about_stat1_label": "متخرج",
        "about_stat2_label": "نسبة توظيف",
        "about_stat3_label": "شريك استراتيجي",
        "page_title_courses": "دوراتنا <span class='blue-accent'>التدريبية</span>",
        "courses_intro": "اختر مسارك المهني — أكثر من ١٠٠ دورة في مختلف المجالات",
        "course1_title": "إدارة المشاريع الاحترافية PMP",
        "course1_desc": "تحضير كامل لشهادة PMP مع مشروع تطبيقي — ٤ أسابيع مكثفة.",
        "course1_meta": "٤ أسابيع · حضوري + عن بُعد",
        "course2_title": "تحليل البيانات باستخدام Python",
        "course2_desc": "من الصفر إلى الاحتراف — Pandas, NumPy, Matplotlib, SQL.",
        "course2_meta": "٦ أسابيع · عن بُعد",
        "course3_title": "الأمن السيبراني للمبتدئين",
        "course3_desc": "أساسيات أمن المعلومات، اختبار الاختراق، شبكات — عملي بالكامل.",
        "course3_meta": "٨ أسابيع · حضوري",
        "course4_title": "الذكاء الاصطناعي التطبيقي",
        "course4_desc": "تعلم الآلة، الشبكات العصبية، ChatGPT API — مشاريع حقيقية.",
        "course4_meta": "١٠ أسابيع · عن بُعد",
        "course5_title": "القيادة والإدارة التنفيذية",
        "course5_desc": "مهارات القيادة، إدارة الفرق، اتخاذ القرارات — للمدراء والتنفيذيين.",
        "course5_meta": "٣ أسابيع · حضوري",
        "course6_title": "تطوير الويب Full-Stack",
        "course6_desc": "React, Node.js, MongoDB — اصنع تطبيقات ويب كاملة من البداية.",
        "course6_meta": "١٢ أسبوع · عن بُعد",
        "page_title_contact": "اتصل بنا — التسجيل في الدورات",
        "contact_heading": "تواصل مع <span class='blue-accent'>فريقنا</span>",
        "form_heading": "طلب التسجيل",
        "form_name": "الاسم الكامل",
        "form_name_ph": "أدخل اسمك",
        "form_email": "البريد الإلكتروني",
        "form_email_ph": "example@email.com",
        "form_phone": "رقم الجوال",
        "form_phone_ph": "05xxxxxxxx",
        "form_course": "الدورة المطلوبة",
        "form_course_ph": "اختر الدورة",
        "form_message": "استفسارك",
        "form_message_ph": "اكتب استفسارك هنا",
        "form_submit": "إرسال الطلب",
        "form_success": "تم إرسال طلبك! فريقنا سيتواصل معك خلال ٢٤ ساعة.",
        "form_course1": "إدارة المشاريع PMP",
        "form_course2": "تحليل البيانات Python",
        "form_course3": "الأمن السيبراني",
        "form_course4": "الذكاء الاصطناعي",
        "form_course5": "القيادة التنفيذية",
        "form_course6": "Full-Stack Web",
        "footer_desc": "وجهتك للتدريب الاحترافي — طور قدراتك وابنِ مستقبلك.",
        "footer_links": "روابط",
        "footer_progs": "الدورات",
        "footer_contact": "تواصل",
        "footer_course1": "إدارة المشاريع",
        "footer_course2": "تحليل البيانات",
        "footer_course3": "الأمن السيبراني",
        "footer_copy": "معهد قدرة — جميع الحقوق محفوظة.",
        "breadcrumb_home": "الرئيسية",
        "breadcrumb_about": "عن المعهد",
        "breadcrumb_courses": "الدورات",
        "breadcrumb_contact": "اتصل بنا",
        "cta_title": "مكانك يبدأ هنا",
        "cta_desc": "سجل في أي دورة وابدأ رحلتك المهنية",
        "cta_btn": "سجل الآن",
        "founder_quote": "نحن لا نقدم شهادات فقط — نصنع محترفين قادرين على المنافسة في سوق العمل.",
        "founder_name": "— أ. فهد العتيبي، المؤسس",
        "why1_title": "خبرة ١٠+ سنوات",
        "why1_desc": "في التدريب الاحترافي",
        "why2_title": "شهادات معتمدة",
        "why2_desc": "من جهات رسمية",
        "why3_title": "تدريب عملي",
        "why3_desc": "مشاريع وورش عمل",
        "why4_title": "دعم توظيف",
        "why4_desc": "شراكات مع ١٠٠+ شركة",
        "back_to_top": "العودة للأعلى",
        "contact_address": "جدة — حي الروضة",
        "contact_phone": "٩٢٠٠٢٢٣٤٥",
        "contact_email": "info@qudra.edu.sa",
        "contact_hours": "٩:٠٠ ص — ٩:٠٠ م (السبت — الخميس)",
        "contact_hours_label": "ساعات العمل",
        "address_label": "العنوان",
        "phone_label": "الهاتف",
        "email_label": "البريد الإلكتروني",
        "course_badge": "الأكثر طلباً",
    },
    "en": {
        "site_name": "Qudra Institute",
        "site_tagline": "Your Skills .. Your Future",
        "nav_home": "Home",
        "nav_about": "About",
        "nav_courses": "Courses",
        "nav_contact": "Contact",
        "lang_btn": "عربي",
        "lang_btn_alt": "EN",
        "hero_tag": "Professional Training — Real Results",
        "hero_title": "Develop <strong>Your Skills</strong><br>Build <span class='blue-accent'>Your Future</span>",
        "hero_desc": "Qudra Institute — your destination for professional training in tech and management. Over 100 accredited courses, expert trainers, and certificates recognized in the job market.",
        "hero_cta_primary": "Browse Courses",
        "hero_cta_secondary": "About Institute",
        "hero_stat1": "Courses",
        "hero_stat2": "Trainees",
        "hero_stat3": "Certifications",
        "sec_why_title": "Why <span class='blue-accent'>Qudra</span>?",
        "sec_why_desc": "Over 10 years in professional training",
        "feat1_title": "Expert Trainers",
        "feat1_desc": "Industry practitioners — not just academics — sharing real-world experience.",
        "feat2_title": "Professional Certificates",
        "feat2_desc": "Official accredited certificates — add them to your resume and boost your career.",
        "feat3_title": "Hands-on Training",
        "feat3_desc": "Applied projects, workshops, real simulations — learn by doing, not just theory.",
        "feat4_title": "Flexible Schedules",
        "feat4_desc": "Morning and evening — in-person or remote — choose what fits your schedule.",
        "hero_accent1": "Courses",
        "hero_accent2": "Trainees",
        "hero_accent3": "Certificates",
        "page_title_about": "About <span class='blue-accent'>Qudra Institute</span>",
        "about_heading": "Our <span class='blue-accent'>Training Story</span>",
        "about_p1": "Qudra Institute launched in 2014 as a professional training platform aimed at bridging the gap between academic skills and labor market demands. Today, we are one of the leading training institutes in the Kingdom.",
        "about_p2": "We offer over 100 training courses in technology, management, and languages, with strategic partnerships with major tech companies such as Microsoft, AWS, and Google.",
        "about_p3": "Our graduates' employment rate exceeds 85% within 3 months of program completion — that's our true measure of success.",
        "about_stat1_label": "Graduates",
        "about_stat2_label": "Employment Rate",
        "about_stat3_label": "Partners",
        "page_title_courses": "Our <span class='blue-accent'>Courses</span>",
        "courses_intro": "Choose your career path — over 100 courses in various fields",
        "course1_title": "Project Management PMP",
        "course1_desc": "Full PMP certification prep with applied project — 4 intensive weeks.",
        "course1_meta": "4 Weeks · In-person + Remote",
        "course2_title": "Data Analysis with Python",
        "course2_desc": "From zero to pro — Pandas, NumPy, Matplotlib, SQL.",
        "course2_meta": "6 Weeks · Remote",
        "course3_title": "Cybersecurity for Beginners",
        "course3_desc": "InfoSec fundamentals, penetration testing, networks — fully hands-on.",
        "course3_meta": "8 Weeks · In-person",
        "course4_title": "Applied AI",
        "course4_desc": "Machine learning, neural networks, ChatGPT API — real projects.",
        "course4_meta": "10 Weeks · Remote",
        "course5_title": "Leadership & Executive Management",
        "course5_desc": "Leadership skills, team management, decision making — for managers.",
        "course5_meta": "3 Weeks · In-person",
        "course6_title": "Full-Stack Web Development",
        "course6_desc": "React, Node.js, MongoDB — build complete web apps from scratch.",
        "course6_meta": "12 Weeks · Remote",
        "page_title_contact": "Contact — Course Registration",
        "contact_heading": "Get in <span class='blue-accent'>Touch</span>",
        "form_heading": "Registration Request",
        "form_name": "Full Name",
        "form_name_ph": "Enter your name",
        "form_email": "Email",
        "form_email_ph": "example@email.com",
        "form_phone": "Phone Number",
        "form_phone_ph": "05xxxxxxxx",
        "form_course": "Desired Course",
        "form_course_ph": "Select a course",
        "form_message": "Your Inquiry",
        "form_message_ph": "Type your inquiry here",
        "form_submit": "Submit Request",
        "form_success": "Request sent! Our team will contact you within 24 hours.",
        "form_course1": "Project Management PMP",
        "form_course2": "Data Analysis Python",
        "form_course3": "Cybersecurity",
        "form_course4": "Artificial Intelligence",
        "form_course5": "Executive Leadership",
        "form_course6": "Full-Stack Web",
        "footer_desc": "Your destination for professional training — develop your skills, build your future.",
        "footer_links": "Links",
        "footer_progs": "Courses",
        "footer_contact": "Contact",
        "footer_course1": "Project Management",
        "footer_course2": "Data Analysis",
        "footer_course3": "Cybersecurity",
        "footer_copy": "Qudra Institute — All Rights Reserved.",
        "breadcrumb_home": "Home",
        "breadcrumb_about": "About",
        "breadcrumb_courses": "Courses",
        "breadcrumb_contact": "Contact",
        "cta_title": "Your Journey Starts Here",
        "cta_desc": "Enroll in any course and begin your professional journey",
        "cta_btn": "Register Now",
        "founder_quote": "We don't just hand out certificates — we create professionals ready to compete in the job market.",
        "founder_name": "— Fahad Al-Otaibi, Founder",
        "why1_title": "10+ Years Experience",
        "why1_desc": "In professional training",
        "why2_title": "Accredited Certificates",
        "why2_desc": "From official bodies",
        "why3_title": "Hands-on Training",
        "why3_desc": "Projects & workshops",
        "why4_title": "Job Support",
        "why4_desc": "Partnerships with 100+ companies",
        "back_to_top": "Back to Top",
        "contact_address": "Jeddah — Al Rawdah District",
        "contact_phone": "920022345",
        "contact_email": "info@qudra.edu.sa",
        "contact_hours": "9:00 AM — 9:00 PM (Sat — Thu)",
        "contact_hours_label": "Hours",
        "address_label": "Address",
        "phone_label": "Phone",
        "email_label": "Email",
        "course_badge": "Most Popular",
    }
}

SITES["03-noor-alhuda"] = {
    "ar": {
        "site_name": "نور الهدى",
        "site_tagline": "نور العلم ... هدى الإسلام ... حياة القرآن",
        "nav_home": "الرئيسية",
        "nav_about": "عن المعهد",
        "nav_programs": "البرامج",
        "nav_contact": "اتصل بنا",
        "lang_btn": "EN",
        "lang_btn_alt": "عربي",
        "hero_tag": "معهد قرآني وتعليمي",
        "hero_title": "نور <strong>العلم</strong><br>وهدى <span class='amber'>الإسلام</span>",
        "hero_desc": "معهد نور الهدى — وجهتك لتعلم القرآن الكريم والعلوم الشرعية واللغة العربية. بمناهج عريقة وأساتذة مجازين.",
        "hero_cta_primary": "برامجنا القرآنية",
        "hero_cta_secondary": "تعرف علينا",
        "hero_stat1_icon": "<i class='fas fa-book-quran'></i>",
        "hero_stat1": "حفظة قرآن",
        "hero_stat2_icon": "<i class='fas fa-chalkboard-user'></i>",
        "hero_stat2": "برنامج تعليمي",
        "hero_stat3_icon": "<i class='fas fa-globe'></i>",
        "hero_stat3": "طلاب حول العالم",
        "sec_why_title": "وش <span class='amber'>يميزنا</span>؟",
        "sec_why_desc": "تعليم يجمع بين الأصالة والمعاصرة",
        "feat1_title": "إسناد متصل",
        "feat1_desc": "قراءات متواترة بأسانيد متصلة إلى النبي ﷺ — نعتز بهذا الشرف العظيم.",
        "feat2_title": "مقرئون مجازون",
        "feat2_desc": "أساتذة حاصلون على إجازات في القراءات العشر برواياتها.",
        "feat3_title": "مناهج معتمدة",
        "feat3_desc": "برامج دراسية معتمدة من وزارة التعليم والهيئات الشرعية.",
        "feat4_title": "حلقات تفاعلية",
        "feat4_desc": "حلقات مباشرة عبر الزووم — تصحيح تلاوة، تحفيظ، تفسير.",
        "page_title_about": "عن معهد <span class='amber'>نور الهدى</span>",
        "about_heading": "رسالتنا <span class='amber'>القرآنية</span>",
        "about_p1": "منذ ١٩٩٨، ومعهد نور الهدى يضيء دروب العلم الشرعي وتعليم القرآن الكريم. بدأ كحلقة صغيرة في مسجد الحي، واليوم أصبح معهداً يضم أكثر من ١٠٠٠ طالب وطالبة من ٢٥ دولة.",
        "about_p2": "نقدم برامج تحفيظ القرآن الكريم برواية حفص عن عاصم والشعبة عن عاصم وورش عن نافع، مع شرح متون التجويد وأحكام التلاوة.",
        "about_p3": "مقرئونا حاصلون على إجازات في القراءات العشر من مشايخ كبار في السعودية ومصر والشام. كل طالب يحصل على إجازة عند إتمام الحفظ. نفتخر بتخريج أكثر من ٣٠٠ حافظ وحافظة للقرآن الكريم.",
        "about_stat1_label": "خريج حافظ",
        "about_stat2_label": "قراءة",
        "about_stat3_label": "دولة",
        "page_title_programs": "برامجنا <span class='amber'>القرآنية</span>",
        "programs_intro": "اختر برنامجك — رحلة مباركة مع القرآن",
        "prog1_title": "تحفيظ القرآن",
        "prog1_desc": "حفظ القرآن الكريم كاملاً بأحكام التجويد — مع متابعة يومية واختبارات دورية.",
        "prog1_meta": "٣-٥ سنوات · جميع الأعمار",
        "prog2_title": "إجازة القراءات",
        "prog2_desc": "القراءات العشر الصغرى والكبرى — بأسانيد متصلة إلى النبي ﷺ.",
        "prog2_meta": "حسب المستوى · للرجال والنساء",
        "prog3_title": "أحكام التجويد",
        "prog3_desc": "شرح متون تحفة الأطفال والجزرية — نظري وتطبيقي مع تصحيح التلاوة.",
        "prog3_meta": "٦ شهور · أسبوعياً",
        "prog4_title": "اللغة العربية",
        "prog4_desc": "نحو، صرف، بلاغة — لفهم القرآن والحديث بشكل أعمق.",
        "prog4_meta": "مستويات · حسب البرنامج",
        "prog5_title": "مواعظ قرآنية",
        "prog5_desc": "تدبر وتفسير — حلقات أسبوعية لفهم معاني القرآن وتطبيقها في الحياة.",
        "prog5_meta": "أسبوعياً · مجاناً",
        "prog6_title": "دورات صيفية",
        "prog6_desc": "برنامج حجز مكثف للصغار — حفظ وتجويد وأنشطة إيمانية.",
        "prog6_meta": "شهرين · صيفاً",
        "page_title_contact": "اتصل بنا — التسجيل في البرامج",
        "contact_heading": "تواصل مع <span class='amber'>نور الهدى</span>",
        "form_heading": "طلب التسجيل",
        "form_name": "الاسم الكامل",
        "form_name_ph": "أدخل اسمك",
        "form_email": "البريد الإلكتروني",
        "form_email_ph": "example@email.com",
        "form_phone": "رقم الجوال",
        "form_phone_ph": "05xxxxxxxx",
        "form_program": "البرنامج المطلوب",
        "form_program_ph": "اختر البرنامج",
        "form_message": "استفسارك",
        "form_message_ph": "اكتب استفسارك هنا",
        "form_submit": "إرسال الطلب",
        "form_success": "تم التسجيل! بارك الله فيك وسنكون على تواصل قريباً.",
        "form_prog1": "تحفيظ القرآن",
        "form_prog2": "إجازة القراءات",
        "form_prog3": "أحكام التجويد",
        "form_prog4": "اللغة العربية",
        "form_prog5": "مواعظ قرآنية",
        "form_prog6": "دورات صيفية",
        "footer_desc": "نور العلم — هدى الإسلام — حياة القرآن.",
        "footer_links": "روابط",
        "footer_progs": "البرامج",
        "footer_contact": "تواصل",
        "footer_prog1": "تحفيظ القرآن",
        "footer_prog2": "إجازة القراءات",
        "footer_prog3": "أحكام التجويد",
        "footer_copy": "معهد نور الهدى — جميع الحقوق محفوظة.",
        "breadcrumb_home": "الرئيسية",
        "breadcrumb_about": "عن المعهد",
        "breadcrumb_programs": "البرامج",
        "breadcrumb_contact": "اتصل بنا",
        "cta_title": "اقترب من القرآن",
        "cta_desc": "سجل الآن في أي برنامج — أول أسبوع مجاني",
        "cta_btn": "سجل الآن",
        "founder_quote": "خيركم من تعلم القرآن وعلمه. في نور الهدى، نجعل هذه البشارة واقعاً حياً.",
        "founder_name": "— الشيخ محمد بن إبراهيم آل سعد",
        "why1_title": "إسناد متصل",
        "why1_desc": "أسانيد متصلة إلى النبي ﷺ",
        "why2_title": "مقرئون مجازون",
        "why2_desc": "إجازات في القراءات العشر",
        "why3_title": "مناهج معتمدة",
        "why3_desc": "من وزارة التعليم",
        "why4_title": "٢٥+ دولة",
        "why4_desc": "طلاب من حول العالم",
        "back_to_top": "العودة للأعلى",
        "contact_address": "المدينة المنورة",
        "contact_phone": "٩٢٠٠٣٣٤٥٦",
        "contact_email": "info@nooralhuda.edu.sa",
        "contact_hours": "٨:٠٠ ص — ٨:٠٠ م (السبت — الأربعاء)",
        "contact_hours_label": "ساعات العمل",
        "address_label": "العنوان",
        "phone_label": "الهاتف",
        "email_label": "البريد الإلكتروني",
        "quran_ayat": "يَا أَيُّهَا الَّذِينَ آمَنُوا اتَّقُوا اللَّهَ وَآمِنُوا بِرَسُولِهِ يُؤْتِكُمْ كِفْلَيْنِ مِن رَّحْمَتِهِ",
        "quran_surah": "— سورة الحديد، الآية ٢٨",
    },
    "en": {
        "site_name": "Noor Alhuda",
        "site_tagline": "Light of Knowledge ... Guidance of Islam ... Life of Quran",
        "nav_home": "Home",
        "nav_about": "About",
        "nav_programs": "Programs",
        "nav_contact": "Contact",
        "lang_btn": "عربي",
        "lang_btn_alt": "EN",
        "hero_tag": "Quranic & Islamic Institute",
        "hero_title": "Light of <strong>Knowledge</strong><br>Guidance of <span class='amber'>Islam</span>",
        "hero_desc": "Noor Alhuda — your destination for learning the Holy Quran, Islamic sciences, and Arabic language. With time-honored curricula and certified reciters.",
        "hero_cta_primary": "Quran Programs",
        "hero_cta_secondary": "About Us",
        "hero_stat1_icon": "<i class='fas fa-book-quran'></i>",
        "hero_stat1": "Quran Memorizers",
        "hero_stat2_icon": "<i class='fas fa-chalkboard-user'></i>",
        "hero_stat2": "Programs",
        "hero_stat3_icon": "<i class='fas fa-globe'></i>",
        "hero_stat3": "Students Worldwide",
        "sec_why_title": "Why <span class='amber'>Noor Alhuda</span>?",
        "sec_why_desc": "Education combining authenticity with modernity",
        "feat1_title": "Connected Chain",
        "feat1_desc": "Uninterrupted chains of transmission to the Prophet ﷺ — we take pride in this great honor.",
        "feat2_title": "Certified Reciters",
        "feat2_desc": "Teachers holding licenses in the Ten Qira'at with all their narrations.",
        "feat3_title": "Accredited Curricula",
        "feat3_desc": "Study programs accredited by the Ministry of Education and Sharia bodies.",
        "feat4_title": "Interactive Circles",
        "feat4_desc": "Live sessions via Zoom — recitation correction, memorization, tafseer.",
        "page_title_about": "About <span class='amber'>Noor Alhuda</span>",
        "about_heading": "Our <span class='amber'>Quranic Mission</span>",
        "about_p1": "Since 1998, Noor Alhuda has been illuminating the path of Islamic learning and Quranic education. It began as a small circle in a neighborhood mosque, and today has become an institute with over 1,000 students from 25 countries.",
        "about_p2": "We offer programs for memorizing the Holy Quran with narration of Hafs from Asim, Al-Sha'ba from Asim, and Warsh from Nafi, along with commentary on Tajweed texts and recitation rules.",
        "about_p3": "Our reciters hold licenses in the Ten Qira'at from senior sheikhs in Saudi Arabia, Egypt, and the Levant. Each student receives a license upon completing memorization. We are proud to have graduated over 300 Quran memorizers.",
        "about_stat1_label": "Graduate Hafiz",
        "about_stat2_label": "Qira'at",
        "about_stat3_label": "Countries",
        "page_title_programs": "Our <span class='amber'>Quran Programs</span>",
        "programs_intro": "Choose your program — a blessed journey with the Quran",
        "prog1_title": "Quran Memorization",
        "prog1_desc": "Memorize the entire Holy Quran with Tajweed rules — daily follow-up and periodic tests.",
        "prog1_meta": "3-5 Years · All Ages",
        "prog2_title": "Qira'at License",
        "prog2_desc": "The Ten Minor and Major Qira'at — with chains of transmission to the Prophet ﷺ.",
        "prog2_meta": "By Level · Men & Women",
        "prog3_title": "Tajweed Rules",
        "prog3_desc": "Commentary on Tuhfat al-Atfal and Al-Jazariyyah texts — theoretical and applied with recitation correction.",
        "prog3_meta": "6 Months · Weekly",
        "prog4_title": "Arabic Language",
        "prog4_desc": "Grammar, morphology, rhetoric — for deeper understanding of Quran and Hadith.",
        "prog4_meta": "Levels · By Program",
        "prog5_title": "Quranic Reflections",
        "prog5_desc": "Tadabbur and Tafseer — weekly circles to understand Quranic meanings and apply them in life.",
        "prog5_meta": "Weekly · Free",
        "prog6_title": "Summer Courses",
        "prog6_desc": "Intensive summer program for children — memorization, Tajweed and faith activities.",
        "prog6_meta": "2 Months · Summer",
        "page_title_contact": "Contact — Program Registration",
        "contact_heading": "Get in <span class='amber'>Touch</span>",
        "form_heading": "Registration Request",
        "form_name": "Full Name",
        "form_name_ph": "Enter your name",
        "form_email": "Email",
        "form_email_ph": "example@email.com",
        "form_phone": "Phone Number",
        "form_phone_ph": "05xxxxxxxx",
        "form_program": "Desired Program",
        "form_program_ph": "Select a program",
        "form_message": "Your Inquiry",
        "form_message_ph": "Type your inquiry here",
        "form_submit": "Submit Request",
        "form_success": "Registration complete! May Allah bless you. We'll be in touch soon.",
        "form_prog1": "Quran Memorization",
        "form_prog2": "Qira'at License",
        "form_prog3": "Tajweed Rules",
        "form_prog4": "Arabic Language",
        "form_prog5": "Quranic Reflections",
        "form_prog6": "Summer Courses",
        "footer_desc": "Light of Knowledge — Guidance of Islam — Life of Quran.",
        "footer_links": "Links",
        "footer_progs": "Programs",
        "footer_contact": "Contact",
        "footer_prog1": "Quran Memorization",
        "footer_prog2": "Qira'at License",
        "footer_prog3": "Tajweed Rules",
        "footer_copy": "Noor Alhuda Institute — All Rights Reserved.",
        "breadcrumb_home": "Home",
        "breadcrumb_about": "About",
        "breadcrumb_programs": "Programs",
        "breadcrumb_contact": "Contact",
        "cta_title": "Draw Closer to the Quran",
        "cta_desc": "Register now in any program — first week free",
        "cta_btn": "Register Now",
        "founder_quote": "The best among you are those who learn the Quran and teach it. At Noor Alhuda, we make this glad tiding a living reality.",
        "founder_name": "— Sheikh Mohammed bin Ibrahim Al-Saad",
        "why1_title": "Connected Chain",
        "why1_desc": "Unbroken chain to the Prophet ﷺ",
        "why2_title": "Certified Reciters",
        "why2_desc": "Licenses in Ten Qira'at",
        "why3_title": "Accredited",
        "why3_desc": "Ministry of Education",
        "why4_title": "25+ Countries",
        "why4_desc": "Students worldwide",
        "back_to_top": "Back to Top",
        "contact_address": "Madinah",
        "contact_phone": "920033456",
        "contact_email": "info@nooralhuda.edu.sa",
        "contact_hours": "8:00 AM — 8:00 PM (Sat — Wed)",
        "contact_hours_label": "Hours",
        "address_label": "Address",
        "phone_label": "Phone",
        "email_label": "Email",
        "quran_ayat": "O you who have believed, fear Allah and believe in His Messenger; He will give you a double portion of His mercy.",
        "quran_surah": "— Surah Al-Hadid, Verse 28",
    }
}

SITES["04-saudi-future-university"] = {
    "ar": {
        "site_name": "جامعة المستقبل السعودي",
        "site_tagline": "تعليم بلا حدود — مستقبل بلا قيود",
        "nav_home": "الرئيسية",
        "nav_about": "عن الجامعة",
        "nav_programs": "البرامج",
        "nav_contact": "اتصل بنا",
        "lang_btn": "EN",
        "lang_btn_alt": "عربي",
        "hero_tag": "أول جامعة رقمية في المملكة",
        "hero_title": "تعليم بلا حدود<br><span class='gold-uni'>مستقبل بلا قيود</span>",
        "hero_desc": "جامعة المستقبل السعودي — أول جامعة رقمية معتمدة بالكامل في المملكة. ادرس عبر الإنترنت، احصل على شهادة معتمدة، وابنِ مستقبلك من أي مكان.",
        "hero_cta_primary": "استعرض التخصصات",
        "hero_cta_secondary": "لماذا SFU؟",
        "hero_stat1": "+ تخصص",
        "hero_stat2": "+ طالب",
        "hero_stat3": "دولة",
        "sec_why_title": "لماذا <span class='gold-uni'>SFU</span>؟",
        "sec_why_desc": "جامعة رقمية بالكامل — اعتماد دولي — مرونة كاملة",
        "feat1_title": "منصة ذكية",
        "feat1_desc": "محاضرات تفاعلية، ذكاء اصطناعي لتخصيص مسار التعلم، واختبارات تكيفية.",
        "feat2_title": "اعتماد دولي",
        "feat2_desc": "جميع برامجنا معتمدة من وزارة التعليم والاعتماد الأكاديمي الدولي (WASC).",
        "feat3_title": "تعلم بمرونة",
        "feat3_desc": "ادرس في أي وقت ومن أي مكان — المحاضرات مسجلة وحية، تناسب المهنيين والطلاب.",
        "feat4_title": "توظيف وشراكات",
        "feat4_desc": "شراكات مع ٢٠٠+ شركة في ١٥ دولة — برامج تدريب وتوظيف مباشر لخريجينا.",
        "page_title_about": "عن <span class='gold-uni'>جامعة المستقبل السعودي</span>",
        "about_heading": "رؤيتنا <span class='gold-uni'>الرقمية</span>",
        "about_p1": "تأسست جامعة المستقبل السعودي عام 2020 كأول جامعة رقمية بالكامل في المملكة العربية السعودية، برؤية طموحة لإعادة تعريف التعليم العالي في العصر الرقمي.",
        "about_p2": "نقدم برامج بكالوريوس وماجستير في أحدث التخصصات التقنية والإدارية، عبر منصة تعليمية ذكية تستخدم تقنيات الذكاء الاصطناعي لتخصيص مسار التعلم لكل طالب.",
        "about_p3": "لدينا طلاب من ٤٥ دولة حول العالم، وشراكات أكاديمية مع ٣٠ جامعة دولية، وأكثر من ٢٠٠ شركة توظف خريجينا.",
        "about_stat1_label": "طالب وطالبة",
        "about_stat2_label": "دولة حول العالم",
        "about_stat3_label": "جامعة شريكة",
        "page_title_programs": "التخصصات <span class='gold-uni'>الرقمية</span>",
        "programs_intro": "١٥ تخصصاً — بكالوريوس وماجستير — في أحدث المجالات التقنية والإدارية",
        "prog1_title": "الذكاء الاصطناعي",
        "prog1_desc": "تعلم الآلة، الشبكات العصبية، معالجة اللغات الطبيعية، الرؤية الحاسوبية.",
        "prog1_meta": "٤ سنوات · عن بُعد",
        "prog2_title": "علوم البيانات",
        "prog2_desc": "تحليل البيانات الضخمة، BI، التعلم الإحصائي، SQL/Python.",
        "prog2_meta": "٤ سنوات · عن بُعد",
        "prog3_title": "الأمن السيبراني",
        "prog3_desc": "أمن المعلومات، اختبار الاختراق، حوكمة، تحليل الثغرات.",
        "prog3_meta": "٤ سنوات · عن بُعد",
        "prog4_title": "الحوسبة السحابية",
        "prog4_desc": "AWS, Azure, GCP, DevOps, Kubernetes.",
        "prog4_meta": "٤ سنوات · عن بُعد",
        "prog5_title": "التجارة الإلكترونية",
        "prog5_desc": "متاجر إلكترونية، تسويق رقمي، تحليلات، وإدارة منصات.",
        "prog5_meta": "٤ سنوات · عن بُعد",
        "prog6_title": "إدارة التقنية (MTech)",
        "prog6_desc": "ماجستير تنفيذي في إدارة التقنية والتحول الرقمي.",
        "prog6_meta": "١.٥ سنة · عن بُعد",
        "page_title_contact": "اتصل بنا — القبول والتسجيل",
        "contact_heading": "القبول والتسجيل",
        "form_heading": "طلب القبول",
        "form_name": "الاسم الكامل",
        "form_name_ph": "أدخل اسمك",
        "form_email": "البريد الإلكتروني",
        "form_email_ph": "example@email.com",
        "form_phone": "رقم الجوال",
        "form_phone_ph": "05xxxxxxxx",
        "form_program": "التخصص المطلوب",
        "form_program_ph": "اختر التخصص",
        "form_nationality": "الجنسية",
        "form_nationality_ph": "سعودي / غير سعودي",
        "form_qualification": "المؤهل السابق",
        "form_submit": "تقديم الطلب",
        "form_success": "تم تقديم طلبك. فريق القبول سيتواصل معك قريباً.",
        "form_prog1": "بكالوريوس الذكاء الاصطناعي",
        "form_prog2": "بكالوريوس علوم البيانات",
        "form_prog3": "بكالوريوس الأمن السيبراني",
        "form_prog4": "بكالوريوس الحوسبة السحابية",
        "form_prog5": "بكالوريوس التجارة الإلكترونية",
        "form_prog6": "ماجستير إدارة التقنية",
        "footer_desc": "أول جامعة رقمية معتمدة بالكامل في المملكة — منذ 2020.",
        "footer_links": "روابط",
        "footer_progs": "التخصصات",
        "footer_contact": "تواصل",
        "footer_prog1": "الذكاء الاصطناعي",
        "footer_prog2": "علوم البيانات",
        "footer_prog3": "الحوسبة السحابية",
        "footer_copy": "جامعة المستقبل السعودي — جميع الحقوق محفوظة.",
        "breadcrumb_home": "الرئيسية",
        "breadcrumb_about": "عن الجامعة",
        "breadcrumb_programs": "البرامج",
        "breadcrumb_contact": "اتصل بنا",
        "cta_title": "مستقبلك يبدأ من هنا",
        "cta_desc": "انضم لأكثر من ١٢ ألف طالب حول العالم",
        "cta_btn": "قدم الآن",
        "founder_quote": "التعليم الرقمي ليس مجرد خيار — إنه المستقبل. في SFU، نصنع هذا المستقبل اليوم.",
        "founder_name": "— د. سليمان القصيبي، رئيس الجامعة",
        "why1_title": "تخصيص بالذكاء الاصطناعي",
        "why1_desc": "مسار تعلم مخصص لكل طالب",
        "why2_title": "شهادة دولية",
        "why2_desc": "معترف بها عالمياً",
        "why3_title": "مرونة كاملة",
        "why3_desc": "ادرس أي وقت وأي مكان",
        "why4_title": "توظيف مباشر",
        "why4_desc": "شراكات مع ٢٠٠+ شركة",
        "back_to_top": "العودة للأعلى",
        "contact_address": "الرياض — حي القدس",
        "contact_phone": "920044556",
        "contact_email": "info@sfu.edu.sa",
        "contact_hours": "على مدار الساعة — 24/7",
        "contact_hours_label": "الدعم الفني",
        "address_label": "الموقع الإداري",
        "phone_label": "الهاتف",
        "email_label": "البريد الإلكتروني",
        "form_qualification_ph": "اختر المؤهل",
        "form_qual_high": "ثانوية عامة",
        "form_qual_diploma": "دبلوم",
        "form_qual_bachelor": "بكالوريوس",
        "form_qual_master": "ماجستير",
        "benefit1": "خصم ٢٥٪",
        "benefit1_desc": "للتسجيل المبكر",
        "benefit2": "منحة لابتوب",
        "benefit2_desc": "جميع الطلاب",
        "benefit3": "ضمان توظيف",
        "benefit3_desc": "خلال ٦ شهور",
        "benefit4": "شهادة دولية",
        "benefit4_desc": "معترف بها عالمياً",
    },
    "en": {
        "site_name": "Saudi Future University",
        "site_tagline": "Education Without Borders — Future Without Limits",
        "nav_home": "Home",
        "nav_about": "About",
        "nav_programs": "Programs",
        "nav_contact": "Contact",
        "lang_btn": "عربي",
        "lang_btn_alt": "EN",
        "hero_tag": "First Digital University in Saudi Arabia",
        "hero_title": "Education Without Borders<br><span class='gold-uni'>Future Without Limits</span>",
        "hero_desc": "Saudi Future University — the first fully accredited digital university in the Kingdom. Study online, earn an accredited degree, and build your future from anywhere.",
        "hero_cta_primary": "Browse Programs",
        "hero_cta_secondary": "Why SFU?",
        "hero_stat1": "+ Majors",
        "hero_stat2": "+ Students",
        "hero_stat3": "Countries",
        "sec_why_title": "Why <span class='gold-uni'>SFU</span>?",
        "sec_why_desc": "Fully digital — international accreditation — complete flexibility",
        "feat1_title": "Smart Platform",
        "feat1_desc": "Interactive lectures, AI-powered learning path personalization, and adaptive assessments.",
        "feat2_title": "International Accreditation",
        "feat2_desc": "All programs accredited by the Ministry of Education and WASC international accreditation.",
        "feat3_title": "Learn with Flexibility",
        "feat3_desc": "Study anytime, anywhere — recorded and live lectures, perfect for professionals and students.",
        "feat4_title": "Employment & Partnerships",
        "feat4_desc": "Partnerships with 200+ companies in 15 countries — direct training and employment programs.",
        "page_title_about": "About <span class='gold-uni'>Saudi Future University</span>",
        "about_heading": "Our <span class='gold-uni'>Digital Vision</span>",
        "about_p1": "Founded in 2020 as the first fully digital university in Saudi Arabia, with an ambitious vision to redefine higher education in the digital age.",
        "about_p2": "We offer bachelor's and master's programs in the latest technical and administrative fields, through a smart educational platform using AI to personalize each student's learning path.",
        "about_p3": "We have students from 45 countries, academic partnerships with 30 international universities, and over 200 companies that employ our graduates.",
        "about_stat1_label": "Students",
        "about_stat2_label": "Countries",
        "about_stat3_label": "Partner Universities",
        "page_title_programs": "<span class='gold-uni'>Digital</span> Programs",
        "programs_intro": "15+ majors — Bachelor's and Master's — in the latest technical and administrative fields",
        "prog1_title": "Artificial Intelligence",
        "prog1_desc": "Machine learning, neural networks, NLP, computer vision.",
        "prog1_meta": "4 Years · Online",
        "prog2_title": "Data Science",
        "prog2_desc": "Big data analysis, BI, statistical learning, SQL/Python.",
        "prog2_meta": "4 Years · Online",
        "prog3_title": "Cybersecurity",
        "prog3_desc": "Information security, penetration testing, governance, vulnerability analysis.",
        "prog3_meta": "4 Years · Online",
        "prog4_title": "Cloud Computing",
        "prog4_desc": "AWS, Azure, GCP, DevOps, Kubernetes.",
        "prog4_meta": "4 Years · Online",
        "prog5_title": "E-Commerce",
        "prog5_desc": "Online stores, digital marketing, analytics, platform management.",
        "prog5_meta": "4 Years · Online",
        "prog6_title": "Tech Management (MTech)",
        "prog6_desc": "Executive master's in technology management and digital transformation.",
        "prog6_meta": "1.5 Years · Online",
        "page_title_contact": "Contact — Admissions",
        "contact_heading": "Admissions & <span class='gold-uni'>Registration</span>",
        "form_heading": "Admission Application",
        "form_name": "Full Name",
        "form_name_ph": "Enter your name",
        "form_email": "Email",
        "form_email_ph": "example@email.com",
        "form_phone": "Phone Number",
        "form_phone_ph": "05xxxxxxxx",
        "form_program": "Desired Program",
        "form_program_ph": "Select program",
        "form_nationality": "Nationality",
        "form_nationality_ph": "Saudi / Non-Saudi",
        "form_qualification": "Previous Qualification",
        "form_submit": "Submit Application",
        "form_success": "Application submitted. Admissions team will contact you soon.",
        "form_prog1": "BSc Artificial Intelligence",
        "form_prog2": "BSc Data Science",
        "form_prog3": "BSc Cybersecurity",
        "form_prog4": "BSc Cloud Computing",
        "form_prog5": "BSc E-Commerce",
        "form_prog6": "MTech Management",
        "footer_desc": "First fully accredited digital university in the Kingdom — since 2020.",
        "footer_links": "Links",
        "footer_progs": "Programs",
        "footer_contact": "Contact",
        "footer_prog1": "Artificial Intelligence",
        "footer_prog2": "Data Science",
        "footer_prog3": "Cloud Computing",
        "footer_copy": "Saudi Future University — All Rights Reserved.",
        "breadcrumb_home": "Home",
        "breadcrumb_about": "About",
        "breadcrumb_programs": "Programs",
        "breadcrumb_contact": "Contact",
        "cta_title": "Your Future Starts Here",
        "cta_desc": "Join over 12,000 students worldwide",
        "cta_btn": "Apply Now",
        "founder_quote": "Digital education isn't just an option — it's the future. At SFU, we're building that future today.",
        "founder_name": "— Dr. Suleiman Al-Qusaibi, President",
        "why1_title": "AI Personalization",
        "why1_desc": "Custom learning path for each student",
        "why2_title": "Global Certificate",
        "why2_desc": "Internationally recognized",
        "why3_title": "Full Flexibility",
        "why3_desc": "Study anytime, anywhere",
        "why4_title": "Direct Employment",
        "why4_desc": "Partnerships with 200+ companies",
        "back_to_top": "Back to Top",
        "contact_address": "Riyadh — Al Quds District",
        "contact_phone": "920044556",
        "contact_email": "info@sfu.edu.sa",
        "contact_hours": "24/7 Support",
        "contact_hours_label": "Support",
        "address_label": "Address",
        "phone_label": "Phone",
        "email_label": "Email",
        "form_qualification_ph": "Select qualification",
        "form_qual_high": "High School",
        "form_qual_diploma": "Diploma",
        "form_qual_bachelor": "Bachelor's",
        "form_qual_master": "Master's",
        "benefit1": "25% Discount",
        "benefit1_desc": "Early registration",
        "benefit2": "Laptop Grant",
        "benefit2_desc": "All students",
        "benefit3": "Job Guarantee",
        "benefit3_desc": "Within 6 months",
        "benefit4": "International Degree",
        "benefit4_desc": "Globally recognized",
    }
}

SITES["05-alwaha-center"] = {
    "ar": {
        "site_name": "مركز الواحة",
        "site_tagline": "مكانك تتعلم وتنمي مهاراتك",
        "nav_home": "الرئيسية",
        "nav_about": "عن المركز",
        "nav_programs": "برامجنا",
        "nav_contact": "اتصل بنا",
        "lang_btn": "EN",
        "lang_btn_alt": "عربي",
        "hero_tag": "مركز تعلم مجتمعي",
        "hero_title": "مكانك <span class='coral'>تتعلم</span><br>وتنمي <span class='sand'>مهاراتك</span>",
        "hero_desc": "مركز الواحة — وجهتك للتعلم والإبداع في جدة. برامج فنية، رقمية، ولغوية للأطفال والكبار في بيئة محفزة وآمنة.",
        "hero_cta_primary": "برامجنا",
        "hero_cta_secondary": "اكتشف المركز",
        "sec_why_title": "ماذا تقدم <span class='coral'>الواحة</span>؟",
        "sec_why_desc": "برامج متنوعة تناسب جميع الأعمار والاهتمامات",
        "feat1_title": "الفنون والإبداع",
        "feat1_desc": "رسم، نحت، فخار، موسيقى — لجميع المستويات والأعمار.",
        "feat2_title": "البرمجة والتقنية",
        "feat2_desc": "برمجة للأطفال، تصميم مواقع، أساسيات الحاسب.",
        "feat3_title": "اللغات",
        "feat3_desc": "الإنجليزية، الفرنسية، التركية — محادثة وقواعد.",
        "feat4_title": "الحرف اليدوية",
        "feat4_desc": "تطريز، نسج، إكسسوارات يدوية — إبداع بيديك.",
        "page_title_about": "عن مركز <span class='coral'>الواحة</span>",
        "about_heading": "من نحن <span class='coral'>في الواحة</span>",
        "about_p1": "افتتح مركز الواحة أبوابه عام 2015 في جدة — حي الشاطئ — كأول مركز تعلم مجتمعي يقدم برامج متنوعة في الفنون واللغات والتقنية.",
        "about_p2": "منذ ذلك الحين، استقبلنا أكثر من 5000 طالب وطالبة من جميع الأعمار، وساعدناهم على اكتشاف مواهبهم وتطوير مهاراتهم.",
        "about_p3": "نفخر بأن العديد من طلابنا أصبحوا فنانين ومبرمجين ومصممين — وقصص نجاحهم هي أكبر دافع لنا للاستمرار والتطوير.",
        "about_stat1_label": "طالب وطالبة",
        "about_stat2_label": "برنامج تعليمي",
        "about_stat3_label": "مدرب معتمد",
        "about_stat4_label": "رضا الطلاب",
        "page_title_programs": "برامج <span class='coral'>الواحة</span>",
        "programs_intro": "٢٥+ برنامجاً — اختر ما يناسبك أو يناسب أطفالك",
        "prog1_title": "الرسم والألوان",
        "prog1_desc": "تعلم الرسم بالألوان الزيتية والمائية والأكريليك — من المبتدئين إلى المحترفين.",
        "prog1_meta": "٨ أسابيع · أطفال + كبار",
        "prog2_title": "البرمجة للأطفال",
        "prog2_desc": "مقدمة في البرمجة باستخدام Scratch و Python — بناء ألعاب وتطبيقات.",
        "prog2_meta": "١٠ أسابيع · من ٨-١٥ سنة",
        "prog3_title": "اللغة الإنجليزية",
        "prog3_desc": "محادثة، قواعد، كتابة — جميع المستويات مع متحدثين أصليين.",
        "prog3_meta": "١٢ أسبوع · جميع الأعمار",
        "prog4_title": "الحرف اليدوية",
        "prog4_desc": "فخار، نسج، تطريز، إكسسوارات — مشاريع إبداعية بمواد طبيعية.",
        "prog4_meta": "٨ أسابيع · جميع الأعمار",
        "prog5_title": "التصوير الفوتوغرافي",
        "prog5_desc": "أساسيات التصوير، الإضاءة، التركيب، المونتاج — التقط الجمال من حولك.",
        "prog5_meta": "٦ أسابيع · +١٥ سنة",
        "prog6_title": "الموسيقى والإيقاع",
        "prog6_desc": "العود، البيانو، الإيقاع — نظري وتطبيقي مع مدربين متخصصين.",
        "prog6_meta": "مستمر · من ١٠ سنوات",
        "page_title_contact": "اتصل بنا — التسجيل",
        "contact_heading": "تواصل مع <span class='coral'>الواحة</span>",
        "form_heading": "طلب التسجيل",
        "form_name": "الاسم الكامل",
        "form_name_ph": "أدخل اسمك",
        "form_email": "البريد الإلكتروني",
        "form_email_ph": "example@email.com",
        "form_phone": "رقم الجوال",
        "form_phone_ph": "05xxxxxxxx",
        "form_program": "البرنامج المطلوب",
        "form_program_ph": "اختر البرنامج",
        "form_message": "استفسارك",
        "form_message_ph": "اكتب استفسارك هنا",
        "form_submit": "تأكيد التسجيل",
        "form_success": "تم التسجيل! سنتواصل معك لتأكيد الموعد.",
        "form_prog1": "الرسم والألوان",
        "form_prog2": "البرمجة للأطفال",
        "form_prog3": "اللغة الإنجليزية",
        "form_prog4": "الحرف اليدوية",
        "form_prog5": "التصوير الفوتوغرافي",
        "form_prog6": "الموسيقى والإيقاع",
        "footer_desc": "مركز تعلم مجتمعي يطلق الإبداع — في جدة منذ 2015.",
        "footer_links": "روابط",
        "footer_progs": "البرامج",
        "footer_contact": "تواصل",
        "footer_prog1": "الفنون",
        "footer_prog2": "البرمجة",
        "footer_prog3": "اللغات",
        "footer_copy": "مركز الواحة — جميع الحقوق محفوظة.",
        "breadcrumb_home": "الرئيسية",
        "breadcrumb_about": "عن المركز",
        "breadcrumb_programs": "برامجنا",
        "breadcrumb_contact": "اتصل بنا",
        "cta_title": "تعال نتعلم ونبدع معاً",
        "cta_desc": "سجل الآن في برامجنا المتنوعة — أول جلسة مجانية",
        "cta_btn": "سجل الآن",
        "founder_quote": "في الواحة، نؤمن بأن كل إنسان لديه موهبة تنتظر من يكتشفها. هدفنا توفير بيئة تعليمية داعمة تطلق العنان للإبداع.",
        "founder_name": "— أ. حصة الغامدي، مؤسسة المركز",
        "why1_title": "بيئة آمنة",
        "why1_desc": "نرعى أطفالكم كما نرعى طلابنا",
        "why2_title": "مدربون معتمدون",
        "why2_desc": "كفاءات بخبرات عالمية",
        "why3_title": "برامج مرنة",
        "why3_desc": "مواعيد تناسب الجميع",
        "why4_title": "مجموعات صغيرة",
        "why4_desc": "تعلم أفضل وتفاعل أقوى",
        "back_to_top": "العودة للأعلى",
        "contact_address": "جدة — حي الشاطئ",
        "contact_phone": "920055678",
        "contact_email": "info@alwaha-center.edu.sa",
        "contact_hours": "٨:٠٠ ص — ٩:٠٠ م (السبت — الخميس)",
        "contact_hours_label": "ساعات العمل",
        "address_label": "العنوان",
        "phone_label": "الهاتف",
        "email_label": "البريد الإلكتروني",
    },
    "en": {
        "site_name": "Al-Waha Center",
        "site_tagline": "Learn, Create, and Grow Your Skills",
        "nav_home": "Home",
        "nav_about": "About",
        "nav_programs": "Programs",
        "nav_contact": "Contact",
        "lang_btn": "عربي",
        "lang_btn_alt": "EN",
        "hero_tag": "Community Learning Center",
        "hero_title": "Your Place <span class='coral'>to Learn</span><br>and <span class='sand'>Grow Your Skills</span>",
        "hero_desc": "Al-Waha Center — your destination for learning and creativity in Jeddah. Art, tech, and language programs for children and adults in a safe, inspiring environment.",
        "hero_cta_primary": "Our Programs",
        "hero_cta_secondary": "Discover Center",
        "sec_why_title": "What <span class='coral'>Al-Waha</span> Offers?",
        "sec_why_desc": "Diverse programs for all ages and interests",
        "feat1_title": "Arts & Creativity",
        "feat1_desc": "Drawing, sculpting, pottery, music — for all levels and ages.",
        "feat2_title": "Programming & Tech",
        "feat2_desc": "Kids coding, web design, computer basics.",
        "feat3_title": "Languages",
        "feat3_desc": "English, French, Turkish — conversation and grammar.",
        "feat4_title": "Handicrafts",
        "feat4_desc": "Embroidery, weaving, handmade accessories — creativity at your fingertips.",
        "page_title_about": "About <span class='coral'>Al-Waha Center</span>",
        "about_heading": "Who We <span class='coral'>Are</span>",
        "about_p1": "Al-Waha Center opened its doors in 2015 in Jeddah — Al Shati District — as the first community learning center offering diverse programs in arts, languages, and technology.",
        "about_p2": "Since then, we have welcomed over 5,000 students of all ages, helping them discover their talents and develop their skills.",
        "about_p3": "We are proud that many of our students have become artists, programmers, and designers — their success stories are our greatest motivation.",
        "about_stat1_label": "Students",
        "about_stat2_label": "Programs",
        "about_stat3_label": "Trainers",
        "about_stat4_label": "Satisfaction",
        "page_title_programs": "<span class='coral'>Al-Waha</span> Programs",
        "programs_intro": "25+ programs — choose what suits you or your children",
        "prog1_title": "Drawing & Painting",
        "prog1_desc": "Learn oil, watercolor, and acrylic painting — from beginners to professionals.",
        "prog1_meta": "8 Weeks · Kids + Adults",
        "prog2_title": "Kids Coding",
        "prog2_desc": "Introduction to programming with Scratch and Python — building games and apps.",
        "prog2_meta": "10 Weeks · Ages 8-15",
        "prog3_title": "English Language",
        "prog3_desc": "Conversation, grammar, writing — all levels with native speakers.",
        "prog3_meta": "12 Weeks · All Ages",
        "prog4_title": "Handicrafts",
        "prog4_desc": "Pottery, weaving, embroidery, accessories — creative projects with natural materials.",
        "prog4_meta": "8 Weeks · All Ages",
        "prog5_title": "Photography",
        "prog5_desc": "Basics of photography, lighting, composition, editing — capture beauty around you.",
        "prog5_meta": "6 Weeks · 15+",
        "prog6_title": "Music & Rhythm",
        "prog6_desc": "Oud, piano, percussion — theory and practice with specialized trainers.",
        "prog6_meta": "Ongoing · 10+",
        "page_title_contact": "Contact — Registration",
        "contact_heading": "Get in <span class='coral'>Touch</span>",
        "form_heading": "Registration Request",
        "form_name": "Full Name",
        "form_name_ph": "Enter your name",
        "form_email": "Email",
        "form_email_ph": "example@email.com",
        "form_phone": "Phone Number",
        "form_phone_ph": "05xxxxxxxx",
        "form_program": "Desired Program",
        "form_program_ph": "Select a program",
        "form_message": "Your Inquiry",
        "form_message_ph": "Type your inquiry here",
        "form_submit": "Confirm Registration",
        "form_success": "Registration confirmed! We will contact you to schedule.",
        "form_prog1": "Drawing & Painting",
        "form_prog2": "Kids Coding",
        "form_prog3": "English Language",
        "form_prog4": "Handicrafts",
        "form_prog5": "Photography",
        "form_prog6": "Music & Rhythm",
        "footer_desc": "A community learning center unleashing creativity — in Jeddah since 2015.",
        "footer_links": "Links",
        "footer_progs": "Programs",
        "footer_contact": "Contact",
        "footer_prog1": "Arts",
        "footer_prog2": "Programming",
        "footer_prog3": "Languages",
        "footer_copy": "Al-Waha Center — All Rights Reserved.",
        "breadcrumb_home": "Home",
        "breadcrumb_about": "About",
        "breadcrumb_programs": "Programs",
        "breadcrumb_contact": "Contact",
        "cta_title": "Let's Learn and Create Together",
        "cta_desc": "Register now in our diverse programs — first session free",
        "cta_btn": "Register Now",
        "founder_quote": "At Al-Waha, we believe every person has a talent waiting to be discovered. Our goal is to provide a supportive learning environment that unleashes creativity.",
        "founder_name": "— Hessa Al-Ghamdi, Founder",
        "why1_title": "Safe Environment",
        "why1_desc": "We care for your children as our own",
        "why2_title": "Certified Trainers",
        "why2_desc": "Expert professionals",
        "why3_title": "Flexible Programs",
        "why3_desc": "Schedules for everyone",
        "why4_title": "Small Groups",
        "why4_desc": "Better learning, stronger interaction",
        "back_to_top": "Back to Top",
        "contact_address": "Jeddah — Al Shati District",
        "contact_phone": "920055678",
        "contact_email": "info@alwaha-center.edu.sa",
        "contact_hours": "8:00 AM — 9:00 PM (Sat — Thu)",
        "contact_hours_label": "Hours",
        "address_label": "Address",
        "phone_label": "Phone",
        "email_label": "Email",
    }
}

# ===================== SCRIPT TEMPLATES =====================

def get_main_script(site_key):
    """Generate enhanced script.js with i18n + polish features for the given site."""
    site_name = site_key.replace('-', ' ').title()
    return f'''// {site_name} — Enhanced Script with i18n + Polish
document.addEventListener('DOMContentLoaded', () => {{
  // ===== Loading Screen =====
  setTimeout(() => document.getElementById('loading')?.classList.add('hide'), 600);

  // ===== Mobile Menu =====
  const menuToggle = document.getElementById('menuToggle');
  const navLinks = document.getElementById('navLinks');
  if (menuToggle && navLinks) {{
    menuToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
    navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));
  }}

  // ===== Language Toggle — Real Translation =====
  const langToggle = document.getElementById('langToggle');
  let currentLang = document.documentElement.lang || 'ar';
  if (langToggle) {{
    // Apply saved language preference
    const saved = localStorage.getItem('{site_key}_lang');
    if (saved && saved !== currentLang) {{
      currentLang = saved;
      applyLang(currentLang);
    }}
    langToggle.addEventListener('click', () => {{
      currentLang = currentLang === 'ar' ? 'en' : 'ar';
      applyLang(currentLang);
      localStorage.setItem('{site_key}_lang', currentLang);
    }});
  }}

  function applyLang(lang) {{
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.querySelectorAll('[data-i18n]').forEach(el => {{
      const key = el.dataset.i18n;
      const trans = window.__i18n && window.__i18n[lang] && window.__i18n[lang][key];
      if (trans) {{
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT') {{
          if (el.placeholder !== undefined && el.dataset.i18nPh) {{
            el.placeholder = window.__i18n[lang][el.dataset.i18nPh] || trans;
          }}
        }} else if (el.tagName === 'OPTION') {{
          el.textContent = trans;
        }} else {{
          el.innerHTML = trans;
        }}
      }}
    }});
    // Update lang button text
    if (langToggle) langToggle.textContent = window.__i18n && window.__i18n[lang] && window.__i18n[lang].lang_btn ? window.__i18n[lang].lang_btn : (lang === 'ar' ? 'EN' : 'عربي');
  }}

  // ===== Active Nav Link =====
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  navLinks?.querySelectorAll('a').forEach(a => {{
    const href = a.getAttribute('href');
    if (href === currentPath || (currentPath === '' && href === 'index.html')) a.classList.add('active');
    else a.classList.remove('active');
  }});

  // ===== Scroll Animations =====
  const observer = new IntersectionObserver(entries => {{
    entries.forEach(entry => {{ if (entry.isIntersecting) entry.target.classList.add('show'); }});
  }}, {{ threshold: 0.1, rootMargin: '0px 0px -50px 0px' }});
  document.querySelectorAll('.fade-in, .feat-uni, .prog-uni-card, .program-full-card, .waha-card, .prog-waha-card, .why-card, .feat-riyadh, .feat-qudra').forEach(el => {{
    if (!el.classList.contains('fade-in')) el.classList.add('fade-in');
    observer.observe(el);
  }});

  // ===== Counter Animation =====
  const counterObserver = new IntersectionObserver(entries => {{
    entries.forEach(entry => {{
      if (entry.isIntersecting) {{
        const el = entry.target;
        const target = parseInt(el.dataset.target);
        if (!target || el.dataset.animated) return;
        el.dataset.animated = 'true';
        let current = 0;
        const step = Math.max(1, Math.ceil(target / 50));
        const timer = setInterval(() => {{
          current = Math.min(current + step, target);
          el.textContent = current.toLocaleString() + '+';
          if (current >= target) clearInterval(timer);
        }}, 20);
        counterObserver.unobserve(el);
      }}
    }});
  }}, {{ threshold: 0.5 }});
  document.querySelectorAll('.stat-num-uni, .stat-num-riyadh, .stat-num-qudra, .stat-num-waha, .counter-num').forEach(el => counterObserver.observe(el));

  // ===== Back to Top Button =====
  let backToTop = document.getElementById('backToTop');
  if (!backToTop) {{
    backToTop = document.createElement('button');
    backToTop.id = 'backToTop';
    backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTop.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:999;width:44px;height:44px;border-radius:12px;background:var(--primary-uni, var(--coral, #7c3aed));color:#fff;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1.1rem;opacity:0;transform:translateY(20px);transition:0.4s;box-shadow:0 4px 16px rgba(0,0,0,.3);';
    backToTop.setAttribute('aria-label', 'Back to top');
    document.body.appendChild(backToTop);
    window.addEventListener('scroll', () => {{
      backToTop.style.opacity = window.scrollY > 400 ? '1' : '0';
      backToTop.style.transform = window.scrollY > 400 ? 'translateY(0)' : 'translateY(20px)';
    }});
    backToTop.addEventListener('click', () => window.scrollTo({{ top: 0, behavior: 'smooth' }}));
  }}

  // ===== Form Handling =====
  document.querySelectorAll('form').forEach(form => {{
    form.addEventListener('submit', e => {{
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      if (btn) btn.disabled = true;
      const successMsg = document.createElement('div');
      successMsg.className = 'form-success';
      const successKey = form.dataset.i18nSuccess || 'form_success';
      const msg = window.__i18n && window.__i18n[currentLang] && window.__i18n[currentLang][successKey];
      if (msg) successMsg.textContent = msg;
      else successMsg.textContent = '✓ تم إرسال الطلب بنجاح!';
      successMsg.style.cssText = 'padding:14px 18px;margin-top:16px;border-radius:10px;background:rgba(74,222,128,.15);color:#4ade80;text-align:center;font-weight:600;';
      form.appendChild(successMsg);
      setTimeout(() => {{ form.reset(); btn.disabled = false; }}, 2000);
      setTimeout(() => successMsg.remove(), 4000);
    }});
  }});

  // ===== Smooth scroll for anchor links =====
  document.querySelectorAll('a[href^="#"]').forEach(a => {{
    a.addEventListener('click', e => {{
      e.preventDefault();
      const target = document.querySelector(a.getAttribute('href'));
      if (target) target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }});
  }});

  // ===== Category Filter (for program pages) =====
  const filterBtns = document.querySelectorAll('.filter-btn');
  if (filterBtns.length) {{
    filterBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        filterBtns.forEach(b => b.style.background = 'var(--bg-card)');
        btn.style.background = 'var(--coral, var(--primary-uni))';
        btn.style.color = '#fff';
        // Simple filter logic — override as needed per page
      }});
    }});
  }}
}});
'''


# ===================== HTML PROCESSING =====================

def process_html(html_content, site_key, page_name, page_keys):
    """
    Process an HTML file:
    1. Add data-i18n attributes to translatable elements
    2. Add a script tag that loads the translation data
    Returns the modified HTML content.
    """
    # Add data-i18n to elements we recognize from page_keys
    for key in page_keys:
        # Replace the key in inner text
        en_text = SITES[site_key]["en"].get(key, "")
        ar_text = SITES[site_key]["ar"].get(key, "")
        if not en_text or not ar_text:
            continue
            
        # Pattern: find the Arabic text in the HTML and wrap it with data-i18n
        # We need to be careful with HTML tags inside the text (like <span>, <strong>)
        # Use the AR text as the marker since the HTML is in Arabic
        
        # Escape the text for regex
        # We look for the Arabic text in the HTML content
        # For texts with HTML tags, match the content flexibly
        
        # Simple approach: look for the Arabic string and add data-i18n attribute
        # to the parent element that contains it
        
        # Skip if text is empty or too short
        if len(ar_text) < 3:
            continue
            
        # For texts that contain HTML, we need a different approach
        has_html = '<' in ar_text or '<' in en_text
        
        if has_html:
            # For HTML content, we look for the pattern and wrap with data-i18n-html
            # Try to find an element that contains this HTML
            # This is tricky with regex — we'll handle specific cases
            pass
        else:
            # For plain text, find elements whose text content matches
            pass

    return html_content


def add_i18n_manually(html, key, ar_text, en_text):
    """Add data-i18n attribute to an element containing ar_text."""
    if not ar_text or len(ar_text) < 3:
        return html
    
    # Escape for regex
    escaped = re.escape(ar_text)
    
    # Try to find a tag that contains this text
    # Pattern: <tag ...>TEXT</tag> where TEXT contains ar_text
    # We want to add data-i18n="key" to the opening tag
    
    # First: handle cases where text might have been split by HTML
    # Simple case: text is directly inside a tag
    simple_pattern = rf'(<[^>]+?)>({re.escape(ar_text)})</'
    
    def add_attr(m):
        open_tag = m.group(1)
        if 'data-i18n' not in open_tag:
            return f'{open_tag} data-i18n="{key}">{m.group(2)}</'
        return m.group(0)
    
    html = re.sub(simple_pattern, add_attr, html)
    return html


def add_i18n_html_block(html, key, ar_text):
    """Add data-i18n-html attribute to block containing ar text with HTML."""
    if not ar_text or len(ar_text) < 3:
        return html

    # The text might contain inner HTML tags
    # Create a pattern that matches any inner tags
    pattern_parts = []
    i = 0
    while i < len(ar_text):
        if ar_text[i] == '<':
            # Find the end of this HTML tag
            j = ar_text.index('>', i)
            # Match any tag content
            pattern_parts.append(r'<[^>]*>')
            i = j + 1
        else:
            # Regular character
            c = re.escape(ar_text[i])
            pattern_parts.append(c)
            i += 1
    
    if not pattern_parts:
        return html
    
    pattern_str = ''.join(pattern_parts)
    
    # Look for this pattern inside a tag
    regex = rf'(<[^>]+?)>({pattern_str})</'
    
    def add_attr(m):
        open_tag = m.group(1)
        if 'data-i18n' not in open_tag:
            return f'{open_tag} data-i18n="{key} data-i18n-html">{m.group(2)}</'
        return m.group(0)
    
    html = re.sub(regex, add_attr, html, count=1)
    return html


# ===================== MAIN PROCESS =====================

def process_site(site_key):
    """Process all HTML files in a site folder."""
    site_dir = BASE / site_key
    if not site_dir.exists():
        print(f"  SKIP: {site_dir} not found")
        return
    
    print(f"\n{'='*60}")
    print(f"Processing: {site_key}")
    print(f"{'='*60}")
    
    # Get page-specific keys
    # We'll match keys by common prefixes
    for html_file in sorted(site_dir.glob("*.html")):
        fname = html_file.name
        print(f"  Reading: {fname}")
        content = html_file.read_text(encoding='utf-8')
        
        # Determine which keys apply to this page
        page_keys = []
        lang_data = SITES[site_key]
        
        # All pages
        base_keys = ['site_name', 'nav_home', 'nav_about', 'nav_programs', 'nav_contact', 
                     'lang_btn', 'back_to_top']
        page_keys.extend(base_keys)
        
        # Page-specific keys based on filename
        if fname == 'index.html':
            page_keys.extend(['hero_tag', 'hero_title', 'hero_desc', 'hero_cta_primary',
                            'hero_cta_secondary', 'sec_why_title', 'sec_why_desc',
                            'feat1_title', 'feat1_desc', 'feat2_title', 'feat2_desc',
                            'feat3_title', 'feat3_desc', 'feat4_title', 'feat4_desc',
                            'cta_title', 'cta_desc', 'cta_btn', 'founder_quote', 'founder_name',
                            'why1_title', 'why1_desc', 'why2_title', 'why2_desc',
                            'why3_title', 'why3_desc', 'why4_title', 'why4_desc',
                            'hero_stat1', 'hero_stat2', 'hero_stat3',
                            'footer_desc', 'footer_links', 'footer_progs', 'footer_contact',
                            'footer_prog1', 'footer_prog2', 'footer_prog3', 'footer_copy'])
            if 'riyadh' in site_key:
                page_keys.extend(['site_tagline', 'hero_stat_label1', 'hero_stat_label2', 'hero_stat_label3'])
            if 'qudra' in site_key:
                page_keys.extend(['hero_accent1', 'hero_accent2', 'hero_accent3'])
            if 'noor' in site_key:
                page_keys.extend(['quran_ayat', 'quran_surah'])
            if 'waha' in site_key:
                page_keys.extend([])
                
        elif fname == 'about.html':
            page_keys.extend(['page_title_about', 'about_heading', 'about_p1', 'about_p2', 'about_p3',
                            'about_stat1_label', 'about_stat2_label', 'about_stat3_label',
                            'footer_desc', 'footer_links', 'footer_progs', 'footer_contact',
                            'footer_prog1', 'footer_prog2', 'footer_prog3', 'footer_copy'])
            if 'waha' in site_key:
                page_keys.extend(['about_stat4_label'])
                            
        elif fname in ('programs.html', 'courses.html'):
            page_keys.extend(['page_title_programs', 'programs_intro',
                            'prog1_title', 'prog1_desc', 'prog1_meta',
                            'prog2_title', 'prog2_desc', 'prog2_meta',
                            'prog3_title', 'prog3_desc', 'prog3_meta',
                            'prog4_title', 'prog4_desc', 'prog4_meta',
                            'prog5_title', 'prog5_desc', 'prog5_meta',
                            'prog6_title', 'prog6_desc', 'prog6_meta',
                            'footer_desc', 'footer_links', 'footer_progs', 'footer_contact',
                            'footer_prog1', 'footer_prog2', 'footer_prog3', 'footer_copy'])
            if 'qudra' in site_key:
                page_keys.extend(['course_badge'])
                
        elif fname == 'contact.html':
            page_keys.extend(['page_title_contact', 'contact_heading', 'form_heading',
                            'form_name', 'form_name_ph', 'form_email', 'form_email_ph',
                            'form_phone', 'form_phone_ph', 'form_program', 'form_program_ph',
                            'form_message', 'form_message_ph', 'form_submit', 'form_success',
                            'footer_desc', 'footer_links', 'footer_progs', 'footer_contact',
                            'footer_prog1', 'footer_prog2', 'footer_prog3', 'footer_copy'])
            if 'riyadh' in site_key:
                page_keys.extend(['form_prog1', 'form_prog2', 'form_prog3', 'form_prog4', 'form_prog5', 'form_prog6',
                                'contact_address', 'contact_phone', 'contact_email', 'contact_hours',
                                'contact_hours_label', 'address_label', 'phone_label', 'email_label',
                                'form_prog1', 'form_prog2', 'form_prog3', 'form_prog4', 'form_prog5', 'form_prog6',
                                'benefit1', 'benefit1_desc', 'benefit2', 'benefit2_desc', 'benefit3', 'benefit3_desc', 'benefit4', 'benefit4_desc'])
            if 'qudra' in site_key:
                page_keys.extend(['form_course', 'form_course_ph', 'form_course1', 'form_course2', 'form_course3', 'form_course4', 'form_course5', 'form_course6',
                                'contact_address', 'contact_phone', 'contact_email', 'contact_hours',
                                'contact_hours_label', 'address_label', 'phone_label', 'email_label'])
            if 'noor' in site_key:
                page_keys.extend(['form_prog1', 'form_prog2', 'form_prog3', 'form_prog4', 'form_prog5', 'form_prog6',
                                'contact_address', 'contact_phone', 'contact_email', 'contact_hours',
                                'contact_hours_label', 'address_label', 'phone_label', 'email_label'])
            if 'waha' in site_key:
                page_keys.extend(['form_prog1', 'form_prog2', 'form_prog3', 'form_prog4', 'form_prog5', 'form_prog6',
                                'contact_address', 'contact_phone', 'contact_email', 'contact_hours',
                                'contact_hours_label', 'address_label', 'phone_label', 'email_label'])
            if 'uni' in site_key or 'future' in site_key:
                page_keys.extend(['form_nationality', 'form_nationality_ph', 'form_qualification', 'form_qualification_ph',
                                'form_qual_high', 'form_qual_diploma', 'form_qual_bachelor', 'form_qual_master',
                                'contact_address', 'contact_phone', 'contact_email', 'contact_hours',
                                'contact_hours_label', 'address_label', 'phone_label', 'email_label',
                                'benefit1', 'benefit1_desc', 'benefit2', 'benefit2_desc', 'benefit3', 'benefit3_desc', 'benefit4', 'benefit4_desc'])
        
        # Deduplicate
        page_keys = list(set(page_keys))
        
        # Add data-i18n attributes for each key
        for key in page_keys:
            ar_text = lang_data['ar'].get(key, '')
            en_text = lang_data['en'].get(key, '')
            
            # Check if the text contains HTML
            has_html = bool(re.search(r'<[^>]+>', ar_text))
            
            if has_html:
                content = add_i18n_html_block(content, key, ar_text)
            else:
                content = add_i18n_manually(content, key, ar_text, en_text)
        
        # Add the i18n data script before </body>
        i18n_script = f'\n<script>window.__i18n={json.dumps(lang_data, ensure_ascii=False, indent=2)};</script>\n'
        
        # Make sure our script.js is loaded (but after our data)
        content = content.replace('</body>', f'{i18n_script}</body>')
        
        # Write back
        html_file.write_text(content, encoding='utf-8')
        print(f"  [OK] Updated: {fname} ({len(page_keys)} keys)")
    
    # Write enhanced script.js
    script_content = get_main_script(site_key)
    script_file = site_dir / 'script.js'
    script_file.write_text(script_content, encoding='utf-8')
    print(f"  [OK] Written: script.js")


def main():
    for site_key in SITES.keys():
        process_site(site_key)
    
    print(f"\n{'='*60}")
    print("ALL SITES PROCESSED!")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
