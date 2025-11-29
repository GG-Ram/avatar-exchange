import React, { useState, useEffect } from 'react';
import './Transactions.css';
import { getTransactions, exportTransactions } from '../../services/transactionService';

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [filteredTransactions, setFilteredTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    symbol: '',
    type: 'all',
    dateFrom: '',
    dateTo: ''
  });

  useEffect(() => {
    fetchTransactions();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [transactions, filters]);

  const fetchTransactions = async () => {
    try {
      setLoading(true);
      const response = await getTransactions();
      if (response.success) {
        setTransactions(response.transactions || []);
      }
    } catch (error) {
      console.error('Error fetching transactions:', error);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...transactions];

    if (filters.symbol) {
      filtered = filtered.filter(t => 
        t.symbol.toLowerCase().includes(filters.symbol.toLowerCase())
      );
    }

    if (filters.type !== 'all') {
      filtered = filtered.filter(t => t.type === filters.type);
    }

    if (filters.dateFrom) {
      filtered = filtered.filter(t => t.timestamp >= filters.dateFrom);
    }

    if (filters.dateTo) {
      filtered = filtered.filter(t => t.timestamp <= filters.dateTo + 'T23:59:59');
    }

    setFilteredTransactions(filtered);
  };

  const handleExport = async () => {
    try {
      const response = await exportTransactions();
      if (response.success) {
        const blob = new Blob([response.csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `transactions_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Error exporting transactions:', error);
      alert('Failed to export transactions');
    }
  };

  const formatDate = (timestamp) => {
    if (!timestamp) return 'N/A';
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  if (loading) {
    return (
      <div className="transactions-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading transactions...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="transactions-container">
      <div className="transactions-header">
        <div>
          <h1>Transaction History</h1>
          <p>View all your buy and sell transactions</p>
        </div>
        <button className="export-button" onClick={handleExport}>
          Export CSV
        </button>
      </div>

      <div className="filters-section">
        <div className="filter-group">
          <label>Symbol</label>
          <input
            type="text"
            placeholder="Filter by symbol..."
            value={filters.symbol}
            onChange={(e) => setFilters({...filters, symbol: e.target.value})}
          />
        </div>
        <div className="filter-group">
          <label>Type</label>
          <select
            value={filters.type}
            onChange={(e) => setFilters({...filters, type: e.target.value})}
          >
            <option value="all">All</option>
            <option value="BUY">Buy</option>
            <option value="SELL">Sell</option>
          </select>
        </div>
        <div className="filter-group">
          <label>From Date</label>
          <input
            type="date"
            value={filters.dateFrom}
            onChange={(e) => setFilters({...filters, dateFrom: e.target.value})}
          />
        </div>
        <div className="filter-group">
          <label>To Date</label>
          <input
            type="date"
            value={filters.dateTo}
            onChange={(e) => setFilters({...filters, dateTo: e.target.value})}
          />
        </div>
      </div>

      <div className="transactions-table-container">
        {filteredTransactions.length === 0 ? (
          <div className="empty-state">
            <p>No transactions found</p>
            <p className="hint">Start trading to see your transaction history</p>
          </div>
        ) : (
          <table className="transactions-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Type</th>
                <th>Symbol</th>
                <th>Shares</th>
                <th>Price</th>
                <th>Total</th>
                <th>Profit/Loss</th>
              </tr>
            </thead>
            <tbody>
              {filteredTransactions.map((txn, index) => (
                <tr key={index} className={txn.type === 'BUY' ? 'buy-row' : 'sell-row'}>
                  <td>{formatDate(txn.timestamp)}</td>
                  <td>
                    <span className={`type-badge ${txn.type.toLowerCase()}`}>
                      {txn.type}
                    </span>
                  </td>
                  <td className="symbol-cell">{txn.symbol}</td>
                  <td>{txn.shares}</td>
                  <td>{formatCurrency(txn.price)}</td>
                  <td>{formatCurrency(txn.total)}</td>
                  <td className={txn.profit_loss >= 0 ? 'positive' : 'negative'}>
                    {txn.profit_loss !== 0 ? formatCurrency(txn.profit_loss) : '-'}
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

export default Transactions;

