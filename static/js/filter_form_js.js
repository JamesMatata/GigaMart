function getCurrentQuery() {
    return document.getElementById('search_query').value || '';
}

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

// Function to update pagination buttons
function updatePaginationButtons(html) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');

    // Get the updated pagination div from the response
    const updatedPagination = doc.querySelector('.pagination');

    // Update the current pagination div
    const paginationDiv = document.querySelector('.pagination');
    if(paginationDiv) {
        paginationDiv.innerHTML = updatedPagination.innerHTML;
        // Now, we need to update the active class on the correct page number
        const buttons = paginationDiv.querySelectorAll('.pagination-link');

        buttons.forEach(button => {
            // Remove the active class from all buttons
            button.classList.remove('active');

            // Add the active class to the button that corresponds to the current page
            if (button.getAttribute('value') === getCurrentPage()) {
                button.classList.add('active');
            }
        });
    }

}


// Function to get current filter parameters as URLSearchParams
function getCurrentFilterParams(form) {
    const isLargeScreen = window.innerWidth > 768;
    if(!isLargeScreen) {
        const formData = new FormData(document.getElementById('small-screen-filter-form'));
        return new URLSearchParams(formData);
    }
    if(isLargeScreen) {
        const formData = new FormData(document.getElementById('large-screen-filter-form'));
        return new URLSearchParams(formData);
    }
}

// Apply filters and handle pagination with AJAX
function applyFilters(form) {
    const params = getCurrentFilterParams(form);
    console.log(params)
    const searchNavInput = document.getElementById('search_query')
    if(searchNavInput) {
        params.append('searchbar_input', getCurrentQuery());
    }

    console.log(window.location.pathname)

    fetch(`${window.location.pathname}?${params.toString()}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById('product-list-div').innerHTML = html;

        // Update pagination links to include current filter parameters
        updatePaginationButtons(html);

        // Close filter form on small screens
        const filterForm = document.getElementById('small-screen-filter-form');
        const toggleIcon = document.getElementById('toggle-icon');
        if (filterForm) {
            filterForm.style.display = 'none';
            toggleIcon.classList.replace('fa-chevron-up', 'fa-chevron-down');
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
            // Apply filters on form submission (for small screen)
            smallScreenForm?.addEventListener('submit', function(event) {
                event.preventDefault();  // Prevent form submission
                applyFilters(smallScreenForm);  // Apply filters when the submit button is clicked
            });
            console.log(getCurrentFilterParams(smallScreenForm))

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

// Update filters and pagination dynamically without reloading
document.addEventListener('DOMContentLoaded', () => {
    restoreFilterState();
    initializeFilters();

    window.addEventListener('resize', initializeFilters);
});


// Pagination handling with AJAX
document.addEventListener('click', event => {
    if (event.target.matches('.pagination-link')) {
        event.preventDefault();  // Prevent default button behavior

        // Get the page number from the button's value attribute
        const page = event.target.getAttribute('value');
        console.log("Page clicked:", page);  // Log the clicked page number

        // Construct the URL based on the current filters and the page number
        const form = document.getElementById('small-screen-filter-form') || document.getElementById('large-screen-filter-form');

        // Collect current filter parameters from the form
        const params = new URLSearchParams(getCurrentFilterParams(form));

        // Add the page number to the filter parameters
        params.set('page', page);  // Set the clicked page number to the URL

        // Construct the URL with the updated search parameters
        const url = new URL(window.location.href);
        url.search = params.toString();  // Update the URL with new search params

        console.log("Final URL with page:", url.href);  // Log the final URL to check

        // Perform an AJAX request with the updated URL
        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(html => {
            // Update the product list dynamically with the new HTML content
            document.getElementById('product-list-div').innerHTML = html;

            // Update the pagination buttons after the content is loaded
            updatePaginationButtons(html);
        })
        .catch(error => {
            console.error('Error fetching paginated products:', error);
        });
    }
});

// Function to get the current page from the URL
function getCurrentPage() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('page') || 1;  // Default to page 1 if not present
}
