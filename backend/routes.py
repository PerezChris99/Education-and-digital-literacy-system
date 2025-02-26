from flask import Blueprint, jsonify, request
from models import User, Course, Grade, Announcement
from app import db
from utils import hash_password, generate_jwt_token, decode_jwt_token
from ai_recommendations import get_user_course_recommendations
from offline_cache import cache_course_content, get_cached_content_url
import jwt
import os
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

api = Blueprint('api', __name__)

# Helper function to check admin role
def is_admin(token):
    try:
        payload = decode_jwt_token(token)
        user_id = payload['user_id']
        user = User.query.get(user_id)
        return user and user.role == 'admin'
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    except Exception as e:
        print(f"Error decoding token: {e}")
        return False

# Helper function to check teacher role
def is_teacher(token):
    try:
        payload = decode_jwt_token(token)
        user_id = payload['user_id']
        user = User.query.get(user_id)
        return user and user.role == 'teacher'
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    except Exception as e:
        print(f"Error decoding token: {e}")
        return False

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    language_preference = data.get('language_preference', 'en')  # Get language preference
    role = data.get('role', 'student') # Get user role
    profile_picture = data.get('profile_picture')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password, language_preference=language_preference, role=role, profile_picture=profile_picture)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error registering user: {e}")
        return jsonify({'message': 'Registration failed'}), 500

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if user and utils.verify_password(password, user.password):
        token = generate_jwt_token(user.id)
        user.last_login = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Login successful', 'token': token, 'role': user.role}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@api.route('/courses', methods=['GET'])
def list_courses():
    courses = Course.query.all()
    course_list = [{'id': course.id, 'name': course.name, 'description': course.description} for course in courses]
    return jsonify(course_list), 200

@api.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    try:
        course = Course.query.get(course_id)
        if course:
            # Get cached URLs
            cached_video_url = get_cached_content_url(f'video_{course_id}.mp4')
            cached_pdf_url = get_cached_content_url(f'pdf_{course_id}.pdf')

            return jsonify({
                'id': course.id,
                'name': course.name,
                'description': course.description,
                'content': course.content,
                'video_url': cached_video_url if cached_video_url else course.video_url,
                'pdf_url': cached_pdf_url if cached_pdf_url else course.pdf_url,
                'quiz_data': course.quiz_data
            }), 200
        else:
            return jsonify({'message': 'Course not found'}), 404
    except Exception as e:
        print(f"Error getting course: {e}")
        return jsonify({'message': 'Failed to retrieve course'}), 500

@api.route('/recommendations', methods=['GET'])
def get_recommendations():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        payload = decode_jwt_token(token)
        user_id = payload['user_id']
        recommendations = get_user_course_recommendations(user_id)
        return jsonify(recommendations), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return jsonify({'message': 'Failed to retrieve recommendations'}), 500

@api.route('/cache/<int:course_id>', methods=['POST'])
def cache_content(course_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401
    try:
        payload = decode_jwt_token(token)
        user_id = payload['user_id']
        user = User.query.get(user_id)
        if not user or user.role == 'student':
            return jsonify({'message': 'Unauthorized'}), 403
        if cache_course_content(course_id):
            return jsonify({'message': f'Course {course_id} cached successfully'}), 200
        else:
            return jsonify({'message': f'Failed to cache course {course_id}'}), 500
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    except Exception as e:
        print(f"Error caching content: {e}")
        return jsonify({'message': 'Caching failed'}), 500

@api.route('/teacher/dashboard', methods=['GET'])
def teacher_dashboard():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        payload = decode_jwt_token(token)
        user_id = payload['user_id']
        user = User.query.get(user_id)

        if not user or user.role != 'teacher':
            return jsonify({'message': 'Unauthorized'}), 403

        # Get courses taught by the teacher
        courses = Course.query.filter(Course.users.any(id=user_id)).all()
        course_list = [{'id': course.id, 'name': course.name, 'description': course.description} for course in courses]

        # Get students enrolled in those courses
        student_list = []
        for course in courses:
            for student in course.users:
                if student.role == 'student':
                    # Fetch the grade for the student in the course
                    grade = Grade.query.filter_by(user_id=student.id, course_id=course.id).first()
                    student_info = {
                        'id': student.id,
                        'username': student.username,
                        'course_name': course.name,
                        'grade': grade.grade if grade else 'N/A'
                    }
                    student_list.append(student_info)

        return jsonify({'courses': course_list, 'students': student_list}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    except Exception as e:
        print(f"Error getting teacher dashboard: {e}")
        return jsonify({'message': 'Failed to retrieve teacher dashboard'}), 500

@api.route('/courses', methods=['POST'])
def create_course():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        payload = decode_jwt_token(token)
        user_id = payload['user_id']
        user = User.query.get(user_id)

        if not user or user.role != 'teacher':
            return jsonify({'message': 'Unauthorized'}), 403

        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        content = data.get('content')
        video_url = data.get('video_url')
        pdf_url = data.get('pdf_url')
        quiz_data = data.get('quiz_data')

        if not name or not content:
            return jsonify({'message': 'Name and content are required'}), 400

        new_course = Course(name=name, description=description, content=content, video_url=video_url, pdf_url=pdf_url, quiz_data=quiz_data)
        new_course.users.append(user)  # Add the teacher to the course
        db.session.add(new_course)
        db.session.commit()

        return jsonify({'message': 'Course created successfully'}), 201
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    except Exception as e:
        db.session.rollback()
        print(f"Error creating course: {e}")
        return jsonify({'message': 'Failed to create course'}), 500

@api.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    if not is_admin(token):
        return jsonify({'message': 'Unauthorized'}), 403

    try:
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'message': 'Course not found'}), 404

        data = request.get_json()
        course.name = data.get('name', course.name)
        course.description = data.get('description', course.description)
        course.content = data.get('content', course.content)
        course.video_url = data.get('video_url', course.video_url)
        course.pdf_url = data.get('pdf_url', course.pdf_url)
        course.quiz_data = data.get('quiz_data', course.quiz_data)  # Update quiz data

        db.session.commit()

        return jsonify({'message': 'Course updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating course: {e}")
        return jsonify({'message': 'Failed to update course'}), 500

@api.route('/user/profile', methods=['GET'])
def get_user_profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        payload = decode_jwt_token(token)
        user_id = payload['user_id']
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        return jsonify({
            'username': user.username,
            'role': user.role,
            'language_preference': user.language_preference,
            'profile_picture': user.profile_picture
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    except Exception as e:
        print(f"Error getting user profile: {e}")
        return jsonify({'message': 'Failed to retrieve user profile'}), 500

@api.route('/user/profile/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    if not is_admin(token):
        return jsonify({'message': 'Unauthorized'}), 403

    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        data = request.get_json()
        # Only admins can change user roles
        if 'role' in data:
            user.role = data['role']
        user.language_preference = data.get('language_preference', user.language_preference)
        user.profile_picture = data.get('profile_picture', user.profile_picture)
        db.session.commit()

        return jsonify({'message': 'User profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating user profile: {e}")
        return jsonify({'message': 'Failed to update user profile'}), 500

@api.route('/admin/users', methods=['GET'])
def list_users():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    if not is_admin(token):
        return jsonify({'message': 'Unauthorized'}), 403

    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'role': user.role} for user in users]
    return jsonify(user_list), 200

@api.route('/admin/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    if not is_admin(token):
        return jsonify({'message': 'Unauthorized'}), 403

    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting user: {e}")
        return jsonify({'message': 'Failed to delete user'}), 500

@api.route('/grades', methods=['POST'])
def add_grade():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    if not is_teacher(token) and not is_admin(token):
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    user_id = data.get('user_id')
    course_id = data.get('course_id')
    grade = data.get('grade')

    if not user_id or not course_id or not grade:
        return jsonify({'message': 'User ID, Course ID, and Grade are required'}), 400

    try:
        new_grade = Grade(user_id=user_id, course_id=course_id, grade=grade)
        db.session.add(new_grade)
        db.session.commit()
        return jsonify({'message': 'Grade added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error adding grade: {e}")
        return jsonify({'message': 'Failed to add grade'}), 500

@api.route('/student/dashboard', methods=['GET'])
def student_dashboard():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        payload = decode_jwt_token(token)
        user_id = payload['user_id']
        user = User.query.get(user_id)

        if not user or user.role != 'student':
            return jsonify({'message': 'Unauthorized'}), 403

        # Get courses the student is enrolled in
        courses = Course.query.filter(Course.users.any(id=user_id)).all()
        course_list = [{'id': course.id, 'name': course.name, 'description': course.description} for course in courses]

        # Get recommended courses
        recommendations = get_user_course_recommendations(user_id)

        # Get announcements for enrolled courses
        announcements = []
        for course in courses:
            course_announcements = Announcement.query.filter_by(course_id=course.id).order_by(Announcement.timestamp.desc()).limit(5).all()
            announcements.extend([{'title': a.title, 'content': a.content, 'timestamp': a.timestamp} for a in course_announcements])

        # Get grades for enrolled courses
        grades = Grade.query.filter_by(user_id=user_id).all()
        grade_list = [{'course_id': g.course_id, 'grade': g.grade} for g in grades]

        return jsonify({
            'username': user.username,
            'profile_picture': user.profile_picture,
            'courses': course_list,
            'recommendations': recommendations,
            'announcements': announcements,
            'grades': grade_list
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    except Exception as e:
        print(f"Error getting student dashboard: {e}")
        return jsonify({'message': 'Failed to retrieve student dashboard'}), 500

@api.route('/announcements', methods=['POST'])
def create_announcement():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    if not is_teacher(token) and not is_admin(token):
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    course_id = data.get('course_id')

    if not title or not content or not course_id:
        return jsonify({'message': 'Title, content, and course ID are required'}), 400

    try:
        new_announcement = Announcement(title=title, content=content, course_id=course_id)
        db.session.add(new_announcement)
        db.session.commit()
        return jsonify({'message': 'Announcement created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating announcement: {e}")
        return jsonify({'message': 'Failed to create announcement'}), 500
