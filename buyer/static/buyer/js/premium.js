/* =======================================================
   PREMIUM PAGE — premium.js  v2.0
   VisionOS-inspired micro-interactions
   ======================================================= */

document.addEventListener('DOMContentLoaded', () => {

  /* ── 1. PAGE LOAD STAGGER ANIMATION ─────────────────── */
  const hero = document.querySelector('.premium-hero');
  if (hero) {
    hero.style.opacity = '0';
    hero.style.transform = 'translateY(30px)';
    requestAnimationFrame(() => {
      hero.style.transition = 'opacity 1s cubic-bezier(0.22,0.61,0.36,1), transform 1s cubic-bezier(0.22,0.61,0.36,1)';
      hero.style.opacity = '1';
      hero.style.transform = 'translateY(0)';
    });
  }

  /* ── 2. SCROLL REVEAL — fade-up elements ────────────── */
  const fadeEls = document.querySelectorAll('.fade-up');
  const revealObserver = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const delay = entry.target.style.transitionDelay || '0s';
        setTimeout(() => {
          entry.target.classList.add('visible');
        }, parseFloat(delay) * 1000);
        obs.unobserve(entry.target);
      });
    },
    { threshold: 0.1 }
  );
  fadeEls.forEach(el => revealObserver.observe(el));

  /* ── 3. FAQ ACCORDION ────────────────────────────────── */
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const answer   = btn.nextElementSibling;
      const isActive = btn.classList.contains('active');

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

  /* ── 4. BUTTON RIPPLE EFFECT ─────────────────────────── */
  document.querySelectorAll('.ripple-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const rect   = this.getBoundingClientRect();
      const circle = document.createElement('span');
      const size   = Math.max(rect.width, rect.height);
      circle.classList.add('ripple');
      circle.style.cssText = `
        width:${size}px; height:${size}px;
        left:${e.clientX - rect.left - size / 2}px;
        top:${e.clientY - rect.top  - size / 2}px;
      `;
      this.appendChild(circle);
      circle.addEventListener('animationend', () => circle.remove());
    });
  });

  /* ── 5. TITLE SHIMMER PULSE ──────────────────────────── */
  const title = document.querySelector('.premium-title');
  if (title) {
    setInterval(() => {
      title.style.opacity = '.7';
      setTimeout(() => { title.style.opacity = '1'; }, 250);
    }, 4500);
  }

  /* ── 6. DYNAMIC PARTICLE SPAWNER ────────────────────── */
  const particlesBg = document.querySelector('.particles-bg');
  const COLORS = ['var(--pm-green)', 'var(--pm-gold)', 'var(--pm-blue)'];
  let paused = false;

  function spawnParticle() {
    if (paused || !particlesBg) return;
    const p = document.createElement('span');
    p.classList.add('particle');
    const size = 2 + Math.random() * 5;
    p.style.cssText = `
      width:${size}px; height:${size}px;
      left:${Math.random() * 100}%;
      top:100%;
      background:${COLORS[Math.floor(Math.random() * COLORS.length)]};
      animation-duration:${10 + Math.random() * 14}s;
      animation-delay:0s;
      opacity:0.18;
      filter:blur(0.5px);
    `;
    particlesBg.appendChild(p);
    setTimeout(() => p.remove(), 24000);
  }

  setInterval(spawnParticle, 2800);

  document.addEventListener('visibilitychange', () => {
    paused = document.hidden;
  });

  /* ── 7. 3D MAGNETIC CARD TILT ────────────────────────── */
  document.querySelectorAll('.plan-card').forEach(card => {
    const isFeatured = card.classList.contains('plan-standard');

    card.addEventListener('mousemove', e => {
      const rect  = card.getBoundingClientRect();
      const cx    = rect.left + rect.width  / 2;
      const cy    = rect.top  + rect.height / 2;
      const dx    = (e.clientX - cx) / (rect.width  / 2);
      const dy    = (e.clientY - cy) / (rect.height / 2);
      const maxRot = isFeatured ? 7 : 9;
      const lift   = isFeatured ? -16 : -12;

      card.style.transform = `
        translateY(${lift}px)
        rotateX(${-dy * maxRot * 0.5}deg)
        rotateY(${dx * maxRot * 0.5}deg)
        scale(${isFeatured ? 1.03 : 1.02})
      `;
      card.style.transition = 'transform 0.1s ease';

      /* Glow follows cursor */
      const glowEl = card.querySelector('.card-glow');
      if (glowEl) {
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        glowEl.style.left = `${x}px`;
        glowEl.style.top  = `${y}px`;
        glowEl.style.opacity = '0.7';
      }
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
      card.style.transition = 'transform 0.5s cubic-bezier(0.34,1.56,0.64,1)';
      const glowEl = card.querySelector('.card-glow');
      if (glowEl) glowEl.style.opacity = '0';
    });

    /* Inject glow element if missing */
    if (!card.querySelector('.card-glow')) {
      const glow = document.createElement('div');
      glow.className = 'card-glow';
      card.appendChild(glow);
    }
  });

  /* ── 8. COMPARISON TABLE — column highlight ──────────── */
  const table = document.querySelector('.compare-table');
  if (table) {
    ['.col-free', '.col-standard', '.col-premium'].forEach(cls => {
      const cells = table.querySelectorAll(`th${cls}, td${cls}`);
      cells.forEach(cell => {
        cell.addEventListener('mouseenter', () => {
          cells.forEach(c => c.style.background = 'rgba(255,255,255,0.05)');
        });
        cell.addEventListener('mouseleave', () => {
          cells.forEach(c => c.style.background = '');
        });
      });
    });
  }

  /* ── 9. SMOOTH SCROLL to pricing ─────────────────────── */
  document.querySelectorAll('a[href="#pricing-plans"]').forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      document.getElementById('pricing-plans')?.scrollIntoView({ behavior: 'smooth' });
    });
  });

  /* ── 10. SCROLL-TO-TOP BUTTON ────────────────────────── */
  const scrollBtn = document.createElement('button');
  scrollBtn.className = 'scroll-top-btn';
  scrollBtn.setAttribute('aria-label', 'Scroll to top');
  scrollBtn.innerHTML = '↑';
  document.body.appendChild(scrollBtn);

  const mainContent = document.querySelector('.main-content');

  const checkScroll = () => {
    const scrollContainer = mainContent || window;
    const scrollTop = mainContent ? mainContent.scrollTop : window.scrollY;
    scrollBtn.classList.toggle('visible', scrollTop > 400);
  };

  (mainContent || window).addEventListener('scroll', checkScroll, { passive: true });

  scrollBtn.addEventListener('click', () => {
    if (mainContent) {
      mainContent.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });

  /* ── 11. FEATURE CARD — stagger entrance ────────────── */
  const featureCards = document.querySelectorAll('.feature-card');
  featureCards.forEach((card, i) => {
    if (!card.style.transitionDelay) {
      card.style.transitionDelay = `${i * 0.08}s`;
    }
  });

  /* ── 12. PLAN BUTTON — press depth effect ───────────── */
  document.querySelectorAll('.plan-btn:not(.plan-btn-free)').forEach(btn => {
    btn.addEventListener('mousedown', () => {
      btn.style.transform = 'translateY(1px) scale(0.99)';
    });
    btn.addEventListener('mouseup', () => {
      btn.style.transform = '';
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = '';
    });
  });

  /* ── 13. TESTIMONIAL CARD — slow drift ───────────────── */
  document.querySelectorAll('.testimonial-card').forEach((card, i) => {
    card.style.animationDelay = `${i * 0.3}s`;
  });

  /* ── 14. KEYBOARD NAVIGATION FOCUS RINGS ─────────────── */
  document.addEventListener('keydown', e => {
    if (e.key === 'Tab') {
      document.body.classList.add('keyboard-nav');
    }
  });
  document.addEventListener('mousedown', () => {
    document.body.classList.remove('keyboard-nav');
  });

  /* ── 15. SECTION HEADINGS — number counter on enter ──── */
  const planAmounts = document.querySelectorAll('.plan-amount');
  const counterObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el     = entry.target;
      const target = parseInt(el.textContent, 10);
      if (isNaN(target) || target === 0) return;
      let current  = 0;
      const step   = Math.ceil(target / 30);
      const tick   = () => {
        current = Math.min(current + step, target);
        el.textContent = current;
        if (current < target) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      counterObserver.unobserve(el);
    });
  }, { threshold: 0.5 });

  planAmounts.forEach(el => counterObserver.observe(el));

});
