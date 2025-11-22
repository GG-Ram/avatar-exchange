import React, { useState } from 'react';
import './StockRow.css';
import { buyStock, sellStock } from '../../services/stockService';
import { useUser } from '../../Hooks/userContext';

function StockRow({ stock, chartRef, onMouseMove, onMouseLeave, onRemove, isFavorite, onToggleFavorite, isFeatured }) {
    const [shares, setShares] = useState(1);
    const { fetchUser } = useUser();
    
    const isPositive = stock.change >= 0;
    const changeClass = isPositive ? 'positive' : 'negative';

    const handleBuy = async () => {
        try {
            const response = await buyStock(stock.symbol, shares);
            alert(response.message);
            fetchUser(); // Refresh user data
        } catch (error) {
            alert(error.response?.data?.error || 'Failed to buy stock');
        }
    };

    const handleSell = async () => {
        try {
            const response = await sellStock(stock.symbol, shares);
            alert(response.message);
            fetchUser(); // Refresh user data
        } catch (error) {
            alert(error.response?.data?.error || 'Failed to sell stock');
        }
    };

    return (
        <div className="stock-row">
            <div className="stock-badges">
                {isFeatured && (
                    <span className="stock-badge featured-badge" title="Featured Stock">
                        ⭐ Featured
                    </span>
                )}
                {onToggleFavorite && (
                    <button
                        className={`favorite-button ${isFavorite ? 'active' : ''}`}
                        onClick={() => onToggleFavorite(stock.symbol)}
                        title={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
                        aria-label={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
                    >
                        {isFavorite ? '❤️' : '🤍'}
                    </button>
                )}
            </div>
            <div className="stock-info">
                <div className="stock-header">
                    <div className="stock-name-section">
                        <h2 className="stock-symbol">{stock.symbol}</h2>
                        <p className="stock-name">{stock.name}</p>
                    </div>
                    <div className="stock-price-section">
                        <span className="stock-price">${stock.price}</span>
                        <span className={`stock-change ${changeClass}`}>
                            {isPositive ? '+' : ''}{stock.change} ({isPositive ? '+' : ''}{stock.changePercent}%)
                        </span>
                    </div>
                </div>

                <div className="buy-section">
                    <div className="shares-input-group">
                        <label htmlFor={`shares-${stock.symbol}`}>Shares:</label>
                        <input
                            id={`shares-${stock.symbol}`}
                            type="number"
                            min="1"
                            value={shares}
                            onChange={(e) => setShares(parseInt(e.target.value) || 1)}
                            className="shares-input"
                        />
                    </div>
                    <div className="total-cost">
                        Total: ${(stock.price * shares).toFixed(2)}
                    </div>
                    <div className="action-buttons">
                        <button className="buy-button" onClick={handleBuy}>
                            Buy {shares}
                        </button>
                        <button className="sell-button" onClick={handleSell}>
                            Sell {shares}
                        </button>
                    </div>
                </div>
            </div>

            <canvas
                ref={chartRef}
                width={400}
                height={100}
                className="stock-chart"
                onMouseMove={(e) => onMouseMove(stock.symbol, stock.graph, e)}
                onMouseLeave={() => onMouseLeave(stock.symbol)}
            />
        </div>
    );
}

export default StockRow;