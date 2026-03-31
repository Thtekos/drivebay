// Cart page interactions

$(document).ready(function () {

    // Remove item from cart
    document.querySelectorAll('.remove-from-cart').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const carId = this.dataset.carId;
            const cartItem = document.querySelector('#cart-item-' + carId);

            $.ajax({
                url: '/cart/remove/' + carId + '/',
                method: 'POST',
                data: { csrfmiddlewaretoken: getCsrf() },
                success: function (response) {
                    if (response.success) {

                        // Animate and remove the item
                        cartItem.style.transition = 'opacity 0.3s ease';
                        cartItem.style.opacity = '0';
                        setTimeout(function () {
                            cartItem.remove();

                            // Update totals
                            document.querySelector('#cart-count-display').textContent = response.cart_count;
                            document.querySelector('#cart-total-display').textContent = '€' + response.total;

                            // Update navbar badge
                            updateNavCartBadge(response.cart_count);

                            // Show empty state if no items left
                            if (response.cart_count === 0) {
                                location.reload();
                            }
                        }, 300);
                    }
                },
                error: function () {
                    showMessage('#cart-message', 'Something went wrong.', 'danger');
                }
            });
        });
    });

    // Update navbar cart badge
    function updateNavCartBadge(count) {
        const badge = document.querySelector('.navbar .badge');
        if (count > 0) {
            if (badge) {
                badge.textContent = count;
            }
        } else {
            if (badge) badge.remove();
        }
    }

    // Helper: get CSRF token
    function getCsrf() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    // Helper: show message
    function showMessage(selector, text, type) {
        const el = document.querySelector(selector);
        el.style.display = 'block';
        el.className = 'alert alert-' + type + ' mt-2';
        el.textContent = text;
    }

});