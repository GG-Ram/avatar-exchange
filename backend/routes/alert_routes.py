"""Price alert routes"""

from flask import Blueprint, jsonify, request
from models import state
from auth_helpers import login_required, get_current_user
from datetime import datetime

alert_bp = Blueprint('alerts', __name__)

@alert_bp.route('/api/alerts', methods=['GET'])
@login_required
def get_alerts():
    """Get all alerts for the current user"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    try:
        from models.user_model import UserModel
        user_data = UserModel.find_by_id(user.user_id)
        alerts = user_data.get("alerts", [])
        
        return jsonify({
            'success': True,
            'alerts': alerts
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@alert_bp.route('/api/alerts', methods=['POST'])
@login_required
def create_alert():
    """Create a new price alert"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    symbol = data.get('symbol', '').upper()
    condition = data.get('condition', 'above')  # 'above' or 'below'
    price = float(data.get('price', 0))
    
    if not symbol or price <= 0:
        return jsonify({"error": "Invalid alert parameters"}), 400
    
    try:
        from models.user_model import UserModel
        user_data = UserModel.find_by_id(user.user_id)
        alerts = user_data.get("alerts", [])
        
        alert = {
            "id": len(alerts) + 1,
            "symbol": symbol,
            "condition": condition,
            "price": price,
            "active": True,
            "created_at": datetime.utcnow().isoformat(),
            "triggered": False
        }
        
        alerts.append(alert)
        UserModel.update_user(user.user_id, {"alerts": alerts})
        
        return jsonify({
            'success': True,
            'alert': alert
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@alert_bp.route('/api/alerts/<int:alert_id>', methods=['DELETE'])
@login_required
def delete_alert(alert_id):
    """Delete an alert"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    try:
        from models.user_model import UserModel
        user_data = UserModel.find_by_id(user.user_id)
        alerts = user_data.get("alerts", [])
        
        alerts = [a for a in alerts if a.get("id") != alert_id]
        UserModel.update_user(user.user_id, {"alerts": alerts})
        
        return jsonify({
            'success': True
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

