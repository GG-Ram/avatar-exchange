import { get } from '../util/util';

export const getTransactions = async () => {
  return await get('/transactions');
};

export const exportTransactions = async () => {
  return await get('/transactions/export');
};

