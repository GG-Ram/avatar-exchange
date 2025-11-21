"""User-related routes"""

from flask import Blueprint, jsonify
from auth_helpers import login_required, get_current_user

user_bp = Blueprint('user', __name__)

@user_bp.route("/api/userData")
@login_required
def get_user_data():
    """Get current authenticated user data"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())

