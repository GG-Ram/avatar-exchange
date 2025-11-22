import { useState, useEffect } from 'react';

const FAVORITES_KEY = 'stock_favorites';

/**
 * Custom hook for managing favorite stocks
 */
export const useFavorites = () => {
    const [favorites, setFavorites] = useState(() => {
        // Load from localStorage on init
        try {
            const stored = localStorage.getItem(FAVORITES_KEY);
            return stored ? JSON.parse(stored) : [];
        } catch {
            return [];
        }
    });

    // Save to localStorage whenever favorites change
    useEffect(() => {
        try {
            localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites));
        } catch (error) {
            console.error('Error saving favorites:', error);
        }
    }, [favorites]);

    const addFavorite = (symbol) => {
        setFavorites(prev => {
            if (!prev.includes(symbol)) {
                return [...prev, symbol];
            }
            return prev;
        });
    };

    const removeFavorite = (symbol) => {
        setFavorites(prev => prev.filter(s => s !== symbol));
    };

    const toggleFavorite = (symbol) => {
        if (isFavorite(symbol)) {
            removeFavorite(symbol);
        } else {
            addFavorite(symbol);
        }
    };

    const isFavorite = (symbol) => {
        return favorites.includes(symbol);
    };

    return {
        favorites,
        addFavorite,
        removeFavorite,
        toggleFavorite,
        isFavorite
    };
};

