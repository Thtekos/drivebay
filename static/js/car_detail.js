// Car detail page interactions

$(document).ready(function () {

    // Star rating hover and click
    const stars = document.querySelectorAll('.star-btn');
    const ratingInput = document.querySelector('#rating-value');

    if (stars.length > 0) {
        stars.forEach(function (star) {
            star.addEventListener('mouseenter', function () {
                const value = parseInt(this.dataset.value);
                highlightStars(value);
            });

            star.addEventListener('mouseleave', function () {
                const current = parseInt(ratingInput.value);
                highlightStars(current);
            });

            star.addEventListener('click', function () {
                const value = parseInt(this.dataset.value);
                ratingInput.value = value;
                highlightStars(value);
            });
        });
    }

    function highlightStars(value) {
        stars.forEach(function (star) {
            const starValue = parseInt(star.dataset.value);
            if (starValue <= value) {
                star.classList.remove('bi-star');
                star.classList.add('bi-star-fill');
                star.style.color = 'var(--accent)';
            } else {
                star.classList.remove('bi-star-fill');
                star.classList.add('bi-star');
                star.style.color = 'var(--text-muted)';
            }
        });
    }

    // AJAX review submission
    const reviewForm = document.querySelector('#review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const carId = this.dataset.carId;
            const rating = document.querySelector('#rating-value').value;
            const comment = document.querySelector('textarea[name="comment"]').value;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            if (rating === '0') {
                showMessage('#review-message', 'Please select a star rating.', 'danger');
                return;
            }

            $.ajax({
                url: '/cars/' + carId + '/review/',
                method: 'POST',
                data: {
                    rating: rating,
                    comment: comment,
                    csrfmiddlewaretoken: csrfToken,
                },
                success: function (response) {
                    if (response.success) {
                        showMessage('#review-message', 'Review submitted successfully!', 'success');
                        setTimeout(function () { location.reload(); }, 1200);
                    } else {
                        showMessage('#review-message', response.error, 'danger');
                    }
                },
                error: function () {
                    showMessage('#review-message', 'Something went wrong. Please try again.', 'danger');
                }
            });
        });
    }

    // AJAX add to cart
    const cartBtn = document.querySelector('#add-to-cart');
    if (cartBtn) {
        cartBtn.addEventListener('click', function () {
            const carId = this.dataset.carId;
            $.ajax({
                url: '/cart/add/' + carId + '/',
                method: 'POST',
                data: { csrfmiddlewaretoken: getCsrf() },
                success: function (response) {
                    if (response.success) {
                        showMessage('#action-message', 'Added to cart!', 'success');
                    } else {
                        showMessage('#action-message', response.error, 'danger');
                    }
                }
            });
        });
    }

    // AJAX add to wishlist
    const wishlistBtn = document.querySelector('#add-to-wishlist');
    if (wishlistBtn) {
        wishlistBtn.addEventListener('click', function () {
            const carId = this.dataset.carId;
            $.ajax({
                url: '/wishlist/add/' + carId + '/',
                method: 'POST',
                data: { csrfmiddlewaretoken: getCsrf() },
                success: function (response) {
                    if (response.success) {
                        showMessage('#action-message', 'Saved to wishlist!', 'success');
                    } else {
                        showMessage('#action-message', response.error, 'danger');
                    }
                }
            });
        });
    }

    // Helper: show message
    function showMessage(selector, text, type) {
        const el = document.querySelector(selector);
        el.style.display = 'block';
        el.className = 'alert alert-' + type + ' mt-2';
        el.textContent = text;
    }

    // Helper: get CSRF token
    function getCsrf() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

});