import React, { useState, useEffect } from 'react';
import './Leaderboard.css';
import { getLeaderboard } from '../../services/leaderboardService';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      const data = await getLeaderboard();
      if (data.success) {
        setLeaderboard(data.leaderboard || []);
      }
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
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
      <div className="leaderboard-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading leaderboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="leaderboard-container">
      <div className="leaderboard-header">
        <h1>Leaderboard</h1>
        <p>Top traders by portfolio value</p>
      </div>

      <div className="leaderboard-table-container">
        {leaderboard.length === 0 ? (
          <div className="empty-state">
            <p>No leaderboard data available</p>
          </div>
        ) : (
          <table className="leaderboard-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Username</th>
                <th>Total Value</th>
                <th>Portfolio Value</th>
                <th>Cash Balance</th>
                <th>Return %</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((user, index) => (
                <tr key={index} className={index < 3 ? `rank-${index + 1}` : ''}>
                  <td className="rank-cell">
                    {index === 0 && '🥇'}
                    {index === 1 && '🥈'}
                    {index === 2 && '🥉'}
                    {index >= 3 && `#${index + 1}`}
                  </td>
                  <td className="username-cell">{user.username}</td>
                  <td className="value-cell">{formatCurrency(user.total_value)}</td>
                  <td>{formatCurrency(user.portfolio_value)}</td>
                  <td>{formatCurrency(user.balance)}</td>
                  <td className={user.return_percent >= 0 ? 'positive' : 'negative'}>
                    {user.return_percent >= 0 ? '+' : ''}{user.return_percent.toFixed(2)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Leaderboard;

