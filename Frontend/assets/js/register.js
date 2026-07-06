const togglePass = document.getElementById("togglePass");
const passInput = document.getElementById("passInput");
togglePass.addEventListener("click", () => {
  passInput.type = passInput.type === "password" ? "text" : "password";
});

const bars = document.querySelectorAll(".pass-strength span");
const colors = ["#EF4444", "#F59E0B", "#F59E0B", "#22C55E"];
passInput.addEventListener("input", () => {
  const val = passInput.value;
  let score = 0;
  if (val.length > 5) score++;
  if (val.length > 9) score++;
  if (/[A-Z]/.test(val) && /[0-9]/.test(val)) score++;
  if (/[^A-Za-z0-9]/.test(val)) score++;
  bars.forEach((bar, i) => {
    bar.style.background =
      i < score ? colors[Math.min(score - 1, 3)] : "#E2E8F0";
  });
});
