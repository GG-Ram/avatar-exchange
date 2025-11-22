import React from 'react';
import './MarketTabs.css';

function MarketTabs({ activeTab, onTabChange }) {
    const tabs = [
        { id: 'featured', label: 'Featured', icon: '⭐' },
        { id: 'favorites', label: 'Favorites', icon: '❤️' },
        { id: 'all', label: 'All Stocks', icon: '📊' }
    ];

    return (
        <div className="market-tabs">
            {tabs.map(tab => (
                <button
                    key={tab.id}
                    className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
                    onClick={() => onTabChange(tab.id)}
                >
                    <span className="tab-icon">{tab.icon}</span>
                    <span className="tab-label">{tab.label}</span>
                </button>
            ))}
        </div>
    );
}

export default MarketTabs;

