document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    if (token && role === 'admin') {
        fetchUsers(token);
    } else {
        window.location.href = '/index.html'; // Redirect if not admin or no token
    }
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
