import React, { useState } from 'react';
import { getStock } from '../../services/stockService';
import './StockSearch.css';

function StockSearch({ onStockFound, onError }) {
    const [symbol, setSymbol] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = async (e) => {
        e.preventDefault();
        
        if (!symbol.trim()) {
            setError('Please enter a stock symbol');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const stockData = await getStock(symbol.trim().toUpperCase());
            if (stockData.error) {
                setError(stockData.message || 'Stock not found');
                if (onError) onError(stockData.message || 'Stock not found');
            } else {
                onStockFound(stockData);
                setSymbol(''); // Clear input on success
            }
        } catch (err) {
            const errorMsg = err.response?.data?.message || 'Failed to fetch stock data';
            setError(errorMsg);
            if (onError) onError(errorMsg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form className="stock-search" onSubmit={handleSearch}>
            <div className="search-input-wrapper">
                <input
                    type="text"
                    className="search-input"
                    placeholder="Search any stock (e.g., TSLA, MSFT, GOOGL)"
                    value={symbol}
                    onChange={(e) => {
                        setSymbol(e.target.value);
                        setError(null);
                    }}
                    disabled={loading}
                />
                <button 
                    type="submit" 
                    className="search-button"
                    disabled={loading || !symbol.trim()}
                >
                    {loading ? 'Searching...' : 'Search'}
                </button>
            </div>
            {error && <div className="search-error">{error}</div>}
        </form>
    );
}

export default StockSearch;

