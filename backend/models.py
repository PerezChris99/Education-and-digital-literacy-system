from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, JSON, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db  # Import db from app.py

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    role = Column(String(20), default='student')  # role can be 'student', 'teacher', or 'admin'
    courses = relationship("Course", secondary="user_courses", back_populates="users")
    language_preference = Column(String(10), default='en')  # User's preferred language
    grades = relationship("Grade", back_populates="user")
    last_login = Column(DateTime, default=datetime.utcnow)
    profile_picture = Column(String(200), nullable=True) # URL to profile picture

    def __repr__(self):
        return f'<User {self.username}>'

class Course(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    content = Column(Text)  # Store course content (e.g., video URLs, text)
    users = relationship("User", secondary="user_courses", back_populates="courses")
    video_url = Column(String(200))  # URL for video content
    pdf_url = Column(String(200))  # URL for PDF notes
    quiz_data = Column(JSON)  # Store quiz data as JSON
    announcements = relationship("Announcement", back_populates="course")

    def __repr__(self):
        return f'<Course {self.name}>'

class Grade(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    grade = Column(Float)
    user = relationship("User", back_populates="grades")
    course = relationship("Course")
    timestamp = Column(DateTime, default=datetime.utcnow)

class Announcement(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    course_id = Column(Integer, ForeignKey('course.id'))
    course = relationship("Course", back_populates="announcements")

# Association table for many-to-many relationship between users and courses
user_courses = db.Table('user_courses',
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('course.id'), primary_key=True)
)
