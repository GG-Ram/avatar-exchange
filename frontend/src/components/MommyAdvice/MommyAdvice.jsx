import React from 'react';
import './MommyAdvice.css';
import { useAdvice } from '../../Hooks/useAdvice';

const MommyAdvice = () => {
    const { advice, loading, error, fetchAdvice, clearAdvice } = useAdvice();

    return (
        <div className="mommy-advice">
            <button 
                className="advice-button"
                onClick={fetchAdvice}
                disabled={loading}
            >
                {loading ? '🤔 Thinking...' : '💡 Get Financial Advice'}
            </button>

            {error && (
                <div className="advice-error">
                    <p>⚠️ {error}</p>
                </div>
            )}

            {advice && (
                <div className="advice-box">
                    <div className="advice-header">
                        <h3>💸 Mommy's Advice</h3>
                        <button className="close-btn" onClick={clearAdvice}>✕</button>
                    </div>
                    <p className="advice-text">{advice}</p>
                </div>
            )}
        </div>
    );
};

export default MommyAdvice;