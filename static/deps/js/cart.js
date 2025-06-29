document.addEventListener('DOMContentLoaded', function () {
    const goodsInCartCount = document.getElementById("goods-in-cart-count");

    document.addEventListener("click", function (e) {
        if (e.target.closest(".add-to-cart")) {
            e.preventDefault();

            const button = e.target.closest(".add-to-cart");
            addToCart(button)
        }

        if (e.target.closest(".remove-from-cart")) {
            e.preventDefault();

            const button = e.target.closest(".remove-from-cart");
            removeFromCart(button)
        }

        if (e.target.closest(".decrement")) {
            const button = e.target.closest(".decrement");
            decreaseQuantity(button)
        }

        if (e.target.closest(".increment")) {
            const button = e.target.closest(".increment");
            increaseQuantity(button)
        }
    });

    function addToCart(button) {
        const addToCartUrl = button.getAttribute("href");
        const productId = button.dataset.productId;

        fetch(addToCartUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken(),
            },
            body: new URLSearchParams({ product_id: productId })
        })
        .then(response => response.json())
        .then(data => {
            showSuccess(data.message);
            updateCartCount(1);

            const htmlWrapper = $("<div>").html(data.cart_item_html);
            const newContent = htmlWrapper.find("#cart-items-container").html();

            $("#cart-items-container").html(newContent);
        })
        .catch((e) => {
            showError('Error while adding product to cart')
            console.log(`Error while adding product to cart, ${e}`)
        });
    }

    function removeFromCart(button) {
        const cartId = button.dataset.cartId;
        const url = button.getAttribute("href");

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken(),
            },
            body: new URLSearchParams({ cart_id: cartId })
        })
        .then(response => response.json())
        .then(data => {
            showSuccess(data.message);
            updateCartCount(-data.quantity_deleted);

            const htmlWrapper = $("<div>").html(data.cart_item_html);
            const newContent = htmlWrapper.find("#cart-items-container").html();


            if (!newContent) {
                console.warn('❗ newContent is undefined — возможно, #cart-items-container отсутствует в HTML');
            }

            $("#cart-items-container").html(newContent);
        })
        .catch((e) => {
            showError('Product delete error')
            console.log(`Product delete error`)
        });
    }

    function updateCart(cartID, quantity, change, url) {
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken(),
            },
            body: new URLSearchParams({
                cart_id: cartID,
                quantity: quantity,
            })
        })
        .then(response => response.json())
        .then(data => {
            showSuccess(data.message);
            updateCartCount(change);

            const htmlWrapper = $("<div>").html(data.cart_item_html);
            const newContent = htmlWrapper.find("#cart-items-container").html();

            $("#cart-items-container").html(newContent);
        })
        .catch((e) => {
            showError("Error updating error")
            console.log(`Error updating error ${e}`)
        });
    }

    function decreaseQuantity(button) {
        const input = button.closest(".input-group").querySelector(".number");
        const currentValue = parseInt(input.value);

        if (currentValue > 1) {
            const newQuantity = currentValue - 1;

            input.value = newQuantity;

            updateCart(
                button.dataset.cartId,
                newQuantity,
                -1,
                button.dataset.cartChangeUrl
            );
        }
    }

    function increaseQuantity(button) {
        const input = button.closest(".input-group").querySelector(".number");
        const currentValue = parseInt(input.value);
        const newQuantity = currentValue + 1;

        input.value = newQuantity;

        updateCart(
            button.dataset.cartId,
            newQuantity,
            1,
            button.dataset.cartChangeUrl
        );
    }

    function showSuccess(message) {
         toastr.options = {
            "closeButton": true,
            "progressBar": true,
            "positionClass": "toast-bottom-right",
            "timeOut": "7000",
        };
        toastr.success(message);
    }

    function showError(message) {
         toastr.options = {
            "closeButton": true,
            "progressBar": true,
            "positionClass": "toast-bottom-right",
            "timeOut": "7000",
        };
        toastr.error(message);
    }

    function updateCartCount(change) {
        const currentCount = parseInt(goodsInCartCount.textContent || 0);
        goodsInCartCount.textContent = currentCount + change;
    }

    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]")?.value;
    }
});