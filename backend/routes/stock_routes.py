"""Stock trading routes"""

from flask import Blueprint, jsonify, request
from models import state
from stock import Stock
from config import STOCKS
from auth_helpers import login_required, get_current_user

stock_bp = Blueprint('stocks', __name__)

@stock_bp.route("/api/stocks")
def get_stocks():
    """Get all stock data"""
    result = []

    for symbol, name in STOCKS.items():
        try:
            # Use cached stock object instead of creating new one
            stock = state.stock_cache[symbol]
            
            # Get last 120 minutes ending at current_index
            data = stock.last_n_minutes_data(newest=state.current_index, n=120)
            result.append(data)
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            result.append({
                "symbol": symbol,
                "name": name,
                "price": 0,
                "change": 0,
                "changePercent": 0,
                "graph": [0]*5,
                "error": True
            })

    # Increment index for next request
    if state.current_index < state.MAX_INDEX:
        state.current_index += 1

    return jsonify(result)

@stock_bp.route('/api/buy', methods=['POST'])
@login_required
def buy_stock():
    """Buy shares of a stock"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    symbol = data.get('symbol')
    shares = data.get('shares')

    if not symbol or not shares or shares <= 0:
        return jsonify({"error": "Missing symbol or shares"}), 400

    # Use cached stock or create new one if not in cache
    if symbol in state.stock_cache:
        stock = state.stock_cache[symbol]
    else:
        stock = Stock(symbol, STOCKS.get(symbol, symbol), fetch_on_init=False)
        state.stock_cache[symbol] = stock

    try:
        # Use simulated price from current_index instead of real yfinance
        stock_data = stock.last_n_minutes_data(newest=state.current_index, n=1)
        latest_price = stock_data['price']
        stock.price = latest_price

        success = user.buy_stock(stock, shares)

        if success:
            return jsonify({
                "success": True,
                "message": f"Bought {shares} shares of {symbol}",
                "user": user.to_dict()
            }), 200
        else:
            return jsonify({"success": False, "error": "Insufficient funds"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@stock_bp.route('/api/sell', methods=['POST'])
@login_required
def sell_stock():
    """Sell shares of a stock"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    symbol = data.get('symbol')
    shares = data.get('shares')

    if not symbol or not shares or shares <= 0:
        return jsonify({"error": "Invalid symbol or shares"}), 400

    # Find the position and update its price with simulated data
    for position in user.positions:
        if position.stock_data.symbol == symbol:
            # Use simulated price from current_index
            stock_data = position.stock_data.last_n_minutes_data(newest=state.current_index, n=1)
            position.stock_data.price = stock_data['price']
            break

    success = user.sell_stock(symbol, shares)
    if success:
        return jsonify({
            "success": True,
            "message": f"Sold {shares} shares of {symbol}",
            "user": user.to_dict()
        }), 200
    else:
        return jsonify({"success": False, "error": "Insufficient shares or stock not owned"}), 400

