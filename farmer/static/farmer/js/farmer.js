// farmer.js
document.addEventListener('DOMContentLoaded', () => {

  /* ══════════════════════════════════════════════════════════════
     THEME TOGGLE — Dark / Light
     ══════════════════════════════════════════════════════════════ */

  // Apply saved theme immediately (before paint)
  const savedTheme = localStorage.getItem('km-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);

  function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';

    // Add transitioning class for smooth animation
    html.classList.add('theme-transitioning');

    // Apply new theme
    html.setAttribute('data-theme', next);
    localStorage.setItem('km-theme', next);

    // Update all toggle buttons on the page
    updateToggleButtons(next);

    // Remove transitioning class after animation completes
    setTimeout(() => html.classList.remove('theme-transitioning'), 450);
  }

  function updateToggleButtons(theme) {
    // Update sidebar toggle
    document.querySelectorAll('.theme-toggle').forEach(btn => {
      const icon = btn.querySelector('.theme-toggle-icon');
      const label = btn.querySelector('.theme-toggle-label');
      const badge = btn.querySelector('.theme-toggle-badge');
      if (icon) icon.textContent = theme === 'dark' ? '🌙' : '☀️';
      if (label) label.textContent = theme === 'dark' ? 'Dark Mode' : 'Light Mode';
      if (badge) badge.textContent = theme === 'dark' ? 'ON' : 'ON';
    });

    // Update floating toggle
    document.querySelectorAll('.theme-toggle-floating').forEach(btn => {
      btn.textContent = theme === 'dark' ? '☀️' : '🌙';
      btn.title = theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
    });
  }

  // Auto-inject toggle button into sidebar
  const sidebarBottom = document.querySelector('.sidebar-bottom');
  if (sidebarBottom) {
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'theme-toggle';
    toggleBtn.id = 'themeToggle';
    toggleBtn.innerHTML = `
      <span class="theme-toggle-icon">${savedTheme === 'dark' ? '🌙' : '☀️'}</span>
      <span class="theme-toggle-label">${savedTheme === 'dark' ? 'Dark Mode' : 'Light Mode'}</span>
      <span class="theme-toggle-badge">ON</span>
    `;
    toggleBtn.addEventListener('click', toggleTheme);
    sidebarBottom.insertBefore(toggleBtn, sidebarBottom.firstChild);
  } else {
    // No sidebar (standalone pages like tool_price) — add floating toggle
    const floatingBtn = document.createElement('button');
    floatingBtn.className = 'theme-toggle-floating';
    floatingBtn.id = 'themeToggleFloating';
    floatingBtn.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
    floatingBtn.title = savedTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
    floatingBtn.addEventListener('click', toggleTheme);
    document.body.appendChild(floatingBtn);
  }

  /* ══════════════════════════════════════════════════════════════
     EXISTING FUNCTIONALITY
     ══════════════════════════════════════════════════════════════ */

  /* ── Active nav highlight ── */
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      navItems.forEach(n => n.classList.remove('active'));
      item.classList.add('active');
    });
  });

  /* ── Sidebar collapse on mobile ── */
  const menuBtn = document.getElementById('menuToggle');
  const sidebar = document.querySelector('.sidebar');
  if (menuBtn && sidebar) {
    menuBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open-mobile');
      let overlay = document.querySelector('.sidebar-overlay');
      if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        document.body.appendChild(overlay);
        overlay.addEventListener('click', () => {
          sidebar.classList.remove('open-mobile');
          overlay.classList.remove('active');
        });
      }
      setTimeout(() => {
        overlay.classList.toggle('active', sidebar.classList.contains('open-mobile'));
      }, 10);
    });
  }

  /* ── Toggle switches (profile page) ── */
  document.querySelectorAll('.toggle-switch').forEach(sw => {
    sw.addEventListener('click', () => sw.classList.toggle('on'));
  });

  /* ── Settings tabs (profile page) ── */
  document.querySelectorAll('.settings-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.settings-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
    });
  });

  /* ── Tab buttons (tools/blogs pages) ── */
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
      btn.classList.add('active');
    });
  });

  /* ── Rating stars (blogs page) ── */
  const stars = document.querySelectorAll('.rating-star');
  stars.forEach((star, i) => {
    star.addEventListener('mouseenter', () => {
      stars.forEach((s, j) => s.classList.toggle('active', j <= i));
    });
    star.addEventListener('click', () => {
      stars.forEach((s, j) => s.classList.toggle('active', j <= i));
    });
  });

});

/* ── Apply theme before DOM ready (prevents flash) ── */
(function () {
  const t = localStorage.getItem('km-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', t);
})();
