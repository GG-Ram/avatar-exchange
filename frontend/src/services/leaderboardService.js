import { get } from '../util/util';

export const getLeaderboard = async () => {
  return await get('/leaderboard');
};

