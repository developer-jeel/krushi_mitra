/* ══════════════════════════════════════════════════════════════
   KRUSHI MITRA — PREMIUM INTERACTION ENGINE v3.0
   Features: Particles · Mouse Glow · Scroll Reveals · Counters
             Ripple · Magnetic Buttons · Topbar Scroll · Toasts
   ══════════════════════════════════════════════════════════════ */

'use strict';

(function () {

  /* ─────────────────────────────────────────────────────────
     UTILITY: runs after DOM is ready
  ───────────────────────────────────────────────────────── */
  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  /* ─────────────────────────────────────────────────────────
     1. FLOATING PARTICLE CANVAS
  ───────────────────────────────────────────────────────── */
  function initParticles() {
    const canvas = document.createElement('canvas');
    canvas.id = 'particle-canvas';
    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    let W = window.innerWidth;
    let H = window.innerHeight;
    canvas.width = W;
    canvas.height = H;

    const particles = [];
    const COUNT = Math.min(22, Math.floor(W / 80));

    // Farming shapes: leaf, seed, droplet, star
    const shapes = ['leaf', 'seed', 'circle', 'star'];

    function randBetween(a, b) { return a + Math.random() * (b - a); }

    function createParticle() {
      return {
        x:       randBetween(0, W),
        y:       randBetween(H * 0.1, H),
        vx:      randBetween(-0.18, 0.18),
        vy:      randBetween(-0.55, -0.18),
        size:    randBetween(3, 9),
        opacity: randBetween(0.15, 0.45),
        shape:   shapes[Math.floor(Math.random() * shapes.length)],
        hue:     Math.random() > 0.75 ? 45 : 145, // gold or green
        rot:     randBetween(0, Math.PI * 2),
        rotV:    randBetween(-0.008, 0.008),
        pulse:   randBetween(0, Math.PI * 2),
        pulseSpeed: randBetween(0.01, 0.025),
      };
    }

    for (let i = 0; i < COUNT; i++) particles.push(createParticle());

    function drawLeaf(ctx, x, y, size, rot) {
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(rot);
      ctx.beginPath();
      ctx.moveTo(0, -size);
      ctx.bezierCurveTo(size * 0.8, -size * 0.5, size * 0.8, size * 0.5, 0, size);
      ctx.bezierCurveTo(-size * 0.8, size * 0.5, -size * 0.8, -size * 0.5, 0, -size);
      ctx.fill();
      ctx.restore();
    }

    function drawStar(ctx, x, y, size, rot) {
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(rot);
      ctx.beginPath();
      for (let i = 0; i < 5; i++) {
        const angle = (i * 4 * Math.PI) / 5 - Math.PI / 2;
        const r = i === 0 ? size : size * 0.4;
        ctx.lineTo(Math.cos(angle) * size, Math.sin(angle) * size);
        const innerAngle = angle + (2 * Math.PI) / 10;
        ctx.lineTo(Math.cos(innerAngle) * size * 0.42, Math.sin(innerAngle) * size * 0.42);
      }
      ctx.closePath();
      ctx.fill();
      ctx.restore();
    }

    function tick() {
      ctx.clearRect(0, 0, W, H);
      particles.forEach(p => {
        // Update
        p.x   += p.vx;
        p.y   += p.vy;
        p.rot += p.rotV;
        p.pulse += p.pulseSpeed;
        const pulsedOpacity = p.opacity * (0.7 + 0.3 * Math.sin(p.pulse));

        // Reset if out of bounds
        if (p.y < -30 || p.x < -30 || p.x > W + 30) {
          p.x = randBetween(0, W);
          p.y = H + 20;
        }

        // Draw
        ctx.globalAlpha = pulsedOpacity;
        ctx.fillStyle = p.hue === 45
          ? `hsla(45, 90%, 60%, ${pulsedOpacity})`
          : `hsla(145, 70%, 55%, ${pulsedOpacity})`;

        if (p.shape === 'leaf') {
          drawLeaf(ctx, p.x, p.y, p.size, p.rot);
        } else if (p.shape === 'star') {
          drawStar(ctx, p.x, p.y, p.size * 0.7, p.rot);
        } else if (p.shape === 'seed') {
          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate(p.rot);
          ctx.beginPath();
          ctx.ellipse(0, 0, p.size * 0.35, p.size, 0, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        } else {
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size * 0.5, 0, Math.PI * 2);
          ctx.fill();
        }
        ctx.globalAlpha = 1;
      });

      requestAnimationFrame(tick);
    }

    tick();

    window.addEventListener('resize', () => {
      W = window.innerWidth;
      H = window.innerHeight;
      canvas.width = W;
      canvas.height = H;
    });
  }

  /* ─────────────────────────────────────────────────────────
     2. MOUSE-FOLLOW GLOW EFFECT
  ───────────────────────────────────────────────────────── */
  function initMouseGlow() {
    const isTouchDevice = window.matchMedia('(hover: none)').matches;
    if (isTouchDevice) return;

    const glow = document.createElement('div');
    glow.id = 'mouse-glow';
    document.body.appendChild(glow);

    let targetX = -400, targetY = -400;
    let currentX = -400, currentY = -400;

    document.addEventListener('mousemove', e => {
      targetX = e.clientX;
      targetY = e.clientY;
    });

    document.addEventListener('mouseleave', () => {
      targetX = -400;
      targetY = -400;
    });

    function animateGlow() {
      // Smooth lerp follow
      currentX += (targetX - currentX) * 0.10;
      currentY += (targetY - currentY) * 0.10;
      glow.style.left = currentX + 'px';
      glow.style.top  = currentY + 'px';
      requestAnimationFrame(animateGlow);
    }
    animateGlow();
  }

  /* ─────────────────────────────────────────────────────────
     3. SCROLL-TRIGGERED REVEAL ANIMATIONS
  ───────────────────────────────────────────────────────── */
  function initScrollReveal() {
    const targets = document.querySelectorAll(
      '.stat-card, .product-card, .blog-card, .review-card, ' +
      '.profile-stat-card, .profile-section, .order-form-card, ' +
      '.write-card, .table-wrapper, .section-header, .section-title, ' +
      '.stat-tile, .b-card, .form-card, .tips-card'
    );

    if (!targets.length) return;

    // Add base reveal class
    targets.forEach((el, i) => {
      el.classList.add('reveal');
      // Add slight scale-in variant
      if (el.classList.contains('stat-card') || el.classList.contains('profile-stat-card')) {
        el.classList.add('scale-in');
      }
      // Stagger siblings
      const parent = el.parentElement;
      const siblings = parent ? [...parent.children].filter(c => c.classList.contains(el.classList[0])) : [];
      const sibIdx = siblings.indexOf(el);
      if (sibIdx > 0 && sibIdx <= 7) {
        el.style.transitionDelay = (sibIdx * 0.07) + 's';
      }
    });

    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
          // Clean up: stop observing after reveal
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });

    targets.forEach(el => io.observe(el));
  }

  /* ─────────────────────────────────────────────────────────
     4. ANIMATED STAT COUNTERS
  ───────────────────────────────────────────────────────── */
  function initCounters() {
    const statValues = document.querySelectorAll('.stat-value, .profile-stat-val, .stat-tile-val');

    if (!statValues.length) return;

    function parseValue(text) {
      // Extract numeric content from strings like "₹48,250", "4.8★", "18", "₹48K"
      const clean = text.replace(/[₹,★\s]/g, '');
      const hasK = clean.endsWith('K');
      const num = parseFloat(clean.replace('K', ''));
      return { value: isNaN(num) ? null : num, hasK, original: text };
    }

    function formatValue(num, original) {
      if (original.includes('₹')) {
        if (original.includes('K')) return '₹' + Math.round(num) + 'K';
        // format with commas
        return '₹' + Math.round(num).toLocaleString('en-IN');
      }
      if (original.includes('★')) return num.toFixed(1) + '★';
      if (Number.isInteger(num) || num > 10) return Math.round(num).toString();
      return num.toFixed(1);
    }

    function animateCounter(el, from, to, duration, original) {
      const startTime = performance.now();
      function step(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // Ease-out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = from + (to - from) * eased;
        el.textContent = formatValue(current, original);
        if (progress < 1) requestAnimationFrame(step);
        else el.textContent = formatValue(to, original);
      }
      requestAnimationFrame(step);
    }

    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        if (el.dataset.counted) return;
        el.dataset.counted = 'true';

        const parsed = parseValue(el.textContent.trim());
        if (parsed.value === null) return;

        const val = parsed.hasK ? parsed.value : parsed.value;
        animateCounter(el, 0, val, 1400, parsed.original);
        io.unobserve(el);
      });
    }, { threshold: 0.5 });

    statValues.forEach(el => io.observe(el));
  }

  /* ─────────────────────────────────────────────────────────
     5. RIPPLE CLICK EFFECT ON ALL BUTTONS
  ───────────────────────────────────────────────────────── */
  function initRipple() {
    document.addEventListener('click', function (e) {
      const btn = e.target.closest('.btn, .nav-item, .tab-btn, .settings-tab');
      if (!btn) return;

      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const ripple = document.createElement('span');
      ripple.style.cssText = `
        position: absolute;
        left: ${x}px;
        top:  ${y}px;
        width: 6px;
        height: 6px;
        background: rgba(255,255,255,0.35);
        border-radius: 50%;
        transform: translate(-50%, -50%) scale(0);
        animation: rippleExpand 0.55s cubic-bezier(0, 0, 0.2, 1) forwards;
        pointer-events: none;
        z-index: 999;
      `;

      const prevPos = window.getComputedStyle(btn).position;
      if (prevPos === 'static') btn.style.position = 'relative';
      btn.style.overflow = 'hidden';
      btn.appendChild(ripple);

      setTimeout(() => ripple.remove(), 600);
    });
  }

  /* ─────────────────────────────────────────────────────────
     6. MAGNETIC HOVER BUTTONS
  ───────────────────────────────────────────────────────── */
  function initMagneticButtons() {
    const isTouchDevice = window.matchMedia('(hover: none)').matches;
    if (isTouchDevice) return;

    const magnetics = document.querySelectorAll('.btn-primary, .btn-amber');

    magnetics.forEach(btn => {
      btn.addEventListener('mousemove', function (e) {
        const rect = this.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;
        const dx = (e.clientX - cx) * 0.25;
        const dy = (e.clientY - cy) * 0.25;
        this.style.transform = `translate(${dx}px, ${dy}px) translateY(-2px)`;
      });

      btn.addEventListener('mouseleave', function () {
        this.style.transform = '';
        this.style.transition = 'transform 0.45s cubic-bezier(0.34, 1.56, 0.64, 1)';
        setTimeout(() => { this.style.transition = ''; }, 450);
      });
    });
  }

  /* ─────────────────────────────────────────────────────────
     7. TOPBAR SCROLL BLUR EFFECT
  ───────────────────────────────────────────────────────── */
  function initTopbarScroll() {
    const topbar = document.querySelector('.topbar');
    if (!topbar) return;

    const pageContent = document.querySelector('.page-content');
    const scrollTarget = pageContent || window;

    function onScroll() {
      const scrollY = pageContent
        ? pageContent.parentElement.scrollTop
        : window.scrollY;
      if (scrollY > 20) {
        topbar.classList.add('scrolled');
      } else {
        topbar.classList.remove('scrolled');
      }
    }

    if (pageContent) {
      const mainEl = pageContent.closest('.main') || document.querySelector('.main');
      if (mainEl) {
        mainEl.addEventListener('scroll', onScroll, { passive: true });
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ─────────────────────────────────────────────────────────
     8. SIDEBAR STAGGER ENTRANCE
  ───────────────────────────────────────────────────────── */
  function initSidebarEntrance() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach((item, i) => {
      item.style.opacity = '0';
      item.style.transform = 'translateX(-18px)';
      setTimeout(() => {
        item.style.transition = 'opacity 0.4s ease, transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)';
        item.style.opacity = '';
        item.style.transform = '';
      }, 80 + i * 50);
    });
  }

  /* ─────────────────────────────────────────────────────────
     9. BUTTON RIPPLE CLASS ASSIGNMENT (for CSS ::after)
  ───────────────────────────────────────────────────────── */
  function initButtonClasses() {
    document.querySelectorAll('.btn').forEach(btn => {
      btn.classList.add('btn-ripple');
    });
  }

  /* ─────────────────────────────────────────────────────────
     10. ACTIVE NAV HIGHLIGHT (preserve existing farmer.js logic)
  ───────────────────────────────────────────────────────── */
  function initActiveNav() {
    // Already handled in farmer.js — just add glow to active item
    const activeItem = document.querySelector('.nav-item.active');
    if (activeItem) {
      activeItem.style.setProperty('--glow', 'rgba(34,197,94,0.15)');
    }
  }

  /* ─────────────────────────────────────────────────────────
     11. TOAST NOTIFICATION SYSTEM
  ───────────────────────────────────────────────────────── */
  function createToastContainer() {
    if (document.getElementById('km-toast-container')) return;
    const container = document.createElement('div');
    container.id = 'km-toast-container';
    container.className = 'km-toast-container';
    document.body.appendChild(container);
  }

  window.kmToast = function (message, type = 'success', duration = 3500) {
    createToastContainer();
    const container = document.getElementById('km-toast-container');

    const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };

    const toast = document.createElement('div');
    toast.className = 'km-toast';
    toast.innerHTML = `
      <span class="km-toast-icon">${icons[type] || icons.success}</span>
      <span>${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('hide');
      setTimeout(() => toast.remove(), 400);
    }, duration);
  };

  /* ─────────────────────────────────────────────────────────
     12. CARD IMAGE PARALLAX ON MOUSE MOVE
  ───────────────────────────────────────────────────────── */
  function initCardParallax() {
    const isTouchDevice = window.matchMedia('(hover: none)').matches;
    if (isTouchDevice) return;

    const cards = document.querySelectorAll('.stat-card, .product-card, .blog-card');

    cards.forEach(card => {
      card.addEventListener('mousemove', function (e) {
        const rect = this.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width  - 0.5) * 10;
        const y = ((e.clientY - rect.top)  / rect.height - 0.5) * 10;
        this.style.transform = `translateY(-6px) rotateY(${x * 0.5}deg) rotateX(${-y * 0.5}deg) scale(1.01)`;
      });

      card.addEventListener('mouseleave', function () {
        this.style.transform = '';
        this.style.transition = 'transform 0.5s cubic-bezier(0.34, 1.2, 0.64, 1)';
        setTimeout(() => { this.style.transition = ''; }, 500);
      });
    });
  }

  /* ─────────────────────────────────────────────────────────
     13. SMOOTH ANCHOR SCROLL
  ───────────────────────────────────────────────────────── */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  /* ─────────────────────────────────────────────────────────
     14. FORM FIELD FOCUS GLOW
  ───────────────────────────────────────────────────────── */
  function initFormEffects() {
    const fields = document.querySelectorAll(
      '.form-field input, .form-field select, .form-field textarea, ' +
      '.blog-form-field input, .blog-form-field textarea, .blog-form-field select'
    );

    fields.forEach(field => {
      field.addEventListener('focus', function () {
        const wrapper = this.closest('.form-field') || this.closest('.blog-form-field');
        if (wrapper) {
          wrapper.style.transform = 'scale(1.005)';
          wrapper.style.transition = 'transform 0.25s ease';
        }
      });

      field.addEventListener('blur', function () {
        const wrapper = this.closest('.form-field') || this.closest('.blog-form-field');
        if (wrapper) {
          wrapper.style.transform = '';
        }
      });
    });
  }

  /* ─────────────────────────────────────────────────────────
     15. TABLE ROW GLOW HOVER
  ───────────────────────────────────────────────────────── */
  function initTableEffects() {
    document.querySelectorAll('tbody tr').forEach(row => {
      row.addEventListener('mouseenter', function () {
        this.style.boxShadow = 'inset 0 0 0 1px rgba(34,197,94,0.08)';
      });
      row.addEventListener('mouseleave', function () {
        this.style.boxShadow = '';
      });
    });
  }

  /* ─────────────────────────────────────────────────────────
     16. NAV ICON FLOAT ON ACTIVE
  ───────────────────────────────────────────────────────── */
  function initNavIconEffects() {
    const activeNav = document.querySelector('.nav-item.active svg');
    if (activeNav) {
      activeNav.style.animation = 'float 3s ease-in-out infinite';
    }
  }

  /* ─────────────────────────────────────────────────────────
     17. BADGE DOT PULSE
  ───────────────────────────────────────────────────────── */
  function initBadgePulse() {
    document.querySelectorAll('.badge').forEach(badge => {
      badge.style.animation = 'badgePulse 2s ease-in-out infinite';
    });
  }

  /* ─────────────────────────────────────────────────────────
     MAIN INIT — Run all effects
  ───────────────────────────────────────────────────────── */
  ready(function () {
    // Performance: check if reduced motion is preferred
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!prefersReduced) {
      initParticles();
      initMouseGlow();
      initCardParallax();
      initSidebarEntrance();
      initNavIconEffects();
    }

    // These run regardless of reduced motion preference
    initScrollReveal();
    initCounters();
    initRipple();
    initMagneticButtons();
    initTopbarScroll();
    initButtonClasses();
    initActiveNav();
    initSmoothScroll();
    initFormEffects();
    initTableEffects();
    initBadgePulse();
  });

})();
