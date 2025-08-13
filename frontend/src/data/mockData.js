// Mock data for Real Estate CRM "Rich Man Dream"

export const mockLeads = [
  {
    id: "1",
    name: "John Williams",
    email: "john.williams@email.com",
    phone: "+1 (555) 123-4567",
    status: "hot",
    source: "Website",
    budget: "$850,000",
    propertyType: "Luxury Condo",
    assignedAgent: "Sarah Johnson",
    createdAt: "2024-01-15",
    lastContact: "2024-01-20",
    notes: "Interested in downtown luxury condos. Prefers high-rise with city view.",
    viewingHistory: [
      { date: "2024-01-18", property: "Skyline Tower #2501", status: "completed" }
    ]
  },
  {
    id: "2",
    name: "Emma Rodriguez",
    email: "emma.rodriguez@email.com",
    phone: "+1 (555) 234-5678",
    status: "warm",
    source: "Referral",
    budget: "$1,200,000",
    propertyType: "Single Family Home",
    assignedAgent: "Michael Chen",
    createdAt: "2024-01-12",
    lastContact: "2024-01-19",
    notes: "Looking for family home in suburbs. Needs 4+ bedrooms.",
    viewingHistory: [
      { date: "2024-01-16", property: "Oak Street Villa", status: "completed" },
      { date: "2024-01-22", property: "Maple Ridge Estate", status: "scheduled" }
    ]
  },
  {
    id: "3",
    name: "David Thompson",
    email: "david.thompson@email.com",
    phone: "+1 (555) 345-6789",
    status: "cold",
    source: "Social Media",
    budget: "$650,000",
    propertyType: "Townhouse",
    assignedAgent: "Lisa Park",
    createdAt: "2024-01-10",
    lastContact: "2024-01-17",
    notes: "First-time buyer. Needs guidance on financing options.",
    viewingHistory: []
  }
];

export const mockCalls = [
  {
    id: "1",
    leadId: "1",
    leadName: "John Williams",
    agent: "Sarah Johnson",
    type: "outbound",
    duration: "12:34",
    date: "2024-01-20",
    time: "2:30 PM",
    status: "completed",
    notes: "Discussed viewing schedule for luxury condos. Very interested in Skyline Tower."
  },
  {
    id: "2",
    leadId: "2",
    leadName: "Emma Rodriguez",
    agent: "Michael Chen",
    type: "inbound",
    duration: "8:15",
    date: "2024-01-19",
    time: "10:15 AM",
    status: "completed",
    notes: "Called to reschedule viewing. Prefers weekend appointments."
  },
  {
    id: "3",
    leadId: "3",
    leadName: "David Thompson",
    agent: "Lisa Park",
    type: "outbound",
    duration: "0:00",
    date: "2024-01-18",
    time: "4:45 PM",
    status: "missed",
    notes: "No answer. Left voicemail about financing pre-approval."
  }
];

export const mockViewings = [
  {
    id: "1",
    property: "Skyline Tower #2501",
    address: "123 Downtown Ave, Suite 2501",
    date: "2024-01-25",
    time: "2:00 PM",
    leadName: "John Williams",
    agent: "Sarah Johnson",
    status: "scheduled",
    price: "$850,000",
    type: "Luxury Condo"
  },
  {
    id: "2",
    property: "Maple Ridge Estate",
    address: "456 Maple Ridge Dr",
    date: "2024-01-22",
    time: "11:00 AM",
    leadName: "Emma Rodriguez",
    agent: "Michael Chen",
    status: "scheduled",
    price: "$1,200,000",
    type: "Single Family Home"
  },
  {
    id: "3",
    property: "Oak Street Villa",
    address: "789 Oak Street",
    date: "2024-01-16",
    time: "3:30 PM",
    leadName: "Emma Rodriguez",
    agent: "Michael Chen",
    status: "completed",
    price: "$1,150,000",
    type: "Single Family Home"
  }
];

export const mockSales = [
  {
    id: "1",
    leadId: "1",
    leadName: "John Williams",
    property: "Skyline Tower #2501",
    agent: "Sarah Johnson",
    stage: "negotiation",
    value: "$850,000",
    probability: 75,
    expectedClose: "2024-02-15",
    lastActivity: "2024-01-20"
  },
  {
    id: "2",
    leadId: "2",
    leadName: "Emma Rodriguez",
    property: "Maple Ridge Estate",
    agent: "Michael Chen",
    stage: "viewed",
    value: "$1,200,000",
    probability: 45,
    expectedClose: "2024-03-01",
    lastActivity: "2024-01-19"
  }
];

export const mockEmails = [
  {
    id: "1",
    leadId: "1",
    leadName: "John Williams",
    subject: "Re: Skyline Tower Viewing",
    preview: "Thank you for showing me the property. I'm very interested in moving forward...",
    date: "2024-01-20",
    time: "3:45 PM",
    type: "received",
    status: "read"
  },
  {
    id: "2",
    leadId: "2",
    leadName: "Emma Rodriguez",
    subject: "Financing Options Discussion",
    preview: "I've reviewed the financing options we discussed. Could we schedule a call to...",
    date: "2024-01-19",
    time: "11:30 AM",
    type: "received",
    status: "unread"
  }
];

export const mockDashboardStats = {
  totalLeads: 156,
  hotLeads: 23,
  scheduledViewings: 12,
  activeSales: 8,
  closedDealsThisMonth: 3,
  totalRevenue: "$2,450,000",
  monthlyGrowth: 12.5
};

export const mockChartData = {
  salesChart: [
    { month: "Jan", sales: 2450000 },
    { month: "Feb", sales: 1890000 },
    { month: "Mar", sales: 3120000 },
    { month: "Apr", sales: 2780000 },
    { month: "May", sales: 3450000 },
    { month: "Jun", sales: 2890000 }
  ],
  leadsChart: [
    { week: "W1", leads: 45 },
    { week: "W2", leads: 52 },
    { week: "W3", leads: 38 },
    { week: "W4", leads: 61 }
  ],
  statusDistribution: [
    { name: "Hot", value: 23, color: "#FFD700" },
    { name: "Warm", value: 45, color: "#FFA500" },
    { name: "Cold", value: 88, color: "#CD853F" }
  ],
  viewingsChart: [
    { day: "Mon", completed: 3, scheduled: 5 },
    { day: "Tue", completed: 4, scheduled: 3 },
    { day: "Wed", completed: 2, scheduled: 6 },
    { day: "Thu", completed: 5, scheduled: 4 },
    { day: "Fri", completed: 3, scheduled: 7 },
    { day: "Sat", completed: 8, scheduled: 9 },
    { day: "Sun", completed: 6, scheduled: 8 }
  ]
};

export const mockUsers = [
  {
    id: "1",
    name: "Sarah Johnson",
    role: "admin",
    email: "sarah.johnson@richmansdream.com",
    avatar: "https://images.unsplash.com/photo-1494790108755-2616b9997701?w=100&h=100&fit=crop&crop=face",
    activeLeads: 12,
    closedDeals: 3
  },
  {
    id: "2",
    name: "Michael Chen",
    role: "agent",
    email: "michael.chen@richmansdream.com",
    avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face",
    activeLeads: 8,
    closedDeals: 2
  },
  {
    id: "3",
    name: "Lisa Park",
    role: "agent",
    email: "lisa.park@richmansdream.com",
    avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop&crop=face",
    activeLeads: 15,
    closedDeals: 1
  }
];