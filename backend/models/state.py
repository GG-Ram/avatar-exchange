"""Global application state management"""

from stock import Stock
from user import User
from mommy import Mommy
from config import STOCKS, CURRENT_INDEX, MAX_INDEX
from models.user_model import UserModel

# Global mommy character instance
mommy_character = Mommy()

# Global index for simulating "live" minutes
current_index = CURRENT_INDEX

# MAX_INDEX is imported from config and available for use

def get_or_create_default_user():
    """
    Get or create a default user in MongoDB.
    Uses a special username 'default_user' for the demo user.
    """
    # Try to find default user
    default_user = UserModel.find_by_username('default_user')
    
    if default_user:
        # Load user from MongoDB
        user = User(user_id=default_user['_id'])
    else:
        # Create new default user
        user_doc = UserModel.create_user(
            username='default_user',
            email='default@avatar-exchange.com',
            password='default_password',  # This will be hashed
            balance=500.0
        )
        user = User(user_id=user_doc['_id'])
    
    return user

# Global user instance (loaded from MongoDB)
new_user = get_or_create_default_user()

# Export for use in routes
__all__ = ['new_user', 'mommy_character', 'current_index', 'stock_cache', 'MAX_INDEX']

# Cache Stock objects to avoid creating new ones on every request
stock_cache = {}
for symbol, name in STOCKS.items():
    # Create stocks without fetching on init to avoid rate limiting
    stock_cache[symbol] = Stock(symbol, name, fetch_on_init=False)

