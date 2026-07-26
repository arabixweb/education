(function() {
  'use strict';
  var LS = 'aracademy_lang';
  var current = localStorage.getItem(LS) || 'ar';
  document.documentElement.lang = current;
  document.documentElement.dir = current === 'ar' ? 'rtl' : 'ltr';

  function apply(lang) {
    var dict = window.__i18n && window.__i18n[lang];
    if (!dict) return;
    elsToArray(document.querySelectorAll('[data-i18n]')).
      sort(depthSort).
      forEach(function(el) {
        var key = el.getAttribute('data-i18n');
        var val = dict[key];
        if (!val) return;
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') return;
        if (el.tagName === 'OPTION') { el.textContent = val.replace(/<[^>]+>/g,''); return; }
        if (el.hasAttribute('data-i18n-html') || val.indexOf('<') !== -1) { el.innerHTML = val; return; }
        el.textContent = val;
      });
    function depthSort(a,b) {
      function depth(n) { var d=0; while(n.parentNode) { d++; n=n.parentNode; } return d; }
      return depth(b) - depth(a);
    }
    function elsToArray(nl) { var a=[]; for(var i=0;i<nl.length;i++) a.push(nl[i]); return a; }
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    var btn = document.getElementById('langToggle');
    if (btn) btn.textContent = lang === 'ar' ? 'EN' : '\u0639\u0631\u0628\u064A';
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
        m.textContent = (dict && dict.form_success) || (current === 'ar' ? '\u2713 \u062A\u0645 \u0627\u0644\u0625\u0631\u0633\u0627\u0644!' : '\u2713 Submitted!');
        f.appendChild(m);
        setTimeout(function() { f.reset(); if (btn) btn.disabled = false; }, 2000);
        setTimeout(function() { m.remove(); }, 4500);
      });
    });

  /* ANIMATIONS */
  var revealObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (e.isIntersecting) { e.target.classList.add('show'); }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(function(el) { revealObserver.observe(el); });

  /* Navbar scroll effect */
  var nbar = document.querySelector('.navbar');
  if (nbar) {
    window.addEventListener('scroll', function() {
      nbar.classList.toggle('scrolled', window.scrollY > 80);
    });
  }

  /* Hero-visual parallax on scroll */
  var hv = document.querySelector('.hero-visual');
  if (hv) {
    window.addEventListener('scroll', function() {
      var y = window.scrollY;
      if (y < window.innerHeight) { hv.style.transform = 'translateY(' + (y * 0.03) + 'px)'; }
    });
  }
  });
})();
