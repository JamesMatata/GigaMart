// Function to toggle the filter form visibility for small screens
document.getElementById('filter-toggle-btn')?.addEventListener('click', function () {
    const filterForm = document.getElementById('small-screen-filter-form');
    const toggleIcon = document.getElementById('toggle-icon');

    // Toggle the display of the filter form for small screens
    if (filterForm.style.display === 'none' || filterForm.style.display === '') {
        filterForm.style.display = 'block';
        toggleIcon.classList.remove('fa-chevron-down');
        toggleIcon.classList.add('fa-chevron-up');

        // Restore the form state when it's shown
        restoreFilterState();
    } else {
        filterForm.style.display = 'none';
        toggleIcon.classList.remove('fa-chevron-up');
        toggleIcon.classList.add('fa-chevron-down');

        // Save the form state when it's hidden
        saveFilterState();
    }
});

// Function to collect filter values and send AJAX request
function applyFilters(form) {
    const formData = new FormData(form);
    const params = new URLSearchParams(formData).toString(); // Convert form data to URL parameters

    fetch(`${window.location.pathname}?${params}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => response.text())
        .then(html => {
            // Update only the product list section with new HTML (excluding the filter form)
            document.getElementById('product-list-div').innerHTML = html;

            // Close the filter form after submission (for small screens)
            const filterForm = document.getElementById('small-screen-filter-form');
            const toggleIcon = document.getElementById('toggle-icon');
            if (filterForm) {
                filterForm.style.display = 'none';
                toggleIcon.classList.remove('fa-chevron-up');
                toggleIcon.classList.add('fa-chevron-down');
            }
        })
        .catch(error => console.error('Error fetching filtered products:', error));
}

// Price range logic
const smallPriceRange = document.getElementById('small_price_range');
const smallPriceMin = document.getElementById('small_price_min');
const smallPriceMax = document.getElementById('small_price_max');

const largePriceRange = document.getElementById('large_price_range');
const largePriceMin = document.getElementById('large_price_min');
const largePriceMax = document.getElementById('large_price_max');

if (smallPriceRange && smallPriceMax) {
    smallPriceRange.addEventListener('input', function () {
        smallPriceMax.value = smallPriceRange.value;
    });
}

if (largePriceRange && largePriceMax) {
    largePriceRange.addEventListener('input', function () {
        largePriceMax.value = largePriceRange.value;
    });
}

// Function to save filter state to sessionStorage
function saveFilterState() {
    const form = document.getElementById('small-screen-filter-form');
    const checkboxes = form.querySelectorAll('input[type="checkbox"]');
    const priceRange = form.querySelector('input[type="range"]');
    const priceMin = form.querySelector('input[name="price_min"]');
    const priceMax = form.querySelector('input[name="price_max"]');

    // Store selected checkboxes values
    const selectedCheckboxes = [];
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            selectedCheckboxes.push(checkbox.value);
        }
    });

    // Save to sessionStorage
    sessionStorage.setItem('selectedCheckboxes', JSON.stringify(selectedCheckboxes));
    sessionStorage.setItem('priceRange', priceRange.value);
    sessionStorage.setItem('priceMin', priceMin.value);
    sessionStorage.setItem('priceMax', priceMax.value);
}

// Function to restore filter state from sessionStorage
function restoreFilterState() {
    const form = document.getElementById('small-screen-filter-form');
    const checkboxes = form.querySelectorAll('input[type="checkbox"]');
    const priceRange = form.querySelector('input[type="range"]');
    const priceMin = form.querySelector('input[name="price_min"]');
    const priceMax = form.querySelector('input[name="price_max"]');

    // Restore checkboxes selection
    const selectedCheckboxes = JSON.parse(sessionStorage.getItem('selectedCheckboxes') || '[]');
    checkboxes.forEach(checkbox => {
        if (selectedCheckboxes.includes(checkbox.value)) {
            checkbox.checked = true;
        }
    });

    // Restore price range and inputs
    if (sessionStorage.getItem('priceRange')) {
        priceRange.value = sessionStorage.getItem('priceRange');
        priceMin.value = sessionStorage.getItem('priceMin');
        priceMax.value = sessionStorage.getItem('priceMax');
    }
}

// Function to initialize filtering for both small and large screens
function initializeFilters() {
    const isLargeScreen = window.innerWidth > 768;

    // For small screen: Add event listeners and toggle form visibility
    if (!isLargeScreen) {
        const smallScreenForm = document.getElementById('small-screen-filter-form');
        if (smallScreenForm) {
            document.querySelectorAll('#small-screen-filter-form select, #small-screen-filter-form input[type="number"]').forEach(input => {
                input.addEventListener('input', function() {
                    applyFilters(smallScreenForm);
                });
            });

            // Apply filters on form submission (for small screen)
            smallScreenForm?.addEventListener('submit', function(event) {
                event.preventDefault();  // Prevent form submission
                applyFilters(smallScreenForm);  // Apply filters when the submit button is clicked
            });

            // Trigger the initial filtering when the page loads for small screen form
            applyFilters(smallScreenForm);
        }
    }
    
    // For large screen: Add event listeners without toggling visibility
    if (isLargeScreen) {
        const largeScreenForm = document.getElementById('large-screen-filter-form');
        if (largeScreenForm) {
            document.querySelectorAll('#large-screen-filter-form input[type="checkbox"], #large-screen-filter-form input[type="number"]').forEach(input => {
                input.addEventListener('input', applyFilters);
            });

            // Trigger the initial filtering when the page loads for large screen form
            applyFilters(largeScreenForm);
        }
    }
}

smallPriceMin.value = largePriceMin.value = 0;

smallPriceMax.value = smallPriceRange.value;

largePriceMax.value = largePriceRange.value;

document.addEventListener('DOMContentLoaded', restoreFilterState);

document.getElementById('large-screen-filter-form').addEventListener('change', function(event) {
    // This function will be called whenever any input/select in the form is changed
    initializeFilters()
});

// Call initializeFilters on page load
document.addEventListener('DOMContentLoaded', initializeFilters);

// Add event listener to handle screen resize
window.addEventListener('resize', initializeFilters);
