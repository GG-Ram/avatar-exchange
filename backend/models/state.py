"""Global application state management"""

from stock import Stock
from user import User
from mommy import Mommy
from config import STOCKS, CURRENT_INDEX, MAX_INDEX

# Global user instance
new_user = User(balance=500)

# Global mommy character instance
mommy_character = Mommy()

# Global index for simulating "live" minutes
current_index = CURRENT_INDEX

# MAX_INDEX is imported from config and available for use
# Export for use in routes
__all__ = ['new_user', 'mommy_character', 'current_index', 'stock_cache', 'MAX_INDEX']

# Cache Stock objects to avoid creating new ones on every request
stock_cache = {}
for symbol, name in STOCKS.items():
    # Create stocks without fetching on init to avoid rate limiting
    stock_cache[symbol] = Stock(symbol, name, fetch_on_init=False)

