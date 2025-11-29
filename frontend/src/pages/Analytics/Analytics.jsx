import React, { useState, useEffect } from 'react';
import './Analytics.css';
import { useUser } from '../../Hooks/userContext';
import { getAnalytics } from '../../services/analyticsService';

const Analytics = () => {
  const { user } = useUser();
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const data = await getAnalytics();
      if (data.success) {
        setAnalytics(data.analytics);
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  if (loading) {
    return (
      <div className="analytics-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="analytics-container">
        <div className="empty-state">
          <p>No analytics data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="analytics-container">
      <div className="analytics-header">
        <h1>Analytics Dashboard</h1>
        <p>Performance metrics and insights</p>
      </div>

      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-label">Total Invested</div>
          <div className="metric-value">{formatCurrency(analytics.total_invested)}</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Total Returned</div>
          <div className="metric-value">{formatCurrency(analytics.total_returned)}</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Total Profit/Loss</div>
          <div className={`metric-value ${analytics.total_profit_loss >= 0 ? 'positive' : 'negative'}`}>
            {formatCurrency(analytics.total_profit_loss)}
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Portfolio Value</div>
          <div className="metric-value">{formatCurrency(analytics.portfolio_value)}</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Win Rate</div>
          <div className="metric-value">{analytics.win_loss_ratio}%</div>
          <div className="metric-subtext">{analytics.wins} wins / {analytics.losses} losses</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Total Transactions</div>
          <div className="metric-value">{analytics.total_transactions}</div>
        </div>
      </div>

      {(analytics.best_performer || analytics.worst_performer) && (
        <div className="performers-section">
          <h2>Top Performers</h2>
          <div className="performers-grid">
            {analytics.best_performer && (
              <div className="performer-card best">
                <div className="performer-label">Best Trade</div>
                <div className="performer-symbol">{analytics.best_performer.symbol}</div>
                <div className="performer-value positive">
                  {formatCurrency(analytics.best_performer.profit_loss)}
                </div>
              </div>
            )}
            {analytics.worst_performer && (
              <div className="performer-card worst">
                <div className="performer-label">Worst Trade</div>
                <div className="performer-symbol">{analytics.worst_performer.symbol}</div>
                <div className="performer-value negative">
                  {formatCurrency(analytics.worst_performer.profit_loss)}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Analytics;

