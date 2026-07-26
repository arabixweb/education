// Saudi Future University v2 — premium bilingual static i18n, dynamic hero, loader, reveals, counters, filter, form, network canvas
(function(){
'use strict';

// ====== LOADER ======
const loading = document.getElementById('loading');

// ====== REDUCED MOTION ======
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
if (reduceMotion) document.documentElement.classList.add('no-motion');

function domReady(fn) {
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
  else fn();
}

domReady(function(){
  // ====== loading screen ======
  if (loading) setTimeout(() => loading.classList.add('hide'), 600);

  // ====== i18n ======
  const i18n = window.__i18n || {};
  const langToggle = document.getElementById('langToggle');
  let currentLang = localStorage.getItem('sfu_lang') || 'ar';

  function applyLang(lang) {
    currentLang = lang;
    localStorage.setItem('sfu_lang', lang);
    const dict = i18n[lang];
    if (!dict) return;
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    // data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (dict[key]) el.textContent = dict[key];
    });
    // data-i18n-html
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
    // lang toggle button text
    if (langToggle) langToggle.innerHTML = `<i class="fa-solid fa-globe"></i><span>${lang === 'ar' ? 'EN' : 'عربي'}</span>`;
    // brand name from shared dict
    const brandName = document.querySelector('.brand-copy strong');
    if (brandName && dict.brand_name) brandName.textContent = dict.brand_name;
    // brand tag
    const brandTag = document.querySelector('.brand-copy small');
    if (brandTag && dict.brand_tag) brandTag.textContent = dict.brand_tag;
  }

  if (langToggle && i18n.ar) {
    // if saved lang is english, apply it
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
    // escape key
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
    }, { threshold: 0.12, rootMargin: '0px 0px -30px 0px' });
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
      const isFloat = target % 1 !== 0;
      let current = 0;
      const steps = 45;
      const increment = target / steps;
      const timer = setInterval(() => {
        current = Math.min(current + increment, target);
        el.textContent = isFloat ? Math.round(current) + '%' : Math.floor(current).toLocaleString() + '+';
        if (current >= target) clearInterval(timer);
      }, 24);
      counterObs.unobserve(el);
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('[data-count]').forEach(el => counterObs.observe(el));

  // ====== COMMAND WINDOW 3D TILT ======
  if (!reduceMotion && matchMedia('(pointer:fine)').matches) {
    const cmd = document.getElementById('commandWindow');
    if (cmd) {
      cmd.addEventListener('mousemove', e => {
        const r = cmd.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width;
        const y = (e.clientY - r.top) / r.height;
        const tiltX = (y - 0.5) * 8;
        const tiltY = (x - 0.5) * -12;
        cmd.style.transform = `rotateX(${tiltX}deg) rotateY(${tiltY}deg)`;
      });
      cmd.addEventListener('mouseleave', () => { cmd.style.transform = ''; });
    }
  }

  // ====== NETWORK CANVAS (HERO & PAGE HERO) ======
  if (!reduceMotion) {
    document.querySelectorAll('.network-canvas').forEach(canvas => {
      const ctx = canvas.getContext('2d');
      let w, h, particles = [];
      const count = Math.min(55, Math.floor(window.innerWidth / 18));

      function resize() {
        const rect = canvas.parentElement.getBoundingClientRect();
        canvas.width = rect.width * devicePixelRatio;
        canvas.height = rect.height * devicePixelRatio;
        w = rect.width; h = rect.height;
        ctx.scale(devicePixelRatio, devicePixelRatio);
      }

      function createParticles() {
        particles = [];
        for (let i = 0; i < count; i++) {
          particles.push({
            x: Math.random() * w, y: Math.random() * h,
            vx: (Math.random() - 0.5) * 0.35,
            vy: (Math.random() - 0.5) * 0.35,
            r: Math.random() * 1.5 + 0.5
          });
        }
      }

      function draw() {
        ctx.clearRect(0, 0, w, h);
        particles.forEach((p, i) => {
          p.x += p.vx; p.y += p.vy;
          if (p.x < 0) p.x = w; if (p.x > w) p.x = 0;
          if (p.y < 0) p.y = h; if (p.y > h) p.y = 0;
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(73,229,255,0.35)';
          ctx.fill();
          // lines
          for (let j = i + 1; j < particles.length; j++) {
            const dx = p.x - particles[j].x, dy = p.y - particles[j].y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 120) {
              ctx.beginPath();
              ctx.moveTo(p.x, p.y);
              ctx.lineTo(particles[j].x, particles[j].y);
              ctx.strokeStyle = `rgba(117,89,255,${(1 - dist / 120) * 0.18})`;
              ctx.lineWidth = 0.6;
              ctx.stroke();
            }
          }
        });
        requestAnimationFrame(draw);
      }

      resize();
      createParticles();
      draw();
      window.addEventListener('resize', () => { resize(); createParticles(); });
    });
  }

  // ====== PROGRAM FILTER ======
  const filterToolbar = document.querySelector('.program-toolbar');
  if (filterToolbar) {
    const buttons = filterToolbar.querySelectorAll('button');
    const cards = document.querySelectorAll('.degree-card');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;
        cards.forEach(card => {
          if (filter === 'all' || card.dataset.level === filter) {
            card.classList.remove('hidden');
          } else {
            card.classList.add('hidden');
          }
        });
      });
    });
  }

  // ====== APPLICATION FORM ======
  const form = document.getElementById('applicationForm');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const btn = form.querySelector('.form-submit');
      if (btn) btn.disabled = true;
      const status = form.querySelector('.form-status');
      const dict = i18n[currentLang];
      const msg = (dict && dict.form_success) || '✓ Application submitted. We will contact you soon.';
      if (status) { status.textContent = msg; status.style.color = '#168c65'; }
      setTimeout(() => { form.reset(); if (btn) btn.disabled = false; }, 2500);
      setTimeout(() => { if (status) status.textContent = ''; }, 5000);
    });
  }

  // ====== BACK TO TOP ======
  const topBtn = document.getElementById('backToTop');
  if (topBtn) {
    const showTop = () => topBtn.classList.toggle('visible', scrollY > 500);
    addEventListener('scroll', showTop, { passive: true });
    showTop();
    topBtn.addEventListener('click', () => scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }));
  }

  // ====== FOOTER TOP BTN ======
  document.querySelector('.footer-top')?.addEventListener('click', () => scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }));

  // ====== SIGNS OF LIFE ======
  window.sfuSiteReady = true;
  document.dispatchEvent(new Event('sfu:ready'));
});

})();
