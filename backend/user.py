from accessory import Accessory
from stock import Stock

class Portfolio_Stock:
    def __init__(self, shares, stock_data: Stock):
        self.shares = shares
        self.stock_data = stock_data

    def to_dict(self):
        current_price = getattr(self.stock_data, "price", 0) or 0
        current_value = current_price * self.shares
        total_cost = current_price * self.shares
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
            # use get and compare string forms to avoid int/str mismatch
            if pid_str is not None and str(item.get("id")) == pid_str:
                product = item
                product_index = i
                break

        # fallback: try matching by name if frontend sent accessory_name instead of id
        if product is None and isinstance(product_id, str):
            for i, item in enumerate(products_list):
                if item.get("name") == product_id:
                    product = item
                    product_index = i
                    break

        if product is None:
            return {
                "success": False,
                "message": "Product not found!"
            }

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

    def buy_stock(self, stock: Stock, shares):
        """
        Add shares of stock to positions. Uses stock.price provided by caller as the current price.
        Does not track historical buyPrice.
        """
        if shares <= 0:
            return False

        total_cost = stock.price * shares
        if self.balance < total_cost:
            return False

        # If we already own this stock, increase shares and update stored current price
        for position in self.positions:
            if position.stock_data.symbol == stock.symbol:
                position.shares += shares
                # update stored current price so frontend sees latest
                position.stock_data.price = stock.price
                self.balance -= total_cost
                return True

        # new position
        new_position = Portfolio_Stock(shares=shares, stock_data=stock)
        self.positions.append(new_position)
        self.balance -= total_cost
        return True
                
    def sell_stock(self, stock: Stock, shares):
        """
        Sell shares at the current price provided by caller (stock.price).
        Proceeds = stock.price * shares are added to balance.
        Stored position price is updated to the current price before removing shares.
        """
        if shares <= 0:
            return False

        for i, position in enumerate(self.positions):
            if position.stock_data.symbol == stock.symbol:
                if shares <= position.shares:
                    # ensure stored position reflects latest market price
                    position.stock_data.price = float(stock.price)

                    proceeds = float(stock.price) * shares
                    self.balance = round(self.balance + proceeds, 2)

                    position.shares -= shares
                    if position.shares == 0:
                        self.positions.pop(i)
                    return True
                else:
                    return False  # Not enough shares
        return False  # Stock not in positions

    def to_dict(self):
        return {
            "balance": round(self.balance, 2),
            "positions": [p.to_dict() for p in self.positions],
            "inventory": self.inventory
        }