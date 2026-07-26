// معهد قدرة — Script
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => document.getElementById('loading')?.classList.add('hide'), 700);

  const menuToggle = document.getElementById('menuToggle');
  const navLinks = document.getElementById('navLinks');
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
    navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));
  }

  const langToggle = document.getElementById('langToggle');
  let currentLang = 'ar';
  if (langToggle) {
    langToggle.addEventListener('click', () => {
      currentLang = currentLang === 'ar' ? 'en' : 'ar';
      document.documentElement.lang = currentLang;
      document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
      langToggle.textContent = currentLang === 'ar' ? 'EN' : 'عربي';
    });
  }

  // Scroll animations
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('show'); });
  }, { threshold: 0.1 });
  document.querySelectorAll('.feat-card, .course-card, .course-full-card, .testimonial-card').forEach(el => {
    el.classList.add('fade-in');
    observer.observe(el);
  });

  // Counters
  const counterObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.dataset.target);
        if (!target) return;
        let current = 0;
        const step = Math.ceil(target / 50);
        const timer = setInterval(() => {
          current += step;
          if (current >= target) { current = target; clearInterval(timer); }
          el.textContent = current.toLocaleString() + (target === 92 ? '%' : '');
        }, 30);
        counterObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.stat-num').forEach(el => counterObserver.observe(el));

  // Navbar scroll
  window.addEventListener('scroll', () => {
    const n = document.querySelector('.navbar');
    if (window.scrollY > 80) {
      n.style.background = 'rgba(8,14,26,.97)';
      n.style.boxShadow = '0 4px 20px rgba(0,0,0,.3)';
    } else {
      n.style.background = 'rgba(8,14,26,.92)';
      n.style.boxShadow = 'none';
    }
  });
});
