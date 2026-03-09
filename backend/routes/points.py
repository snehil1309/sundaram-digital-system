from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal, Customer, PointsHistory
from models.schemas import PointsRedeemRequest, PointsHistoryResponse
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/redeem-points")
def redeem_points(request: PointsRedeemRequest, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == request.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    if customer.total_points < request.points_to_redeem:
        raise HTTPException(status_code=400, detail="Insufficient points balance")
        
    customer.total_points -= request.points_to_redeem
    if customer.total_points < 0:
        customer.total_points = 0

    points_history = PointsHistory(
        customer_id=customer.id,
        points_added=0,
        points_redeemed=request.points_to_redeem,
        balance_points=customer.total_points
    )

    if points_history.balance_points < 0:
        points_history.balance_points = 0

    db.add(points_history)
    db.commit()
    db.refresh(points_history)

    return {"message": "Points redeemed successfully", "remaining_balance": customer.total_points}

@router.get("/points-history/{customer_id}", response_model=List[PointsHistoryResponse])
def get_points_history(customer_id: int, db: Session = Depends(get_db)):
    return db.query(PointsHistory).filter(PointsHistory.customer_id == customer_id).order_by(PointsHistory.date.desc()).all()
