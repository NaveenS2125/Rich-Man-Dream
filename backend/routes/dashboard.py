from fastapi import APIRouter, Depends
from database.connection import leads_collection, calls_collection, viewings_collection, sales_collection
from auth.middleware import get_current_user_data
from datetime import datetime, timedelta
from bson import ObjectId

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
async def get_dashboard_stats(user_data: dict = Depends(get_current_user_data)):
    """Get dashboard statistics."""
    
    # Role-based filtering
    base_filter = {}
    if user_data.get("role") == "agent":
        agent_id = ObjectId(user_data.get("user_id"))
        base_filter = {"agent_id": agent_id}
    
    # Get current month start
    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)
    
    # Count total leads
    leads_filter = {}
    if user_data.get("role") == "agent":
        leads_filter["assigned_agent_id"] = ObjectId(user_data.get("user_id"))
    
    total_leads = await leads_collection.count_documents(leads_filter)
    
    # Count hot leads
    hot_leads_filter = {**leads_filter, "status": "hot"}
    hot_leads = await leads_collection.count_documents(hot_leads_filter)
    
    # Count scheduled viewings
    viewings_filter = {**base_filter, "status": "scheduled"}
    scheduled_viewings = await viewings_collection.count_documents(viewings_filter)
    
    # Count active sales (not closed)
    sales_filter = {**base_filter, "stage": {"$ne": "closed"}}
    active_sales = await sales_collection.count_documents(sales_filter)
    
    # Count closed deals this month
    closed_deals_filter = {
        **base_filter,
        "stage": "closed",
        "last_activity": {"$gte": month_start}
    }
    closed_deals_this_month = await sales_collection.count_documents(closed_deals_filter)
    
    # Calculate total revenue from closed deals this month
    pipeline = [
        {"$match": closed_deals_filter},
        {
            "$addFields": {
                "value_numeric": {
                    "$toDouble": {
                        "$replaceAll": {
                            "input": {"$replaceAll": {"input": "$value", "find": "$", "replacement": ""}},
                            "find": ",",
                            "replacement": ""
                        }
                    }
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "total_revenue": {"$sum": "$value_numeric"}
            }
        }
    ]
    
    revenue_result = await sales_collection.aggregate(pipeline).to_list(1)
    total_revenue = revenue_result[0]["total_revenue"] if revenue_result else 0
    
    # Calculate monthly growth (mock for now)
    monthly_growth = 12.5  # This would require historical data comparison
    
    return {
        "totalLeads": total_leads,
        "hotLeads": hot_leads,
        "scheduledViewings": scheduled_viewings,
        "activeSales": active_sales,
        "closedDealsThisMonth": closed_deals_this_month,
        "totalRevenue": f"${total_revenue:,.0f}",
        "monthlyGrowth": monthly_growth
    }


@router.get("/charts")
async def get_dashboard_charts(user_data: dict = Depends(get_current_user_data)):
    """Get chart data for dashboard."""
    
    # Role-based filtering
    base_filter = {}
    if user_data.get("role") == "agent":
        agent_id = ObjectId(user_data.get("user_id"))
        base_filter = {"agent_id": agent_id}
    
    # Sales chart data (last 6 months)
    sales_chart = []
    for i in range(6):
        month_start = datetime(datetime.utcnow().year, datetime.utcnow().month - i, 1)
        if month_start.month <= 0:
            month_start = datetime(month_start.year - 1, month_start.month + 12, 1)
        
        next_month = month_start.replace(month=month_start.month + 1) if month_start.month < 12 else month_start.replace(year=month_start.year + 1, month=1)
        
        # Get closed deals for the month
        sales_filter = {
            **base_filter,
            "stage": "closed",
            "last_activity": {"$gte": month_start, "$lt": next_month}
        }
        
        # Calculate revenue for the month
        pipeline = [
            {"$match": sales_filter},
            {
                "$addFields": {
                    "value_numeric": {
                        "$toDouble": {
                            "$replaceAll": {
                                "input": {"$replaceAll": {"input": "$value", "find": "$", "replacement": ""}},
                                "find": ",",
                                "replacement": ""
                            }
                        }
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$value_numeric"}
                }
            }
        ]
        
        result = await sales_collection.aggregate(pipeline).to_list(1)
        monthly_revenue = result[0]["total"] if result else 0
        
        sales_chart.insert(0, {
            "month": month_start.strftime("%b"),
            "sales": int(monthly_revenue)
        })
    
    # Leads chart data (last 4 weeks)
    leads_chart = []
    for i in range(4):
        week_start = datetime.utcnow() - timedelta(weeks=i, days=datetime.utcnow().weekday())
        week_end = week_start + timedelta(days=7)
        
        leads_filter = {}
        if user_data.get("role") == "agent":
            leads_filter["assigned_agent_id"] = ObjectId(user_data.get("user_id"))
        
        leads_filter["created_at"] = {"$gte": week_start, "$lt": week_end}
        
        week_leads = await leads_collection.count_documents(leads_filter)
        
        leads_chart.insert(0, {
            "week": f"W{4-i}",
            "leads": week_leads
        })
    
    # Status distribution
    leads_filter = {}
    if user_data.get("role") == "agent":
        leads_filter["assigned_agent_id"] = ObjectId(user_data.get("user_id"))
    
    hot_count = await leads_collection.count_documents({**leads_filter, "status": "hot"})
    warm_count = await leads_collection.count_documents({**leads_filter, "status": "warm"})
    cold_count = await leads_collection.count_documents({**leads_filter, "status": "cold"})
    
    status_distribution = [
        {"name": "Hot", "value": hot_count, "color": "#FFD700"},
        {"name": "Warm", "value": warm_count, "color": "#FFA500"},
        {"name": "Cold", "value": cold_count, "color": "#CD853F"}
    ]
    
    # Viewings chart data (last 7 days)
    viewings_chart = []
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    for i, day in enumerate(days):
        day_start = datetime.utcnow() - timedelta(days=6-i)
        day_start = day_start.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        completed_filter = {
            **base_filter,
            "status": "completed",
            "created_at": {"$gte": day_start, "$lt": day_end}
        }
        
        scheduled_filter = {
            **base_filter,
            "status": "scheduled",
            "created_at": {"$gte": day_start, "$lt": day_end}
        }
        
        completed = await viewings_collection.count_documents(completed_filter)
        scheduled = await viewings_collection.count_documents(scheduled_filter)
        
        viewings_chart.append({
            "day": day,
            "completed": completed,
            "scheduled": scheduled
        })
    
    return {
        "salesChart": sales_chart,
        "leadsChart": leads_chart,
        "statusDistribution": status_distribution,
        "viewingsChart": viewings_chart
    }