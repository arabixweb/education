// Qudra Institute — reliable explicit i18n, premium motion and interactions
(() => {
  'use strict';
  document.documentElement.classList.add('js');

  document.addEventListener('DOMContentLoaded', () => {
    const root = document.documentElement;
    const dictionary = window.__i18n || { ar: {}, en: {} };
    const langToggle = document.getElementById('langToggle');
    const loading = document.getElementById('loading');
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let currentLang = localStorage.getItem('edu_lang') === 'en' ? 'en' : 'ar';

    const valueFor = (lang, key) => dictionary[lang] && dictionary[lang][key];

    function applyLanguage(lang) {
      if (!dictionary[lang]) return;
      currentLang = lang;
      root.lang = lang;
      root.dir = lang === 'ar' ? 'rtl' : 'ltr';
      root.dataset.lang = lang;

      document.querySelectorAll('[data-i18n]').forEach((el) => {
        const value = valueFor(lang, el.dataset.i18n);
        if (typeof value === 'string') el.textContent = value;
      });
      document.querySelectorAll('[data-i18n-ph]').forEach((el) => {
        const value = valueFor(lang, el.dataset.i18nPh);
        if (typeof value === 'string') el.placeholder = value;
      });
      document.querySelectorAll('[data-i18n-alt]').forEach((el) => {
        const value = valueFor(lang, el.dataset.i18nAlt);
        if (typeof value === 'string') el.alt = value;
      });

      const titleKey = root.dataset.titleI18n;
      if (titleKey && valueFor(lang, titleKey)) document.title = valueFor(lang, titleKey);
      if (langToggle) {
        langToggle.textContent = lang === 'ar' ? 'EN' : 'عربي';
        langToggle.setAttribute('aria-label', lang === 'ar' ? 'Switch to English' : 'التبديل إلى العربية');
      }
      document.querySelectorAll('.nav-logo svg text').forEach((text) => { text.textContent = lang === 'ar' ? 'ق' : 'Q'; });
      document.querySelectorAll('.fa-arrow-left, .fa-arrow-right').forEach((icon) => {
        icon.classList.toggle('fa-arrow-left', lang === 'ar');
        icon.classList.toggle('fa-arrow-right', lang === 'en');
      });
      localStorage.setItem('edu_lang', lang);
      window.dispatchEvent(new CustomEvent('qudra:languagechange', { detail: { lang } }));
    }

    applyLanguage(currentLang);
    if (langToggle) langToggle.addEventListener('click', () => applyLanguage(currentLang === 'ar' ? 'en' : 'ar'));
    window.qudraLanguageReady = true;

    // Loading screen always releases, even if another feature fails.
    const releaseLoader = () => loading && loading.classList.add('hide');
    window.addEventListener('load', releaseLoader, { once: true });
    setTimeout(releaseLoader, 850);

    // Navigation.
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');
    if (menuToggle && navLinks) {
      menuToggle.setAttribute('aria-label', 'Menu');
      menuToggle.setAttribute('aria-expanded', 'false');
      menuToggle.addEventListener('click', () => {
        const open = navLinks.classList.toggle('open');
        menuToggle.classList.toggle('open', open);
        menuToggle.setAttribute('aria-expanded', String(open));
      });
      navLinks.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => {
        navLinks.classList.remove('open');
        menuToggle.classList.remove('open');
        menuToggle.setAttribute('aria-expanded', 'false');
      }));
      const file = location.pathname.split('/').pop() || 'index.html';
      navLinks.querySelectorAll('a').forEach((a) => a.classList.toggle('active', a.getAttribute('href') === file));
    }

    const navbar = document.querySelector('.navbar');
    const onScroll = () => navbar && navbar.classList.toggle('scrolled', scrollY > 50);
    onScroll();
    addEventListener('scroll', onScroll, { passive: true });

    // Progressive reveal: content is visible without JS; observers only enhance it.
    const revealElements = document.querySelectorAll('.reveal, .fade-in');
    if (!reduceMotion && 'IntersectionObserver' in window) {
      const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('show');
            revealObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.08, rootMargin: '0px 0px -35px 0px' });
      revealElements.forEach((el, i) => {
        el.style.setProperty('--reveal-delay', `${Math.min(i % 4, 3) * 80}ms`);
        revealObserver.observe(el);
      });
    } else revealElements.forEach((el) => el.classList.add('show'));

    // Counters; labels are never overwritten.
    const animateCounter = (el) => {
      if (el.dataset.animated) return;
      el.dataset.animated = 'true';
      const target = Number.parseInt(el.dataset.target || '0', 10);
      if (!target) return;
      const started = performance.now();
      const duration = 1500;
      const tick = (now) => {
        const progress = Math.min((now - started) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(target * eased).toLocaleString(currentLang === 'ar' ? 'ar-SA' : 'en-US');
        if (progress < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    const counters = document.querySelectorAll('[data-target]');
    if ('IntersectionObserver' in window && !reduceMotion) {
      const counterObserver = new IntersectionObserver((entries) => entries.forEach((entry) => {
        if (entry.isIntersecting) { animateCounter(entry.target); counterObserver.unobserve(entry.target); }
      }), { threshold: 0.4 });
      counters.forEach((el) => counterObserver.observe(el));
    } else counters.forEach(animateCounter);

    // Hero depth follows pointer without obscuring content.
    const heroVisual = document.getElementById('heroVisual') || document.querySelector('.hero-visual');
    if (heroVisual && !reduceMotion && matchMedia('(pointer:fine)').matches) {
      const shell = heroVisual.querySelector('.hero-image-shell') || heroVisual;
      heroVisual.addEventListener('pointermove', (event) => {
        const rect = heroVisual.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - 0.5;
        const y = (event.clientY - rect.top) / rect.height - 0.5;
        shell.style.transform = `perspective(1100px) rotateY(${x * 5}deg) rotateX(${-y * 5}deg) translateY(-4px)`;
      });
      heroVisual.addEventListener('pointerleave', () => { shell.style.transform = ''; });
    }

    // Back to top.
    const back = document.createElement('button');
    back.id = 'backToTop';
    back.innerHTML = '<i class="fas fa-arrow-up"></i>';
    back.setAttribute('aria-label', 'Back to top');
    document.body.appendChild(back);
    const toggleBack = () => back.classList.toggle('visible', scrollY > 500);
    addEventListener('scroll', toggleBack, { passive: true }); toggleBack();
    back.addEventListener('click', () => scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }));

    // Demo form feedback.
    document.querySelectorAll('form').forEach((form) => form.addEventListener('submit', (event) => {
      event.preventDefault();
      form.querySelector('.form-success')?.remove();
      const box = document.createElement('div');
      box.className = 'form-success';
      box.textContent = currentLang === 'ar' ? 'تم إرسال طلبك بنجاح. سيتواصل معك فريقنا قريباً.' : 'Your request was sent successfully. Our team will contact you shortly.';
      form.appendChild(box);
      setTimeout(() => box.remove(), 5000);
    }));

    window.qudraSiteReady = true;
    window.dispatchEvent(new Event('qudra:ready'));
  });
})();
