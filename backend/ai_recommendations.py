from models import User, Course, user_courses
from app import db
from sqlalchemy import func

def get_user_course_recommendations(user_id):
    """
    Recommend courses to a user based on collaborative filtering and content-based filtering.
    """
    user = User.query.get(user_id)
    if not user:
        return []

    # Get courses the user is already enrolled in
    enrolled_course_ids = [course.id for course in user.courses]

    # Collaborative Filtering: Find other users who have similar course enrollments
    similar_users = db.session.query(
        user_courses.c.user_id,
        func.count(user_courses.c.course_id).label('course_count')
    ).filter(
        user_courses.c.course_id.in_([course.id for course in user.courses]),
        user_courses.c.user_id != user_id
    ).group_by(user_courses.c.user_id).order_by(func.count(user_courses.c.course_id).desc()).limit(10).all()

    recommended_course_ids_cf = set()
    for similar_user_id, _ in similar_users:
        # Get courses that similar users have taken but the current user hasn't
        courses_taken_by_similar_user = db.session.query(Course.id).join(user_courses).filter(
            user_courses.c.user_id == similar_user_id,
            Course.id.notin_(enrolled_course_ids)
        ).all()
        recommended_course_ids_cf.update([course_id for course_id, in courses_taken_by_similar_user])

    # Content-Based Filtering: Recommend courses with similar descriptions
    user_enrolled_courses = User.courses
    keywords = []
    for course in user_enrolled_courses:
        keywords.extend(course.description.split())

    # Find courses that contain any of the keywords
    recommended_course_ids_cb = db.session.query(Course.id).filter(
        Course.description.like(f"%{'%'.join(keywords)}%"),
        Course.id.notin_(enrolled_course_ids)
    ).limit(5).all()

    recommended_course_ids_cb = [course_id for course_id, in recommended_course_ids_cb]

    # Combine recommendations from both methods
    recommended_course_ids = recommended_course_ids_cf.union(recommended_course_ids_cb)

    # Fetch the recommended courses
    recommended_courses = Course.query.filter(Course.id.in_(recommended_course_ids)).limit(5).all()

    return [{'id': course.id, 'name': course.name, 'description': course.description} for course in recommended_courses]
