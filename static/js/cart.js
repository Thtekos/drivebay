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
                        cartItem.style.transition = 'opacity 0.3s ease';
                        cartItem.style.opacity = '0';
                        setTimeout(function () {
                            cartItem.remove();
                            document.querySelector('#cart-count-display').textContent = response.cart_count;
                            document.querySelector('#cart-total-display').textContent = '€' + response.total;
                            window.updateNavCartBadge(response.cart_count);
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
        const cartLink = document.querySelector('.navbar a[href="/cart/"]');
        if (!cartLink) return;
        let badge = cartLink.querySelector('.badge');
        if (count > 0) {
            if (badge) {
                badge.textContent = count;
            } else {
                badge = document.createElement('span');
                badge.className = 'badge bg-warning text-dark ms-1';
                badge.textContent = count;
                cartLink.appendChild(badge);
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
        if (!el) return;
        el.style.display = 'block';
        el.className = 'alert alert-' + type + ' mt-2';
        el.textContent = text;
    }

});