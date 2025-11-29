import React, { useEffect, useState } from "react";
import { getStockPrices, sellStock } from "../../services/stockService";
import { useUser } from "../../Hooks/userContext";
import "./Portfolio.css";

const Portfolio = () => {
  const { user, fetchUser } = useUser();
  const [stockPrices, setStockPrices] = useState({});
  const [loading, setLoading] = useState(true);
  const [selling, setSelling] = useState({});
  const [sellShares, setSellShares] = useState({});
  const [message, setMessage] = useState(null);

  useEffect(() => {
    const fetchStockPrices = async () => {
      if (!user?.positions || user.positions.length === 0) {
        setLoading(false);
        return;
      }

      try {
        // Get all symbols from user's positions
        const symbols = user.positions.map(p => p.stock_data?.symbol || p.stock_data?.symbol).filter(Boolean);
        
        if (symbols.length === 0) {
          setLoading(false);
          return;
        }

        // Fetch prices for all owned stocks
        const prices = await getStockPrices(symbols);
        setStockPrices(prices);
        setLoading(false);
      } catch (err) {
        console.error("[DEBUG] Error fetching stock prices:", err.message);
        setLoading(false);
      }
    };

    fetchStockPrices();
    const interval = setInterval(fetchStockPrices, 5000);
    return () => clearInterval(interval);
  }, [user?.positions]);

  const calculateTotalValue = () => {
    return (
      user?.positions?.reduce((total, position) => {
        const price =
          stockPrices[position.stock_data.symbol] ||
          position.stock_data.price;
        return total + position.shares * price;
      }, 0) || 0
    );
  };

  const handleSell = async (symbol, shares) => {
    if (!shares || shares <= 0) {
      setMessage({ type: 'error', text: 'Please enter a valid number of shares' });
      setTimeout(() => setMessage(null), 3000);
      return;
    }

    setSelling({ ...selling, [symbol]: true });
    setMessage(null);
    
    try {
      const response = await sellStock(symbol, shares);
      setMessage({ type: 'success', text: response.message || `Successfully sold ${shares} shares of ${symbol}` });
      fetchUser();
      setSellShares({ ...sellShares, [symbol]: 1 });
      setTimeout(() => setMessage(null), 3000);
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.error || 'Failed to sell stock' });
      setTimeout(() => setMessage(null), 3000);
    } finally {
      setSelling({ ...selling, [symbol]: false });
    }
  };

  if (loading)
    return <div className="loading">Loading portfolio data...</div>;

  return (
    <div className="portfolio-container">
      <div className="portfolio-header">
        <h1>Your Portfolio</h1>
        <div className="balance-section">
          <div className="balance-card">
            <span className="label">Cash Balance</span>
            <span className="amount">${user?.balance?.toFixed(2)}</span>
          </div>
          <div className="balance-card">
            <span className="label">Total Portfolio Value</span>
            <span className="amount">${calculateTotalValue().toFixed(2)}</span>
          </div>
          <div className="balance-card total">
            <span className="label">Total Net Worth</span>
            <span className="amount">
              ${(calculateTotalValue() + (user?.balance || 0)).toFixed(2)}
            </span>
          </div>
        </div>
      </div>

      {message && (
        <div className={`portfolio-message ${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="holdings-section">
        <h2>Stock Holdings</h2>
        {user?.positions?.length > 0 ? (
          <div className="holdings-grid">
            {user.positions.map((position, i) => {
              const symbol = position.stock_data?.symbol || position.symbol;
              const priceData = stockPrices[symbol] || {};
              const price = priceData.price || position.stock_data?.price || position.price || 0;
              const buyPrice = position.buyPrice || position.totalCost / position.shares || 0;
              const totalValue = position.shares * price;
              const totalCost = position.totalCost || (buyPrice * position.shares);
              const profit = totalValue - totalCost;
              const profitPercent =
                totalCost > 0
                  ? (profit / totalCost) * 100
                  : 0;
              const sharesToSell = sellShares[symbol] || 1;

              return (
                <div key={i} className="holding-card">
                  <div className="holding-header">
                    <h3 className="stock-symbol">
                      {symbol}
                    </h3>
                    <span className="shares-badge">
                      {position.shares} shares
                    </span>
                  </div>
                  <div className="holding-details">
                    <div className="detail-row">
                      <span className="detail-label">Current Price:</span>
                      <span className="detail-value">
                        ${price.toFixed(2)}
                        {priceData.changePercent !== undefined && (
                          <span className={`price-change ${priceData.changePercent >= 0 ? 'positive' : 'negative'}`}>
                            {' '}({priceData.changePercent >= 0 ? '+' : ''}{priceData.changePercent?.toFixed(2)}%)
                          </span>
                        )}
                      </span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Avg Buy Price:</span>
                      <span className="detail-value">
                        ${buyPrice.toFixed(2)}
                      </span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Total Value:</span>
                      <span className="detail-value total">
                        ${totalValue.toFixed(2)}
                      </span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Profit/Loss:</span>
                      <span
                        className={`detail-value ${
                          profit >= 0 ? "positive" : "negative"
                        }`}
                      >
                        ${profit.toFixed(2)} ({profitPercent.toFixed(2)}%)
                      </span>
                    </div>
                  </div>
                  <div className="holding-actions">
                    <div className="sell-input-group">
                      <label htmlFor={`sell-shares-${symbol}`}>Sell Shares:</label>
                      <input
                        id={`sell-shares-${symbol}`}
                        type="number"
                        min="1"
                        max={position.shares}
                        value={sharesToSell}
                        onChange={(e) => setSellShares({ ...sellShares, [symbol]: Math.max(1, Math.min(position.shares, parseInt(e.target.value) || 1)) })}
                        className="sell-shares-input"
                        disabled={selling[symbol]}
                      />
                    </div>
                    <button
                      className="sell-button"
                      onClick={() => handleSell(symbol, sharesToSell)}
                      disabled={selling[symbol] || sharesToSell > position.shares}
                    >
                      {selling[symbol] ? 'Selling...' : `Sell ${sharesToSell}`}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="empty-state">
            <p>📈 No stocks in your portfolio yet!</p>
            <p>Start trading to build your portfolio.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Portfolio;
