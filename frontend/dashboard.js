// Dashboard logic (e.g., loading user-specific content)
document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    if (token) {
        if (role === 'teacher') {
            window.location.href = '/teacher_dashboard.html';
            return;
        }
         if (role === 'admin') {
            window.location.href = '/admin_dashboard.html';
            return;
        }
        getUserProfile(token);
        document.getElementById('content').innerText = "Welcome to your dashboard!";
        fetchRecommendations(token);
    } else {
        document.getElementById('content').innerText = "Please login to access the dashboard.";
    }
});

function getUserProfile(token) {
    fetch('/user/profile', {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(response => response.json())
    .then(data => {
        localStorage.setItem('language_preference', data.language_preference);
        translate(data.language_preference);
    });
}

function fetchRecommendations(token) {
    fetch('/recommendations', {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(response => response.json())
    .then(recommendations => {
        const courseList = document.getElementById('course-list');
        recommendations.forEach(course => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<a href="#" onclick="loadCourseContent(${course.id})">${course.name}</a> - ${course.description} (Recommended)`;
            courseList.appendChild(listItem);
        });
    });
}
