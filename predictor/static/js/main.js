/* Cancer Risk Intelligence System - Main JavaScript Engine */

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initBackToTop();
  initFormSliders();
  initWizardSteps();
  initToastMessages();
});

/* Theme Toggle */
function initThemeToggle() {
  const toggleBtn = document.getElementById('themeToggleBtn');
  if (!toggleBtn) return;

  const currentTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-bs-theme', currentTheme);
  updateThemeIcon(currentTheme);

  toggleBtn.addEventListener('click', () => {
    const activeTheme = document.documentElement.getAttribute('data-bs-theme');
    const newTheme = activeTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
  });
}

function updateThemeIcon(theme) {
  const icon = document.getElementById('themeToggleIcon');
  if (!icon) return;
  if (theme === 'dark') {
    icon.className = 'fas fa-sun text-warning';
  } else {
    icon.className = 'fas fa-moon text-primary';
  }
}

/* Back to Top */
function initBackToTop() {
  const btn = document.getElementById('backToTopBtn');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

/* Toast Messages */
function initToastMessages() {
  const toastElList = [].slice.call(document.querySelectorAll('.toast'));
  toastElList.forEach((toastEl) => {
    const toast = new bootstrap.Toast(toastEl, { delay: 5000 });
    toast.show();
  });
}

/* Range Sliders Sync */
function initFormSliders() {
  syncSliderInput('ageSlider', 'ageInput', 'ageVal');
  syncSliderInput('bmiSlider', 'bmiInput', 'bmiVal', updateBMIBadge);
  syncSliderInput('tumorSlider', 'tumorInput', 'tumorVal');
  syncSliderInput('survivalSlider', 'survivalInput', 'survivalVal');
}

function syncSliderInput(sliderId, inputId, displayId, callback) {
  const slider = document.getElementById(sliderId);
  const input = document.getElementById(inputId);
  const display = document.getElementById(displayId);

  if (!slider || !input) return;

  slider.addEventListener('input', (e) => {
    const val = e.target.value;
    input.value = val;
    if (display) display.textContent = val;
    if (callback) callback(val);
  });

  input.addEventListener('input', (e) => {
    const val = e.target.value;
    slider.value = val;
    if (display) display.textContent = val;
    if (callback) callback(val);
  });
}

function updateBMIBadge(bmiVal) {
  const badge = document.getElementById('bmiStatusBadge');
  if (!badge) return;
  const bmi = parseFloat(bmiVal);
  if (isNaN(bmi)) return;

  if (bmi < 18.5) {
    badge.className = 'badge bg-info ms-2';
    badge.textContent = 'Underweight';
  } else if (bmi <= 24.9) {
    badge.className = 'badge bg-success ms-2';
    badge.textContent = 'Normal';
  } else if (bmi <= 29.9) {
    badge.className = 'badge bg-warning text-dark ms-2';
    badge.textContent = 'Overweight';
  } else {
    badge.className = 'badge bg-danger ms-2';
    badge.textContent = 'Obese';
  }
}

/* Multi-Step Prediction Wizard */
let currentStep = 1;

function initWizardSteps() {
  const form = document.getElementById('predictionForm');
  if (!form) return;

  showStep(currentStep);

  form.addEventListener('submit', (e) => {
    showLoadingOverlay();
  });
}

function navigateStep(direction) {
  const totalSteps = 4;
  const nextStep = currentStep + direction;

  if (direction > 0 && !validateCurrentStep(currentStep)) {
    return;
  }

  if (nextStep >= 1 && nextStep <= totalSteps) {
    currentStep = nextStep;
    showStep(currentStep);
  }
}

function showStep(stepNum) {
  const steps = document.querySelectorAll('.wizard-section');
  if (!steps.length) return;

  steps.forEach((el, index) => {
    if (index + 1 === stepNum) {
      el.classList.remove('d-none');
    } else {
      el.classList.add('d-none');
    }
  });

  // Update wizard icons
  for (let i = 1; i <= 4; i++) {
    const stepIcon = document.getElementById(`step-icon-${i}`);
    if (!stepIcon) continue;

    if (i === stepNum) {
      stepIcon.className = 'wizard-step active';
    } else if (i < stepNum) {
      stepIcon.className = 'wizard-step completed';
      stepIcon.innerHTML = '<i class="fas fa-check"></i>';
    } else {
      stepIcon.className = 'wizard-step';
      stepIcon.textContent = i;
    }
  }

  // Progress Bar
  const progressBar = document.getElementById('wizardProgressBar');
  if (progressBar) {
    const pct = ((stepNum - 1) / 3) * 100;
    progressBar.style.width = `${pct}%`;
  }

  // Prev / Next Button states
  const prevBtn = document.getElementById('wizardPrevBtn');
  const nextBtn = document.getElementById('wizardNextBtn');
  const submitBtn = document.getElementById('wizardSubmitBtn');

  if (prevBtn) prevBtn.style.display = stepNum === 1 ? 'none' : 'inline-block';
  if (nextBtn) nextBtn.style.display = stepNum === 4 ? 'none' : 'inline-block';
  if (submitBtn) submitBtn.style.display = stepNum === 4 ? 'inline-block' : 'none';
}

function validateCurrentStep(stepNum) {
  const currentSection = document.getElementById(`step-section-${stepNum}`);
  if (!currentSection) return true;

  const inputs = currentSection.querySelectorAll('input[required], select[required]');
  let valid = true;

  inputs.forEach((input) => {
    if (!input.checkValidity()) {
      input.classList.add('is-invalid');
      valid = false;
    } else {
      input.classList.remove('is-invalid');
    }
  });

  if (!valid) {
    alert('Please fill out all required fields in this step before proceeding.');
  }
  return valid;
}

function showLoadingOverlay() {
  const overlay = document.getElementById('scannerOverlay');
  if (overlay) {
    overlay.classList.remove('d-none');
  }
}

/* History Page CSV Export & Filter */
function filterHistoryTable() {
  const searchInput = document.getElementById('historySearchInput');
  const filterSelect = document.getElementById('historyRiskFilter');
  const table = document.getElementById('historyTable');

  if (!table) return;

  const query = searchInput ? searchInput.value.toLowerCase() : '';
  const filterRisk = filterSelect ? filterSelect.value.toLowerCase() : 'all';

  const rows = table.querySelectorAll('tbody tr');

  rows.forEach((row) => {
    const text = row.textContent.toLowerCase();
    const riskAttr = row.getAttribute('data-risk') || '';

    const matchesSearch = text.includes(query);
    const matchesFilter = filterRisk === 'all' || riskAttr.toLowerCase() === filterRisk;

    if (matchesSearch && matchesFilter) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}

function exportHistoryCSV() {
  const table = document.getElementById('historyTable');
  if (!table) return;

  let csv = [];
  const rows = table.querySelectorAll('tr');

  rows.forEach((row) => {
    const cols = row.querySelectorAll('th, td');
    let rowData = [];
    cols.forEach((col, idx) => {
      // Exclude actions column (last column)
      if (idx < cols.length - 1) {
        let text = col.innerText.replace(/"/g, '""').trim();
        rowData.push(`"${text}"`);
      }
    });
    if (rowData.length) csv.push(rowData.join(','));
  });

  const csvString = csv.join('\n');
  const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', 'cancer_risk_prediction_history.csv');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

/* Real-time Height & Weight to BMI Calculator for Risk Assessment Module */
document.addEventListener('DOMContentLoaded', () => {
  initRiskAssessmentBMICalculator();
  initCounterAnimation();
});

function initRiskAssessmentBMICalculator() {
  const heightInput = document.getElementById('id_height_cm');
  const weightInput = document.getElementById('id_weight_kg');
  const bmiDisplay = document.getElementById('bmiCalcDisplay');
  const bmiCategoryBadge = document.getElementById('bmiCategoryBadge');
  const autoBmiValHidden = document.getElementById('id_bmi_auto_val');

  if (!heightInput || !weightInput) return;

  function calculate() {
    const h = parseFloat(heightInput.value);
    const w = parseFloat(weightInput.value);

    if (h > 0 && w > 0) {
      const heightM = h / 100;
      const bmi = w / (heightM * heightM);
      const roundedBMI = bmi.toFixed(1);

      if (bmiDisplay) bmiDisplay.textContent = roundedBMI;
      if (autoBmiValHidden) autoBmiValHidden.value = roundedBMI;

      if (bmiCategoryBadge) {
        if (bmi < 18.5) {
          bmiCategoryBadge.className = 'badge bg-info text-white ms-2';
          bmiCategoryBadge.textContent = 'Underweight';
        } else if (bmi <= 24.9) {
          bmiCategoryBadge.className = 'badge bg-success text-white ms-2';
          bmiCategoryBadge.textContent = 'Normal Weight';
        } else if (bmi <= 29.9) {
          bmiCategoryBadge.className = 'badge bg-warning text-dark ms-2';
          bmiCategoryBadge.textContent = 'Overweight';
        } else {
          bmiCategoryBadge.className = 'badge bg-danger text-white ms-2';
          bmiCategoryBadge.textContent = 'Obese';
        }
      }
    }
  }

  heightInput.addEventListener('input', calculate);
  weightInput.addEventListener('input', calculate);
  calculate();
}

/* Animated Counters */
function initCounterAnimation() {
  const counters = document.querySelectorAll('.counter-animate');
  if (!counters.length) return;

  counters.forEach((counter) => {
    const target = parseFloat(counter.getAttribute('data-target') || counter.textContent);
    if (isNaN(target)) return;

    let start = 0;
    const duration = 1200;
    const stepTime = 20;
    const steps = duration / stepTime;
    const increment = target / steps;

    const timer = setInterval(() => {
      start += increment;
      if (start >= target) {
        counter.textContent = Number.isInteger(target) ? target : target.toFixed(1);
        clearInterval(timer);
      } else {
        counter.textContent = Number.isInteger(target) ? Math.floor(start) : start.toFixed(1);
      }
    }, stepTime);
  });
}

