import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Mock user data
  const mockUser = {
    id: "1",
    name: "Sarah Johnson",
    email: "sarah.johnson@richmansdream.com",
    role: "admin",
    avatar: "https://images.unsplash.com/photo-1494790108755-2616b9997701?w=100&h=100&fit=crop&crop=face"
  };

  useEffect(() => {
    // Simulate checking for existing auth token
    const token = localStorage.getItem('authToken');
    if (token) {
      // In a real app, validate token with backend
      setUser(mockUser);
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock validation - accept any email/password for demo
      if (email && password) {
        const token = 'mock_jwt_token_' + Date.now();
        localStorage.setItem('authToken', token);
        setUser(mockUser);
        return { success: true };
      } else {
        return { success: false, error: 'Invalid credentials' };
      }
    } catch (error) {
      return { success: false, error: 'Login failed' };
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setUser(null);
  };

  const value = {
    user,
    login,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};