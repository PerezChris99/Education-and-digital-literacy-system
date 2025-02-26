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
-   Signaling Server: Node.js with WebSocket

## Setup Instructions

1.  Install Python dependencies: `pip install -r requirements.txt`
2.  Set up the database (PostgreSQL/MongoDB) and update the connection string in `backend/config.py`.
3.  Run the Flask application: `python backend/app.py`
4.  Open `frontend/index.html` in your browser.
5.  To access the teacher dashboard, create a user with `is_teacher` set to `true` in the database and navigate to `teacher_dashboard.html`.

## Additional Setup

### WebRTC Virtual Classrooms
To enable virtual classrooms, you need a WebRTC signaling server.
1.  Install Node.js dependencies: `cd signaling_server && npm install ws`
2.  Run the signaling server: `node signaling_server/server.js`
3.  Update the `signalingServerUrl` variable in `frontend/webrtc.js` with the URL of your signaling server.

### Offline Content Caching
Cached content is stored in the `offline_cache` directory. The server serves this content via the `/offline_cache/<filename>` route.
