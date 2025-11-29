import { get, post, del } from '../util/util';

export const getAlerts = async () => {
  return await get('/alerts');
};

export const createAlert = async (symbol, condition, price) => {
  return await post('/alerts', {
    symbol,
    condition,
    price
  });
};

export const deleteAlert = async (alertId) => {
  return await del(`/alerts/${alertId}`);
};

