"""Mommy character routes"""

from flask import Blueprint, jsonify, request
from models import state
from accessory import ALL_ACCESSORIES

mommy_bp = Blueprint('mommy', __name__)

@mommy_bp.route('/api/mommy', methods=['GET'])
def get_mommy():
    """Get current mommy state"""
    try:
        return jsonify(state.mommy_character.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mommy_bp.route('/api/mommy/equip', methods=['POST'])
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
        for acc in state.mommy_character.owned_accessories:
            if acc.name == accessory_name:
                accessory = acc
                break
        
        if not accessory:
            return jsonify({
                'success': False,
                'message': f'Accessory "{accessory_name}" not found in inventory'
            }), 404
        
        success = state.mommy_character.equip_accessory(accessory, slot)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Equipped {accessory_name}',
                'mommy': state.mommy_character.to_dict()
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

@mommy_bp.route('/api/mommy/unequip', methods=['POST'])
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
        
        success = state.mommy_character.unequip_slot(slot)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Unequipped {slot}',
                'mommy': state.mommy_character.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'No accessory in {slot} slot'
            }), 400
            
    except Exception as e:
        print(f"❌ Error in unequip_accessory: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@mommy_bp.route('/api/mommy/owned', methods=['GET'])
def get_owned_accessories():
    """Get all owned accessories"""
    try:
        return jsonify({
            'owned_accessories': [
                {
                    'id': acc.id,
                    'name': acc.name,
                    'category': acc.category,
                    'price': acc.price,
                    'image': acc.image,
                    'frontimg': acc.frontimg,
                    'backimg': acc.backimg
                }
                for acc in state.mommy_character.owned_accessories
            ]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mommy_bp.route('/api/mommy/addAccessory', methods=['POST'])
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
        
        success = state.mommy_character.add_owned_accessory(accessory)
        
        return jsonify({
            'success': True,
            'message': f'Added {accessory_name} to inventory',
            'mommy': state.mommy_character.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

