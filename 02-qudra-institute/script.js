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
      document.querySelectorAll('.brand-letter').forEach((text) => { text.textContent = lang === 'ar' ? 'ق' : 'Q'; });
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
    const menuBackdrop = document.getElementById('menuBackdrop');
    if (menuToggle && navLinks) {
      menuToggle.setAttribute('aria-label', 'Menu');
      menuToggle.setAttribute('aria-expanded', 'false');
      const setMenu = (open) => {
        navLinks.classList.toggle('open', open);
        menuToggle.classList.toggle('open', open);
        menuBackdrop?.classList.toggle('open', open);
        menuToggle.setAttribute('aria-expanded', String(open));
        document.body.classList.toggle('menu-open', open);
      };
      menuToggle.addEventListener('click', () => setMenu(!navLinks.classList.contains('open')));
      menuBackdrop?.addEventListener('click', () => setMenu(false));
      document.addEventListener('keydown', (event) => { if (event.key === 'Escape') setMenu(false); });
      navLinks.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => {
        setMenu(false);
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

    // Living hero network — lightweight animated nodes, connections and pointer response.
    const networkCanvas = document.getElementById('heroNetwork');
    if (networkCanvas && !reduceMotion) {
      const context = networkCanvas.getContext('2d');
      let networkFrame = 0;
      let networkWidth = 0;
      let networkHeight = 0;
      let particles = [];
      const pointer = { x: -1000, y: -1000 };
      const resizeNetwork = () => {
        const rect = networkCanvas.getBoundingClientRect();
        const ratio = Math.min(devicePixelRatio || 1, 1.5);
        networkWidth = rect.width; networkHeight = rect.height;
        networkCanvas.width = Math.round(networkWidth * ratio);
        networkCanvas.height = Math.round(networkHeight * ratio);
        context.setTransform(ratio, 0, 0, ratio, 0, 0);
        const count = Math.max(22, Math.min(54, Math.round(networkWidth / 27)));
        particles = Array.from({ length: count }, () => ({
          x: Math.random() * networkWidth, y: Math.random() * networkHeight,
          vx: (Math.random() - .5) * .18, vy: (Math.random() - .5) * .18,
          size: Math.random() * 1.3 + .55, phase: Math.random() * Math.PI * 2
        }));
      };
      const drawNetwork = (time) => {
        context.clearRect(0, 0, networkWidth, networkHeight);
        particles.forEach((point, index) => {
          point.x += point.vx; point.y += point.vy;
          if (point.x < -15) point.x = networkWidth + 15; else if (point.x > networkWidth + 15) point.x = -15;
          if (point.y < -15) point.y = networkHeight + 15; else if (point.y > networkHeight + 15) point.y = -15;
          const dxp = pointer.x - point.x, dyp = pointer.y - point.y;
          const pd = Math.hypot(dxp, dyp);
          if (pd < 130) { point.x -= dxp * .0008; point.y -= dyp * .0008; }
          for (let j = index + 1; j < particles.length; j += 1) {
            const other = particles[j]; const dx = other.x - point.x; const dy = other.y - point.y;
            const distance = Math.hypot(dx, dy);
            if (distance < 135) {
              context.beginPath(); context.moveTo(point.x, point.y); context.lineTo(other.x, other.y);
              context.strokeStyle = `rgba(46,205,255,${(1 - distance / 135) * .13})`; context.lineWidth = .65; context.stroke();
            }
          }
          const glow = .55 + Math.sin(time * .0015 + point.phase) * .3;
          context.beginPath(); context.arc(point.x, point.y, point.size, 0, Math.PI * 2);
          context.fillStyle = `rgba(103,232,255,${glow})`; context.fill();
        });
        networkFrame = requestAnimationFrame(drawNetwork);
      };
      resizeNetwork(); networkFrame = requestAnimationFrame(drawNetwork);
      addEventListener('resize', resizeNetwork, { passive: true });
      networkCanvas.closest('.hero')?.addEventListener('pointermove', (event) => {
        const rect = networkCanvas.getBoundingClientRect(); pointer.x = event.clientX - rect.left; pointer.y = event.clientY - rect.top;
      });
      networkCanvas.closest('.hero')?.addEventListener('pointerleave', () => { pointer.x = -1000; pointer.y = -1000; });
      document.addEventListener('visibilitychange', () => {
        if (document.hidden) cancelAnimationFrame(networkFrame); else networkFrame = requestAnimationFrame(drawNetwork);
      });
    }

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
