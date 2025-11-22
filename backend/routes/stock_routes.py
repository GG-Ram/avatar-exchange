"""Stock trading routes"""

from flask import Blueprint, jsonify, request
from models import state
from stock import Stock
from config import STOCKS
from auth_helpers import login_required, get_current_user
import yfinance as yf

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
        # Try to get stock name from yfinance if not in config
        name = STOCKS.get(symbol)
        if not name:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                name = info.get('longName') or info.get('shortName') or symbol
            except:
                name = symbol
        stock = Stock(symbol, name, fetch_on_init=False)
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

@stock_bp.route("/api/stock/<symbol>")
def get_stock(symbol):
    """Get data for a specific stock by symbol"""
    symbol = symbol.upper().strip()
    
    if not symbol:
        return jsonify({"error": "Invalid symbol"}), 400
    
    try:
        # Check if stock is in cache, otherwise create new one
        if symbol in state.stock_cache:
            stock = state.stock_cache[symbol]
        else:
            # Try to get stock name from yfinance
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                name = info.get('longName') or info.get('shortName') or symbol
            except:
                name = symbol
            
            # Create stock and add to cache
            stock = Stock(symbol, name, fetch_on_init=False)
            state.stock_cache[symbol] = stock
        
        # Get last 120 minutes ending at current_index
        data = stock.last_n_minutes_data(newest=state.current_index, n=120)
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return jsonify({
            "symbol": symbol,
            "name": symbol,
            "price": 0,
            "change": 0,
            "changePercent": 0,
            "graph": [0]*120,
            "error": True,
            "message": f"Failed to fetch stock data: {str(e)}"
        }), 500

@stock_bp.route("/api/stocks/prices", methods=['POST'])
def get_stock_prices():
    """Get current prices for a list of stock symbols"""
    data = request.get_json()
    symbols = data.get('symbols', [])
    
    if not symbols or not isinstance(symbols, list):
        return jsonify({"error": "Invalid symbols list"}), 400
    
    result = {}
    
    for symbol in symbols:
        symbol = symbol.upper().strip()
        try:
            # Check if stock is in cache, otherwise create new one
            if symbol in state.stock_cache:
                stock = state.stock_cache[symbol]
            else:
                # Try to get stock name from yfinance
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    name = info.get('longName') or info.get('shortName') or symbol
                except:
                    name = symbol
                
                # Create stock and add to cache
                stock = Stock(symbol, name, fetch_on_init=False)
                state.stock_cache[symbol] = stock
            
            # Get current price data
            stock_data = stock.last_n_minutes_data(newest=state.current_index, n=1)
            result[symbol] = {
                "price": stock_data.get('price', 0),
                "change": stock_data.get('change', 0),
                "changePercent": stock_data.get('changePercent', 0)
            }
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            result[symbol] = {
                "price": 0,
                "change": 0,
                "changePercent": 0,
                "error": True
            }
    
    return jsonify(result)

