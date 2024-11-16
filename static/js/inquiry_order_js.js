document.addEventListener('DOMContentLoaded', function () {
    // Get elements
    const getButton = document.getElementById('get_inquiry_button');
    const inquiryInput = document.getElementById('inquiry_id');
    const getInquiryUrl = document.getElementById('get_inquiry_url').value; // Ensure this URL is correct
    const resultsDiv = document.getElementById('all_inquiry_order_cards_div'); // Div where the results will be displayed

    // Function to handle the inquiry fetch
    function fetchInquiry() {

        const inquiryId = inquiryInput.value.trim(); // Get and trim input value

        // Check if inquiry ID is provided
        if (!inquiryId) {
            alert('Please enter a valid inquiry ID.');
            return;
        }

        // Construct the URL with query parameters
        const params = new URLSearchParams();
        params.append('inquiry_id', inquiryId);

        const requestUrl = `${getInquiryUrl}?${params.toString()}`;

        // Perform the fetch request
        fetch(requestUrl, {
            method: 'GET', // Default method is GET
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Ensure that this is an AJAX request
                'X-CSRFToken': getCSRFToken() // Include CSRF token if needed
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json(); // Parse the JSON response
            })
            .then(data => {
                // Check if there is any HTML data in the response and update the div
                if (data.html) {
                    resultsDiv.innerHTML = data.html; // Dynamically update the results div with the HTML
                } else {
                    resultsDiv.innerHTML = '<p>No inquiry details found.</p>'; // Fallback if no HTML returned
                }
            })
            .catch(error => {
                alert('An error occurred while fetching the inquiry. Please try again.');
            });
    }

    // Function to get CSRF token from cookies
    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        console.log('CSRF Token:', cookieValue);
        return cookieValue || '';
    }

    // Add click event listener to the button
    getButton.addEventListener('click', function (e) {
        e.preventDefault(); // Prevent default button behavior
        fetchInquiry(); // Call the fetchInquiry function
    });
});