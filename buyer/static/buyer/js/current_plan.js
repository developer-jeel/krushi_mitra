/* ============================================
   KRUSHI MITRA - CURRENT PLAN PAGE JS
   Animations only. Uses existing app.js as base.
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ---- 1. Animate progress ring ---- */
  function animateRing() {
    const fill = document.querySelector('.ring-fill');
    const percentEl = document.querySelector('.ring-percent');
    if (!fill || !percentEl) return;

    const target = parseInt(fill.getAttribute('data-percent') || '0', 10);
    const circumference = 346; // 2 * PI * 55
    const offset = circumference - (target / 100) * circumference;

    // Slight delay so the transition is visible
    setTimeout(function () {
      fill.style.strokeDashoffset = offset;
    }, 300);

    // Animate the number
    let current = 0;
    const step = Math.ceil(target / 60);
    const interval = setInterval(function () {
      current = Math.min(current + step, target);
      percentEl.textContent = current + '%';
      if (current >= target) clearInterval(interval);
    }, 25);
  }
  animateRing();

  /* ---- 2. Animate counter numbers ---- */
  function animateCounters() {
    document.querySelectorAll('[data-counter]').forEach(function (el) {
      const target = parseInt(el.getAttribute('data-counter'), 10);
      if (isNaN(target)) return;
      let current = 0;
      const step = Math.max(1, Math.ceil(target / 60));
      const interval = setInterval(function () {
        current = Math.min(current + step, target);
        el.textContent = current;
        if (current >= target) clearInterval(interval);
      }, 22);
    });
  }
  animateCounters();

  /* ---- 3. Animate progress bars ---- */
  function animateBars() {
    document.querySelectorAll('.cp-progress-fill[data-width]').forEach(function (bar) {
      var w = bar.getAttribute('data-width');
      setTimeout(function () {
        bar.style.width = w;
      }, 400);
    });
  }
  animateBars();

  /* ---- 4. Scroll-reveal (uses existing fadeInUp keyframe) ---- */
  function initReveal() {
    const els = document.querySelectorAll('.reveal-on-scroll');
    if (!els.length) return;
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var delay = entry.target.getAttribute('data-delay') || '0';
          entry.target.style.animationDelay = delay + 's';
          entry.target.classList.add('animate-fade-in-up');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { io.observe(el); });
  }
  initReveal();

  /* ---- 5. FAQ Accordion ---- */
  function initAccordion() {
    document.querySelectorAll('.cp-accordion-header').forEach(function (header) {
      header.addEventListener('click', function () {
        var item = this.closest('.cp-accordion-item');
        var body = item.querySelector('.cp-accordion-body');
        var isOpen = item.classList.contains('open');

        // Close all
        document.querySelectorAll('.cp-accordion-item').forEach(function (i) {
          i.classList.remove('open');
          var b = i.querySelector('.cp-accordion-body');
          if (b) b.classList.remove('open');
        });

        // Toggle clicked
        if (!isOpen) {
          item.classList.add('open');
          if (body) body.classList.add('open');
        }
      });
    });
  }
  initAccordion();

  /* ---- 6. Button ripple (consistent with rest of buyer panel) ---- */
  function initRipple() {
    document.querySelectorAll('.btn').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        var rect = this.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
        var ripple = document.createElement('span');
        ripple.style.cssText = [
          'position:absolute',
          'border-radius:50%',
          'width:4px',
          'height:4px',
          'background:rgba(255,255,255,0.4)',
          'transform:scale(0)',
          'animation:ripple 0.6s linear',
          'left:' + x + 'px',
          'top:' + y + 'px',
          'pointer-events:none'
        ].join(';');
        this.style.position = 'relative';
        this.style.overflow = 'hidden';
        this.appendChild(ripple);
        setTimeout(function () { ripple.remove(); }, 700);
      });
    });
  }
  initRipple();

});
