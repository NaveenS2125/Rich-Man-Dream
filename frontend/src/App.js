import React, { useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { ThemeProvider } from "./contexts/ThemeContext";
import { Toaster } from "./components/ui/toaster";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Leads from "./pages/Leads";
import Sidebar from "./components/Layout/Sidebar";
import Header from "./components/Layout/Header";

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-yellow-500"></div>
      </div>
    );
  }
  
  return user ? children : <Navigate to="/login" />;
};

// Main Layout Component
const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header onMenuClick={() => setSidebarOpen(true)} />
        <main className="flex-1 overflow-x-hidden overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
};

// App Routes Component
const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/*" element={
        <ProtectedRoute>
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/leads" element={<Leads />} />
              <Route path="/calls" element={<div className="p-6"><h1 className="text-2xl font-bold text-gray-900 dark:text-white">Call Log</h1><p className="text-gray-600 dark:text-gray-400 mt-2">Coming soon...</p></div>} />
              <Route path="/viewings" element={<div className="p-6"><h1 className="text-2xl font-bold text-gray-900 dark:text-white">Viewing Scheduler</h1><p className="text-gray-600 dark:text-gray-400 mt-2">Coming soon...</p></div>} />
              <Route path="/sales" element={<div className="p-6"><h1 className="text-2xl font-bold text-gray-900 dark:text-white">Sales Tracker</h1><p className="text-gray-600 dark:text-gray-400 mt-2">Coming soon...</p></div>} />
              <Route path="/emails" element={<div className="p-6"><h1 className="text-2xl font-bold text-gray-900 dark:text-white">Email Sync</h1><p className="text-gray-600 dark:text-gray-400 mt-2">Coming soon...</p></div>} />
              <Route path="/reports" element={<div className="p-6"><h1 className="text-2xl font-bold text-gray-900 dark:text-white">Reports</h1><p className="text-gray-600 dark:text-gray-400 mt-2">Coming soon...</p></div>} />
              <Route path="/settings" element={<div className="p-6"><h1 className="text-2xl font-bold text-gray-900 dark:text-white">Settings</h1><p className="text-gray-600 dark:text-gray-400 mt-2">Coming soon...</p></div>} />
            </Routes>
          </Layout>
        </ProtectedRoute>
      } />
    </Routes>
  );
};

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <div className="App">
            <AppRoutes />
            <Toaster />
          </div>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
