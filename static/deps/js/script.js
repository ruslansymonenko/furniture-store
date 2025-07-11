document.addEventListener('DOMContentLoaded', function () {
    const notification = document.getElementById('notification');

    if (notification) {
        setTimeout(function () {
            const alert = bootstrap.Alert.getOrCreateInstance(notification);
            alert.close();
        }, 7000);
    }

    const modalButton = document.getElementById('modalButton');
    const modalElement = document.getElementById('modalWindow');

    if (modalButton && modalElement) {
        const bootstrapModal = new bootstrap.Modal(modalElement);

        modalButton.addEventListener('click', function () {
            document.body.appendChild(modalElement);
            bootstrapModal.show();
        });

        const modalCloseBtn = modalElement.querySelector('.btn-close');
        if (modalCloseBtn) {
            modalCloseBtn.addEventListener('click', function () {
                // document.activeElement.blur();
                bootstrapModal.hide();
                modalButton.focus();
            });
        }
    }

    const deliveryInputs = document.querySelectorAll("input[name='requires_delivery']");
    const deliveryField = document.getElementById('deliveryAddressField');

    if (deliveryInputs.length && deliveryField) {
        deliveryInputs.forEach(function (input) {
            input.addEventListener('change', function () {
                if (input.value === "1") {
                    deliveryField.style.display = 'block';
                } else {
                    deliveryField.style.display = 'none';
                }
            });
        });
    }
});

