// أكاديمية الرياض — Script
document.addEventListener('DOMContentLoaded', () => {
  // Loading Screen
  setTimeout(() => document.getElementById('loading')?.classList.add('hide'), 800);

  // Mobile Menu
  const menuToggle = document.getElementById('menuToggle');
  const navLinks = document.getElementById('navLinks');
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
    navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));
  }

  // Language Toggle
  const langToggle = document.getElementById('langToggle');
  let currentLang = 'ar';
  if (langToggle) {
    langToggle.addEventListener('click', () => {
      currentLang = currentLang === 'ar' ? 'en' : 'ar';
      document.documentElement.lang = currentLang;
      document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
      langToggle.textContent = currentLang === 'ar' ? 'EN' : 'عربي';
      document.querySelectorAll('[data-ar]').forEach(el => {
        el.textContent = currentLang === 'ar' ? el.dataset.ar : el.dataset.en;
      });
    });
  }

  // Scroll Animation
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add('show');
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
  document.querySelectorAll('.feat-card, .prog-card, .program-full-card').forEach(el => {
    el.classList.add('fade-in');
    observer.observe(el);
  });

  // Counter Animation
  const counterObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.dataset.target);
        if (!target) return;
        let current = 0;
        const step = Math.ceil(target / 60);
        const timer = setInterval(() => {
          current += step;
          if (current >= target) { current = target; clearInterval(timer); }
          el.textContent = current.toLocaleString();
        }, 30);
        counterObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.stat-num').forEach(el => counterObserver.observe(el));

  // Navbar scroll effect
  window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
      navbar.style.background = 'rgba(13,17,23,.96)';
      navbar.style.boxShadow = '0 4px 20px rgba(0,0,0,.3)';
    } else {
      navbar.style.background = 'rgba(13,17,23,.88)';
      navbar.style.boxShadow = 'none';
    }
  });
});
