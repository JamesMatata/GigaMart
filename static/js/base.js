const productsDropdownMenu = document.getElementById("products_dropdown_menu");
const accountDropdownMenu = document.getElementById("account_dropdown_menu");
const minNavProductsDropdownMenu = document.getElementById("min_nav_products_dropdown_menu");
const minNavAccountDropdownMenu = document.getElementById("min_nav_account_dropdown_menu");

function toggleProductsDropdown() {
    productsDropdownMenu.classList.toggle("show");
    document
        .querySelector(".products_button_icon_right")
        .classList.toggle("rotate-icon");
}

function toggleMinNavProductsDropdown() {
    minNavProductsDropdownMenu.classList.toggle("show");
}

function toggleAccountDropdown() {
    accountDropdownMenu.classList.toggle("show");
    document
        .querySelector(".account_button_icon_right")
        .classList.toggle("rotate-icon");
}

function toggleMinNavAccountDropdown() {
    minNavAccountDropdownMenu.classList.toggle("show");
}

document.addEventListener("click", function (event) {
    const productsDropdownButton = document.getElementById(
        "products_dropdown_button"
    );
    const accountDropdownButton = document.getElementById(
        "account_dropdown_button"
    );
    const minNavProductsDropdownButton = document.getElementById(
        "min_nav_products_dropdown_button"
    );
    const minNavAccountDropdownButton = document.getElementById(
        "min_nav_account_dropdown_button"
    );

    if (!productsDropdownButton.contains(event.target)) {
        productsDropdownMenu.classList.remove("show");
        document
            .querySelector(".products_button_icon_right")
            .classList.remove("rotate-icon");
    }

    if (!accountDropdownButton.contains(event.target)) {
        accountDropdownMenu.classList.remove("show");
        document
            .querySelector(".account_button_icon_right")
            .classList.remove("rotate-icon");
    }

    if (!minNavProductsDropdownButton.contains(event.target)) {
        minNavProductsDropdownMenu.classList.remove("show");
    }

    if (!minNavAccountDropdownButton.contains(event.target)) {
        minNavAccountDropdownMenu.classList.remove("show");
    }
});
  