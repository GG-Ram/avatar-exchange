// contexts/UserContext.jsx
import { createContext, useContext, useState, useEffect } from 'react';
import { get } from '../util/util';
import { getCurrentUser, login as loginApi, register as registerApi, logout as logoutApi } from '../services/authService';

const UserContext = createContext();

export function UserProvider({ children }) {
    const [user, setUser] = useState(null);
    const [userInfo, setUserInfo] = useState(null); // User info (username, email, id)
    const [loading, setLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        try {
            const response = await getCurrentUser();
            if (response.success) {
                setUser(response.userData);
                setUserInfo(response.user);
                setIsAuthenticated(true);
            } else {
                setIsAuthenticated(false);
            }
        } catch (error) {
            console.error('Error checking auth:', error);
            setIsAuthenticated(false);
        } finally {
            setLoading(false);
        }
    };

    const fetchUser = async () => {
        try {
            const data = await get('/userData');
            setUser(data);
        } catch (error) {
            console.error('Error fetching user:', error);
            if (error.response?.status === 401) {
                setIsAuthenticated(false);
                setUser(null);
                setUserInfo(null);
            }
        }
    };

    const login = async (username, password) => {
        try {
            const response = await loginApi(username, password);
            if (response.success) {
                setUser(response.userData);
                setUserInfo(response.user);
                setIsAuthenticated(true);
                return { success: true };
            }
            return { success: false, error: response.error };
        } catch (error) {
            return { 
                success: false, 
                error: error.response?.data?.error || 'Login failed' 
            };
        }
    };

    const register = async (username, email, password) => {
        try {
            const response = await registerApi(username, email, password);
            if (response.success) {
                setUser(response.userData);
                setUserInfo(response.user);
                setIsAuthenticated(true);
                return { success: true };
            }
            return { success: false, error: response.error };
        } catch (error) {
            return { 
                success: false, 
                error: error.response?.data?.error || 'Registration failed' 
            };
        }
    };

    const logout = async () => {
        try {
            await logoutApi();
            // Token is already removed by logoutApi
            setUser(null);
            setUserInfo(null);
            setIsAuthenticated(false);
        } catch (error) {
            console.error('Error logging out:', error);
            // Clear state even if API call fails
            localStorage.removeItem('token'); // Ensure token is removed
            setUser(null);
            setUserInfo(null);
            setIsAuthenticated(false);
        }
    };

    const updateBalance = (newBalance) => {
        setUser(prev => ({ ...prev, balance: newBalance }));
    };

    return (
        <UserContext.Provider value={{ 
            user, 
            userInfo,
            setUser, 
            updateBalance, 
            loading, 
            fetchUser,
            login,
            register,
            logout,
            isAuthenticated,
            checkAuth
        }}>
            {children}
        </UserContext.Provider>
    );
}

// Custom hook to use the context
export function useUser() {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error('useUser must be used within UserProvider');
    }
    return context;
}