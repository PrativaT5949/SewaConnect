const loginForm = document.getElementById("loginForm");

if (loginForm) {
  loginForm.addEventListener("submit", login);
}

async function login(event) {
  event.preventDefault();

  const email = document.getElementById("email").value;

  const password = document.getElementById("password").value;

  try {
    const response = await fetch(API.login, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        email,

        password,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      saveTokens(
        data.access,

        data.refresh,
      );

      alert("Login Successful");

      window.location.href = "customer-dashboard.html";
    } else {
      alert(data.detail || "Invalid Credentials");
    }
  } catch (error) {
    console.error(error);

    alert("Server Error");
  }
}
