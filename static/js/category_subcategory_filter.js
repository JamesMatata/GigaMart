document.addEventListener("DOMContentLoaded", function () {
    const categoryField = document.getElementById("id_category");
    const subcategoryField = document.getElementById("id_subcategory");

    if (categoryField) {
        categoryField.addEventListener("change", function () {
            const categoryId = this.value;

            // Clear current subcategory options
            subcategoryField.length = 0;

            // Hide subcategory field by default
            subcategoryField.style.display = "none";

            if (!categoryId) return;

            // Fetch subcategories based on selected category
            fetch(`/get-subcategories/${categoryId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.length > 0) {
                        // Show subcategory field if subcategories are available
                        subcategoryField.style.display = "block";

                        // Populate subcategory dropdown with new options
                        data.forEach(subcategory => {
                            const option = new Option(subcategory.name, subcategory.id);
                            subcategoryField.add(option);
                        });
                    }
                })
                .catch(error => console.error("Error fetching subcategories:", error));
        });
    }

    const form = document.querySelector('form');

    // Add event listener to form submission
    form.addEventListener('submit', function(event) {
        // Get key_features and specifications fields
        const keyFeaturesField = document.querySelector('textarea[name="key_features"]');
        const specificationsField = document.querySelector('textarea[name="specifications"]');

        // Check key_features field
        if (!isValidKeyFeatures(keyFeaturesField.value)) {
            alert('Key Features must be in the format: ["Feature: Description"]');
            event.preventDefault();  // Prevent form submission
            return;
        }

        // Check specifications field
        if (!isValidSpecifications(specificationsField.value)) {
            alert('Specifications must be in a valid JSON format: {"Category": {"Key": "Value"}}');
            event.preventDefault();  // Prevent form submission
            return;
        }
    });

    // Function to validate key features format
    function isValidKeyFeatures(value) {
        try {
            const features = JSON.parse(value);
            return Array.isArray(features) && features.every(item => typeof item === 'string');
        } catch (e) {
            return false;  // If JSON parsing fails, return false
        }
    }

    // Function to validate specifications format
    function isValidSpecifications(value) {
        try {
            const specifications = JSON.parse(value);
            return typeof specifications === 'object' && specifications !== null;
        } catch (e) {
            return false;  // If JSON parsing fails, return false
        }
    }

});


