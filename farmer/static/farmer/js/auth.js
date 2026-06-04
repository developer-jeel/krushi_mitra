// ── Helper: show or hide error ──
function showError(id, show) {
  var el = document.getElementById(id);
  if (show) {
    el.classList.add('show');
  } else {
    el.classList.remove('show');
  }
}


// ══════════════════════════════
//  LOGIN PAGE
// ══════════════════════════════
if (document.getElementById('loginForm')) {

  // Aadhar auto-format (XXXX XXXX XXXX)
  var aadharInput = document.getElementById('aadhar');
  aadharInput.addEventListener('input', function () {
    var digits = aadharInput.value.replace(/\D/g, '').slice(0, 12);
    aadharInput.value = digits.replace(/(\d{4})(?=\d)/g, '$1 ');
    showError('aadharErr', false);
  });

  // Password clear error on type
  document.getElementById('password').addEventListener('input', function () {
    showError('passErr', false);
  });

  // Login form submit
  document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();

    var aadhar   = aadharInput.value.replace(/\s/g, '');
    var password = document.getElementById('password').value;
    var valid    = true;

    if (!/^\d{12}$/.test(aadhar)) {
      showError('aadharErr', true);
      valid = false;
    }

    if (password.length < 6) {
      showError('passErr', true);
      valid = false;
    }

    if (valid) {
      var btn = document.getElementById('loginBtn');
      btn.disabled    = true;
      btn.textContent = 'Logging in...';
      setTimeout(function () {
        alert('Login successful!');
        btn.disabled    = false;
        btn.textContent = 'Login';
      }, 1500);
    }
  });
}


// ══════════════════════════════
//  REGISTER PAGE
// ══════════════════════════════
if (document.getElementById('registerForm')) {

  var aadharGroup  = document.getElementById('aadharGroup');
  var gstGroup     = document.getElementById('gstGroup');
  var roleFarmer   = document.getElementById('roleFarmer');
  var roleBuyer    = document.getElementById('roleBuyer');
  var cardFarmer   = document.querySelector('label[for="roleFarmer"]');
  var cardBuyer    = document.querySelector('label[for="roleBuyer"]');

  // ── Update card visual state ──
  function updateRoleCards() {
    cardFarmer.classList.toggle('selected', roleFarmer.checked);
    cardBuyer.classList.toggle('selected',  roleBuyer.checked);
  }

  // ── Role radio toggle ──
  function handleRoleChange() {
    showError('roleErr', false);
    updateRoleCards();
    if (roleFarmer.checked) {
      aadharGroup.style.display = 'block';
      gstGroup.style.display    = 'none';
      document.getElementById('gst').value = '';
      showError('gstErr', false);
    } else if (roleBuyer.checked) {
      gstGroup.style.display    = 'block';
      aadharGroup.style.display = 'none';
      document.getElementById('aadhar').value = '';
      showError('aadharErr', false);
    }
  }

  roleFarmer.addEventListener('change', handleRoleChange);
  roleBuyer.addEventListener('change',  handleRoleChange);

  // Also allow clicking the card label to trigger radio
  cardFarmer.addEventListener('click', function () {
    roleFarmer.checked = true;
    handleRoleChange();
  });
  cardBuyer.addEventListener('click', function () {
    roleBuyer.checked = true;
    handleRoleChange();
  });

  // ── Aadhar auto-format ──
  var aadharReg = document.getElementById('aadhar');
  aadharReg.addEventListener('input', function () {
    var digits = aadharReg.value.replace(/\D/g, '').slice(0, 12);
    aadharReg.value = digits.replace(/(\d{4})(?=\d)/g, '$1 ');
    showError('aadharErr', false);
  });

  // ── GST uppercase ──
  var gstInput = document.getElementById('gst');
  gstInput.addEventListener('input', function () {
    gstInput.value = gstInput.value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 15);
    showError('gstErr', false);
  });

  // ── Contact: digits only ──
  var contactInput = document.getElementById('contact');
  contactInput.addEventListener('input', function () {
    contactInput.value = contactInput.value.replace(/\D/g, '').slice(0, 10);
    showError('contactErr', false);
  });

  // ── Clear errors on typing ──
  document.getElementById('name').addEventListener('input',      function () { showError('nameErr',    false); });
  document.getElementById('password').addEventListener('input',  function () { showError('passErr',    false); });
  document.getElementById('confirmPw').addEventListener('input', function () { showError('confirmErr', false); });

  // ── Register form submit ──
  document.getElementById('registerForm').addEventListener('submit', function (e) {
    e.preventDefault();

    var name      = document.getElementById('name').value.trim();
    var contact   = contactInput.value.trim();
    var password  = document.getElementById('password').value;
    var confirmPw = document.getElementById('confirmPw').value;
    var valid     = true;

    if (name.length < 2) {
      showError('nameErr', true);
      valid = false;
    }

    if (!/^\d{10}$/.test(contact)) {
      showError('contactErr', true);
      valid = false;
    }

    // Role validation
    if (!roleFarmer.checked && !roleBuyer.checked) {
      showError('roleErr', true);
      valid = false;
    } else if (roleFarmer.checked) {
      var aadhar = aadharReg.value.replace(/\s/g, '');
      if (!/^\d{12}$/.test(aadhar)) {
        showError('aadharErr', true);
        valid = false;
      }
    } else if (roleBuyer.checked) {
      var gst = gstInput.value.trim();
      if (!/^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/.test(gst)) {
        showError('gstErr', true);
        valid = false;
      }
    }

    if (password.length < 6) {
      showError('passErr', true);
      valid = false;
    }

    if (password !== confirmPw) {
      showError('confirmErr', true);
      valid = false;
    }

    if (valid) {
      var btn = document.getElementById('registerBtn');
      btn.disabled    = true;
      btn.textContent = 'Creating account...';
      setTimeout(function () {
        alert('Account created! Redirecting to login...');
        window.location.href = 'login.html';
      }, 1500);
    }
  });
}
