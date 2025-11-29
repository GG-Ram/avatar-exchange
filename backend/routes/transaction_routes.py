"""Transaction history routes"""

from flask import Blueprint, jsonify
from models import state
from auth_helpers import login_required, get_current_user
from datetime import datetime

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/api/transactions', methods=['GET'])
@login_required
def get_transactions():
    """Get all transactions for the current user"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    try:
        # Get transactions from user model
        from models.user_model import UserModel
        user_data = UserModel.find_by_id(user.user_id)
        transactions = user_data.get("transactions", [])
        
        # Sort by date (newest first)
        transactions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return jsonify({
            'success': True,
            'transactions': transactions
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@transaction_bp.route('/api/transactions/export', methods=['GET'])
@login_required
def export_transactions():
    """Export transactions as CSV"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    try:
        from models.user_model import UserModel
        user_data = UserModel.find_by_id(user.user_id)
        transactions = user_data.get("transactions", [])
        
        # Generate CSV content
        csv_lines = ["Date,Type,Symbol,Shares,Price,Total,Profit/Loss"]
        for txn in transactions:
            date = txn.get("timestamp", "")
            txn_type = txn.get("type", "")
            symbol = txn.get("symbol", "")
            shares = txn.get("shares", 0)
            price = txn.get("price", 0)
            total = txn.get("total", 0)
            profit_loss = txn.get("profit_loss", 0)
            
            csv_lines.append(f"{date},{txn_type},{symbol},{shares},{price},{total},{profit_loss}")
        
        csv_content = "\n".join(csv_lines)
        
        return jsonify({
            'success': True,
            'csv': csv_content
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

