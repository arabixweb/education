// ===== Saudi Future University — Script =====
const hamburger = document.getElementById('hamburger'), nav = document.getElementById('nav');
hamburger?.addEventListener('click', () => nav?.classList.toggle('open'));
document.querySelectorAll('.nav a').forEach(a => a.addEventListener('click', () => nav?.classList.remove('open')));
const counters = document.querySelectorAll('.num');
const speed = 150;
const animateCounters = () => { counters.forEach(c => { const t=+c.getAttribute('data-target'), inc=t/speed; (function up(){ const v=+c.innerText; if(v<t){c.innerText=Math.ceil(v+inc);requestAnimationFrame(up)}else c.innerText=t })(); }); };
const observer = new IntersectionObserver((entries) => { entries.forEach(e => { if(e.isIntersecting){animateCounters();observer.disconnect()}}); }, {threshold:0.5});
const hs = document.querySelector('.hero-stats'); if(hs) observer.observe(hs);
