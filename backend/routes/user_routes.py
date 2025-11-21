"""User-related routes"""

from flask import Blueprint, jsonify
from models import state

user_bp = Blueprint('user', __name__)

@user_bp.route("/api/userData")
def get_user_data():
    """Get current user data"""
    # CHANGE BALANCE HERE
    return jsonify(state.new_user.to_dict())

