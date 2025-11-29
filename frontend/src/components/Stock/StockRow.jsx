import React, { useState } from 'react';
import './StockRow.css';
import { buyStock, sellStock } from '../../services/stockService';
import { useUser } from '../../Hooks/userContext';

function StockRow({ stock, chartRef, onMouseMove, onMouseLeave, onRemove, isFavorite, onToggleFavorite, isFeatured, userShares }) {
    const [shares, setShares] = useState(1);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);
    const { fetchUser, user } = useUser();
    
    const isPositive = stock.change >= 0;
    const changeClass = isPositive ? 'positive' : 'negative';
    const totalCost = stock.price * shares;
    const canAfford = user?.balance >= totalCost;

    const handleBuy = async () => {
        if (!canAfford) {
            setMessage({ type: 'error', text: 'Insufficient funds' });
            setTimeout(() => setMessage(null), 3000);
            return;
        }
        
        setLoading(true);
        setMessage(null);
        try {
            const response = await buyStock(stock.symbol, shares);
            setMessage({ type: 'success', text: response.message || `Successfully bought ${shares} shares of ${stock.symbol}` });
            fetchUser(); // Refresh user data
            setTimeout(() => setMessage(null), 3000);
        } catch (error) {
            setMessage({ type: 'error', text: error.response?.data?.error || 'Failed to buy stock' });
            setTimeout(() => setMessage(null), 3000);
        } finally {
            setLoading(false);
        }
    };

    const handleSell = async () => {
        if (userShares < shares) {
            setMessage({ type: 'error', text: `You only own ${userShares} shares` });
            setTimeout(() => setMessage(null), 3000);
            return;
        }
        
        setLoading(true);
        setMessage(null);
        try {
            const response = await sellStock(stock.symbol, shares);
            setMessage({ type: 'success', text: response.message || `Successfully sold ${shares} shares of ${stock.symbol}` });
            fetchUser(); // Refresh user data
            setTimeout(() => setMessage(null), 3000);
        } catch (error) {
            setMessage({ type: 'error', text: error.response?.data?.error || 'Failed to sell stock' });
            setTimeout(() => setMessage(null), 3000);
        } finally {
            setLoading(false);
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
                        <div className="stock-symbol-row">
                            <h2 className="stock-symbol">{stock.symbol}</h2>
                            {userShares > 0 && (
                                <span className="owned-shares-badge">
                                    {userShares} {userShares === 1 ? 'share' : 'shares'}
                                </span>
                            )}
                        </div>
                        <p className="stock-name">{stock.name}</p>
                    </div>
                    <div className="stock-price-section">
                        <span className="stock-price">${stock.price}</span>
                        <span className={`stock-change ${changeClass}`}>
                            {isPositive ? '+' : ''}{stock.change} ({isPositive ? '+' : ''}{stock.changePercent}%)
                        </span>
                    </div>
                </div>

                {message && (
                    <div className={`trade-message ${message.type}`}>
                        {message.text}
                    </div>
                )}
                
                <div className="buy-section">
                    <div className="shares-input-group">
                        <label htmlFor={`shares-${stock.symbol}`}>Shares:</label>
                        <input
                            id={`shares-${stock.symbol}`}
                            type="number"
                            min="1"
                            value={shares}
                            onChange={(e) => setShares(Math.max(1, parseInt(e.target.value) || 1))}
                            className="shares-input"
                            disabled={loading}
                        />
                    </div>
                    <div className={`total-cost ${!canAfford && userShares === 0 ? 'insufficient' : ''}`}>
                        Total: ${totalCost.toFixed(2)}
                        {!canAfford && userShares === 0 && (
                            <span className="insufficient-hint"> (Insufficient funds)</span>
                        )}
                    </div>
                    <div className="action-buttons">
                        <button 
                            className="buy-button" 
                            onClick={handleBuy}
                            disabled={loading || !canAfford}
                            title={!canAfford ? 'Insufficient funds' : `Buy ${shares} shares`}
                        >
                            {loading ? 'Processing...' : `Buy ${shares}`}
                        </button>
                        <button 
                            className="sell-button" 
                            onClick={handleSell}
                            disabled={loading || userShares === 0 || userShares < shares}
                            title={userShares === 0 ? 'You don\'t own this stock' : userShares < shares ? `You only own ${userShares} shares` : `Sell ${shares} shares`}
                        >
                            {loading ? 'Processing...' : `Sell ${shares}`}
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