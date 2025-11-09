import { get, post } from '../util/util';

/**
 * Get funny AI financial advice based on user's portfolio
 * @returns {Promise<Object>} Response with advice
 */
export const getFinancialAdvice = async () => {
    return await get('/getAdvice');
};