/**
 * premiumcheckout.js — Krushi Mitra Premium Checkout
 * Vanilla JavaScript · No frameworks · No API calls
 */

(function () {
  'use strict';

  /* ============================================================
     PLAN DATA
     ============================================================ */
  const PLANS = {
    standard: {
      name:        'Standard',
      icon:        '🔵',
      crown:       '⭐',
      badge:       '🔵 Standard',
      monthly:     99,
      yearly_per:  84,   // per month if billed yearly
      yearly_total: 1008,
      desc:        'Best for growing buyers — unlock bulk tools, AI advisor and more.',
      features: [
        '✔ Buy up to 5,000 KG',
        '✔ Bulk Purchase Unlock',
        '✔ AI Buying Advisor',
        '✔ Real-Time Price Alerts',
        '✔ Wishlist Alerts',
        '✔ Priority Orders',
        '✔ Faster Checkout',
        '✔ Premium Support',
      ],
    },
    premium: {
      name:         'Premium',
      icon:         '👑',
      crown:        '👑',
      badge:        '👑 Premium',
      monthly:      199,
      yearly_per:   169,
      yearly_total: 2028,
      desc:         'For serious bulk buyers — unlimited KG, zero fees, and dedicated support.',
      features: [
        '✔ Buy up to 50,000 KG (Unlimited)',
        '✔ Everything in Standard',
        '✔ Export Reports (PDF / Excel / CSV)',
        '✔ Zero Platform Fee',
        '✔ Highest Priority Orders',
        '✔ Premium Buyer Badge',
        '✔ Advanced Purchase Analytics',
        '✔ Dedicated Premium Support',
      ],
    },
  };

  const GST_RATE  = 0.18;
  const COUPONS   = {
    'KRUSHI20': { type: 'percent', value: 20, label: '20% off' },
    'SAVE50':   { type: 'flat',    value: 50, label: '₹50 off'  },
    'WELCOME10':{ type: 'percent', value: 10, label: '10% off'  },
  };

  /* ============================================================
     STATE
     ============================================================ */
  let state = {
    plan:          'standard',
    isYearly:      false,
    couponCode:    null,
    couponDiscount:0,
    paymentMethod: 'upi',
  };

  /* ============================================================
     ELEMENT REFS
     ============================================================ */
  const $  = (id)  => document.getElementById(id);
  const $$ = (sel) => document.querySelectorAll(sel);

  /* ============================================================
     INIT
     ============================================================ */
  document.addEventListener('DOMContentLoaded', () => {
    detectPlanFromURL();
    initScrollReveal();
    initProgressAnimation();
    initPlanCard();
    initBillingToggle();
    initPaymentMethods();
    initCoupon();
    initBuyerForm();
    initPayButtons();
    initRippleEffect();
    initStickyObserver();
    updateSummary();
  });

  /* ============================================================
     1. DETECT PLAN FROM URL / SESSION
     ============================================================ */
  function detectPlanFromURL() {
    const params = new URLSearchParams(window.location.search);
    const p = params.get('plan');
    if (p === 'premium') state.plan = 'premium';
    else state.plan = 'standard';

    const cycle = params.get('cycle');
    if (cycle === 'yearly') {
      state.isYearly = true;
    }
  }

  /* ============================================================
     2. SCROLL REVEAL
     ============================================================ */
  function initScrollReveal() {
    const items = $$('.fade-up');
    if (!items.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, idx) => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const delay = parseFloat(el.dataset.delay || 0) || (idx * 0.07);
          setTimeout(() => el.classList.add('visible'), delay * 1000);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    items.forEach((el, i) => {
      el.dataset.delay = (i * 0.07).toFixed(2);
      observer.observe(el);
    });
  }

  /* ============================================================
     3. PROGRESS ANIMATION
     ============================================================ */
  function initProgressAnimation() {
    const line1 = $('line1');
    if (line1) {
      setTimeout(() => line1.classList.add('active-line'), 300);
    }
  }

  /* ============================================================
     4. PLAN CARD
     ============================================================ */
  function initPlanCard() {
    renderPlanCard();
    const changePlanBtn = $('changePlanBtn');
    if (changePlanBtn) {
      changePlanBtn.addEventListener('click', () => {
        window.history.back();
      });
    }
  }

  function renderPlanCard() {
    const p = PLANS[state.plan];
    if (!p) return;

    const amount = state.isYearly ? p.yearly_per : p.monthly;

    setTextContent('planDisplayName',  p.name);
    setTextContent('planCrownIcon',    p.crown);
    setTextContent('planTypeBadge',    p.badge);
    setTextContent('planCycleBadge',   state.isYearly ? 'Yearly' : 'Monthly');
    animateValue('planDisplayAmount',  amount);
    setTextContent('planDisplayPeriod', state.isYearly ? '/mo · billed yearly' : '/month');
    setTextContent('planDisplayDesc',  p.desc);

    const featEl = $('planDisplayFeatures');
    if (featEl) {
      featEl.innerHTML = p.features.map(f => `<li>${f}</li>`).join('');
    }

    // Style premium plan
    const crownEl = $('planCrownIcon');
    if (crownEl && state.plan === 'premium') {
      crownEl.style.background = 'linear-gradient(135deg, rgba(253,186,45,0.25), rgba(253,186,45,0.08))';
      crownEl.style.borderColor = 'rgba(253,186,45,0.4)';
    }
  }

  /* ============================================================
     5. BILLING TOGGLE  (in-card + optional standalone)
     ============================================================ */
  function initBillingToggle() {
    // ── In-card toggle (inside Selected Plan card) ──
    const planBtn     = $('planBillingToggle');
    const planLblMon  = $('planLblMonthly');
    const planLblYear = $('planLblYearly');

    if (planBtn) {
      // Set initial visual state
      if (state.isYearly) applyToggleOn(planBtn, planLblMon, planLblYear);

      planBtn.addEventListener('click', () => {
        state.isYearly = !state.isYearly;
        if (state.isYearly) {
          applyToggleOn(planBtn, planLblMon, planLblYear);
        } else {
          applyToggleOff(planBtn, planLblMon, planLblYear);
        }
        renderPlanCard();
        updateSummary();
        updateBillingNote();
        syncStandaloneToggle();
      });

      // Clicking the labels also toggles
      if (planLblMon) planLblMon.addEventListener('click', () => {
        if (state.isYearly) { state.isYearly = false; applyToggleOff(planBtn, planLblMon, planLblYear); renderPlanCard(); updateSummary(); updateBillingNote(); syncStandaloneToggle(); }
      });
      if (planLblYear) planLblYear.addEventListener('click', () => {
        if (!state.isYearly) { state.isYearly = true; applyToggleOn(planBtn, planLblMon, planLblYear); renderPlanCard(); updateSummary(); updateBillingNote(); syncStandaloneToggle(); }
      });
    }

    // ── Standalone toggle (separate billing section, if present) ──
    const btn      = $('billingToggle');
    const lblMon   = $('lblMonthly');
    const lblYear  = $('lblYearly');
    const saveTag  = $('billingSaveTag');

    if (btn) {
      if (state.isYearly) applyYearlyToggle(btn, lblMon, lblYear, saveTag);

      btn.addEventListener('click', () => {
        state.isYearly = !state.isYearly;
        if (state.isYearly) {
          applyYearlyToggle(btn, lblMon, lblYear, saveTag);
        } else {
          removeYearlyToggle(btn, lblMon, lblYear, saveTag);
        }
        renderPlanCard();
        updateSummary();
        updateBillingNote();
        // Sync in-card toggle
        if (planBtn) {
          if (state.isYearly) applyToggleOn(planBtn, planLblMon, planLblYear);
          else                 applyToggleOff(planBtn, planLblMon, planLblYear);
        }
      });
    }
  }

  function applyToggleOn(btn, lblMon, lblYear) {
    btn.classList.add('on');
    btn.setAttribute('aria-checked', 'true');
    if (lblMon)  lblMon.classList.remove('active');
    if (lblYear) lblYear.classList.add('active');
    // Show save pill next to price
    const pill = $('planYearlySavePill');
    if (pill) pill.style.display = 'inline-flex';
  }

  function applyToggleOff(btn, lblMon, lblYear) {
    btn.classList.remove('on');
    btn.setAttribute('aria-checked', 'false');
    if (lblMon)  lblMon.classList.add('active');
    if (lblYear) lblYear.classList.remove('active');
    const pill = $('planYearlySavePill');
    if (pill) pill.style.display = 'none';
  }

  function syncStandaloneToggle() {
    const btn     = $('billingToggle');
    const lblMon  = $('lblMonthly');
    const lblYear = $('lblYearly');
    const saveTag = $('billingSaveTag');
    if (!btn) return;
    if (state.isYearly) applyYearlyToggle(btn, lblMon, lblYear, saveTag);
    else                 removeYearlyToggle(btn, lblMon, lblYear, saveTag);
  }

  function applyYearlyToggle(btn, lblMon, lblYear, saveTag) {
    btn.classList.add('active-toggle');
    btn.setAttribute('aria-checked', 'true');
    if (lblMon)  { lblMon.classList.remove('active');  }
    if (lblYear) { lblYear.classList.add('active'); }
    if (saveTag) { saveTag.classList.add('show'); }
  }

  function removeYearlyToggle(btn, lblMon, lblYear, saveTag) {
    btn.classList.remove('active-toggle');
    btn.setAttribute('aria-checked', 'false');
    if (lblMon)  { lblMon.classList.add('active'); }
    if (lblYear) { lblYear.classList.remove('active'); }
    if (saveTag) { saveTag.classList.remove('show'); }
  }

  function updateBillingNote() {
    const p      = PLANS[state.plan];
    const amount = state.isYearly ? p.yearly_per : p.monthly;

    // Standalone billing note
    const span   = $('billingTotalSpan');
    const note   = $('billingNote');
    if (span) span.textContent = amount;
    if (note) note.textContent = state.isYearly
      ? `Billed ₹${p.yearly_total} per year (₹${p.yearly_per}/mo). Cancel anytime.`
      : `Billed ₹${amount} per month. Cancel anytime.`;

    // In-card billing note
    const planBillingAmt  = $('planBillingAmount');
    const planBillingNote = $('planBillingNote');
    if (planBillingAmt) planBillingAmt.textContent = amount;
    if (planBillingNote) {
      planBillingNote.innerHTML = state.isYearly
        ? `Billed &#8377;${p.yearly_total}/year &nbsp;·&nbsp; <strong style="color:var(--success)">Save &#8377;${(p.monthly - p.yearly_per) * 12}</strong> vs monthly &nbsp;·&nbsp; Cancel anytime`
        : `Billed &#8377;<span id="planBillingAmount">${amount}</span>/month &nbsp;·&nbsp; Cancel anytime`;
    }
  }

  /* ============================================================
     6. PAYMENT METHODS
     ============================================================ */
  function initPaymentMethods() {
    const cards = $$('.payment-method-card');
    cards.forEach(card => {
      card.addEventListener('click', () => {
        cards.forEach(c => {
          c.classList.remove('active');
          c.setAttribute('aria-checked', 'false');
        });
        card.classList.add('active');
        card.setAttribute('aria-checked', 'true');
        state.paymentMethod = card.dataset.method;

        // Micro-bounce
        card.style.transform = 'scale(0.96)';
        setTimeout(() => { card.style.transform = ''; }, 150);
      });
    });
  }

  /* ============================================================
     7. COUPON
     ============================================================ */
  function initCoupon() {
    const applyBtn  = $('couponApplyBtn');
    const removeBtn = $('couponRemoveBtn');
    const input     = $('couponInput');

    if (!applyBtn || !input) return;

    applyBtn.addEventListener('click', applyCoupon);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') { e.preventDefault(); applyCoupon(); }
    });
    if (removeBtn) removeBtn.addEventListener('click', removeCoupon);
  }

  function applyCoupon() {
    const input    = $('couponInput');
    const code     = (input.value || '').trim().toUpperCase();
    const successEl = $('couponSuccess');
    const errorEl   = $('couponError');
    const errorText = $('couponErrorText');
    const discText  = $('couponDiscountText');

    hideEl(successEl);
    hideEl(errorEl);

    if (!code) {
      showEl(errorEl);
      if (errorText) errorText.textContent = 'Please enter a coupon code.';
      return;
    }

    const coupon = COUPONS[code];
    if (!coupon) {
      showEl(errorEl);
      if (errorText) errorText.textContent = `"${code}" is not a valid coupon code.`;
      shakeEl($('couponInputWrap'));
      return;
    }

    // Calculate discount
    const p       = PLANS[state.plan];
    const price   = state.isYearly ? p.yearly_per : p.monthly;
    let discount  = 0;
    if (coupon.type === 'percent') discount = Math.round(price * coupon.value / 100);
    else                           discount = Math.min(coupon.value, price);

    state.couponCode     = code;
    state.couponDiscount = discount;

    if (discText) discText.textContent = `You saved ₹${discount} (${coupon.label})`;
    showEl(successEl);

    // Disable input & button
    $('couponInput').disabled = true;
    $('couponApplyBtn').disabled = true;
    $('couponApplyBtn').style.opacity = '0.5';

    updateSummary();
  }

  function removeCoupon() {
    state.couponCode     = null;
    state.couponDiscount = 0;

    const successEl = $('couponSuccess');
    hideEl(successEl);

    const input   = $('couponInput');
    const applyEl = $('couponApplyBtn');
    if (input)   { input.value = ''; input.disabled = false; }
    if (applyEl) { applyEl.disabled = false; applyEl.style.opacity = ''; }

    updateSummary();
  }

  /* ============================================================
     8. BUYER FORM VALIDATION
     ============================================================ */
  function initBuyerForm() {
    const form = $('buyerForm');
    if (!form) return;

    // Live validation on blur
    const nameInput  = $('buyerName');
    const emailInput = $('buyerEmail');
    const phoneInput = $('buyerPhone');

    if (nameInput)  nameInput.addEventListener('blur',  () => validateName(nameInput));
    if (emailInput) emailInput.addEventListener('blur', () => validateEmail(emailInput));
    if (phoneInput) phoneInput.addEventListener('blur', () => validatePhone(phoneInput));

    // Phone: digits only
    if (phoneInput) {
      phoneInput.addEventListener('input', () => {
        phoneInput.value = phoneInput.value.replace(/\D/g, '').slice(0, 10);
      });
    }

    // GST: uppercase
    const gstInput = $('gstNumber');
    if (gstInput) {
      gstInput.addEventListener('input', () => {
        gstInput.value = gstInput.value.toUpperCase();
      });
    }
  }

  function validateName(input) {
    const group = input.closest('.form-group');
    if (!group) return true;
    const val = input.value.trim();
    if (val.length < 2) {
      group.classList.add('error'); group.classList.remove('valid');
      return false;
    }
    group.classList.remove('error'); group.classList.add('valid');
    return true;
  }

  function validateEmail(input) {
    const group = input.closest('.form-group');
    if (!group) return true;
    const re  = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const val = input.value.trim();
    if (!re.test(val)) {
      group.classList.add('error'); group.classList.remove('valid');
      const errEl = $('emailError');
      if (errEl) errEl.textContent = val ? 'Please enter a valid email address.' : 'Email is required.';
      return false;
    }
    group.classList.remove('error'); group.classList.add('valid');
    return true;
  }

  function validatePhone(input) {
    const group = input.closest('.form-group');
    if (!group) return true;
    const val = input.value.trim();
    if (!/^\d{10}$/.test(val)) {
      group.classList.add('error'); group.classList.remove('valid');
      return false;
    }
    group.classList.remove('error'); group.classList.add('valid');
    return true;
  }

  function validateForm() {
    const nameInput  = $('buyerName');
    const emailInput = $('buyerEmail');
    const phoneInput = $('buyerPhone');
    let valid = true;
    if (!validateName(nameInput))  valid = false;
    if (!validateEmail(emailInput)) valid = false;
    if (!validatePhone(phoneInput)) valid = false;
    return valid;
  }

  /* ============================================================
     9. PAY BUTTONS
     ============================================================ */
  function initPayButtons() {
    const btnDesktop = $('payBtnDesktop');
    const btnMobile  = $('payBtnMobile');

    [btnDesktop, btnMobile].forEach(btn => {
      if (!btn) return;
      btn.addEventListener('click', handlePayClick);
    });
  }

  function handlePayClick(e) {
    if (!validateForm()) {
      // Scroll to first error
      const firstError = document.querySelector('.form-group.error');
      if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
      shakeEl(firstError);
      return;
    }
    triggerRipple(e.currentTarget, e);
    simulatePaymentFlow();
  }

  function simulatePaymentFlow() {
    const btn = $('payBtnDesktop') || $('payBtnMobile');
    if (btn) {
      const origText = btn.querySelector('.pay-btn-text').textContent;
      btn.querySelector('.pay-btn-text').textContent = 'Processing…';
      btn.disabled = true;
      btn.style.opacity = '0.8';
      setTimeout(() => {
        showSuccessOverlay();
        btn.querySelector('.pay-btn-text').textContent = origText;
        btn.disabled = false;
        btn.style.opacity = '';
      }, 1800);
    }
  }

  /* ============================================================
     10. SUCCESS OVERLAY
     ============================================================ */
  function showSuccessOverlay() {
    const overlay = $('successOverlay');
    if (!overlay) return;
    const badge = $('successPlanBadge');
    if (badge) {
      const p = PLANS[state.plan];
      badge.textContent = `${p.crown} ${p.name} Plan — Active`;
    }
    overlay.style.display = 'flex';
    overlay.style.animation = 'none';
    void overlay.offsetWidth;
    document.body.style.overflow = 'hidden';

    // Restart SVG animations
    const ring  = overlay.querySelector('.success-ring');
    const check = overlay.querySelector('.success-check');
    if (ring)  { ring.style.animation  = 'none'; void ring.offsetWidth;  ring.style.animation  = 'drawRing 0.8s ease forwards'; }
    if (check) { check.style.animation = 'none'; void check.offsetWidth; check.style.animation = 'drawCheck 0.5s 0.6s ease forwards'; }

    // Close on backdrop click
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) hideSuccessOverlay();
    }, { once: true });
  }

  function hideSuccessOverlay() {
    const overlay = $('successOverlay');
    if (overlay) {
      overlay.style.display = 'none';
      document.body.style.overflow = '';
    }
  }

  /* ============================================================
     11. ORDER SUMMARY CALCULATIONS
     ============================================================ */
  function updateSummary() {
    const p         = PLANS[state.plan];
    const basePrice = state.isYearly ? p.yearly_per : p.monthly;
    const couponDis = state.couponDiscount;
    const subtotal  = Math.max(0, basePrice - couponDis);
    const gst       = parseFloat((subtotal * GST_RATE).toFixed(2));
    const total     = parseFloat((subtotal + gst).toFixed(2));

    // Summary Panel
    setTextContent('summaryPlanName',  `${p.name} Plan`);
    setTextContent('summaryCycleBadge', state.isYearly ? 'Yearly' : 'Monthly');
    setTextContent('summaryPlanPrice', `₹${basePrice}.00`);
    setTextContent('summaryGST',       `₹${gst}`);

    // Coupon discount line
    const discLine = $('summaryDiscountLine');
    if (discLine) {
      if (couponDis > 0) {
        showEl(discLine);
        setTextContent('summaryDiscountValue', `-₹${couponDis}`);
      } else {
        hideEl(discLine);
      }
    }

    // Yearly savings line
    const yearlySavLine = $('summaryYearlySavingsLine');
    if (yearlySavLine) {
      if (state.isYearly) {
        const saving = (p.monthly - p.yearly_per) * 12;
        showEl(yearlySavLine);
        setTextContent('summaryYearlySavings', `-₹${saving}`);
      } else {
        hideEl(yearlySavLine);
      }
    }

    // Animate total
    const totalEls = [
      $('summaryTotal'),
      $('payBtnDesktopAmount'),
      $('payBtnMobileAmount'),
    ];
    totalEls.forEach(el => {
      if (!el) return;
      el.classList.remove('price-change');
      void el.offsetWidth;
      el.classList.add('price-change');
      el.textContent = `₹${total}`;
    });

    updateBillingNote();
  }

  /* ============================================================
     12. RIPPLE EFFECT
     ============================================================ */
  function initRippleEffect() {
    $$('.ripple-btn').forEach(btn => {
      btn.addEventListener('click', (e) => triggerRipple(btn, e));
    });
  }

  function triggerRipple(el, e) {
    if (!el) return;
    const rect   = el.getBoundingClientRect();
    const size   = Math.max(rect.width, rect.height) * 2;
    const x      = (e.clientX - rect.left) - size / 2;
    const y      = (e.clientY - rect.top)  - size / 2;
    const ripple = document.createElement('span');
    ripple.classList.add('ripple-effect');
    ripple.style.cssText = `width:${size}px;height:${size}px;left:${x}px;top:${y}px;`;
    el.appendChild(ripple);
    ripple.addEventListener('animationend', () => ripple.remove());
  }

  /* ============================================================
     13. STICKY SUMMARY ANIMATION ON SCROLL
     ============================================================ */
  function initStickyObserver() {
    const header = $('checkoutHeader');
    if (!header) return;
    window.addEventListener('scroll', () => {
      if (window.scrollY > 40) {
        header.style.boxShadow = '0 4px 30px rgba(0,0,0,0.5)';
      } else {
        header.style.boxShadow = '';
      }
    }, { passive: true });
  }

  /* ============================================================
     HELPERS
     ============================================================ */
  function setTextContent(id, text) {
    const el = $(id);
    if (el) el.textContent = text;
  }

  function animateValue(id, newVal) {
    const el = $(id);
    if (!el) return;
    el.style.animation = 'none';
    void el.offsetWidth;
    el.style.animation = 'priceFlip 0.4s ease forwards';
    setTimeout(() => { el.textContent = newVal; }, 100);
  }

  function showEl(el) {
    if (el) el.style.display = '';
  }

  function hideEl(el) {
    if (el) el.style.display = 'none';
  }

  function shakeEl(el) {
    if (!el) return;
    el.style.animation = 'none';
    void el.offsetWidth;
    const keyframes = [
      { transform: 'translateX(0)' },
      { transform: 'translateX(-8px)' },
      { transform: 'translateX(8px)' },
      { transform: 'translateX(-6px)' },
      { transform: 'translateX(6px)' },
      { transform: 'translateX(0)' },
    ];
    el.animate(keyframes, { duration: 400, easing: 'ease-in-out' });
  }

})();
