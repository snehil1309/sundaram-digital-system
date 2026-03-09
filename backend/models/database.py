from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime
import os

# Create database directory if it doesn't exist
os.makedirs(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database")), exist_ok=True)
DATABASE_URL = "sqlite:///" + os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database", "database.db"))

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, index=True)
    email = Column(String)
    address = Column(String)
    customer_type = Column(String) # Individual / Organization
    total_spent = Column(Float, default=0.0)
    total_points = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    orders = relationship("Order", back_populates="customer")
    points_history = relationship("PointsHistory", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_category = Column(String)
    description = Column(String)
    amount = Column(Float)
    points_earned = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    customer = relationship("Customer", back_populates="orders")
    points_history = relationship("PointsHistory", back_populates="order")

class PointsHistory(Base):
    __tablename__ = "points_history"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    points_added = Column(Integer, default=0)
    points_redeemed = Column(Integer, default=0)
    balance_points = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    
    customer = relationship("Customer", back_populates="points_history")
    order = relationship("Order", back_populates="points_history")

class OrderCategory(Base):
    __tablename__ = "order_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, unique=True)

Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    categories = [
        "Xerox", "Printing", "Binding", "Book Making", "Flex Banner",
        "Brand Board", "Graphic Designing", "Foam Sheet Printing",
        "MDF Sheet Printing", "Cardboard Printing", "Lamination", "Other"
    ]
    for cat in categories:
        existing = db.query(OrderCategory).filter(OrderCategory.category_name == cat).first()
        if not existing:
            new_cat = OrderCategory(category_name=cat)
            db.add(new_cat)
    db.commit()
    db.close()

init_db()
