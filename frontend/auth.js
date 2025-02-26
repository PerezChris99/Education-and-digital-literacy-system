// Authentication logic (e.g., login, registration)
function register() {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const language_preference = document.getElementById('language-preference').value;
    const role = document.getElementById('role').value;

    const profilePictureInput = document.getElementById('profile-picture');
    const profile_picture = profilePictureInput.files[0];

    // Convert image to base64
    const reader = new FileReader();

    reader.onloadend = function() {
        const base64String = reader.result;
        sendRegistrationRequest(username, password, language_preference, role, base64String);
    }

    if (profile_picture) {
        reader.readAsDataURL(profile_picture);
    } else {
        sendRegistrationRequest(username, password, language_preference, role, null);
    }
}

function sendRegistrationRequest(username, password, language_preference, role, profile_picture) {
    fetch('/register', {
        method: 'POST',
        body: JSON.stringify({ username, password, language_preference, role, profile_picture }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        window.location.href = '/index.html';
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
