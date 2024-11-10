const cardsWrapper = document.querySelector('.category-cards-wrapper');
const cardWidth = document.querySelector('.category_card').offsetWidth + 10; // Card width plus gap
let currentIndex = 0;

function moveCard(direction) {
    const totalWidth = cardsWrapper.scrollWidth;

    if (direction === 'left' && currentIndex > 0) {
        currentIndex--;
    } else if (direction === 'right' && currentIndex < (totalWidth / cardWidth - 1)) {
        currentIndex++;
    }

    cardsWrapper.scrollLeft = currentIndex * cardWidth;
}