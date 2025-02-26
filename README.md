# Education & Digital Literacy System

A system to address overcrowded schools, limited digital access, and teacher training in Uganda.

## Features

-   Web-Based E-Learning Platform
    -   Student, teacher, and admin dashboards
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
-   Signaling Server: Node.js with WebSocket

## Account Roles and Permissions

-   **Student:**
    -   Access to course content
    -   Enroll in courses
    -   Take quizzes
    -   View recommended courses
    -   Set language preference
-   **Teacher:**
    -   All student permissions
    -   Create and manage courses
    -   Access teacher dashboard
-   **Admin:**
    -   All teacher permissions
    -   User management (create, edit, delete users)
    -   Update course content

## Setup Instructions

1.  Install Python dependencies: `pip install -r requirements.txt`
2.  Set up the database (PostgreSQL/MongoDB) and update the connection string in `backend/config.py`.
3.  Run the Flask application: `python backend/app.py`
4.  Open `frontend/index.html` in your browser.
5.  To access the teacher dashboard, create a user with the `teacher` role in the database and navigate to `frontend/teacher_dashboard.html`.
6.  To access the admin dashboard, create a user with the `admin` role in the database and navigate to `frontend/admin_dashboard.html`.

## Additional Setup

### WebRTC Virtual Classrooms
To enable virtual classrooms, you need a WebRTC signaling server.
1.  Install Node.js dependencies: `cd signaling_server && npm install ws`
2.  Run the signaling server: `node signaling_server/server.js`
3.  Update the `signalingServerUrl` variable in `frontend/webrtc.js` with the URL of your signaling server.

### Offline Content Caching
Cached content is stored in the `offline_cache` directory. The server serves this content via the `/offline_cache/<filename>` route.

## Low Bandwidth Mode
To enable low bandwidth mode, click the "Toggle Low Bandwidth Mode" button. This will reduce image quality, disable videos, and simplify styles.

## API Endpoints

-   `/register` (POST): Register a new user.
    -   Requires: `username`, `password`, `language_preference`, `role`
-   `/login` (POST): Login a user.
    -   Requires: `username`, `password`
-   `/courses` (GET): List all courses.
-   `/courses/<course_id>` (GET): Get a specific course.
-   `/recommendations` (GET): Get recommended courses for the user.
    -   Requires: `Authorization` header with JWT token
-   `/cache/<course_id>` (POST): Cache course content.
    -   Requires: `Authorization` header with JWT token, teacher or admin role
-   `/teacher/dashboard` (GET): Get teacher dashboard.
    -   Requires: `Authorization` header with JWT token, teacher role
-   `/courses` (POST): Create a new course.
    -   Requires: `Authorization` header with JWT token, teacher role
    -   Requires: `name`, `description`, `content`, `video_url`, `pdf_url`, `quiz_data`
-   `/courses/<course_id>` (PUT): Update a course.
    -   Requires: `Authorization` header with JWT token, admin role
    -   Requires: `name`, `description`, `content`, `video_url`, `pdf_url`, `quiz_data`
-   `/user/profile` (GET): Get user profile.
    -   Requires: `Authorization` header with JWT token
-   `/user/profile/<user_id>` (PUT): Update user profile (Admin only).
    -   Requires: `Authorization` header with JWT token, admin role
    -   Requires: `role`, `language_preference`
-   `/admin/users` (GET): List all users (Admin only).
    -   Requires: `Authorization` header with JWT token, admin role
-   `/admin/users/<user_id>` (DELETE): Delete a user (Admin only).
    -   Requires: `Authorization` header with JWT token, admin role

## Error Handling
The backend API includes robust error handling to provide informative responses in case of issues such as invalid credentials, missing tokens, unauthorized access, or database errors.

## WebRTC Implementation
The WebRTC implementation provides basic video and audio communication. To improve the virtual classroom experience, consider implementing features such as:
- Screen sharing
- Text chat
- User muting
- Recording