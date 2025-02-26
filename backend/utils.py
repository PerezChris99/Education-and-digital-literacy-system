import bcrypt
import jwt
from datetime import datetime, timedelta
from config import Config

# Utility functions (e.g., for password hashing, JWT generation)
def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password, hashed_password):
    # Verify the password against the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_jwt_token(user_id):
    # Generate a JWT token
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token expiration time
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt_token(token):
    # Decode the JWT token
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError
