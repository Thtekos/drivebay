// Checkout page interactions

$(document).ready(function () {

    // Format card number with spaces every 4 digits
    const cardNumber = document.querySelector('#card-number');
    if (cardNumber) {
        cardNumber.addEventListener('input', function () {
            let value = this.value.replace(/\D/g, '');
            value = value.replace(/(.{4})/g, '$1 ').trim();
            this.value = value;
        });
    }

    // Format expiry date with slash
    const expiryDate = document.querySelector('#expiry-date');
    if (expiryDate) {
        expiryDate.addEventListener('input', function () {
            let value = this.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.substring(0, 2) + '/' + value.substring(2);
            }
            this.value = value;
        });
    }

    // Allow only numbers in CVV
    const cvv = document.querySelector('#cvv');
    if (cvv) {
        cvv.addEventListener('input', function () {
            this.value = this.value.replace(/\D/g, '');
        });
    }

    // Client side validation before submit
    const checkoutForm = document.querySelector('#checkout-form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function (e) {
            const cardNum = document.querySelector('#card-number').value.replace(/\s/g, '');
            const expiry = document.querySelector('#expiry-date').value;
            const cvvVal = document.querySelector('#cvv').value;

            if (cardNum.length !== 16) {
                e.preventDefault();
                alert('Please enter a valid 16-digit card number.');
                return;
            }
            if (!/^\d{2}\/\d{2}$/.test(expiry)) {
                e.preventDefault();
                alert('Please enter a valid expiry date (MM/YY).');
                return;
            }
            if (cvvVal.length !== 3) {
                e.preventDefault();
                alert('Please enter a valid 3-digit CVV.');
                return;
            }
        });
    }

});