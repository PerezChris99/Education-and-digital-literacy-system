document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    if (token) {
        fetchTeacherDashboard(token);
        populateCourseSelect(token); // Populate course select for announcements
    } else {
        window.location.href = '/index.html'; // Redirect to login if no token
    }

    document.getElementById('create-course-form').addEventListener('submit', function(event) {
        event.preventDefault();
        createCourse(token);
    });

    document.getElementById('announcement-form').addEventListener('submit', function(event) {
        event.preventDefault();
        createAnnouncement(token);
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
        courseList.innerHTML = '';
        data.courses.forEach(course => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `${course.name} - ${course.description} <button onclick="editCourse(${course.id})">Edit</button>`;
            courseList.appendChild(listItem);
        });

        const studentList = document.getElementById('student-list');
        studentList.innerHTML = '';
        data.students.forEach(student => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `${student.username} - ${student.course_name} - Grade: ${student.grade}
                                  <button onclick="editGrade(${student.id}, ${course.id})">Edit Grade</button>`;
            studentList.appendChild(listItem);
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

function editGrade(studentId, courseId) {
    const token = localStorage.getItem('token');
    const newGrade = prompt("Enter new grade for the student:");
    if (newGrade) {
        updateGrade(studentId, courseId, newGrade, token);
    }
}

function updateGrade(studentId, courseId, newGrade, token) {
    fetch('/grades', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ user_id: studentId, course_id: courseId, grade: newGrade })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchTeacherDashboard(token); // Refresh the student list
    });
}

function createAnnouncement(token) {
    const title = document.getElementById('announcement-title').value;
    const content = document.getElementById('announcement-content').value;
    const courseId = document.getElementById('announcement-course').value;

    fetch('/announcements', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ title: title, content: content, course_id: courseId })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchTeacherDashboard(token); // Refresh the dashboard
    });
}

function populateCourseSelect(token) {
    fetch('/teacher/dashboard', {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(response => response.json())
    .then(data => {
        const courseSelect = document.getElementById('announcement-course');
        courseSelect.innerHTML = '';
        data.courses.forEach(course => {
            const option = document.createElement('option');
            option.value = course.id;
            option.text = course.name;
            courseSelect.appendChild(option);
        });
    });
}

function editCourse(courseId) {
    // Implement course editing functionality (e.g., open a modal with course details)
    alert('Editing course - Implement course editing functionality');
}
