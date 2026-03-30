// Management panel interactions

$(document).ready(function () {

    // Delete car confirmation modal
    const modal = document.querySelector('#delete-modal');
    const deleteForm = document.querySelector('#delete-form');
    const modalText = document.querySelector('#delete-modal-text');

    if (modal) {
        // Show modal on delete button click
        document.querySelectorAll('.delete-btn').forEach(function (btn) {
            btn.addEventListener('click', function () {
                const carId = this.dataset.carId;
                const carName = this.dataset.carName;
                modalText.textContent = `Are you sure you want to delete "${carName}"? This cannot be undone.`;
                deleteForm.action = '/management/cars/' + carId + '/delete/';
                modal.style.display = 'flex';
            });
        });

        // Cancel button
        document.querySelector('#cancel-delete').addEventListener('click', function () {
            modal.style.display = 'none';
        });

        // Close on backdrop click
        modal.addEventListener('click', function (e) {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }

    // Filter models by selected make in car form
    const makeSelect = document.querySelector('#make-select');
    const modelSelect = document.querySelector('#model-select');

    if (makeSelect && modelSelect) {
        function filterModels() {
            const selectedMake = makeSelect.value;
            const options = modelSelect.querySelectorAll('option');
            options.forEach(function (option) {
                if (!option.value) return;
                if (option.dataset.make === selectedMake) {
                    option.style.display = '';
                } else {
                    option.style.display = 'none';
                    if (option.selected) {
                        option.selected = false;
                    }
                }
            });
        }

        makeSelect.addEventListener('change', filterModels);
        filterModels();
    }

    // Custom image upload button
    const carImageBtn = document.querySelector('#car-image-btn');
    const carImageInput = document.querySelector('#car-image-input');
    const carImageFilename = document.querySelector('#car-image-filename');

    if (carImageBtn) {
        carImageBtn.addEventListener('click', function () {
            carImageInput.click();
        });

        carImageInput.addEventListener('change', function () {
            if (this.files[0]) {
                carImageFilename.textContent = this.files[0].name;
            }
        });
    }

});