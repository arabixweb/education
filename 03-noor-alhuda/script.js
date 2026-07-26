// Noor Alhuda — explicit bilingual i18n and progressive premium interactions
(() => {
  'use strict';
  document.addEventListener('DOMContentLoaded', () => {
    const root = document.documentElement;
    const dict = window.__i18n || { ar: {}, en: {} };
    const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let lang = localStorage.getItem('edu_lang') === 'en' ? 'en' : 'ar';
    const get = (l, k) => dict[l] && dict[l][k];
    const toggle = document.getElementById('langToggle');

    function setLanguage(next) {
      if (!dict[next]) return;
      lang = next; root.lang = next; root.dir = next === 'ar' ? 'rtl' : 'ltr'; root.dataset.lang = next;
      document.querySelectorAll('[data-i18n]').forEach(el => { const v = get(next, el.dataset.i18n); if (typeof v === 'string') el.textContent = v; });
      document.querySelectorAll('[data-i18n-ph]').forEach(el => { const v = get(next, el.dataset.i18nPh); if (typeof v === 'string') el.placeholder = v; });
      document.querySelectorAll('[data-i18n-alt]').forEach(el => { const v = get(next, el.dataset.i18nAlt); if (typeof v === 'string') el.alt = v; });
      const titleKey = root.dataset.titleI18n; if (titleKey && get(next, titleKey)) document.title = get(next, titleKey);
      document.querySelectorAll('[data-logo-letter]').forEach(el => { el.textContent = next === 'ar' ? 'ن' : 'N'; });
      document.querySelectorAll('.fa-arrow-left,.fa-arrow-right').forEach(icon => { icon.classList.toggle('fa-arrow-left', next === 'ar'); icon.classList.toggle('fa-arrow-right', next === 'en'); });
      if (toggle) { const label = toggle.querySelector('span'); if (label) label.textContent = next === 'ar' ? 'EN' : 'عربي'; toggle.setAttribute('aria-label', next === 'ar' ? 'Switch to English' : 'التبديل إلى العربية'); }
      localStorage.setItem('edu_lang', next);
      dispatchEvent(new CustomEvent('noor:languagechange', { detail: { lang: next } }));
    }
    setLanguage(lang); toggle?.addEventListener('click', () => setLanguage(lang === 'ar' ? 'en' : 'ar'));

    const loader = document.getElementById('loading');
    const release = () => loader?.classList.add('hide');
    addEventListener('load', release, { once: true }); setTimeout(release, 900);

    const menu = document.getElementById('navLinks'), menuBtn = document.getElementById('menuToggle'), backdrop = document.getElementById('menuBackdrop');
    function setMenu(open) { menu?.classList.toggle('open', open); menuBtn?.classList.toggle('open', open); backdrop?.classList.toggle('open', open); menuBtn?.setAttribute('aria-expanded', String(open)); document.body.classList.toggle('menu-open', open); }
    if (menu && menuBtn) { menuBtn.setAttribute('aria-expanded', 'false'); menuBtn.addEventListener('click', () => setMenu(!menu.classList.contains('open'))); backdrop?.addEventListener('click', () => setMenu(false)); menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false))); document.addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); }); }
    const current = location.pathname.split('/').pop() || 'index.html'; menu?.querySelectorAll('a:not(.nav-enroll)').forEach(a => a.classList.toggle('active', a.getAttribute('href') === current));

    const navbar = document.querySelector('.navbar'); const scrollHeader = () => navbar?.classList.toggle('scrolled', scrollY > 45); scrollHeader(); addEventListener('scroll', scrollHeader, { passive: true });

    const reveals = document.querySelectorAll('.reveal');
    if (!reduceMotion && 'IntersectionObserver' in window) { const obs = new IntersectionObserver(entries => entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('show'); obs.unobserve(e.target); } }), { threshold: .08, rootMargin: '0px 0px -30px' }); reveals.forEach((el, i) => { el.style.setProperty('--delay', `${(i % 4) * 75}ms`); obs.observe(el); }); } else reveals.forEach(el => el.classList.add('show'));

    function animateCounter(el) { if (el.dataset.animated) return; el.dataset.animated = '1'; const target = parseInt(el.dataset.target || '0', 10), start = performance.now(), duration = 1500; const tick = now => { const p = Math.min((now - start) / duration, 1), eased = 1 - Math.pow(1 - p, 3); el.textContent = Math.round(target * eased).toLocaleString(lang === 'ar' ? 'ar-SA' : 'en-US') + (target >= 1000 ? '+' : ''); if (p < 1) requestAnimationFrame(tick); }; requestAnimationFrame(tick); }
    const counters = document.querySelectorAll('[data-target]'); if (!reduceMotion && 'IntersectionObserver' in window) { const co = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { animateCounter(e.target); co.unobserve(e.target); } }), { threshold: .45 }); counters.forEach(c => co.observe(c)); } else counters.forEach(animateCounter);

    // A softly moving geometric constellation unique to Noor Alhuda's hero.
    const canvas = document.getElementById('geometryCanvas');
    if (canvas && !reduceMotion) {
      const ctx = canvas.getContext('2d'); let w = 0, h = 0, ratio = 1, raf = 0, points = []; const pointer = { x: -999, y: -999 };
      function resize() { const r = canvas.getBoundingClientRect(); ratio = Math.min(devicePixelRatio || 1, 1.5); w = r.width; h = r.height; canvas.width = w * ratio; canvas.height = h * ratio; ctx.setTransform(ratio, 0, 0, ratio, 0, 0); const n = Math.max(26, Math.min(52, Math.round(w / 28))); points = Array.from({ length: n }, (_, i) => ({ x: Math.random() * w, y: Math.random() * h, baseX: 0, baseY: 0, radius: 35 + Math.random() * 45, speed: .00009 + Math.random() * .00012, phase: Math.random() * Math.PI * 2, type: i % 5 })); }
      function draw(t) { ctx.clearRect(0, 0, w, h); points.forEach((p, i) => { p.x += Math.cos(t * p.speed + p.phase) * .13; p.y += Math.sin(t * p.speed + p.phase) * .1; const pd = Math.hypot(pointer.x - p.x, pointer.y - p.y); if (pd < 150) { p.x -= (pointer.x - p.x) * .0007; p.y -= (pointer.y - p.y) * .0007; } for (let j = i + 1; j < points.length; j++) { const q = points[j], d = Math.hypot(q.x - p.x, q.y - p.y); if (d < 145) { ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.strokeStyle = `rgba(11,73,56,${(1-d/145)*.085})`; ctx.lineWidth = .7; ctx.stroke(); } } ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(t * .00004 + p.phase); ctx.beginPath(); const sides = p.type === 0 ? 8 : 4, size = p.type === 0 ? 3.5 : 1.7; for (let k=0;k<sides;k++){ const a=Math.PI*2*k/sides-Math.PI/2, x=Math.cos(a)*size,y=Math.sin(a)*size;k?ctx.lineTo(x,y):ctx.moveTo(x,y); }ctx.closePath();ctx.fillStyle=p.type===0?'rgba(200,155,74,.45)':'rgba(11,73,56,.28)';ctx.fill();ctx.restore(); }); raf=requestAnimationFrame(draw); }
      resize(); raf=requestAnimationFrame(draw); addEventListener('resize', resize, { passive: true }); canvas.closest('.hero')?.addEventListener('pointermove', e => { const r=canvas.getBoundingClientRect();pointer.x=e.clientX-r.left;pointer.y=e.clientY-r.top; }); canvas.closest('.hero')?.addEventListener('pointerleave',()=>{pointer.x=-999;pointer.y=-999}); document.addEventListener('visibilitychange',()=>{if(document.hidden)cancelAnimationFrame(raf);else raf=requestAnimationFrame(draw)});
    }

    // subtle image depth
    const visual = document.querySelector('.hero-visual'); if (visual && !reduceMotion && matchMedia('(pointer:fine)').matches) { const arch=visual.querySelector('.arch-frame'); visual.addEventListener('pointermove',e=>{const r=visual.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;arch.style.transform=`perspective(1100px) rotateY(${x*4}deg) rotateX(${-y*4}deg)`});visual.addEventListener('pointerleave',()=>arch.style.transform=''); }

    document.querySelectorAll('.program-filter button').forEach(btn => btn.addEventListener('click', () => { btn.parentElement.querySelectorAll('button').forEach(b => b.classList.remove('active')); btn.classList.add('active'); }));
    document.querySelectorAll('form').forEach(form => form.addEventListener('submit', e => { e.preventDefault(); const status=form.querySelector('.form-status'); if(status) status.textContent=lang==='ar'?'تم استلام طلبك بنجاح. سنتواصل معك قريباً بإذن الله.':'Your request has been received. We will contact you shortly.'; form.reset(); }));
    // Stagger common card collections independently so each section feels intentional.
    document.querySelectorAll('.pillars-grid,.values-grid,.courses-grid,.program-showcase,.steps-line').forEach(group => {
      [...group.children].forEach((card, index) => card.style.setProperty('--card-index', index));
    });

    // Gentle magnetic lift on primary controls (fine pointers only).
    if (!reduceMotion && matchMedia('(pointer:fine)').matches) {
      document.querySelectorAll('.btn,.portal-cta,.nav-enroll').forEach(el => {
        el.addEventListener('pointermove', e => { const r=el.getBoundingClientRect(),x=(e.clientX-r.left-r.width/2)*.07,y=(e.clientY-r.top-r.height/2)*.1;el.style.transform=`translate(${x}px,${y}px) translateY(-2px)`; });
        el.addEventListener('pointerleave', () => el.style.transform='');
      });
    }

    // Footer has its own visible back-to-top control in addition to the floating helper.
    document.querySelector('.footer-to-top')?.addEventListener('click', () => scrollTo({top:0,behavior:reduceMotion?'auto':'smooth'}));

    const top=document.createElement('button');top.id='backToTop';top.innerHTML='<i class="fas fa-arrow-up"></i>';top.setAttribute('aria-label','Back to top');document.body.appendChild(top);const showTop=()=>top.classList.toggle('visible',scrollY>550);addEventListener('scroll',showTop,{passive:true});showTop();top.addEventListener('click',()=>scrollTo({top:0,behavior:reduceMotion?'auto':'smooth'}));
    window.noorSiteReady=true; dispatchEvent(new Event('noor:ready'));
  });
})();
