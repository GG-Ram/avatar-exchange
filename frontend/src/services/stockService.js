import {post, get} from "../util/util";

/**
 * Buy stock shares
 * @param {string} symbol - Stock symbol (e.g., "AAPL")
 * @param {number} shares - Number of shares to buy
 * @returns {Promise} - Response with updated user data
 */
export const buyStock = async (symbol, shares) => {
    return await post('/buy', {
        symbol: symbol,
        shares: shares
    });
};

/**
 * Sell stock shares
 * @param {string} symbol - Stock symbol (e.g., "AAPL")
 * @param {number} shares - Number of shares to sell
 * @returns {Promise} - Response with updated user data
 */
export const sellStock = async (symbol, shares) => {
    return await post('/sell', {
        symbol: symbol,
        shares: shares
    });
};

/**
 * Get data for a specific stock by symbol
 * @param {string} symbol - Stock symbol (e.g., "AAPL")
 * @returns {Promise} - Stock data object
 */
export const getStock = async (symbol) => {
    return await get(`/stock/${symbol}`);
};

/**
 * Get current prices for multiple stock symbols
 * @param {string[]} symbols - Array of stock symbols
 * @returns {Promise} - Object mapping symbols to price data
 */
export const getStockPrices = async (symbols) => {
    return await post('/stocks/prices', { symbols });
};
