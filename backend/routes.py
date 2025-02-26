from flask import Blueprint, jsonify, request
from models import User, Course
from app import db
from utils import hash_password, generate_jwt_token, decode_jwt_token
from ai_recommendations import get_user_course_recommendations
from offline_cache import cache_course_content
import jwt

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    language_preference = data.get('language_preference', 'en')  # Get language preference

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password, language_preference=language_preference)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

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
    course = Course.query.get(course_id)
    if course:
        return jsonify({'id': course.id, 'name': course.name, 'description': course.description, 'content': course.content}), 200
    else:
        return jsonify({'message': 'Course not found'}), 404

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

@api.route('/cache/<int:course_id>', methods=['POST'])
def cache_content(course_id):
    if cache_course_content(course_id):
        return jsonify({'message': f'Course {course_id} cached successfully'}), 200
    else:
        return jsonify({'message': f'Failed to cache course {course_id}'}), 500

@api.route('/teacher/dashboard', methods=['GET'])
def teacher_dashboard():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        payload = decode_jwt_token(token)
        user_id = payload['user_id']
        user = User.query.get(user_id)

        if not user or not user.is_teacher:
            return jsonify({'message': 'Unauthorized'}), 403

        courses = Course.query.filter(Course.users.any(id=user_id)).all()
        course_list = [{'id': course.id, 'name': course.name, 'description': course.description} for course in courses]

        return jsonify({'courses': course_list}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

@api.route('/courses', methods=['POST'])
def create_course():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        payload = decode_jwt_token(token)
        user_id = payload['user_id']
        user = User.query.get(user_id)

        if not user or not user.is_teacher:
            return jsonify({'message': 'Unauthorized'}), 403

        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        content = data.get('content')
        video_url = data.get('video_url')
        pdf_url = data.get('pdf_url')

        if not name or not content:
            return jsonify({'message': 'Name and content are required'}), 400

        new_course = Course(name=name, description=description, content=content, video_url=video_url, pdf_url=pdf_url)
        new_course.users.append(user)  # Add the teacher to the course
        db.session.add(new_course)
        db.session.commit()

        return jsonify({'message': 'Course created successfully'}), 201
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

@api.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        payload = decode_jwt_token(token)
        user_id = payload['user_id']
        user = User.query.get(user_id)

        if not user or not user.is_teacher:
            return jsonify({'message': 'Unauthorized'}), 403

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
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

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
            'language_preference': user.language_preference
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

@api.route('/user/profile', methods=['PUT'])
def update_user_profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        payload = decode_jwt_token(token)
        user_id = payload['user_id']
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        data = request.get_json()
        user.language_preference = data.get('language_preference', user.language_preference)
        db.session.commit()

        return jsonify({'message': 'User profile updated successfully'}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
