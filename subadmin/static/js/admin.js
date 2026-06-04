// ── Sidebar toggle (mobile) ──
const sidebar = document.querySelector('.sidebar');
const hamburger = document.getElementById('hamburgerBtn');
if(hamburger && sidebar){
  hamburger.addEventListener('click',()=> sidebar.classList.toggle('open'));
  document.addEventListener('click', e=>{
    if(!sidebar.contains(e.target) && !hamburger.contains(e.target)) sidebar.classList.remove('open');
  });
}

// ── Active nav highlight ──
const currentPage = location.pathname.split('/').pop();
document.querySelectorAll('.nav-item').forEach(link=>{
  if(link.getAttribute('href') === currentPage) link.classList.add('active');
});

// ── Tab switching ──
document.querySelectorAll('.tab-btn').forEach(btn=>{
  btn.addEventListener('click',()=>{
    const group = btn.closest('.tab-group') || document;
    group.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
    group.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));
    btn.classList.add('active');
    const target = btn.dataset.tab;
    const el = document.getElementById(target);
    if(el) el.classList.add('active');
  });
});

// ── Modal helpers ──
function openModal(id){ document.getElementById(id)?.classList.add('open'); }
function closeModal(id){ document.getElementById(id)?.classList.remove('open'); }
document.querySelectorAll('[data-modal-open]').forEach(btn=>{
  btn.addEventListener('click',()=> openModal(btn.dataset.modalOpen));
});
document.querySelectorAll('[data-modal-close]').forEach(btn=>{
  btn.addEventListener('click',()=> closeModal(btn.dataset.modalClose));
});
document.querySelectorAll('.modal-overlay').forEach(overlay=>{
  overlay.addEventListener('click', e=>{ if(e.target===overlay) overlay.classList.remove('open'); });
});

// ── Approve / Reject buttons feedback ──
document.querySelectorAll('.btn-approve').forEach(btn=>{
  btn.addEventListener('click',function(){
    const pill = this.closest('tr')?.querySelector('.status-pill') || this.closest('.kyc-card')?.querySelector('.status-pill') || this.closest('.product-card')?.querySelector('.status-pill');
    if(pill){ pill.className='status-pill approved'; pill.textContent='Approved'; }
    this.closest('.action-btns')?.querySelectorAll('.btn').forEach(b=>b.setAttribute('disabled',''));
    this.closest('.kyc-card-footer')?.querySelectorAll('.btn').forEach(b=>b.setAttribute('disabled',''));
    this.closest('.product-card-footer')?.querySelectorAll('.btn').forEach(b=>b.setAttribute('disabled',''));
  });
});
document.querySelectorAll('.btn-reject').forEach(btn=>{
  btn.addEventListener('click',function(){
    const pill = this.closest('tr')?.querySelector('.status-pill') || this.closest('.kyc-card')?.querySelector('.status-pill') || this.closest('.product-card')?.querySelector('.status-pill');
    if(pill){ pill.className='status-pill rejected'; pill.textContent='Rejected'; }
    this.closest('.action-btns')?.querySelectorAll('.btn').forEach(b=>b.setAttribute('disabled',''));
    this.closest('.kyc-card-footer')?.querySelectorAll('.btn').forEach(b=>b.setAttribute('disabled',''));
    this.closest('.product-card-footer')?.querySelectorAll('.btn').forEach(b=>b.setAttribute('disabled',''));
  });
});

// ── Search filter ──
const searchInput = document.getElementById('searchInput');
if(searchInput){
  searchInput.addEventListener('input',function(){
    const q = this.value.toLowerCase();
    document.querySelectorAll('tbody tr').forEach(row=>{
      row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
    document.querySelectorAll('.kyc-card,.product-card').forEach(card=>{
      card.style.display = card.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
  });
}
