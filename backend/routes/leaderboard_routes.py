"""Leaderboard routes"""

from flask import Blueprint, jsonify
from models import state
from auth_helpers import login_required
from database import db

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/api/leaderboard', methods=['GET'])
@login_required
def get_leaderboard():
    """Get leaderboard data"""
    try:
        # Get all users
        users = list(db.users.find({}))
        
        leaderboard = []
        for user in users:
            balance = user.get("balance", 0)
            positions = user.get("positions", [])
            
            # Calculate portfolio value
            portfolio_value = sum(
                p.get("shares", 0) * p.get("buyPrice", 0) 
                for p in positions
            )
            
            total_value = balance + portfolio_value
            
            # Calculate return percentage (simplified)
            transactions = user.get("transactions", [])
            total_invested = sum(t.get("total", 0) for t in transactions if t.get("type") == "BUY")
            total_profit = sum(t.get("profit_loss", 0) for t in transactions if t.get("type") == "SELL")
            return_percent = (total_profit / total_invested * 100) if total_invested > 0 else 0
            
            leaderboard.append({
                "username": user.get("username", "Unknown"),
                "balance": round(balance, 2),
                "portfolio_value": round(portfolio_value, 2),
                "total_value": round(total_value, 2),
                "return_percent": round(return_percent, 2)
            })
        
        # Sort by total value
        leaderboard.sort(key=lambda x: x["total_value"], reverse=True)
        
        return jsonify({
            'success': True,
            'leaderboard': leaderboard[:50]  # Top 50
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

