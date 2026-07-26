// مركز الواحة — Script
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

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('show'); });
  }, { threshold: 0.1 });
  document.querySelectorAll('.waha-card, .prog-waha-card, .why-card').forEach(el => {
    el.classList.add('fade-in');
    observer.observe(el);
  });
});
