// Feedback logic
function submitFeedback(courseId) {
    const rating = document.getElementById('feedback-rating').value;
    const comment = document.getElementById('feedback-comment').value;
    const token = localStorage.getItem('token');

    fetch('/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ course_id: courseId, rating: rating, comment: comment })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
}
