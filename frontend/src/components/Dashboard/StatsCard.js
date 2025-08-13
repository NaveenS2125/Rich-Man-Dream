import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import { Card, CardContent } from '../ui/card';
import { cn } from '../../lib/utils';

const StatsCard = ({ 
  title, 
  value, 
  change, 
  icon: Icon, 
  trend = 'up',
  color = 'yellow',
  chart
}) => {
  const isPositive = trend === 'up';
  
  const colorClasses = {
    yellow: {
      bg: 'from-yellow-500/20 to-yellow-600/20',
      border: 'border-yellow-500/30',
      icon: 'text-yellow-500',
      shadow: 'shadow-yellow-500/10'
    },
    green: {
      bg: 'from-green-500/20 to-green-600/20',
      border: 'border-green-500/30',
      icon: 'text-green-500',
      shadow: 'shadow-green-500/10'
    },
    blue: {
      bg: 'from-blue-500/20 to-blue-600/20',
      border: 'border-blue-500/30',
      icon: 'text-blue-500',
      shadow: 'shadow-blue-500/10'
    },
    purple: {
      bg: 'from-purple-500/20 to-purple-600/20',
      border: 'border-purple-500/30',
      icon: 'text-purple-500',
      shadow: 'shadow-purple-500/10'
    }
  };

  const currentColor = colorClasses[color] || colorClasses.yellow;

  return (
    <Card className={cn(
      "bg-gradient-to-br bg-white/5 dark:bg-white/5 backdrop-blur-sm border hover:shadow-lg transition-all duration-300 hover:scale-[1.02]",
      currentColor.border,
      currentColor.shadow
    )}>
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
              {title}
            </p>
            <div className="flex items-baseline gap-2">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
                {value}
              </h3>
              {change && (
                <div className={cn(
                  "flex items-center text-sm font-medium",
                  isPositive ? "text-green-600 dark:text-green-400" : "text-red-600 dark:text-red-400"
                )}>
                  {isPositive ? (
                    <TrendingUp className="h-4 w-4 mr-1" />
                  ) : (
                    <TrendingDown className="h-4 w-4 mr-1" />
                  )}
                  {change}
                </div>
              )}
            </div>
          </div>
          
          <div className={cn(
            "p-3 rounded-xl bg-gradient-to-br",
            currentColor.bg,
            currentColor.border
          )}>
            <Icon className={cn("h-6 w-6", currentColor.icon)} />
          </div>
        </div>
        
        {/* Mini chart */}
        {chart && (
          <div className="mt-4 h-16">
            {chart}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default StatsCard;