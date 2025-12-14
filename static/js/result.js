// 🌟 Dynamic Medical Report Page

document.addEventListener("DOMContentLoaded", () => {
  // Fade-in animation for summary card
  const summaryCard = document.querySelector(".summary");
  if (summaryCard) {
    summaryCard.style.opacity = "0";
    setTimeout(() => {
      summaryCard.style.transition = "opacity 1s ease-in-out";
      summaryCard.style.opacity = "1";
    }, 200);
  }

  // 🔍 Highlight important medical keywords
  const keywords = ["Disease", "Causes", "Prevention", "Recommendations", "Precautions", "Diet", "Drinks"];
  const summaryText = document.querySelector(".summary pre");
  if (summaryText) {
    let html = summaryText.innerHTML;
    keywords.forEach(word => {
      const regex = new RegExp(`(${word})`, "gi");
      html = html.replace(regex, `<span class="highlight">$1</span>`);
    });
    summaryText.innerHTML = html;
  }

  // 🌙 Dark mode toggle
  const darkModeBtn = document.createElement("button");
  darkModeBtn.innerText = "🌙 Toggle Dark Mode";
  darkModeBtn.classList.add("btn");
  document.querySelector("footer")?.appendChild(darkModeBtn);

  darkModeBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
  });
});
