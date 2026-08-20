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
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/; Secure; SameSite=Strict`;
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
// Task 2 - Index

function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (let cookie of cookies) {
        cookie = cookie.trim();

        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }

    return null;
}


function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
        }
    }

    return token;
}

async function fetchPlaces(token) {
    const headers = {};

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(
            'http://127.0.0.1:5000/api/v1/places/',
            {
                method: 'GET',
                headers: headers
            }
        );

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

    if (!placesList) {
        return;
    }

    placesList.innerHTML = '';

    places.forEach((place) => {
        const placeCard = document.createElement('article');

        placeCard.classList.add('place-card');
        placeCard.dataset.price = place.price;

        placeCard.innerHTML = `
            <h3>${place.title}</h3>
            <p>Price: $${place.price} / night</p>
            <a href="place.html?id=${place.id}" class="details-button">
                View Details
            </a>
        `;

        placesList.appendChild(placeCard);
    });
    
    filterPlaces();
}

function filterPlaces() {
    const priceFilter = document.getElementById('price-filter');

    if (!priceFilter) {
        return;
    }

    const selectedPrice = priceFilter.value;
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach((card) => {
        const placePrice = Number(card.dataset.price);

        if (
            selectedPrice === 'all' ||
            placePrice <= Number(selectedPrice)
        ) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');

    if (!priceFilter) {
        return;
    }

    const prices = ['10', '50', '100', 'All'];

    prices.forEach((price) => {
        const option = document.createElement('option');

        option.value = price.toLowerCase();
        option.textContent = price;

        priceFilter.appendChild(option);
    });

    priceFilter.addEventListener('change', filterPlaces);
}

document.addEventListener('DOMContentLoaded', () => {
    const placesList = document.getElementById('places-list');

    if (placesList) {
        const token = checkAuthentication();

        setupPriceFilter();
        fetchPlaces(token);
    }
});
document.addEventListener('DOMContentLoaded', () => {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');

    checkAuthentication(token);

    if (placeId) {
        fetchPlaceDetails(token, placeId);
    }
});

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication(token) {
    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        if (!token) {
            addReviewSection.style.display = 'none';
        } else {
            addReviewSection.style.display = 'block';
        }
    }
}

async function fetchPlaceDetails(token, placeId) {
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`https://your-api-url.com/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) return;

        const place = await response.json();
        displayPlaceDetails(place);
    } catch (error) {
        
    }
}

function displayPlaceDetails(place) {
    const placeDetailsSection = document.getElementById('place-details');
    if (!placeDetailsSection) return;

    placeDetailsSection.innerHTML = '';

    const amenitiesList = place.amenities && place.amenities.length > 0
        ? place.amenities.map(item => `<li>${item.name || item}</li>`).join('')
        : '<li>No amenities available</li>';

    const reviewsList = place.reviews && place.reviews.length > 0
        ? place.reviews.map(rev => `
            <div class="review-card">
                <p><strong>${rev.user_name || 'User'}:</strong> ${rev.comment || rev.text}</p>
                <p>Rating: ${rev.rating} / 5</p>
            </div>
        `).join('')
        : '<p>No reviews yet.</p>';

    placeDetailsSection.innerHTML = `
        <h1>${place.name}</h1>
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
document.addEventListener("DOMContentLoaded", () => {
    const placesData = {
        "1": {
            title: "Cozy Beachhouse",
            price: "$150 / night",
            description: "A lovely beach house right next to the shore with peaceful vibes.",
            amenities: "Wi-Fi, Ocean View, Kitchen, AC",
        
            reviews: [
                { name: "Ahmad Hassan", rating: "5.0", text: "Amazing stay! The sound of the waves at night was so relaxing." },
                { name: "Mona Ali", rating: "4.5", text: "Very clean and cozy, highly recommended." }
            ]
        },
        "2": {
            title: "City Center Apartment",
            price: "$90 / night",
            description: "Modern apartment located right in the heart of the city near all attractions.",
            amenities: "Wi-Fi, Elevator, Free Parking, Smart TV",
            reviews: [
                { name: "Fahad Salem", rating: "4.0", text: "Great location! Close to all restaurants and shops." }
            ]
        },
        "3": {
            title: "Corniche Luxury Resort",
            price: "$200 / night",
            description: "A high-end resort with premium services and full sea view.",
            amenities: "Wi-Fi, Swimming Pool, Gym, Spa, Breakfast included",
            reviews: [
                { name: "Sara Abdullah", rating: "5.0", text: "The view was breathtaking! Very clean and quiet place." },
                { name: "Khaled Omar", rating: "4.0", text: "Great experience overall, host was very welcoming." }
            ]
        }
    };

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get("id") || "1";
    const place = placesData[placeId];

    if (place) {
        document.getElementById("place-title").innerText = place.title;
        document.getElementById("place-price").innerText = place.price;
        document.getElementById("place-desc").innerText = place.description;
        document.getElementById("place-amenities").innerText = place.amenities;

        const reviewsContainer = document.getElementById("reviews-list");
        if (reviewsContainer) {
            reviewsContainer.innerHTML = place.reviews.map(review => `
                <article class="review-card">
                    <h4>${review.name} <span class="rating-badge">★ ${review.rating}</span></h4>
                    <p>"${review.text}"</p>
                </article>
            `).join("");
        }
    }
});