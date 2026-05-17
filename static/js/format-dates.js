export function formatDate(el) {

  const isoDate = el.dataset.date;

  if (!isoDate) return;

  el.textContent = new Date(isoDate).toLocaleString();
}

document.querySelectorAll(".date-field").forEach(el => {
  formatDate(el);
});