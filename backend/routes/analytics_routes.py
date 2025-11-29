"""Analytics routes"""

from flask import Blueprint, jsonify
from models import state
from auth_helpers import login_required, get_current_user

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/api/analytics', methods=['GET'])
@login_required
def get_analytics():
    """Get analytics data for the current user"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    try:
        from models.user_model import UserModel
        user_data = UserModel.find_by_id(user.user_id)
        if not user_data:
            return jsonify({"error": "User data not found"}), 404
        
        transactions = user_data.get("transactions", [])
        positions = user_data.get("positions", [])
        
        # Calculate metrics with defaults
        total_invested = sum(float(t.get("total", 0)) for t in transactions if t.get("type") == "BUY")
        total_returned = sum(float(t.get("total", 0)) for t in transactions if t.get("type") == "SELL")
        total_profit_loss = sum(float(t.get("profit_loss", 0)) for t in transactions if t.get("type") == "SELL")
        
        # Portfolio value - calculate from current positions
        portfolio_value = 0
        for pos in positions:
            shares = float(pos.get("shares", 0))
            buy_price = float(pos.get("buyPrice", 0))
            portfolio_value += shares * buy_price
        
        # Win/Loss ratio
        sell_transactions = [t for t in transactions if t.get("type") == "SELL"]
        wins = sum(1 for t in sell_transactions if float(t.get("profit_loss", 0)) > 0)
        losses = sum(1 for t in sell_transactions if float(t.get("profit_loss", 0)) < 0)
        win_loss_ratio = (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0
        
        # Best/Worst performers
        sell_with_profit = [t for t in sell_transactions if float(t.get("profit_loss", 0)) != 0]
        best = None
        worst = None
        if sell_with_profit:
            best = max(sell_with_profit, key=lambda x: float(x.get("profit_loss", 0)))
            worst = min(sell_with_profit, key=lambda x: float(x.get("profit_loss", 0)))
        
        return jsonify({
            'success': True,
            'analytics': {
                'total_invested': round(total_invested, 2),
                'total_returned': round(total_returned, 2),
                'total_profit_loss': round(total_profit_loss, 2),
                'portfolio_value': round(portfolio_value, 2),
                'win_loss_ratio': round(win_loss_ratio * 100, 2),
                'wins': wins,
                'losses': losses,
                'best_performer': best,
                'worst_performer': worst,
                'total_transactions': len(transactions)
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

