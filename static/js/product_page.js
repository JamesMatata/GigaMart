function swapImage(element) {
    // Get the main image element
    const mainImage = document.getElementById("main_image");
    // Store the current src of the main image
    const mainImageSrc = mainImage.src;
    // Get the src of the clicked thumbnail image
    const thumbnailImage = element.querySelector("img");

    // Swap the images
    mainImage.src = thumbnailImage.src;
    thumbnailImage.src = mainImageSrc;
}

function showSection(sectionId, activeDivId) {
    // Hide all sections
    document.getElementById("product_description").classList.add("hidden");
    document.getElementById("product_key_features").classList.add("hidden");
    document.getElementById("product_specifications").classList.add("hidden");
    // Remove 'active' class from all title divs
    document.getElementById("description_div").classList.remove("active");
    document.getElementById("features_div").classList.remove("active");
    document.getElementById("specifications_div").classList.remove("active");
    // Show selected section
    document.getElementById(sectionId).classList.remove("hidden");
    // Add 'active' class to the clicked div
    document.getElementById(activeDivId).classList.add("active");
}

// Set the default view to 'Description'
showSection("product_description", "description_div");