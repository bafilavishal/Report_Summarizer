document.addEventListener("DOMContentLoaded", function () {
  console.log("MediEase website loaded!");

  const loginBtn = document.getElementById("login-btn");
  const userInfo = document.getElementById("user-info");
  const userPic = document.getElementById("user-pic");
  const userName = document.getElementById("user-name");
  const logoutBtn = document.getElementById("logout-btn");
  const uploadForm = document.getElementById("upload-form");

  // 🧠 Initialize Google Sign-In button
  window.onload = function () {
    if (window.google) {
      google.accounts.id.initialize({
        client_id: "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com", // ← replace this
        callback: handleCredentialResponse,
      });

      google.accounts.id.renderButton(loginBtn, {
        theme: "outline",
        size: "medium",
        text: "signin_with",
      });
    } else {
      console.error("Google Sign-In script not loaded!");
    }
  };

  // 🧾 Handle login
  function handleCredentialResponse(response) {
    const data = parseJwt(response.credential);
    console.log("User Info:", data);

    loginBtn.style.display = "none";
    userInfo.style.display = "flex";
    userPic.src = data.picture;
    userName.textContent = data.name;

    // Allow uploads only after login
    uploadForm.style.display = "block";
  }

  // 🔒 Logout
  document.addEventListener("DOMContentLoaded", () => {
  const loginBtn = document.getElementById("loginBtn");
  const signupBtn = document.getElementById("signupBtn");

  if (loginBtn) {
    loginBtn.addEventListener("click", handleLogin);
  }

  if (signupBtn) {
    signupBtn.addEventListener("click", handleSignup);
  }
});

  // 🔍 Decode JWT
  function parseJwt(token) {
    try {
      const base64Url = token.split(".")[1];
      const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split("")
          .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
          .join("")
      );
      return JSON.parse(jsonPayload);
    } catch (e) {
      console.error("Invalid token", e);
      return {};
    }
  }

  // Hide form by default (until user logs in)
document.addEventListener("DOMContentLoaded", () => {
  const loadingScreen = document.getElementById("loadingScreen");
  if (loadingScreen) {
    loadingScreen.style.display = "none";  // or whatever you need
  }
});

});
