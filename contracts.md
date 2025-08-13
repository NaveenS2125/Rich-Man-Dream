# Rich Man Dream CRM - Backend Integration Contracts

## API Endpoints to Implement

### 1. Authentication APIs
```
POST /api/auth/login
- Body: { email, password }
- Response: { success: boolean, token?: string, user?: UserObject, error?: string }

POST /api/auth/logout
- Headers: Authorization: Bearer <token>
- Response: { success: boolean }

GET /api/auth/me
- Headers: Authorization: Bearer <token>
- Response: { user: UserObject }
```

### 2. Leads Management APIs
```
GET /api/leads
- Query params: ?search, ?status, ?page, ?limit
- Response: { leads: Lead[], total: number, page: number }

GET /api/leads/:id
- Response: { lead: Lead }

POST /api/leads
- Body: { name, email, phone, status, source, budget, propertyType, notes }
- Response: { lead: Lead }

PUT /api/leads/:id
- Body: Partial<Lead>
- Response: { lead: Lead }

DELETE /api/leads/:id
- Response: { success: boolean }
```

### 3. Calls Management APIs
```
GET /api/calls
- Query params: ?leadId, ?agent, ?page, ?limit
- Response: { calls: Call[], total: number }

POST /api/calls
- Body: { leadId, type, duration, notes, status }
- Response: { call: Call }
```

### 4. Viewings Management APIs
```
GET /api/viewings
- Query params: ?date, ?status, ?agent
- Response: { viewings: Viewing[] }

POST /api/viewings
- Body: { property, address, date, time, leadName, agent, price, type }
- Response: { viewing: Viewing }

PUT /api/viewings/:id
- Body: Partial<Viewing>
- Response: { viewing: Viewing }
```

### 5. Sales Tracker APIs
```
GET /api/sales
- Response: { sales: Sale[] }

PUT /api/sales/:id
- Body: { stage, probability, expectedClose }
- Response: { sale: Sale }
```

### 6. Dashboard Analytics APIs
```
GET /api/dashboard/stats
- Response: { totalLeads, hotLeads, scheduledViewings, activeSales, closedDealsThisMonth, totalRevenue, monthlyGrowth }

GET /api/dashboard/charts
- Response: { salesChart, leadsChart, statusDistribution, viewingsChart }
```

## Data Models (MongoDB Collections)

### User Model
```javascript
{
  _id: ObjectId,
  name: String,
  email: String (unique),
  password: String (hashed),
  role: String (admin|agent|viewer),
  avatar: String,
  createdAt: Date,
  updatedAt: Date
}
```

### Lead Model
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  phone: String,
  status: String (hot|warm|cold),
  source: String,
  budget: String,
  propertyType: String,
  assignedAgent: String,
  assignedAgentId: ObjectId,
  notes: String,
  createdAt: Date,
  updatedAt: Date,
  lastContact: Date
}
```

### Call Model
```javascript
{
  _id: ObjectId,
  leadId: ObjectId,
  leadName: String,
  agent: String,
  agentId: ObjectId,
  type: String (inbound|outbound),
  duration: String,
  date: String,
  time: String,
  status: String (completed|missed),
  notes: String,
  createdAt: Date
}
```

### Viewing Model
```javascript
{
  _id: ObjectId,
  property: String,
  address: String,
  date: String,
  time: String,
  leadName: String,
  leadId: ObjectId,
  agent: String,
  agentId: ObjectId,
  status: String (scheduled|completed|cancelled),
  price: String,
  type: String,
  createdAt: Date
}
```

### Sale Model
```javascript
{
  _id: ObjectId,
  leadId: ObjectId,
  leadName: String,
  property: String,
  agent: String,
  agentId: ObjectId,
  stage: String (contacted|viewed|negotiation|closed),
  value: String,
  probability: Number,
  expectedClose: String,
  lastActivity: Date,
  createdAt: Date
}
```

## Mock Data Replacement Plan

### Frontend Files to Update:
1. **mockData.js** - Remove after backend integration
2. **AuthContext.js** - Replace mock login with real API calls
3. **Dashboard.js** - Replace mockDashboardStats and mockChartData with API calls
4. **App.js** - Update API base URL usage

### Mock Data Currently Used:
- `mockLeads` → GET /api/leads
- `mockCalls` → GET /api/calls  
- `mockViewings` → GET /api/viewings
- `mockSales` → GET /api/sales
- `mockEmails` → GET /api/emails (future)
- `mockDashboardStats` → GET /api/dashboard/stats
- `mockChartData` → GET /api/dashboard/charts
- `mockUsers` → GET /api/users (admin only)

## Authentication Integration
1. Update AuthContext to call `/api/auth/login`
2. Store JWT token in localStorage
3. Add Authorization header to all API requests
4. Implement token refresh logic
5. Handle authentication errors

## Error Handling
- Global error interceptor for API calls
- Toast notifications for errors
- Loading states for all API operations
- Form validation on frontend and backend

## Security Implementation
- Password hashing with bcrypt
- JWT token validation middleware
- Role-based access control
- Input validation and sanitization
- CORS configuration

This contract ensures seamless integration between the existing frontend mock implementation and the new backend APIs.