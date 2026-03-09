from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import SessionLocal, Customer, Order, PointsHistory
from sqlalchemy import func
import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/reports/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_customers = db.query(func.count(Customer.id)).scalar()
    total_orders = db.query(func.count(Order.id)).scalar()
    total_revenue = db.query(func.sum(Order.amount)).scalar() or 0.0
    total_points_issued = db.query(func.sum(Customer.total_points)).scalar() or 0
    
    return {
        "total_customers": total_customers,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_points_issued": total_points_issued
    }

@router.get("/reports/sales")
def get_sales_report(period: str = "daily", db: Session = Depends(get_db)):
    now = datetime.datetime.utcnow()
    
    if period == "daily":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "weekly":
        start_date = now - datetime.timedelta(days=7)
    elif period == "monthly":
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        start_date = datetime.datetime(2000, 1, 1) # All time
        
    revenue = db.query(func.sum(Order.amount)).filter(Order.created_at >= start_date).scalar() or 0.0
    
    return {"period": period, "revenue": revenue}

@router.get("/reports/top-customers")
def get_top_customers(db: Session = Depends(get_db)):
    return db.query(Customer).order_by(Customer.total_spent.desc()).limit(10).all()
