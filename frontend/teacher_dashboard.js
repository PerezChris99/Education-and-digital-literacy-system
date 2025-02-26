document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    if (token) {
        fetchTeacherDashboard(token);
    } else {
        window.location.href = '/index.html'; // Redirect to login if no token
    }

    document.getElementById('create-course-form').addEventListener('submit', function(event) {
        event.preventDefault();
        createCourse(token);
    });
});

function fetchTeacherDashboard(token) {
    fetch('/teacher/dashboard', {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            return;
        }
        const courseList = document.getElementById('course-list');
        data.courses.forEach(course => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `${course.name} - ${course.description}`;
            courseList.appendChild(listItem);
        });
    });
}

function createCourse(token) {
    const name = document.getElementById('course-name').value;
    const description = document.getElementById('course-description').value;
    const content = document.getElementById('course-content').value;
    const video_url = document.getElementById('course-video-url').value;
    const pdf_url = document.getElementById('course-pdf-url').value;

    fetch('/courses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ name, description, content, video_url, pdf_url })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchTeacherDashboard(token); // Refresh the course list
    });
}
