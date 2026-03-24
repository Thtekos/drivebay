// Register page — client side validation

$(document).ready(function () {

    const password1 = document.querySelector('#password1');
    const password2 = document.querySelector('#password2');
    const matchMsg = document.querySelector('#password-match-msg');

    // Live password match check
    password2.addEventListener('input', function () {
        if (password1.value === '' || password2.value === '') {
            matchMsg.textContent = '';
            return;
        }
        if (password1.value === password2.value) {
            matchMsg.textContent = 'Passwords match';
            matchMsg.style.color = 'var(--success)';
        } else {
            matchMsg.textContent = 'Passwords do not match';
            matchMsg.style.color = 'var(--danger)';
        }
    });

    // Prevent submit if passwords don't match
    document.querySelector('#register-form').addEventListener('submit', function (e) {
        if (password1.value !== password2.value) {
            e.preventDefault();
            matchMsg.textContent = 'Passwords do not match';
            matchMsg.style.color = 'var(--danger)';
        }
    });

});