import React from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

// Custom Tooltip Component
const CustomTooltip = ({ active, payload, label, formatter = (value) => value }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white dark:bg-gray-800 p-3 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg">
        <p className="font-medium text-gray-900 dark:text-white">{label}</p>
        {payload.map((entry, index) => (
          <p key={index} className="text-sm" style={{ color: entry.color }}>
            {`${entry.name}: ${formatter(entry.value)}`}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

// Sales Chart Component
export const SalesChart = ({ data }) => (
  <ResponsiveContainer width="100%" height={300}>
    <AreaChart data={data}>
      <defs>
        <linearGradient id="salesGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="5%" stopColor="#FFD700" stopOpacity={0.3}/>
          <stop offset="95%" stopColor="#FFD700" stopOpacity={0}/>
        </linearGradient>
      </defs>
      <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
      <XAxis 
        dataKey="month" 
        axisLine={false}
        tickLine={false}
        className="text-gray-600 dark:text-gray-400"
      />
      <YAxis 
        axisLine={false}
        tickLine={false}
        className="text-gray-600 dark:text-gray-400"
        tickFormatter={(value) => `$${(value / 1000000).toFixed(1)}M`}
      />
      <Tooltip content={<CustomTooltip formatter={(value) => `$${value.toLocaleString()}`} />} />
      <Area
        type="monotone"
        dataKey="sales"
        stroke="#FFD700"
        strokeWidth={3}
        fillOpacity={1}
        fill="url(#salesGradient)"
        className="drop-shadow-sm"
      />
    </AreaChart>
  </ResponsiveContainer>
);

// Leads Chart Component
export const LeadsChart = ({ data }) => (
  <ResponsiveContainer width="100%" height={300}>
    <LineChart data={data}>
      <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
      <XAxis 
        dataKey="week" 
        axisLine={false}
        tickLine={false}
        className="text-gray-600 dark:text-gray-400"
      />
      <YAxis 
        axisLine={false}
        tickLine={false}
        className="text-gray-600 dark:text-gray-400"
      />
      <Tooltip content={<CustomTooltip />} />
      <Line
        type="monotone"
        dataKey="leads"
        stroke="#FFD700"
        strokeWidth={3}
        dot={{ fill: '#FFD700', strokeWidth: 2, r: 6 }}
        activeDot={{ r: 8, className: "drop-shadow-md" }}
        className="drop-shadow-sm"
      />
    </LineChart>
  </ResponsiveContainer>
);

// Status Distribution Chart Component
export const StatusDistributionChart = ({ data }) => (
  <ResponsiveContainer width="100%" height={300}>
    <PieChart>
      <Pie
        data={data}
        cx="50%"
        cy="50%"
        labelLine={false}
        label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
        outerRadius={100}
        fill="#8884d8"
        dataKey="value"
        className="text-sm font-medium"
      >
        {data.map((entry, index) => (
          <Cell key={`cell-${index}`} fill={entry.color} className="drop-shadow-sm" />
        ))}
      </Pie>
      <Tooltip content={<CustomTooltip />} />
    </PieChart>
  </ResponsiveContainer>
);

// Viewings Chart Component
export const ViewingsChart = ({ data }) => (
  <ResponsiveContainer width="100%" height={300}>
    <BarChart data={data} barGap={10}>
      <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
      <XAxis 
        dataKey="day" 
        axisLine={false}
        tickLine={false}
        className="text-gray-600 dark:text-gray-400"
      />
      <YAxis 
        axisLine={false}
        tickLine={false}
        className="text-gray-600 dark:text-gray-400"
      />
      <Tooltip content={<CustomTooltip />} />
      <Bar 
        dataKey="completed" 
        fill="#FFD700" 
        radius={[4, 4, 0, 0]}
        name="Completed"
        className="drop-shadow-sm"
      />
      <Bar 
        dataKey="scheduled" 
        fill="#FFA500" 
        radius={[4, 4, 0, 0]}
        name="Scheduled"
        className="drop-shadow-sm"
      />
    </BarChart>
  </ResponsiveContainer>
);

// Mini Chart Component for Cards
export const MiniLineChart = ({ data, dataKey, color = "#FFD700" }) => (
  <ResponsiveContainer width="100%" height={60}>
    <LineChart data={data}>
      <Line
        type="monotone"
        dataKey={dataKey}
        stroke={color}
        strokeWidth={2}
        dot={false}
        className="drop-shadow-sm"
      />
    </LineChart>
  </ResponsiveContainer>
);