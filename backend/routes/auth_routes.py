"""Authentication routes (register, login, logout)"""

from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from user import User
from jwt_utils import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not username or not email or not password:
            return jsonify({
                "success": False,
                "error": "Username, email, and password are required"
            }), 400
        
        if len(password) < 6:
            return jsonify({
                "success": False,
                "error": "Password must be at least 6 characters"
            }), 400
        
        # Check if username already exists
        if UserModel.find_by_username(username):
            return jsonify({
                "success": False,
                "error": "Username already taken"
            }), 400
        
        # Check if email already exists
        if UserModel.find_by_email(email):
            return jsonify({
                "success": False,
                "error": "Email already registered"
            }), 400
        
        # Create new user
        user_doc = UserModel.create_user(
            username=username,
            email=email,
            password=password,
            balance=500.0  # Starting balance
        )
        
        # Generate JWT token for the new user
        token = generate_token(user_doc['_id'], username)
        
        # Load user object for response
        user = User(user_id=user_doc['_id'])
        
        return jsonify({
            "success": True,
            "message": "User registered successfully",
            "token": token,
            "user": {
                "id": user_doc['_id'],
                "username": username,
                "email": email
            },
            "userData": user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    """Login an existing user"""
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({
                "success": False,
                "error": "Username and password are required"
            }), 400
        
        # Find user by username
        user_data = UserModel.find_by_username(username)
        
        if not user_data:
            return jsonify({
                "success": False,
                "error": "Invalid username or password"
            }), 401
        
        # Verify password
        if not UserModel.verify_password(user_data['password'], password):
            return jsonify({
                "success": False,
                "error": "Invalid username or password"
            }), 401
        
        # Generate JWT token
        token = generate_token(user_data['_id'], user_data['username'])
        
        # Load user object for response
        user = User(user_id=user_data['_id'])
        
        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user_data['_id'],
                "username": user_data['username'],
                "email": user_data['email']
            },
            "userData": user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    """Logout the current user (client should delete token)"""
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    }), 200

@auth_bp.route('/api/me', methods=['GET'])
def get_current_user():
    """Get the current authenticated user"""
    from jwt_utils import get_token_from_request, verify_token
    
    token = get_token_from_request()
    
    if not token:
        return jsonify({
            "success": False,
            "error": "Not authenticated"
        }), 401
    
    payload = verify_token(token)
    if not payload:
        return jsonify({
            "success": False,
            "error": "Invalid or expired token"
        }), 401
    
    try:
        user_data = UserModel.find_by_id(payload['user_id'])
        
        if not user_data:
            return jsonify({
                "success": False,
                "error": "User not found"
            }), 404
        
        # Load user object for response
        user = User(user_id=user_data['_id'])
        
        return jsonify({
            "success": True,
            "user": {
                "id": user_data['_id'],
                "username": user_data['username'],
                "email": user_data['email']
            },
            "userData": user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@auth_bp.route('/api/debug/token', methods=['GET'])
def debug_token():
    """Debug endpoint to check token status"""
    from jwt_utils import get_token_from_request, verify_token
    
    token = get_token_from_request()
    if token:
        payload = verify_token(token)
        return jsonify({
            "has_token": True,
            "token_valid": payload is not None,
            "payload": payload
        }), 200
    else:
        return jsonify({
            "has_token": False,
            "token_valid": False
        }), 200

