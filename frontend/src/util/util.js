import axios from 'axios';

// Base URL for your Flask backend API
const BASE_URL = 'http://127.0.0.1:5000/api';

// Create axios instance with default config
const axiosInstance = axios.create({
    baseURL: BASE_URL,
    timeout: 10000, // 10 seconds timeout
    withCredentials: false, // Not needed with JWT tokens
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor - you can add auth tokens here
axiosInstance.interceptors.request.use(
    (config) => {
        // Add auth token if available
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor - handle errors globally
axiosInstance.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // Handle errors globally
        if (error.response) {
            // Server responded with error status
            console.error('Response Error:', error.response.data);
            console.error('Status Code:', error.response.status);
        } else if (error.request) {
            // Request made but no response received
            console.error('Network Error:', error.request);
        } else {
            // Something else happened
            console.error('Error:', error.message);
        }
        return Promise.reject(error);
    }
);

/**
 * GET request utility
 * @param {string} endpoint - API endpoint (relative to BASE_URL)
 * @param {object} params - Query parameters (optional)
 * @param {object} config - Additional axios config (optional)
 * @returns {Promise} - Axios promise with response data
 */
export const get = async (endpoint, params = {}, config = {}) => {
    try {
        const response = await axiosInstance.get(endpoint, {
            params,
            ...config,
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};

/**
 * POST request utility
 * @param {string} endpoint - API endpoint (relative to BASE_URL)
 * @param {object} data - Request body data
 * @param {object} config - Additional axios config (optional)
 * @returns {Promise} - Axios promise with response data
 */
export const post = async (endpoint, data = {}, config = {}) => {
    try {
        const response = await axiosInstance.post(endpoint, data, config);
        return response.data;
    } catch (error) {
        throw error;
    }
};

/**
 * PUT request utility
 * @param {string} endpoint - API endpoint (relative to BASE_URL)
 * @param {object} data - Request body data
 * @param {object} config - Additional axios config (optional)
 * @returns {Promise} - Axios promise with response data
 */
export const put = async (endpoint, data = {}, config = {}) => {
    try {
        const response = await axiosInstance.put(endpoint, data, config);
        return response.data;
    } catch (error) {
        throw error;
    }
};

/**
 * DELETE request utility
 * @param {string} endpoint - API endpoint (relative to BASE_URL)
 * @param {object} config - Additional axios config (optional)
 * @returns {Promise} - Axios promise with response data
 */
export const del = async (endpoint, config = {}) => {
    try {
        const response = await axiosInstance.delete(endpoint, config);
        return response.data;
    } catch (error) {
        throw error;
    }
};

// Export axios instance for custom usage
export default axiosInstance;