import yfinance as yf

class Stock:
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name
        self.ticker = yf.Ticker(symbol)
        self.price = None

    def last_n_minutes_data(self, newest, n):
        """Fetch last 5 minutes of 1-minute interval data"""
        data = self.ticker.history(period="2d", interval="1m")
        last_n = data.iloc[newest-n:newest] #goes from n-120 to n
        closes = last_n["Close"].tolist()
        self.price = closes[-1]
        change = closes[-1] - closes[0]
        change_percent = (change / closes[0]) * 100
        return {
            "symbol": self.symbol,
            "name": self.name,
            "price": round(self.price, 2),
            "change": round(change, 2),
            "changePercent": round(change_percent, 2),
            "graph": [round(c, 2) for c in closes]
        }
