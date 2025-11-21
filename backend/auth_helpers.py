"""Authentication helper functions and decorators"""

from functools import wraps
from flask import jsonify, request
from models.user_model import UserModel
from user import User
from jwt_utils import get_token_from_request, verify_token

def login_required(f):
    """Decorator to require authentication for routes using JWT"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_request()
        
        if not token:
            return jsonify({"error": "Authentication required"}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Store user info in request context for use in route
        request.current_user_id = payload['user_id']
        request.current_username = payload['username']
        
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get the currently authenticated user as a User object from JWT token"""
    token = get_token_from_request()
    
    if not token:
        return None
    
    payload = verify_token(token)
    if not payload:
        return None
    
    user_id = payload['user_id']
    user_data = UserModel.find_by_id(user_id)
    
    if not user_data:
        return None
    
    # Create User object with MongoDB integration
    user = User(user_id=user_id)
    return user

def get_current_user_id():
    """Get the current user's ID from JWT token"""
    token = get_token_from_request()
    if not token:
        return None
    
    payload = verify_token(token)
    if not payload:
        return None
    
    return payload.get('user_id', None)

