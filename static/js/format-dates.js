export function formatDate(el) {

  const isoDate = el.dataset.date;

  if (!isoDate) return;

  el.textContent = new Date(isoDate).toLocaleString();
}

export function formatDatesInHTML(htmlString) {
  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = htmlString;
  
  tempDiv.querySelectorAll(".date-field").forEach(el => {
    formatDate(el);
  });
  
  return tempDiv.innerHTML;
}

document.querySelectorAll(".date-field").forEach(el => {
  formatDate(el);
});


