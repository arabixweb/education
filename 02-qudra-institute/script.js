// ===== Qudra Institute — Script =====

const hamburger = document.getElementById('hamburger');
const nav = document.getElementById('nav');
hamburger?.addEventListener('click', () => nav?.classList.toggle('open'));
document.querySelectorAll('.nav a').forEach(a => a.addEventListener('click', () => nav?.classList.remove('open')));

// Stats animation
const counters = document.querySelectorAll('.num');
const speed = 150;
const animateCounters = () => {
  counters.forEach(counter => {
    const target = +counter.getAttribute('data-target');
    const increment = target / speed;
    const updateCount = () => {
      const count = +counter.innerText;
      if (count < target) { counter.innerText = Math.ceil(count + increment); requestAnimationFrame(updateCount); }
      else { counter.innerText = target; }
    };
    updateCount();
  });
};
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => { if (entry.isIntersecting) { animateCounters(); observer.disconnect(); } });
}, { threshold: 0.5 });
const heroStats = document.querySelector('.hero-stats');
if (heroStats) observer.observe(heroStats);
