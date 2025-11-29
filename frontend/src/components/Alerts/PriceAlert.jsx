import React, { useState } from 'react';
import './PriceAlert.css';
import { createAlert } from '../../services/alertService';

const PriceAlert = ({ stockSymbol, onAlertCreated }) => {
  const [condition, setCondition] = useState('above');
  const [price, setPrice] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!price || parseFloat(price) <= 0) {
      setError('Please enter a valid price');
      return;
    }

    try {
      setLoading(true);
      setError('');
      const response = await createAlert(stockSymbol, condition, parseFloat(price));
      if (response.success) {
        setPrice('');
        if (onAlertCreated) onAlertCreated();
      } else {
        setError(response.message || 'Failed to create alert');
      }
    } catch (err) {
      setError('Failed to create alert');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="price-alert-form">
      <h3>Set Price Alert for {stockSymbol}</h3>
      <form onSubmit={handleSubmit}>
        <div className="alert-form-group">
          <label>Alert when price is:</label>
          <select value={condition} onChange={(e) => setCondition(e.target.value)}>
            <option value="above">Above</option>
            <option value="below">Below</option>
          </select>
        </div>
        <div className="alert-form-group">
          <label>Price:</label>
          <input
            type="number"
            step="0.01"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            placeholder="Enter price"
            required
          />
        </div>
        {error && <div className="alert-error">{error}</div>}
        <button type="submit" disabled={loading} className="alert-submit-button">
          {loading ? 'Creating...' : 'Create Alert'}
        </button>
      </form>
    </div>
  );
};

export default PriceAlert;

