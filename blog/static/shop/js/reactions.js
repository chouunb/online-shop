import { postAction } from "../../../../static/js/utils.js";
import { formatDate } from "../../../../static/js/format-dates.js";

document.addEventListener('DOMContentLoaded', () => {

  const reviewFormElement = document.getElementById('reviewForm');

  if (!reviewFormElement) return;

  reviewFormElement.addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const url = this.dataset.addReviewUrl;

    const reviewErrorsElement =
      document.getElementById('reviewErrors');

    reviewErrorsElement.classList.add('d-none');
    reviewErrorsElement.textContent = '';

    try {
      const data = await postAction(url, formData);

      if (!data) {
        reviewErrorsElement.textContent =
          'Ошибка сервера';

        reviewErrorsElement.classList.remove('d-none');

        return;
      }
      if (data.success) {

        this.querySelector('textarea').value = '';

        const reviewsListElement =
          document.getElementById('reviewsList');

        const emptyMessageElement =
          reviewsListElement.querySelector('#emptyMessage');

        if (emptyMessageElement) {
          emptyMessageElement.remove();
        }

        reviewsListElement.insertAdjacentHTML(
          'afterbegin',
          data.review_html
        );

        const newReviewElement =
          reviewsListElement.firstElementChild;

        const dateElement =
          newReviewElement.querySelector('.date-field');

        // УВЕЛИЧИВАЕМ offset на 1, так как добавили новый отзыв
        window.reviewsBatchLoader.offset += 1;

        if (dateElement) {
          formatDate(dateElement);
        }

        const reviewsTitleElement =
          document.querySelector('#reviewsTitle');

        reviewsTitleElement.textContent =
          `Отзывы (${data.reviews_count})`;

      } else {

        reviewErrorsElement.textContent = data.error;
        reviewErrorsElement.classList.remove('d-none');

      }

    } catch (error) {

      console.error('Ошибка при добавлении отзыва:', error);

      reviewErrorsElement.textContent =
        'Произошла ошибка при отправке отзыва';

      reviewErrorsElement.classList.remove('d-none');
    }
  });
});