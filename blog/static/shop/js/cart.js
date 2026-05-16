function getCookie(name) {
  let cookieValue = null;

  if (document.cookie && document.cookie !== '') {

    const cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {

      const cookie = cookies[i].trim();

      if (cookie.substring(0, name.length + 1) === (name + '=')) {

        cookieValue = decodeURIComponent(
          cookie.substring(name.length + 1)
        );

        break;
      }
    }
  }

  return cookieValue;
}


document.addEventListener('click', async (event) => {

  // ADD TO CART
  if (event.target.closest('.add-to-cart-btn')) {

    const btn = event.target.closest('.add-to-cart-btn');

    const isAuthenticated =
      btn.dataset.isAuthenticated === 'true';

    if (!isAuthenticated) {
      window.location.href = btn.dataset.loginUrl;
      return;
    }

    const productId = btn.dataset.productId;

    try {

      const response = await fetch(`/products/add/${productId}/`, {

        method: 'POST',

        headers: {
          'X-CSRFToken': getCookie('csrftoken')
        }

      });

      const data = await response.json();

      if (data.success) {
        btn.textContent =
          `В корзине (${data.quantity})`;
      }

    } catch (error) {

      console.error(error);

    }
  }


  // PLUS
  if (event.target.closest('.plus-btn')) {

    const btn = event.target.closest('.plus-btn');

    const productId = btn.dataset.productId;

    const response = await fetch(`/products/add/${productId}/`, {

      method: 'POST',

      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }

    });

    const data = await response.json();

    btn.closest('.quantity-controls').querySelector('.quantity')
      .textContent = data.quantity;
  }


  // MINUS
  if (event.target.closest('.minus-btn')) {

    const btn = event.target.closest('.minus-btn');

    const productId = btn.dataset.productId;

    const response = await fetch(`/products/remove/${productId}/`, {

      method: 'POST',

      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }

    });

    const data = await response.json();

    if (data.quantity > 0) {

      btn.closest('.quantity-controls').querySelector('.quantity')
        .textContent = data.quantity;

    } else {

      btn.closest('.cart-item').remove();

    }
  }

// DELETE ITEM
  if (event.target.closest('.remove-cart-item-btn')) {

      const btn =
        event.target.closest('.remove-cart-item-btn');

      const productId = btn.dataset.productId;

      const response = await fetch(
        `/products/delete/${productId}/`,
        {
          method: 'POST',

          headers: {
            'X-CSRFToken': getCookie('csrftoken')
          }
        }
      );

      const data = await response.json();

      if (data.success) {

        btn.closest('.cart-item').remove();

        const remainingItems =
          document.querySelectorAll('.cart-item');

        if (remainingItems.length === 0) {

          document.querySelector('.container').innerHTML =
            '<p class="text-center">Корзина пуста.</p>';
        }
      }
  }
});