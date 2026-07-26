// Al-Waha Center v2 — premium bilingual static i18n, oasis particles, loader, reveals, counters, form, back-to-top
(function(){
'use strict';

// ====== REDUCED MOTION ======
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
if (reduceMotion) document.documentElement.classList.add('no-motion');

// ====== LOADER ======
const loading = document.getElementById('loading');

function domReady(fn) {
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
  else fn();
}

domReady(function(){
  // ====== LOADER ======
  if (loading) setTimeout(() => loading.classList.add('hide'), 600);

  // ====== i18n ======
  const i18n = window.__i18n || {};
  const langToggle = document.getElementById('langToggle');
  let currentLang = localStorage.getItem('waha_lang') || 'ar';

  function applyLang(lang) {
    currentLang = lang;
    localStorage.setItem('waha_lang', lang);
    const dict = i18n[lang];
    if (!dict) return;
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    // data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (dict[key]) el.textContent = dict[key];
    });
    // data-i18n-html (titles with markup)
    document.querySelectorAll('[data-i18n-html]').forEach(el => {
      const key = el.getAttribute('data-i18n-html');
      if (dict[key]) el.innerHTML = dict[key];
    });
    // data-i18n-placeholder
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      if (dict[key]) el.placeholder = dict[key];
    });
    // data-i18n-alt
    document.querySelectorAll('[data-i18n-alt]').forEach(el => {
      const key = el.getAttribute('data-i18n-alt');
      if (dict[key]) el.alt = dict[key];
    });
    // page title
    const titleKey = dict.page_title;
    if (titleKey) document.title = titleKey;
    // lang toggle
    if (langToggle) langToggle.innerHTML = `<i class="fa-solid fa-globe"></i><span>${lang === 'ar' ? 'EN' : 'عربي'}</span>`;
    // brand name
    const brandName = document.querySelector('.brand-copy strong');
    if (brandName && dict.brand_name) brandName.textContent = dict.brand_name;
    // brand tag
    const brandTag = document.querySelector('.brand-copy small');
    if (brandTag && dict.brand_tag) brandTag.textContent = dict.brand_tag;
    // aria-labels
    document.getElementById('langToggle')?.setAttribute('aria-label', lang === 'ar' ? 'Switch to English' : 'التبديل إلى العربية');
  }

  if (langToggle && i18n.ar) {
    if (currentLang === 'en') applyLang('en');
    langToggle.addEventListener('click', () => applyLang(currentLang === 'ar' ? 'en' : 'ar'));
  }

  // ====== MOBILE MENU ======
  const menuToggle = document.getElementById('menuToggle');
  const navLinks = document.getElementById('navLinks');
  const menuBackdrop = document.getElementById('menuBackdrop');

  function closeMenu() {
    navLinks && navLinks.classList.remove('open');
    menuToggle && menuToggle.classList.remove('open');
    menuBackdrop && menuBackdrop.classList.remove('open');
    menuToggle && menuToggle.setAttribute('aria-expanded', 'false');
  }

  function openMenu() {
    navLinks && navLinks.classList.add('open');
    menuToggle && menuToggle.classList.add('open');
    menuBackdrop && menuBackdrop.classList.add('open');
    menuToggle && menuToggle.setAttribute('aria-expanded', 'true');
  }

  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      const open = navLinks.classList.contains('open');
      open ? closeMenu() : openMenu();
    });
    navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
    if (menuBackdrop) menuBackdrop.addEventListener('click', closeMenu);
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
  }

  // ====== ACTIVE NAV LINK ======
  if (navLinks) {
    const file = window.location.pathname.split('/').pop() || 'index.html';
    navLinks.querySelectorAll('a').forEach(a => {
      const href = a.getAttribute('href');
      if (href === file || (file === 'index.html' && href === 'index.html')) a.classList.add('active');
    });
  }

  // ====== SCROLL REVEALS ======
  let observer;
  if (!reduceMotion && 'IntersectionObserver' in window) {
    observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('show');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  } else {
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('show'));
  }

  // ====== COUNTERS ======
  const counterObs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseFloat(el.getAttribute('data-count'));
      if (!target || el.dataset.animated === '1') return;
      el.dataset.animated = '1';
      let current = 0;
      const steps = 45;
      const increment = target / steps;
      const timer = setInterval(() => {
        current = Math.min(current + increment, target);
        el.textContent = Math.floor(current).toLocaleString() + '+';
        if (current >= target) clearInterval(timer);
      }, 24);
      counterObs.unobserve(el);
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('[data-count]').forEach(el => counterObs.observe(el));

  // ====== HERO PARTICLES ======
  const particleContainer = document.getElementById('heroParticles');
  if (particleContainer && !reduceMotion) {
    const count = Math.min(30, Math.floor(window.innerWidth / 35));
    for (let i = 0; i < count; i++) {
      const span = document.createElement('span');
      span.style.left = Math.random() * 100 + '%';
      span.style.top = Math.random() * 100 + '%';
      span.style.animationDelay = Math.random() * 8 + 's';
      span.style.animationDuration = (6 + Math.random() * 4) + 's';
      particleContainer.appendChild(span);
    }
  }

  // ====== FOOTER BACK TO TOP ======
  document.querySelector('.footer-top')?.addEventListener('click', () => scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }));

  // ====== BACK TO TOP BUTTON ======
  const topBtn = document.getElementById('backToTop');
  if (topBtn) {
    const showTop = () => topBtn.classList.toggle('visible', scrollY > 500);
    addEventListener('scroll', showTop, { passive: true });
    showTop();
    topBtn.addEventListener('click', () => scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }));
  }

  // ====== CONTACT FORM ======
  const form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const btn = form.querySelector('.form-submit');
      if (btn) btn.disabled = true;
      const status = form.querySelector('.form-status');
      const dict = i18n[currentLang];
      const msg = (dict && dict.form_success) || '✓ We received your request. We will contact you soon.';
      if (status) { status.textContent = msg; status.style.color = '#328267'; }
      setTimeout(() => { form.reset(); if (btn) btn.disabled = false; }, 2500);
      setTimeout(() => { if (status) status.textContent = ''; }, 5000);
    });
  }

  // ====== SIGNAL READY ======
  window.wahaSiteReady = true;
  document.dispatchEvent(new Event('waha:ready'));
});
})();
