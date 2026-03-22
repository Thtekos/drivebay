// Car list page interactions

$(document).ready(function () {

    // Auto-submit form when sort changes
    querySelector('#sort-select').addEventListener('change', function () {
        const form = document.querySelector('#filter-form');
        const sortInput = document.createElement('input');
        sortInput.type = 'hidden';
        sortInput.name = 'sort';
        sortInput.value = this.value;
        form.appendChild(sortInput);
        form.submit();
    });

});