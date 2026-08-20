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