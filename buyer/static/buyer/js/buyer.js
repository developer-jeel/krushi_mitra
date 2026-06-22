/* buyer.js — UI interactions only, no business logic */

// ── Language Modal ──
const langModal   = document.getElementById('langModal');
const langTriggers = document.querySelectorAll('[data-lang-trigger]');
const langClose   = document.getElementById('langClose');

langTriggers.forEach(t => {
  t.addEventListener('click', () => langModal?.classList.add('open'));
});

langClose?.addEventListener('click', () => langModal?.classList.remove('open'));

langModal?.addEventListener('click', e => {
  if (e.target === langModal) langModal.classList.remove('open');
});

// ── Language item selection ──
document.querySelectorAll('.lang-item').forEach(item => {
  item.addEventListener('click', () => {
    document.querySelectorAll('.lang-item').forEach(i => i.classList.remove('selected'));
    item.classList.add('selected');
  });
});

// ── Active nav item highlight ──
const currentPage = window.location.pathname.split('/').pop();
document.querySelectorAll('.nav-item').forEach(link => {
  if (link.getAttribute('href') === currentPage) {
    link.classList.add('active');
  }
});
