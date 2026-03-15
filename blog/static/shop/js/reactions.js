import { postAction } from "../../../../static/js/utils.js";

const productSavesElement = document.querySelector("#productSaves");

productSavesElement.addEventListener("click", async (event) => {
  const btnElement = event.target.closest(".js-save-btn");

  if (!btnElement) return;

  const isAuthenticated = productSavesElement.dataset.isAuthenticated === "true";
  if (!isAuthenticated) {
    window.location.href = productSavesElement.dataset.loginUrl;
    return;
  }

  const url = btnElement.dataset.url;
  const data = await postAction(url);

  if (!data) return;

  document.querySelector("#savesCount").textContent = data.saved_count;

  const saveBtnElement = document.querySelector("#saveBtn");
  const saveIconElement = saveBtnElement.querySelector("i");

  if (data.has_saved) {
    saveBtnElement.classList.replace("btn-outline-warning", "btn-warning");
    saveIconElement.classList.replace("bi-bookmark", "bi-bookmark-fill");
  } else {
    saveBtnElement.classList.replace("btn-warning", "btn-outline-warning");
    saveIconElement.classList.replace("bi-bookmark-fill", "bi-bookmark");
  }
});