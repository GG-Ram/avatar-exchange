import yfinance as yf
import time

class Stock:
    CACHE_DURATION = 60  # seconds

    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name
        self.ticker = yf.Ticker(symbol)
        self.price = 0
        self.last_fetch = 0
        self.history_cache = None
        self.update_price()  # initial fetch

    def fetch_latest_price(self):
        """Fetch latest price only if cache expired"""
        now = time.time()
        if now - self.last_fetch < self.CACHE_DURATION and self.price != 0:
            return self.price  # use cached price

        try:
            history = self.ticker.history(period="1d", interval="1m")
            if history.empty:
                return self.price  # fallback to old price
            self.price = float(history['Close'].iloc[-1])
            self.history_cache = history  # cache full history
            self.last_fetch = now
            return self.price
        except Exception as e:
            print(f"Error fetching price for {self.symbol}: {e}")
            return self.price

    def update_price(self):
        return self.fetch_latest_price()

    def last_n_minutes_data(self, newest, n=120):
        """
        Return last `n` minutes of stock data ending at index `newest`.
        Uses cached history to avoid repeated API calls.
        """
        try:
            if self.history_cache is None or self.price == 0:
                self.fetch_latest_price()

            history = self.history_cache
            if history is None or history.empty:
                return {
                    "symbol": self.symbol,
                    "name": self.name,
                    "price": 0,
                    "change": 0,
                    "changePercent": 0,
                    "graph": [0]*n,
                    "error": True
                }

            # take last n minutes ending at newest index
            data_slice = history['Close'].iloc[max(0, newest - n):newest]
            latest_price = float(data_slice.iloc[-1])
            self.price = latest_price  # update stock price

            start_price = float(data_slice.iloc[0])
            change = latest_price - start_price
            change_percent = (change / start_price * 100) if start_price != 0 else 0

            return {
                "symbol": self.symbol,
                "name": self.name,
                "price": round(latest_price, 2),
                "change": round(change, 2),
                "changePercent": round(change_percent, 2),
                "graph": [round(p, 2) for p in data_slice.tolist()],
                "error": False
            }

        except Exception as e:
            print(f"Error fetching last_n_minutes_data for {self.symbol}: {e}")
            return {
                "symbol": self.symbol,
                "name": self.name,
                "price": 0,
                "change": 0,
                "changePercent": 0,
                "graph": [0]*n,
                "error": True
            }
