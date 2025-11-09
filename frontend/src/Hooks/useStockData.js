import { useState, useEffect } from 'react';
import { get } from '../util/util';

/**
 * Custom hook for fetching stock data
 */
export const useStockData = (refreshInterval = 1000) => {
    const [stocks, setStocks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchStockData();
        const interval = setInterval(fetchStockData, refreshInterval);
        return () => clearInterval(interval);
    }, [refreshInterval]);

    const fetchStockData = async () => {
        try {
            setLoading(true);
            const data = await get('/stocks');
            setStocks(data);
            setError(null);
        } catch (err) {
            console.error('Error fetching stock data:', err);
            setError('Failed to load stock data');
        } finally {
            setLoading(false);
        }
    };

    return {
        stocks,
        loading,
        error,
        fetchStockData
    };
};