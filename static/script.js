document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const pwd = document.getElementById("pwd").value;
  const label = document.getElementById("label");
  const fill = document.getElementById("meter-fill");

  if (!pwd) {
    label.textContent = "Please enter a password.";
    return;
  }

  const res = await fetch("/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password: pwd }),
  });
  const data = await res.json();

  document.getElementById("entropy").textContent = data.entropy;
  document.getElementById("crack").textContent = data.crack_time;
  document.getElementById("details").classList.remove("hidden");

  const strengthColors = {
    "Very Weak": "#ef4444",
    "Weak": "#f97316",
    "Moderate": "#facc15",
    "Strong": "#22c55e",
    "Very Strong": "#16a34a",
  };

  fill.style.width = `${Math.min(data.entropy, 100)}%`;
  fill.style.background = strengthColors[data.strength_label] || "#64748b";
  label.textContent = data.strength_label;
});
// Show / hide password toggle
document.getElementById("togglePwd").addEventListener("click", () => {
  const pwdInput = document.getElementById("pwd");
  const toggleBtn = document.getElementById("togglePwd");
  if (pwdInput.type === "password") {
    pwdInput.type = "text";
    toggleBtn.textContent = "🙈";
  } else {
    pwdInput.type = "password";
    toggleBtn.textContent = "👁️";
  }
});
