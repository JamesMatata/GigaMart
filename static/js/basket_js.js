function updateSummarySection(basketItems) {
    const summaryTable = document.querySelector(".basket_summary_div table");

    // Clear existing rows before updating
    summaryTable.querySelectorAll("tr.basket_summary_item").forEach(row => row.remove());

    // Ensure basketItems is defined and an array
    if (basketItems && Array.isArray(basketItems)) {
        basketItems.forEach(item => {
            const row = document.createElement("tr");
            row.classList.add("basket_summary_item");
            row.style.display = "flex";

            row.innerHTML = `
                <td class="basket_summary_td" style="flex: 1;">
                    <p class="basket_summary_product_title">${item.product_name}</p>
                </td>
                <td class="basket_summary_td quantity" style="width: 60px;">${item.qty}</td>
                <td class="basket_summary_td price" style="width: 110px;overflow: hidden;">${parseFloat(item.price).toFixed(2)}</td>
            `;

            summaryTable.appendChild(row);
        });
    }

    // Recalculate the total cost after updating the summary section
    refreshBasketSummary();
}

function refreshBasketSummary() {
    $.ajax({
        type: 'GET',
        url: '/basket/',  // The URL for the summary view, should be '/basket/' if it's the correct endpoint
        dataType: 'json',
        success: function (json) {
            // Update the summary section with the basket items
            updateSummarySection(json.basket_items);

            // Update subtotal if needed
            document.getElementById("total-costs").textContent = "KES " + json.subtotal;
        },
        error: function (xhr) {
            console.log('Error: ' + xhr.responseText);
        }
    });
}


// Delete Item
$(document).on('click', '.delete-button', function (e) {
    e.preventDefault();
    const productId = $(this).data('index');
    const deleteUrl = $(this).data('delete-url'); // Ensure delete URL is set correctly

    $.ajax({
        type: 'POST',
        url: deleteUrl,
        headers: { 'X-CSRFToken': getCSRFToken() }, // Add CSRF token here
        data: JSON.stringify({ productid: productId }),
        contentType: 'application/json',  // Ensure data type matches expected JSON format
        success: function (json) {
            $(`.product-item[data-index="${productId}"]`).remove();
            document.getElementById("basket-qty").innerHTML = json.qty;
            document.getElementById("small_device_basket-qty").innerHTML = json.qty;
            refreshBasketSummary()

            if (json.qty === 0) {
                document.querySelector('.container').innerHTML = `
                    <p id="no-items-in-basket" style="margin-bottom: 400px; margin-top: 20px; text-align: center; font-size: 18px;font-weight: 500">
                        Your basket is empty <a href="{% url 'store:index' %}">Shop</a>
                    </p>`;
            }

            refreshBasketSummary();
        },
        error: function (xhr) {
            console.log('Error: ' + xhr.responseText);
        }
    });
});

// Update Item Quantity
$(document).on('click', '.update-button', function (e) {
    e.preventDefault();
    const productId = $(this).data('index');
    const quantity = $(`#quantity${productId}`).val();
    const updateUrl = $(this).data('update-url'); // Ensure update URL is set correctly

    $.ajax({
        type: 'POST',
        url: updateUrl,
        headers: { 'X-CSRFToken': getCSRFToken() }, // Add CSRF token here
        data: JSON.stringify({ productid: productId, productqty: quantity }),
        contentType: 'application/json',  // Ensure data type matches expected JSON format
        success: function (json) {
            document.getElementById("basket-qty").innerHTML = json.qty;
            document.getElementById("small_device_basket-qty").innerHTML = json.qty;
            refreshBasketSummary()
        },
        error: function (xhr) {
            console.log('Error: ' + xhr.responseText);
        }
    });
});

refreshBasketSummary()


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


