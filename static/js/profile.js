// Profile page interactions

$(document).ready(function () {

// Custom avatar button trigger
const avatarBtn = document.querySelector('#avatar-btn');
if (avatarBtn) {
    avatarBtn.addEventListener('click', function () {
        document.querySelector('#avatar-input').click();
    });
}

// Avatar image preview before upload
const avatarInput = document.querySelector('#avatar-input');
if (avatarInput) {
    avatarInput.addEventListener('change', function () {
        const file = this.files[0];
        if (!file) return;

        // Update filename label
        document.querySelector('#avatar-filename').textContent = file.name;

        const reader = new FileReader();
        reader.onload = function (e) {
            const preview = document.querySelector('#avatar-preview');
            const container = document.querySelector('#avatar-preview-container');
            preview.src = e.target.result;
            container.style.display = 'block';
        };
        reader.readAsDataURL(file);
    });
}

    // Live password match check
    const newPw1 = document.querySelector('#new-password1');
    const newPw2 = document.querySelector('#new-password2');
    const pwMsg = document.querySelector('#pw-match-msg');

    if (newPw2) {
        newPw2.addEventListener('input', function () {
            if (newPw1.value === '' || newPw2.value === '') {
                pwMsg.textContent = '';
                return;
            }
            if (newPw1.value === newPw2.value) {
                pwMsg.textContent = 'Passwords match';
                pwMsg.style.color = 'var(--success)';
            } else {
                pwMsg.textContent = 'Passwords do not match';
                pwMsg.style.color = 'var(--danger)';
            }
        });
    }

    // Prevent password form submit if passwords don't match
    const passwordForm = document.querySelector('#password-form');
    if (passwordForm) {
        passwordForm.addEventListener('submit', function (e) {
            if (newPw1.value !== newPw2.value) {
                e.preventDefault();
                pwMsg.textContent = 'Passwords do not match';
                pwMsg.style.color = 'var(--danger)';
            }
        });
    }

});