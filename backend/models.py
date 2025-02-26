from app import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    role = Column(String(20), default='student')
    courses = relationship("Course", secondary="user_courses", back_populates="users")
    is_teacher = Column(Boolean, default=False)  # New field to indicate if the user is a teacher
    language_preference = Column(String(10), default='en')  # User's preferred language

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

    def __repr__(self):
        return f'<Course {self.name}>'

# Association table for many-to-many relationship between users and courses
user_courses = db.Table('user_courses',
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('course.id'), primary_key=True)
)
