const form = document.getElementById("loan-form");
const btn = document.getElementById("predict-btn");
const btnLabel = document.getElementById("predict-btn-label");
const resultSection = document.getElementById("result-section");
const resultIconWrap = document.getElementById("result-icon-wrap");
const resultIcon = document.getElementById("result-icon");
const resultTitle = document.getElementById("result-title");
const resultPct = document.getElementById("result-pct");
const resultBar = document.getElementById("result-bar");
const resultDesc = document.getElementById("result-desc");
const errorMessage = document.getElementById("error-message");
const loanAmntInput = document.getElementById("loan_amnt");
const incomeInput = document.getElementById("person_income");
const ratioValue = document.getElementById("ratio-value");

function updateRatio() {
  const income = parseFloat(incomeInput.value) || 0;
  const amnt = parseFloat(loanAmntInput.value) || 0;
  const ratio = income > 0 ? (amnt / income) * 100 : 0;
  ratioValue.textContent = ratio.toFixed(1) + "%";
}
loanAmntInput.addEventListener("input", updateRatio);
incomeInput.addEventListener("input", updateRatio);
updateRatio();

function animateCount(el, target, durationMs) {
  const start = performance.now();
  function step(ts) {
    const progress = Math.min((ts - start) / durationMs, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(eased * target);
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorMessage.style.display = "none";
  btn.disabled = true;
  btnLabel.textContent = "Predicting...";

  const payload = {
    person_age: document.getElementById("person_age").value,
    person_gender: document.getElementById("person_gender").value,
    person_education: document.getElementById("person_education").value,
    person_income: document.getElementById("person_income").value,
    person_emp_exp: document.getElementById("person_emp_exp").value,
    person_home_ownership: document.getElementById("person_home_ownership").value,
    loan_amnt: document.getElementById("loan_amnt").value,
    loan_intent: document.getElementById("loan_intent").value,
    loan_int_rate: document.getElementById("loan_int_rate").value,
    cb_person_cred_hist_length: document.getElementById("cb_person_cred_hist_length").value,
    credit_score: document.getElementById("credit_score").value,
    previous_loan_defaults_on_file: document.getElementById("previous_loan_defaults_on_file").value,
  };

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Prediction failed");
    }

    const probPct = Math.round((data.probability ?? (data.approved ? 1 : 0)) * 100);

    if (data.approved) {
      resultIconWrap.style.background = "#eaf3de";
      resultIcon.style.color = "#27500a";
      resultIcon.textContent = "check_circle";
      resultTitle.textContent = "Likely approved";
      resultTitle.style.color = "#27500a";
      resultBar.style.background = "#3b6d11";
      resultDesc.textContent = "Based on current credit analysis and loan-to-income ratios, this profile meets typical institutional thresholds.";
    } else {
      resultIconWrap.style.background = "#ffdad6";
      resultIcon.style.color = "#93000a";
      resultIcon.textContent = "cancel";
      resultTitle.textContent = "Likely rejected";
      resultTitle.style.color = "#ba1a1a";
      resultBar.style.background = "#ba1a1a";
      resultDesc.textContent = "Based on current credit analysis and loan-to-income ratios, the risk profile exceeds typical institutional thresholds.";
    }

    resultSection.style.display = "flex";

    resultPct.textContent = "0";
    resultBar.style.width = "0%";
    requestAnimationFrame(() => {
      resultBar.style.width = probPct + "%";
    });
    animateCount(resultPct, probPct, 900);

    resultSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
  } catch (err) {
    errorMessage.textContent = err.message;
    errorMessage.style.display = "block";
  } finally {
    btn.disabled = false;
    btnLabel.textContent = "Predict Loan Approval";
  }
});
