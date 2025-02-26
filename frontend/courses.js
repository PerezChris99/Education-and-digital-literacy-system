// Course-related logic (e.g., fetching course list, displaying content)
document.addEventListener('DOMContentLoaded', function() {
    fetchCourses();
});

function fetchCourses() {
    fetch('/courses')
    .then(response => response.json())
    .then(courses => {
        const courseList = document.getElementById('course-list');
        courses.forEach(course => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<a href="#" onclick="loadCourseContent(${course.id})">${course.name}</a> - ${course.description} <button onclick="cacheCourse(${course.id})">Cache</button>`;
            courseList.appendChild(listItem);
        });
    });
}

function loadCourseContent(courseId) {
    fetch(`/courses/${courseId}`)
    .then(response => response.json())
    .then(course => {
        let content = `<h2>${course.name}</h2><p>${course.content}</p>`;
        if (course.video_url) {
            content += `<video width="320" height="240" controls><source src="${course.video_url}" type="video/mp4">Your browser does not support the video tag.</video>`;
        }
        if (course.pdf_url) {
            content += `<a href="${course.pdf_url}" target="_blank">View PDF Notes</a>`;
        }
        document.getElementById('content').innerHTML = content;
    });
}

function cacheCourse(courseId) {
    fetch(`/cache/${courseId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
}
