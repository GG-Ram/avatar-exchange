"""Financial advice routes"""

from flask import Blueprint, jsonify
from models import state
from aiadvice import get_funny_financial_advice
from auth_helpers import login_required, get_current_user

advice_bp = Blueprint('advice', __name__)

@advice_bp.route('/api/getAdvice', methods=['GET'])
@login_required
def get_advice():
    """Get funny AI financial advice based on user's portfolio"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    try:
        user_data = user.to_dict()
        advice = get_funny_financial_advice(user_data)
        
        return jsonify({
            'success': True,
            'advice': advice
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

