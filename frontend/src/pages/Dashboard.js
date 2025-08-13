import React from 'react';
import { Users, Phone, Calendar, TrendingUp, DollarSign, Eye, Target, Award } from 'lucide-react';
import StatsCard from '../components/Dashboard/StatsCard';
import { SalesChart, LeadsChart, StatusDistributionChart, ViewingsChart, MiniLineChart } from '../components/Charts/ChartComponents';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar';
import { mockDashboardStats, mockChartData, mockLeads, mockUsers } from '../data/mockData';
import { formatCurrency, formatDate } from '../lib/utils';

const Dashboard = () => {
  // Mini chart data for stats cards
  const miniChartData = [
    { value: 45 }, { value: 52 }, { value: 38 }, { value: 61 }, { value: 58 }, { value: 67 }, { value: 72 }
  ];

  const recentLeads = mockLeads.slice(0, 3);
  const topAgents = mockUsers.slice(0, 3);

  return (
    <div className="p-6 space-y-6 bg-gray-50 dark:bg-gray-900/50 min-h-screen">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Welcome Back, Sarah! 👋
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Here's what's happening with your real estate empire today.
          </p>
        </div>
        <Button className="bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-600 hover:to-yellow-700 text-black font-semibold shadow-lg shadow-yellow-500/25">
          Add New Lead
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Leads"
          value={mockDashboardStats.totalLeads}
          change="+12.5%"
          icon={Users}
          color="yellow"
          chart={<MiniLineChart data={miniChartData} dataKey="value" />}
        />
        <StatsCard
          title="Hot Leads"
          value={mockDashboardStats.hotLeads}
          change="+8.2%"
          icon={Target}
          color="green"
          chart={<MiniLineChart data={miniChartData} dataKey="value" color="#10B981" />}
        />
        <StatsCard
          title="Scheduled Viewings"
          value={mockDashboardStats.scheduledViewings}
          change="+15.3%"
          icon={Calendar}
          color="blue"
          chart={<MiniLineChart data={miniChartData} dataKey="value" color="#3B82F6" />}
        />
        <StatsCard
          title="Monthly Revenue"
          value={formatCurrency(2450000)}
          change="+18.7%"
          icon={DollarSign}
          color="purple"
          chart={<MiniLineChart data={miniChartData} dataKey="value" color="#8B5CF6" />}
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sales Performance */}
        <Card className="bg-white dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200 dark:border-gray-700 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-gray-900 dark:text-white">
              <TrendingUp className="h-5 w-5 text-yellow-500" />
              Sales Performance
            </CardTitle>
          </CardHeader>
          <CardContent>
            <SalesChart data={mockChartData.salesChart} />
          </CardContent>
        </Card>

        {/* Lead Distribution */}
        <Card className="bg-white dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200 dark:border-gray-700 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-gray-900 dark:text-white">
              <Eye className="h-5 w-5 text-yellow-500" />
              Lead Status Distribution
            </CardTitle>
          </CardHeader>
          <CardContent>
            <StatusDistributionChart data={mockChartData.statusDistribution} />
          </CardContent>
        </Card>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Leads */}
        <Card className="lg:col-span-2 bg-white dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200 dark:border-gray-700 shadow-lg">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-gray-900 dark:text-white">Recent Leads</CardTitle>
            <Button variant="outline" size="sm" className="border-yellow-500/50 text-yellow-600 hover:bg-yellow-500/10">
              View All
            </Button>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentLeads.map((lead) => (
                <div key={lead.id} className="flex items-center justify-between p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                  <div className="flex items-center gap-4">
                    <Avatar className="h-10 w-10">
                      <AvatarFallback className="bg-gradient-to-br from-yellow-500 to-yellow-600 text-black font-semibold">
                        {lead.name.split(' ').map(n => n[0]).join('')}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">{lead.name}</p>
                      <p className="text-sm text-gray-500 dark:text-gray-400">{lead.email}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <Badge 
                      className={
                        lead.status === 'hot' 
                          ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400' 
                          : lead.status === 'warm'
                          ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                          : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
                      }
                    >
                      {lead.status.toUpperCase()}
                    </Badge>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{lead.budget}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Top Agents */}
        <Card className="bg-white dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200 dark:border-gray-700 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-gray-900 dark:text-white">
              <Award className="h-5 w-5 text-yellow-500" />
              Top Agents
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {topAgents.map((agent, index) => (
                <div key={agent.id} className="flex items-center gap-3">
                  <div className="relative">
                    <Avatar className="h-10 w-10">
                      <AvatarImage src={agent.avatar} alt={agent.name} />
                      <AvatarFallback className="bg-gradient-to-br from-yellow-500 to-yellow-600 text-black font-semibold">
                        {agent.name.split(' ').map(n => n[0]).join('')}
                      </AvatarFallback>
                    </Avatar>
                    {index === 0 && (
                      <div className="absolute -top-1 -right-1 h-4 w-4 bg-yellow-500 rounded-full flex items-center justify-center">
                        <span className="text-xs font-bold text-black">1</span>
                      </div>
                    )}
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-gray-900 dark:text-white text-sm">{agent.name}</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {agent.closedDeals} deals closed
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold text-gray-900 dark:text-white">
                      {agent.activeLeads}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">leads</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;