// --- Authentication & Login ---
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }
});

async function loginUser(email, password) {
    const apiUrl = 'http://127.0.0.1:5000/api/v1/auth/login';

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            window.location.href = 'index.html';
        } else {
            const errorData = await response.json().catch(() => null);
            const errorMessage = errorData?.msg || response.statusText;
            alert('Login failed: ' + errorMessage);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred. Please try again later.');
    }
}

// --- Storage & Auth Helpers ---
function getCookie(name) {
    return localStorage.getItem(name);
}

function checkAuthentication(token) {
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }

    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }
}

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// --- Index Page Logic ---
document.addEventListener('DOMContentLoaded', () => {
    const placesList = document.getElementById('places-list');

    if (placesList) {
        const token = getCookie('token');
        checkAuthentication(token);
        setupPriceFilter();
        fetchPlaces(token);
    }
});

async function fetchPlaces(token) {
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.log('Failed to fetch places');
        }
    } catch (error) {
        console.log('Error:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    places.forEach((place) => {
        const placeCard = document.createElement('article');
        placeCard.classList.add('place-card');
        placeCard.dataset.price = place.price;

        placeCard.innerHTML = `
            <h3>${place.title || place.name}</h3>
            <p>Price: $${place.price} / night</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesList.appendChild(placeCard);
    });
    
    filterPlaces();
}

function filterPlaces() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    const selectedPrice = priceFilter.value;
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach((card) => {
        const placePrice = Number(card.dataset.price);
        if (selectedPrice === 'all' || placePrice <= Number(selectedPrice)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    const prices = ['10', '50', '100', 'All'];
    prices.forEach((price) => {
        const option = document.createElement('option');
        option.value = price.toLowerCase();
        option.textContent = price;
        priceFilter.appendChild(option);
    });

    priceFilter.addEventListener('change', filterPlaces);
}

// --- Place Details Page Logic ---
document.addEventListener('DOMContentLoaded', () => {
    const placeDetailsSection = document.getElementById('place-details');
    
    if (placeDetailsSection) {
        const placeId = getPlaceIdFromURL();
        const token = getCookie('token');
        checkAuthentication(token);

        if (placeId) {
            fetchPlaceDetails(token, placeId);
        }
    }
});

async function fetchPlaceDetails(token, placeId) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) return;

        const place = await response.json();

        try {
            const reviewsResponse = await fetch(`http://127.0.0.1:5000/api/v1/reviews/`, {
                method: 'GET',
                headers: headers
            });
            if (reviewsResponse.ok) {
                const allReviews = await reviewsResponse.json();
                place.reviews = allReviews.filter(rev => rev.place_id === placeId);
            } else {
                place.reviews = [];
            }
        } catch (err) {
            console.error('Error fetching reviews:', err);
            place.reviews = [];
        }

        displayPlaceDetails(place);
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

function displayPlaceDetails(place) {
    const placeDetailsSection = document.getElementById('place-details');
    if (!placeDetailsSection) return;

    const amenitiesList = place.amenities && place.amenities.length > 0
        ? place.amenities.map(item => `<li>${item.name || item}</li>`).join('')
        : '<li>No amenities available</li>';

    const reviewsList = place.reviews && place.reviews.length > 0
        ? place.reviews.map(rev => `
            <div class="review-card">
                <p><strong>Review:</strong> ${rev.text || rev.comment}</p>
                <p>Rating: ${rev.rating} / 5</p>
            </div>
        `).join('')
        : '<p>No reviews yet.</p>';

    placeDetailsSection.innerHTML = `
        <h1>${place.name || place.title}</h1>
        <p class="description">${place.description}</p>
        <p class="price"><strong>Price:</strong> $${place.price}</p>
        
        <div class="amenities-section">
            <h3>Amenities:</h3>
            <ul>${amenitiesList}</ul>
        </div>

        <div class="reviews-section">
            <h3>Reviews:</h3>
            ${reviewsList}
        </div>
    `;
}

// --- Add Review Logic ---
document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;

    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();

    if (!token) return;

    if (!placeId) {
        console.error('Place ID is missing from the URL.');
        return;
    }

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const reviewText = document.getElementById('review-text').value;
        const selectedRating = document.querySelector('input[name="rating"]:checked');
        
        if (!selectedRating) {
            alert('Please select a rating star.');
            return;
        }

        const rating = selectedRating.value;

        await submitReview(token, placeId, reviewText, rating, reviewForm);
    });
});

async function submitReview(token, placeId, reviewText, rating, reviewForm) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: Number(rating),
                place_id: placeId
            })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            reviewForm.reset();
            fetchPlaceDetails(token, placeId);
        } else {
            const errorData = await response.json().catch(() => null);
            const message = errorData?.error || errorData?.message || errorData?.msg || 'Failed to submit review';
            alert(message);
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('An error occurred while submitting the review.');
    }
}