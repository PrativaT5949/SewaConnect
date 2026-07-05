const form = document.getElementById("loginForm");

form.addEventListener("submit", async function (e) {
  e.preventDefault();

  const email = document.getElementById("email").value;

  const password = document.getElementById("password").value;

  const errorMessage = document.getElementById("errorMessage");

  errorMessage.style.display = "none";

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

    if (!response.ok) {
      errorMessage.innerText = data.detail || "Login Failed";

      errorMessage.style.display = "block";

      return;
    }

    localStorage.setItem(
      "access",

      data.access,
    );

    localStorage.setItem(
      "refresh",

      data.refresh,
    );

    alert("Login Successful");
    const userResponse = await fetch(API.me, {
      headers: {
        Authorization: `Bearer ${data.access}`,
      },
    });

    const user = await userResponse.json();

    localStorage.setItem("user", JSON.stringify(user));

    if (user.role === "CUSTOMER") {
      window.location.href = "customer-dashboard.html";
    } else if (user.role === "PROVIDER") {
      window.location.href = "provider-dashboard.html";
    } else {
      window.location.href = "../index.html";
    }
  } catch (error) {
    errorMessage.innerText = "Unable to connect to server.";

    errorMessage.style.display = "block";
  }
});
