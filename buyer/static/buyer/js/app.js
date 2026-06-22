/* ============================================
   KRUSHI MITRA - PREMIUM BUYER PANEL
   GLOBAL APPLICATION JAVASCRIPT
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {

  // ==========================================
  // THEME SYSTEM
  // ==========================================
  function initTheme() {
    const savedTheme = localStorage.getItem('krushi-mitra-theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    const themeToggles = document.querySelectorAll('.theme-toggle');
    themeToggles.forEach(btn => {
      btn.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
      btn.addEventListener('click', function() {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('krushi-mitra-theme', next);
        document.querySelectorAll('.theme-toggle').forEach(t => {
          t.innerHTML = next === 'dark' ? '☀️' : '🌙';
        });
        showToast('success', 'Theme', `Switched to ${next} mode`);
      });
    });
  }
  initTheme();

  // ==========================================
  // SIDEBAR SYSTEM
  // ==========================================
  function initSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const toggleBtn = document.querySelector('.sidebar-toggle');
    const mainWrapper = document.querySelector('.main-wrapper');
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const backdrop = document.querySelector('.sidebar-backdrop');

    // Desktop collapse
    if (toggleBtn) {
      toggleBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        sidebar.classList.toggle('collapsed');
        mainWrapper.classList.toggle('expanded');
        const isCollapsed = sidebar.classList.contains('collapsed');
        localStorage.setItem('krushi-mitra-sidebar', isCollapsed ? 'collapsed' : 'expanded');
      });

      // Restore sidebar state
      const savedState = localStorage.getItem('krushi-mitra-sidebar');
      if (savedState === 'collapsed' && window.innerWidth > 768) {
        sidebar.classList.add('collapsed');
        mainWrapper.classList.add('expanded');
      }
    }

    // Mobile toggle
    if (mobileMenuBtn) {
      mobileMenuBtn.addEventListener('click', function() {
        sidebar.classList.toggle('open');
        if (backdrop) backdrop.classList.toggle('open');
      });
    }

    if (backdrop) {
      backdrop.addEventListener('click', function() {
        sidebar.classList.remove('open');
        backdrop.classList.remove('open');
      });
    }

    // Sidebar navigation highlighting
    const currentPath = window.location.pathname.split('/').pop() || 'dashboard.html';
    const sidebarItems = document.querySelectorAll('.sidebar-item');
    sidebarItems.forEach(item => {
      const href = item.getAttribute('href');
      if (href && currentPath.includes(href)) {
        item.classList.add('active');
      }
    });
  }
  initSidebar();

  // ==========================================
  // DROPDOWN SYSTEM
  // ==========================================
  function initDropdowns() {
    document.querySelectorAll('.dropdown').forEach(dropdown => {
      const trigger = dropdown.querySelector('.dropdown-trigger');
      const menu = dropdown.querySelector('.dropdown-menu');
      
      if (trigger && menu) {
        trigger.addEventListener('click', function(e) {
          e.stopPropagation();
          // Close other dropdowns
          document.querySelectorAll('.dropdown-menu.open').forEach(m => {
            if (m !== menu) m.classList.remove('open');
          });
          menu.classList.toggle('open');
        });
      }
    });

    // Close dropdowns on outside click
    document.addEventListener('click', function() {
      document.querySelectorAll('.dropdown-menu.open').forEach(m => {
        m.classList.remove('open');
      });
    });
  }
  initDropdowns();

  // ==========================================
  // MODAL SYSTEM
  // ==========================================
  function initModals() {
    // Open modals
    document.querySelectorAll('[data-modal]').forEach(btn => {
      btn.addEventListener('click', function() {
        const modalId = this.getAttribute('data-modal');
        const modal = document.getElementById(modalId);
        if (modal) {
          modal.classList.add('open');
          document.body.style.overflow = 'hidden';
        }
      });
    });

    // Close modals
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      const closeBtn = overlay.querySelector('.modal-close');
      const closeBtns = overlay.querySelectorAll('[data-dismiss="modal"]');
      
      function closeModal() {
        overlay.classList.remove('open');
        document.body.style.overflow = '';
      }

      if (closeBtn) closeBtn.addEventListener('click', closeModal);
      closeBtns.forEach(btn => btn.addEventListener('click', closeModal));
      
      overlay.addEventListener('click', function(e) {
        if (e.target === overlay) closeModal();
      });
    });
  }
  initModals();

  // ==========================================
  // TABS SYSTEM
  // ==========================================
  function initTabs() {
    document.querySelectorAll('.tabs').forEach(tabContainer => {
      const tabs = tabContainer.querySelectorAll('.tab');
      tabs.forEach(tab => {
        tab.addEventListener('click', function() {
          const target = this.getAttribute('data-tab');
          
          // Update tab active state
          tabs.forEach(t => t.classList.remove('active'));
          this.classList.add('active');
          
          // Show corresponding content
          const parent = tabContainer.closest('[data-tabs]') || document;
          const contents = parent.querySelectorAll('[data-tab-content]');
          contents.forEach(c => {
            c.classList.remove('active');
            if (c.getAttribute('data-tab-content') === target) {
              c.classList.add('active');
            }
          });
        });
      });
    });
  }
  initTabs();

  // ==========================================
  // TOAST NOTIFICATION SYSTEM
  // ==========================================
  window.showToast = function(type, title, message, duration = 4000) {
    const container = document.querySelector('.toast-container');
    if (!container) {
      const newContainer = document.createElement('div');
      newContainer.className = 'toast-container';
      document.body.appendChild(newContainer);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
    
    toast.innerHTML = `
      <span class="toast-icon">${icons[type] || 'ℹ️'}</span>
      <div class="toast-content">
        <div class="toast-title">${title}</div>
        <div class="toast-message">${message}</div>
      </div>
      <button class="toast-close">✕</button>
    `;

    document.querySelector('.toast-container').appendChild(toast);
    
    // Trigger animation
    requestAnimationFrame(() => {
      toast.classList.add('show');
    });

    // Close handler
    toast.querySelector('.toast-close').addEventListener('click', function() {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    });

    // Auto close
    setTimeout(() => {
      if (toast.parentElement) {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
      }
    }, duration);
  };

  // ==========================================
  // COUNTER ANIMATION
  // ==========================================
  function initCounters() {
    const counterElements = document.querySelectorAll('[data-counter]');
    
    if (counterElements.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.getAttribute('data-counter'));
          const duration = parseInt(el.getAttribute('data-duration')) || 2000;
          const prefix = el.getAttribute('data-prefix') || '';
          const suffix = el.getAttribute('data-suffix') || '';
          
          animateCounter(el, target, duration, prefix, suffix);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.3 });

    counterElements.forEach(el => observer.observe(el));
  }

  function animateCounter(element, target, duration, prefix, suffix) {
    const start = performance.now();
    
    function update(currentTime) {
      const elapsed = currentTime - start;
      const progress = Math.min(elapsed / duration, 1);
      const easeOut = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(easeOut * target);
      
      element.textContent = prefix + current.toLocaleString() + suffix;
      
      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        element.textContent = prefix + target.toLocaleString() + suffix;
      }
    }
    
    requestAnimationFrame(update);
  }
  initCounters();

  // ==========================================
  // SCROLL REVEAL ANIMATIONS
  // ==========================================
  function initScrollReveal() {
    const revealElements = document.querySelectorAll('[data-reveal]');
    
    if (revealElements.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const animation = el.getAttribute('data-reveal') || 'fadeInUp';
          const delay = el.getAttribute('data-delay') || '0';
          
          el.style.animationDelay = delay + 'ms';
          el.style.animationName = animation;
          el.style.animationDuration = '0.6s';
          el.style.animationFillMode = 'both';
          
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.1 });

    revealElements.forEach(el => {
      el.style.opacity = '0';
      observer.observe(el);
    });
  }
  initScrollReveal();

  // ==========================================
  // SEARCH SYSTEM
  // ==========================================
  function initSearch() {
    const searchInputs = document.querySelectorAll('.search-box input');

    searchInputs.forEach(input => {
      input.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();
        const searchTarget = this.closest('[data-search-target]');
        
        if (searchTarget) {
          const items = searchTarget.querySelectorAll('[data-search-item]');
          items.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(query) ? '' : 'none';
          });
        }
      });
    });

    // Global search overlay
    const globalSearch = document.querySelector('.global-search');
    if (globalSearch) {
      document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
          e.preventDefault();
          globalSearch.classList.add('open');
          globalSearch.querySelector('input')?.focus();
        }
        if (e.key === 'Escape') {
          globalSearch.classList.remove('open');
        }
      });

      globalSearch.addEventListener('click', function(e) {
        if (e.target === this) {
          this.classList.remove('open');
        }
      });
    }
  }
  initSearch();

  // ==========================================
  // QUANTITY SELECTOR
  // ==========================================
  function initQuantitySelectors() {
    document.querySelectorAll('.qty-selector').forEach(container => {
      const input = container.querySelector('.qty-input');
      const minus = container.querySelector('.qty-minus');
      const plus = container.querySelector('.qty-plus');
      
      if (!input || !minus || !plus) return;

      const min = parseInt(input.getAttribute('min') || 1);
      const max = parseInt(input.getAttribute('max') || 99999);

      minus.addEventListener('click', function() {
        let val = parseInt(input.value) || min;
        if (val > min) {
          input.value = val - 1;
          triggerEvent(input, 'change');
        }
      });

      plus.addEventListener('click', function() {
        let val = parseInt(input.value) || min;
        if (val < max) {
          input.value = val + 1;
          triggerEvent(input, 'change');
        }
      });

      input.addEventListener('change', function() {
        let val = parseInt(this.value) || min;
        if (val < min) this.value = min;
        if (val > max) this.value = max;
      });
    });
  }
  initQuantitySelectors();

  function triggerEvent(element, eventName) {
    const event = new Event(eventName, { bubbles: true });
    element.dispatchEvent(event);
  }

  // ==========================================
  // CART QUANTITY UPDATE
  // ==========================================
  function initCartQuantity() {
    document.querySelectorAll('.cart-qty-input').forEach(input => {
      input.addEventListener('change', function() {
        const row = this.closest('.cart-item');
        if (row) {
          const price = parseFloat(row.querySelector('.cart-unit-price')?.getAttribute('data-price') || 0);
          const qty = parseInt(this.value) || 1;
          const totalEl = row.querySelector('.cart-total-price');
          if (totalEl) {
            totalEl.textContent = '₹' + (price * qty).toLocaleString('en-IN');
          }
        }
        updateCartSummary();
      });
    });
  }
  initCartQuantity();

  function updateCartSummary() {
    // Override in cart page
  }

  // ==========================================
  // PRICE CALCULATOR
  // ==========================================
  function initPriceCalculator() {
    const calc = document.querySelector('.price-calculator');
    if (!calc) return;

    const qtyInput = calc.querySelector('.calc-qty');
    const priceDisplay = calc.querySelector('.calc-total-price');
    const unitPrice = parseFloat(calc.getAttribute('data-unit-price') || 0);

    if (qtyInput && priceDisplay) {
      qtyInput.addEventListener('input', function() {
        const qty = parseFloat(this.value) || 1;
        priceDisplay.textContent = '₹' + (unitPrice * qty).toLocaleString('en-IN');
      });
    }
  }
  initPriceCalculator();

  // ==========================================
  // COUPON SYSTEM
  // ==========================================
  function initCoupon() {
    const couponBtns = document.querySelectorAll('.apply-coupon');
    couponBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        const input = this.closest('.coupon-section')?.querySelector('.coupon-input');
        if (input && input.value.trim()) {
          const discountEl = document.querySelector('.discount-amount');
          if (discountEl) {
            discountEl.textContent = '-₹500';
            discountEl.closest('.discount-row')?.classList.remove('hidden');
          }
          showToast('success', 'Coupon Applied', `Coupon "${input.value}" applied successfully!`);
          updateOrderTotal();
        } else {
          showToast('error', 'Invalid Coupon', 'Please enter a valid coupon code.');
        }
      });
    });
  }
  initCoupon();

  function updateOrderTotal() {
    // Override per page
  }

  // ==========================================
  // RIPPLE EFFECT
  // ==========================================
  function initRipple() {
    document.querySelectorAll('.btn, .sidebar-item, .nav-btn, .stat-card').forEach(el => {
      el.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        ripple.className = 'ripple-effect';
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
        ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
        this.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
      });
    });
  }
  initRipple();

  // Add ripple style dynamically
  const rippleStyle = document.createElement('style');
  rippleStyle.textContent = `
    .ripple-effect {
      position: absolute;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.3);
      transform: scale(0);
      animation: ripple 0.6s ease-out;
      pointer-events: none;
      z-index: 1;
    }
    [data-theme="dark"] .ripple-effect {
      background: rgba(255, 255, 255, 0.15);
    }
    .btn, .sidebar-item, .nav-btn, .stat-card {
      position: relative;
      overflow: hidden;
    }
  `;
  document.head.appendChild(rippleStyle);

  // ==========================================
  // MOBILE RESPONSIVE HANDLER
  // ==========================================
  function handleResponsive() {
    const sidebar = document.querySelector('.sidebar');
    const backdrop = document.querySelector('.sidebar-backdrop');
    
    function checkWidth() {
      if (window.innerWidth > 768) {
        if (sidebar) sidebar.classList.remove('open');
        if (backdrop) backdrop.classList.remove('open');
      }
    }

    window.addEventListener('resize', checkWidth);
    checkWidth();
  }
  handleResponsive();

  // ==========================================
  // PAGE REVEAL ANIMATION
  // ==========================================
  function initPageReveal() {
    const pageContent = document.querySelector('.main-content');
    if (pageContent) {
      pageContent.style.opacity = '0';
      pageContent.style.transform = 'translateY(20px)';
      
      requestAnimationFrame(() => {
        pageContent.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        pageContent.style.opacity = '1';
        pageContent.style.transform = 'translateY(0)';
      });
    }
  }
  initPageReveal();

  // ==========================================
  // FILTER SYSTEM (BROWSE CROPS)
  // ==========================================
  function initFilters() {
    const applyFilters = document.querySelectorAll('.apply-filters');
    applyFilters.forEach(btn => {
      btn.addEventListener('click', function() {
        showToast('info', 'Filters Applied', 'Showing filtered results');
        
        const grid = document.querySelector('.crop-grid');
        if (grid) {
          grid.querySelectorAll('.crop-card').forEach(card => {
            card.style.animation = 'none';
            card.offsetHeight;
            card.style.animation = `fadeInUp 0.4s forwards`;
          });
        }
      });
    });

    const clearFilters = document.querySelectorAll('.clear-filters');
    clearFilters.forEach(btn => {
      btn.addEventListener('click', function() {
        const filterForm = this.closest('.filter-sidebar') || this.closest('[data-filter-form]');
        if (filterForm) {
          filterForm.querySelectorAll('input, select').forEach(el => {
            if (el.type === 'text' || el.type === 'number') el.value = '';
            else if (el.type === 'checkbox' || el.type === 'radio') el.checked = false;
            else if (el.tagName === 'SELECT') el.selectedIndex = 0;
          });
        }
        showToast('info', 'Filters Cleared', 'All filters have been reset');
      });
    });
  }
  initFilters();

  // ==========================================
  // PAGINATION
  // ==========================================
  function initPagination() {
    document.querySelectorAll('.pagination .page-btn').forEach(btn => {
      btn.addEventListener('click', function() {
        if (this.classList.contains('disabled')) return;
        
        document.querySelectorAll('.pagination .page-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        // Scroll to top of results
        const results = document.querySelector('.results-container');
        if (results) {
          results.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }
  initPagination();

  // ==========================================
  // INQUIRY FORM HANDLING
  // ==========================================
  function initInquiryForms() {
    document.querySelectorAll('.inquiry-form').forEach(form => {
      const submitBtn = form.querySelector('.submit-inquiry');
      const draftBtn = form.querySelector('.save-draft');

      if (submitBtn) {
        submitBtn.addEventListener('click', function(e) {
          e.preventDefault();
          this.innerHTML = '<span class="spinner spinner-sm"></span> Submitting...';
          this.disabled = true;

          setTimeout(() => {
            this.innerHTML = '✅ Submitted Successfully';
            showToast('success', 'Inquiry Submitted', 'Your inquiry has been submitted successfully.');
            
            setTimeout(() => {
              this.innerHTML = 'Submit Inquiry';
              this.disabled = false;
              form.reset();
            }, 2000);
          }, 1500);
        });
      }

      if (draftBtn) {
        draftBtn.addEventListener('click', function(e) {
          e.preventDefault();
          showToast('info', 'Draft Saved', 'Your inquiry has been saved as draft.');
        });
      }
    });
  }
  initInquiryForms();

  // ==========================================
  // WISHLIST TOGGLE
  // ==========================================
  function initWishlistToggles() {
    document.querySelectorAll('.wishlist-toggle').forEach(btn => {
      btn.addEventListener('click', function() {
        this.classList.toggle('active');
        const isActive = this.classList.contains('active');
        this.innerHTML = isActive ? '❤️' : '🤍';
        
        if (isActive) {
          showToast('success', 'Added to Wishlist', 'Item added to your wishlist.');
        } else {
          showToast('info', 'Removed from Wishlist', 'Item removed from your wishlist.');
        }
      });
    });
  }
  initWishlistToggles();

  // ==========================================
  // CHARACTER COUNTER
  // ==========================================
  function initCharCounters() {
    document.querySelectorAll('[data-maxlength]').forEach(textarea => {
      const max = parseInt(textarea.getAttribute('data-maxlength'));
      const counter = textarea.parentElement?.querySelector('.char-count');
      
      if (counter) {
        textarea.addEventListener('input', function() {
          const remaining = max - this.value.length;
          counter.textContent = `${remaining} characters remaining`;
          counter.style.color = remaining < 20 ? 'var(--red-500)' : 'var(--text-muted)';
        });
      }
    });
  }
  initCharCounters();

  // ==========================================
  // ACCORDION
  // ==========================================
  function initAccordion() {
    document.querySelectorAll('.accordion').forEach(accordion => {
      accordion.querySelectorAll('.accordion-header').forEach(header => {
        header.addEventListener('click', function() {
          const item = this.closest('.accordion-item');
          const content = item.querySelector('.accordion-content');
          const isOpen = item.classList.contains('open');
          
          // Close others
          accordion.querySelectorAll('.accordion-item.open').forEach(i => {
            if (i !== item) {
              i.classList.remove('open');
              i.querySelector('.accordion-content').style.maxHeight = '0';
            }
          });

          if (isOpen) {
            item.classList.remove('open');
            content.style.maxHeight = '0';
          } else {
            item.classList.add('open');
            content.style.maxHeight = content.scrollHeight + 'px';
          }
        });
      });
    });
  }
  initAccordion();

  // ==========================================
  // FORM VALIDATION HELPERS
  // ==========================================
  function initFormValidation() {
    document.querySelectorAll('.needs-validation').forEach(form => {
      form.addEventListener('submit', function(e) {
        e.preventDefault();
        let valid = true;

        this.querySelectorAll('[required]').forEach(field => {
          if (!field.value.trim()) {
            field.classList.add('error');
            valid = false;
            
            const errorEl = field.parentElement.querySelector('.form-error');
            if (errorEl) errorEl.textContent = 'This field is required';
          } else {
            field.classList.remove('error');
            const errorEl = field.parentElement.querySelector('.form-error');
            if (errorEl) errorEl.textContent = '';
          }
        });

        if (valid) {
          showToast('success', 'Success', 'Form submitted successfully!');
        } else {
          showToast('error', 'Validation Error', 'Please fill in all required fields.');
        }
      });
    });

    // Clear errors on input
    document.querySelectorAll('.form-input, .form-select, .form-textarea').forEach(field => {
      field.addEventListener('input', function() {
        this.classList.remove('error');
        const errorEl = this.parentElement.querySelector('.form-error');
        if (errorEl) errorEl.textContent = '';
      });
    });
  }
  initFormValidation();

  // ==========================================
  // TOOLTIP INIT
  // ==========================================
  function initTooltips() {
    document.querySelectorAll('[data-tooltip]').forEach(el => {
      el.addEventListener('mouseenter', function() {
        // Tooltips handled via CSS pseudo-elements for collapsed sidebar
      });
    });
  }
  initTooltips();

  // ==========================================
  // ACTIVE STATUS INDICATORS
  // ==========================================
  function initOnlineStatus() {
    document.querySelectorAll('.online-status').forEach(el => {
      const isOnline = Math.random() > 0.3;
      el.className = `online-status ${isOnline ? 'online' : 'offline'}`;
      el.innerHTML = isOnline ? '● Online' : '○ Offline';
    });
  }
  initOnlineStatus();

  // ==========================================
  // TYPING INDICATOR (Messages)
  // ==========================================
  function initTypingIndicator() {
    const chatInputs = document.querySelectorAll('.chat-input');
    chatInputs.forEach(input => {
      input.addEventListener('input', function() {
        const indicator = document.querySelector('.typing-indicator');
        if (indicator) {
          if (this.value.trim()) {
            indicator.classList.add('active');
          } else {
            indicator.classList.remove('active');
          }
        }
      });
    });
  }
  initTypingIndicator();

  // ==========================================
  // SEND MESSAGE (Messages)
  // ==========================================
  function initSendMessage() {
    document.querySelectorAll('.send-message').forEach(btn => {
      btn.addEventListener('click', function() {
        const chatContainer = document.querySelector('.chat-messages');
        const input = document.querySelector('.chat-input');
        
        if (!chatContainer || !input || !input.value.trim()) return;

        const message = input.value.trim();
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble sent';
        bubble.innerHTML = `
          <div class="message-text">${message}</div>
          <div class="message-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
        `;
        
        chatContainer.appendChild(bubble);
        input.value = '';
        chatContainer.scrollTop = chatContainer.scrollHeight;

        // Simulate reply
        setTimeout(() => {
          const reply = document.createElement('div');
          reply.className = 'message-bubble received';
          const replies = [
            'Sure, I\'ll check the latest pricing.',
            'We have fresh stock available.',
            'Let me confirm with the warehouse.',
            'I can arrange bulk delivery.',
            'The quality report is ready.'
          ];
          reply.innerHTML = `
            <div class="message-text">${replies[Math.floor(Math.random() * replies.length)]}</div>
            <div class="message-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
          `;
          chatContainer.appendChild(reply);
          chatContainer.scrollTop = chatContainer.scrollHeight;
        }, 1000 + Math.random() * 2000);
      });
    });
  }
  initSendMessage();

  // ==========================================
  // NOTIFICATION MARK READ
  // ==========================================
  function initNotificationActions() {
    document.querySelectorAll('.mark-read').forEach(btn => {
      btn.addEventListener('click', function() {
        const card = this.closest('.notification-card');
        if (card) {
          card.classList.remove('unread');
          card.classList.add('read');
          showToast('info', 'Marked as Read', 'Notification marked as read.');
        }
      });
    });

    document.querySelectorAll('.archive-notification').forEach(btn => {
      btn.addEventListener('click', function() {
        const card = this.closest('.notification-card');
        if (card) {
          card.style.transition = 'all 0.3s ease';
          card.style.transform = 'translateX(100%)';
          card.style.opacity = '0';
          setTimeout(() => card.remove(), 300);
          showToast('info', 'Archived', 'Notification archived.');
        }
      });
    });

    document.querySelectorAll('.mark-all-read').forEach(btn => {
      btn.addEventListener('click', function() {
        document.querySelectorAll('.notification-card.unread').forEach(card => {
          card.classList.remove('unread');
          card.classList.add('read');
        });
        showToast('success', 'All Read', 'All notifications marked as read.');
      });
    });
  }
  initNotificationActions();

  // ==========================================
  // SETTINGS TOGGLES
  // ==========================================
  function initSettingsToggles() {
    document.querySelectorAll('.toggle-switch input').forEach(toggle => {
      toggle.addEventListener('change', function() {
        const label = this.closest('.toggle-switch')?.querySelector('.toggle-label');
        if (label) {
          label.textContent = this.checked ? 'Enabled' : 'Disabled';
        }
      });
    });
  }
  initSettingsToggles();

  // ==========================================
  // IMAGE ZOOM ON CROP DETAILS
  // ==========================================
  function initImageZoom() {
    const mainImage = document.querySelector('.product-gallery-main img');
    if (!mainImage) return;

    const gallery = document.querySelector('.product-gallery-main');
    
    gallery.addEventListener('mousemove', function(e) {
      const rect = this.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      mainImage.style.transformOrigin = `${x}% ${y}%`;
      mainImage.style.transform = 'scale(2)';
    });

    gallery.addEventListener('mouseleave', function() {
      mainImage.style.transformOrigin = 'center center';
      mainImage.style.transform = 'scale(1)';
    });

    // Thumbnail navigation
    const thumbs = document.querySelectorAll('.thumbnail-nav img');
    thumbs.forEach(thumb => {
      thumb.addEventListener('click', function() {
        const src = this.getAttribute('src');
        mainImage.setAttribute('src', src);
        thumbs.forEach(t => t.classList.remove('active'));
        this.classList.add('active');
      });
    });
  }
  initImageZoom();

  // ==========================================
  // ORDER TIMELINE
  // ==========================================
  function initOrderTimeline() {
    // Timeline steps are already styled via CSS
    // Add a simple animation to highlight current step
    const currentStep = document.querySelector('.timeline-step.active');
    if (currentStep) {
      currentStep.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }
  initOrderTimeline();

  // ==========================================
  // QUICK ACTIONS BUTTON
  // ==========================================
  function initQuickActions() {
    document.querySelectorAll('.quick-actions-btn').forEach(btn => {
      btn.addEventListener('click', function() {
        const menu = this.nextElementSibling;
        if (menu && menu.classList.contains('dropdown-menu')) {
          menu.classList.toggle('open');
        }
      });
    });
  }
  initQuickActions();

  // ==========================================
  // PASSWORD VISIBILITY TOGGLE
  // ==========================================
  function initPasswordToggle() {
    document.querySelectorAll('.password-toggle').forEach(btn => {
      btn.addEventListener('click', function() {
        const input = this.closest('.password-field')?.querySelector('input');
        if (input) {
          const type = input.type === 'password' ? 'text' : 'password';
          input.type = type;
          this.innerHTML = type === 'password' ? '👁️' : '👁️‍🗨️';
        }
      });
    });
  }
  initPasswordToggle();

  // ==========================================
  // DYNAMIC BREADCRUMB UPDATE
  // ==========================================
  function updateBreadcrumb() {
    const breadcrumb = document.querySelector('.breadcrumb');
    if (!breadcrumb) return;

    const path = window.location.pathname.split('/').pop().replace('.html', '');
    const pageNames = {
      'dashboard': 'Dashboard',
      'browse-crops': 'Browse Crops',
      'crop-details': 'Crop Details',
      'cart': 'Cart',
      'checkout': 'Checkout',
      'orders': 'Orders',
      'order-details': 'Order Details',
      'wishlist': 'Wishlist',
      'bulk-order': 'Bulk Order',
      'export-inquiry': 'Export Inquiry',
      'messages': 'Messages',
      'notifications': 'Notifications',
      'profile': 'Profile',
      'verification': 'Verification',
      'bank-details': 'Bank Details',
      'settings': 'Settings'
    };

    const pageName = pageNames[path] || 'Dashboard';
    const lastCrumb = breadcrumb.querySelector('.current');
    if (lastCrumb) {
      lastCrumb.textContent = pageName;
    }

    const title = document.querySelector('.page-title');
    if (title) {
      title.textContent = pageName;
    }
  }
  updateBreadcrumb();

  // ==========================================
  // BULK ORDER / EXPORT INQUIRY HISTORY
  // ==========================================
  function initInquiryHistory() {
    document.querySelectorAll('.inquiry-card').forEach(card => {
      card.addEventListener('click', function() {
        this.classList.toggle('expanded');
        const details = this.querySelector('.inquiry-details');
        if (details) {
          details.style.maxHeight = details.style.maxHeight ? null : details.scrollHeight + 'px';
        }
      });
    });
  }
  initInquiryHistory();

  // ==========================================
  // PROFILE IMAGE UPLOAD PREVIEW
  // ==========================================
  function initImageUpload() {
    document.querySelectorAll('.image-upload input[type="file"]').forEach(input => {
      input.addEventListener('change', function() {
        const preview = this.closest('.image-upload')?.querySelector('.upload-preview');
        if (preview && this.files && this.files[0]) {
          const reader = new FileReader();
          reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
          };
          reader.readAsDataURL(this.files[0]);
        }
      });
    });
  }
  initImageUpload();

  // ==========================================
  // DOCUMENT PREVIEW MODAL
  // ==========================================
  function initDocumentPreview() {
    document.querySelectorAll('.doc-preview-btn').forEach(btn => {
      btn.addEventListener('click', function() {
        const docName = this.getAttribute('data-doc') || 'Document';
        showToast('info', 'Document Preview', `Previewing: ${docName}`);
      });
    });
  }
  initDocumentPreview();

  console.log('✅ Krushi Mitra Buyer Panel initialized successfully');
});
