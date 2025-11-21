import { post, get } from '../util/util';

/**
 * Register a new user
 * @param {string} username - Username
 * @param {string} email - Email address
 * @param {string} password - Password
 * @returns {Promise} - Response with user data and token
 */
export const register = async (username, email, password) => {
    const response = await post('/register', {
        username,
        email,
        password
    });
    // Store token in localStorage
    if (response.success && response.token) {
        localStorage.setItem('token', response.token);
    }
    return response;
};

/**
 * Login an existing user
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise} - Response with user data and token
 */
export const login = async (username, password) => {
    const response = await post('/login', {
        username,
        password
    });
    // Store token in localStorage
    if (response.success && response.token) {
        localStorage.setItem('token', response.token);
    }
    return response;
};

/**
 * Logout current user
 * @returns {Promise} - Response
 */
export const logout = async () => {
    // Remove token from localStorage
    localStorage.removeItem('token');
    return await post('/logout');
};

/**
 * Get current authenticated user
 * @returns {Promise} - Response with user data
 */
export const getCurrentUser = async () => {
    return await get('/me');
};

