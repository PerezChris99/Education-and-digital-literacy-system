from flask import Flask, send_from_directory
from config import Config
import os
from flask_sqlalchemy import SQLAlchemy  # Import Flask-SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

from routes import api  # Import routes after initializing db

# Register blueprints
app.register_blueprint(api)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Serve cached content
@app.route('/offline_cache/<path:filename>')
def serve_cached_content(filename):
    cache_dir = os.path.join(app.root_path, 'offline_cache')
    return send_from_directory(cache_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)
