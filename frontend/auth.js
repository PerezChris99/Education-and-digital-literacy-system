// Authentication logic (e.g., login, registration)
function register() {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const language_preference = document.getElementById('language-preference').value;

    fetch('/register', {
        method: 'POST',
        body: JSON.stringify({ username, password, language_preference }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
}

function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    fetch('/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('role', data.role);
            window.location.href = '/dashboard';
        } else {
            alert(data.message);
        }
    });
}
