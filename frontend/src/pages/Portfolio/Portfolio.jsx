import React, { useEffect, useState } from 'react';
import { useUser } from '../../Hooks/userContext';
import './Portfolio.css';

const Portfolio = () => {
    const { user } = useUser();
    const [stockPrices, setStockPrices] = useState({});

    // Fetch latest stock prices every 5 seconds
    useEffect(() => {
        const fetchStockPrices = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/stocks');
                const data = await response.json();
                const prices = {};
                data.forEach(stock => {
                    prices[stock.symbol] = stock.price;
                });
                setStockPrices(prices);
            } catch (error) {
                console.error('Error fetching stock prices:', error);
            }
        };

        fetchStockPrices(); // Initial fetch
        const interval = setInterval(fetchStockPrices, 5000);

        return () => clearInterval(interval);
    }, []);

    // Calculate total portfolio value using latest prices
    const calculateTotalValue = () => {
        return user?.positions?.reduce((total, position) => {
            const currentPrice = stockPrices[position.stock_data.symbol] || position.stock_data.price;
            return total + (position.shares * currentPrice);
        }, 0) || 0;
    };

    // ...existing loading check code...

    return (
        <div className="portfolio-container">
            {/* ...existing header code... */}

            <div className="holdings-section">
                <h2>Stock Holdings</h2>
                {user.positions && user.positions.length > 0 ? (
                    <div className="holdings-grid">
                        {user.positions.map((position, index) => {
                            const currentPrice = stockPrices[position.stock_data.symbol] || position.stock_data.price;
                            const totalValue = position.shares * currentPrice;
                            
                            return (
                                <div key={index} className="holding-card">
                                    <div className="holding-header">
                                        <h3 className="stock-symbol">{position.stock_data.symbol}</h3>
                                        <span className="shares-badge">{position.shares} shares</span>
                                    </div>
                                    <div className="holding-details">
                                        {/* ...existing detail rows... */}
                                        <div className="detail-row">
                                            <span className="detail-label">Current Price:</span>
                                            <span className="detail-value">${currentPrice.toFixed(2)}</span>
                                        </div>
                                        <div className="detail-row">
                                            <span className="detail-label">Total Value:</span>
                                            <span className="detail-value total">
                                                ${totalValue.toFixed(2)}
                                            </span>
                                        </div>
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