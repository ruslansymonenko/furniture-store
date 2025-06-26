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

            console.log(data.message);

            document.getElementById("cart-items-container").innerHTML = data.cart_item_html;
        })
        .catch((e) => console.log(`Error while adding product to cart, ${e}`));
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

            document.getElementById("cart-items-container").innerHTML = data.cart_items_html;
        })
        .catch(() => console.log("Product delete error"));
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
            document.getElementById("cart-items-container").innerHTML = data.cart_items_html;
        })
        .catch(() => console.log("Error updating error"));
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
        const notification = document.getElementById("notification");
        if (!notification) return;

        const alertDiv = document.createElement("div");
        alertDiv.className = "alert alert-success alert-dismissible fade show custom-shadow";
        alertDiv.setAttribute("role", "alert");

        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        notification.appendChild(alertDiv);

        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alertDiv);
            bsAlert.close();
        }, 7000);
    }

    function showError(message) {
        const notification = document.getElementById("notification");
        if (!notification) return;

        const alertDiv = document.createElement("div");
        alertDiv.className = "alert alert-danger alert-dismissible fade show custom-shadow";
        alertDiv.setAttribute("role", "alert");

        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        notification.appendChild(alertDiv);

        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alertDiv);
            bsAlert.close();
        }, 7000);
    }


    function updateCartCount(change) {
        const currentCount = parseInt(goodsInCartCount.textContent || 0);
        goodsInCartCount.textContent = currentCount + change;
    }

    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]")?.value;
    }
});