import os
import requests
from urllib.parse import urlparse

CACHE_DIR = 'offline_cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def cache_course_content(course_id):
    """
    Cache course content (video and PDF) locally.
    """
    from models import Course
    course = Course.query.get(course_id)
    if not course:
        return False

    if course.video_url:
        cache_file(course.video_url, os.path.join(CACHE_DIR, f'video_{course_id}.mp4'))
    if course.pdf_url:
        cache_file(course.pdf_url, os.path.join(CACHE_DIR, f'pdf_{course_id}.pdf'))
    if course.content:
        cache_text_content(course.content, os.path.join(CACHE_DIR, f'text_{course_id}.txt'))
    return True

def cache_file(url, filepath):
    """
    Download and cache a file.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Cached {url} to {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to cache {url}: {e}")

def cache_text_content(text, filepath):
    """
    Cache text content to a file.
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Cached text content to {filepath}")
    except Exception as e:
        print(f"Failed to cache text content: {e}")

def get_cached_content_url(filename):
    """
    Get the local URL for cached content.
    """
    filepath = os.path.join(CACHE_DIR, filename)
    if os.path.exists(filepath):
        return f'/offline_cache/{filename}'  # Serve files from a static route
    return None
