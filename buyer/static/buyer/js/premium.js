/* premium.js — Krushi Mitra Buyer Panel */

document.addEventListener('DOMContentLoaded', () => {

  /* ────────────────────────────────────────────────────
   * 1. SCROLL REVEAL — fade-up elements
   * ──────────────────────────────────────────────────── */
  const fadeEls = document.querySelectorAll('.fade-up');
  const revealObserver = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry, i) => {
        if (!entry.isIntersecting) return;
        // stagger children that share a parent (plan cards, feature cards)
        const delay = entry.target.style.transitionDelay || '0s';
        setTimeout(() => {
          entry.target.classList.add('visible');
        }, parseFloat(delay) * 1000);
        obs.unobserve(entry.target);
      });
    },
    { threshold: 0.12 }
  );
  fadeEls.forEach(el => revealObserver.observe(el));


  /* ────────────────────────────────────────────────────
   * 2. FAQ ACCORDION
   * ──────────────────────────────────────────────────── */
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const answer   = btn.nextElementSibling;
      const isActive = btn.classList.contains('active');

      // close all
      document.querySelectorAll('.faq-question.active').forEach(other => {
        if (other !== btn) {
          other.classList.remove('active');
          other.nextElementSibling.style.maxHeight = null;
        }
      });

      btn.classList.toggle('active', !isActive);
      answer.style.maxHeight = isActive ? null : answer.scrollHeight + 'px';
    });
  });


  /* ────────────────────────────────────────────────────
   * 3. BUTTON RIPPLE EFFECT
   * ──────────────────────────────────────────────────── */
  document.querySelectorAll('.ripple-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const rect   = this.getBoundingClientRect();
      const circle = document.createElement('span');
      const size   = Math.max(rect.width, rect.height);
      circle.classList.add('ripple');
      circle.style.cssText = `
        width: ${size}px; height: ${size}px;
        left: ${e.clientX - rect.left - size / 2}px;
        top:  ${e.clientY - rect.top  - size / 2}px;
      `;
      this.appendChild(circle);
      circle.addEventListener('animationend', () => circle.remove());
    });
  });


  /* ────────────────────────────────────────────────────
   * 4. HERO TITLE SHIMMER (subtle pulse every ~4 s)
   * ──────────────────────────────────────────────────── */
  const title = document.querySelector('.premium-title');
  if (title) {
    setInterval(() => {
      title.style.opacity = '.75';
      setTimeout(() => { title.style.opacity = '1'; }, 220);
    }, 4200);
  }


  /* ────────────────────────────────────────────────────
   * 5. FLOATING PARTICLE SPAWNER (dynamic extras)
   *    Adds occasional random micro-particles on scroll
   * ──────────────────────────────────────────────────── */
  const particlesBg = document.querySelector('.particles-bg');
  const COLORS = ['var(--pm-green)', 'var(--pm-gold)', 'var(--pm-blue)'];
  let particleSpawnPaused = false;

  function spawnParticle() {
    if (particleSpawnPaused || !particlesBg) return;
    const p = document.createElement('span');
    p.classList.add('particle');
    const size = 3 + Math.random() * 6;
    p.style.cssText = `
      width: ${size}px; height: ${size}px;
      left: ${Math.random() * 100}%;
      top: 100%;
      background: ${COLORS[Math.floor(Math.random() * COLORS.length)]};
      animation-duration: ${10 + Math.random() * 12}s;
      animation-delay: 0s;
      opacity: 0.2;
    `;
    particlesBg.appendChild(p);
    setTimeout(() => p.remove(), 22000);
  }
  // spawn one particle every 2.5 s
  setInterval(spawnParticle, 2500);

  // pause spawning when tab is hidden to save resources
  document.addEventListener('visibilitychange', () => {
    particleSpawnPaused = document.hidden;
  });


  /* ────────────────────────────────────────────────────
   * 6. PLAN CARD — hover lift with glass reflection
   * ──────────────────────────────────────────────────── */
  document.querySelectorAll('.plan-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width  - 0.5) * 16;
      const y = ((e.clientY - rect.top)  / rect.height - 0.5) * 16;
      card.style.transform = `translateY(-10px) rotateX(${-y * 0.4}deg) rotateY(${x * 0.4}deg) scale(1.02)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });


  /* ────────────────────────────────────────────────────
   * 7. COMPARISON TABLE — highlight column on hover
   * ──────────────────────────────────────────────────── */
  const table = document.querySelector('.compare-table');
  if (table) {
    const colMaps = ['.col-free', '.col-standard', '.col-premium'];
    colMaps.forEach(cls => {
      const cells = table.querySelectorAll(`th${cls}, td${cls}`);
      cells.forEach(cell => {
        cell.addEventListener('mouseenter', () => {
          cells.forEach(c => c.style.background = 'rgba(255,255,255,.05)');
        });
        cell.addEventListener('mouseleave', () => {
          cells.forEach(c => c.style.background = '');
        });
      });
    });
  }


  /* ────────────────────────────────────────────────────
   * 8. SMOOTH SCROLL to pricing when "Upgrade" clicked in navbar
   * ──────────────────────────────────────────────────── */
  document.querySelectorAll('a[href="#pricing-plans"]').forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      document.getElementById('pricing-plans')?.scrollIntoView({ behavior: 'smooth' });
    });
  });

});
