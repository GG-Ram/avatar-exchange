import yfinance as yf
import time
import numpy as np
import pandas as pd

class Stock:
    CACHE_DURATION = 60  # seconds

    def __init__(self, symbol, name, fetch_on_init=True):
        self.symbol = symbol
        self.name = name
        self.ticker = yf.Ticker(symbol)
        self.price = 0
        self.last_fetch = 0
        self.history_cache = None
        self.fetch_on_init = fetch_on_init
        
        if fetch_on_init:
            self.update_price()  # initial fetch
        else:
            # Generate simulated data if not fetching
            self._generate_simulated_data()

    def _generate_simulated_data(self):
        """Generate simulated stock data for development/testing"""
        # Generate 500 minutes of simulated price data
        base_price = 100.0 + hash(self.symbol) % 200  # Different base price per symbol
        np.random.seed(hash(self.symbol) % 1000)  # Consistent seed per symbol
        
        # Generate random walk price data
        minutes = 500
        returns = np.random.normal(0, 0.5, minutes)  # Small random changes
        prices = [base_price]
        for ret in returns:
            prices.append(prices[-1] * (1 + ret / 100))
        
        # Create a DataFrame-like structure
        timestamps = pd.date_range(end=pd.Timestamp.now(), periods=minutes, freq='1min')
        self.history_cache = pd.DataFrame({'Close': prices[:minutes]}, index=timestamps)
        self.price = float(prices[-1])
        self.last_fetch = time.time()

    def fetch_latest_price(self):
        """Fetch latest price only if cache expired"""
        now = time.time()
        if now - self.last_fetch < self.CACHE_DURATION and self.price != 0 and self.history_cache is not None:
            return self.price  # use cached price

        try:
            history = self.ticker.history(period="1d", interval="1m")
            if history.empty or history is None:
                # Fallback to simulated data if fetch fails
                if self.history_cache is None:
                    self._generate_simulated_data()
                return self.price
            self.price = float(history['Close'].iloc[-1])
            self.history_cache = history  # cache full history
            self.last_fetch = now
            return self.price
        except Exception as e:
            # Silently fall back to simulated data
            if self.history_cache is None:
                self._generate_simulated_data()
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
