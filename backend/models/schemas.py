from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CustomerBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    customer_type: str

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    total_spent: float
    total_points: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_id: int
    order_category: str
    description: Optional[str] = None
    amount: float

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    invoice_number: str
    points_earned: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PointsRedeemRequest(BaseModel):
    customer_id: int
    points_to_redeem: int

class PointsHistoryResponse(BaseModel):
    id: int
    customer_id: int
    order_id: Optional[int]
    points_added: int
    points_redeemed: int
    balance_points: int
    date: datetime

    class Config:
        from_attributes = True
