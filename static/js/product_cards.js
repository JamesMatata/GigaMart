function updateQuantity(button, action, productId) {
    const productCard = button.closest('.product_card_basket_and_later_div');
    const quantityInput = productCard.querySelector('.product_cart_items_to_add_no');
    let currentQty = parseInt(quantityInput.value);

    if (action === 'increase') {
        quantityInput.value = currentQty + 1;
    } else if (action === 'decrease' && currentQty > 1) {
        quantityInput.value = currentQty - 1;
    }
}

// Add the item to the cart
function addToCart(productId) {
    const productCard = document.querySelector(`[data-product-id="${productId}"]`);
    const quantityInput = productCard.querySelector('.product_cart_items_to_add_no');
    const quantity = quantityInput.value;
    const delUrl = productCard.getAttribute('data-delete-url');

    fetch(delUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            productid: productId,
            productqty: quantity
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById("small_device_basket-qty").innerText = data.basket_qty;
                document.getElementById('basket-qty').innerText = data.basket_qty;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred');
        });
}

function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

function addToWishlist(productId) {
    const button = document.getElementById(`wishlist-btn-${productId}`);
    const url = button.getAttribute('data-add-to-wishlist-url');

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ product_id: productId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'added') {
            button.querySelector('svg path').setAttribute('fill', '#800080');  // Change to purple
        } else {
            button.querySelector('svg path').setAttribute('fill', '#808080');  // Change to gray
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
