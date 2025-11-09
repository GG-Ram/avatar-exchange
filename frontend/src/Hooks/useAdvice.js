import { useState } from 'react';
import { getFinancialAdvice } from '../services/adviceService';

export function useAdvice() {
    const [advice, setAdvice] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchAdvice = async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getFinancialAdvice();
            if (result.success) {
                setAdvice(result.advice);
            } else {
                setError(result.message || 'Failed to get advice');
            }
        } catch (err) {
            console.error('Error getting advice:', err);
            setError('Something went wrong! Try again later.');
        } finally {
            setLoading(false);
        }
    };

    const clearAdvice = () => {
        setAdvice(null);
        setError(null);
    };

    return { advice, loading, error, fetchAdvice, clearAdvice };
}