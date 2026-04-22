// Global DriveBay interactions - runs on every page

$(document).ready(function () {

    // Update navbar cart badge
    window.updateNavCartBadge = function (count) {
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
    };

});