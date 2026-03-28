// Car list page interactions

$(document).ready(function () {

    // Auto submit form when sort select changes
    const sortSelect = document.querySelector('#sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', function () {
            const form = document.querySelector('#filter-form');
            const sortInput = document.createElement('input');
            sortInput.type = 'hidden';
            sortInput.name = 'sort';
            sortInput.value = this.value;
            form.appendChild(sortInput);
            form.submit();
        });
    }

    // Live search suggestions
    const searchInput = document.querySelector('input[name="q"]');
    const suggestionsBox = document.querySelector('#search-suggestions');

    if (searchInput && suggestionsBox) {
        searchInput.addEventListener('input', function () {
            const query = this.value.trim();
            if (query.length < 2) {
                suggestionsBox.style.display = 'none';
                return;
            }

            $.ajax({
                url: '/cars/search/suggestions/',
                data: { q: query },
                success: function (response) {
                    suggestionsBox.innerHTML = '';
                    if (response.results.length === 0) {
                        suggestionsBox.style.display = 'none';
                        return;
                    }
                    response.results.forEach(function (car) {
                        const item = document.createElement('div');
                        item.className = 'suggestion-item';
                        item.innerHTML = `
                            <span style="color:var(--text-primary); font-size:0.875rem;">${car.label}</span>
                            <span style="color:var(--accent); font-size:0.8rem;">${car.price}</span>
                        `;
                        item.addEventListener('click', function () {
                            window.location.href = '/cars/' + car.id + '/';
                        });
                        suggestionsBox.appendChild(item);
                    });
                    suggestionsBox.style.display = 'block';
                }
            });
        });

        // Hide suggestions when clicking outside
        document.addEventListener('click', function (e) {
            if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
                suggestionsBox.style.display = 'none';
            }
        });
    }

});