from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import api
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Register blueprints
app.register_blueprint(api)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
