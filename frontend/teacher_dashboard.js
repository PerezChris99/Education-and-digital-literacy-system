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
            listItem.innerHTML = `${course.name} - ${course.description} <button onclick="editCourse(${course.id})">Edit</button>`;
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

function editCourse(courseId) {
    // Implement course editing functionality (e.g., open a modal with course details)
    const token = localStorage.getItem('token');
    // For simplicity, let's just add a prompt for new quiz data
    const quizData = prompt("Enter quiz data as JSON:");
    if (quizData) {
        try {
            const parsedQuizData = JSON.parse(quizData);
            updateCourse(courseId, parsedQuizData, token);
        } catch (e) {
            alert("Invalid JSON format for quiz data.");
        }
    }
}

function updateCourse(courseId, quizData, token) {
    fetch(`/courses/${courseId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ quiz_data: quizData })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchTeacherDashboard(token); // Refresh the course list
    });
}
