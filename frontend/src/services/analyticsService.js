import { get } from '../util/util';

export const getAnalytics = async () => {
  return await get('/analytics');
};

