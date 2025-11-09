from accessory import Accessory
from stock import Stock

class Portfolio_Stock:
    def __init__(self, shares, stock_data: Stock, buyPrice=None):
        self.shares = shares
        self.stock_data = stock_data
        # Track average purchase price per share
        self.buyPrice = buyPrice or getattr(stock_data, "price", 0)

    def to_dict(self):
        current_price = getattr(self.stock_data, "price", 0) or 0
        current_value = current_price * self.shares
        total_cost = self.buyPrice * self.shares
        profit = current_value - total_cost
        profit_percent = (profit / total_cost * 100) if total_cost > 0 else 0

        return {
            "shares": self.shares,
            "symbol": self.stock_data.symbol,
            "name": self.stock_data.name,
            "price": round(current_price, 2),
            "totalValue": round(current_value, 2),
            "totalCost": round(total_cost, 2),
            "profit": round(profit, 2),
            "profitPercent": round(profit_percent, 2),
            "stock_data": {
                "symbol": self.stock_data.symbol,
                "name": self.stock_data.name,
                "price": round(current_price, 2),
            }
        }

class User:
    def __init__(self, balance=500):
        self.balance = balance
        self.positions = []  # list[Portfolio_Stock]
        self.inventory = []

    # ----------------- Shop / Inventory -----------------
    def buy_product(self, product_id, products_list):
        """
        Buy a product from the shop and add it to user's inventory.
        Accepts numeric or string IDs (compares as strings to avoid type-mismatch).
        """
        product = None
        product_index = None

        # Normalize product_id for comparison
        pid_str = None if product_id is None else str(product_id)

        for i, item in enumerate(products_list):
            if pid_str is not None and str(item.get("id")) == pid_str:
                product = item
                product_index = i
                break

        # fallback: match by name
        if product is None and isinstance(product_id, str):
            for i, item in enumerate(products_list):
                if item.get("name") == product_id:
                    product = item
                    product_index = i
                    break

        if product is None:
            return {"success": False, "message": "Product not found!"}

        price = float(product.get("price", 0))
        if self.balance < price:
            return {
                "success": False,
                "message": f"Not enough money! You need ${price} but only have ${self.balance}"
            }

        self.balance -= price
        products_list.pop(product_index)
        self.inventory.append(product)

        return {
            "success": True,
            "message": f"Successfully purchased {product.get('emoji','')} {product.get('name','')}!",
            "product": product,
            "new_balance": round(self.balance, 2)
        }

    # ----------------- Stock Trading -----------------
    def buy_stock(self, stock: Stock, shares: int):
        """Buy shares of a stock using live price."""
        cost = stock.price * shares
        if self.balance < cost:
            return False

        self.balance -= cost

        # Update existing stock in portfolio if already owned
        for position in self.positions:
            if position.stock_data.symbol == stock.symbol:
                total_shares = position.shares + shares
                # update average buyPrice
                position.buyPrice = (
                    (position.buyPrice * position.shares + stock.price * shares)
                    / total_shares
                )
                position.shares = total_shares
                return True

        # New stock
        self.positions.append(Portfolio_Stock(shares, stock, stock.price))
        return True

    def sell_stock(self, symbol: str, shares: int):
        for position in self.positions:
            if position.stock_data.symbol == symbol:
                if position.shares >= shares:
                    print(f"\n{'='*50}")
                    print(f"🔴 SELLING {shares} shares of {symbol}")
                    print(f"💰 Balance BEFORE sell: ${self.balance}")
                    print(f"📊 Original Buy Price: ${position.buyPrice}")
                    
                    # Get the latest price from the market
                    position.stock_data.update_price()  # fetch latest price
                    current_price = position.stock_data.price
                    
                    print(f"📈 Current Market Price: ${current_price}")
                    print(f"💵 Money to receive: {shares} shares × ${current_price} = ${current_price * shares}")
                    
                    # Update balance with current market value
                    self.balance += current_price * shares
                    
                    print(f"💰 Balance AFTER sell: ${self.balance}")
                    print(f"📊 Profit/Loss per share: ${current_price - position.buyPrice}")
                    print(f"📊 Total Profit/Loss: ${(current_price - position.buyPrice) * shares}")
                    print(f"{'='*50}\n")
                    
                    # Reduce shares in portfolio
                    position.shares -= shares
                    if position.shares == 0:
                        self.positions.remove(position)
                    return True
        return False



    # ----------------- Serialization -----------------
    def to_dict(self):
        return {
            "balance": round(self.balance, 2),
            "positions": [p.to_dict() for p in self.positions],
            "inventory": self.inventory
        }
