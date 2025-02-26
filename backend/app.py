from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from routes import api
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

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
