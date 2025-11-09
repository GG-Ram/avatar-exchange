from flask import Flask, jsonify, request
from flask_cors import CORS
from stock import Stock
from user import User
from shopdata import products
from mommy import Mommy
from accessory import ALL_ACCESSORIES


app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

STOCKS = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "GOOG": "Alphabet Inc.",
    "TSLA": "Tesla Inc.",
}
new_user = User(balance=5000)
mommy_character = Mommy()

# Global index for simulating “live” minutes
current_index = 153
MAX_INDEX = 400

@app.route("/api/stocks")
def get_stocks():
    global current_index

    result = []

    for symbol, name in STOCKS.items():
        try:
            stock = Stock(symbol, name)
            # Get last 120 minutes ending at current_index
            data = stock.last_n_minutes_data(newest=current_index, n=120)
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
    if current_index < MAX_INDEX:
        current_index += 1

    return jsonify(result)

@app.route("/api/userData")
def get_user_data():
 # CHANGE BALANCE HERE
    return jsonify(new_user.to_dict())

@app.route('/api/buy', methods=['POST'])
def buy_stock():
    data = request.get_json()
    symbol = data.get('symbol')
    shares = data.get('shares')

    # Validate input
    if not symbol or not shares:
        return jsonify({"error": "Missing symbol or shares"}), 400
    if shares <= 0:
        return jsonify({"error": "Shares must be positive"}), 400

    stock = Stock(symbol, STOCKS.get(symbol, symbol))

    try:
        history = stock.ticker.history(period="1d", interval="1m")
        if history.empty:
            return jsonify({"error": "No price data"}), 500
        latest_price = float(history['Close'].iloc[-1])
        stock.price = latest_price

        success = new_user.buy_stock(stock, shares)

        if success:
            return jsonify({
                "success": True,
                "message": f"Bought {shares} shares of {symbol}",
                "user": new_user.to_dict()
            }), 200
        else:
            return jsonify({"success": False, "error": "Insufficient funds"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sell', methods=['POST'])
def sell_stock():
    data = request.get_json()
    symbol = data.get('symbol')
    shares = data.get('shares')

    # Validate input
    if not symbol or not shares:
        return jsonify({"error": "Missing symbol or shares"}), 400
    if shares <= 0:
        return jsonify({"error": "Shares must be positive"}), 400

    stock = Stock(symbol, STOCKS.get(symbol, symbol))

    try:
        history = stock.ticker.history(period="1d", interval="1m")
        if history.empty:
            return jsonify({"error": "No price data"}), 500
        latest_price = float(history['Close'].iloc[-1])
        stock.price = latest_price

        success = new_user.sell_stock(stock, shares)

        if success:
            return jsonify({
                "success": True,
                "message": f"Sold {shares} shares of {symbol}",
                "user": new_user.to_dict()
            }), 200
        else:
            return jsonify({"success": False, "error": "Insufficient shares or stock not owned"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def fetchAccessories():
    return products

@app.route('/api/getAccessories', methods=['GET'])
def get_accessories():
    try:
        return jsonify(products), 200  # products is your global shop list
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/buyAccessory', methods=['POST'])
def buy_accessory():
    try:
        data = request.get_json()
        product_id = data.get('id')
        
        global products  # Access shop products
        
        result = new_user.buy_product(product_id, products)

        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message'],
                'new_balance': new_user.balance
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/mommy', methods=['GET'])
def get_mommy():
    """Get current mommy state"""
    try:
        return jsonify(mommy_character.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mommy/equip', methods=['POST'])
def equip_accessory():
    """Equip an accessory to mommy"""
    try:
        data = request.get_json()
        accessory_name = data.get('accessory_name')
        slot = data.get('slot')
        
        if not accessory_name or not slot:
            return jsonify({
                'success': False,
                'message': 'Missing accessory_name or slot'
            }), 400
        
        # Find the accessory by name from owned accessories
        accessory = None
        for acc in mommy_character.owned_accessories:
            if acc.name == accessory_name:
                accessory = acc
                break
        
        if not accessory:
            return jsonify({
                'success': False,
                'message': f'Accessory "{accessory_name}" not found in inventory'
            }), 404
        
        success = mommy_character.equip_accessory(accessory, slot)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Equipped {accessory_name}',
                'mommy': mommy_character.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to equip accessory'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/mommy/unequip', methods=['POST'])
def unequip_accessory():
    """Unequip an accessory from mommy"""
    try:
        data = request.get_json()
        slot = data.get('slot')
        
        if not slot:
            return jsonify({
                'success': False,
                'message': 'Missing slot'
            }), 400
        
        success = mommy_character.unequip_slot(slot)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Unequipped {slot}',
                'mommy': mommy_character.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'No accessory in {slot} slot'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/mommy/owned', methods=['GET'])
def get_owned_accessories():
    """Get all owned accessories"""
    try:
        return jsonify({
            'owned_accessories': [
                {
                    'name': acc.name,
                    'price': acc.price,
                    'front': acc.front,
                    'back': acc.back
                }
                for acc in mommy_character.owned_accessories
            ]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mommy/addAccessory', methods=['POST'])
def add_accessory_to_mommy():
    """Add an accessory to mommy's owned collection (for when buying from shop)"""
    try:
        data = request.get_json()
        accessory_name = data.get('accessory_name')
        
        if not accessory_name:
            return jsonify({
                'success': False,
                'message': 'Missing accessory_name'
            }), 400
        
        # Find accessory from global accessory list
        accessory = None
        
        for acc in ALL_ACCESSORIES:
            if acc.name == accessory_name:
                accessory = acc
                break
        
        if not accessory:
            return jsonify({
                'success': False,
                'message': 'Accessory not found'
            }), 404
        
        success = mommy_character.add_owned_accessory(accessory)
        
        return jsonify({
            'success': True,
            'message': f'Added {accessory_name} to inventory',
            'mommy': mommy_character.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500




if __name__ == "__main__":
    app.run(debug=True)
