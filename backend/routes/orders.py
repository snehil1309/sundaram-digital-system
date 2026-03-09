from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal, Order, Customer, PointsHistory
from models.schemas import OrderCreate, OrderResponse
import datetime
from typing import Optional
from sqlalchemy import func

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_invoice_number(db: Session):
    year = datetime.datetime.now().year
    count = db.query(func.count(Order.id)).filter(func.extract('year', Order.created_at) == year).scalar()
    return f"SD-{year}-{count + 1:04d}"

@router.post("/order", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    invoice_number = generate_invoice_number(db)
    points_earned = int(order.amount // 10) if order.amount >= 500 else 0

    new_order = Order(
        invoice_number=invoice_number,
        customer_id=order.customer_id,
        order_category=order.order_category,
        description=order.description,
        amount=order.amount,
        points_earned=points_earned
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Update customer spent
    customer.total_spent += order.amount
    
    # Process points if any
    if points_earned > 0:
        customer.total_points += points_earned
        points_history = PointsHistory(
            customer_id=customer.id,
            order_id=new_order.id,
            points_added=points_earned,
            points_redeemed=0,
            balance_points=customer.total_points
        )
        db.add(points_history)

    db.commit()
    db.refresh(new_order)

    return new_order

@router.get("/orders", response_model=list[OrderResponse])
def get_orders(customer_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Order)
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    return query.order_by(Order.created_at.desc()).all()

@router.put("/order/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_data: OrderCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    old_customer_id = order.customer_id
    if order_data.customer_id != old_customer_id:
        # Complex scenario: customer changed. For simplicity, we just reject changing customer on update
        # If we had to handle it, we would adjust both old and new customers.
        raise HTTPException(status_code=400, detail="Cannot change customer ID on update")
        
    customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
    
    old_amount = order.amount
    old_points = order.points_earned
    new_points = int(order_data.amount // 10) if order_data.amount >= 500 else 0
    points_diff = new_points - old_points
    
    order.order_category = order_data.order_category
    order.description = order_data.description
    order.amount = order_data.amount
    order.points_earned = new_points
    
    if customer:
        customer.total_spent += (order.amount - old_amount)
        if points_diff != 0:
            customer.total_points += points_diff
            if customer.total_points < 0:
                customer.total_points = 0
            points_history = PointsHistory(
                customer_id=customer.id,
                order_id=order.id,
                points_added=points_diff if points_diff > 0 else 0,
                points_redeemed=abs(points_diff) if points_diff < 0 else 0,
                balance_points=customer.total_points
            )
            if points_history.balance_points < 0:
                points_history.balance_points = 0
            db.add(points_history)
        # Always log the new balance, even if points don't change
        points_history_balance = PointsHistory(
            customer_id=customer.id,
            order_id=order.id,
            points_added=0,
            points_redeemed=0,
            balance_points=customer.total_points if customer.total_points > 0 else 0
        )
        db.add(points_history_balance)
            
    db.commit()
    db.refresh(order)
    return order

@router.delete("/order/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
    if customer:
        customer.total_spent -= order.amount
        if order.points_earned > 0:
            customer.total_points -= order.points_earned
            if customer.total_points < 0:
                customer.total_points = 0
            points_history = PointsHistory(
                customer_id=customer.id,
                order_id=order.id,
                points_added=0,
                points_redeemed=order.points_earned,
                balance_points=customer.total_points
            )
            if points_history.balance_points < 0:
                points_history.balance_points = 0
            db.add(points_history)
        # Always log the new balance after delete
        points_history_balance = PointsHistory(
            customer_id=customer.id,
            order_id=order.id,
            points_added=0,
            points_redeemed=0,
            balance_points=customer.total_points if customer.total_points > 0 else 0
        )
        db.add(points_history_balance)
            
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
