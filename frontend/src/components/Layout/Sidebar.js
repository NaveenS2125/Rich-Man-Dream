import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users, 
  Phone, 
  Calendar, 
  TrendingUp, 
  Mail, 
  BarChart3, 
  Settings,
  Crown
} from 'lucide-react';
import { cn } from '../../lib/utils';

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Leads', href: '/leads', icon: Users },
  { name: 'Calls', href: '/calls', icon: Phone },
  { name: 'Viewings', href: '/viewings', icon: Calendar },
  { name: 'Sales', href: '/sales', icon: TrendingUp },
  { name: 'Emails', href: '/emails', icon: Mail },
  { name: 'Reports', href: '/reports', icon: BarChart3 },
  { name: 'Settings', href: '/settings', icon: Settings },
];

const Sidebar = ({ isOpen, onClose }) => {
  const location = useLocation();

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-40 lg:hidden bg-black/50 backdrop-blur-sm"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <div className={cn(
        "fixed inset-y-0 left-0 z-50 w-64 transform bg-gradient-to-b from-black via-gray-900 to-black border-r border-yellow-500/20 transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0",
        isOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        {/* Logo */}
        <div className="flex items-center px-6 py-6 border-b border-yellow-500/20">
          <Crown className="h-8 w-8 text-yellow-500" />
          <div className="ml-3">
            <h1 className="text-xl font-bold bg-gradient-to-r from-yellow-400 to-yellow-600 bg-clip-text text-transparent">
              Rich Man Dream
            </h1>
            <p className="text-xs text-gray-400">Real Estate CRM</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="mt-6 px-3">
          <ul className="space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.href;
              
              return (
                <li key={item.name}>
                  <Link
                    to={item.href}
                    onClick={onClose}
                    className={cn(
                      "group flex items-center px-3 py-3 text-sm font-medium rounded-lg transition-all duration-200 ease-in-out",
                      isActive
                        ? "bg-gradient-to-r from-yellow-500/20 to-yellow-600/20 text-yellow-400 border-l-4 border-yellow-500 shadow-lg shadow-yellow-500/10"
                        : "text-gray-300 hover:text-yellow-400 hover:bg-yellow-500/5 hover:shadow-md hover:shadow-yellow-500/5"
                    )}
                  >
                    <Icon className={cn(
                      "mr-3 h-5 w-5 transition-colors",
                      isActive ? "text-yellow-400" : "text-gray-400 group-hover:text-yellow-400"
                    )} />
                    {item.name}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Bottom section */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-yellow-500/20">
          <div className="bg-gradient-to-r from-yellow-500/10 to-yellow-600/10 rounded-lg p-3 border border-yellow-500/20">
            <p className="text-xs text-gray-400 text-center">
              Elevating Real Estate Success
            </p>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;