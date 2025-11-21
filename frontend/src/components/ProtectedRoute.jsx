import React from 'react';
import { Navigate } from 'react-router-dom';
import { useUser } from '../Hooks/userContext';

const ProtectedRoute = ({ children }) => {
    const { isAuthenticated, loading } = useUser();

    if (loading) {
        return (
            <div style={{ 
                display: 'flex', 
                justifyContent: 'center', 
                alignItems: 'center', 
                height: '100vh' 
            }}>
                <div>Loading...</div>
            </div>
        );
    }

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    return children;
};

export default ProtectedRoute;

