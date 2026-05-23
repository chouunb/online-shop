import { postAction } from "../../../../static/js/utils.js";
import { formatDate } from "../../../../static/js/format-dates.js";

document.addEventListener('DOMContentLoaded', () => {

  // Форма добавления отзыва
  const reviewFormElement =
    document.getElementById('reviewForm');

  if (!reviewFormElement) return;

  reviewFormElement.addEventListener(
    'submit',
    async function(event) {

      event.preventDefault();

      const formData = new FormData(this);
      const url = this.dataset.addReviewUrl;

      // Блок ошибок
      const reviewErrorsElement =
        document.getElementById('reviewErrors');

      reviewErrorsElement.classList.add('d-none');
      reviewErrorsElement.textContent = '';

      try {

        const data = await postAction(url, formData);

        // Ошибка сервера
        if (!data) {

          reviewErrorsElement.textContent =
            'Ошибка сервера';

          reviewErrorsElement.classList.remove('d-none');

          return;
        }

        // Успешное добавление
        if (data.success) {

          // Очищаем textarea
          this.querySelector('textarea').value = '';

          // Контейнер с отзывами
          const reviewsContainerElement =
            document.getElementById('reviewsContainer');

          // Сообщение "нет отзывов"
          const emptyMessageElement =
            document.getElementById('emptyMessage');

          if (emptyMessageElement) {
            emptyMessageElement.remove();
          }

          // Добавляем новый отзыв В НАЧАЛО
          reviewsContainerElement.insertAdjacentHTML(
            'afterbegin',
            data.review_html
          );

          // Новый отзыв
          const newReviewElement =
            reviewsContainerElement.firstElementChild;

          // Форматирование даты
          const dateElement =
            newReviewElement.querySelector('.date-field');

          if (dateElement) {
            formatDate(dateElement);
          }

          // Обновляем количество отзывов
          const reviewsTitleElement =
            document.getElementById('reviewsTitle');

          if (reviewsTitleElement) {

            reviewsTitleElement.textContent =
              `Отзывы (${data.reviews_count})`;
          }

          // Увеличиваем offset batch loader
          if (window.reviewsBatchLoader) {

            window.reviewsBatchLoader.offset += 1;
          }

        } else {

          // Ошибки формы
          reviewErrorsElement.textContent =
            data.error;

          reviewErrorsElement.classList.remove('d-none');
        }

      } catch (error) {

        console.error(
          'Ошибка при добавлении отзыва:',
          error
        );

        reviewErrorsElement.textContent =
          'Произошла ошибка при отправке отзыва';

        reviewErrorsElement.classList.remove('d-none');
      }
    }
  );
});