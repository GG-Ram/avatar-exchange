"""Shop and accessory routes"""

from flask import Blueprint, jsonify, request
from models import state
from shopdata import products
from accessory import ALL_ACCESSORIES

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/api/getAccessories', methods=['GET'])
def get_accessories():
    """Get all available accessories"""
    try:
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@shop_bp.route('/api/buyAccessory', methods=['POST'])
def buy_accessory():
    """Buy an accessory from the shop"""
    try:
        data = request.get_json()
        product_id = data.get('id')
        
        print(f"🛒 Buying accessory with ID: {product_id}")
        
        result = state.new_user.buy_product(product_id, products)
        
        print(f"🛒 Purchase result: {result}")

        if result['success']:
            # Find the accessory that was just purchased
            purchased_accessory = None
            for acc in ALL_ACCESSORIES:
                if acc.id == product_id:
                    purchased_accessory = acc
                    break
            
            print(f"🛒 Found accessory: {purchased_accessory.name if purchased_accessory else 'NOT FOUND'}")
            
            # Add it to mommy's owned accessories
            if purchased_accessory:
                success = state.mommy_character.add_owned_accessory(purchased_accessory)
                print(f"🛒 Added to mommy: {success}")
                print(f"🛒 Mommy now owns {len(state.mommy_character.owned_accessories)} accessories")
            
            return jsonify({
                'success': True,
                'message': result['message'],
                'new_balance': state.new_user.balance
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400

    except Exception as e:
        print(f"❌ Error in buyAccessory: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

