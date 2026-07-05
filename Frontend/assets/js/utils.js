function saveTokens(access, refresh) {
  localStorage.setItem("access", access);
  localStorage.setItem("refresh", refresh);
}

function getAccessToken() {
  return localStorage.getItem("access");
}

function logout() {
  localStorage.clear();

  window.location.href = "../pages/login.html";
}

function authHeaders() {
  return {
    "Content-Type": "application/json",

    Authorization: `Bearer ${getAccessToken()}`,
  };
}
