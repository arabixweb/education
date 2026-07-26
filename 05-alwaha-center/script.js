// ===== Al-Waha Center — Script =====
const hamburger = document.getElementById('hamburger'), nav = document.getElementById('nav');
hamburger?.addEventListener('click', () => nav?.classList.toggle('open'));
document.querySelectorAll('.nav a').forEach(a => a.addEventListener('click', () => nav?.classList.remove('open')));
