import React, { useState, useMemo } from 'react';
import './MarketPage.css';
import StockRow from '../../components/Stock/StockRow';
import StockSearch from '../../components/Stock/StockSearch';
import MarketTabs from '../../components/Stock/MarketTabs';
import { LoadingState, ErrorState } from '../../components/Stock/StockState';
import { useStockData } from '../../Hooks/useStockData';
import { useStockChart } from '../../Hooks/useStockChart';
import { useUser } from '../../Hooks/userContext';
import { useFavorites } from '../../Hooks/useFavorites';

/**
 * MarketPage - Clean stock trading dashboard with tabs and favorites
 */
function MarketPage() {
    const { stocks: defaultStocks, loading, error, fetchStockData } = useStockData();
    const [searchedStocks, setSearchedStocks] = useState([]);
    const [activeTab, setActiveTab] = useState('featured');
    const { user } = useUser();
    const { favorites, toggleFavorite, isFavorite } = useFavorites();

    // Combine all stocks with metadata
    const allStocks = useMemo(() => {
        const stockMap = new Map();
        
        // Add default stocks (featured)
        defaultStocks.forEach(stock => {
            if (!stock.error) {
                stockMap.set(stock.symbol, { 
                    ...stock, 
                    isFeatured: true,
                    isSearched: false 
                });
            }
        });
        
        // Add searched stocks
        searchedStocks.forEach(stock => {
            if (!stock.error) {
                const existing = stockMap.get(stock.symbol);
                stockMap.set(stock.symbol, { 
                    ...stock, 
                    isFeatured: existing?.isFeatured || false,
                    isSearched: true 
                });
            }
        });
        
        return Array.from(stockMap.values());
    }, [defaultStocks, searchedStocks]);

    // Get user's owned shares for each stock
    const getUserShares = (symbol) => {
        const position = user?.positions?.find(p => p.stock_data?.symbol === symbol);
        return position?.shares || 0;
    };

    // Filter stocks based on active tab
    const filteredStocks = useMemo(() => {
        switch (activeTab) {
            case 'favorites':
                // Show all favorited stocks, including featured ones
                return allStocks.filter(stock => isFavorite(stock.symbol));
            case 'featured':
                return allStocks.filter(stock => stock.isFeatured);
            case 'all':
            default:
                // In "All Stocks", only show:
                // 1. Stocks that were manually searched (isSearched = true)
                // 2. Featured stocks that are favorited
                return allStocks.filter(stock => 
                    stock.isSearched || (stock.isFeatured && isFavorite(stock.symbol))
                );
        }
    }, [allStocks, activeTab, isFavorite]);

    const { chartRefs, handleMouseMove, handleMouseLeave } = useStockChart(filteredStocks);

    const handleStockFound = (stockData) => {
        // Check if stock already exists
        const exists = searchedStocks.some(s => s.symbol === stockData.symbol);
        if (!exists) {
            setSearchedStocks(prev => [...prev, stockData]);
        } else {
            // Update existing stock
            setSearchedStocks(prev => 
                prev.map(s => s.symbol === stockData.symbol ? stockData : s)
            );
        }
    };

    if (loading && allStocks.length === 0) {
        return <LoadingState />;
    }

    if (error && allStocks.length === 0) {
        return <ErrorState error={error} onRetry={fetchStockData} />;
    }

    return (
        <div className="container">
            <div className="header">
                <div className="header-content">
                    <div className="header-text">
                        <h1>Market Dashboard</h1>
                        <p>Search and trade any stock in real-time</p>
                    </div>
                    <div className="user-balance">
                        <span className="balance-label">Available Balance</span>
                        <span className="balance-amount">${user?.balance?.toFixed(2) || '0.00'}</span>
                    </div>
                </div>
            </div>

            <div className="search-section">
                <StockSearch 
                    onStockFound={handleStockFound}
                    onError={(error) => console.error('Search error:', error)}
                />
            </div>

            <MarketTabs activeTab={activeTab} onTabChange={setActiveTab} />

            {filteredStocks.length > 0 ? (
                <div className="stocks-section">
                    <div className="section-header">
                        <h2 className="section-title">
                            {activeTab === 'featured' && 'Featured Stocks'}
                            {activeTab === 'favorites' && 'Your Favorites'}
                            {activeTab === 'all' && 'All Stocks'}
                        </h2>
                        <span className="stock-count">{filteredStocks.length} {filteredStocks.length === 1 ? 'stock' : 'stocks'}</span>
                    </div>
                    <div className="stock-container">
                        {filteredStocks.map((stock) => (
                            <StockRow
                                key={stock.symbol}
                                stock={stock}
                                chartRef={el => chartRefs.current[stock.symbol] = el}
                                onMouseMove={handleMouseMove}
                                onMouseLeave={handleMouseLeave}
                                isFavorite={isFavorite(stock.symbol)}
                                onToggleFavorite={toggleFavorite}
                                isFeatured={stock.isFeatured}
                                userShares={getUserShares(stock.symbol)}
                            />
                        ))}
                    </div>
                </div>
            ) : (
                <div className="empty-state">
                    <div className="empty-state-icon">
                        {activeTab === 'favorites' ? '❤️' : '📈'}
                    </div>
                    <h3>
                        {activeTab === 'favorites' 
                            ? 'No favorite stocks yet' 
                            : 'No stocks to display'}
                    </h3>
                    <p>
                        {activeTab === 'favorites' 
                            ? 'Click the heart icon on any stock to add it to your favorites'
                            : 'Search for a stock symbol above to get started'}
                    </p>
                </div>
            )}
        </div>
    );
}

export default MarketPage;