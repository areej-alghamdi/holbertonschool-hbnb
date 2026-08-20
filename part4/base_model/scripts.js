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
    const apiUrl = 'http://127.0.0.1:5000/api/v1/login';

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