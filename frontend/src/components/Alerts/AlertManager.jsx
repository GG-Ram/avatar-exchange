import React, { useState, useEffect } from 'react';
import './AlertManager.css';
import { getAlerts, deleteAlert } from '../../services/alertService';
import PriceAlert from './PriceAlert';

const AlertManager = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      const response = await getAlerts();
      if (response.success) {
        setAlerts(response.alerts || []);
      }
    } catch (error) {
      console.error('Error fetching alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (alertId) => {
    try {
      const response = await deleteAlert(alertId);
      if (response.success) {
        fetchAlerts();
      }
    } catch (error) {
      console.error('Error deleting alert:', error);
    }
  };

  const formatDate = (timestamp) => {
    if (!timestamp) return 'N/A';
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  if (loading) {
    return <div className="loading">Loading alerts...</div>;
  }

  return (
    <div className="alert-manager">
      <h2>Price Alerts</h2>
      {alerts.length === 0 ? (
        <div className="empty-alerts">
          <p>No alerts set</p>
        </div>
      ) : (
        <div className="alerts-list">
          {alerts.map((alert) => (
            <div key={alert.id} className="alert-item">
              <div className="alert-info">
                <div className="alert-symbol">{alert.symbol}</div>
                <div className="alert-condition">
                  Alert when price is {alert.condition} ${alert.price.toFixed(2)}
                </div>
                <div className="alert-date">Created: {formatDate(alert.created_at)}</div>
              </div>
              <button
                className="delete-alert-button"
                onClick={() => handleDelete(alert.id)}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AlertManager;

