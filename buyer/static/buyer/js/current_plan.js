/* ============================================
   KRUSHI MITRA - CURRENT PLAN PAGE JS
   Animations for the redesigned unique UI.
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ---- 1. Animate progress ring (.cp-ring-fill / .cp-ring-pct) ---- */
  var fill = document.querySelector('.cp-ring-fill');
  var pctEl = document.querySelector('.cp-ring-pct');
  if (fill && pctEl) {
    var target = parseInt(fill.getAttribute('data-percent') || '0', 10);
    var circumference = 377; // 2 * PI * 60
    var offset = circumference - (target / 100) * circumference;
    setTimeout(function () { fill.style.strokeDashoffset = offset; }, 350);
    var current = 0;
    var step = Math.max(1, Math.ceil(target / 60));
    var interval = setInterval(function () {
      current = Math.min(current + step, target);
      pctEl.textContent = current + '%';
      if (current >= target) clearInterval(interval);
    }, 22);
  }

  /* ---- 2. Animate cart bar (.cp-cart-bar-fill) ---- */
  document.querySelectorAll('.cp-cart-bar-fill[data-width]').forEach(function (bar) {
    var w = bar.getAttribute('data-width');
    setTimeout(function () { bar.style.width = w; }, 480);
  });

  /* ---- 3. FAQ accordion (.cp-faq-item / .cp-faq-body) ---- */
  document.querySelectorAll('.cp-faq-item').forEach(function (item) {
    var q = item.querySelector('.cp-faq-q');
    var body = item.querySelector('.cp-faq-body');
    if (!q || !body) return;
    q.addEventListener('click', function () {
      var isOpen = item.classList.contains('open');
      document.querySelectorAll('.cp-faq-item').forEach(function (i) {
        i.classList.remove('open');
        var b = i.querySelector('.cp-faq-body');
        if (b) b.classList.remove('open');
      });
      if (!isOpen) {
        item.classList.add('open');
        body.classList.add('open');
      }
    });
  });

  /* ---- 4. Button ripple ---- */
  document.querySelectorAll('.btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      var rect = this.getBoundingClientRect();
      var ripple = document.createElement('span');
      ripple.style.cssText = [
        'position:absolute', 'border-radius:50%', 'width:4px', 'height:4px',
        'background:rgba(255,255,255,0.35)', 'transform:scale(0)',
        'animation:ripple 0.6s linear',
        'left:' + (e.clientX - rect.left) + 'px',
        'top:' + (e.clientY - rect.top) + 'px',
        'pointer-events:none'
      ].join(';');
      this.style.position = 'relative';
      this.style.overflow = 'hidden';
      this.appendChild(ripple);
      setTimeout(function () { ripple.remove(); }, 700);
    });
  });

});
