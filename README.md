# Education & Digital Literacy System

A system to address overcrowded schools, limited digital access, and teacher training in Uganda.

## Features

-   Web-Based E-Learning Platform
    -   Student and teacher dashboards
    -   User authentication (JWT-based)
    -   Interactive course content (videos, quizzes, PDF notes)
    -   Live and recorded virtual classrooms (integrate WebRTC)
    -   Multilingual support (English, Luganda, Swahili)
    -   Low-bandwidth mode with text-based learning
    -   AI-Powered Recommendations
    -   Offline Content Caching

## Technologies Used

-   Frontend: JavaScript
-   Backend: Python-Flask
-   Database: PostgreSQL/MongoDB (to be configured)

## Setup Instructions

1.  Install Python dependencies: `pip install -r requirements.txt`
2.  Set up the database (PostgreSQL/MongoDB) and update the connection string in `backend/config.py`.
3.  Run the Flask application: `python backend/app.py`
4.  Open `frontend/index.html` in your browser.
5.  To access the teacher dashboard, create a user with `is_teacher` set to `true` in the database and navigate to `teacher_dashboard.html`.
