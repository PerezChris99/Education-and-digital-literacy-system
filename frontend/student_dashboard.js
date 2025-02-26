document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    if (token && role === 'student') {
        fetchStudentDashboard(token);
    } else {
        window.location.href = '/index.html'; // Redirect if not student or no token
    }
});

function fetchStudentDashboard(token) {
    fetch('/student/dashboard', {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('welcome-message').innerText = `Welcome, ${data.username}!`;
        document.getElementById('profile-picture').src = data.profile_picture || 'default_profile.png';

        const courseList = document.getElementById('course-list');
        courseList.innerHTML = '';
        data.courses.forEach(course => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<a href="#" onclick="loadCourseContent(${course.id})">${course.name}</a> - ${course.description}`;
            courseList.appendChild(listItem);
        });

        const recommendationList = document.getElementById('recommendation-list');
        recommendationList.innerHTML = '';
        data.recommendations.forEach(course => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<a href="#" onclick="loadCourseContent(${course.id})">${course.name}</a> - ${course.description} (Recommended)`;
            recommendationList.appendChild(listItem);
        });

        const announcementList = document.getElementById('announcement-list');
        announcementList.innerHTML = '';
        data.announcements.forEach(announcement => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<strong>${announcement.title}</strong><br>${announcement.content} - ${new Date(announcement.timestamp).toLocaleString()}`;
            announcementList.appendChild(listItem);
        });

        const gradeList = document.getElementById('grade-list');
        gradeList.innerHTML = '';
        data.grades.forEach(grade => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `Course ID: ${grade.course_id} - Grade: ${grade.grade}`;
            gradeList.appendChild(listItem);
        });

    })
    .catch(error => {
        console.error('Error fetching student dashboard:', error);
        alert('Failed to load student dashboard data.');
    });
}
