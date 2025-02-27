document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    if (token && role === 'admin') {
        fetchUsers(token);
        fetchCourses(token);
    } else {
        window.location.href = '/index.html'; // Redirect if not admin or no token
    }

    document.getElementById('user-management-form').addEventListener('submit', function(event) {
        event.preventDefault();
        createUser(token);
    });

    document.getElementById('course-management-form').addEventListener('submit', function(event) {
        event.preventDefault();
        createCourse(token);
    });
});

function fetchUsers(token) {
    fetch('/admin/users', {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(response => response.json())
    .then(users => {
        const userList = document.getElementById('user-list');
        userList.innerHTML = ''; // Clear existing list
        users.forEach(user => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `${user.username} - ${user.role} 
                                  <button onclick="editUser(${user.id})">Edit</button>
                                  <button onclick="deleteUser(${user.id})">Delete</button>`;
            userList.appendChild(listItem);
        });
    });
}

function editUser(userId) {
    const token = localStorage.getItem('token');
    const newRole = prompt("Enter new role (student, teacher, admin):");
    if (newRole) {
        updateUserRole(userId, newRole, token);
    }
}

function updateUserRole(userId, newRole, token) {
    fetch(`/user/profile/${userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ role: newRole })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchUsers(token); // Refresh user list
    });
}

function deleteUser(userId) {
    const token = localStorage.getItem('token');
    if (confirm("Are you sure you want to delete this user?")) {
        fetch(`/admin/users/${userId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchUsers(token); // Refresh user list
        });
    }
}

function createUser(token) {
    const username = document.getElementById('new-username').value;
    const password = document.getElementById('new-password').value;
    const language_preference = document.getElementById('new-language-preference').value;
    const role = document.getElementById('new-role').value;

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ username, password, language_preference, role })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchUsers(token); // Refresh user list
    });
}

function createCourse(token) {
    const name = document.getElementById('course-name').value;
    const description = document.getElementById('course-description').value;
    const content = document.getElementById('course-content').value;
    const video_url = document.getElementById('course-video-url').value;
    const pdf_url = document.getElementById('course-pdf-url').value;
    const quiz_data = document.getElementById('course-quiz-data').value;

    fetch('/courses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ name, description, content, video_url, pdf_url, quiz_data })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchCourses(token); // Refresh the course list
    });
}

function fetchCourses(token) {
    fetch('/courses', {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(response => response.json())
    .then(courses => {
        const courseList = document.getElementById('course-list');
        courseList.innerHTML = '';
        courses.forEach(course => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `${course.name} - ${course.description} <button onclick="editCourse(${course.id})">Edit</button>`;
            courseList.appendChild(listItem);
        });
    });
}

function editCourse(courseId) {
     // Implement course editing functionality (e.g., open a modal with course details)
    alert('Editing course - Implement course editing functionality');
}
