// Select all product cards
const productCards = document.querySelectorAll(".product_card");

// Loop through each product card to add event listeners
productCards.forEach((card) => {
    const increaseButton = card.querySelector(
        ".product_cart_increase_items_button"
    );
    const decreaseButton = card.querySelector(
        ".product_cart_decrease_items_button"
    );
    const quantityInput = card.querySelector(
        ".product_cart_items_to_add_no"
    );

    // Increase quantity
    increaseButton.addEventListener("click", () => {
        let currentValue = parseInt(quantityInput.value) || 1;
        quantityInput.value = currentValue + 1;
    });

    // Decrease quantity
    decreaseButton.addEventListener("click", () => {
        let currentValue = parseInt(quantityInput.value) || 1;
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
        }
    });
});